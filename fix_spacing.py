import re
import sys

# ... (其他函數 is_chinese, extract_param, process_macro, process_link 不變) ...

def is_chinese_punctuation(char):
    """
    Checks if a character is in the CJK Symbols and Punctuation (U+3000-303F)
    or Fullwidth and Halfwidth Forms (U+FF00-FFEF) Unicode ranges,
    which commonly contain fullwidth punctuation.
    """
    # CJK Ideographic Punctuation range (U+3000 to U+303F)
    # Fullwidth ASCII punctuation and other symbols (U+FF00 to U+FFEF)
    return ('\u3000' <= char <= '\u303F') or ('\uFF00' <= char <= '\uFFEF')

# ... (fix_spacing_in_file 和 __main__ 部分不變) ...

# 完整的程式碼如下：

import re
import sys

def is_chinese(char):
    """Checks if a character is a Chinese character."""
    return '\u4e00' <= char <= '\u9fff'

def is_chinese_punctuation(char):
    """
    Checks if a character is in the CJK Symbols and Punctuation (U+3000-303F)
    or Fullwidth and Halfwidth Forms (U+FF00-FFEF) Unicode ranges,
    which commonly contain fullwidth punctuation.
    """
    # CJK Ideographic Punctuation range (U+3000 to U+303F)
    # Fullwidth ASCII punctuation and other symbols (U+FF00 to U+FFEF)
    return ('\u3000' <= char <= '\u303F') or ('\uFF00' <= char <= '\uFFEF')


def extract_param(macro):
    """Extracts the first or second parameter string from a specific macro format."""
    match = re.match(r'{{.*?\("([^"]+)"(?:,\s*"([^"]*)")?\)}}', macro)
    if match:
        # Returns the second parameter if present, otherwise the first
        p1 = match.group(1)
        p2 = match.group(2)
        return p2 if p2 else p1
    return None # Return None if macro format doesn't match

def process_macro(match):
    """Processes a matched macro pattern to add or remove spacing."""
    before = match.group(1) # Character before the macro
    macro = match.group(2)  # The full macro string, e.g., {{macro("param")}}
    after = match.group(3)  # Character after the macro
    param = extract_param(macro) # The text content within the macro

    if not param:
        return before + macro + after

    result = ''

    # --- Logic for spacing *before* the macro ---
    # If the character before is Chinese punctuation (fullwidth), no space is added
    if is_chinese_punctuation(before):
        result += before + macro
    # Otherwise, apply the original rule: add space if before is not Chinese OR macro's param starts with non-Chinese
    elif not (is_chinese(before) and is_chinese(param[0])):
         result += before + ' ' + macro
    else: # before is Chinese AND param[0] is Chinese -> no space
         result += before + macro


    # --- Logic for spacing *after* the macro ---
    # If the character after is Chinese punctuation (fullwidth), no space is added
    if is_chinese_punctuation(after):
        result += after
    # Otherwise, apply the original rule: add space if after is not Chinese OR macro's param ends with non-Chinese
    elif not (is_chinese(after) and is_chinese(param[-1])):
         result += ' ' + after
    else: # after is Chinese AND param[-1] is Chinese -> no space
         result += after

    return result

def process_link(match):
    """Processes a matched link pattern to add or remove spacing."""
    before = match.group(1)    # Character before the link
    link_text = match.group(2) # The link text part, e.g., [顯示文字]
    link_url = match.group(3)    # The link URL part, e.g., (url/path)
    after = match.group(4)     # Character after the link
    # Extract the text inside the brackets [] for language check
    text_inside = link_text[1:-1]

    is_text_inside_valid = bool(text_inside)

    result = ''

    # --- Logic for spacing *before* the link ---
    # If the character before is Chinese punctuation (fullwidth), no space is added
    if is_chinese_punctuation(before):
        result += before + link_text + link_url
    # Otherwise, apply the original rule: add space if before is not Chinese OR link text starts with non-Chinese
    # Also ensure text_inside is not empty before checking its first character
    elif is_text_inside_valid and not (is_chinese(before) and is_chinese(text_inside[0])):
         result += before + ' ' + link_text + link_url
    else: # before is Chinese AND link text starts with Chinese -> no space
         result += before + link_text + link_url

    # --- Logic for spacing *after* the link ---
    # If the character after is Chinese punctuation (fullwidth), no space is added
    if is_chinese_punctuation(after):
        result += after
    # Otherwise, apply the original rule: add space if after is not Chinese OR link text ends with non-Chinese
    # Also ensure text_inside is not empty before checking its last character
    elif is_text_inside_valid and not (is_chinese(after) and is_chinese(text_inside[-1])):
         result += ' ' + after
    else: # after is Chinese AND link text ends with Chinese -> no space
         result += after

    return result


def fix_spacing_in_file(filepath):
    """Reads a markdown file, applies spacing fixes line by line, and writes back."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return

    # Split the text into lines, keeping the original line endings.
    lines = text.splitlines(keepends=True)
    processed_lines = []

    # Regex patterns applied to individual lines.
    macro_pattern = r'(.)\s*({{.*?\(".*?"(?:,\s*".*?")?\)}})\s*(.)'
    link_pattern = r'(.)\s*(\[[^\]]+?\])(\([^)]+?\))\s*(.)'

    for line in lines:
        # Apply macro processing to the current line
        processed_line = re.sub(macro_pattern, process_macro, line)
        # Apply link processing to the result of macro processing on the current line
        processed_line = re.sub(link_pattern, process_link, processed_line)
        processed_lines.append(processed_line)

    # Join the processed lines back together.
    output_text = "".join(processed_lines)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"Spacing fixed in {filepath}")
    except Exception as e:
        print(f"Error writing to file {filepath}: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_spacing.py <markdown_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    fix_spacing_in_file(filepath)
