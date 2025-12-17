.PHONY: help install dev test lint format check app serve serve-dev console build run mcp-container mcp-serve clean

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

clean: ## Clean up build artifacts
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
