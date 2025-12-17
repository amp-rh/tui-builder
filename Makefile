.PHONY: help install dev test lint format check serve serve-dev build run mcp-container mcp-serve clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Install with dev dependencies
	uv sync --extra dev

mcp: ## Install with MCP dependencies
	uv sync --extra mcp

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

serve: ## Serve API MCP server locally (external interface)
	# TODO: Update path to your package name
	uv run python src/my_package/mcp_server.py

serve-dev: ## Serve dev MCP server locally (project development)
	# TODO: Update path to your package name
	uv run python src/my_package/dev_mcp.py

build: ## Build container image
	podman build -t python-project-template:latest .

run: ## Run container
	podman run --rm -p 8000:8000 python-project-template:latest

mcp-container: ## Build MCP server container
	# TODO: Update image name to your project
	podman build -t my-project-mcp:latest .

mcp-serve: mcp-container ## Build and serve MCP server container
	# TODO: Update image name to your project
	podman run --rm -p 8000:8000 my-project-mcp:latest

clean: ## Clean up build artifacts
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
