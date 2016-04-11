#pdftotext in_pdf, out_text, -layout -f 2

import re
import os

os.chdir("/home/josh/projects/miller_diversified")

out = 'clean_csi_codes.txt'
infile = 'csi_masterformat_50.txt'

def starts_with_code(string):
	pat = re.compile(r"\d{2} \d{2} \d{2}")

	if re.match(pat, string):
		return True
	else:
		return False

def has_chars(string):
	pat = re.compile(r'[^\s]+')

	if re.search(pat, string):
		return True
	else:
		return False

old_line=''
with open(infile, 'r') as f, open(out, 'w') as outfile:
	for line in f:
		stripped_line = line.lstrip() #Strip leading whitespace
		stripped_line = re.sub(" {5,}","\t",stripped_line)

		if starts_with_code(old_line) and (not starts_with_code(stripped_line) and has_chars(stripped_line)):
			if old_line.endswith("-"):
				outfile.write(old_line.rstrip("\n") + stripped_line)
			else:
				outfile.write(old_line.rstrip("\n") + " " + stripped_line)
		elif starts_with_code(old_line) and (starts_with_code(stripped_line) or not has_chars(stripped_line)):
			outfile.write(old_line)

		old_line = stripped_line


