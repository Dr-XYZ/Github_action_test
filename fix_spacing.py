import re
import sys

def is_chinese(char):
    """Checks if a character is a Chinese character."""
    # print(f"  [DEBUG] Checking if '{char!r}' is Chinese: {'\u4e00' <= char <= '\u9fff'}")
    return '\u4e00' <= char <= '\u9fff'

def is_chinese_punctuation(char):
    """
    Checks if a character is in the CJK Symbols and Punctuation (U+3000-303F)
    or Fullwidth and Halfwidth Forms (U+FF00-FFEF) Unicode ranges,
    which commonly contain fullwidth punctuation.
    """
    # Handle potential None or whitespace input
    if char is None or char.isspace():
        return False
    is_punct = ('\u3000' <= char <= '\u303F') or ('\uFF00' <= char <= '\uFFEF')
    # print(f"  [DEBUG] Checking if '{char!r}' is Chinese punctuation (U+3000-303F or U+FF00-FFEF): {is_punct}")
    return is_punct

def extract_param(macro):
    """Extracts the first or second parameter string from a specific macro format."""
    # print(f"  [DEBUG] Extracting param from macro: {macro!r}")
    match = re.match(r'{{.*?\("([^"]+)"(?:,\s*"([^"]*)")?\)}}', macro)
    if match:
        p1 = match.group(1)
        p2 = match.group(2)
        param = p2 if p2 is not None else p1 # Use 'is not None' for clarity
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
    # Use keepends=True to correctly handle original line breaks
    lines = text.splitlines(keepends=True)
    print(f"Split into {len(lines)} lines.")
    processed_lines = []

    # Define patterns that match the macro/link AND adjacent optional *horizontal* whitespace
    # Using [ \t]* instead of \s* to avoid matching newlines.
    # Capture groups: (leading_hws, pattern, trailing_hws)
    macro_pattern_hws = r'([ \t]*)({{.*?\(".*?"(?:,\s*".*?")?\)}})([ \t]*)'
    link_pattern_hws = r'([ \t]*)(\[[^\]]+?\]\([^)]+?\))([ \t]*)'

    # Combine patterns for a single re.sub call per line
    # Groups will be: (macro_leading_hws, macro, macro_trailing_hws, link_leading_hws, link, link_trailing_hws)
    # IMPORTANT: Apply [ \t]* to ALL whitespace groups
    combined_pattern_hws = r'([ \t]*)({{.*?\(".*?"(?:,\s*".*?")?\)}})([ \t]*)|([ \t]*)(\[[^\]]+?\]\([^)]+?\))([ \t]*)'

    print("\n--- Starting line-by-line processing ---")
    for line_num, line in enumerate(lines):
        # print(f"\n[LINE {line_num + 1}/{len(lines)}] Processing line: {line!r}") # Keep debug prints minimal

        # Define nested processing function to access the 'line' variable
        def process_match_with_context(match):
            """Processes a matched macro or link pattern with context from the original line."""
            # Determine which pattern matched and extract groups
            is_macro = match.group(2) is not None # Group 2 is macro pattern_content
            is_link = match.group(5) is not None  # Group 5 is link pattern_content

            if is_macro:
                leading_hws = match.group(1)
                pattern_content = match.group(2)
                trailing_hws = match.group(3)
                # Span of the pattern content itself (macro)
                pattern_content_span = match.span(2)
                # print("-" * 30) # Debug print
                # print(f"[CONTEXT_PROCESS] Detected: Macro") # Debug print
            elif is_link:
                leading_hws = match.group(4)
                pattern_content = match.group(5)
                trailing_hws = match.group(6)
                # Span of the pattern content itself (link)
                pattern_content_span = match.span(5)
                # print("=" * 30) # Debug print
                # print(f"[CONTEXT_PROCESS] Detected: Link") # Debug print
            else:
                # print("[CONTEXT_PROCESS]   Error: Neither macro nor link matched. Returning original.") # Debug print
                return match.group(0) # Should not happen with correct pattern

            # Get the start and end indices of the *entire match* (including consumed horizontal whitespace)
            full_match_start_index, full_match_end_index = match.span(0)

            # print(f"[CONTEXT_PROCESS]   Pattern: {pattern_content!r}") # Debug print
            # print(f"[CONTEXT_PROCESS]   Leading HWS: {leading_hws!r}, Trailing HWS: {trailing_hws!r}") # Debug print
            # print(f"[CONTEXT_PROCESS]   Pattern Span (in original line): {pattern_content_span}") # Debug print
            # print(f"[CONTEXT_PROCESS]   Full Match Span (in original line): {full_match_start_index, full_match_end_index}") # Debug print

            # Get the character *immediately* before and after the *full match* in the original line
            actual_char_before_full_match = line[full_match_start_index - 1] if full_match_start_index > 0 else None
            actual_char_after_full_match = line[full_match_end_index] if full_match_end_index < len(line) else None

            # print(f"[CONTEXT_PROCESS]   Actual characters surrounding FULL match: before={actual_char_before_full_match!r}, after={actual_char_after_full_match!r}") # Debug print

            # Extract internal characters for spacing logic
            internal_start_char = None
            internal_end_char = None

            if is_macro:
                param = extract_param(pattern_content)
                if param is None:
                    # print("[CONTEXT_PROCESS]   Param extraction failed. Returning original match group(0).") # Debug print
                    return match.group(0)
                internal_start_char = param[0] if param else None
                internal_end_char = param[-1] if param and len(param) > 0 else None
                # print(f"[CONTEXT_PROCESS]   Internal (Param) start='{internal_start_char!r}', end='{internal_end_char!r}'") # Debug print

            elif is_link:
                link_text_match = re.match(r'(\[[^\]]+?\])(\([^)]+?\))', pattern_content)
                if link_text_match:
                    link_text = link_text_match.group(1)
                    text_inside = link_text[1:-1]
                    is_text_inside_valid = bool(text_inside)
                    if not is_text_inside_valid:
                        # print("[CONTEXT_PROCESS]   Text inside link is empty.") # Debug print
                        pass
                    internal_start_char = text_inside[0] if is_text_inside_valid else None
                    internal_end_char = text_inside[-1] if is_text_inside_valid and len(text_inside) > 0 else None
                    # print(f"[CONTEXT_PROCESS]   Internal (Link Text) start='{internal_start_char!r}', end='{internal_end_char!r}'") # Debug print
                else:
                    # print("[CONTEXT_PROCESS]   Link format invalid. Returning original match group(0).") # Debug print
                    return match.group(0)

            # --- Determine required spacing ---
            add_space_before = False
            add_space_after = False

            # Space BEFORE logic
            # print(f"[CONTEXT_PROCESS]   --- Space before logic (check char before full match: {actual_char_before_full_match!r}) ---") # Debug print
            if actual_char_before_full_match is not None:
                is_punct_before = is_chinese_punctuation(actual_char_before_full_match)
                is_chinese_before = is_chinese(actual_char_before_full_match)
                is_internal_start_chinese = is_chinese(internal_start_char) if internal_start_char is not None else False

                if not is_punct_before and not (is_chinese_before and is_internal_start_chinese):
                    add_space_before = True
                    # print("[CONTEXT_PROCESS]     Decision: Add space before.") # Debug print
                else:
                    # print("[CONTEXT_PROCESS]     Decision: No space before (punct or Chi+Chi).") # Debug print
                    pass
            else:
                # print("[CONTEXT_PROCESS]     Decision: No char before full match (start of line). No space before.") # Debug print
                pass

            # Space AFTER logic
            # print(f"[CONTEXT_PROCESS]   --- Space after logic (check char after full match: {actual_char_after_full_match!r}) ---") # Debug print
            is_line_ending_after = actual_char_after_full_match in ('\n', '\r') if actual_char_after_full_match is not None else False

            if actual_char_after_full_match is not None and not is_line_ending_after:
                is_punct_after = is_chinese_punctuation(actual_char_after_full_match)
                is_chinese_after = is_chinese(actual_char_after_full_match)
                is_internal_end_chinese = is_chinese(internal_end_char) if internal_end_char is not None else False

                if not is_punct_after and not (is_chinese_after and is_internal_end_chinese):
                    add_space_after = True
                    # print("[CONTEXT_PROCESS]     Decision: Add space after.") # Debug print
                else:
                    # print("[CONTEXT_PROCESS]     Decision: No space after (punct, Chi+Chi, or line ending).") # Debug print
                    pass
            else:
                # print("[CONTEXT_PROCESS]     Decision: No char after full match, or it's a line ending. No space after.") # Debug print
                pass

            # --- Construct the replacement string ---
            final_replacement_segment = (" " if add_space_before else "") + pattern_content + (" " if add_space_after else "")

            # print(f"[CONTEXT_PROCESS]   Original matched segment (group 0): {match.group(0)!r}") # Debug print
            # print(f"[CONTEXT_PROCESS]   Final replacement segment: {final_replacement_segment!r}") # Debug print
            # if is_macro: print("-" * 30) # Debug print
            # if is_link: print("=" * 30) # Debug print

            return final_replacement_segment

        # Use re.sub with the combined pattern and the nested processing function
        processed_line = re.sub(combined_pattern_hws, process_match_with_context, line)

        # NEW: Replace "- :" with "- : "
        processed_line = re.sub(r'- :', '- : ', processed_line)

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