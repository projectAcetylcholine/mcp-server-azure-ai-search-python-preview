from typing import Any, MutableMapping

from shared import AISearchMCP
from .data_access_objects import SearchIndexDao

mcp = AISearchMCP("AI Search MCP Service", log_level="DEBUG")

@mcp.tool(description="Retrieve all names of indexes from the AI Search Service")
async def retrieve_index_names() -> list[str]:
    dao = SearchIndexDao()
    return dao.retrieve_index_names()

@mcp.tool(description="Retrieve all index schemas from the AI Search Service")
async def retrieve_index_schemas() -> list[MutableMapping[str, Any]]:
    dao = SearchIndexDao()
    return dao.retrieve_index_schemas()

@mcp.tool(description="Retrieve the schema for a specific index from the AI Search Service")
async def retrieve_index_schema(index_name: str) -> MutableMapping[str, Any]:
    dao = SearchIndexDao()
    return dao.retrieve_index_schema(index_name)

def run_mcp_service():
    mcp.run('stdio')

if __name__ == "__main__":
    run_mcp_service()
