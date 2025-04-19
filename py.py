"""
AI‑Powered Code Analyzer & Enhancer Demo
========================================

This script demonstrates:
1. Classifying application type based on keywords
2. Detecting missing default features in the code
3. Suggesting and injecting template code for high‑importance features
"""

import re
import json
import argparse
import sys

from colorama import Fore, Style, init

# Initialize colorama for colored output in terminal
init(autoreset=True)

class AppClassifier:
    """A mock classifier that predicts application type by simple keyword matching."""
    def __init__(self):
        self.keywords = {
            "game":    ["game", "snake", "tetris", "pygame", "arcade", "player"],
            "gui_app": ["gui", "window", "button", "interface", "tkinter", "qt"],
            "cli_tool":["command", "terminal", "shell", "console", "argument"],
            "web_app": ["web", "http", "server", "flask", "django", "request"]
        }

    def predict(self, text: str) -> str:
        """Return the app type whose keyword set matches the most."""
        text = text.lower()
        scores = {app: 0 for app in self.keywords}
        for app, kws in self.keywords.items():
            for kw in kws:
                if kw in text:
                    scores[app] += 1
        # pick the maximum‑score app type
        return max(scores, key=scores.get)

# Define which default features to check for each app type
DEFAULT_FEATURES = {
    "game": [
        {
            "name": "exit_option",
            "description": "Game exit option",
            "importance": "high",
            "pattern": r"(def\s+exit_game|pygame\.QUIT|KEYDOWN\s+and\s+K_ESCAPE)"
        }
    ],
    "gui_app": [
        {
            "name": "close_button",
            "description": "Close window button",
            "importance": "high",
            "pattern": r"(Button\(.+['\"](Close|Exit|Quit)['\"]|root\.destroy\(\))"
        }
    ],
    "cli_tool": [
        {
            "name": "help_command",
            "description": "Help command via argparse",
            "importance": "high",
            "pattern": r"(ArgumentParser|add_argument.+help=|--help|-h)"
        }
    ],
    "web_app": [
        {
            "name": "error_handling",
            "description": "Global error handler",
            "importance": "high",
            "pattern": r"@app\.errorhandler|try:|except"
        }
    ]
}

# Template snippets for each feature
FEATURE_TEMPLATES = {
    "game": {
        "exit_option": """
# === Added: exit_game() function ===
def exit_game():
    \"\"\"Cleanly exit the game and quit pygame.\"\"\"
    print("Exiting game...")
    pygame.quit()
    sys.exit()

# In the main loop, add:
# if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#     exit_game()
"""
    },
    "gui_app": {
        "close_button": """
# === Added: Close Window Button ===
close_btn = tk.Button(root, text="Close", command=root.destroy)
close_btn.pack(padx=10, pady=10)
"""
    },
    "cli_tool": {
        "help_command": """
# === Added: Help Option ===
parser = argparse.ArgumentParser(description="Your tool description")
parser.add_argument("-h", "--help", action="help", help="Show this help message")
args = parser.parse_args()
"""
    },
    "web_app": {
        "error_handling": """
# === Added: Global Error Handler ===
@app.errorhandler(500)
def handle_server_error(e):
    return jsonify({"error": "Internal Server Error"}), 500
"""
    }
}


class CodeAnalyzer:
    """Analyzes code, detects missing features, and injects templates."""
    
    def __init__(self, classifier: AppClassifier, features: dict):
        self.classifier = classifier
        self.features = features

    def detect_app_type(self, code: str, description: str = "") -> str:
        """Combine code + optional description to predict app type."""
        return self.classifier.predict(code + " " + description)
    
        
    def find_missing_features(self, code: str, app_type: str) -> list:
        """Return a list of feature dicts that are missing from the code."""
        missing = []
        for feature in self.features.get(app_type, []):
            if not re.search(feature["pattern"], code, re.IGNORECASE | re.MULTILINE):
                missing.append(feature)
        return missing
    
def enhance_code(self, code, app_type, missing_features):
    """Enhance the code by adding missing default features"""
    enhanced_code = code

    # Only add high-importance features for demonstration
    important_features = [f for f in missing_features if f["importance"] == "high"]

    for feature in important_features:
        if app_type in FEATURE_TEMPLATES and feature["name"] in FEATURE_TEMPLATES[app_type]:
            # Insert the feature code at the proper location based on app type
            if app_type == "game" and "pygame" in code:
                # For Pygame games, insert before the main loop
                main_loop_match = re.search(r'(while\s+.*?:)', code, re.MULTILINE)
                if main_loop_match:
                    insert_pos = main_loop_match.start()
                    feature_code = FEATURE_TEMPLATES[app_type][feature["name"]]
                    enhanced_code = enhanced_code[:insert_pos] + feature_code + enhanced_code[insert_pos:]
                else:
                    # If no main loop found, append to the end
                    feature_code = FEATURE_TEMPLATES[app_type][feature["name"]]
                    enhanced_code += "\n\n" + feature_code

            elif app_type == "gui_app":
                # For GUI apps, try to insert after window creation
                window_match = re.search(r'(root|window)\s*=\s*[Tt]k\.[Tt]k\(\)', code)
                if window_match:
                    # Insert before mainloop()
                    lines = enhanced_code.split('\n')
                    for i, line in enumerate(lines):
                        if 'mainloop()' in line:
                            lines.insert(i, FEATURE_TEMPLATES[app_type][feature["name"]])
                            enhanced_code = '\n'.join(lines)
                            break

            else:
                # For other types, just append to the end of the file
                feature_code = FEATURE_TEMPLATES[app_type][feature["name"]] if app_type in FEATURE_TEMPLATES and feature["name"] in FEATURE_TEMPLATES[app_type] else f"\n# TODO: Add feature: {feature['description']}\n"
                enhanced_code += "\n\n" + feature_code

    return enhanced_code



def highlight_print(text: str, term: str = None):
    """Print 'term' in green if found, else normal text."""
    if term and term in text:
        parts = text.split(term)
        sys.stdout.write(parts[0])
        sys.stdout.write(Fore.GREEN + term + Style.RESET_ALL)
        sys.stdout.write(parts[1] if len(parts) > 1 else "")
        print()
    else:
        print(text)

def demo_with_code(code_example, description):
    """Demonstrate functionality using the given code"""
    print("\n" + "="*80)
    print(f"Demo: {description}")
    print("="*80)
    
    analyzer = CodeAnalyzer(MockClassifier(), DEFAULT_FEATURES)
    
    # Detect application type
    app_type = analyzer.detect_app_type(code_example + " " + description)
    print(f"\nDetected application type: {Fore.CYAN}{app_type}{Style.RESET_ALL}")
    
    # Detect missing features
    missing_features = analyzer.detect_missing_features(code_example, app_type)
    
    if missing_features:
        print(f"\nMissing default features detected:")
        for feature in missing_features:
            importance_color = Fore.RED if feature["importance"] == "high" else Fore.YELLOW
            print(f" - {importance_color}{feature['description']}{Style.RESET_ALL} (Importance: {feature['importance']})")
        
        # Enhance the code
        enhanced_code = analyzer.enhance_code(code_example, app_type, missing_features)
        
        print(f"\nOriginal code: ({len(code_example.split(chr(10)))} lines)")
        print("-"*40)
        print(code_example[:300] + "..." if len(code_example) > 300 else code_example)
        
        print(f"\nEnhanced code: ({len(enhanced_code.split(chr(10)))} lines)")
        print("-"*40)
        
        # Highlight the added part
        diff_start = 0
        for i in range(min(len(code_example), len(enhanced_code))):
            if code_example[i] != enhanced_code[i]:
                diff_start = i
                break
        
        # Show the context around the change
        context_start = max(0, diff_start - 50)
        added_code = enhanced_code[context_start:context_start+500]
        print(added_code + "..." if len(enhanced_code) - context_start > 500 else added_code)
        
        # Display what features were added
        print(f"\nAutomatically added features:")
        for feature in [f for f in missing_features if f["importance"] == "high"]:
            print(f" + {Fore.GREEN}{feature['description']}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}No missing essential features detected!{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="Warp Assistant: analyze Python code and auto‑inject missing features."
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to the Python file to analyze",
        required=True
    )
    args = parser.parse_args()
    # Try to read the file user assigns
    try:
        with open(args.file, "r", encoding="utf-8") as fp:
            source = fp.read()
    except Exception as e:
        print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")
        sys.exit(1)

    # Use the written function and print the result in the command
    run_demo_on_code(source, f"Analysis of {args.file}")


if __name__ == "__main__":
    main()
    

    



这个演示展示了我们的系统如何:
1. 自动识别不同类型的应用（游戏、GUI应用、CLI工具、Web应用等）
2. 检测缺失的关键默认功能（如退出选项、关闭按钮、帮助命令、错误处理等）
3. 智能地向代码中添加这些功能
4. 提供相关的实现建议和注释

在实际的Warp集成中，这个过程将无缝进行，为用户生成更完整、更用户友好的代码。
系统会随着时间学习哪些默认功能对不同类型的应用是必要的，从而不断改进其推荐。
    """)
