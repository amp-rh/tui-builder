"""Tests for MCP prompts."""

from tui_builder.prompts.debug import (
    get_debug_layout_prompt,
    get_debug_styling_prompt,
    get_optimize_app_prompt,
)
from tui_builder.prompts.design import (
    get_create_widget_prompt,
    get_design_form_prompt,
    get_design_layout_prompt,
)


class TestDesignLayoutPrompt:
    """Tests for design_layout prompt."""

    def test_returns_dict(self):
        """get_design_layout_prompt returns a dictionary."""
        result = get_design_layout_prompt()
        assert isinstance(result, dict)

    def test_contains_name(self):
        """Prompt has a name."""
        result = get_design_layout_prompt()
        assert "name" in result
        assert len(result["name"]) > 0

    def test_contains_description(self):
        """Prompt has a description."""
        result = get_design_layout_prompt()
        assert "description" in result

    def test_contains_template(self):
        """Prompt has a template or messages."""
        result = get_design_layout_prompt()
        assert "template" in result or "messages" in result


class TestCreateWidgetPrompt:
    """Tests for create_widget prompt."""

    def test_returns_dict(self):
        """get_create_widget_prompt returns a dictionary."""
        result = get_create_widget_prompt()
        assert isinstance(result, dict)

    def test_contains_name(self):
        """Prompt has a name."""
        result = get_create_widget_prompt()
        assert "name" in result

    def test_contains_template(self):
        """Prompt has a template."""
        result = get_create_widget_prompt()
        assert "template" in result or "messages" in result


class TestDesignFormPrompt:
    """Tests for design_form prompt."""

    def test_returns_dict(self):
        """get_design_form_prompt returns a dictionary."""
        result = get_design_form_prompt()
        assert isinstance(result, dict)

    def test_contains_name(self):
        """Prompt has a name."""
        result = get_design_form_prompt()
        assert "name" in result


class TestDebugLayoutPrompt:
    """Tests for debug_layout prompt."""

    def test_returns_dict(self):
        """get_debug_layout_prompt returns a dictionary."""
        result = get_debug_layout_prompt()
        assert isinstance(result, dict)

    def test_contains_name(self):
        """Prompt has a name."""
        result = get_debug_layout_prompt()
        assert "name" in result

    def test_contains_troubleshooting_steps(self):
        """Prompt template includes troubleshooting guidance."""
        result = get_debug_layout_prompt()
        template = result.get("template", "")
        # Should mention common layout issues
        assert "layout" in template.lower() or "css" in template.lower()


class TestDebugStylingPrompt:
    """Tests for debug_styling prompt."""

    def test_returns_dict(self):
        """get_debug_styling_prompt returns a dictionary."""
        result = get_debug_styling_prompt()
        assert isinstance(result, dict)

    def test_contains_name(self):
        """Prompt has a name."""
        result = get_debug_styling_prompt()
        assert "name" in result


class TestOptimizeAppPrompt:
    """Tests for optimize_app prompt."""

    def test_returns_dict(self):
        """get_optimize_app_prompt returns a dictionary."""
        result = get_optimize_app_prompt()
        assert isinstance(result, dict)

    def test_contains_name(self):
        """Prompt has a name."""
        result = get_optimize_app_prompt()
        assert "name" in result

    def test_contains_performance_guidance(self):
        """Prompt includes performance guidance."""
        result = get_optimize_app_prompt()
        template = result.get("template", "")
        assert "performance" in template.lower() or "optimize" in template.lower()
