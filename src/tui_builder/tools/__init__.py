"""TUI Builder MCP Tools.

Tools for generating, validating, and testing TUI applications.
"""

from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP) -> None:
    """Register all TUI Builder tools with the MCP server."""
    from tui_builder.tools.generate import register_generate_tools
    from tui_builder.tools.testing import register_testing_tools
    from tui_builder.tools.validate import register_validate_tools

    register_generate_tools(mcp)
    register_validate_tools(mcp)
    register_testing_tools(mcp)
