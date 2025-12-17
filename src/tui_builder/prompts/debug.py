"""Debug workflow prompts."""

from mcp.server.fastmcp import FastMCP

DEBUG_LAYOUT_PROMPT = {
    "name": "debug_layout",
    "description": "Troubleshoot layout issues in TUI apps.",
    "template": """# Debug Layout Issues

Help me troubleshoot layout problems in my Textual TUI application.

## Common Layout Issues

### 1. Widget Not Visible
Check:
- Is `display: none` set?
- Is `visibility: hidden` set?
- Is the widget's height/width 0?
- Is it outside the parent's bounds?

### 2. Unexpected Sizing
Check:
- Are width/height explicitly set?
- Is the parent container sized correctly?
- Are you using `fr` units or percentages?
- Check `box-sizing` property

### 3. Wrong Positioning
Check:
- Is `dock` set on the wrong widgets?
- Check `layout` property (vertical, horizontal, grid)
- Check `align` properties
- Is overflow hidden cutting off content?

### 4. Overlapping Widgets
Check:
- Are you using `layers`?
- Check `dock` properties
- Are absolute positions being used?

## CSS Debugging Steps

1. Add visible borders to all elements:
```css
* {
    border: solid red;
}
```

2. Check inheritance - styles cascade from parent

3. Use Textual's devtools:
```bash
textual run --dev your_app.py
```

4. Press F12 to open the Textual console

## Common Fixes

- Use `Container` to group widgets
- Set explicit sizes with `width: 100%`
- Use `Vertical`/`Horizontal` for linear layouts
- Use `Grid` with `grid-size` for complex layouts
""",
}

DEBUG_STYLING_PROMPT = {
    "name": "debug_styling",
    "description": "Fix CSS/styling problems in TUI apps.",
    "template": """# Debug Styling Issues

Help me fix styling problems in my Textual TUI application.

## Common Styling Issues

### 1. Colors Not Applying
Check:
- Is the selector correct?
- Is there a more specific selector overriding?
- Are you using valid color values or CSS variables?
- Check for typos in property names

### 2. Borders Not Showing
Check:
- Border syntax: `border: <style> <color>`
- Valid styles: solid, double, dashed, heavy, wide, tall
- Individual sides: border-top, border-bottom, etc.

### 3. Text Styling Issues
Check:
- `color` for text color
- `text-style` for bold, italic, etc.
- `text-align` for alignment

### 4. Spacing Problems
Check:
- `padding` for internal spacing
- `margin` for external spacing
- Values: single number or "top right bottom left"

## CSS Variables (Theme Colors)
Use these for consistent theming:
- `$primary` - Primary accent color
- `$secondary` - Secondary color
- `$surface` - Background for elevated surfaces
- `$background` - Main background
- `$text` - Primary text color
- `$error`, `$warning`, `$success` - Status colors

## Debugging CSS

1. Check selector specificity:
   - Type selectors: `Button`
   - Class selectors: `.my-class`
   - ID selectors: `#my-id`
   - Pseudo-classes: `:hover`, `:focus`

2. Use Textual console (F12) to inspect styles

3. Validate CSS with the `validate_css` tool
""",
}

OPTIMIZE_APP_PROMPT = {
    "name": "optimize_app",
    "description": "Optimize TUI app performance.",
    "template": """# Optimize TUI App Performance

Help me improve the performance of my Textual TUI application.

## Performance Checklist

### 1. Reduce Redraws
- Use `batch_update()` for multiple changes
- Set `auto_refresh=False` on Static widgets when not needed
- Use `refresh(layout=False)` when layout doesn't change

### 2. Optimize compose()
- Don't do heavy computation in compose()
- Use lazy loading for large data sets
- Consider using `yield from` for widget lists

### 3. Efficient Data Loading
- Load data asynchronously with `asyncio`
- Show loading indicators during async operations
- Paginate large data sets in DataTable

### 4. CSS Performance
- Avoid overly complex selectors
- Use ID selectors for single elements
- Minimize use of universal selector `*`

### 5. Widget Optimization
- Reuse widgets instead of creating new ones
- Use `query_one()` instead of `query()` when expecting single result
- Cache query results if used multiple times

## Profiling Tools

1. Use Python's cProfile:
```bash
python -m cProfile -o output.prof your_app.py
```

2. Use Textual's devtools:
```bash
textual run --dev your_app.py
```

3. Monitor with `textual console`

## Common Performance Issues

- Updating widgets in a loop without batching
- Loading entire datasets into memory
- Complex CSS selectors with many descendants
- Not using async for I/O operations
- Creating many temporary widgets

## Quick Wins
1. Add `ALLOW_SELECT = True` only where needed
2. Use `Static` for display-only content
3. Limit DataTable rows with virtual scrolling
4. Use CSS `display: none` instead of removing widgets
""",
}


def get_debug_layout_prompt() -> dict:
    """Get the debug layout prompt.

    Returns:
        Prompt dictionary with name, description, and template.
    """
    return DEBUG_LAYOUT_PROMPT.copy()


def get_debug_styling_prompt() -> dict:
    """Get the debug styling prompt.

    Returns:
        Prompt dictionary with name, description, and template.
    """
    return DEBUG_STYLING_PROMPT.copy()


def get_optimize_app_prompt() -> dict:
    """Get the optimize app prompt.

    Returns:
        Prompt dictionary with name, description, and template.
    """
    return OPTIMIZE_APP_PROMPT.copy()


def register_debug_prompts(mcp: FastMCP) -> None:
    """Register debug workflow prompts."""

    @mcp.prompt()
    def debug_layout() -> str:
        """Troubleshoot layout issues in TUI apps."""
        return DEBUG_LAYOUT_PROMPT["template"]

    @mcp.prompt()
    def debug_styling() -> str:
        """Fix CSS/styling problems in TUI apps."""
        return DEBUG_STYLING_PROMPT["template"]

    @mcp.prompt()
    def optimize_app() -> str:
        """Optimize TUI app performance."""
        return OPTIMIZE_APP_PROMPT["template"]
