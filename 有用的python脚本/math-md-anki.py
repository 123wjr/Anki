import os
import re

def process_line(line, filename):
    # 替换行内数学环境标识符
    line = re.sub(r'\$(.*?)\$', r'<anki-mathjax>\1</anki-mathjax>', line)
    
    # 提取序号并添加制表符
    line = re.sub(r'(\d+)\.\s', r'\1\t', line)
    
    # 在行末添加制表符和文件名中除去非汉字的部分
    filename_part = re.sub(r'[^\u4e00-\u9fa5]', '', filename).replace('.md', '')
    line = line.strip() + '\t' + filename_part + '\n'
    
    return line

def process_files_in_folder(folder_path):
    output_lines = []
    errors = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if line.strip() == "":
                        if i + 1 < len(lines) and lines[i + 1].strip() != "":
                            errors.append(f"提示：文件 '{filename}' 第 {i + 1} 行存在空行。")
                    elif re.match(r'^\d+\.\s*$', line):
                        errors.append(f"提示：文件 '{filename}' 第 {i + 1} 行只有序号没有内容。")
                    elif not line.startswith('#') and not re.match(r'^\d+\.\s', line):
                        errors.append(f"提示：文件 '{filename}' 第 {i + 1} 行存在无序号的内容。")
                    elif not line.startswith('#'):
                        processed_line = process_line(line, filename)
                        output_lines.append(processed_line)
    
    if errors:
        for error in errors:
            print(error)
    else:
        output_file_path = os.path.join(folder_path, 'processed_output.txt')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(output_lines)

# 示例调用
folder_path = r'd:/OneDrive - 8yb506/文件/笔记本/课内学习/02数学/数学错题'
process_files_in_folder(folder_path)