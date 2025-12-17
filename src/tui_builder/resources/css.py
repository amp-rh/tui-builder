"""CSS reference resources."""

from mcp.server.fastmcp import FastMCP

# CSS Properties reference
CSS_PROPERTIES: dict[str, dict] = {
    "background": {
        "description": "Sets the background color of the widget.",
        "values": ["color", "$variable", "transparent"],
        "example": "background: $surface;",
    },
    "color": {
        "description": "Sets the text color.",
        "values": ["color", "$variable", "auto"],
        "example": "color: $text;",
    },
    "padding": {
        "description": "Sets the padding inside the widget.",
        "values": ["integer", "integer integer", "integer integer integer integer"],
        "example": "padding: 1 2;",
    },
    "margin": {
        "description": "Sets the margin outside the widget.",
        "values": ["integer", "integer integer", "integer integer integer integer"],
        "example": "margin: 1;",
    },
    "width": {
        "description": "Sets the width of the widget.",
        "values": ["integer", "percentage", "auto", "1fr"],
        "example": "width: 100%;",
    },
    "height": {
        "description": "Sets the height of the widget.",
        "values": ["integer", "percentage", "auto", "1fr"],
        "example": "height: auto;",
    },
    "border": {
        "description": "Sets the border around the widget.",
        "values": ["none", "solid", "double", "dashed", "heavy", "wide", "tall"],
        "example": "border: solid $primary;",
    },
    "layout": {
        "description": "Sets the layout mode for arranging children.",
        "values": ["vertical", "horizontal", "grid"],
        "example": "layout: horizontal;",
    },
    "align": {
        "description": "Aligns children within the widget.",
        "values": ["left", "center", "right", "top", "middle", "bottom"],
        "example": "align: center middle;",
    },
    "display": {
        "description": "Controls whether the widget is displayed.",
        "values": ["block", "none"],
        "example": "display: none;",
    },
    "dock": {
        "description": "Docks the widget to an edge.",
        "values": ["top", "bottom", "left", "right"],
        "example": "dock: top;",
    },
    "visibility": {
        "description": "Controls widget visibility.",
        "values": ["visible", "hidden"],
        "example": "visibility: hidden;",
    },
    "overflow": {
        "description": "Controls scrolling behavior.",
        "values": ["auto", "hidden", "scroll"],
        "example": "overflow: auto;",
    },
    "text-align": {
        "description": "Sets text alignment within the widget.",
        "values": ["left", "center", "right", "justify"],
        "example": "text-align: center;",
    },
    "text-style": {
        "description": "Sets text style.",
        "values": ["bold", "italic", "underline", "strike", "reverse"],
        "example": "text-style: bold italic;",
    },
}

# CSS Selectors reference
CSS_SELECTORS: dict[str, dict] = {
    "type": {
        "description": "Selects widgets by their class name.",
        "syntax": "WidgetClassName",
        "example": "Button { background: $primary; }",
    },
    "id": {
        "description": "Selects a widget by its ID.",
        "syntax": "#widget-id",
        "example": "#my-button { border: solid green; }",
    },
    "class": {
        "description": "Selects widgets by CSS class.",
        "syntax": ".class-name",
        "example": ".highlighted { background: yellow; }",
    },
    "pseudo-class": {
        "description": "Selects widgets in a specific state.",
        "syntax": ":state",
        "example": "Button:hover { background: $primary-lighten-1; }",
    },
    "descendant": {
        "description": "Selects widgets nested inside another.",
        "syntax": "Parent Child",
        "example": "Container Button { margin: 1; }",
    },
    "child": {
        "description": "Selects direct children only.",
        "syntax": "Parent > Child",
        "example": "Container > Button { padding: 1; }",
    },
}

# CSS Variables (theme colors)
CSS_VARIABLES: dict[str, dict] = {
    "$primary": {
        "description": "Primary theme color.",
        "usage": "Buttons, accents, important elements.",
    },
    "$secondary": {
        "description": "Secondary theme color.",
        "usage": "Less prominent UI elements.",
    },
    "$surface": {
        "description": "Surface/background color.",
        "usage": "Container backgrounds, cards.",
    },
    "$background": {
        "description": "Main background color.",
        "usage": "App background.",
    },
    "$text": {
        "description": "Primary text color.",
        "usage": "Body text, labels.",
    },
    "$text-muted": {
        "description": "Muted/secondary text color.",
        "usage": "Hints, placeholders, disabled text.",
    },
    "$error": {
        "description": "Error state color.",
        "usage": "Error messages, validation failures.",
    },
    "$warning": {
        "description": "Warning state color.",
        "usage": "Warning messages, caution states.",
    },
    "$success": {
        "description": "Success state color.",
        "usage": "Success messages, confirmations.",
    },
}


def get_css_properties() -> dict[str, dict]:
    """Get all CSS properties with descriptions.

    Returns:
        Dictionary of CSS properties and their documentation.
    """
    return CSS_PROPERTIES.copy()


def get_css_selectors() -> dict[str, dict]:
    """Get CSS selector reference.

    Returns:
        Dictionary of CSS selector types and their documentation.
    """
    return CSS_SELECTORS.copy()


def get_css_variables() -> dict[str, dict]:
    """Get CSS variables (theme colors) reference.

    Returns:
        Dictionary of CSS variables and their documentation.
    """
    return CSS_VARIABLES.copy()


def register_css_resources(mcp: FastMCP) -> None:
    """Register CSS reference resources."""

    @mcp.resource("tui://css/properties")
    def css_properties_resource() -> str:
        """Get CSS properties reference."""
        lines = ["# Textual CSS Properties\n"]
        for name, info in CSS_PROPERTIES.items():
            lines.append(f"## {name}")
            lines.append(f"{info['description']}")
            lines.append(f"Values: {', '.join(info['values'])}")
            lines.append(f"Example: `{info['example']}`\n")
        return "\n".join(lines)

    @mcp.resource("tui://css/selectors")
    def css_selectors_resource() -> str:
        """Get CSS selectors reference."""
        lines = ["# Textual CSS Selectors\n"]
        for name, info in CSS_SELECTORS.items():
            lines.append(f"## {name.title()} Selector")
            lines.append(f"{info['description']}")
            lines.append(f"Syntax: `{info['syntax']}`")
            lines.append(f"Example: `{info['example']}`\n")
        return "\n".join(lines)

    @mcp.resource("tui://css/variables")
    def css_variables_resource() -> str:
        """Get CSS variables reference."""
        lines = ["# Textual CSS Variables (Theme Colors)\n"]
        for name, info in CSS_VARIABLES.items():
            lines.append(f"## {name}")
            lines.append(f"{info['description']}")
            lines.append(f"Usage: {info['usage']}\n")
        return "\n".join(lines)
