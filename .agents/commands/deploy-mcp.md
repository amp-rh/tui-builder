# /deploy-mcp

Deploy the MCP servers locally or to a container.

## Purpose

Build and deploy the MCP (Model Context Protocol) servers for local development or production use.

## Server Types

| Server | Command | Purpose |
|--------|---------|---------|
| Dev Server | `make serve-dev` | Tools for developing this project |
| API Server | `make serve` | External interface for other agents |

See @.agents/docs/mcp/overview.md for architecture details.

## Steps

### Local Development (Editable)

1. **Ensure dependencies**: Run `uv sync --extra mcp`
2. **Generate mcp.json**: If `.agents/mcp.json` doesn't exist, run the generation script below
3. **Start server**:
   - Dev server: `make serve-dev`
   - API server: `make serve`
4. **Verify**: Server should start on stdio transport

### Container Deployment

1. **Build image**: Run `make mcp-container`
2. **Run container**: Run `make mcp-serve`
3. **Verify**: Server should be accessible on port 8000

Note: Container deployment uses the API server by default. For dev server in container, modify the CMD in Containerfile.

## Generate mcp.json

```bash
# Get project info
PROJECT_NAME=$(basename $(pwd))
PROJECT_PATH=$(pwd)
PACKAGE_NAME=$(ls src/ | grep -v __pycache__ | grep -v __init__.py | grep -v AGENTS.md | head -1)

# Generate mcp.json with both servers
cat > .agents/mcp.json << EOF
{
  "mcpServers": {
    "${PROJECT_NAME}-dev": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${PROJECT_PATH}",
        "python",
        "src/${PACKAGE_NAME}/dev_mcp.py"
      ]
    },
    "${PROJECT_NAME}": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${PROJECT_PATH}",
        "python",
        "src/${PACKAGE_NAME}/mcp_server.py"
      ]
    }
  }
}
EOF
```

## Cursor Integration

To use with Cursor IDE, add the contents of `.agents/mcp.json` to your Cursor MCP settings.

Both servers will appear:
- `<project>-dev` - Use when developing this project
- `<project>` - Use when consuming this project's API

## Verification

Test the servers are working:

```bash
# Dev server
make serve-dev

# API server
make serve

# Container (API server)
make mcp-serve
```

The server should output MCP protocol messages on stdio.

## Rules

- MUST have `mcp[cli]` installed (`uv sync --extra mcp`)
- MUST have both `dev_mcp.py` and `mcp_server.py` in the package
- MUST generate `mcp.json` before first use
- SHOULD use container for production deployments

## Related

- @.agents/default.mcp.json - MCP config template
- @.agents/AGENTS.md - MCP configuration instructions
- @.agents/docs/mcp/overview.md - MCP architecture
- @.agents/docs/mcp/dev-server.md - Dev server guide
- @.agents/docs/mcp/api-server.md - API server guide
- @src/my_package/dev_mcp.py - Dev server implementation
- @src/my_package/mcp_server.py - API server implementation
- @Containerfile - Container build definition
- @Makefile - Build and run commands
