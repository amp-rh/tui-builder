# TUI Builder

A TUI (Text User Interface) builder application.

## Features

- **AGENTS.md System**: Hierarchical documentation indexes for AI agents
- **Dual MCP Servers**: Dev server for project development, API server for external interface
- **Modern Python Tooling**: uv, pytest, ruff
- **Container Support**: Rootless UBI9 S2I container builds
- **Agent Workspace**: Structured scratch space with templates

## Quick Start

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/amp-rh/tui-builder.git
cd tui-builder
uv sync --extra dev

# Run tests
make test

# Run linting
make lint
```

## Project Structure

```
├── AGENTS.md           # AI agent guidance (start here)
├── .agents/            # Agent-specific resources
│   ├── commands/       # Slash command definitions
│   ├── docs/           # Granular documentation
│   │   ├── tooling/    # uv, pytest, ruff
│   │   ├── patterns/   # Code patterns
│   │   ├── conventions/# Naming, imports
│   │   ├── workflows/  # PR, testing, releases, contributing
│   │   ├── architecture/# Design decisions
│   │   └── mcp/        # MCP server documentation
│   ├── learnings/      # Discovered patterns
│   ├── scratch/        # Agent working space
│   └── templates/      # Reusable templates
├── src/tui_builder/    # Source code
│   ├── dev_mcp.py      # Dev MCP server
│   └── mcp_server.py   # API MCP server
└── tests/              # Tests
```

## For AI Agents

This project uses AGENTS.md files as indexes. Before making changes:

1. Read the `AGENTS.md` in the directory you're working in
2. Follow linked documentation in `.agents/docs/`
3. Update docs when patterns are learned

See [AGENTS.md](AGENTS.md) for the root index.

## MCP Servers

Two MCP servers are provided:

| Server | Command | Purpose |
|--------|---------|---------|
| Dev Server | `make serve-dev` | Tools for developing this project |
| API Server | `make serve` | External interface for other agents |

```bash
# Install MCP dependencies
uv sync --extra mcp

# Start dev server
make serve-dev

# Start API server
make serve
```

## Using This Template

1. **Create from template** or clone this repository
2. **Rename package**: Already done (`src/tui_builder`)
3. **Update references**: Already done
4. **Update pyproject.toml**: Change name, description, authors
5. **Generate MCP config**: Run the script in `.agents/commands/deploy-mcp.md`

## Make Targets

```bash
make help          # Show all targets
make install       # Install dependencies
make dev           # Install with dev dependencies
make mcp           # Install with MCP dependencies
make test          # Run tests
make lint          # Run linting
make format        # Format code
make serve         # Start API MCP server
make serve-dev     # Start dev MCP server
make mcp-serve     # Build and run container
```

## Contributing

See [.agents/docs/workflows/contributing.md](.agents/docs/workflows/contributing.md) for agent contribution guidelines.

## License

Apache License 2.0 - see [LICENSE](LICENSE)
