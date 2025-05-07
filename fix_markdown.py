import re
import os

# 進行格式修正：中英之間要有空格，中中之間不能有空格
def fix_format(text):
    # 中文與英數之間補空格
    text = re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])', r'\1 \2', text)
    # 中文與中文之間去掉空格
    text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
    return text

# 修正單行文字
def fix_line(line):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    parts = []
    texts = []
    last_index = 0

    # 抽出連結與前後文字，並將渲染文字加入 texts
    for match in re.finditer(pattern, line):
        start, end = match.span()
        display, url = match.groups()

        before = line[last_index:start]
        texts.append(before)               # 普通文字
        texts.append(display)              # 超連結顯示文字
        parts.append((len(texts) - 1, url))  # 標記哪段要包成 [xx](url)

        last_index = end

    texts.append(line[last_index:])  # 加入最後一段文字

    # 全部合併為一整段進行修正
    fixed_texts = [fix_format(t) for t in texts]

    # 重建原始結構，插入超連結
    for idx, url in parts:
        fixed_texts[idx] = f'[{fixed_texts[idx]}]({url})'

    return ''.join(fixed_texts)

# 修正整個 markdown 檔案
def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = [fix_line(line) for line in lines]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

# 遍歷所有 markdown 檔案
def fix_all_markdown_files():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                fix_file(os.path.join(root, file))

if __name__ == '__main__':
    fix_all_markdown_files()