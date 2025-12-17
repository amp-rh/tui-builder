"""TUI Builder MCP Prompts.

Prompts providing guided workflows for TUI development.
"""

from mcp.server.fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register all TUI Builder prompts with the MCP server."""
    from tui_builder.prompts.debug import register_debug_prompts
    from tui_builder.prompts.design import register_design_prompts

    register_design_prompts(mcp)
    register_debug_prompts(mcp)
