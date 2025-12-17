"""Validation tools for TUI applications."""

import re
from dataclasses import dataclass, field

from mcp.server.fastmcp import FastMCP

# Valid Textual CSS properties
TEXTUAL_CSS_PROPERTIES = {
    "align",
    "align-horizontal",
    "align-vertical",
    "background",
    "border",
    "border-bottom",
    "border-left",
    "border-right",
    "border-top",
    "border-subtitle-align",
    "border-subtitle-background",
    "border-subtitle-color",
    "border-subtitle-style",
    "border-title-align",
    "border-title-background",
    "border-title-color",
    "border-title-style",
    "box-sizing",
    "color",
    "column-span",
    "constrain",
    "content-align",
    "content-align-horizontal",
    "content-align-vertical",
    "display",
    "dock",
    "grid-columns",
    "grid-gutter",
    "grid-rows",
    "grid-size",
    "height",
    "hatch",
    "keyline",
    "layer",
    "layers",
    "layout",
    "link-background",
    "link-background-hover",
    "link-color",
    "link-color-hover",
    "link-style",
    "link-style-hover",
    "margin",
    "margin-bottom",
    "margin-left",
    "margin-right",
    "margin-top",
    "max-height",
    "max-width",
    "min-height",
    "min-width",
    "offset",
    "offset-x",
    "offset-y",
    "opacity",
    "outline",
    "outline-bottom",
    "outline-left",
    "outline-right",
    "outline-top",
    "overflow",
    "overflow-x",
    "overflow-y",
    "padding",
    "padding-bottom",
    "padding-left",
    "padding-right",
    "padding-top",
    "row-span",
    "scrollbar-background",
    "scrollbar-background-active",
    "scrollbar-background-hover",
    "scrollbar-color",
    "scrollbar-color-active",
    "scrollbar-color-hover",
    "scrollbar-corner-color",
    "scrollbar-gutter",
    "scrollbar-size",
    "scrollbar-size-horizontal",
    "scrollbar-size-vertical",
    "text-align",
    "text-opacity",
    "text-style",
    "tint",
    "visibility",
    "width",
}


@dataclass
class ValidationResult:
    """Result of a validation check."""

    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def validate_css(css: str) -> ValidationResult:
    """Validate Textual CSS syntax.

    Args:
        css: The CSS string to validate.

    Returns:
        ValidationResult with any errors or warnings.
    """
    result = ValidationResult()

    if not css.strip():
        return result

    # Check for balanced braces
    open_braces = css.count("{")
    close_braces = css.count("}")
    if open_braces != close_braces:
        result.valid = False
        result.errors.append(
            f"Unbalanced braces: {open_braces} opening, {close_braces} closing"
        )
        return result

    # Extract property names and check them
    property_pattern = re.compile(r"([a-zA-Z-]+)\s*:")
    for match in property_pattern.finditer(css):
        prop_name = match.group(1).lower()
        if prop_name not in TEXTUAL_CSS_PROPERTIES:
            result.warnings.append(f"Unknown CSS property: {prop_name}")

    return result


def lint_widget(code: str) -> ValidationResult:
    """Lint widget code for best practices.

    Args:
        code: Python code containing a widget class.

    Returns:
        ValidationResult with any errors or warnings.
    """
    result = ValidationResult()

    # Check for class definition
    class_pattern = re.compile(r"class\s+(\w+)\s*\([^)]*\)\s*:")
    class_match = class_pattern.search(code)

    if not class_match:
        result.valid = False
        result.errors.append("No class definition found")
        return result

    class_name = class_match.group(1)

    # Check for docstring after class definition
    docstring_pattern = re.compile(
        r"class\s+" + class_name + r"\s*\([^)]*\)\s*:\s*\n\s*\"\"\"", re.MULTILINE
    )
    if not docstring_pattern.search(code):
        result.warnings.append(f"Class '{class_name}' is missing a docstring")

    # Check for compose method
    compose_pattern = re.compile(r"def\s+compose\s*\(")
    if not compose_pattern.search(code):
        result.warnings.append(f"Widget '{class_name}' doesn't define a compose method")

    return result


def check_accessibility(code: str) -> ValidationResult:
    """Check code for accessibility best practices.

    Args:
        code: Python code to check for accessibility.

    Returns:
        ValidationResult with any errors or warnings.
    """
    result = ValidationResult()

    # Check for BINDINGS
    bindings_pattern = re.compile(r"BINDINGS\s*=\s*\[")
    if not bindings_pattern.search(code):
        result.warnings.append(
            "No keyboard bindings defined. Consider adding BINDINGS for accessibility."
        )

    return result


def register_validate_tools(mcp: FastMCP) -> None:
    """Register validation tools."""
    mcp.tool()(validate_css)
    mcp.tool()(lint_widget)
    mcp.tool()(check_accessibility)
