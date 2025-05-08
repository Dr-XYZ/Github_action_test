import re
import sys

def is_chinese(char):
    """Checks if a character is a Chinese character."""
    if char is None: # Handle None input safely
        return False
    # print(f"  [DEBUG] Checking if '{char!r}' is Chinese: {'\u4e00' <= char <= '\u9fff'}")
    return '\u4e00' <= char <= '\u9fff'

def is_chinese_punctuation(char):
    """
    Checks if a character is in the CJK Symbols and Punctuation (U+3000-303F)
    or Fullwidth and Halfwidth Forms (U+FF00-FFEF) Unicode ranges,
    which commonly contain fullwidth punctuation.
    """
    # Handle potential None or whitespace input. Whitespace itself is not punctuation.
    if char is None or char.isspace():
        return False
    is_punct = ('\u3000' <= char <= '\u303F') or ('\uFF00' <= char <= '\uFFEF')
    # print(f"  [DEBUG] Checking if '{char!r}' is Chinese punctuation (U+3000-303F or U+FF00-FFEF): {is_punct}")
    return is_punct

def is_whitespace(char):
    """Checks if a character is a whitespace character."""
    return char is not None and char.isspace()


def extract_param(macro):
    """Extracts the first or second parameter string from a specific macro format."""
    # print(f"  [DEBUG] Extracting param from macro: {macro!r}")
    match = re.match(r'{{.*?\("([^"]+)"(?:,\s*"([^"]*)")?\)}}', macro)
    if match:
        p1 = match.group(1)
        p2 = match.group(2)
        param = p2 if p2 else p1
        # print(f"  [DEBUG] Extracted param: {param!r}")
        return param
    # print("  [DEBUG] Macro format did not match, param extraction failed.")
    return None # Return None if macro format doesn't match


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
    # Use splitlines(keepends=True) to keep original line breaks in each line string
    lines = text.splitlines(keepends=True)
    print(f"Split into {len(lines)} lines.")
    processed_lines = []

    # Define patterns that match macro or link, including surrounding optional SPACES/TABS
    # Use [ \t]* instead of \s* to avoid matching newline characters
    # Groups: (macro_leading_ws, macro, macro_trailing_ws, link_leading_ws, link, link_trailing_ws)
    macro_pattern_ws = r'([ \t]*)({{.*?\(".*?"(?:,\s*".*?")?\)}})([ \t]*)'
    link_pattern_ws = r'([ \t]*)(\[[^\]]+?\]\([^)]+?\))([ \t]*)'

    # Combine patterns for a single re.sub call per line
    # Groups: (macro_leading_ws, macro, macro_trailing_ws) OR (link_leading_ws, link, link_trailing_ws)
    # The groups are numbered sequentially across alternatives: 1,2,3 for macro; 4,5,6 for link
    combined_pattern_ws = f"({macro_pattern_ws})|({link_pattern_ws})"


    print("\n--- Starting line-by-line processing ---")
    for line_num, line in enumerate(lines):
        print(f"\n[LINE {line_num + 1}/{len(lines)}] Processing line: {line!r}")

        # Define nested processing function to access the 'line' variable
        def process_match_with_context(match):
            """Processes a matched macro or link pattern with context from the original line."""
            # Determine which pattern matched and extract groups
            # Check which alternative group (macro or link) is not None
            is_macro = match.group(2) is not None # Group 2 is the macro content
            is_link = match.group(5) is not None  # Group 5 is the link content

            if is_macro:
                # Groups for macro: (ws, macro, ws) are 1, 2, 3
                leading_ws = match.group(1)
                pattern_content = match.group(2)
                trailing_ws = match.group(3)
                # Span of the pattern content itself (macro)
                pattern_content_span = match.span(2)
                print("-" * 30)
                print(f"[CONTEXT_PROCESS] Detected: Macro")
            elif is_link:
                # Groups for link: (ws, link, ws) are 4, 5, 6
                leading_ws = match.group(4)
                pattern_content = match.group(5)
                trailing_ws = match.group(6)
                # Span of the pattern content itself (link)
                pattern_content_span = match.span(5)
                print("=" * 30)
                print(f"[CONTEXT_PROCESS] Detected: Link")
            else:
                 print("[CONTEXT_PROCESS]   Error: Neither macro nor link matched. Returning original.")
                 # Should not happen with correct pattern, but return original match group(0) just in case
                 return match.group(0)


            # Get the start and end indices of the *entire match* (including consumed spaces/tabs)
            full_match_start_index, full_match_end_index = match.span(0)
            # Get the start and end indices of the *pattern content* itself
            pattern_start_index, pattern_end_index = pattern_content_span


            print(f"[CONTEXT_PROCESS]   Pattern: {pattern_content!r}")
            print(f"[CONTEXT_PROCESS]   Original Match Span (in original line): {full_match_start_index, full_match_end_index}")
            print(f"[CONTEXT_PROCESS]   Pattern Content Span (in original line): {pattern_start_index, pattern_end_index}")
            print(f"[CONTEXT_PROCESS]   Original Leading WS: {leading_ws!r}, Original Trailing WS: {trailing_ws!r}")


            # Get the character *immediately* before the *full match span* in the original line
            # This character is OUTSIDE the [ \t]*pattern[ \t]* match
            actual_char_before_full_match = line[full_match_start_index - 1] if full_match_start_index > 0 else None
            # Get the character *immediately* after the *full match span* in the original line
            # This character is OUTSIDE the [ \t]*pattern[ \t]* match
            actual_char_after_full_match = line[full_match_end_index] if full_match_end_index < len(line) else None


            print(f"[CONTEXT_PROCESS]   Actual characters surrounding FULL match: before={actual_char_before_full_match!r}, after={actual_char_after_full_match!r}")


            # Extract internal characters for spacing logic
            internal_start_char = None
            internal_end_char = None
            param = None
            text_inside = None
            is_text_inside_valid = False

            if is_macro:
                 param = extract_param(pattern_content)
                 if param is None:
                      print("[CONTEXT_PROCESS]   Param extraction failed. Returning original match group(0).")
                      return match.group(0) # Return the original text matched (including original spaces/tabs)
                 internal_start_char = param[0] if param else None
                 internal_end_char = param[-1] if param and len(param) > 0 else None
                 print(f"[CONTEXT_PROCESS]   Internal (Param) start='{internal_start_char!r}', end='{internal_end_char!r}'")

            elif is_link:
                link_text_match = re.match(r'(\[[^\]]+?\])(\([^)]+?\))', pattern_content)
                if link_text_match:
                    # link_text_part = link_text_match.group(1) # e.g., [text]
                    # link_url_part = link_text_match.group(2) # e.g., (url)
                    text_inside = link_text_match.group(1)[1:-1] # Text inside brackets []
                    is_text_inside_valid = bool(text_inside)
                    if not is_text_inside_valid:
                         print("[CONTEXT_PROCESS]   Text inside link is empty.")
                    internal_start_char = text_inside[0] if is_text_inside_valid else None
                    internal_end_char = text_inside[-1] if is_text_inside_valid and len(text_inside) > 0 else False
                    print(f"[CONTEXT_PROCESS]   Internal (Link Text) start='{internal_start_char!r}', end='{internal_end_char!r}'")
                else:
                    print("[CONTEXT_PROCESS]   Link format invalid. Returning original match group(0).")
                    return match.group(0) # Return the original text matched (including original spaces/tabs)


            # --- Determine required spacing ---
            # Logic based on standard rules:
            # Add space BEFORE pattern IF:
            #   - actual_char_before_full_match exists
            #   - AND is NOT whitespace (prevents space next to existing space outside the match)
            #   - AND is NOT Chinese punctuation
            #   - AND (is NOT Chinese OR internal_start_char is NOT Chinese) -> i.e., language change or both English/Symbol
            # Add space AFTER pattern IF:
            #   - actual_char_after_full_match exists
            #   - AND is NOT whitespace
            #   - AND is NOT Chinese punctuation
            #   - AND (is NOT Chinese OR internal_end_char is NOT Chinese) -> i.e., language change or both English/Symbol

            add_space_before = False
            add_space_after = False

            # Space BEFORE logic (check actual_char_before_full_match vs internal_start_char)
            print(f"[CONTEXT_PROCESS]   --- Space before logic ---")
            if actual_char_before_full_match is not None:
                 is_whitespace_before = is_whitespace(actual_char_before_full_match)
                 is_punct_before = is_chinese_punctuation(actual_char_before_full_match)
                 is_chinese_before = is_chinese(actual_char_before_full_match)
                 is_internal_start_chinese = is_chinese(internal_start_char) if internal_start_char is not None else False

                 # Add space before if the character before exists, is not whitespace, not punctuation, AND (language changes or both English/Symbol)
                 if not is_whitespace_before and not is_punct_before and (not is_chinese_before or not is_internal_start_chinese):
                      add_space_before = True
                      print(f"[CONTEXT_PROCESS]     Decision: Add space before (context='{actual_char_before_full_match!r}').")
                 else:
                      print(f"[CONTEXT_PROCESS]     Decision: No space before (context='{actual_char_before_full_match!r}').")
            else:
                 print("[CONTEXT_PROCESS]     Decision: No char before full match. No space before.")


            # Space AFTER logic (check actual_char_after_full_match vs internal_end_char)
            print(f"[CONTEXT_PROCESS]   --- Space after logic ---")
            if actual_char_after_full_match is not None:
                 is_whitespace_after = is_whitespace(actual_char_after_full_match)
                 is_punct_after = is_chinese_punctuation(actual_char_after_full_match)
                 is_chinese_after = is_chinese(actual_char_after_full_match)
                 is_internal_end_chinese = is_chinese(internal_end_char) if internal_end_char is not None else False

                 # Add space after if the character after exists, is not whitespace, not punctuation, AND (language changes or both English/Symbol)
                 if not is_whitespace_after and not is_punct_after and (not is_chinese_after or not is_internal_end_chinese):
                      add_space_after = True
                      print(f"[CONTEXT_PROCESS]     Decision: Add space after (context='{actual_char_after_full_match!r}').")
                 else:
                      print(f"[CONTEXT_PROCESS]     Decision: No space after (context='{actual_char_after_full_match!r}').")
            else:
                 print("[CONTEXT_PROCESS]     Decision: No char after full match. No space after.")


            # --- Construct the replacement string ---
            # We replace the *full match* (including original leading/trailing spaces/tabs)
            # with calculated_space + pattern_content + calculated_space
            # Original spaces/tabs matched by [ \t]* are discarded and replaced by our calculated spaces.
            # The newline character, if it was after the trailing [ \t]*, is NOT part of the match and remains untouched.

            final_replacement_segment = (" " if add_space_before else "") + pattern_content + (" " if add_space_after else "")

            # print(f"[CONTEXT_PROCESS]   Original matched segment (group 0): {match.group(0)!r}")
            print(f"[CONTEXT_PROCESS]   Final replacement segment: {final_replacement_segment!r}")
            if is_macro: print("-" * 30)
            if is_link: print("=" * 30)

            # Return the constructed segment
            return final_replacement_segment


        # Use re.sub with the combined pattern and the nested processing function
        # re.sub will find all non-overlapping matches of the combined pattern in 'line'
        # The process_match_with_context function will be called for each match found in the line
        processed_line = re.sub(combined_pattern_ws, process_match_with_context, line)

        processed_lines.append(processed_line)

    print("\n--- Finished line-by-line processing ---")

    print("Joining processed lines back together...")
    # Since splitlines(keepends=True) was used, each line string in processed_lines
    # already includes its original line ending (or is the last line).
    # Simply concatenate the processed lines. The newlines were preserved.
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
