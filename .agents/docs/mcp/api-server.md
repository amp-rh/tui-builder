# API MCP Server

The API MCP server (`mcp_server.py`) provides the project's external interface for other agents.

## Purpose

This server is **external-facing** - it exposes the project's functionality:

- Domain-specific tools
- Data access and resources
- Business logic operations
- Integration endpoints

This is the "product" that projects built from this template expose to the world.

## Starting the Server

```bash
# Local development
make serve

# Or directly
uv run python src/my_package/mcp_server.py

# Container
make mcp-serve
```

## Template Tools

The template includes example tools to demonstrate patterns:

| Tool | Description |
|------|-------------|
| `hello` | Example greeting tool |
| `add` | Example arithmetic tool |

**These are placeholders** - replace them with your domain-specific tools.

## Adding Domain Tools

### 1. Identify Tool Candidates

Good API tools are:
- **Domain-specific**: Provide value unique to your project
- **Stateless**: Don't rely on server-side state between calls
- **Well-typed**: Full type hints for inputs and outputs
- **Documented**: Clear docstrings explaining usage

### 2. Implement the Tool

```python
@mcp.tool()
def your_domain_tool(param1: str, param2: int = 10) -> dict[str, Any]:
    """Short description of what this tool does.

    Args:
        param1: Description of param1.
        param2: Description of param2 with default.

    Returns:
        Description of return value structure.
    """
    # Your implementation
    result = do_domain_operation(param1, param2)
    return {"result": result, "status": "success"}
```

### 3. Add Resources

Expose data that agents need:

```python
@mcp.resource("data://schema")
def get_schema() -> str:
    """Get the data schema.

    Returns:
        JSON schema as string.
    """
    return json.dumps(SCHEMA, indent=2)
```

### 4. Add Prompts

Guide agent interactions:

```python
@mcp.prompt()
def query_guide(query_type: str) -> str:
    """Guide for constructing queries.

    Args:
        query_type: The type of query to construct.
    """
    return f"""You are helping construct a {query_type} query.

## Available Fields
{list_fields()}

## Examples
{get_examples(query_type)}
"""
```

## Example Domain Implementations

### Data Processing Service

```python
@mcp.tool()
def process_data(input_path: str, format: str = "json") -> dict:
    """Process data from a file."""
    ...

@mcp.resource("schema://input")
def input_schema() -> str:
    """Input data schema."""
    ...
```

### API Integration

```python
@mcp.tool()
def fetch_records(query: str, limit: int = 100) -> list[dict]:
    """Fetch records matching query."""
    ...

@mcp.tool()
def create_record(data: dict) -> dict:
    """Create a new record."""
    ...
```

### Analysis Service

```python
@mcp.tool()
def analyze(data: str, analysis_type: str) -> dict:
    """Perform analysis on data."""
    ...

@mcp.prompt()
def analysis_guide(data_type: str) -> str:
    """Guide for analyzing specific data types."""
    ...
```

## Best Practices

1. **Keep tools focused**: One tool, one purpose
2. **Return structured data**: Use dicts/lists, not formatted strings
3. **Handle errors gracefully**: Return error info, don't crash
4. **Validate inputs**: Check parameters before processing
5. **Document thoroughly**: Agents rely on docstrings

## Related

- @.agents/docs/mcp/overview.md - Architecture overview
- @.agents/docs/mcp/patterns.md - Implementation patterns
- @.agents/commands/extract-mcp-tools.md - Extract tools from codebase
- @src/my_package/mcp_server.py - Implementation

