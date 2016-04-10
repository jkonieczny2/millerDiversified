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
"""Command for describing target SSL proxies."""
from googlecloudsdk.api_lib.compute import base_classes


class Describe(base_classes.GlobalDescriber):
  """Display detailed information about a target SSL proxy."""

  @staticmethod
  def Args(parser):
    base_classes.GlobalDescriber.Args(
        parser, 'compute.targetSslProxies')
    base_classes.AddFieldsFlag(parser, 'targetSslProxies')

  @property
  def service(self):
    return self.compute.targetSslProxies

  @property
  def resource_type(self):
    return 'targetSslProxies'


Describe.detailed_help = {
    'brief': 'Display detailed information about a target SSL proxy',
    'DESCRIPTION': """\
        *{command}* displays all data associated with a target SSL proxy
        in a project.
        """,
}
