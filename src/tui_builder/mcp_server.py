"""TUI Builder MCP Server.

An MCP server providing prompts, resources, and tools for building
high-quality TUI (Text User Interface) applications with Textual.
"""

from mcp.server.fastmcp import FastMCP

from tui_builder.prompts import register_prompts
from tui_builder.resources import register_resources
from tui_builder.tools import register_tools

mcp = FastMCP(
    "tui-builder",
    instructions="""TUI Builder helps you create high-quality Text User Interface
applications using the Textual framework.

Use the available tools to:
- Generate component code following best practices
- Validate CSS and layouts
- Create app scaffolding
- Run and test TUI applications

Use resources to access:
- Textual component documentation
- CSS reference and examples
- Design patterns and best practices

Use prompts for guided workflows:
- Designing TUI layouts
- Creating custom widgets
- Debugging and optimization
""",
)

# Register all MCP capabilities
register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)


if __name__ == "__main__":
    mcp.run()
