"""Code generation tools for TUI applications."""

from mcp.server.fastmcp import FastMCP

# Available Textual widgets for reference
TEXTUAL_WIDGETS: dict[str, str] = {
    "Button": "A clickable button widget",
    "Input": "A text input field",
    "Label": "A simple text label",
    "Static": "A widget for static content with Rich markup",
    "TextArea": "A multi-line text editor",
    "Switch": "A toggle switch",
    "Checkbox": "A checkbox widget",
    "RadioButton": "A radio button (use with RadioSet)",
    "RadioSet": "A container for radio buttons",
    "Select": "A dropdown select widget",
    "SelectionList": "A list with selectable items",
    "OptionList": "A list of options",
    "ListView": "A vertical list of items",
    "DataTable": "A table for displaying data",
    "Tree": "A tree view widget",
    "DirectoryTree": "A tree view for file system navigation",
    "Markdown": "A widget for rendering Markdown",
    "MarkdownViewer": "A Markdown viewer with scrolling",
    "RichLog": "A log widget with Rich formatting",
    "Log": "A simple log widget",
    "ProgressBar": "A progress bar",
    "LoadingIndicator": "A loading spinner",
    "Sparkline": "A sparkline chart",
    "Digits": "Large digit display",
    "Rule": "A horizontal rule/divider",
    "Placeholder": "A placeholder widget for layouts",
    "Pretty": "Pretty-print Python objects",
    "Collapsible": "A collapsible container",
    "TabbedContent": "Tabbed content panels",
    "ContentSwitcher": "Switch between content views",
}

TEXTUAL_CONTAINERS: dict[str, str] = {
    "Container": "A generic container",
    "Horizontal": "Arrange children horizontally",
    "Vertical": "Arrange children vertically",
    "Grid": "A CSS grid container",
    "Center": "Center content horizontally and vertically",
    "Middle": "Center content vertically",
    "ScrollableContainer": "A scrollable container",
    "VerticalScroll": "Vertical scrolling container",
    "HorizontalScroll": "Horizontal scrolling container",
}


def list_widgets() -> dict[str, str]:
    """List all available Textual widgets with descriptions.

    Returns:
        Dictionary mapping widget names to their descriptions.
    """
    return TEXTUAL_WIDGETS.copy()


def list_containers() -> dict[str, str]:
    """List all available Textual containers with descriptions.

    Returns:
        Dictionary mapping container names to their descriptions.
    """
    return TEXTUAL_CONTAINERS.copy()


def _to_class_name(name: str) -> str:
    """Convert a name to a proper class name."""
    if name[0].isupper() and "_" not in name:
        return name
    return name.title().replace("_", "")


def generate_widget(
    name: str,
    widget_type: str = "Static",
    with_css: bool = True,
    with_bindings: bool = False,
) -> str:
    """Generate a custom widget class.

    Args:
        name: Name for the custom widget class (e.g., "StatusBar").
        widget_type: Base widget to extend (default: "Static").
        with_css: Include example CSS styling.
        with_bindings: Include example key bindings.

    Returns:
        Python code for the custom widget.
    """
    class_name = _to_class_name(name)

    css_block = ""
    if with_css:
        css_block = f'''
    CSS = """
    {class_name} {{
        padding: 1 2;
        background: $surface;
        border: solid $primary;
    }}
    """
'''

    bindings_block = ""
    if with_bindings:
        bindings_block = '''
    BINDINGS = [
        ("enter", "activate", "Activate"),
    ]

    def action_activate(self) -> None:
        """Handle activation."""
        self.notify("Activated!")
'''

    return f'''"""Custom {class_name} widget."""

from textual.app import ComposeResult
from textual.widgets import {widget_type}


class {class_name}({widget_type}):
    """{class_name} widget."""
{css_block}{bindings_block}
    def compose(self) -> ComposeResult:
        """Compose the widget content."""
        yield {widget_type}("Content here")
'''


def generate_screen(
    name: str,
    modal: bool = False,
    with_header_footer: bool = True,
) -> str:
    """Generate a screen class.

    Args:
        name: Name for the screen class (e.g., "SettingsScreen").
        modal: Whether this is a modal screen.
        with_header_footer: Include Header and Footer widgets.

    Returns:
        Python code for the screen.
    """
    class_name = _to_class_name(name)
    base_class = "ModalScreen" if modal else "Screen"

    widgets = ["Static"]
    if with_header_footer and not modal:
        widgets.extend(["Header", "Footer"])

    compose_content = []
    if with_header_footer and not modal:
        compose_content.append("        yield Header()")
    compose_content.append(f'        yield Static("Welcome to {class_name}")')
    if with_header_footer and not modal:
        compose_content.append("        yield Footer()")

    return f'''"""The {class_name} screen."""

from textual.app import ComposeResult
from textual.screen import {base_class}
from textual.widgets import {", ".join(sorted(set(widgets)))}


class {class_name}({base_class}):
    """{class_name} screen."""

    CSS = """
    {class_name} {{
        align: center middle;
    }}
    """

    BINDINGS = [
        ("escape", "dismiss", "Close"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the screen content."""
{chr(10).join(compose_content)}
'''


def generate_app(
    name: str,
    with_screens: bool = False,
    with_sidebar: bool = False,
) -> str:
    """Generate a complete Textual application.

    Args:
        name: Name for the application (e.g., "MyApp").
        with_screens: Include example screen navigation.
        with_sidebar: Include a sidebar layout.

    Returns:
        Python code for the complete application.
    """
    class_name = _to_class_name(name)

    widgets = ["Footer", "Header", "Static"]
    containers = ["Container"]

    if with_sidebar:
        containers.append("Horizontal")

    css = """
    CSS = \"\"\"
    Screen {
"""
    if with_sidebar:
        css += "        layout: horizontal;\n"
    css += "    }\n"

    if with_sidebar:
        css += """
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
    css += '    """'

    compose_body = "        yield Header()\n"
    if with_sidebar:
        compose_body += """        yield Horizontal(
            Static("Sidebar", id="sidebar"),
            Container(
                Static("Main Content"),
                id="main",
            ),
        )
"""
    else:
        compose_body += '        yield Container(Static("Main Content"))\n'
    compose_body += "        yield Footer()"

    return f'''"""{class_name} - A Textual Application."""

from textual.app import App, ComposeResult
from textual.containers import {", ".join(sorted(set(containers)))}
from textual.widgets import {", ".join(sorted(set(widgets)))}


class {class_name}(App):
    """{class_name} application."""
{css}

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle Dark Mode"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
{compose_body}

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "textual-light" if self.theme == "textual-dark" else "textual-dark"
        )


def main() -> None:
    """Run the application."""
    app = {class_name}()
    app.run()


if __name__ == "__main__":
    main()
'''


def register_generate_tools(mcp: FastMCP) -> None:
    """Register code generation tools."""
    mcp.tool()(list_widgets)
    mcp.tool()(list_containers)
    mcp.tool()(generate_widget)
    mcp.tool()(generate_screen)
    mcp.tool()(generate_app)
