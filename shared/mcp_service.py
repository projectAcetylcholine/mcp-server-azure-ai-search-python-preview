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
            "retrieve_index_schema"
        ]

    def _get_role_tools(self) -> list[str]:
        user_role = os.environ.get("AZURE_AI_SEARCH_MCP_TOOL_GROUPS", "ALL")

        # ["hospital-admin", "caregiver", "patient"]
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

        return tool_database[user_role]

    async def list_tools(self) -> list[MCPTool]:

        context = self.get_context()
        session = context.session

        filtered_tool_names = self._get_role_tools()
        filtered_tool_list: list[MCPTool] = []
        tool_list: list[MCPTool] = await super().list_tools()

        logger.debug(context)
        logger.debug(session)

        for current_tool in tool_list:
            if current_tool.name in filtered_tool_names:
                filtered_tool_list.append(current_tool)

        return filtered_tool_list