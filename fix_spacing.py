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
    # Handle potential None input if slicing goes out of bounds
    if char is None:
        return False
    is_punct = ('\u3000' <= char <= '\u303F') or ('\uFF00' <= char <= '\uFFEF')
    # print(f"  [DEBUG] Checking if '{char!r}' is Chinese punctuation (U+3000-303F or U+FF00-FFEF): {is_punct}")
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


# The main processing function will be defined inside the loop in fix_spacing_in_file
# to access the current line string.

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
    # Use keepends=True to correctly handle original line breaks
    lines = text.splitlines(keepends=True)
    print(f"Split into {len(lines)} lines.")
    processed_lines = []

    # Define simpler regex patterns that match only the macro or link block
    # This pattern does NOT consume surrounding characters or spaces
    macro_pattern = r'({{.*?\(".*?"(?:,\s*".*?")?\)}})'
    link_pattern = r'(\[[^\]]+?\]\([^)]+?\))'

    print("\n--- Starting line-by-line processing ---")
    for line_num, line in enumerate(lines):
        print(f"\n[LINE {line_num + 1}/{len(lines)}] Processing line: {line!r}")

        # Define nested processing function to access the 'line' variable
        def process_match_with_context(match):
            """Processes a matched macro or link pattern with context from the original line."""
            # match.group(0) is the full matched string (the macro or link block)
            pattern_content = match.group(0)
            # Get the start and end indices of the match in the original line
            start_index, end_index = match.span(0)

            print("-" * 30)
            print(f"[CONTEXT_PROCESS] Processing pattern: {pattern_content!r}")
            print(f"[CONTEXT_PROCESS]   Indices in line: start={start_index}, end={end_index}")

            # Get the character *immediately* before and after the match in the original line
            actual_before_char = line[start_index - 1] if start_index > 0 else None
            actual_after_char = line[end_index] if end_index < len(line) else None

            print(f"[CONTEXT_PROCESS]   Actual surrounding characters: before={actual_before_char!r}, after={actual_after_char!r}")

            # Determine if it's a macro or a link to extract internal text
            is_macro = pattern_content.startswith('{{')
            is_link = pattern_content.startswith('[') # Assuming valid format, one of these must be true

            param = None
            text_inside = None
            is_text_inside_valid = False

            if is_macro:
                print("[CONTEXT_PROCESS]   Detected: Macro")
                param = extract_param(pattern_content)
                # For spacing logic, param[0] and param[-1] are used
                if param is None: # Cannot process spacing rules without param
                     print("[CONTEXT_PROCESS]   Param extraction failed, returning original pattern.")
                     return pattern_content # Return the original macro string
                param_start_char = param[0] if param else None
                param_end_char = param[-1] if param and len(param) > 0 else None
                print(f"[CONTEXT_PROCESS]   Param start='{param_start_char!r}', end='{param_end_char!r}'")

            elif is_link:
                print("[CONTEXT_PROCESS]   Detected: Link")
                # Extract text inside [] for links
                # Assuming link_text part is always match.group(1) from the link pattern
                # With the simplified pattern, the *whole* link is match.group(0)
                # We need to re-parse slightly or rely on the structure [text](url)
                link_text_match = re.match(r'(\[[^\]]+?\])(\([^)]+?\))', pattern_content)
                if link_text_match:
                    link_text = link_text_match.group(1)
                    text_inside = link_text[1:-1]
                    is_text_inside_valid = bool(text_inside)
                    print(f"[CONTEXT_PROCESS]   Text inside link='{text_inside!r}'")
                    if not is_text_inside_valid:
                         print("[CONTEXT_PROCESS]   Text inside link is empty, spacing logic might be simplified.")
                    link_start_char = text_inside[0] if is_text_inside_valid else None
                    link_end_char = text_inside[-1] if is_text_inside_valid and len(text_inside) > 0 else None
                    print(f"[CONTEXT_PROCESS]   Link text start='{link_start_char!r}', end='{link_end_char!r}'")
                else:
                    print("[CONTEXT_PROCESS]   Link format invalid, returning original pattern.")
                    return pattern_content # Return the original link string

            # --- Building the result string: optional_space + pattern + optional_space ---
            prefix_space = ""
            suffix_space = ""

            # Determine internal characters for spacing logic
            internal_start_char = None
            internal_end_char = None
            if is_macro:
                 internal_start_char = param_start_char
                 internal_end_char = param_end_char
            elif is_link and is_text_inside_valid:
                 internal_start_char = link_start_char
                 internal_end_char = link_end_char

            # --- Logic for space *before* the pattern ---
            print(f"[CONTEXT_PROCESS]   --- Space before logic (actual char: {actual_before_char!r}) ---")
            # Add space BEFORE if actual_before_char exists AND is NOT Chinese punctuation AND (is NOT Chinese OR internal_start_char is NOT Chinese)
            if actual_before_char is not None and not is_chinese_punctuation(actual_before_char):
                is_chinese_before = is_chinese(actual_before_char)
                is_internal_start_chinese = is_chinese(internal_start_char) if internal_start_char is not None else False # Treat None internal start as not Chinese

                # Add space if the character before is NOT Chinese OR the internal start is NOT Chinese
                # This covers Eng-Eng, Eng-Chi, Chi-Eng transitions (if before is not punct)
                if not is_chinese_before or not is_internal_start_chinese:
                     print("[CONTEXT_PROCESS]     Decision: Before char exists and not punct, AND (not Chinese or internal start not Chinese), ADD space before.")
                     prefix_space = " "
                else:
                     print("[CONTEXT_PROCESS]     Decision: Before char exists and not punct, AND (is Chinese and internal start is Chinese), NO space before.")
            else:
                 print("[CONTEXT_PROCESS]     Decision: No before char or before char is punctuation, NO space before.")


            # --- Logic for space *after* the pattern ---
            print(f"[CONTEXT_PROCESS]   --- Space after logic (actual char: {actual_after_char!r}) ---")
            # Add space AFTER if actual_after_char exists AND is NOT Chinese punctuation AND (is NOT Chinese OR internal_end_char is NOT Chinese)
            if actual_after_char is not None and not is_chinese_punctuation(actual_after_char):
                is_chinese_after = is_chinese(actual_after_char)
                is_internal_end_chinese = is_chinese(internal_end_char) if internal_end_char is not None else False # Treat None internal end as not Chinese

                # Add space if the character after is NOT Chinese OR the internal end is NOT Chinese
                if not is_chinese_after or not is_internal_end_chinese:
                     print("[CONTEXT_PROCESS]     Decision: After char exists and not punct, AND (not Chinese or internal end not Chinese), ADD space after.")
                     suffix_space = " "
                else:
                     print("[CONTEXT_PROCESS]     Decision: After char exists and not punct, AND (is Chinese and internal end is Chinese), NO space after.")
            else:
                 print("[CONTEXT_PROCESS]     Decision: No after char or after char is punctuation, NO space after.")


            final_result_segment = prefix_space + pattern_content + suffix_space
            print(f"[CONTEXT_PROCESS]   Final constructed segment for replacement: {final_result_segment!r}")
            print("-" * 30)
            return final_result_segment # This replaces the *original* pattern_content


        # Apply the processing function to the current line using the simpler patterns
        # Note: We apply macro processing first, then link processing on the result.
        # The nested function 'process_match_with_context' now encapsulates the logic for BOTH.
        # We need two separate re.sub calls, each using a lambda that wraps the nested function
        # and passes the correct 'is_macro'/'is_link' context, or we just handle both pattern types
        # within a single re.sub call with a combined pattern.

        # Let's use a combined pattern for efficiency and simpler logic flow
        # Match either a macro OR a link
        combined_pattern = r'({{.*?\(".*?"(?:,\s*".*?")?\)}})|(\[[^\]]+?\]\([^)]+?\))'

        # Use re.sub with the combined pattern and the nested processing function
        # The nested function 'process_match_with_context' will be called for each match
        # Match groups for combined_pattern: group(1) for macro, group(2) for link
        processed_line_temp = re.sub(combined_pattern, process_match_with_context, line)

        # The previous separate macro/link processing steps are now combined.
        # We need to update the variable name.
        processed_line = processed_line_temp


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
