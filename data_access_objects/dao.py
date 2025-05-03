import os
from typing import MutableMapping, Any, Optional, List, Union

from azure.core.credentials import AzureKeyCredential
from azure.core.paging import ItemPaged
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient, SearchItemPaged
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndex, SearchIndexer


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

    def create_index(self, index_definition: SearchIndex) ->  MutableMapping[str, Any]:
        operation_results = self.client.create_index(index_definition)
        return operation_results.serialize(keep_readonly=True)


    def delete_index(self, index_name: str):
        self.client.delete_index(index_name)

class SearchClientDao(SearchBaseDao):

    def __init__(self, index_name: str):
        """
        Initializes the SearchIndexDao with a SearchIndexClient instance.
        :param index_name: The name of the index to connect to
        """
        super().__init__()
        credentials = self._fetch_credentials()
        self.client = SearchClient(self.service_endpoint, index_name, credentials, api_version=self.api_version)


    def add_document(self, document: dict):

        documents_to_add = [document]
        operation_results = self.add_documents(documents_to_add)
        return operation_results[0]


    def add_documents(self, documents: list[dict]) -> list[MutableMapping[str, Any]]:

        operation_results = self.client.upload_documents(documents)

        results: list[ MutableMapping[str, Any]] = []

        for operation_result in operation_results:
            results.append(operation_result.serialize(keep_readonly=True))

        return results

    def delete_document(self, documents: list[dict]) -> list[MutableMapping[str, Any]]:

        operation_results = self.client.delete_documents(documents)

        results: list[MutableMapping[str, Any]] = []

        for operation_result in operation_results:
            results.append(operation_result.serialize(keep_readonly=True))

        return results

    def query_index(self,
                    search_text: Optional[str] = None,
                    *,
                    query_filter: Optional[str] = None,
                    order_by: Optional[List[str]] = None,
                    select: Optional[List[str]] = None,
                    skip: Optional[int] = None,
                    top: Optional[int] = None,
                    include_total_count: Optional[bool] = None,
                    ) -> list[dict]:
        """Search the Azure search index for documents.

        :param str search_text: A full-text search query expression; Use "*" or omit this parameter to
            match all documents.
        :param str query_filter: The OData $filter expression to apply to the search query.
        :param list[str] order_by: The list of OData $orderby expressions by which to sort the results. Each
            expression can be either a field name or a call to either the geo.distance() or the
            search.score() functions. Each expression can be followed by asc to indicate ascending, and
            desc to indicate descending. The default is ascending order. Ties will be broken by the match
            scores of documents. If no OrderBy is specified, the default sort order is descending by
            document match score. There can be at most 32 $orderby clauses.
        :param list[str] select: The list of fields to retrieve. If unspecified, all fields marked as retrievable
            in the schema are included.
        :param int skip: The number of search results to skip. This value cannot be greater than 100,000.
            If you need to scan documents in sequence, but cannot use $skip due to this limitation,
            consider using $orderby on a totally-ordered key and $filter with a range query instead.
        :param int top: The number of search results to retrieve. This can be used in conjunction with
            $skip to implement client-side paging of search results. If results are truncated due to
            server-side paging, the response will include a continuation token that can be used to issue
            another Search request for the next page of results.
        :param bool include_total_count: A value that specifies whether to fetch the total count of
            results. Default is false. Setting this value to true may have a performance impact. Note that
            the count returned is an approximation.
        :rtype: list[dict]
        """
        search_results: SearchItemPaged[dict] = self.client.search(search_text=search_text,
                                                                   include_total_count=include_total_count,
                                                                   filter=query_filter,
                                                                   order_by=order_by,
                                                                   select=select,
                                                                   skip=skip,
                                                                   top=top
                                                                   )

        query_results: list[dict] = []

        for search_result_item in search_results:
            query_results.append(search_result_item)

        return query_results


class SearchIndexerDao(SearchBaseDao):
    """
    A data access object (DAO) for managing Azure AI Search indexers, data sources, and skillsets.

    This class provides methods for listing, retrieving, creating, and deleting indexers,
    as well as accessing data source connections and skillsets configured in the Azure AI Search service.
    """

    def __init__(self):
        """
        Initializes the SearchIndexerDao by creating a SearchIndexerClient using credentials
        and service configuration from the base class.
        """
        super().__init__()
        credentials = self._fetch_credentials()
        self.client = SearchIndexerClient(self.service_endpoint, credentials, api_version=self.api_version)

    def list_indexers(self) -> list[str]:
        """
        Retrieves the names of all indexers registered in the Azure AI Search service.

        Returns:
            list[str]: A list of indexer names.
        """
        search_results = self.client.get_indexer_names()
        indexer_names: list[str] = []

        for search_result in search_results:
            indexer_names.append(search_result)
        return indexer_names

    def get_indexer(self, name: str) -> MutableMapping[str, Any]:
        """
        Retrieves the full definition of a specific indexer.

        Args:
            name (str): The name of the indexer to retrieve.

        Returns:
            MutableMapping[str, Any]: A dictionary representing the serialized indexer definition.
        """
        indexer_details = self.client.get_indexer(name)
        indexer_result = indexer_details.serialize(keep_readonly=True)
        return indexer_result

    def create_indexer(self, indexer: SearchIndexer) -> MutableMapping[str, Any]:
        """
        Creates a new indexer in the Azure AI Search service.

        The following properties must be set on the indexer object:
            - name (str)
            - data_source_name (str)
            - target_index_name (str)
            - description (Optional[str])

        Args:
            indexer (SearchIndexer): The SearchIndexer object to be created.

        Returns:
            MutableMapping[str, Any]: A dictionary representing the created indexer.
        """
        indexer_result = self.client.create_indexer(indexer)
        return indexer_result.serialize(keep_readonly=True)

    def delete_indexer(self, name: str) -> None:
        """
        Deletes an indexer by name from the Azure AI Search service.

        Args:
            name (str): The name of the indexer to delete.
        """
        self.client.delete_indexer(name)

    def list_data_sources(self) -> list[str]:
        """
        Lists the names of all data source connections configured in the AI Search service.

        Returns:
            list[str]: A list of data source connection names.
        """
        data_source_names = self.client.get_data_source_connection_names()
        search_results: list[str] = []
        for data_source_name in data_source_names:
            search_results.append(data_source_name)
        return search_results

    def get_data_source(self, name: str) -> MutableMapping[str, Any]:
        """
        Retrieves the full definition of a specific data source connection.

        Args:
            name (str): The name of the data source connection to retrieve.

        Returns:
            MutableMapping[str, Any]: A dictionary representing the serialized data source definition.
        """
        data_source_detail = self.client.get_data_source_connection(name=name)
        data_source_result = data_source_detail.serialize(keep_readonly=True)
        return data_source_result

    def list_skill_sets(self) -> list[str]:
        """
        Lists the names of all skillsets configured in the Azure AI Search service.

        Returns:
            list[str]: A list of skillset names.
        """
        skill_set_names = self.client.get_skillset_names()
        search_results: list[str] = []
        for skill_set_name in skill_set_names:
            search_results.append(skill_set_name)
        return search_results

    def get_skill_set(self, skill_set_name: str) -> MutableMapping[str, Any]:
        """
        Retrieves the full definition of a specific skillset.

        Args:
            skill_set_name (str): The name of the skillset to retrieve.

        Returns:
            MutableMapping[str, Any]: A dictionary representing the serialized skillset definition.
        """
        skill_set_result = self.client.get_skillset(skill_set_name)
        return skill_set_result.serialize(keep_readonly=True)
