import re
import sys

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'

def extract_param(macro):
    match = re.match(r'{{.*?\("([^"]+)"(?:,\s*"([^"]*)")?\)}}', macro)
    if match:
        p1 = match.group(1)
        p2 = match.group(2)
        return p2 if p2 else p1
    return None

def process_macro(match):
    before = match.group(1)
    macro = match.group(2)
    after = match.group(3)
    param = extract_param(macro)

    if not param:
        return before + macro + after

    result = ''
    if is_chinese(before) and is_chinese(param[0]):
        result += before + macro
    else:
        result += before + ' ' + macro

    if is_chinese(after) and is_chinese(param[-1]):
        result += after
    else:
        result += ' ' + after

    return result

def process_link(match):
    before = match.group(1)
    link_text = match.group(2)
    link_url = match.group(3)
    after = match.group(4)
    text_inside = link_text[1:-1]

    result = ''
    if is_chinese(before) and is_chinese(text_inside[0]):
        result += before + link_text + link_url
    else:
        result += before + ' ' + link_text + link_url

    if is_chinese(after) and is_chinese(text_inside[-1]):
        result += after
    else:
        result += ' ' + after

    return result

def fix_spacing_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    macro_pattern = r'(.)\s*({{.*?\(".*?"(?:,\s*".*?")?\)}})\s*(.)'
    link_pattern = r'(.)\s*(\[[^\]]+?\])(\([^)]+?\))\s*(.)'

    text = re.sub(macro_pattern, process_macro, text)
    text = re.sub(link_pattern, process_link, text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_spacing.py <markdown_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    fix_spacing_in_file(filepath)