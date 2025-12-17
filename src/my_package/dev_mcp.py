"""Dev MCP Server for project development.

This server provides tools for agents developing and maintaining this project.
For external/domain-specific tools, see mcp_server.py.

See @AGENTS.md for project-wide rules.
See @.agents/docs/mcp/dev-server.md for usage guide.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# Initialize the dev MCP server
# TODO: Update the server name to match your project
mcp = FastMCP("my-project-dev")


# =============================================================================
# Testing & Quality Tools
# =============================================================================


@mcp.tool()
def run_tests(path: str | None = None) -> dict[str, Any]:
    """Run pytest tests.

    Args:
        path: Optional specific test path (e.g., 'tests/test_example.py').

    Returns:
        Test results including stdout, stderr, and exit code.
    """
    cmd = ["uv", "run", "pytest", "-v"]
    if path:
        cmd.append(path)

    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "success": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


@mcp.tool()
def run_lint(fix: bool = False) -> dict[str, Any]:
    """Run ruff linter.

    Args:
        fix: If True, automatically fix issues.

    Returns:
        Lint results including any issues found.
    """
    cmd = ["uv", "run", "ruff", "check", "."]
    if fix:
        cmd.append("--fix")

    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "success": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


@mcp.tool()
def format_code(path: str | None = None) -> dict[str, Any]:
    """Format code with ruff.

    Args:
        path: Optional specific path to format.

    Returns:
        Format results.
    """
    target = path or "."
    result = subprocess.run(
        ["uv", "run", "ruff", "format", target], capture_output=True, text=True
    )
    return {
        "success": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# =============================================================================
# Task Management Tools
# =============================================================================


def _get_tasks_dir() -> Path:
    """Get the tasks directory path."""
    return Path(".agents/tasks")


@mcp.tool()
def list_tasks(status: str | None = None) -> dict[str, Any]:
    """List all tasks.

    Args:
        status: Optional filter by status ('pending', 'in_progress', 'completed').

    Returns:
        List of tasks with their details.
    """
    tasks_dir = _get_tasks_dir()
    if not tasks_dir.exists():
        return {"tasks": [], "count": 0}

    tasks = []
    for task_file in tasks_dir.glob("*.md"):
        content = task_file.read_text()
        # Parse basic task info from frontmatter if present
        task_info = {"id": task_file.stem, "file": str(task_file)}

        # Simple frontmatter parsing
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        task_info[key.strip()] = value.strip()

        # Filter by status if specified
        if status and task_info.get("status") != status:
            continue

        tasks.append(task_info)

    return {"tasks": tasks, "count": len(tasks)}


@mcp.tool()
def add_task(title: str, description: str | None = None) -> dict[str, Any]:
    """Create a new task.

    Args:
        title: Task title.
        description: Optional task description.

    Returns:
        Created task info.
    """
    tasks_dir = _get_tasks_dir()
    tasks_dir.mkdir(parents=True, exist_ok=True)

    # Generate task ID from timestamp
    task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_file = tasks_dir / f"{task_id}.md"

    content = f"""---
title: {title}
status: pending
created: {datetime.now().isoformat()}
---

# {title}

{description or "No description provided."}
"""

    task_file.write_text(content)
    return {"success": True, "task_id": task_id, "file": str(task_file)}


@mcp.tool()
def complete_task(task_id: str) -> dict[str, Any]:
    """Mark a task as completed.

    Args:
        task_id: The task ID to complete.

    Returns:
        Updated task info.
    """
    tasks_dir = _get_tasks_dir()
    task_file = tasks_dir / f"{task_id}.md"

    if not task_file.exists():
        return {"success": False, "error": f"Task not found: {task_id}"}

    content = task_file.read_text()
    # Update status in frontmatter
    content = content.replace("status: pending", "status: completed")
    content = content.replace("status: in_progress", "status: completed")
    task_file.write_text(content)

    return {"success": True, "task_id": task_id, "status": "completed"}


# =============================================================================
# Project Management Tools
# =============================================================================


@mcp.tool()
def add_learning(category: str, title: str, content: str) -> dict[str, Any]:
    """Add a new learning to the project.

    Args:
        category: Category (e.g., 'patterns', 'gotchas', 'decisions', 'tips').
        title: Short title for the learning.
        content: The learning content.

    Returns:
        Created learning info.
    """
    learnings_dir = Path(".agents/learnings")
    learnings_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename from title
    filename = title.lower().replace(" ", "-")[:50]
    learning_file = learnings_dir / f"{filename}.md"

    # Avoid overwriting
    counter = 1
    while learning_file.exists():
        learning_file = learnings_dir / f"{filename}-{counter}.md"
        counter += 1

    file_content = f"""# {title}

**Category:** {category}
**Date:** {datetime.now().strftime("%Y-%m-%d")}

## Learning

{content}
"""

    learning_file.write_text(file_content)
    return {"success": True, "file": str(learning_file), "category": category}


@mcp.tool()
def create_from_template(
    template: str, destination: str, variables: dict[str, str] | None = None
) -> dict[str, Any]:
    """Create a file from a template.

    Args:
        template: Template filename in .agents/templates/.
        destination: Destination path for the new file.
        variables: Optional dict of variables to substitute ({{var_name}}).

    Returns:
        Created file info.
    """
    templates_dir = Path(".agents/templates")
    template_file = templates_dir / template

    if not template_file.exists():
        available = [f.name for f in templates_dir.glob("*") if f.is_file()]
        return {
            "success": False,
            "error": f"Template not found: {template}",
            "available": available,
        }

    dest_path = Path(destination)
    if dest_path.exists():
        return {"success": False, "error": f"Destination already exists: {destination}"}

    content = template_file.read_text()

    # Substitute variables
    if variables:
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", value)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(content)

    return {"success": True, "file": str(dest_path), "template": template}


# =============================================================================
# Resources
# =============================================================================


@mcp.resource("config://pyproject")
def get_pyproject() -> str:
    """Get the project configuration.

    Returns:
        Contents of pyproject.toml.
    """
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return "# pyproject.toml not found"
    return pyproject.read_text()


@mcp.resource("docs://agents")
def get_root_agents_md() -> str:
    """Get the root AGENTS.md file.

    Returns:
        Contents of AGENTS.md.
    """
    agents_md = Path("AGENTS.md")
    if not agents_md.exists():
        return "# AGENTS.md not found"
    return agents_md.read_text()


@mcp.resource("docs://agents/{path}")
def get_agents_md(path: str) -> str:
    """Get a specific AGENTS.md file.

    Args:
        path: Path to the AGENTS.md (e.g., 'src' for src/AGENTS.md).

    Returns:
        Contents of the AGENTS.md file.
    """
    agents_file = Path(path) / "AGENTS.md"
    if not agents_file.exists():
        return f"# AGENTS.md not found at {path}"
    return agents_file.read_text()


@mcp.resource("tasks://list")
def get_tasks_list() -> str:
    """Get the current task list as JSON.

    Returns:
        JSON array of tasks.
    """
    result = list_tasks()
    return json.dumps(result, indent=2)


@mcp.resource("learnings://all")
def get_all_learnings() -> str:
    """Get all project learnings.

    Returns:
        Combined learnings content.
    """
    learnings_dir = Path(".agents/learnings")
    if not learnings_dir.exists():
        return "# No learnings yet"

    content_parts = ["# Project Learnings\n"]
    for learning_file in sorted(learnings_dir.glob("*.md")):
        content_parts.append(f"\n---\n\n{learning_file.read_text()}")

    return "\n".join(content_parts)


# =============================================================================
# Prompts
# =============================================================================


@mcp.prompt()
def code_review(code: str) -> str:
    """Review code against project standards.

    Args:
        code: The code to review.

    Returns:
        A prompt for reviewing the code.
    """
    return f"""Review this code against our project standards.

## Project Standards

- Use type hints on all public functions
- Follow naming conventions (snake_case for functions/variables, PascalCase for classes)
- Handle errors with try/except, return error info don't crash
- Add docstrings to public functions with Args/Returns sections
- Use logging instead of print() for operational output

## Code to Review

```python
{code}
```

## Your Review

Provide specific, actionable feedback covering:
1. Type hint completeness
2. Naming convention adherence
3. Error handling adequacy
4. Documentation quality
5. Any potential bugs or issues
"""


@mcp.prompt()
def implement_feature(description: str) -> str:
    """Guide for implementing a new feature.

    Args:
        description: Description of the feature to implement.

    Returns:
        A prompt guiding feature implementation.
    """
    return f"""I need to implement a new feature in this project.

## Feature Description

{description}

## Implementation Guide

Please help me implement this by:

1. **Understanding Requirements**
   - What are the inputs and outputs?
   - What edge cases should we handle?

2. **Identifying Affected Files**
   - Which existing files need modification?
   - What new files should be created?

3. **Planning the Implementation**
   - What's the logical order of changes?
   - What dependencies exist between components?

4. **Writing the Code**
   - Follow project conventions (see AGENTS.md)
   - Add proper type hints and docstrings
   - Handle errors gracefully

5. **Adding Tests**
   - What unit tests are needed?
   - What edge cases should be tested?

## Project Context

This project uses:
- Python with uv for package management
- pytest for testing
- ruff for linting/formatting
- Type hints on all public functions

Start by analyzing the requirements and proposing an implementation plan.
"""


if __name__ == "__main__":
    mcp.run()
