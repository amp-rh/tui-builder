"""Design workflow prompts."""

from mcp.server.fastmcp import FastMCP

DESIGN_LAYOUT_PROMPT = {
    "name": "design_layout",
    "description": "Guide through designing a TUI layout.",
    "template": """# TUI Layout Design Workflow

Help me design a layout for a Textual TUI application.

## Step 1: Define the Purpose
What is the main purpose of this application?
- Dashboard
- Form/Data Entry
- File Browser
- Chat/Messaging
- Other: {purpose}

## Step 2: Choose a Layout Pattern
Common patterns:
1. **Header/Content/Footer** - Classic app structure
2. **Sidebar + Main** - Navigation sidebar with content area
3. **Card Grid** - Grid of cards/tiles
4. **Tabbed Interface** - Content organized in tabs
5. **Modal Dialogs** - Main content with popup dialogs

Recommended pattern based on purpose: Consider the user's workflow.

## Step 3: Identify Key Widgets
Based on the purpose, suggest widgets:
- Navigation: TabbedContent, Tree, ListView
- Content: DataTable, Markdown, TextArea
- Input: Input, Button, Switch, Select
- Feedback: ProgressBar, LoadingIndicator, Static

## Step 4: Define CSS Structure
Key CSS properties to consider:
- `layout`: vertical, horizontal, or grid
- `dock`: top, bottom, left, right for fixed elements
- `width`/`height`: sizing (percentages, fr units, auto)
- `padding`/`margin`: spacing
- `background`/`border`: visual styling

## Step 5: Generate Skeleton Code
Use the `generate_app` tool with the chosen options.
""",
}

CREATE_WIDGET_PROMPT = {
    "name": "create_widget",
    "description": "Step-by-step custom widget creation.",
    "template": """# Custom Widget Creation Workflow

Help me create a custom Textual widget.

## Step 1: Define Widget Purpose
What should this widget do?
- Display: Show static or dynamic content
- Input: Accept user input
- Container: Group other widgets
- Composite: Combine multiple widgets

Widget name: {widget_name}

## Step 2: Choose Base Class
Select the appropriate base:
- `Static` - For content display
- `Widget` - For custom rendering
- `Container` - For grouping widgets
- `Input` - For text input
- Existing widget to extend (Button, etc.)

## Step 3: Define Properties
What data does the widget need?
- Use reactive properties for dynamic updates
- Consider validation requirements

## Step 4: Handle Events
What events should the widget emit?
- Define custom message classes
- Use `@on()` decorators for handlers

## Step 5: Add Styling
CSS properties for the widget:
- Default styles in CSS class attribute
- Consider theming with CSS variables

## Step 6: Generate Code
Use `generate_widget` tool with:
- name: {widget_name}
- widget_type: chosen base class
- with_css: True
- with_bindings: True (if keyboard interaction needed)
""",
}

DESIGN_FORM_PROMPT = {
    "name": "design_form",
    "description": "Design a form layout with validation.",
    "template": """# Form Design Workflow

Help me design a form for a Textual TUI application.

## Step 1: Identify Form Fields
List the required fields:
- Text inputs (name, email, etc.)
- Selections (dropdowns, radio buttons)
- Toggles (checkboxes, switches)
- Rich text (TextArea)

## Step 2: Define Validation Rules
For each field:
- Required or optional?
- Format validation (email, phone, etc.)
- Length constraints
- Custom validation logic

## Step 3: Layout Organization
Organize fields logically:
- Group related fields together
- Use labels consistently
- Consider tab order for keyboard navigation

## Step 4: Error Handling
Display validation errors:
- Inline error messages near fields
- Summary at top/bottom
- Visual indicators (border color, icons)

## Step 5: Form Submission
Handle form submission:
- Submit button placement
- Loading state during submission
- Success/error feedback

## CSS for Forms
```css
Label {
    margin-top: 1;
}
Input {
    margin-bottom: 1;
}
.error {
    color: $error;
}
Button {
    margin-top: 2;
}
```
""",
}


def get_design_layout_prompt() -> dict:
    """Get the design layout prompt.

    Returns:
        Prompt dictionary with name, description, and template.
    """
    return DESIGN_LAYOUT_PROMPT.copy()


def get_create_widget_prompt() -> dict:
    """Get the create widget prompt.

    Returns:
        Prompt dictionary with name, description, and template.
    """
    return CREATE_WIDGET_PROMPT.copy()


def get_design_form_prompt() -> dict:
    """Get the design form prompt.

    Returns:
        Prompt dictionary with name, description, and template.
    """
    return DESIGN_FORM_PROMPT.copy()


def register_design_prompts(mcp: FastMCP) -> None:
    """Register design workflow prompts."""

    @mcp.prompt()
    def design_layout() -> str:
        """Guide through designing a TUI layout."""
        return DESIGN_LAYOUT_PROMPT["template"]

    @mcp.prompt()
    def create_widget() -> str:
        """Step-by-step custom widget creation."""
        return CREATE_WIDGET_PROMPT["template"]

    @mcp.prompt()
    def design_form() -> str:
        """Design a form layout with validation."""
        return DESIGN_FORM_PROMPT["template"]
