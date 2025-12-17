"""TUI Builder MCP Resources.

Resources providing documentation and references for TUI development.
"""

from mcp.server.fastmcp import FastMCP


def register_resources(mcp: FastMCP) -> None:
    """Register all TUI Builder resources with the MCP server."""
    from tui_builder.resources.components import register_component_resources
    from tui_builder.resources.css import register_css_resources
    from tui_builder.resources.patterns import register_pattern_resources

    register_component_resources(mcp)
    register_css_resources(mcp)
    register_pattern_resources(mcp)
