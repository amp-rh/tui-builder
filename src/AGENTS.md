# AGENTS.md - Source Code

See @AGENTS.md for project-wide rules.

## Documentation

### Patterns

- @.agents/docs/patterns/error-handling.md - Error handling patterns
- @.agents/docs/patterns/typing.md - Type hints and annotations
- @.agents/docs/patterns/logging.md - Logging conventions

### Conventions

- @.agents/docs/conventions/naming.md - Naming conventions
- @.agents/docs/conventions/imports.md - Import organization
- @.agents/docs/conventions/project-structure.md - Module organization

### Tooling

- @.agents/docs/tooling/ruff.md - Linting and formatting

### MCP

- @.agents/docs/mcp/overview.md - MCP architecture
- @.agents/docs/mcp/dev-server.md - Dev server guide
- @.agents/docs/mcp/api-server.md - API server guide
- @.agents/docs/mcp/patterns.md - MCP patterns

## Rules

- MUST follow coding style in @.agents/docs/conventions/coding-style.md
- MUST use type hints on all public functions
- MUST use dataclasses for data structures
- MUST write tests first (TDD)
- MUST NOT include comments (code should self-document)
- MUST NOT use `print()` for operational output (use logging)
- MUST follow naming conventions in @.agents/docs/conventions/naming.md

## Structure

```
src/
├── AGENTS.md                   # This file
├── __init__.py                 # Package root
└── my_package/                 # Main package (TODO: rename to your package)
    ├── __init__.py             # Package init with version
    ├── dev_mcp.py              # Dev MCP server (project development)
    └── mcp_server.py           # API MCP server (external interface)
```

## MCP Servers

This project has two MCP servers:

### Dev Server (`dev_mcp.py`)

For agents **developing this project**:
- Run tests, lint, format
- Manage tasks and learnings
- Create files from templates
- Git operations

```bash
make serve-dev
```

### API Server (`mcp_server.py`)

For **external agents** using this project's functionality:
- Domain-specific tools
- Data access and manipulation
- Business logic execution

```bash
make serve
```

See @.agents/docs/mcp/overview.md for full details.

## Adding MCP Tools

- **Dev tools** (run tests, manage tasks) → Add to `dev_mcp.py`
- **Domain tools** (project functionality) → Add to `mcp_server.py`

Commands:
- @.agents/commands/extract-mcp-tools.md - Add new tools
- @.agents/commands/extract-mcp-prompts.md - Add prompts
- @.agents/commands/extract-mcp-resources.md - Add resources
- @.agents/commands/deploy-mcp.md - Deploy the servers
