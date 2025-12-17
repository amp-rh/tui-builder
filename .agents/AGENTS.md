# AGENTS.md - Agent Resources

See @AGENTS.md for project-wide rules.

## Overview

This directory contains resources for AI agents working on this project.

## Structure

```
.agents/
├── AGENTS.md           # This file
├── commands/           # Slash command definitions
│   └── AGENTS.md       # Command index and format
├── docs/               # Granular documentation
│   ├── tooling/        # uv, pytest, ruff
│   ├── patterns/       # Error handling, typing, logging
│   ├── conventions/    # Naming, imports, structure
│   ├── workflows/      # PR process, testing, releases
│   ├── architecture/   # Design decisions
│   └── mcp/            # MCP server documentation
├── learnings/          # Discovered patterns and insights
├── plans/              # Implementation plans
├── scratch/            # Working space (mostly gitignored)
│   └── AGENTS.md       # Scratch workspace guide
├── tasks/              # Task tracking
├── templates/          # Reusable templates
├── default.mcp.json    # MCP server config template
└── mcp.json            # Generated - actual MCP config (gitignored)
```

## MCP Servers

This project supports two MCP servers:

| Server | File | Purpose |
|--------|------|---------|
| Dev Server | `dev_mcp.py` | Tools for developing this project |
| API Server | `mcp_server.py` | External interface for other agents |

See @.agents/docs/mcp/overview.md for architecture details.

### Quick Start

```bash
# Install MCP dependencies
uv sync --extra mcp

# Start dev server (for project development)
make serve-dev

# Start API server (external interface)
make serve
```

## MCP Server Configuration

The `default.mcp.json` file is a template with placeholders. Agents should generate `mcp.json` with actual project values:

1. Copy `default.mcp.json` to `mcp.json`
2. Replace `<project-name>` with the actual project name
3. Replace `<absolute-path-to-project>` with the full path to the project
4. Replace `<package_name>` with the Python package name from `src/`

Example:
```json
{
  "mcpServers": {
    "my-project-dev": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/project", "python", "src/my_package/dev_mcp.py"]
    },
    "my-project": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/project", "python", "src/my_package/mcp_server.py"]
    }
  }
}
```

## Directory Index

- @.agents/commands/AGENTS.md - Slash commands
- @.agents/docs/ - Documentation (see root @AGENTS.md for full index)
- @.agents/docs/mcp/ - MCP server documentation
- @.agents/learnings/ - Discovered patterns and insights
- @.agents/plans/ - Implementation plans
- @.agents/scratch/AGENTS.md - Working space
- @.agents/tasks/ - Task tracking
- @.agents/templates/ - Reusable templates
- @.agents/default.mcp.json - MCP config template
