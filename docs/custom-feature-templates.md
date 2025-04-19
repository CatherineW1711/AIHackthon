# Defining New Default Feature Templates

This guide explains how to create and add new default feature templates to the DevMind framework, allowing you to extend the system with additional features for any application type.

## Table of Contents
- [Understanding Feature Templates](#understanding-feature-templates)
- [Creating a New Feature Template](#creating-a-new-feature-template)
- [Advanced Template Techniques](#advanced-template-techniques)
- [Integration Points](#integration-points)
- [Testing Templates](#testing-templates)
- [Example: Adding a Dark Mode Feature](#example-adding-a-dark-mode-feature)

## Understanding Feature Templates

Feature templates are code snippets that get inserted into applications when the framework detects that a certain default feature is missing. Each template is associated with:

1. An application type (game, gui_app, cli_tool, web_app)
2. A specific feature (e.g., exit_option, help_command)

Templates should be designed to be as self-contained as possible, with clear instructions on where and how to integrate them into the existing code.

## Creating a New Feature Template

Adding a new feature template involves three steps:

### 1. Define the Feature in DEFAULT_FEATURES

First, add the feature to the appropriate application type in the `DEFAULT_FEATURES` dictionary:

```python
DEFAULT_FEATURES = {
    "gui_app": [
        # Existing features...
        {"name": "dark_mode", "description": "Dark mode toggle", "importance": "medium", 
         "pattern": r"(def\s+(?:toggle_dark_mode|switch_theme)|dark_mode|night_mode|theme_switch)"}
    ]
}
```

The pattern is a regular expression that detects if the feature is already present in the code.

### 2. Create the Template Code

Next, add the template to the `FEATURE_TEMPLATES` dictionary:

```python
FEATURE_TEMPLATES = {
    "gui_app": {
        # Existing templates...
        "dark_mode": """
# Add dark mode functionality
def toggle_dark_mode():
    """Toggle between light and dark theme."""
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled
    
    if dark_mode_enabled:
        # Apply dark theme colors
        root.configure(bg="#333333")
        for widget in all_widgets:
            try:
                widget.configure(bg="#333333", fg="#FFFFFF")
            except:
                pass
    else:
        # Apply light theme colors
        root.configure(bg="#FFFFFF")
        for widget in all_widgets:
            try:
                widget.configure(bg="#FFFFFF", fg="#000000")
            except:
                pass
    
    print(f"Dark mode: {'enabled' if dark_mode_enabled else 'disabled'}")

# Add to UI:
# dark_mode_button = Button(text="Toggle Dark Mode", command=toggle_dark_mode)
# dark_mode_button.pack(pady=10)

# Initialize state variable
dark_mode_enabled = False
"""
    }
}
```

### 3. Update the Code Analyzer

If your feature requires special handling for insertion, you may need to update the `enhance_code` method in the `CodeAnalyzer` class to properly place the template in the right location.

## Advanced Template Techniques

### Conditional Template Sections

Sometimes you want parts of the template to be included only under certain conditions:

```python
def toggle_dark_mode():
    """Toggle between light and dark theme."""
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled
    
    # For Tkinter
    if 'tkinter' in code or 'Tk' in code:
        # Tkinter-specific theming code
    # For PyQt/PySide
    elif 'PyQt' in code or 'PySide' in code:
        # Qt-specific theming code
    # Generic fallback
    else:
        # Generic theming approach
```

### Framework-Specific Adaptations

Design templates to adapt to the frameworks detected in the code:

```python
"save_load": """
# Add save/load functionality
{% if 'pygame' in code %}
# Pygame-specific save/load implementation
{% elif 'tkinter' in code %}
# Tkinter-specific save/load implementation
{% else %}
# Generic save/load implementation
{% endif %}
"""
```

## Integration Points

Templates should include comments that indicate where and how to integrate the code:

1. **Function definitions**: Typically added at the module level
2. **UI elements**: Added in UI initialization sections
3. **Event handlers**: Added in event processing loops
4. **Initialization code**: Added near the beginning of main functions or entry points

Use clear comments to suggest integration points:

```python
# Add to event loop:
# if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
#     exit_game()

# Add to UI initialization:
# dark_mode_button = Button(root, text="Dark Mode", command=toggle_dark_mode)
# dark_mode_button.pack(side=tk.RIGHT)
```

## Testing Templates

Always test your templates on various code examples to ensure they work correctly:

1. Create a sample application missing the feature
2. Run the framework to enhance it
3. Verify the enhanced code compiles and runs correctly 
4. Check that the feature works as expected
5. Ensure the template integrates well with different coding styles

## Example: Adding a Dark Mode Feature

Let's walk through the complete process of adding a dark mode toggle feature for GUI applications:

### 1. Define the Feature

```python
DEFAULT_FEATURES["gui_app"].append({
    "name": "dark_mode", 
    "description": "Dark mode toggle", 
    "importance": "medium", 
    "pattern": r"(def\s+(?:toggle_dark_mode|switch_theme)|dark_mode|night_mode|theme_switch)"
})
```

### 2. Create the Template

```python
FEATURE_TEMPLATES["gui_app"]["dark_mode"] = """
# Add dark mode functionality
dark_mode_enabled = False  # Global state variable

def toggle_dark_mode():
    """Toggle between light and dark theme."""
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled
    
    if 'tkinter' in globals() or 'Tk' in globals() or 'tk' in globals():
        # Tkinter implementation
        if dark_mode_enabled:
            root.configure(bg="#333333")
            for widget in root.winfo_children():
                try:
                    widget.configure(bg="#333333", fg="#FFFFFF")
                except:
                    pass
        else:
            root.configure(bg="#FFFFFF")
            for widget in root.winfo_children():
                try:
                    widget.configure(bg="#FFFFFF", fg="#000000")
                except:
                    pass
    else:
        # Generic implementation
        print(f"Dark mode: {'enabled' if dark_mode_enabled else 'disabled'}")
        # Implementation would depend on the specific GUI framework

# Add to UI initialization:
# dark_mode_button = Button(root, text="Dark Mode", command=toggle_dark_mode)
# dark_mode_button.pack(side=RIGHT, pady=10)
"""
```

### 3. Test the Feature

```python
# Sample calculator app without dark mode
calculator_code = """
import tkinter as tk

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

root = tk.Tk()
root.title("Simple Calculator")

entry = tk.Entry(root, width=20)
entry.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

for i in range(1, 10):
    btn = tk.Button(button_frame, text=str(i), command=lambda i=i: entry.insert(tk.END, str(i)))
    btn.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)

equal_btn = tk.Button(button_frame, text="=", command=calculate)
equal_btn.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()
"""

# Test the feature addition
analyzer = CodeAnalyzer(MockClassifier(), DEFAULT_FEATURES)
app_type = analyzer.detect_app_type(calculator_code)
missing_features = analyzer.detect_missing_features(calculator_code, app_type)
enhanced_code = analyzer.enhance_code(calculator_code, app_type, missing_features)

# Verify dark mode feature was added
if "dark_mode" in [f["name"] for f in missing_features]:
    print("Dark mode feature was successfully detected as missing")
    if "toggle_dark_mode" in enhanced_code:
        print("Dark mode feature was successfully added")
```

By following these guidelines, you can create effective feature templates that enhance applications with important default functionality, improving the user experience across a wide range of AI-generated applications.
