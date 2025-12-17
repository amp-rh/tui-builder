# /extract-mcp-tools

Extract and create MCP tools from the codebase.

## Purpose

Identify useful functions or capabilities in the codebase and expose them as MCP tools that agents can call.

## Which Server?

| Tool Type | Server | File |
|-----------|--------|------|
| Project development (tests, lint, tasks) | Dev Server | `dev_mcp.py` |
| Domain-specific (your project's API) | API Server | `mcp_server.py` |

See @.agents/docs/mcp/overview.md for architecture details.

## Steps

1. **Analyze codebase**: Scan for functions that would be useful as tools
2. **Identify candidates**: Look for:
   - Utility functions with clear inputs/outputs
   - Service methods that perform actions
   - Query functions that retrieve data
   - Validation or transformation functions
3. **Choose server**: Dev tools → `dev_mcp.py`, Domain tools → `mcp_server.py`
4. **Create tool definitions**: Add `@mcp.tool()` decorated functions
5. **Add documentation**: Write clear docstrings with Args/Returns
6. **Test tools**: Verify tools work correctly

## Tool Candidates

Good MCP tools are:
- **Atomic**: Do one thing well
- **Documented**: Clear description and parameter docs
- **Typed**: Full type hints for parameters and return
- **Safe**: Don't have dangerous side effects without confirmation

### Examples of Good Tools

**Dev Server (dev_mcp.py):**
- Run tests, lint, format
- Task management
- Template creation
- Git operations

**API Server (mcp_server.py):**
- Search/query functions
- Data transformation utilities
- Validation functions
- CRUD operations

### Examples to Avoid
- Functions with complex internal state
- Operations requiring multiple steps
- Functions with unclear side effects

## Tool Template

```python
@mcp.tool()
def tool_name(param1: str, param2: int = 10) -> dict[str, Any]:
    """Short description of what the tool does.

    Args:
        param1: Description of param1.
        param2: Description of param2 with default.

    Returns:
        Description of return value structure.
    """
    # Implementation
    return {"result": value}
```

## Output Location

**Dev tools** → Add to `src/<package_name>/dev_mcp.py`:

```python
# In dev_mcp.py
@mcp.tool()
def run_tests(path: str | None = None) -> dict[str, Any]:
    """Run pytest tests."""
    ...
```

**Domain tools** → Add to `src/<package_name>/mcp_server.py`:

```python
# In mcp_server.py
@mcp.tool()
def search_data(query: str) -> list[dict]:
    """Search the data store."""
    ...
```

## Rules

- MUST have complete type hints
- MUST have docstrings with Args/Returns
- MUST handle errors gracefully (return error info, don't crash)
- MUST choose the correct server (dev vs API)
- SHOULD keep tools focused and single-purpose
- SHOULD NOT expose internal implementation details

## Related

- @.agents/docs/mcp/overview.md - MCP architecture
- @.agents/docs/mcp/dev-server.md - Dev server tools
- @.agents/docs/mcp/api-server.md - API server tools
- @.agents/docs/mcp/patterns.md - Implementation patterns
- @src/my_package/dev_mcp.py - Dev server implementation
- @src/my_package/mcp_server.py - API server implementation
- @.agents/commands/deploy-mcp.md - Deploy the servers
- @.agents/commands/extract-mcp-prompts.md - Extract prompts
- @.agents/commands/extract-mcp-resources.md - Extract resources
