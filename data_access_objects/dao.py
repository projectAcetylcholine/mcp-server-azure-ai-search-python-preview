import os
from typing import MutableMapping, Any

from azure.core.credentials import AzureKeyCredential
from azure.core.paging import ItemPaged
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex


class SearchBaseDao:
    """
    Base class for Azure Cognitive Search data access operations.

    Handles environment configuration and authentication setup
    for interacting with Azure AI Search services.
    """

    def __init__(self):
        """
        Initializes the SearchBaseDao by reading configuration from environment variables.
        """
        self.authentication_method = self._get_env_variable("AZURE_AUTHENTICATION_METHOD", "api-search-key")
        self.service_endpoint = self._get_env_variable("AZURE_AI_SEARCH_ENDPOINT")
        self.api_version = self._get_env_variable('AZURE_AI_SEARCH_API_VERSION', '2025-03-01-preview')

    @staticmethod
    def _get_env_variable(key: str, default_value: str | None = None) -> str:
        """
        Retrieves an environment variable value or returns a default if not set.

        Args:
            key (str): The name of the environment variable.
            default_value (str | None): Optional fallback value.

        Returns:
            str: The value of the environment variable or the default.
        """
        return os.environ.get(key, default_value)

    def _fetch_credentials(self) -> AzureKeyCredential | DefaultAzureCredential:
        """
        Fetches the appropriate credentials for Azure Search based on the configured authentication method.

        Returns:
            AzureKeyCredential | DefaultAzureCredential: A credential object for authenticating requests.

        Raises:
            Exception: If the authentication method is missing or invalid.
        """
        if self.authentication_method == 'api-search-key':
            api_key = self._get_env_variable('AZURE_AI_SEARCH_API_KEY')
            credential = AzureKeyCredential(api_key)
            return credential
        elif self.authentication_method == 'service-principal':
            credential = DefaultAzureCredential()
            return credential

        error_message = (
            "AZURE_AUTHENTICATION_METHOD was not specified or is invalid. "
            "Must be one of api-search-key or service-principal"
        )
        raise Exception(error_message)


class SearchIndexDao(SearchBaseDao):
    """
    Data Access Object (DAO) for interacting with Azure AI Search Indexes.

    Inherits configuration and authentication from SearchBaseDao.
    """

    def __init__(self):
        """
        Initializes the SearchIndexDao with a SearchIndexClient instance.
        """
        super().__init__()
        credentials = self._fetch_credentials()
        self.client = SearchIndexClient(self.service_endpoint, credentials, api_version=self.api_version)

    def retrieve_index_names(self) -> list[str]:
        """
        Retrieves a list of all search index names from the Azure Search service.

        Returns:
            list[str]: A list of index names.
        """
        search_results = self.client.list_index_names()
        results: list[str] = []

        for search_result in search_results:
            results.append(search_result)

        return results

    def retrieve_index_schemas(self) -> list[MutableMapping[str, Any]]:
        """
        Retrieves the full schema definition for each search index.

        Returns:
            list[SearchIndex]: A list of serialized index schema definitions.
        """
        search_results: ItemPaged[SearchIndex] = self.client.list_indexes()
        results = []

        for search_result in search_results:
            results.append(search_result.serialize(keep_readonly=True))

        return results

    def retrieve_index_schema(self, index_name: str) -> MutableMapping[str, Any]:
        """
        Retrieves the full schema definition for a search index.

        Returns:
            SearchIndex: A serialized index schema definition.
        """
        search_results = self.client.get_index(index_name)

        return search_results.serialize(keep_readonly=True)
