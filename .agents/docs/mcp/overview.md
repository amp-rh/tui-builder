# MCP Server Overview

This project supports two MCP (Model Context Protocol) servers with distinct purposes.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Interactions                        │
├─────────────────────────────┬───────────────────────────────┤
│   Internal Development      │    External API               │
│                             │                               │
│   ┌─────────────────────┐   │   ┌─────────────────────┐     │
│   │    dev_mcp.py       │   │   │   mcp_server.py     │     │
│   │                     │   │   │                     │     │
│   │  - run_tests        │   │   │  - domain tools     │     │
│   │  - run_lint         │   │   │  - domain resources │     │
│   │  - task management  │   │   │  - domain prompts   │     │
│   │  - templates        │   │   │                     │     │
│   │  - git operations   │   │   │  (customize these)  │     │
│   └─────────────────────┘   │   └─────────────────────┘     │
│                             │                               │
│   For: Building this        │   For: External agents        │
│        project              │        using this project     │
└─────────────────────────────┴───────────────────────────────┘
```

## When to Use Which Server

### Dev MCP Server (`dev_mcp.py`)

Use for agents that are **developing or maintaining this project**:

- Running tests and linting
- Creating files from templates
- Managing tasks and learnings
- Git operations
- Updating documentation

**Start with:** `make serve-dev` or configure `<project>-dev` in MCP client

### API MCP Server (`mcp_server.py`)

Use for agents that are **consuming this project's functionality**:

- Domain-specific operations
- Data access and manipulation
- Business logic execution
- External integrations

**Start with:** `make serve` or configure `<project>` in MCP client

## Quick Start

1. Install MCP dependencies:
   ```bash
   uv sync --extra mcp
   ```

2. Start the dev server (for project development):
   ```bash
   make serve-dev
   ```

3. Start the API server (for external use):
   ```bash
   make serve
   ```

## Configuration

See @.agents/default.mcp.json for the configuration template. Both servers are defined:

```json
{
  "mcpServers": {
    "<project-name>-dev": { ... },  // Dev server
    "<project-name>": { ... }       // API server
  }
}
```

## Related Documentation

- @.agents/docs/mcp/dev-server.md - Dev server details
- @.agents/docs/mcp/api-server.md - API server details
- @.agents/docs/mcp/patterns.md - Common MCP patterns
- @.agents/commands/deploy-mcp.md - Deployment guide

