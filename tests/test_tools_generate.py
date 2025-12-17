"""Tests for generation tools."""

from tui_builder.tools.generate import (
    generate_app,
    generate_screen,
    generate_widget,
    list_containers,
    list_widgets,
)


class TestListWidgets:
    """Tests for list_widgets tool."""

    def test_returns_dict(self):
        """list_widgets returns a dictionary."""
        result = list_widgets()
        assert isinstance(result, dict)

    def test_contains_common_widgets(self):
        """list_widgets includes common Textual widgets."""
        result = list_widgets()
        assert "Button" in result
        assert "Input" in result
        assert "Static" in result
        assert "DataTable" in result

    def test_widgets_have_descriptions(self):
        """Each widget has a non-empty description."""
        result = list_widgets()
        for name, description in result.items():
            assert isinstance(description, str)
            assert len(description) > 0, f"{name} has empty description"


class TestListContainers:
    """Tests for list_containers tool."""

    def test_returns_dict(self):
        """list_containers returns a dictionary."""
        result = list_containers()
        assert isinstance(result, dict)

    def test_contains_common_containers(self):
        """list_containers includes common Textual containers."""
        result = list_containers()
        assert "Container" in result
        assert "Horizontal" in result
        assert "Vertical" in result

    def test_containers_have_descriptions(self):
        """Each container has a non-empty description."""
        result = list_containers()
        for name, description in result.items():
            assert isinstance(description, str)
            assert len(description) > 0, f"{name} has empty description"


class TestGenerateWidget:
    """Tests for generate_widget tool."""

    def test_returns_string(self):
        """generate_widget returns a string."""
        result = generate_widget(name="MyWidget")
        assert isinstance(result, str)

    def test_contains_class_definition(self):
        """Generated code contains class definition."""
        result = generate_widget(name="StatusBar")
        assert "class StatusBar" in result

    def test_class_name_capitalized(self):
        """Class name is properly capitalized."""
        result = generate_widget(name="status_bar")
        assert "class StatusBar" in result

    def test_extends_specified_widget(self):
        """Widget extends the specified base widget."""
        result = generate_widget(name="MyButton", widget_type="Button")
        assert "class MyButton(Button)" in result

    def test_includes_css_by_default(self):
        """CSS is included by default."""
        result = generate_widget(name="MyWidget")
        assert "CSS = " in result

    def test_css_can_be_disabled(self):
        """CSS can be disabled."""
        result = generate_widget(name="MyWidget", with_css=False)
        assert "CSS = " not in result

    def test_bindings_optional(self):
        """Bindings can be included optionally."""
        without = generate_widget(name="MyWidget", with_bindings=False)
        with_bindings = generate_widget(name="MyWidget", with_bindings=True)
        assert "BINDINGS" not in without
        assert "BINDINGS" in with_bindings

    def test_includes_imports(self):
        """Generated code includes necessary imports."""
        result = generate_widget(name="MyWidget", widget_type="Static")
        assert "from textual" in result
        assert "Static" in result


class TestGenerateScreen:
    """Tests for generate_screen tool."""

    def test_returns_string(self):
        """generate_screen returns a string."""
        result = generate_screen(name="MainScreen")
        assert isinstance(result, str)

    def test_contains_class_definition(self):
        """Generated code contains class definition."""
        result = generate_screen(name="SettingsScreen")
        assert "class SettingsScreen" in result

    def test_regular_screen_extends_screen(self):
        """Regular screen extends Screen."""
        result = generate_screen(name="MainScreen", modal=False)
        assert "class MainScreen(Screen)" in result

    def test_modal_screen_extends_modal_screen(self):
        """Modal screen extends ModalScreen."""
        result = generate_screen(name="ConfirmDialog", modal=True)
        assert "class ConfirmDialog(ModalScreen)" in result

    def test_includes_header_footer_by_default(self):
        """Header and Footer are included by default for non-modal screens."""
        result = generate_screen(name="MainScreen", modal=False)
        assert "Header" in result
        assert "Footer" in result

    def test_modal_no_header_footer(self):
        """Modal screens don't include Header/Footer by default."""
        result = generate_screen(name="Dialog", modal=True)
        # Modal screens typically don't have header/footer in compose
        assert "yield Header()" not in result

    def test_includes_escape_binding(self):
        """Screens include escape binding to dismiss."""
        result = generate_screen(name="MainScreen")
        assert "escape" in result.lower()


class TestGenerateApp:
    """Tests for generate_app tool."""

    def test_returns_string(self):
        """generate_app returns a string."""
        result = generate_app(name="MyApp")
        assert isinstance(result, str)

    def test_contains_app_class(self):
        """Generated code contains App class."""
        result = generate_app(name="TodoApp")
        assert "class TodoApp(App)" in result

    def test_includes_main_function(self):
        """Generated code includes main function."""
        result = generate_app(name="MyApp")
        assert "def main()" in result
        assert 'if __name__ == "__main__"' in result

    def test_includes_quit_binding(self):
        """App includes quit binding."""
        result = generate_app(name="MyApp")
        assert '"q"' in result or "'q'" in result
        assert "quit" in result.lower()

    def test_includes_header_and_footer(self):
        """App includes Header and Footer."""
        result = generate_app(name="MyApp")
        assert "Header" in result
        assert "Footer" in result

    def test_sidebar_option(self):
        """Sidebar layout can be optionally included."""
        without = generate_app(name="MyApp", with_sidebar=False)
        with_sidebar = generate_app(name="MyApp", with_sidebar=True)
        assert "sidebar" not in without.lower()
        assert "sidebar" in with_sidebar.lower()

    def test_includes_css(self):
        """Generated app includes CSS."""
        result = generate_app(name="MyApp")
        assert "CSS = " in result
