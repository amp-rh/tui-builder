# MCP Implementation Patterns

Common patterns for implementing MCP tools, resources, and prompts.

## Tool Patterns

### Basic Tool

```python
@mcp.tool()
def tool_name(required_param: str, optional_param: int = 10) -> dict[str, Any]:
    """Short description.

    Args:
        required_param: What this parameter is for.
        optional_param: What this parameter is for.

    Returns:
        Description of return structure.
    """
    return {"result": value}
```

### Tool with Validation

```python
@mcp.tool()
def validated_tool(path: str) -> dict[str, Any]:
    """Process a file safely.

    Args:
        path: Path to the file (must be within project).

    Returns:
        Processing result or error.
    """
    # Validate input
    file_path = Path(path)
    if not file_path.exists():
        return {"error": f"File not found: {path}"}
    
    # Prevent directory traversal
    try:
        file_path.resolve().relative_to(Path.cwd())
    except ValueError:
        return {"error": "Path must be within project directory"}
    
    # Process
    return {"content": file_path.read_text()}
```

### Tool Running Subprocess

```python
import subprocess

@mcp.tool()
def run_command(command: str) -> dict[str, Any]:
    """Run a predefined command.

    Args:
        command: Command name (must be in allowed list).

    Returns:
        Command output and exit code.
    """
    ALLOWED = {"test": ["uv", "run", "pytest"], "lint": ["uv", "run", "ruff", "check", "."]}
    
    if command not in ALLOWED:
        return {"error": f"Unknown command: {command}", "allowed": list(ALLOWED.keys())}
    
    result = subprocess.run(ALLOWED[command], capture_output=True, text=True)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
        "success": result.returncode == 0
    }
```

## Resource Patterns

### Static Resource

```python
@mcp.resource("config://pyproject")
def get_pyproject() -> str:
    """Get project configuration."""
    return Path("pyproject.toml").read_text()
```

### Dynamic Resource with Parameters

```python
@mcp.resource("file://{path}")
def get_file(path: str) -> str:
    """Read a project file.

    Args:
        path: Relative path to file.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"File not found: {path}")
    return file_path.read_text()
```

### Resource Listing Directory

```python
@mcp.resource("tasks://list")
def list_tasks() -> str:
    """List all task files."""
    tasks_dir = Path(".agents/tasks")
    if not tasks_dir.exists():
        return "[]"
    
    tasks = []
    for f in tasks_dir.glob("*.md"):
        tasks.append({"name": f.stem, "path": str(f)})
    return json.dumps(tasks, indent=2)
```

## Prompt Patterns

### Simple String Prompt

```python
@mcp.prompt()
def code_review(code: str) -> str:
    """Review code against project standards.

    Args:
        code: The code to review.
    """
    return f"""Review this code against our project standards.

## Project Standards
- Use type hints on all functions
- Follow naming conventions (snake_case for functions)
- Handle errors with try/except
- Add docstrings to public functions

## Code to Review
```python
{code}
```

## Your Review
Provide specific, actionable feedback.
"""
```

### Message-based Prompt

```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt()
def implement_feature(description: str) -> list[base.Message]:
    """Guide for implementing a feature.

    Args:
        description: Feature description.
    """
    return [
        base.UserMessage(f"I need to implement: {description}"),
        base.AssistantMessage("""I'll help you implement this feature. Let me:

1. Understand the requirements
2. Identify affected files
3. Plan the implementation
4. Write the code
5. Add tests

Let's start by clarifying the requirements..."""),
    ]
```

## Error Handling

### Return Errors, Don't Raise

```python
@mcp.tool()
def safe_tool(param: str) -> dict[str, Any]:
    """A tool that handles errors gracefully."""
    try:
        result = risky_operation(param)
        return {"success": True, "result": result}
    except FileNotFoundError as e:
        return {"success": False, "error": "file_not_found", "message": str(e)}
    except ValueError as e:
        return {"success": False, "error": "invalid_value", "message": str(e)}
    except Exception as e:
        return {"success": False, "error": "unexpected", "message": str(e)}
```

### Validation Before Processing

```python
@mcp.tool()
def create_file(path: str, content: str) -> dict[str, Any]:
    """Create a file with validation."""
    # Validate path
    if ".." in path:
        return {"error": "Path cannot contain '..'"}
    
    if not path.startswith("src/") and not path.startswith("tests/"):
        return {"error": "Path must be in src/ or tests/"}
    
    # Check if exists
    file_path = Path(path)
    if file_path.exists():
        return {"error": f"File already exists: {path}"}
    
    # Create
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return {"success": True, "path": path}
```

## Testing Tools

### Unit Test Pattern

```python
# tests/test_mcp.py
import pytest
from my_package.dev_mcp import run_tests, list_tasks

def test_run_tests_returns_dict():
    result = run_tests()
    assert isinstance(result, dict)
    assert "success" in result

def test_list_tasks_empty():
    result = list_tasks()
    assert isinstance(result, dict)
    assert "tasks" in result
```

### Integration Test Pattern

```python
import pytest
from mcp.server.fastmcp import FastMCP

@pytest.fixture
def mcp_server():
    from my_package.dev_mcp import mcp
    return mcp

def test_tool_registered(mcp_server):
    tools = mcp_server.list_tools()
    tool_names = [t.name for t in tools]
    assert "run_tests" in tool_names
```

## Related

- @.agents/docs/mcp/overview.md - Architecture overview
- @.agents/docs/mcp/dev-server.md - Dev server guide
- @.agents/docs/mcp/api-server.md - API server guide
- @.agents/docs/patterns/error-handling.md - General error handling
- @.agents/docs/patterns/typing.md - Type hints guide

