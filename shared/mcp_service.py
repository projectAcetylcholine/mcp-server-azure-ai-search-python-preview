import os
from typing import Any

from mcp.server.fastmcp.server import logger, FastMCP
from mcp.types import Tool as MCPTool


class AISearchMCP(FastMCP):

    def __init__(
        self, name: str | None = None, instructions: str | None = None, **settings: Any):
        super().__init__(name=name, instructions=instructions, **settings)

        self.all_tool_names: list[str] = [
            "retrieve_index_names",
            "retrieve_index_schemas",
            "retrieve_index_schema",
            "query_index"
        ]

    def _get_role_tools(self) -> list[str]:
        tool_groups_raw = os.environ.get("AZURE_AI_SEARCH_MCP_TOOL_GROUPS", "ALL")
        tool_groups_list = tool_groups_raw.split(",")

        filtered_list_of_tools: list[str] = []

        # This is a dictionary of the groups
        tool_database: dict[str, list[str]] = {
            "ALL" : self.all_tool_names,
            "READ_INDEX": self.all_tool_names,
            "WRITE_INDEX": self.all_tool_names,
            "READ_DOCUMENTS": self.all_tool_names,
            "WRITE_DOCUMENTS": self.all_tool_names,
            "READ_INDEXERS": self.all_tool_names,
            "WRITE_INDEXERS": self.all_tool_names,
            "RUN_INDEXERS" : self.all_tool_names
        }

        for tool_group_name in tool_groups_list:
            current_list_of_tools = tool_database[tool_group_name]
            filtered_list_of_tools += current_list_of_tools

        # Eliminate duplicates while preserving order
        unique_tool_names = list(dict.fromkeys(filtered_list_of_tools))

        return unique_tool_names

    async def list_tools(self) -> list[MCPTool]:

        # This is the filtered names of tools to send back to calling MCP client
        filtered_tool_names = self._get_role_tools()
        filtered_tool_list: list[MCPTool] = []

        # This is the list of tools registered at the service
        tool_list: list[MCPTool] = await super().list_tools()

        # Preparing the filtered list of tools
        for current_tool in tool_list:
            if current_tool.name in filtered_tool_names:
                filtered_tool_list.append(current_tool)

        return filtered_tool_list