.PHONY: help install dev test lint format check app serve serve-dev console build run mcp-container mcp-serve mcp-deeplink clean

# GitHub repo URL for uvx install
REPO_URL ?= https://github.com/amp-rh/tui-builder
MCP_NAME ?= tui-builder

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Install with dev dependencies
	uv sync --extra dev

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .
	uv run ruff check --fix .

check: lint test ## Run all checks (lint + test)

app: ## Run the TUI Builder application
	uv run tui-builder

console: ## Run Textual dev console (for debugging)
	uv run textual console

serve: ## Serve MCP server locally
	uv run python src/tui_builder/mcp_server.py

serve-dev: ## Serve dev MCP server locally
	uv run python src/tui_builder/dev_mcp.py

build: ## Build container image
	podman build -t tui-builder:latest .

run: ## Run container
	podman run --rm -it tui-builder:latest

mcp-container: ## Build MCP server container
	podman build -t tui-builder-mcp:latest .

mcp-serve: mcp-container ## Build and serve MCP server container
	podman run --rm -p 8000:8000 tui-builder-mcp:latest

mcp-deeplink: ## Generate Cursor install deeplink for MCP server
	@echo "Generating Cursor MCP install deeplink..."
	@CONFIG='{"command":"uvx","args":["--from","git+$(REPO_URL)","tui-builder-mcp"]}'; \
	ENCODED=$$(echo -n "$$CONFIG" | python3 -c "import sys,base64;print(base64.b64encode(sys.stdin.read().encode()).decode())"); \
	echo ""; \
	echo "Click this link to install in Cursor:"; \
	echo ""; \
	echo "  cursor://anysphere.cursor-deeplink/mcp/install?name=$(MCP_NAME)&config=$$ENCODED"; \
	echo ""; \
	echo "Or add this to your Cursor MCP settings manually:"; \
	echo ""; \
	echo "  $$CONFIG" | python3 -m json.tool; \
	echo ""

clean: ## Clean up build artifacts
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
