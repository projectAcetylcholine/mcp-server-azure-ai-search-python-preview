from typing import Any, MutableMapping, Optional, List

from azure.search.documents.indexes.models import SearchIndexer

from shared import AISearchMCP
from data_access_objects import SearchIndexDao, SearchClientDao, SearchIndexerDao

mcp = AISearchMCP("AI Search MCP Service", log_level="DEBUG")

@mcp.tool(description="Retrieves the names of all indexes from the Azure AI Search service")
async def retrieve_index_names() -> list[str]:
    """
    Retrieves the names of all indexes from the Azure AI Search service.

    Returns:
        list[str]: A list containing the names of all available search indexes.
    """
    dao = SearchIndexDao()
    return dao.retrieve_index_names()


@mcp.tool(description="Retrieves the schemas for all indexes from the Azure AI Search service")
async def retrieve_index_schemas() -> list[MutableMapping[str, Any]]:
    """
    Retrieves the schemas for all indexes from the Azure AI Search service.

    Returns:
        list[MutableMapping[str, Any]]: A list of dictionaries, each representing the schema of an index.
    """
    dao = SearchIndexDao()
    return dao.retrieve_index_schemas()


@mcp.tool(description="Retrieves the schema for a specific index from the Azure AI Search service")
async def retrieve_index_schema(index_name: str) -> MutableMapping[str, Any]:
    """
    Retrieves the schema for a specific index from the Azure AI Search service.

    Args:
        index_name (str): The name of the index for which the schema should be retrieved.

    Returns:
        MutableMapping[str, Any]: A dictionary representing the schema of the specified index.
    """
    dao = SearchIndexDao()
    return dao.retrieve_index_schema(index_name)


@mcp.tool(description="Search a specific index for documents in that index")
async def query_index(
        index_name: str,
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

        :param str index_name: The name of the index to query. This parameter is required
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
    search_client_dao = SearchClientDao(index_name)

    search_results: list[dict] = search_client_dao.query_index(
        search_text=search_text,
        include_total_count=include_total_count,
        query_filter=query_filter,
        order_by=order_by,
        select=select,
        skip=skip,
        top=top
    )

    return search_results

@mcp.tool(description="Retrieves the list of all the names of the indexers registered in the Azure AI Search service")
async def list_indexers() -> list[str]:
    """
    Retrieves the list of all indexers registered in the Azure AI Search service.

    Returns:
        list[str]: A list of indexer names.
    """
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.list_indexers()

@mcp.tool(description="Retrieves the details of a specific indexer by name.")
async def get_indexer(name: str) -> MutableMapping[str, Any]:
    """
    Retrieves the details of a specific indexer by name.

    Args:
        name (str): The name of the indexer to retrieve.

    Returns:
        MutableMapping[str, Any]: A dictionary containing the indexer details.
    """
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.get_indexer(name)

@mcp.tool(description="Creates a new indexer in the Azure AI Search service")
async def create_indexer(indexer: SearchIndexer) -> MutableMapping[str, Any]:
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
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.create_indexer(indexer)

@mcp.tool(description="Deletes an indexer from the Azure AI Search service by name")
async def delete_indexer(name: str) -> None:
    """
    Deletes an indexer from the Azure AI Search service by name.

    Args:
        name (str): The name of the indexer to delete.

    Returns:
        None
    """
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.delete_indexer(name)

@mcp.tool(description="Retrieves the list of all data source names configured in the Azure AI Search service")
async def list_data_sources() -> list[str]:
    """
    Retrieves the list of all data source names configured in the Azure AI Search service.

    Returns:
        list[str]: A list of data source names.
    """
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.list_data_sources()

@mcp.tool(description="Retrieves the details of a specific data source by name")
async def get_data_source(name: str) -> MutableMapping[str, Any]:
    """
    Retrieves the details of a specific data source by name.

    Args:
        name (str): The name of the data source to retrieve.

    Returns:
        MutableMapping[str, Any]: A dictionary containing the data source details.
    """
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.get_data_source(name)

@mcp.tool(description="Retrieves the list of the names of all skill sets configured in the Azure AI Search service")
async def list_skill_sets() -> list[str]:
    """
    Retrieves the list of all skill sets configured in the Azure AI Search service.

    Returns:
        list[str]: A list of skill set names.
    """
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.list_skill_sets()

@mcp.tool(description="Retrieves the details of a specific skill set by nam")
async def get_skill_set(skill_set_name: str) -> MutableMapping[str, Any]:
    """
    Retrieves the details of a specific skill set by name.

    Args:
        skill_set_name (str): The name of the skill set to retrieve.

    Returns:
        MutableMapping[str, Any]: A dictionary containing the skill set details.
    """
    search_indexer_dao = SearchIndexerDao()
    return search_indexer_dao.get_skill_set(skill_set_name)


def run_mcp_service():
    mcp.run('stdio')


if __name__ == "__main__":
    run_mcp_service()
