"""Tests for MCP resources."""

from tui_builder.resources.components import (
    get_container_docs,
    get_widget_docs,
)
from tui_builder.resources.css import (
    get_css_properties,
    get_css_selectors,
    get_css_variables,
)
from tui_builder.resources.patterns import (
    get_layout_patterns,
)


class TestWidgetDocs:
    """Tests for widget documentation resources."""

    def test_returns_dict(self):
        """get_widget_docs returns a dictionary."""
        result = get_widget_docs("Button")
        assert isinstance(result, dict)

    def test_contains_description(self):
        """Widget docs contain a description."""
        result = get_widget_docs("Button")
        assert "description" in result
        assert len(result["description"]) > 0

    def test_contains_example(self):
        """Widget docs contain usage example."""
        result = get_widget_docs("Button")
        assert "example" in result

    def test_unknown_widget_returns_none(self):
        """Unknown widget returns None."""
        result = get_widget_docs("UnknownWidget123")
        assert result is None


class TestContainerDocs:
    """Tests for container documentation resources."""

    def test_returns_dict(self):
        """get_container_docs returns a dictionary."""
        result = get_container_docs("Horizontal")
        assert isinstance(result, dict)

    def test_contains_description(self):
        """Container docs contain a description."""
        result = get_container_docs("Container")
        assert "description" in result

    def test_unknown_container_returns_none(self):
        """Unknown container returns None."""
        result = get_container_docs("UnknownContainer123")
        assert result is None


class TestCssProperties:
    """Tests for CSS properties resource."""

    def test_returns_dict(self):
        """get_css_properties returns a dictionary."""
        result = get_css_properties()
        assert isinstance(result, dict)

    def test_contains_common_properties(self):
        """Result contains common CSS properties."""
        result = get_css_properties()
        assert "background" in result
        assert "padding" in result
        assert "margin" in result
        assert "width" in result

    def test_properties_have_descriptions(self):
        """Each property has a description."""
        result = get_css_properties()
        for name, info in result.items():
            assert "description" in info, f"{name} missing description"


class TestCssSelectors:
    """Tests for CSS selectors resource."""

    def test_returns_dict(self):
        """get_css_selectors returns a dictionary."""
        result = get_css_selectors()
        assert isinstance(result, dict)

    def test_contains_selector_types(self):
        """Result contains common selector types."""
        result = get_css_selectors()
        # Should have info about type selectors, ID selectors, class selectors
        assert len(result) > 0


class TestCssVariables:
    """Tests for CSS variables resource."""

    def test_returns_dict(self):
        """get_css_variables returns a dictionary."""
        result = get_css_variables()
        assert isinstance(result, dict)

    def test_contains_theme_variables(self):
        """Result contains theme variables."""
        result = get_css_variables()
        assert "$primary" in result or "primary" in str(result).lower()
        assert "$surface" in result or "surface" in str(result).lower()


class TestLayoutPatterns:
    """Tests for layout patterns resource."""

    def test_returns_list(self):
        """get_layout_patterns returns a list."""
        result = get_layout_patterns()
        assert isinstance(result, list)

    def test_patterns_have_names(self):
        """Each pattern has a name."""
        result = get_layout_patterns()
        for pattern in result:
            assert "name" in pattern

    def test_patterns_have_code(self):
        """Each pattern has example code."""
        result = get_layout_patterns()
        for pattern in result:
            assert "code" in pattern or "example" in pattern
