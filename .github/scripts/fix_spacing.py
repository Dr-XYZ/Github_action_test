import re
import sys
import os

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'

def is_english_or_number(char):
    return char.isascii() and (char.isalpha() or char.isdigit())

def fix_spacing(text):
    # 一、處理 markdown 連結前後的空格問題
    def link_spacing(match):
        before = match.group(1) or ''
        link_text = match.group(2)  # [文字](網址)
        after = match.group(3) or ''

        # 從 link_text 中提取中括號內的文字
        inner_text = re.search(r'\[([^\]]+)\]', link_text).group(1)
        first_inner = inner_text[0]
        last_inner = inner_text[-1]

        # 判斷需不需要在 before 與 link 之間加空格
        if before and is_chinese(before[-1]) and is_english_or_number(first_inner):
            before += ' '
        elif before and is_english_or_number(before[-1]) and is_chinese(first_inner):
            before += ' '
        elif before and before.endswith(' '):  # 避免多餘空格
            before = before.rstrip()

        # 判斷需不需要在 link 與 after 之間加空格
        if after and is_chinese(after[0]) and is_english_or_number(last_inner):
            after = ' ' + after
        elif after and is_english_or_number(after[0]) and is_chinese(last_inner):
            after = ' ' + after
        elif after and after.startswith(' '):  # 避免多餘空格
            after = after.lstrip()

        return f"{before}{link_text}{after}"

    text = re.sub(r'(.)?(\[[^\]]+\]\([^)]+\))(.?)', link_spacing, text)

    # 二、處理一般中英混合：中→英 / 英→中都要空格
    text = re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])', r'\1 \2', text)

    # 三、移除所有中文與中文之間的多餘空格
    text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)

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
