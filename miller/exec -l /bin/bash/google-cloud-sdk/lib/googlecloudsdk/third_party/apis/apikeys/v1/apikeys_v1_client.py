"""Generated client library for apikeys version v1."""
# NOTE: This file is autogenerated and should not be edited by hand.
from googlecloudsdk.third_party.apitools.base.py import base_api
from googlecloudsdk.third_party.apis.apikeys.v1 import apikeys_v1_messages as messages


class ApikeysV1(base_api.BaseApiClient):
  """Generated client library for service apikeys version v1."""

  MESSAGES_MODULE = messages

  _PACKAGE = u'apikeys'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform', u'https://www.googleapis.com/auth/service.management']
  _VERSION = u'v1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'ApikeysV1'
  _URL_VERSION = u'v1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None):
    """Create a new apikeys handle."""
    url = url or u'https://apikeys.googleapis.com/'
    super(ApikeysV1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers)
    self.projects_apiKeys = self.ProjectsApiKeysService(self)
    self.projects_deletedApiKeys = self.ProjectsDeletedApiKeysService(self)
    self.projects = self.ProjectsService(self)

  class ProjectsApiKeysService(base_api.BaseApiService):
    """Service class for the projects_apiKeys resource."""

    _NAME = u'projects_apiKeys'

    def __init__(self, client):
      super(ApikeysV1.ProjectsApiKeysService, self).__init__(client)
      self._method_configs = {
          'BatchDelete': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'apikeys.projects.apiKeys.batchDelete',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[u'keyIds'],
              relative_path=u'v1/projects/{projectId}/apiKeys:batchDelete',
              request_field='',
              request_type_name=u'ApikeysProjectsApiKeysBatchDeleteRequest',
              response_type_name=u'Empty',
              supports_download=False,
          ),
          'Create': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'apikeys.projects.apiKeys.create',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[],
              relative_path=u'v1/projects/{projectId}/apiKeys',
              request_field=u'apiKey',
              request_type_name=u'ApikeysProjectsApiKeysCreateRequest',
              response_type_name=u'ApiKey',
              supports_download=False,
          ),
          'Delete': base_api.ApiMethodInfo(
              http_method=u'DELETE',
              method_id=u'apikeys.projects.apiKeys.delete',
              ordered_params=[u'projectId', u'keyId'],
              path_params=[u'keyId', u'projectId'],
              query_params=[],
              relative_path=u'v1/projects/{projectId}/apiKeys/{keyId}',
              request_field='',
              request_type_name=u'ApikeysProjectsApiKeysDeleteRequest',
              response_type_name=u'Empty',
              supports_download=False,
          ),
          'Get': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'apikeys.projects.apiKeys.get',
              ordered_params=[u'projectId', u'keyId'],
              path_params=[u'keyId', u'projectId'],
              query_params=[],
              relative_path=u'v1/projects/{projectId}/apiKeys/{keyId}',
              request_field='',
              request_type_name=u'ApikeysProjectsApiKeysGetRequest',
              response_type_name=u'ApiKey',
              supports_download=False,
          ),
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'apikeys.projects.apiKeys.list',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[u'pageSize', u'pageToken'],
              relative_path=u'v1/projects/{projectId}/apiKeys',
              request_field='',
              request_type_name=u'ApikeysProjectsApiKeysListRequest',
              response_type_name=u'ListApiKeysResponse',
              supports_download=False,
          ),
          'Patch': base_api.ApiMethodInfo(
              http_method=u'PATCH',
              method_id=u'apikeys.projects.apiKeys.patch',
              ordered_params=[u'projectId', u'keyId'],
              path_params=[u'keyId', u'projectId'],
              query_params=[u'updateMask'],
              relative_path=u'v1/projects/{projectId}/apiKeys/{keyId}',
              request_field=u'apiKey',
              request_type_name=u'ApikeysProjectsApiKeysPatchRequest',
              response_type_name=u'ApiKey',
              supports_download=False,
          ),
          'Regenerate': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'apikeys.projects.apiKeys.regenerate',
              ordered_params=[u'projectId', u'keyId'],
              path_params=[u'keyId', u'projectId'],
              query_params=[],
              relative_path=u'v1/projects/{projectId}/apiKeys/{keyId}:regenerate',
              request_field='',
              request_type_name=u'ApikeysProjectsApiKeysRegenerateRequest',
              response_type_name=u'ApiKey',
              supports_download=False,
          ),
          'Revert': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'apikeys.projects.apiKeys.revert',
              ordered_params=[u'projectId', u'keyId'],
              path_params=[u'keyId', u'projectId'],
              query_params=[],
              relative_path=u'v1/projects/{projectId}/apiKeys/{keyId}:revert',
              request_field='',
              request_type_name=u'ApikeysProjectsApiKeysRevertRequest',
              response_type_name=u'ApiKey',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def BatchDelete(self, request, global_params=None):
      """Bulk delete a list of API keys.

      Args:
        request: (ApikeysProjectsApiKeysBatchDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('BatchDelete')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Create(self, request, global_params=None):
      """Creates a new API key.

      Args:
        request: (ApikeysProjectsApiKeysCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApiKey) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Delete(self, request, global_params=None):
      """Deletes an API key.

      Args:
        request: (ApikeysProjectsApiKeysDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Get(self, request, global_params=None):
      """Gets the metadata for an API key.

      Args:
        request: (ApikeysProjectsApiKeysGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApiKey) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    def List(self, request, global_params=None):
      """Lists the API keys owned by a project.

      Args:
        request: (ApikeysProjectsApiKeysListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListApiKeysResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Patch(self, request, global_params=None):
      """Patches the modifiable fields of an API key.

      Args:
        request: (ApikeysProjectsApiKeysPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApiKey) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Regenerate(self, request, global_params=None):
      """Regenerates the key string for the specified API key.
This writes a new key string to `current_key` and writes the previous key
string to `previous_key`.
Returns the updated key entry.

      Args:
        request: (ApikeysProjectsApiKeysRegenerateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApiKey) The response message.
      """
      config = self.GetMethodConfig('Regenerate')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Revert(self, request, global_params=None):
      """Reverts a previous key regeneration.
This swaps the contents of `current_key` and `previous_key`.
Returns the updated key entry.

      Args:
        request: (ApikeysProjectsApiKeysRevertRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ApiKey) The response message.
      """
      config = self.GetMethodConfig('Revert')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsDeletedApiKeysService(base_api.BaseApiService):
    """Service class for the projects_deletedApiKeys resource."""

    _NAME = u'projects_deletedApiKeys'

    def __init__(self, client):
      super(ApikeysV1.ProjectsDeletedApiKeysService, self).__init__(client)
      self._method_configs = {
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'apikeys.projects.deletedApiKeys.list',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[u'pageSize', u'pageToken'],
              relative_path=u'v1/projects/{projectId}/deletedApiKeys',
              request_field='',
              request_type_name=u'ApikeysProjectsDeletedApiKeysListRequest',
              response_type_name=u'ListDeletedApiKeysResponse',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      """Lists the deleted API keys owned by a project.

      Args:
        request: (ApikeysProjectsDeletedApiKeysListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListDeletedApiKeysResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = u'projects'

    def __init__(self, client):
      super(ApikeysV1.ProjectsService, self).__init__(client)
      self._method_configs = {
          'GetProjectForApiKey': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'apikeys.projects.getProjectForApiKey',
              ordered_params=[],
              path_params=[],
              query_params=[u'apiKey'],
              relative_path=u'v1/projects:getProjectForApiKey',
              request_field='',
              request_type_name=u'ApikeysProjectsGetProjectForApiKeyRequest',
              response_type_name=u'GetProjectForApiKeyResponse',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def GetProjectForApiKey(self, request, global_params=None):
      """Get the project info about an API key.

      Args:
        request: (ApikeysProjectsGetProjectForApiKeyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (GetProjectForApiKeyResponse) The response message.
      """
      config = self.GetMethodConfig('GetProjectForApiKey')
      return self._RunMethod(
          config, request, global_params=global_params)
