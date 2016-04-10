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
"""Command for getting autoscalers."""

# TODO(user): Rename get command to describe to be consistent with compute.

from googlecloudsdk.api_lib.compute import autoscaler_utils as util
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import exceptions as calliope_exceptions
from googlecloudsdk.core import log
from googlecloudsdk.third_party.apitools.base.py import exceptions


def UtilizationTargetTypeForItem(item):
  if hasattr(item, 'utilizationTargetType') and item.utilizationTargetType:
    return item.utilizationTargetType
  return ''


class GetAutoscaler(base_classes.BaseCommand):
  """Get Autoscaler instances."""

  @staticmethod
  def Args(parser):
    parser.add_argument('name', help='Autoscaler name.')

  def Run(self, args):
    log.warn('Please use instead [gcloud compute instance-groups '
             'managed describe].')
    client = self.context['autoscaler-client']
    messages = self.context['autoscaler_messages_module']
    resources = self.context['autoscaler_resources']
    autoscaler_ref = resources.Parse(
        args.name, collection='autoscaler.autoscalers')
    request = messages.AutoscalerAutoscalersGetRequest()
    request.project = autoscaler_ref.project
    request.zone = autoscaler_ref.zone
    request.autoscaler = autoscaler_ref.autoscaler

    try:
      return client.autoscalers.Get(request)

    except exceptions.HttpError as error:
      raise calliope_exceptions.HttpException(util.GetErrorMessage(error))

  def Display(self, unused_args, result):
    self.format(result)
