import re

# 读取文件内容
with open('D:/OneDrive - 8yb506/电脑与手机/桌面/选中的笔记.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 处理每一行
modified_lines = []
for line in lines:
    columns = line.split('\t')
    if len(columns) >= 5:
        # 只对第6列进行操作
        columns[4] = re.sub(r'([\u4e00-\u9fa5]+)', r'{{c1::\1}}', columns[4])
    modified_lines.append('\t'.join(columns))

# 将修改后的内容写回文件
with open('D:/OneDrive - 8yb506/电脑与手机/桌面/选中的笔记.txt', 'w', encoding='utf-8') as file:
    file.writelines(modified_lines)