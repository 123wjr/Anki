import os
import re
import requests

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def process_line_content(line):
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
    new_line = new_line.replace('$$', '').replace('$,$', '').replace('  ', '').replace('$.$', '')
    return new_line

def process_line(line, filename):
    # 替换行内数学环境标识符
    line = re.sub(r'\$(.*?)\$', r' \\(\1\\) ', line)
    line = re.sub(r'  +', r' ', line)
    line = re.sub(r'(\d+)\.\s', r'\1\t', line, count=1)
    filename_part = re.sub(r'[^\u4e00-\u9fa5]', '', filename).replace('.md', '')
    return line.strip() + '\t' + filename_part + '\n'

def download_image(url, mediapath):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(mediapath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"图片 {url} 下载成功，保存到 {mediapath}")
    except Exception as e:
        print(f"下载图片 {url} 时出错: {e}")

def replace_image_links(markdown_file, mediapath):
    if not os.path.exists(mediapath):
        os.makedirs(mediapath)

    content = read_file(markdown_file)
    image_links = re.findall(r'!\[.*?\]\((https?://.*?)\)', content)

    for link in image_links:
        file_name = os.path.join(mediapath, os.path.basename(link))
        download_image(link, file_name)
        relative_path = os.path.relpath(file_name, os.path.dirname(markdown_file))
        content = content.replace(link, relative_path)

    write_file(markdown_file, content)

def process_file_content(content):
    # 转换 aligned 环境为普通环境
    content = re.sub(r'\\begin{aligned}&', '', content)
    content = re.sub(r'\\end{aligned}', '', content)
    
    # 去除 \text{} 外壳但保留其中的内容与前后内容的空格
    content = re.sub(r'\\text{([^}]*)}', r'\1', content)
    content = re.sub(r'\)\\', r') \\', content)
    # 替换 \\&
    content = content.replace('\\\\&', '')
    content = re.sub(r'(?<!<br)(?<!<br\s)(?<!<br\s\/)\s*<\s*(?!br\s*\/?>)(?!img\s*src\s*=\s*")', r' < ', content)
    content = re.sub(r'(?<!<br)(?<!<br\s)(?<!<br\s\/)\s*>\s*(?!br\s*\/?>)(?!img\s*src\s*=\s*")', r' > ', content)
    content = re.sub(r'!\[.*?\]\((.*?)\)', r'<img src="\1">', content)
    return content

def merge_lines(lines, filename):
    merged = []
    errors = []
    current_entry = None
    current_line_num = 0

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            errors.append(f"提示：文件 '{filename}' 第 {line_num} 行存在空行。")
            continue

        if re.match(r'^\d', stripped):
            if current_entry is not None:
                if re.match(r'^\d+\.\s*$', current_entry):
                    errors.append(f"提示：文件 '{filename}' 第 {current_line_num} 行只有序号没有内容。")
                merged.append(current_entry)
            current_entry = stripped
            current_line_num = line_num
        else:
            if current_entry is None:
                errors.append(f"提示：文件 '{filename}' 第 {line_num} 行存在无序号的内容。")
            else:
                current_entry += ' ' + stripped

    if current_entry is not None:
        if re.match(r'^\d+\.\s*$', current_entry):
            errors.append(f"提示：文件 '{filename}' 第 {current_line_num} 行只有序号没有内容。")
        merged.append(current_entry)
    
    return merged, errors

def process_files_in_folder(folder_path):
    output_lines = []
    errors = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            file_path = os.path.join(root, filename)
            replace_image_links(file_path, mediapath)
            content = read_file(file_path)
            content = process_file_content(content)
            write_file(file_path, content)

            lines = content.split('\n')
            merged_lines, file_errors = merge_lines(lines, filename)
            errors.extend(file_errors)

            for line in merged_lines:
                processed_line = process_line(line, filename)
                output_lines.append(processed_line)

    if errors:
        for error in errors:
            print(error)
    else:
        output_path = os.path.join(folder_path, 'processed_output.txt')
        write_file(output_path, ''.join(output_lines))
        print(f"处理完成，结果已保存至 {output_path}")

folder_path_math = r'D:/GitHub/笔记本/课内学习/02数学/数学错题'
folder_path_physics = r'D:/GitHub/笔记本/课内学习/04物理'
mediapath = 'D:/嘉睿吴/AppData/Roaming/Anki2/Jerry/collection.media'
process_files_in_folder(folder_path_math)
process_files_in_folder(folder_path_physics)