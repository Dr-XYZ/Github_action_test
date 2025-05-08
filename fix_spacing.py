import re
import sys

def is_chinese(char):
    """Checks if a character is a Chinese character."""
    # print(f"  [DEBUG] Checking if '{char}' is Chinese: {'\u4e00' <= char <= '\u9fff'}")
    return '\u4e00' <= char <= '\u9fff'

def is_chinese_punctuation(char):
    """
    Checks if a character is in the CJK Symbols and Punctuation (U+3000-303F)
    or Fullwidth and Halfwidth Forms (U+FF00-FFEF) Unicode ranges,
    which commonly contain fullwidth punctuation.
    """
    is_punct = ('\u3000' <= char <= '\u303F') or ('\uFF00' <= char <= '\uFFEF')
    # print(f"  [DEBUG] Checking if '{char}' is Chinese punctuation (U+3000-303F or U+FF00-FFEF): {is_punct}")
    return is_punct


def extract_param(macro):
    """Extracts the first or second parameter string from a specific macro format."""
    print(f"  [DEBUG] Extracting param from macro: {macro!r}")
    match = re.match(r'{{.*?\("([^"]+)"(?:,\s*"([^"]*)")?\)}}', macro)
    if match:
        p1 = match.group(1)
        p2 = match.group(2)
        param = p2 if p2 else p1
        print(f"  [DEBUG] Extracted param: {param!r}")
        return param
    print("  [DEBUG] Macro format did not match, param extraction failed.")
    return None # Return None if macro format doesn't match

def process_macro(match):
    """Processes a matched macro pattern to add or remove spacing."""
    # match.group(0) is the entire matched string including surrounding chars and spaces
    # match.group(1) is the character before
    # match.group(2) is the macro itself
    # match.group(3) is the character after
    full_match_str = match.group(0)
    before = match.group(1)
    macro = match.group(2)
    after = match.group(3)

    print("-" * 30)
    print(f"[MACRO] Processing match: {full_match_str!r}")
    print(f"[MACRO]   Groups: before={before!r}, macro={macro!r}, after={after!r}")

    param = extract_param(macro)

    if not param:
        print("[MACRO]   Param not extracted, returning original match.")
        # Note: The original regex captures spaces into \s*. re.sub replaces match.group(0).
        # If param fails, we return the captured parts, which implicitly removes original spaces.
        # This might not perfectly restore original spacing around failed macros.
        return before + macro + after

    print(f"[MACRO]   Param first char: {param[0]!r}, last char: {param[-1]!r}")

    result = ''

    # --- Logic for spacing *before* the macro ---
    print(f"[MACRO]   --- Spacing before logic (char: {before!r}) ---")
    is_punct_before = is_chinese_punctuation(before)
    is_chinese_before = is_chinese(before)
    is_param_start_chinese = is_chinese(param[0]) if param else False # Added safety check if param somehow empty

    print(f"[MACRO]     Before Checks: is_chinese={is_chinese_before!r}, is_punct={is_punct_before!r}")
    if param:
        print(f"[MACRO]     Param Start is Chinese: {is_param_start_chinese!r}")

    if is_punct_before:
        print("[MACRO]     Decision: Before is punctuation, NO space before.")
        result += before + macro
    # Otherwise, apply the original rule: add space if before is not Chinese OR macro's param starts with non-Chinese
    elif not (is_chinese_before and is_param_start_chinese):
         print("[MACRO]     Decision: Before is not Chinese OR Param Start is not Chinese, ADD space before.")
         result += before + ' ' + macro
    else: # before is Chinese AND param[0] is Chinese -> no space
         print("[MACRO]     Decision: Before is Chinese AND Param Start is Chinese, NO space before.")
         result += before + macro
    print(f"[MACRO]   Intermediate result after adding prefix: {result!r}")


    # --- Logic for spacing *after* the macro ---
    print(f"[MACRO]   --- Spacing after logic (char: {after!r}) ---")
    is_punct_after = is_chinese_punctuation(after)
    is_chinese_after = is_chinese(after)
    is_param_end_chinese = is_chinese(param[-1]) if param and len(param) > 0 else False # Added safety check

    print(f"[MACRO]     After Checks: is_chinese={is_chinese_after!r}, is_punct={is_punct_after!r}")
    if param and len(param) > 0:
        print(f"[MACRO]     Param End is Chinese: {is_param_end_chinese!r}")

    if is_punct_after:
        print("[MACRO]     Decision: After is punctuation, NO space after.")
        result += after
    # Otherwise, apply the original rule: add space if after is not Chinese OR macro's param ends with non-Chinese
    elif not (is_chinese_after and is_param_end_chinese):
         print("[MACRO]     Decision: After is not Chinese OR Param End is not Chinese, ADD space after.")
         result += ' ' + after
    else: # after is Chinese AND param[-1] is Chinese -> no space
         print("[MACRO]     Decision: After is Chinese AND Param End is Chinese, NO space after.")
         result += after

    print(f"[MACRO]   Final constructed segment for replacement: {result!r}")
    print("-" * 30)
    return result

def process_link(match):
    """Processes a matched link pattern to add or remove spacing."""
    # match.group(0) is the entire matched string including surrounding chars and spaces
    # match.group(1) is the character before
    # match.group(2) is the link text part, e.g., [顯示文字]
    # match.group(3) is the link URL part, e.g., (url/path)
    # match.group(4) is the character after
    full_match_str = match.group(0)
    before = match.group(1)
    link_text = match.group(2)
    link_url = match.group(3)
    after = match.group(4)

    print("=" * 30)
    print(f"[LINK] Processing match: {full_match_str!r}")
    print(f"[LINK]   Groups: before={before!r}, link_text={link_text!r}, link_url={link_url!r}, after={after!r}")

    # Extract the text inside the brackets [] for language check
    # Assumes link_text is like [text]
    text_inside = link_text[1:-1]
    print(f"[LINK]   Extracted text inside link: {text_inside!r}")

    # If the text inside the link is empty, handle as an edge case
    is_text_inside_valid = bool(text_inside)
    if not is_text_inside_valid:
        print("[LINK]   Text inside link is empty or invalid, using simplified logic for spacing.")

    result = ''

    # --- Logic for spacing *before* the link ---
    print(f"[LINK]   --- Spacing before logic (char: {before!r}) ---")
    is_punct_before = is_chinese_punctuation(before)
    is_chinese_before = is_chinese(before)
    is_link_start_chinese = is_chinese(text_inside[0]) if is_text_inside_valid else False

    print(f"[LINK]     Before Checks: is_chinese={is_chinese_before!r}, is_punct={is_punct_before!r}")
    if is_text_inside_valid:
        print(f"[LINK]     Link Text Start is Chinese: {is_link_start_chinese!r}")


    if is_punct_before:
        print("[LINK]     Decision: Before is punctuation, NO space before.")
        result += before + link_text + link_url
    # Otherwise, apply the original rule: add space if before is not Chinese OR link text starts with non-Chinese
    # Also ensure text_inside is not empty before checking its first character
    elif is_text_inside_valid and not (is_chinese_before and is_link_start_chinese):
         print("[LINK]     Decision: Before is not Chinese OR Link Text Start is not Chinese, ADD space before.")
         result += before + ' ' + link_text + link_url
    else: # before is Chinese AND link text starts with Chinese -> no space (or text_inside is invalid)
         if not is_text_inside_valid:
              print("[LINK]     Decision: Text inside link is invalid, NO space before.")
         else:
              print("[LINK]     Decision: Before is Chinese AND Link Text Start is Chinese, NO space before.")
         result += before + link_text + link_url
    print(f"[LINK]   Intermediate result after adding prefix: {result!r}")


    # --- Logic for spacing *after* the link ---
    print(f"[LINK]   --- Spacing after logic (char: {after!r}) ---")
    is_punct_after = is_chinese_punctuation(after)
    is_chinese_after = is_chinese(after)
    is_link_end_chinese = is_chinese(text_inside[-1]) if is_text_inside_valid and len(text_inside) > 0 else False

    print(f"[LINK]     After Checks: is_chinese={is_chinese_after!r}, is_punct={is_punct_after!r}")
    if is_text_inside_valid and len(text_inside) > 0:
        print(f"[LINK]     Link Text End is Chinese: {is_link_end_chinese!r}")


    if is_punct_after:
        print("[LINK]     Decision: After is punctuation, NO space after.")
        result += after
    # Otherwise, apply the original rule: add space if after is not Chinese OR link text ends with non-Chinese
    # Also ensure text_inside is not empty before checking its last character
    elif is_text_inside_valid and not (is_chinese_after and is_link_end_chinese):
         print("[LINK]     Decision: After is not Chinese OR Link Text End is not Chinese, ADD space after.")
         result += ' ' + after
    else: # after is Chinese AND link text ends with Chinese -> no space (or text_inside is invalid/short)
         if not (is_text_inside_valid and len(text_inside) > 0):
             print("[LINK]     Decision: Text inside link is invalid or too short, NO space after.")
         else:
             print("[LINK]     Decision: After is Chinese AND Link Text End is Chinese, NO space after.")
         result += after

    print(f"[LINK]   Final constructed segment for replacement: {result!r}")
    print("=" * 30)
    return result


def fix_spacing_in_file(filepath):
    """Reads a markdown file, applies spacing fixes line by line, and writes back."""
    print(f"\n--- Starting file processing for: {filepath} ---")
    try:
        print("Attempting to read file...")
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        print("File read successfully.")
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        print("--- File processing failed ---")
        return
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        print("--- File processing failed ---")
        return

    print("Splitting text into lines, preserving line endings...")
    lines = text.splitlines(keepends=True)
    print(f"Split into {len(lines)} lines.")
    processed_lines = []

    # Regex patterns applied to individual lines.
    macro_pattern = r'(.)\s*({{.*?\(".*?"(?:,\s*".*?")?\)}})\s*(.)'
    link_pattern = r'(.)\s*(\[[^\]]+?\])(\([^)]+?\))\s*(.)'

    print("\n--- Starting line-by-line processing ---")
    for line_num, line in enumerate(lines):
        print(f"\n[LINE {line_num + 1}/{len(lines)}] Processing line: {line!r}")

        # Apply macro processing to the current line
        print(f"[LINE {line_num + 1}] Applying macro pattern: {macro_pattern!r}")
        processed_line = re.sub(macro_pattern, process_macro, line)
        print(f"[LINE {line_num + 1}] Line after macro processing: {processed_line!r}")

        # Apply link processing to the result of macro processing on the current line
        print(f"[LINE {line_num + 1}] Applying link pattern: {link_pattern!r}")
        processed_line = re.sub(link_pattern, process_link, processed_line)
        print(f"[LINE {line_num + 1}] Line after link processing: {processed_line!r}")

        processed_lines.append(processed_line)
    print("\n--- Finished line-by-line processing ---")

    print("Joining processed lines back together...")
    output_text = "".join(processed_lines)
    # print(f"Joined text: {output_text!r}") # Careful: might print very long text

    print(f"\nAttempting to write processed text back to: {filepath}")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"Successfully fixed spacing in {filepath}")
        print("--- File processing complete ---")
    except Exception as e:
        print(f"Error writing to file {filepath}: {e}")
        print("--- File writing failed ---")


if __name__ == '__main__':
    print("--- Script started ---")
    print(f"Command line arguments: {sys.argv}")
    if len(sys.argv) < 2:
        print("Usage: python fix_spacing.py <markdown_file>")
        print("--- Script exiting ---")
        sys.exit(1)

    filepath = sys.argv[1]
    fix_spacing_in_file(filepath)
    print("--- Script finished ---")
