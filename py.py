###########################
# This script demonstrates how to use machine learning and code analysis techniques to detect and automatically add missing default functions to complete codes.
# The demonstrations include:
# 1. Classification of Application type 
# 2. Detection of missing functions
# 3. Code enhancement
###########################

import re
import json
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import ast
import numpy as np
from colorama import Fore, Style, init

# Initialize colorama
init()

# Define模拟训练好的分类器
class MockClassifier:
    """模拟一个训练好的应用类型分类器"""
    
    def __init__(self):
        self.app_keywords = {
            "game": ["game", "snake", "tetris", "pygame", "arcade", "player"],
            "gui_app": ["gui", "window", "button", "interface", "tkinter", "qt"],
            "cli_tool": ["command", "terminal", "shell", "console", "argument"],
            "web_app": ["web", "http", "server", "flask", "django", "request"]
        }
    
    def predict(self, text):
        """简单关键词匹配来预测应用类型"""
        text = text.lower()
        scores = {}
        
        for app_type, keywords in self.app_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[app_type] = score
        
        # 返回得分最高的应用类型
        return max(scores.items(), key=lambda x: x[1])[0]

# 默认功能定义
DEFAULT_FEATURES = {
    "game": [
        {"name": "exit_option", "description": "游戏退出选项", "importance": "high", 
         "pattern": r"(def\s+(?:exit|quit|close)_game|if\s+.*?(?:event\.key\s*==\s*(?:pygame\.K_q|pygame\.K_ESCAPE)|event\.type\s*==\s*pygame\.QUIT))"},
        {"name": "pause_function", "description": "游戏暂停功能", "importance": "medium", 
         "pattern": r"def\s+(?:pause|toggle_pause)|paused\s*=\s*not\s*paused"},
        {"name": "restart_option", "description": "游戏重新开始选项", "importance": "medium", 
         "pattern": r"def\s+(?:restart|reset|new_game)|if\s+.*?event\.key\s*==\s*pygame\.K_r"}
    ],
    "gui_app": [
        {"name": "close_button", "description": "关闭窗口按钮", "importance": "high", 
         "pattern": r"(?:Button|QPushButton)\(.*?[\"'](?:Close|Exit|Quit)[\"']|\.destroy\(\)"},
        {"name": "minimize_maximize", "description": "最小化/最大化功能", "importance": "medium", 
         "pattern": r"(?:iconify|deiconify|minimize|maximize|showMinimized|showMaximized)"}
    ],
    "cli_tool": [
        {"name": "help_command", "description": "帮助命令", "importance": "high", 
         "pattern": r"(?:ArgumentParser|add_argument|help=)|\-h|\-\-help"},
        {"name": "version_command", "description": "版本信息", "importance": "medium", 
         "pattern": r"__version__|VERSION|version\s*="}
    ],
    "web_app": [
        {"name": "error_handling", "description": "错误处理", "importance": "high", 
         "pattern": r"try\s*:|except\s+|error_handler|errorhandler"},
        {"name": "logging", "description": "日志记录", "importance": "medium", 
         "pattern": r"log\.|logger\.|logging\."}
    ]
}

# 功能模板代码
FEATURE_TEMPLATES = {
    "game": {
        "exit_option": """
# 添加退出功能
def exit_game():
    """退出游戏"""
    print("退出游戏...")
    pygame.quit()
    quit()

# 在事件处理中添加:
# if event.type == pygame.QUIT:
#     exit_game()
# if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#     exit_game()
""",
        "pause_function": """
# 添加暂停功能
paused = False

def toggle_pause():
    """切换游戏暂停状态"""
    global paused
    paused = not paused
    if paused:
        print("游戏暂停")
    else:
        print("游戏继续")

# 在事件处理中添加:
# if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
#     toggle_pause()
# 在主循环中添加:
# if paused:
#     continue
""",
        "restart_option": """
# 添加重新开始功能
def restart_game():
    """重新开始游戏"""
    global snake_list, snake_length, game_over
    snake_list = []
    snake_length = 1
    game_over = False
    # 重置其他游戏变量...

# 在事件处理中添加:
# if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
#     restart_game()
"""
    },
    "gui_app": {
        "close_button": """
# 添加关闭按钮
close_button = Button(root, text="关闭", command=root.destroy)
close_button.pack(pady=10)
"""
    },
    # 其他应用类型的模板...
}

class CodeAnalyzer:
    """代码分析器，用于检测缺失的默认功能"""
    
    def __init__(self, classifier, default_features):
        self.classifier = classifier
        self.default_features = default_features
    
    def detect_app_type(self, code_or_description):
        """检测应用类型"""
        return self.classifier.predict(code_or_description)
    
    def detect_missing_features(self, code, app_type):
        """检测代码中缺失的默认功能"""
        missing_features = []
        
        if app_type in self.default_features:
            for feature in self.default_features[app_type]:
                if not re.search(feature["pattern"], code, re.IGNORECASE | re.MULTILINE):
                    missing_features.append(feature)
        
        return missing_features
    
    def enhance_code(self, code, app_type, missing_features):
        """增强代码，添加缺失的默认功能"""
        enhanced_code = code
        
        # 仅添加重要性高的功能为演示
        important_features = [f for f in missing_features if f["importance"] == "high"]
        
        for feature in important_features:
            if app_type in FEATURE_TEMPLATES and feature["name"] in FEATURE_TEMPLATES[app_type]:
                # 根据应用类型查找适当位置插入功能
                if app_type == "game" and "pygame" in code:
                    # 对于Pygame游戏，在主循环前插入功能定义
                    main_loop_match = re.search(r'(while\s+.*?:)', code, re.MULTILINE)
                    if main_loop_match:
                        insert_pos = main_loop_match.start()
                        feature_code = FEATURE_TEMPLATES[app_type][feature["name"]]
                        enhanced_code = enhanced_code[:insert_pos] + feature_code + enhanced_code[insert_pos:]
                    else:
                        # 如果找不到主循环，就在文件末尾添加
                        feature_code = FEATURE_TEMPLATES[app_type][feature["name"]]
                        enhanced_code += "\n\n" + feature_code
                elif app_type == "gui_app":
                    # 对于GUI应用，尝试在主窗口创建后添加
                    window_match = re.search(r'(root|window)\s*=\s*[Tt]k\.[Tt]k\(\)', code)
                    if window_match:
                        # 找到适当位置，在窗口创建之后添加
                        lines = enhanced_code.split('\n')
                        for i, line in enumerate(lines):
                            if 'mainloop()' in line:
                                # 在mainloop前添加
                                lines.insert(i, FEATURE_TEMPLATES[app_type][feature["name"]])
                                enhanced_code = '\n'.join(lines)
                                break
                else:
                    # 默认情况下，在文件末尾添加
                    feature_code = FEATURE_TEMPLATES[app_type][feature["name"]] if app_type in FEATURE_TEMPLATES and feature["name"] in FEATURE_TEMPLATES[app_type] else f"\n# TODO: 添加 {feature['description']} 功能\n"
                    enhanced_code += "\n\n" + feature_code
        
        return enhanced_code

def print_with_highlight(text, highlight_term=None):
    """打印高亮文本"""
    if highlight_term and highlight_term in text:
        parts = text.split(highlight_term)
        print(parts[0], end='')
        print(Fore.GREEN + highlight_term + Style.RESET_ALL, end='')
        print(''.join(parts[1:]))
    else:
        print(text)

def demo_with_code(code_example, description):
    """使用给定代码演示功能"""
    print("\n" + "="*80)
    print(f"演示: {description}")
    print("="*80)
    
    analyzer = CodeAnalyzer(MockClassifier(), DEFAULT_FEATURES)
    
    # 检测应用类型
    app_type = analyzer.detect_app_type(code_example + " " + description)
    print(f"\n检测到的应用类型: {Fore.CYAN}{app_type}{Style.RESET_ALL}")
    
    # 分析缺失功能
    missing_features = analyzer.detect_missing_features(code_example, app_type)
    
    if missing_features:
        print(f"\n检测到缺失的默认功能:")
        for feature in missing_features:
            importance_color = Fore.RED if feature["importance"] == "high" else Fore.YELLOW
            print(f" - {importance_color}{feature['description']}{Style.RESET_ALL} (重要性: {feature['importance']})")
        
        # 代码增强
        enhanced_code = analyzer.enhance_code(code_example, app_type, missing_features)
        
        print(f"\n原始代码: ({len(code_example.split(chr(10)))} 行)")
        print("-"*40)
        print(code_example[:300] + "..." if len(code_example) > 300 else code_example)
        
        print(f"\n增强后的代码: ({len(enhanced_code.split(chr(10)))} 行)")
        print("-"*40)
        
        # 高亮显示添加的部分
        diff_start = 0
        for i in range(min(len(code_example), len(enhanced_code))):
            if code_example[i] != enhanced_code[i]:
                diff_start = i
                break
        
        # 显示差异上下文
        context_start = max(0, diff_start - 50)
        added_code = enhanced_code[context_start:context_start+500]
        print(added_code + "..." if len(enhanced_code) - context_start > 500 else added_code)
        
        # 展示添加了哪些功能
        print(f"\n自动添加的功能:")
        for feature in [f for f in missing_features if f["importance"] == "high"]:
            print(f" + {Fore.GREEN}{feature['description']}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}没有检测到缺失的必要默认功能!{Style.RESET_ALL}")

def main():
    """主函数"""
    print(Fore.CYAN + Style.BRIGHT + """
    ===================================================
     默认功能自动添加演示 - Warp增强hackathon项目
    ===================================================
    """ + Style.RESET_ALL)
    
    print("""这个演示展示了如何使用机器学习和代码分析技术来检测并自动添加
缺失的默认功能到应用代码中，适用于多种不同类型的应用程序。
    
在实际的Warp实现中，系统将:
1. 理解用户的自然语言请求
2. 分析生成的代码是否缺少关键默认功能
3. 智能地集成这些功能到代码中适当位置
4. 随着用户反馈不断学习和改进
    """)
    
    # 示例代码集合
    code_examples = {
        # 示例1: 贪吃蛇游戏缺少退出选项
        "贪吃蛇游戏缺少退出选项": """
import pygame
import random

# 初始化pygame
pygame.init()

# 设置游戏窗口
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# 贪吃蛇初始位置和大小
snake_block = 20
snake_x = width / 2
snake_y = height / 2
snake_list = []
snake_length = 1

# 食物位置
food_x = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
food_y = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

# 移动速度和方向
x_change = 0
y_change = 0
clock = pygame.time.Clock()
snake_speed = 15

# 游戏主循环
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -snake_block
                y_change = 0
            elif event.key == pygame.K_RIGHT:
                x_change = snake_block
                y_change = 0
            elif event.key == pygame.K_UP:
                y_change = -snake_block
                x_change = 0
            elif event.key == pygame.K_DOWN:
                y_change = snake_block
                x_change = 0
    
    # 更新蛇的位置
    snake_x += x_change
    snake_y += y_change
    
    # 检测边界碰撞
    if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
        game_over = True
    
    # 画背景
    screen.fill(black)
    
    # 画食物
    pygame.draw.rect(screen, red, [food_x, food_y, snake_block, snake_block])
    
    # 更新蛇
    snake_head = []
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]
    
    # 画蛇
    for segment in snake_list:
        pygame.draw.rect(screen, green, [segment[0], segment[1], snake_block, snake_block])
    
    # 检测食物碰撞
    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
        food_y = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
        snake_length += 1
    
    pygame.display.update()
    clock.tick(snake_speed)

pygame.quit()
""",

        # 示例2: 简单GUI应用缺少关闭按钮
        "简单GUI计算器应用缺少关闭按钮": """
import tkinter as tk

root = tk.Tk()
root.title("简单计算器")
root.geometry("300x200")

# 创建输入框
entry = tk.Entry(root, width=20)
entry.pack(pady=10)

# 创建按钮框架
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 添加数字按钮
for i in range(1, 10):
    btn = tk.Button(button_frame, text=str(i), width=5)
    btn.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)

# 添加操作按钮
plus_btn = tk.Button(button_frame, text="+", width=5)
plus_btn.grid(row=3, column=0, padx=5, pady=5)

zero_btn = tk.Button(button_frame, text="0", width=5)
zero_btn.grid(row=3, column=1, padx=5, pady=5)

equal_btn = tk.Button(button_frame, text="=", width=5)
equal_btn.grid(row=3, column=2, padx=5, pady=5)

root.mainloop()
""",

        # 示例3: 21点游戏缺少退出和重新开始选项
        "21点游戏缺少退出和重新开始选项": """
import random

def deal_card():
    """返回一张随机牌"""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """计算手牌得分"""
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # 黑杰克 (A + 10)
    
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    
    return sum(cards)

def compare(user_score, computer_score):
    """比较玩家和电脑的分数"""
    if user_score == computer_score:
        return "平局！"
    elif computer_score == 0:
        return "你输了，对手有黑杰克！"
    elif user_score == 0:
        return "你赢了，有黑杰克！"
    elif user_score > 21:
        return "你输了，爆牌了！"
    elif computer_score > 21:
        return "你赢了，对手爆牌了！"
    elif user_score > computer_score:
        return "你赢了！"
    else:
        return "你输了！"

def play_game():
    """开始游戏"""
    user_cards = []
    computer_cards = []
    game_over = False
    
    # 发两张牌给玩家和电脑
    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
    
    # 玩家回合
    while not game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        
        print(f"你的牌: {user_cards}, 当前分数: {user_score}")
        print(f"电脑的第一张牌: {computer_cards[0]}")
        
        if user_score == 0 or computer_score == 0 or user_score > 21:
            game_over = True
        else:
            should_continue = input("输入 'y' 再要一张牌, 输入 'n' 停牌: ")
            if should_continue == 'y':
                user_cards.append(deal_card())
            else:
                game_over = True
    
    # 电脑回合
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)
    
    print(f"你的最终手牌: {user_cards}, 最终分数: {user_score}")
    print(f"电脑的最终手牌: {computer_cards}, 最终分数: {computer_score}")
    print(compare(user_score, computer_score))

# 启动游戏
play_game()
""",

        # 示例4: 命令行工具缺少帮助选项
        "命令行工具缺少帮助和版本选项": """
import os
import shutil
import time

def list_files(directory='.'):
    """列出指定目录下的所有文件"""
    print(f"目录 {directory} 中的文件:")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        last_modified = time.ctime(os.path.getmtime(item_path))
        size = os.path.getsize(item_path)
        
        if os.path.isdir(item_path):
            print(f"[DIR]  {item:30} {last_modified:30} {size:10} bytes")
        else:
            print(f"[FILE] {item:30} {last_modified:30} {size:10} bytes")

def search_files(keyword, directory='.'):
    """搜索包含关键词的文件"""
    print(f"搜索包含 '{keyword}' 的文件:")
    found = False
    
    for root, _, files in os.walk(directory):
        for file in files:
            if keyword.lower() in file.lower():
                file_path = os.path.join(root, file)
                print(f"找到: {file_path}")
                found = True
    
    if not found:
        print(f"没有找到包含 '{keyword}' 的文件")

def copy_file(source, destination):
    """复制文件"""
    try:
        shutil.copy2(source, destination)
        print(f"已复制: {source} -> {destination}")
    except Exception as e:
        print(f"复制失败: {e}")

def main():
    """主函数"""
    # 简单命令解析
    import sys
    
    if len(sys.argv) < 2:
        print("请提供一个命令")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        if len(sys.argv) > 2:
            list_files(sys.argv[2])
        else:
            list_files()
    elif command == "search":
        if len(sys.argv) > 2:
            if len(sys.argv) > 3:
                search_files(sys.argv[2], sys.argv[3])
            else:
                search_files(sys.argv[2])
        else:
            print("请提供搜索关键词")
    elif command == "copy":
        if len(sys.argv) > 3:
            copy_file(sys.argv[2], sys.argv[3])
        else:
            print("请提供源文件和目标路径")
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
""",

        # 示例5: Web应用缺少错误处理
        "Web应用缺少错误处理": """
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 数据库连接
def get_db():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT
    )
    ''')
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

@app.route('/contacts', methods=['GET'])
def get_contacts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(contacts)

@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.json
    name = data['name']
    email = data['email']
    phone = data.get('phone', '')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)',
        (name, email, phone)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Contact added', 'id': cursor.lastrowid}), 201

@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    contact = dict(cursor.fetchone())
    conn.close()
    
    return jsonify(contact)

@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?',
        (name, email, phone, contact_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Contact updated'})

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Contact deleted'})

if __name__ == '__main__':
    app.run(debug=True)
"""
    }
    
    # 运行演示 - 让用户选择示例
    print(f"\n{Fore.YELLOW}可用的示例代码:{Style.RESET_ALL}")
    for i, (desc, _) in enumerate(code_examples.items(), 1):
        print(f"{i}. {desc}")
    
    print("\n选择运行方式:")
    print("1. 运行所有示例")
    print("2. 选择特定示例运行")
    choice = input("请输入选择 (1/2): ").strip()
    
    if choice == "1":
        # 运行所有示例
        for desc, code in code_examples.items():
            demo_with_code(code, desc)
            print("\n" + "-"*80 + "\n")
    else:
        # 运行特定示例
        while True:
            try:
                example_num = int(input(f"请选择示例 (1-{len(code_examples)}): ").strip())
                if 1 <= example_num <= len(code_examples):
                    desc = list(code_examples.keys())[example_num-1]
                    demo_with_code(code_examples[desc], desc)
                    
                    run_another = input("\n运行另一个示例? (y/n): ").strip().lower()
                    if run_another != 'y':
                        break
                else:
                    print(f"请输入1到{len(code_examples)}之间的数字")
            except ValueError:
                print("请输入有效的数字")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}演示总结:{Style.RESET_ALL}")
    print("""
这个演示展示了我们的系统如何:
1. 自动识别不同类型的应用（游戏、GUI应用、CLI工具、Web应用等）
2. 检测缺失的关键默认功能（如退出选项、关闭按钮、帮助命令、错误处理等）
3. 智能地向代码中添加这些功能
4. 提供相关的实现建议和注释

在实际的Warp集成中，这个过程将无缝进行，为用户生成更完整、更用户友好的代码。
系统会随着时间学习哪些默认功能对不同类型的应用是必要的，从而不断改进其推荐。
    """)

if __name__ == "__main__":
    main()
