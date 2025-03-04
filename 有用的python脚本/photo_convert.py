#将markdown中网络图片转化为本地图片
import os
import re
import requests
from urllib.parse import urlparse

def download_image(url, save_dir):
    response = requests.get(url)
    if response.status_code == 200:
        parsed_url = urlparse(url)
        image_name = os.path.basename(parsed_url.path)
        image_path = image_name
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    return None

def process_markdown_file(file_path, save_dir):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_image(match):
        url = match.group(1)
        local_image_path = download_image(url, save_dir)
        if local_image_path:
            return f'<img src="{local_image_path}">'
        return match.group(0)

    new_content = re.sub(r'!\[.*?\]\((http[s]?://.*?)\)', replace_image, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def process_markdown_files_in_directory(directory, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_markdown_file(file_path, save_dir)

# 使用示例
markdown_directory = 'D:/Github/笔记本/课内学习/02数学/数学错题'
images_save_directory = 'C:/Users/嘉睿吴/AppData/Roaming/Anki2/Jerry/collection.media'
process_markdown_files_in_directory(markdown_directory, images_save_directory)