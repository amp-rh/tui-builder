# /extract-mcp-prompts

Extract and create MCP prompts from the codebase.

## Purpose

Identify common interaction patterns and create reusable MCP prompts that guide agent behavior for specific tasks.

## Which Server?

| Prompt Type | Server | File |
|-------------|--------|------|
| Project development (code review, implementation) | Dev Server | `dev_mcp.py` |
| Domain-specific (your project's workflows) | API Server | `mcp_server.py` |

See @.agents/docs/mcp/overview.md for architecture details.

## Steps

1. **Analyze patterns**: Review common tasks and workflows
2. **Identify candidates**: Look for:
   - Repetitive multi-step operations
   - Tasks requiring specific context
   - Workflows with consistent structure
   - Domain-specific operations
3. **Choose server**: Dev prompts → `dev_mcp.py`, Domain prompts → `mcp_server.py`
4. **Create prompt definitions**: Add `@mcp.prompt()` decorated functions
5. **Add documentation**: Write clear descriptions
6. **Test prompts**: Verify prompts produce useful output

## Prompt Candidates

Good MCP prompts:
- **Task-oriented**: Guide completion of specific tasks
- **Contextual**: Include relevant project context
- **Structured**: Provide clear steps or format
- **Reusable**: Apply to multiple similar situations

### Examples of Good Prompts

**Dev Server (dev_mcp.py):**
- Code review checklist for this project
- Feature implementation guide
- Debugging workflow for common issues

**API Server (mcp_server.py):**
- Domain-specific query construction
- Data analysis workflows
- Integration patterns

## Prompt Template

```python
@mcp.prompt()
def prompt_name(param1: str) -> str:
    """Short description of what this prompt helps with.

    Args:
        param1: Context or input for the prompt.

    Returns:
        A formatted prompt string.
    """
    return f"""You are helping with {param1}.

## Context
This project uses...

## Task
Please...

## Format
Respond with...
"""
```

## Prompt with Messages

```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt()
def review_code(code: str) -> list[base.Message]:
    """Review code against project standards.

    Args:
        code: The code to review.
    """
    return [
        base.UserMessage(f"Please review this code:\n\n```\n{code}\n```"),
        base.AssistantMessage("I'll review this against the project standards..."),
    ]
```

## Output Location

**Dev prompts** → Add to `src/<package_name>/dev_mcp.py`:

```python
# In dev_mcp.py
@mcp.prompt()
def code_review(code: str) -> str:
    """Review code against project standards."""
    ...
```

**Domain prompts** → Add to `src/<package_name>/mcp_server.py`:

```python
# In mcp_server.py
@mcp.prompt()
def query_guide(query_type: str) -> str:
    """Guide for constructing domain queries."""
    ...
```

## Rules

- MUST have clear descriptions
- MUST include relevant project context
- MUST choose the correct server (dev vs API)
- SHOULD be specific to this project's needs
- SHOULD NOT duplicate generic prompts available elsewhere

## Related

- @.agents/docs/mcp/overview.md - MCP architecture
- @.agents/docs/mcp/dev-server.md - Dev server prompts
- @.agents/docs/mcp/api-server.md - API server prompts
- @.agents/docs/mcp/patterns.md - Implementation patterns
- @src/my_package/dev_mcp.py - Dev server implementation
- @src/my_package/mcp_server.py - API server implementation
- @.agents/commands/deploy-mcp.md - Deploy the servers
- @.agents/commands/extract-mcp-tools.md - Extract tools
- @.agents/commands/extract-mcp-resources.md - Extract resources
