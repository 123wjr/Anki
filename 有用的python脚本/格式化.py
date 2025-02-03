def convert_newlines_to_br(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 删除空行并将换行符转换为<br>
    converted_lines = [line.strip() for line in lines if line.strip()]
    result = '<br>'.join(converted_lines)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(result)

# 调用函数并传入文件路径
convert_newlines_to_br('D:/笔记本/课内学习/02数学/测试与预输出/processed_output.txt')