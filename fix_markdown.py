import re
import os

# 修正文字中的中英空格與中中空格
def fix_format(text):
    # 中後英補空格
    text = re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])', r'\1 \2', text)
    # 英後中補空格
    text = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])', r'\1 \2', text)
    # 中文與中文之間不能有空格
    text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
    return text

# 修正單行
def fix_line(line):
    # 將超連結依照 pattern 拆開：[文字](連結)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    parts = []
    last_index = 0

    for match in re.finditer(pattern, line):
        start, end = match.span()
        # 處理連結前的普通文字
        before = line[last_index:start]
        parts.append(fix_format(before))

        # 處理超連結內的顯示文字（修正格式）
        text = fix_format(match.group(1))
        url = match.group(2)
        parts.append(f"[{text}]({url})")

        last_index = end

    # 處理剩餘部分
    parts.append(fix_format(line[last_index:]))

    return ''.join(parts)

# 處理整個 markdown 檔案
def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = [fix_line(line) for line in lines]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

# 遍歷所有 md 檔案
def fix_all_markdown_files():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                fix_file(os.path.join(root, file))

if __name__ == '__main__':
    fix_all_markdown_files()