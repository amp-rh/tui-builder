"""TUI Builder main application."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, Header, Static


class WelcomeScreen(Static):
    """Welcome screen widget."""

    def compose(self) -> ComposeResult:
        yield Static(
            "[bold cyan]TUI Builder[/]\n\n"
            "Build text user interfaces with ease.\n\n"
            "Press [bold]q[/] to quit.",
            id="welcome-text",
        )


class TUIBuilderApp(App):
    """The main TUI Builder application."""

    CSS = """
    Screen {
        align: center middle;
    }

    #welcome-text {
        text-align: center;
        padding: 2 4;
        border: solid $primary;
        background: $surface;
    }

    #button-container {
        margin-top: 2;
        align: center middle;
        width: auto;
    }

    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            WelcomeScreen(),
            Horizontal(
                Button("New Project", id="new", variant="primary"),
                Button("Open Project", id="open"),
                Button("Settings", id="settings"),
                id="button-container",
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        if button_id == "new":
            self.notify("Creating new project...")
        elif button_id == "open":
            self.notify("Opening project...")
        elif button_id == "settings":
            self.notify("Opening settings...")


def main() -> None:
    """Run the TUI Builder application."""
    app = TUIBuilderApp()
    app.run()


if __name__ == "__main__":
    main()

