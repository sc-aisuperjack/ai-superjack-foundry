"""Minimal MCP-style scaffold.

This file intentionally avoids depending on a moving MCP SDK API.
It provides a clear place to wire tools, resources, and prompts.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class MCPTool:
    name: str
    description: str

    def invoke(self, arguments: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "arguments": arguments, "status": "ok"}


TOOLS = [
    MCPTool(name="search_collection", description="Search a MongoDB-backed collection"),
    MCPTool(name="list_knowledge_sources", description="List available knowledge sources"),
    MCPTool(name="run_health_check", description="Return service health"),
]


def list_tools() -> list[dict[str, str]]:
    return [{"name": tool.name, "description": tool.description} for tool in TOOLS]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    for tool in TOOLS:
        if tool.name == name:
            return tool.invoke(arguments)
    return {"status": "error", "message": f"Unknown tool: {name}"}
