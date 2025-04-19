# Adding New Application Types

This guide explains how to extend the DevMind framework to support new application types beyond the default ones (games, GUI applications, CLI tools, and web applications).

## Table of Contents
- [Understanding the Classification System](#understanding-the-classification-system)
- [Adding a New Application Type](#adding-a-new-application-type)
- [Creating Default Features for the New Type](#creating-default-features-for-the-new-type)
- [Implementing Feature Templates](#implementing-feature-templates)
- [Testing Your New Application Type](#testing-your-new-application-type)
- [Example: Adding Mobile App Support](#example-adding-mobile-app-support)

## Understanding the Classification System

The framework uses a classifier to determine the application type of a given code. Currently, this is implemented as the `MockClassifier` class, which uses keyword matching. In the future, this could be replaced with a machine learning-based classifier.

The current application types are:
- `game`: Games (Snake, Blackjack, etc.)
- `gui_app`: GUI applications (calculators, text editors, etc.)
- `cli_tool`: Command-line tools (file managers, task managers, etc.)
- `web_app`: Web applications (APIs, web services, etc.)

## Adding a New Application Type

To add a new application type, you need to:

1. Update the classifier to recognize the new type
2. Define default features for this type
3. Implement templates for these features

### 1. Update the Classifier

Modify the `MockClassifier` class to include keywords for your new application type:

```python
def __init__(self):
    self.app_keywords = {
        "game": ["game", "snake", "tetris", "pygame", "arcade", "player"],
        "gui_app": ["gui", "window", "button", "interface", "tkinter", "qt"],
        "cli_tool": ["command", "terminal", "shell", "console", "argument"],
        "web_app": ["web", "http", "server", "flask", "django", "request"],
        # Add your new type here
        "mobile_app": ["android", "ios", "mobile", "app", "kivy", "flutter"]
    }
```

## Creating Default Features for the New Type

Next, define what default features should be expected for this application type. Add these to the `DEFAULT_FEATURES` dictionary:

```python
DEFAULT_FEATURES = {
    # Existing types...
    
    "mobile_app": [
        {"name": "back_button", "description": "Back navigation button", "importance": "high", 
         "pattern": r"(def\s+(?:go_back|navigate_back|on_back_pressed)|\.back\(\))"},
        {"name": "settings_menu", "description": "Settings or preferences menu", "importance": "medium", 
         "pattern": r"(def\s+(?:open_settings|show_preferences)|settings_screen)"},
        {"name": "permissions_handling", "description": "Permission request handling", "importance": "high", 
         "pattern": r"(request_permissions|check_permission|on_permission_result)"}
    ]
}
```

Each feature needs:
- `name`: A unique identifier
- `description`: Human-readable description
- `importance`: Priority level ("high", "medium", "low")
- `pattern`: Regular expression to detect if the feature exists

## Implementing Feature Templates

For each feature, implement a template that will be used to add the feature to code that's missing it. Add these to the `FEATURE_TEMPLATES` dictionary:

```python
FEATURE_TEMPLATES = {
    # Existing templates...
    
    "mobile_app": {
        "back_button": """
# Add back button functionality
def handle_back_button():
    """Handle back button press."""
    # Save state if needed
    print("Going back to previous screen")
    # Navigate to previous screen
    previous_screen()

# Add to event handler or UI setup:
# back_button = Button(text="Back")
# back_button.bind(on_press=lambda x: handle_back_button())
""",
        "settings_menu": """
# Add settings menu
def open_settings():
    """Open the settings/preferences screen."""
    print("Opening settings")
    # Navigate to settings screen
    # save_current_state()
    # load_settings_screen()
"""
    }
}
```

## Testing Your New Application Type

Create test code examples for your new application type and verify that the framework:
1. Correctly identifies the application type
2. Properly detects missing features
3. Adds the features in appropriate locations

## Example: Adding Mobile App Support

Here's a complete example of adding support for mobile applications:

```python
# 1. Update the classifier
def __init__(self):
    self.app_keywords = {
        # Existing types...
        "mobile_app": ["android", "ios", "mobile", "kivy", "flutter", "react-native"]
    }

# 2. Define default features
DEFAULT_FEATURES["mobile_app"] = [
    {"name": "back_button", "description": "Back navigation button", "importance": "high", 
     "pattern": r"(def\s+(?:go_back|navigate_back|on_back_pressed)|\.back\(\))"},
    {"name": "settings_menu", "description": "Settings or preferences menu", "importance": "medium", 
     "pattern": r"(def\s+(?:open_settings|show_preferences)|settings_screen)"},
    {"name": "permissions_handling", "description": "Permission request handling", "importance": "high", 
     "pattern": r"(request_permissions|check_permission|on_permission_result)"}
]

# 3. Implement feature templates
FEATURE_TEMPLATES["mobile_app"] = {
    "back_button": """
# Add back button functionality
def handle_back_button():
    """Handle back button press."""
    # Save state if needed
    print("Going back to previous screen")
    # Navigate to previous screen
    previous_screen()

# Add to event handler:
# if event.type == BACK_BUTTON_PRESSED:
#     handle_back_button()
""",
    # Add other templates...
}

# 4. Test with a sample mobile app
mobile_app_code = """
import kivy
from kivy.app import App
from kivy.uix.label import Label

class MyMobileApp(App):
    def build(self):
        return Label(text='Hello Mobile World!')

if __name__ == '__main__':
    MyMobileApp().run()
"""

# Verify detection and enhancement
app_type = analyzer.detect_app_type(mobile_app_code)
assert app_type == "mobile_app"

missing_features = analyzer.detect_missing_features(mobile_app_code, app_type)
assert "back_button" in [f["name"] for f in missing_features]

enhanced_code = analyzer.enhance_code(mobile_app_code, app_type, missing_features)
# Verify the enhanced code includes the back button functionality
```

By following these steps, you can extend the framework to support any application type that AI tools might generate.
