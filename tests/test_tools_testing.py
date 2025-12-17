"""Tests for testing tools."""

from tui_builder.tools.testing import (
    SnapshotResult,
    compare_snapshots,
    generate_test_cases,
    run_app_pilot,
    simulate_click,
    simulate_keys,
    take_snapshot,
)

# Sample app code for testing
SIMPLE_APP_CODE = '''
from textual.app import App, ComposeResult
from textual.widgets import Static, Button

class TestApp(App):
    """A simple test app."""

    def compose(self) -> ComposeResult:
        yield Static("Hello World", id="greeting")
        yield Button("Click Me", id="btn")
'''


class TestRunAppPilot:
    """Tests for run_app_pilot tool."""

    def test_returns_snapshot_result(self):
        """run_app_pilot returns a SnapshotResult."""
        result = run_app_pilot(SIMPLE_APP_CODE)
        assert isinstance(result, SnapshotResult)

    def test_captures_output(self):
        """run_app_pilot captures app output."""
        result = run_app_pilot(SIMPLE_APP_CODE)
        assert result.output is not None
        assert len(result.output) > 0

    def test_output_not_empty(self):
        """Output is not empty when app runs successfully."""
        result = run_app_pilot(SIMPLE_APP_CODE)
        assert result.success is True
        assert len(result.output) > 0

    def test_reports_success(self):
        """Successful run reports success."""
        result = run_app_pilot(SIMPLE_APP_CODE)
        assert result.success is True

    def test_invalid_code_reports_failure(self):
        """Invalid code reports failure."""
        result = run_app_pilot("invalid python code {{{")
        assert result.success is False
        assert result.error is not None


class TestTakeSnapshot:
    """Tests for take_snapshot tool."""

    def test_returns_snapshot_result(self):
        """take_snapshot returns a SnapshotResult."""
        result = take_snapshot(SIMPLE_APP_CODE)
        assert isinstance(result, SnapshotResult)

    def test_captures_snapshot(self):
        """take_snapshot captures rendered output."""
        result = take_snapshot(SIMPLE_APP_CODE)
        assert result.success is True
        assert len(result.output) > 0


class TestSimulateKeys:
    """Tests for simulate_keys tool."""

    def test_returns_snapshot_result(self):
        """simulate_keys returns a SnapshotResult."""
        result = simulate_keys(SIMPLE_APP_CODE, keys=["q"])
        assert isinstance(result, SnapshotResult)

    def test_accepts_key_sequence(self):
        """simulate_keys accepts a sequence of keys."""
        result = simulate_keys(SIMPLE_APP_CODE, keys=["tab", "enter"])
        assert result.success is True


class TestSimulateClick:
    """Tests for simulate_click tool."""

    def test_returns_snapshot_result(self):
        """simulate_click returns a SnapshotResult."""
        result = simulate_click(SIMPLE_APP_CODE, selector="#btn")
        assert isinstance(result, SnapshotResult)

    def test_clicks_by_selector(self):
        """simulate_click can target widgets by selector."""
        result = simulate_click(SIMPLE_APP_CODE, selector="#btn")
        assert result.success is True


class TestGenerateTestCases:
    """Tests for generate_test_cases tool."""

    def test_returns_string(self):
        """generate_test_cases returns test code as string."""
        result = generate_test_cases(SIMPLE_APP_CODE)
        assert isinstance(result, str)

    def test_includes_imports(self):
        """Generated tests include pytest imports."""
        result = generate_test_cases(SIMPLE_APP_CODE)
        assert "import pytest" in result or "from pytest" in result

    def test_includes_test_class(self):
        """Generated tests include a test class."""
        result = generate_test_cases(SIMPLE_APP_CODE)
        assert "class Test" in result or "def test_" in result

    def test_includes_app_test(self):
        """Generated tests include basic app test."""
        result = generate_test_cases(SIMPLE_APP_CODE)
        assert "async" in result  # Textual tests are async


class TestCompareSnapshots:
    """Tests for compare_snapshots tool."""

    def test_identical_snapshots_match(self):
        """Identical snapshots compare as equal."""
        snapshot = "Hello World"
        result = compare_snapshots(snapshot, snapshot)
        assert result.match is True

    def test_different_snapshots_dont_match(self):
        """Different snapshots compare as not equal."""
        result = compare_snapshots("Hello", "World")
        assert result.match is False

    def test_returns_diff(self):
        """compare_snapshots returns a diff for mismatches."""
        result = compare_snapshots("Hello", "World")
        assert result.diff is not None
        assert len(result.diff) > 0
