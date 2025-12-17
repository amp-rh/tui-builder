# TUI Builder

An MCP server providing prompts, resources, and tools for building high-quality TUI (Text User Interface) applications with Textual.

## Features

- **14 MCP Tools**: Generate widgets, screens, apps; validate CSS; run tests
- **6 MCP Prompts**: Guided workflows for design and debugging
- **Rich Resources**: Widget docs, CSS reference, layout patterns
- **Modern Python Tooling**: uv, pytest, ruff
- **95 Tests**: TDD-developed with comprehensive coverage

## Quick Start

```bash
# Install dependencies
uv sync --extra dev

# Run tests
make test

# Start MCP server
make serve
```

## MCP Capabilities

### Tools

| Category | Tools |
|----------|-------|
| **Generation** | `list_widgets`, `list_containers`, `generate_widget`, `generate_screen`, `generate_app` |
| **Validation** | `validate_css`, `lint_widget`, `check_accessibility` |
| **Testing** | `run_app_pilot`, `take_snapshot`, `simulate_keys`, `simulate_click`, `generate_test_cases`, `compare_snapshots` |

### Resources

| URI | Description |
|-----|-------------|
| `tui://widgets/{name}` | Widget documentation |
| `tui://containers/{name}` | Container documentation |
| `tui://css/properties` | CSS properties reference |
| `tui://css/selectors` | CSS selectors reference |
| `tui://css/variables` | Theme variables reference |
| `tui://patterns/layouts` | Layout pattern examples |

### Prompts

| Prompt | Purpose |
|--------|---------|
| `design_layout` | Guide through TUI layout design |
| `create_widget` | Step-by-step widget creation |
| `design_form` | Form layout and validation design |
| `debug_layout` | Troubleshoot layout issues |
| `debug_styling` | Fix CSS/styling problems |
| `optimize_app` | Performance optimization guidance |

## Project Structure

```
src/tui_builder/
├── mcp_server.py          # Main MCP server entry point
├── tools/
│   ├── generate.py        # Code generation tools
│   ├── validate.py        # CSS/layout validation
│   └── testing.py         # Snapshot, unit, interactive testing
├── resources/
│   ├── components.py      # Widget/container documentation
│   ├── css.py             # CSS property reference
│   └── patterns.py        # Design patterns and examples
├── prompts/
│   ├── design.py          # Layout design workflows
│   └── debug.py           # Troubleshooting workflows
└── app.py                 # Demo TUI app
```

## Example Usage

Generate a new app:

```python
from tui_builder.tools.generate import generate_app

code = generate_app("MyDashboard", with_sidebar=True)
print(code)
```

Validate CSS:

```python
from tui_builder.tools.validate import validate_css

result = validate_css("Button { background: $primary; }")
print(f"Valid: {result.valid}")
```

## Make Targets

```bash
make help          # Show all targets
make app           # Run the TUI Builder demo app
make serve         # Start MCP server
make serve-dev     # Start dev MCP server
make test          # Run tests
make lint          # Run linting
make format        # Format code
```

## License

Apache License 2.0 - see [LICENSE](LICENSE)
