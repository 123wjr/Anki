import tkinter as tk
from tkinter import ttk
import re
import time
import threading

# 定义一个包含常见化学物质及其Anki-MathJax表示的字典
chemical_dict = {
    "CO<ruby>3<rt>2－</rt></ruby>": r"CO3^2-",
    "HCO<ruby>3<rt>－</rt></ruby>": r"HCO3^-",
    "SO<ruby>4<rp>(</rp><rt>2－</rt><rp>)</rp></ruby>": r"SO4^2-",
    "SO<ruby>3<rp>(</rp><rt>2－</rt><rp>)</rp></ruby>": r"SO3^2-",
    "NO<ruby>3<rp>(</rp><rt>－</rt><rp>)</rp></ruby>": r"NO3^-",
    "NO<ruby>2<rp>(</rp><rt>－</rt><rp>)</rp></ruby>": r"NO3-",
    "SiO<ruby>3<rp>(</rp><rt>2－</rt><rp>)</rp></ruby>": r"SiO3^2-",
    "PO<ruby>4<rp>(</rp><rt>3－</rt><rp>)</rp></ruby>": r"PO4^3-",
    "AlO<ruby>2<rp>(</rp><rt>－</rt><rp>)</rp></ruby>": r"AlO2^-",
    "NH<ruby>4<rp>(</rp><rt>＋</rt><rp>)</rp></ruby>": r"NH4+",
    
    "H2O": r"H2O",
    "CO2": r"CO2",
    "O2": r"O2",
    "N2": r"N2",
    "NH3": r"NH3",
    "CH4": r"CH4",
    "NaCl": r"NaCl",
    "HCl": r"HCl",
    "H2SO4": r"H2SO4",
    "NaOH": r"NaOH",
    "KCl": r"KCl",
    "CaCO3": r"CaCO3",
    "C6H12O6": r"C6H12O6",
    "C2H5OH": r"C2H5OH",
    "I2": r"I2",
    "I<sub>2</sub>": r"I2",
    "CO<ruby>3<rt>2－</rt></ruby>": r"CO3^2-",
    "Fe2O3": r"Fe2O3",
    "CuSO4": r"CuSO4",
    "AgNO3": r"AgNO3",
    "BaSO4": r"BaSO4",
    "Mg(OH)2": r"Mg(OH)2",
    "Al2O3": r"Al2O3",
    "KNO3": r"KNO3",
    "ZnSO4": r"ZnSO4",
    "Pb(NO3)2": r"Pb(NO3)2",
    "Ca(OH)2": r"Ca(OH)2",
    "Na+": r"Na+",
    "K+": r"K+",
    "Ca^2+": r"Ca^2+",
    "Mg^2+": r"Mg^2+",
    "Cl-": r"Cl-",
    "===":r"->"
}
def convert_to_anki_mathjax(text):
    for key, value in chemical_dict.items():
        text = re.sub(re.escape(key), f"<anki-mathjax>\ce{{re.escape(value)}}</anki-mathjax>", text)
    return text

def update_output():
    while True:
        input_text = input_textbox.get("1.0", tk.END)
        converted_text = convert_to_anki_mathjax(input_text)
        output_textbox.delete("1.0", tk.END)
        output_textbox.insert(tk.END, converted_text)
        time.sleep(0.5)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_textbox.get("1.0", tk.END))
    input_textbox.delete("1.0", tk.END)

# 创建主窗口
root = tk.Tk()
root.title("化学物质转换器")
root.geometry("800x600")

# 创建输入文本框
input_label = ttk.Label(root, text="输入文本：")
input_label.pack(pady=5)
input_textbox = tk.Text(root, height=10, width=80)
input_textbox.pack(pady=5)

# 创建输出文本框
output_label = ttk.Label(root, text="输出文本：")
output_label.pack(pady=5)
output_textbox = tk.Text(root, height=10, width=80)
output_textbox.pack(pady=5)

# 创建复制按钮
copy_button = ttk.Button(root, text="复制", command=copy_to_clipboard)
copy_button.pack(pady=5)

# 启动实时检测线程
threading.Thread(target=update_output, daemon=True).start()

# 运行主循环
root.mainloop()
