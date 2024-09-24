import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES  # 引入 TkinterDnD
import re
import os

def replace_dollars_and_process_lines(md_content):
    """
    处理.md文件内容，替换$符号并合并行。
    """
    lines = md_content.splitlines()
    processed_lines = []
    current_line = ""
    
    
    def replace_dollar(match):
        replace_dollar.counter += 1
        if replace_dollar.counter % 2 == 1:
            return '<anki-mathjax>'
        else:
            return '</anki-mathjax>'
    
    replace_dollar.counter = 0  # 初始化计数器

    for line in lines:
        if line.strip() == "":  # 如果是空行
            if current_line:
                processed_lines.append(current_line)  # 将当前行添加到结果
                current_line = ""
        else:
            processed_line = re.sub(r'\$', replace_dollar, line) + "<br>"
            current_line += processed_line

    if current_line:  # 最后一行可能没有被添加
        processed_lines.append(current_line)

    return "\n".join(processed_lines)

def remove_lines_starting_with(file_path, char):
    # 读取原始文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 筛选出不以指定字符开头的行
    filtered_lines = [line for line in lines if not line.startswith(char)]

    # 将过滤后的内容写回到同一个文件或另存为新文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)

def add_line_numbers(file_path, special_char='*'):
    # 读取处理后的文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 为每一行添加序号和分隔符
    numbered_lines = [
        f"{index + 1}{special_char} {line}" for index, line in enumerate(lines)
    ]

    # 将添加序号后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(numbered_lines)

def process_file(file_path):
    """
    读取.md文件，处理内容后保存为同名.txt文件。
    """
    with open(file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    processed_content = replace_dollars_and_process_lines(md_content)

    txt_file_path = os.path.splitext(file_path)[0] + '.txt'
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(processed_content)
    remove_lines_starting_with(txt_file_path, '#')
    add_line_numbers(txt_file_path,';')
    messagebox.showinfo("完成", f"文件已保存为: {txt_file_path}")

def on_file_drop(event):
    """
    处理文件拖放事件。
    """
    files = root.tk.splitlist(event.data)
    for file_path in files:
        if os.path.isfile(file_path):
            process_file(file_path)

def paste_from_clipboard():
    """
    从剪贴板粘贴文件路径并处理文件。
    """
    file_path = root.clipboard_get().strip()
    if os.path.isfile(file_path):
        process_file(file_path)
    else:
        messagebox.showerror("错误", "剪贴板中的内容不是有效的文件路径")

# 创建主窗口，使用 TkinterDnD2
root = TkinterDnD.Tk()  # 注意这里继承的是 TkinterDnD.Tk 而不是 tk.Tk
root.title("Markdown 文件处理器")

# 创建并放置按钮
paste_button = tk.Button(root, text="从剪贴板粘贴路径并处理", command=paste_from_clipboard)
paste_button.pack(pady=10)

# 配置文件拖放
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_file_drop)

# 启动主循环
root.mainloop()
