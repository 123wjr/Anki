import os
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
from docx import Document
import re

def process_bold_tags(docx_path):
    """
    处理 .docx 文件中的粗体字，在每段连续的粗体字前添加 <b>，后添加 </b>，并保持原文其他内容不变。
    """
    doc = Document(docx_path)
    processed_text = ""

    for para in doc.paragraphs:
        i = 0
        runs = para.runs
        
        while i < len(runs):
            run = runs[i]
            if run.bold:
                # 开始一个新的粗体字序列
                processed_text += "<u><b>"
                while i < len(runs) and runs[i].bold:
                    processed_text += runs[i].text
                    i += 1
                # 结束粗体字序列
                processed_text += "</b></u>"
            else:
                processed_text += run.text
                i += 1
        processed_text += "\n"
    
    return processed_text

def convert_and_save_to_txt(processed_text, output_folder, file_name):
    """
    将处理后的文本保存为 .txt 文件。
    """
    output_path = os.path.join(output_folder, f"{file_name}.txt")
    
    # 保存为 UTF-8 编码的 .txt 文件
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(processed_text)
    
    return output_path

import re

def process_paragraph(paragraph_text):
    """Process a paragraph to replace parentheses as described."""
    left_count = 1  # Initialize left parenthesis count

    # Function to replace left parentheses with counter
    def replace_left(match):
        nonlocal left_count
        replacement = f"（{{{{c{left_count}::"
        left_count += 1
        return replacement

    # Replace left parentheses `(` with `{{cx::x`
    modified_text = re.sub(r'\（', replace_left, paragraph_text)
    
    # Replace right parentheses `)` with `}}`
    modified_text = re.sub(r'\）', '}}）', modified_text)
    #去除txt中空格

    # Check if the original text had no parentheses, return None to indicate deletion
    if '（' not in paragraph_text and '）' not in paragraph_text:
        return None

    return modified_text

def modify_txt_in_place(file_path):
    """Modify the .txt file in place according to the specified rules."""
    # Read all lines from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # List to store modified paragraphs
    new_paragraphs = []

    # Process each line (paragraph)
    for line in lines:
        modified_text = process_paragraph(line.strip())
        if modified_text:
            new_paragraphs.append(modified_text)

    # Write modified paragraphs back to the original file
    with open(file_path, 'w', encoding='utf-8') as file:
        for para in new_paragraphs:
            file.write(para + '\n')

# Example usage


def handle_drop(event):
    file_path = event.data.strip('{}')  # 处理路径
    if file_path.lower().endswith('.docx'):
        # 获取保存目录
        folder_path = os.path.dirname(file_path)
        subfolder_path = "txt"
        output_folder = os.path.join(folder_path,subfolder_path)
        if output_folder:
            # 处理文档中的粗体字，添加 <b> 和 </b> 标签
            processed_text = process_bold_tags(file_path)
            
            # 获取文件名（不包含扩展名）
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # 保存为 .txt 文件
            output_file = convert_and_save_to_txt(processed_text, output_folder, base_name)
            output_file = modify_txt_in_place(output_file)
            messagebox.showinfo("转换成功", f"文件已处理并保存为：\n{output_file}")
        else:
            messagebox.showwarning("未选择文件夹", "请选择一个保存文件夹。")
    else:
        messagebox.showwarning("不支持的文件类型", "只支持 .docx 文件。")

# 创建主窗口
root = TkinterDnD.Tk()
root.title("拖拽文件并转换为TXT")
root.geometry("400x200")

# 标签提示
label = tk.Label(root, text="将 .docx 文件拖拽到此窗口中", pady=20)
label.pack(expand=True)

# 配置拖拽文件的处理
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drop)

# 运行主循环
root.mainloop()
