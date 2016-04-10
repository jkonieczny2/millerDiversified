# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Table format resource printer."""

import cStringIO
import json
import operator

from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_attr
from googlecloudsdk.core.resource import resource_printer_base
from googlecloudsdk.core.resource import resource_transform


# Table output column padding.
_TABLE_COLUMN_PAD = 2


def _Stringify(value):  # pylint: disable=invalid-name
  """Represents value as a JSON string if it's not a string."""
  if value is None:
    return ''
  elif isinstance(value, (basestring, console_attr.Colorizer)):
    return value
  elif isinstance(value, float):
    return resource_transform.TransformFloat(value)
  elif hasattr(value, '__str__'):
    return unicode(value)
  else:
    return json.dumps(value, sort_keys=True)


class _Justify(object):
  """Represents a unicode object for justification using display width.

  Attributes:
    _adjust: The justification width adjustment. The builtin justification
      functions use len() but unicode data requires console_attr.DisplayWidth().
    _string: The unicode string to justify.
  """

  def __init__(self, attr, string):
    self._adjust = attr.DisplayWidth(string) - len(string)
    self._string = string

  def ljust(self, width):
    return self._string.ljust(width - self._adjust)

  def rjust(self, width):
    return self._string.rjust(width - self._adjust)

  def center(self, width):
    return self._string.center(width - self._adjust)


class SubFormat(object):
  """A sub format object.

  Attributes:
    index: The parent column index.
    printer: The nested printer object.
    out: The nested printer output stream.
    rows: The nested format aggregate rows if the parent has no columns.
  """

  def __init__(self, index, printer, out):
    self.index = index
    self.printer = printer
    self.out = out
    self.rows = []


class TablePrinter(resource_printer_base.ResourcePrinter):
  """A printer for printing human-readable tables.

  Aligned left-adjusted columns with optional title, column headings and
  sorting. This format requires a projection to define the table columns. The
  default column headings are the disambiguated right hand components of the
  column keys in ANGRY_SNAKE_CASE. For example, the projection keys
  (first.name, last.name) produce the default column heading
  ('NAME', 'LAST_NAME').

  If *--page-size*=_N_ is specified then output is grouped into tables with
  at most _N_ rows. Headings, alignment and sorting are done per-page. The
  title, if any, is printed before the first table. The legend, if any, is
  printed after the last table.

  Printer attributes:
    box: Prints a box around the entire table and each cell, including the
      title if any.
    empty-legend=_SENTENCES_: Prints _SENTENCES_ to the *status* logger if there
      are no items. The default *empty-legend* is "Listed 0 items.".
      *no-empty-legend* disables the default.
    format=_FORMAT-STRING_: Prints the key data indented by 4 spaces using
      _FORMAT-STRING_ which can reference any of the supported formats.
    no-heading: Disables the column headings.
    legend=_SENTENCES_: Prints _SENTENCES_ to the *out* logger after the last
      item if there is at least one item.
    legend-log=_TYPE_: Prints the legend to the _TYPE_ logger instead of the
      default.  _TYPE_ may be: *out* (the default), *status* (standard error),
      *debug*, *info*, *warn*, or *error*.
    pad=N: Sets the column horizontal pad to _N_ spaces. The default is 1 for
      box, 2 otherwise.
    title=_TITLE_: Prints a centered _TITLE_ at the top of the table, within
      the table box if *box* is enabled.

  Attributes:
    _page_count: The output page count, incremented before each page.
    _rows_per_page: The number of rows in each resource page. 0 for no paging.
    _rows: The list of all resource columns indexed by row.
  """

  # TODO(user): Drop TablePrinter._rows_per_page 3Q2016.

  def __init__(self, *args, **kwargs):
    """Creates a new TablePrinter."""
    self._rows = []
    self._nest = []
    super(TablePrinter, self).__init__(*args, by_columns=True,
                                       non_empty_projection_required=True,
                                       **kwargs)
    encoding = None
    for name in ['ascii', 'utf8', 'win']:
      if name in self.attributes:
        encoding = name
        break
    if not self._console_attr:
      self._console_attr = console_attr.GetConsoleAttr(encoding=encoding,
                                                       out=self._out)
    self._rows_per_page = self.attributes.get('page', 0)
    if self._rows_per_page:
      log.warn('The [page=N] printer attribute is deprecated. '
               'Use the --page-size=N flag instead.')
    self._page_count = 0

    # Check for subformat columns.
    self._subformats = []
    has_subformats = False
    self._aggregate = True
    if self.column_attributes:
      for col in self.column_attributes.Columns():
        if col.attribute.subformat:
          has_subformats = True
        else:
          self._aggregate = False
      index = 0
      for col in self.column_attributes.Columns():
        if col.attribute.subformat:
          # This initializes a Printer to a string stream.
          out = self._out if self._aggregate else cStringIO.StringIO()
          printer = self.Printer(col.attribute.subformat, out=out,
                                 console_attr=self._console_attr)
        else:
          out = None
          printer = None
        self._subformats.append(SubFormat(index, printer, out))
        index += 1
    if not has_subformats:
      self._subformats = None
      self._aggregate = False

  def _AddRecord(self, record, delimit=True):
    """Adds a list of columns. Output delayed until Finish().

    Args:
      record: A JSON-serializable object.
      delimit: Prints resource delimiters if True.
    """
    if self._rows_per_page and len(self._rows) >= self._rows_per_page:
      self.Page()
    if self._subformats and not self._aggregate:
      row = []
      for subformat in self._subformats:
        if not subformat.printer:
          row.append(record[subformat.index])
      self._rows.append(row)
      self._nest.append(record)
    else:
      self._rows.append(record)

  def Finish(self, last_page=True):
    """Prints the table.

    Args:
      last_page: True if this is the last resource page.
    """
    if not self._rows:
      # Table is empty.
      if last_page:
        # There might be an empty legend.
        self.AddLegend()
      return

    if self._aggregate:
      # No parent columns, only nested formats. Aggregate each subformat
      # column to span all records.
      for subformat in self._subformats:
        for row in self._rows:
          subformat.printer.Print(row[subformat.index], intermediate=True)
        subformat.printer.Finish()
      if last_page:
        self.AddLegend()
      return

    # Border box decorations.
    if 'box' in self.attributes:
      box = self._console_attr.GetBoxLineCharacters()
      table_column_pad = 1
    else:
      box = None
      table_column_pad = self.attributes.get('pad', _TABLE_COLUMN_PAD)
      if self._page_count > 1:
        self._out.write('\n')

    # Determine the max column widths of heading + rows
    rows = [[_Stringify(cell) for cell in row] for row in self._rows]
    self._rows = []
    heading = []
    if 'no-heading' not in self.attributes:
      if self._heading:
        labels = self._heading
      elif self.column_attributes:
        labels = self.column_attributes.Labels()
      else:
        labels = None
      if labels:
        if self._subformats:
          cells = []
          for subformat in self._subformats:
            if not subformat.printer and subformat.index < len(labels):
              cells.append(_Stringify(labels[subformat.index]))
          heading = [cells]
        else:
          heading = [[_Stringify(cell) for cell in labels]]
    col_widths = [0] * max(len(x) for x in rows + heading)
    for row in rows + heading:
      for i in range(len(row)):
        col_widths[i] = max(col_widths[i],
                            self._console_attr.DisplayWidth(row[i]))

    # Print the title if specified.
    title = self.attributes.get('title') if self._page_count <= 1 else None
    if title is not None:
      if box:
        line = box.dr
      width = 0
      sep = 2
      for i in range(len(col_widths)):
        width += col_widths[i]
        if box:
          line += box.h * (col_widths[i] + sep)
        sep = 3
      if width < self._console_attr.DisplayWidth(title):
        # Title is wider than the table => pad each column to make room.
        pad = ((self._console_attr.DisplayWidth(title) + len(col_widths) - 1) /
               len(col_widths))
        width += len(col_widths) * pad
        if box:
          line += box.h * len(col_widths) * pad
        for i in range(len(col_widths)):
          col_widths[i] += pad
      if box:
        width += 3 * len(col_widths) - 1
        line += box.dl
        self._out.write(line)
        self._out.write('\n')
        line = box.v + title.center(width) + box.v
      else:
        line = title.center(width)
      self._out.write(line)
      self._out.write('\n')

    # Set up box borders.
    if box:
      t_sep = box.vr if title else box.dr
      m_sep = box.vr
      b_sep = box.ur
      t_rule = ''
      m_rule = ''
      b_rule = ''
      for i in range(len(col_widths)):
        cell = box.h * (col_widths[i] + 2)
        t_rule += t_sep + cell
        t_sep = box.hd
        m_rule += m_sep + cell
        m_sep = box.vh
        b_rule += b_sep + cell
        b_sep = box.hu
      t_rule += box.vl if title else box.dl
      m_rule += box.vl
      b_rule += box.ul
      self._out.write(t_rule)
      self._out.write('\n')
      if heading:
        line = []
        row = heading[0]
        heading = []
        for i in range(len(row)):
          line.append(box.v)
          line.append(row[i].center(col_widths[i]))
        line.append(box.v)
        self._out.write(u' '.join(line))
        self._out.write('\n')
        self._out.write(m_rule)
        self._out.write('\n')

    # Sort by columns if requested.
    if self.column_attributes:
      # Order() is a list of (key,reverse) tuples from highest to lowest key
      # precedence. This loop partitions the keys into groups with the same
      # reverse value. The groups are then applied in reverse order to maintain
      # the original precedence.
      groups = []  # [(keys, reverse)] LIFO to preserve precedence
      keys = []  # keys for current group
      for key_index, key_reverse in self.column_attributes.Order():
        if not keys:
          # This only happens the first time through the loop.
          reverse = key_reverse
        if reverse != key_reverse:
          groups.insert(0, (keys, reverse))
          keys = []
          reverse = key_reverse
        keys.append(key_index)
      if keys:
        groups.insert(0, (keys, reverse))
      for keys, reverse in groups:
        rows = sorted(rows, key=operator.itemgetter(*keys), reverse=reverse)
      align = self.column_attributes.Alignments()
    else:
      align = None

    # Print the left-adjusted columns with space stripped from rightmost column.
    # We must flush directly to the output just in case there is a Windows-like
    # colorizer. This complicates the trailing space logic.
    first = True
    for row in heading + rows:
      if first:
        first = False
      elif box and self._subformats:
        self._out.write(t_rule)
        self._out.write('\n')
      pad = 0
      for i in range(len(row)):
        if box:
          self._out.write(box.v + ' ')
          width = col_widths[i]
        elif i < len(row) - 1:
          width = col_widths[i]
        else:
          width = 0
        justify = align[i] if align else lambda s, w: s.ljust(w)
        cell = row[i]
        if isinstance(cell, console_attr.Colorizer):
          if pad:
            self._out.write(' ' * pad)
            pad = 0
          # pylint: disable=cell-var-from-loop
          cell.Render(justify=lambda s: justify(s, width))
          if box:
            self._out.write(' ' * table_column_pad)
          else:
            pad = table_column_pad
        else:
          value = justify(_Justify(self._console_attr, cell), width)
          if box:
            self._out.write(value)
            self._out.write(' ' * table_column_pad)
          elif value.strip():
            if pad:
              self._out.write(' ' * pad)
              pad = 0
            stripped = value.rstrip()
            self._out.write(stripped)
            pad = (table_column_pad + self._console_attr.DisplayWidth(value) -
                   self._console_attr.DisplayWidth(stripped))
          else:
            pad += table_column_pad + self._console_attr.DisplayWidth(value)
      if box:
        self._out.write(box.v)
      if self._nest:
        self._out.write('\n')
        if heading:
          heading = []
          continue
        if box:
          self._out.write(b_rule)
          self._out.write('\n')
        r = self._nest.pop()
        for subformat in self._subformats:
          if subformat.printer:
            # Indent the nested printer lines.
            subformat.printer.Print(r[subformat.index])
            nested_output = subformat.out.getvalue()
            for line in nested_output.split('\n')[:-1]:
              self._out.write('    ' + line + '\n')
            # Rewind the output buffer.
            subformat.out.truncate(0)
      else:
        self._out.write('\n')
    if box and not self._subformats:
      self._out.write(b_rule)
      self._out.write('\n')

    # Print the legend if any.
    if last_page:
      self.AddLegend()

  def Page(self):
    """Flushes the current resource page output."""
    self._page_count += 1
    self.Finish(last_page=False)
    self._rows = []
    self._nest = []
