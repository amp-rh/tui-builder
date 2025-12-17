"""Component documentation resources."""

from mcp.server.fastmcp import FastMCP

# Widget documentation
WIDGET_DOCS: dict[str, dict] = {
    "Button": {
        "description": "A clickable button widget that can trigger actions.",
        "example": """
from textual.widgets import Button

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Button("Click Me", id="my-button", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "my-button":
            self.notify("Button clicked!")
""",
        "properties": ["label", "variant", "disabled"],
        "events": ["Button.Pressed"],
    },
    "Input": {
        "description": "A text input field for user text entry.",
        "example": """
from textual.widgets import Input

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter text...", id="my-input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.notify(f"You entered: {event.value}")
""",
        "properties": ["value", "placeholder", "password", "max_length"],
        "events": ["Input.Changed", "Input.Submitted"],
    },
    "Static": {
        "description": "A widget for displaying static content with Rich markup.",
        "example": """
from textual.widgets import Static

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Static("[bold]Hello[/bold] World!", id="greeting")
""",
        "properties": ["renderable"],
        "events": [],
    },
    "Label": {
        "description": "A simple text label widget.",
        "example": """
from textual.widgets import Label

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Label("Username:")
""",
        "properties": ["renderable"],
        "events": [],
    },
    "DataTable": {
        "description": "A table widget for displaying tabular data.",
        "example": """
from textual.widgets import DataTable

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable(id="my-table")

    def on_mount(self) -> None:
        table = self.query_one("#my-table", DataTable)
        table.add_columns("Name", "Age", "City")
        table.add_rows([
            ("Alice", 30, "New York"),
            ("Bob", 25, "London"),
        ])
""",
        "properties": ["cursor_type", "zebra_stripes", "show_header"],
        "events": ["DataTable.RowSelected", "DataTable.CellSelected"],
    },
    "TextArea": {
        "description": "A multi-line text editor widget.",
        "example": """
from textual.widgets import TextArea

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield TextArea(id="editor")
""",
        "properties": ["text", "language", "show_line_numbers"],
        "events": ["TextArea.Changed"],
    },
    "Switch": {
        "description": "A toggle switch widget for boolean values.",
        "example": """
from textual.widgets import Switch

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Switch(value=True, id="dark-mode")

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.notify(f"Switch is now: {event.value}")
""",
        "properties": ["value"],
        "events": ["Switch.Changed"],
    },
    "ProgressBar": {
        "description": "A progress bar widget to show task progress.",
        "example": """
from textual.widgets import ProgressBar

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield ProgressBar(total=100, id="progress")

    async def update_progress(self) -> None:
        bar = self.query_one("#progress", ProgressBar)
        bar.advance(10)
""",
        "properties": ["total", "progress", "show_eta"],
        "events": [],
    },
}

# Container documentation
CONTAINER_DOCS: dict[str, dict] = {
    "Container": {
        "description": "A generic container widget for grouping other widgets.",
        "example": """
from textual.containers import Container

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("Item 1"),
            Static("Item 2"),
            id="my-container"
        )
""",
    },
    "Horizontal": {
        "description": "A container that arranges children horizontally.",
        "example": """
from textual.containers import Horizontal

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("Left"),
            Button("Center"),
            Button("Right"),
        )
""",
    },
    "Vertical": {
        "description": "A container that arranges children vertically.",
        "example": """
from textual.containers import Vertical

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Top"),
            Static("Middle"),
            Static("Bottom"),
        )
""",
    },
    "Grid": {
        "description": "A container that arranges children in a CSS grid.",
        "example": '''
from textual.containers import Grid

class MyApp(App):
    CSS = """
    Grid {
        grid-size: 2 2;
        grid-gutter: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Cell 1"),
            Static("Cell 2"),
            Static("Cell 3"),
            Static("Cell 4"),
        )
''',
    },
    "ScrollableContainer": {
        "description": "A container with scrolling capability.",
        "example": """
from textual.containers import ScrollableContainer

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            *[Static(f"Line {i}") for i in range(100)]
        )
""",
    },
}


def get_widget_docs(widget_name: str) -> dict | None:
    """Get documentation for a widget.

    Args:
        widget_name: Name of the widget (e.g., "Button").

    Returns:
        Documentation dict or None if not found.
    """
    return WIDGET_DOCS.get(widget_name)


def get_container_docs(container_name: str) -> dict | None:
    """Get documentation for a container.

    Args:
        container_name: Name of the container (e.g., "Horizontal").

    Returns:
        Documentation dict or None if not found.
    """
    return CONTAINER_DOCS.get(container_name)


def register_component_resources(mcp: FastMCP) -> None:
    """Register component documentation resources."""

    @mcp.resource("tui://widgets/{name}")
    def widget_resource(name: str) -> str:
        """Get widget documentation."""
        docs = get_widget_docs(name)
        if docs is None:
            return f"Widget '{name}' not found."
        return f"""# {name}

{docs["description"]}

## Example

```python
{docs["example"]}
```

## Properties
{", ".join(docs.get("properties", []))}

## Events
{", ".join(docs.get("events", []))}
"""

    @mcp.resource("tui://containers/{name}")
    def container_resource(name: str) -> str:
        """Get container documentation."""
        docs = get_container_docs(name)
        if docs is None:
            return f"Container '{name}' not found."
        return f"""# {name}

{docs["description"]}

## Example

```python
{docs["example"]}
```
"""
