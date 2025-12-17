# Dev MCP Server

The dev MCP server (`dev_mcp.py`) provides tools for agents developing and maintaining this project.

## Purpose

This server is **internal-facing** - it helps agents work on the project itself:

- Run tests and check code quality
- Create files from templates
- Manage project tasks and learnings
- Perform git operations
- Access project configuration and documentation

## Starting the Server

```bash
# Local development
make serve-dev

# Or directly
uv run python src/my_package/dev_mcp.py
```

## Available Tools

### Testing & Quality

| Tool | Description | Parameters |
|------|-------------|------------|
| `run_tests` | Run pytest | `path?` - specific test path |
| `run_lint` | Run ruff check | `fix?` - auto-fix issues |
| `format_code` | Run ruff format | `path?` - specific path |

### Task Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_tasks` | List all tasks | `status?` - filter by status |
| `add_task` | Create a new task | `title`, `description?` |
| `complete_task` | Mark task complete | `task_id` |

### Project Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_learning` | Add to learnings | `category`, `title`, `content` |
| `create_from_template` | Create file from template | `template`, `destination`, `vars?` |

## Available Resources

| URI | Description |
|-----|-------------|
| `config://pyproject` | Project configuration (pyproject.toml) |
| `docs://agents` | Root AGENTS.md |
| `docs://agents/{path}` | Specific AGENTS.md file |
| `tasks://list` | Current task list |
| `learnings://all` | All project learnings |

## Available Prompts

| Prompt | Description | Parameters |
|--------|-------------|------------|
| `code_review` | Review code against project standards | `code` |
| `implement_feature` | Guide for implementing a feature | `description` |

## Example Usage

### Running Tests

```python
# Run all tests
result = await mcp.call_tool("run_tests", {})

# Run specific test file
result = await mcp.call_tool("run_tests", {"path": "tests/test_example.py"})
```

### Managing Tasks

```python
# List pending tasks
tasks = await mcp.call_tool("list_tasks", {"status": "pending"})

# Add a new task
await mcp.call_tool("add_task", {
    "title": "Add validation",
    "description": "Add input validation to the API endpoints"
})
```

### Creating from Templates

```python
# Create a new module from template
await mcp.call_tool("create_from_template", {
    "template": "module.py",
    "destination": "src/my_package/new_module.py",
    "vars": {"module_name": "new_module"}
})
```

## Adding New Dev Tools

When adding tools to the dev server, consider:

1. **Is it project-internal?** Dev tools modify or inspect this project
2. **Is it reusable?** Should work across different project states
3. **Is it safe?** Should not have destructive side effects without confirmation

See @.agents/docs/mcp/patterns.md for implementation patterns.

## Related

- @.agents/docs/mcp/overview.md - Architecture overview
- @.agents/docs/mcp/patterns.md - Implementation patterns
- @src/my_package/dev_mcp.py - Implementation

