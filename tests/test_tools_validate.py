"""Tests for validation tools."""

from tui_builder.tools.validate import (
    ValidationResult,
    check_accessibility,
    lint_widget,
    validate_css,
)


class TestValidateCss:
    """Tests for validate_css tool."""

    def test_returns_validation_result(self):
        """validate_css returns a ValidationResult."""
        result = validate_css("Static { color: red; }")
        assert isinstance(result, ValidationResult)

    def test_valid_css_passes(self):
        """Valid CSS passes validation."""
        css = """
        Screen {
            background: $surface;
        }
        """
        result = validate_css(css)
        assert result.valid is True
        assert len(result.errors) == 0

    def test_empty_css_is_valid(self):
        """Empty CSS is valid."""
        result = validate_css("")
        assert result.valid is True

    def test_reports_unclosed_brace(self):
        """Reports unclosed brace error."""
        css = "Screen { background: red;"
        result = validate_css(css)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_reports_unknown_property_as_warning(self):
        """Unknown properties are reported as warnings."""
        css = "Screen { unknown-property: value; }"
        result = validate_css(css)
        # Unknown properties should be warnings, not errors
        assert len(result.warnings) > 0

    def test_valid_textual_properties(self):
        """Recognizes valid Textual CSS properties."""
        css = """
        Widget {
            padding: 1 2;
            margin: 1;
            background: $primary;
            color: auto;
            border: solid green;
            width: 100%;
            height: auto;
        }
        """
        result = validate_css(css)
        assert result.valid is True


class TestLintWidget:
    """Tests for lint_widget tool."""

    def test_returns_validation_result(self):
        """lint_widget returns a ValidationResult."""
        code = """
class MyWidget(Static):
    pass
"""
        result = lint_widget(code)
        assert isinstance(result, ValidationResult)

    def test_valid_widget_passes(self):
        """Valid widget code passes linting."""
        code = '''
from textual.widgets import Static

class MyWidget(Static):
    """A custom widget."""

    def compose(self):
        yield Static("Hello")
'''
        result = lint_widget(code)
        assert result.valid is True

    def test_warns_missing_docstring(self):
        """Warns about missing class docstring."""
        code = """
class MyWidget(Static):
    pass
"""
        result = lint_widget(code)
        assert any("docstring" in w.lower() for w in result.warnings)

    def test_warns_missing_compose(self):
        """Warns if widget doesn't override compose."""
        code = '''
class MyWidget(Static):
    """A widget without compose."""
    pass
'''
        result = lint_widget(code)
        assert any("compose" in w.lower() for w in result.warnings)


class TestCheckAccessibility:
    """Tests for check_accessibility tool."""

    def test_returns_validation_result(self):
        """check_accessibility returns a ValidationResult."""
        code = """
class MyApp(App):
    pass
"""
        result = check_accessibility(code)
        assert isinstance(result, ValidationResult)

    def test_warns_no_bindings(self):
        """Warns if app has no keyboard bindings."""
        code = '''
class MyApp(App):
    """An app without bindings."""
    pass
'''
        result = check_accessibility(code)
        assert any("binding" in w.lower() for w in result.warnings)

    def test_passes_with_bindings(self):
        """Passes when app has keyboard bindings."""
        code = '''
class MyApp(App):
    """An accessible app."""
    BINDINGS = [("q", "quit", "Quit")]
'''
        result = check_accessibility(code)
        assert result.valid is True
        # Should not warn about bindings
        assert not any("binding" in w.lower() for w in result.warnings)
