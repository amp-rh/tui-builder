# /extract-mcp-resources

Extract and create MCP resources from the codebase.

## Purpose

Identify data sources and content in the codebase that should be exposed as MCP resources for agents to read.

## Which Server?

| Resource Type | Server | File |
|---------------|--------|------|
| Project config, docs, tasks | Dev Server | `dev_mcp.py` |
| Domain data, schemas | API Server | `mcp_server.py` |

See @.agents/docs/mcp/overview.md for architecture details.

## Steps

1. **Analyze codebase**: Scan for data that agents would find useful
2. **Identify candidates**: Look for:
   - Configuration files
   - Documentation
   - Data files (JSON, YAML, etc.)
   - Generated content
   - Database schemas or sample data
3. **Choose server**: Project resources → `dev_mcp.py`, Domain resources → `mcp_server.py`
4. **Create resource definitions**: Add `@mcp.resource()` decorated functions
5. **Add documentation**: Write clear descriptions
6. **Test resources**: Verify resources return expected content

## Resource Candidates

Good MCP resources:
- **Static or semi-static**: Don't change frequently
- **Useful context**: Help agents understand the project
- **Structured**: Have consistent format
- **Readable**: Text-based content

### Examples of Good Resources

**Dev Server (dev_mcp.py):**
- Project configuration (`pyproject.toml`)
- AGENTS.md files
- Task lists
- Project learnings

**API Server (mcp_server.py):**
- API schemas or specs
- Database schemas
- Domain data files
- Environment templates

## Resource Template

### Static Resource (URI-based)

```python
@mcp.resource("config://pyproject")
def get_pyproject() -> str:
    """Get the project configuration.

    Returns:
        Contents of pyproject.toml.
    """
    return Path("pyproject.toml").read_text()
```

### Dynamic Resource (with parameters)

```python
@mcp.resource("file://{path}")
def get_file(path: str) -> str:
    """Read a file from the project.

    Args:
        path: Path to the file relative to project root.

    Returns:
        Contents of the file.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"File not found: {path}")
    return file_path.read_text()
```

### Resource with Metadata

```python
from mcp.server.fastmcp.resources import FunctionResource

@mcp.resource("docs://readme")
def get_readme() -> FunctionResource:
    """Get the project README.

    Returns:
        README content with metadata.
    """
    content = Path("README.md").read_text()
    return FunctionResource(
        uri="docs://readme",
        name="README",
        description="Project README file",
        mime_type="text/markdown",
        text=content,
    )
```

## Output Location

**Dev resources** → Add to `src/<package_name>/dev_mcp.py`:

```python
# In dev_mcp.py
@mcp.resource("config://pyproject")
def get_pyproject() -> str:
    """Get project configuration."""
    ...
```

**Domain resources** → Add to `src/<package_name>/mcp_server.py`:

```python
# In mcp_server.py
@mcp.resource("schema://api")
def get_api_schema() -> str:
    """Get the API schema."""
    ...
```

## URI Schemes

Use consistent URI schemes:
- `config://` - Configuration files
- `docs://` - Documentation
- `data://` - Data files
- `schema://` - Schemas and definitions
- `file://` - Generic file access
- `log://` - Log files
- `tasks://` - Task management
- `learnings://` - Project learnings

## Rules

- MUST use consistent URI schemes
- MUST handle missing files gracefully
- MUST choose the correct server (dev vs API)
- MUST NOT expose sensitive data (secrets, credentials)
- SHOULD include appropriate MIME types
- SHOULD validate paths to prevent directory traversal

## Related

- @.agents/docs/mcp/overview.md - MCP architecture
- @.agents/docs/mcp/dev-server.md - Dev server resources
- @.agents/docs/mcp/api-server.md - API server resources
- @.agents/docs/mcp/patterns.md - Implementation patterns
- @src/my_package/dev_mcp.py - Dev server implementation
- @src/my_package/mcp_server.py - API server implementation
- @.agents/commands/deploy-mcp.md - Deploy the servers
- @.agents/commands/extract-mcp-tools.md - Extract tools
- @.agents/commands/extract-mcp-prompts.md - Extract prompts
