import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        new_line = ""
        dollar_count = 0
        i = 0
        while i < len(line):
            char = line[i]
            if char == '$':
                dollar_count += 1
                new_line += char
            elif re.match(r'[\u4e00-\u9fff，。？！]', char):
                if dollar_count % 2 == 1:
                    new_line += f"${char}$"
                else:
                    new_line += char
            else:
                new_line += char
            i += 1
        # 删除连续出现的“$$”
        new_line = new_line.replace('$$', '')
        new_line = new_line.replace('$,$', '')
        new_line = new_line.replace('  ', '')
        new_line = new_line.replace('$.$', '')
        new_lines.append(new_line)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

# 替换为你的文件夹路径
folder_path = 'D:/OneDrive - 8yb506/文件/笔记本/课内学习/02数学/数学错题'
process_folder(folder_path)