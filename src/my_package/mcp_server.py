"""MCP Server implementation using FastMCP.

See @AGENTS.md for project-wide rules.
See @.agents/docs/tooling/uv.md for dependency management.
"""

from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
# TODO: Update the server name to match your project
mcp = FastMCP("<project-name>")


@mcp.tool()
def hello(name: str = "World") -> str:
    """Say hello to someone.

    Args:
        name: The name to greet.

    Returns:
        A greeting message.
    """
    return f"Hello, {name}!"


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b.
    """
    return a + b


if __name__ == "__main__":
    mcp.run()
