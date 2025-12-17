"""Testing tools for TUI applications."""

import difflib
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import FastMCP


@dataclass
class SnapshotResult:
    """Result of a snapshot operation."""

    success: bool = True
    output: str = ""
    error: str | None = None


@dataclass
class CompareResult:
    """Result of comparing two snapshots."""

    match: bool = True
    diff: str | None = None


def _extract_app_class_name(code: str) -> str | None:
    """Extract the App class name from code."""
    pattern = re.compile(r"class\s+(\w+)\s*\(\s*App\s*\)")
    match = pattern.search(code)
    return match.group(1) if match else None


async def _run_app_async(code: str, actions: list[tuple[str, ...]] | None = None):
    """Run an app asynchronously with Pilot."""
    # Write code to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_path = Path(f.name)

    try:
        # Import the app module
        import importlib.util

        spec = importlib.util.spec_from_file_location("temp_app", temp_path)
        if spec is None or spec.loader is None:
            return SnapshotResult(success=False, error="Failed to load module")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find the App class
        app_class_name = _extract_app_class_name(code)
        if not app_class_name:
            return SnapshotResult(success=False, error="No App class found")

        app_class = getattr(module, app_class_name, None)
        if app_class is None:
            return SnapshotResult(
                success=False, error=f"Class {app_class_name} not found"
            )

        # Run the app with Pilot
        app = app_class()
        output = ""

        async with app.run_test(size=(80, 24)) as pilot:
            # Execute any actions
            if actions:
                for action in actions:
                    action_type = action[0]
                    if action_type == "press":
                        await pilot.press(*action[1:])
                    elif action_type == "click":
                        selector = action[1]
                        try:
                            widget = app.query_one(selector)
                            await pilot.click(widget)
                        except Exception as e:
                            return SnapshotResult(
                                success=False, error=f"Click failed: {e}"
                            )

            # Capture the output using console export
            from io import StringIO

            from rich.console import Console

            console = Console(file=StringIO(), force_terminal=True, width=80)
            # Get screen content by rendering widgets
            screen_content = []
            for widget in app.screen.walk_children():
                if hasattr(widget, "renderable"):
                    screen_content.append(str(widget.renderable))
                elif hasattr(widget, "render"):
                    try:
                        rendered = widget.render()
                        if rendered:
                            console.print(rendered)
                    except Exception:
                        pass

            # Build output from widget content
            output_parts = []
            for widget in app.screen.query("*"):
                # Get text content from widgets
                if hasattr(widget, "renderable"):
                    output_parts.append(str(widget.renderable))

            output = "\n".join(output_parts) if output_parts else "App rendered"

        return SnapshotResult(success=True, output=output)

    except Exception as e:
        return SnapshotResult(success=False, error=str(e))
    finally:
        temp_path.unlink(missing_ok=True)


def _run_sync(coro):
    """Run an async coroutine synchronously."""
    import asyncio

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None:
        # Already in async context, create a new task
        import threading

        result = None
        exception = None

        def run_in_thread():
            nonlocal result, exception
            try:
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    result = new_loop.run_until_complete(coro)
                finally:
                    new_loop.close()
            except Exception as e:
                exception = e

        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()

        if exception:
            raise exception
        return result
    else:
        return asyncio.run(coro)


def run_app_pilot(code: str) -> SnapshotResult:
    """Run an app with Textual Pilot for testing.

    Args:
        code: Python code containing a Textual App class.

    Returns:
        SnapshotResult with the rendered output or error.
    """
    try:
        # Check for syntax errors first
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        return SnapshotResult(success=False, error=f"Syntax error: {e}")

    try:
        return _run_sync(_run_app_async(code))
    except Exception as e:
        return SnapshotResult(success=False, error=str(e))


def take_snapshot(code: str) -> SnapshotResult:
    """Capture app output as a text snapshot.

    Args:
        code: Python code containing a Textual App class.

    Returns:
        SnapshotResult with the captured snapshot.
    """
    return run_app_pilot(code)


def simulate_keys(code: str, keys: list[str]) -> SnapshotResult:
    """Simulate keyboard input in a Textual app.

    Args:
        code: Python code containing a Textual App class.
        keys: List of key names to press (e.g., ["tab", "enter", "q"]).

    Returns:
        SnapshotResult after key simulation.
    """
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        return SnapshotResult(success=False, error=f"Syntax error: {e}")

    actions = [("press", key) for key in keys]

    try:
        return _run_sync(_run_app_async(code, actions))
    except Exception as e:
        return SnapshotResult(success=False, error=str(e))


def simulate_click(code: str, selector: str) -> SnapshotResult:
    """Simulate a mouse click on a widget.

    Args:
        code: Python code containing a Textual App class.
        selector: CSS selector for the widget to click.

    Returns:
        SnapshotResult after click simulation.
    """
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        return SnapshotResult(success=False, error=f"Syntax error: {e}")

    actions = [("click", selector)]

    try:
        return _run_sync(_run_app_async(code, actions))
    except Exception as e:
        return SnapshotResult(success=False, error=str(e))


def generate_test_cases(code: str) -> str:
    """Generate pytest test cases for a Textual app.

    Args:
        code: Python code containing a Textual App class.

    Returns:
        Python code containing pytest test cases.
    """
    app_class_name = _extract_app_class_name(code)
    if not app_class_name:
        app_class_name = "App"

    return f'''"""Tests for {app_class_name}."""

import pytest
from textual.testing import PilotTest


class Test{app_class_name}:
    """Tests for {app_class_name}."""

    @pytest.fixture
    def app(self):
        """Create app instance for testing."""
        # TODO: Import your app here
        # from your_module import {app_class_name}
        # return {app_class_name}()
        raise NotImplementedError("Import your app class")

    @pytest.mark.asyncio
    async def test_app_starts(self, app):
        """Test that the app starts without errors."""
        async with app.run_test() as pilot:
            # App should start successfully
            assert app.is_running

    @pytest.mark.asyncio
    async def test_app_quits(self, app):
        """Test that the app can quit."""
        async with app.run_test() as pilot:
            await pilot.press("q")

    @pytest.mark.asyncio
    async def test_initial_state(self, app):
        """Test the app's initial state."""
        async with app.run_test() as pilot:
            # TODO: Add assertions about initial state
            pass

    @pytest.mark.asyncio
    async def test_keyboard_navigation(self, app):
        """Test keyboard navigation works."""
        async with app.run_test() as pilot:
            await pilot.press("tab")
            # TODO: Assert focus moved correctly
            pass
'''


def compare_snapshots(snapshot1: str, snapshot2: str) -> CompareResult:
    """Compare two snapshots for differences.

    Args:
        snapshot1: First snapshot text.
        snapshot2: Second snapshot text.

    Returns:
        CompareResult indicating if they match and any diff.
    """
    if snapshot1 == snapshot2:
        return CompareResult(match=True, diff=None)

    # Generate unified diff
    diff_lines = list(
        difflib.unified_diff(
            snapshot1.splitlines(keepends=True),
            snapshot2.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        )
    )

    return CompareResult(match=False, diff="".join(diff_lines))


def register_testing_tools(mcp: FastMCP) -> None:
    """Register testing tools."""
    mcp.tool()(run_app_pilot)
    mcp.tool()(take_snapshot)
    mcp.tool()(simulate_keys)
    mcp.tool()(simulate_click)
    mcp.tool()(generate_test_cases)
    mcp.tool()(compare_snapshots)
