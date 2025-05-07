import re
import sys
import os

import re

def spacing(text):
    # 1. 刪除中文字+[中文字之間的多餘空格
    text = re.sub(r'([\u4e00-\u9fff])\s+\[([\u4e00-\u9fff])', r'\1[\2', text)

    # 2. 刪除中文字+](link)+中文字之間的多餘空格
    text = re.sub(r'([\u4e00-\u9fff])\s+\]\((.*?)\)\s+([\u4e00-\u9fff])', r'\1](\2)\3', text)

    # 3. 中英混合：英文字 + [ + 中文字，若無空格則加入空格
    text = re.sub(r'([a-zA-Z0-9])\[(?=[\u4e00-\u9fff])', r'\1 [', text)

    # 4. 中英混合：英文字 + ](link) + 中文字，若無空格則加入空格
    def add_space_after_link(match):
        return f"{match.group(1)}](\{match.group(2)}) {match.group(3)}"

    text = re.sub(r'([a-zA-Z0-9])\]\((.*?)\)(?=[\u4e00-\u9fff])', r'\1](\2) \3', text)

    # 5. 中英混合：中文字 + [ + 英文字，若無空格則加入空格
    text = re.sub(r'([\u4e00-\u9fff])\[(?=[a-zA-Z0-9])', r'\1 [', text)

    # 6. 中英混合：中文字 + ](link) + 英文字，若無空格則加入空格
    text = re.sub(r'([\u4e00-\u9fff])\]\((.*?)\)(?=[a-zA-Z0-9])', r'\1](\2) \3', text)

    return text

def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    updated = fix_spacing(content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated)

    print(f"✔ 已處理：{file_path}")

# 取得命令列參數中傳入的檔案路徑
if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        process_markdown_file(file_path)
