import re
import os

def extract_and_replace_links(text):
    pattern = r'\[([^\]]+)\]\([^)]+\)'
    links = []
    def replacer(match):
        links.append(match.group(0))
        return f"[[[LINK_{len(links)-1}]]]"
    text = re.sub(pattern, replacer, text)
    return text, links

def restore_links(text, links):
    for i, link in enumerate(links):
        text = text.replace(f"[[[LINK_{i}]]]", link)
    return text

def fix_format(text):
    text = re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
    return text

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        replaced, links = extract_and_replace_links(line)
        fixed = fix_format(replaced)
        restored = restore_links(fixed, links)
        fixed_lines.append(restored)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

def fix_all_markdown_files():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                fix_file(os.path.join(root, file))

if __name__ == '__main__':
    fix_all_markdown_files()