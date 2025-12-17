"""Design pattern resources."""

from mcp.server.fastmcp import FastMCP

# Layout patterns
LAYOUT_PATTERNS: list[dict] = [
    {
        "name": "Sidebar Layout",
        "description": "A layout with a fixed sidebar and main content area.",
        "code": '''
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

class SidebarApp(App):
    CSS = """
    #sidebar {
        width: 30;
        background: $surface;
        border-right: solid $primary;
        padding: 1;
    }
    #main {
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Static("Sidebar", id="sidebar"),
            Static("Main Content", id="main"),
        )
''',
    },
    {
        "name": "Header/Content/Footer",
        "description": "Classic layout with header, main content, and footer.",
        "code": """
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static

class StandardApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(Static("Main Content"), id="content")
        yield Footer()
""",
    },
    {
        "name": "Card Grid",
        "description": "A grid of card-style widgets.",
        "code": '''
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Static

class CardGridApp(App):
    CSS = """
    Grid {
        grid-size: 3;
        grid-gutter: 1;
        padding: 1;
    }
    .card {
        background: $surface;
        border: solid $primary;
        padding: 1;
        height: 10;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            *[Static(f"Card {i}", classes="card") for i in range(6)]
        )
''',
    },
    {
        "name": "Modal Dialog",
        "description": "A modal screen that appears over the main content.",
        "code": '''
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static

class ConfirmDialog(ModalScreen):
    CSS = """
    ConfirmDialog {
        align: center middle;
    }
    #dialog {
        background: $surface;
        border: solid $primary;
        padding: 1 2;
        width: 50;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Are you sure?"),
            Button("Yes", id="yes", variant="primary"),
            Button("No", id="no"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")
''',
    },
    {
        "name": "Tabbed Interface",
        "description": "Content organized in tabs.",
        "code": """
from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Static

class TabbedApp(App):
    def compose(self) -> ComposeResult:
        yield TabbedContent(
            TabPane("Home", Static("Home content"), id="home"),
            TabPane("Settings", Static("Settings content"), id="settings"),
            TabPane("About", Static("About content"), id="about"),
        )
""",
    },
    {
        "name": "Form Layout",
        "description": "A form with labeled inputs.",
        "code": '''
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Label, Button

class FormApp(App):
    CSS = """
    Vertical {
        padding: 1 2;
    }
    Label {
        margin-top: 1;
    }
    Input {
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Username:"),
            Input(placeholder="Enter username", id="username"),
            Label("Password:"),
            Input(placeholder="Enter password", password=True, id="password"),
            Button("Submit", variant="primary"),
        )
''',
    },
]


def get_layout_patterns() -> list[dict]:
    """Get layout pattern examples.

    Returns:
        List of layout pattern dictionaries.
    """
    return LAYOUT_PATTERNS.copy()


def register_pattern_resources(mcp: FastMCP) -> None:
    """Register design pattern resources."""

    @mcp.resource("tui://patterns/layouts")
    def layout_patterns_resource() -> str:
        """Get layout patterns reference."""
        lines = ["# Textual Layout Patterns\n"]
        for pattern in LAYOUT_PATTERNS:
            lines.append(f"## {pattern['name']}")
            lines.append(f"{pattern['description']}\n")
            lines.append("```python")
            lines.append(pattern["code"])
            lines.append("```\n")
        return "\n".join(lines)
