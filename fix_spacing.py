import re
import sys

# ... (is_chinese, is_chinese_punctuation, extract_param functions remain the same) ...

def fix_spacing_in_file(filepath):
    """Reads a markdown file, applies spacing fixes line by line, and writes back."""
    print(f"\n--- Starting file processing for: {filepath} ---")
    try:
        print("Attempting to read file...")
        # Read the entire content
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

    # Define patterns that match the macro/link AND adjacent optional whitespace
    # Capture groups: (leading_ws, pattern, trailing_ws)
    # combined_pattern_ws remains the same as it correctly identifies segments
    combined_pattern_ws = r'(\s*)({{.*?\(".*?"(?:,\s*".*?")?\)}})(\s*)|(\s*)(\[[^\]]+?\]\([^)]+?\))(\s*)'


    print("\n--- Starting line-by-line processing ---")
    for line_num, line in enumerate(lines):
        print(f"\n[LINE {line_num + 1}/{len(lines)}] Processing line: {line!r}")

        # Store the original line ending
        # splitlines(keepends=True) ensures the ending is part of 'line'
        original_ending = ""
        if line.endswith('\r\n'):
            original_ending = '\r\n'
        elif line.endswith('\n'):
            original_ending = '\n'

        print(f"[LINE {line_num + 1}] Original ending: {original_ending!r}")

        # Define nested processing function to access the 'line' variable (remains the same)
        def process_match_with_context(match):
            # ... (function content remains exactly as before) ...
            # This function's logic for calculating replacement is correct for the segment spacing.
            # The issue is how re.sub applies it relative to the line ending,
            # which we will fix *after* re.sub.
            # ... (return final_replacement_segment) ...

             # Determine which pattern matched and extract groups
            is_macro = match.group(2) is not None # Group 2 is macro part
            is_link = match.group(5) is not None  # Group 5 is link part

            if is_macro:
                leading_ws = match.group(1)
                pattern_content = match.group(2)
                trailing_ws = match.group(3)
                pattern_content_span = match.span(2)
                print("-" * 30)
                print(f"[CONTEXT_PROCESS] Detected: Macro")
            elif is_link:
                leading_ws = match.group(4)
                pattern_content = match.group(5)
                trailing_ws = match.group(6)
                pattern_content_span = match.span(5)
                print("=" * 30)
                print(f"[CONTEXT_PROCESS] Detected: Link")
            else:
                 print("[CONTEXT_PROCESS]   Error: Neither macro nor link matched. Returning original.")
                 return match.group(0) # Should not happen with correct pattern


            # Get the start and end indices of the *pattern content* in the original line
            pattern_start_index, pattern_end_index = pattern_content_span
            # Get the start and end indices of the *entire match* (including consumed whitespace)
            full_match_start_index, full_match_end_index = match.span(0)


            print(f"[CONTEXT_PROCESS]   Pattern: {pattern_content!r}")
            print(f"[CONTEXT_PROCESS]   Leading WS: {leading_ws!r}, Trailing WS: {trailing_ws!r}")
            print(f"[CONTEXT_PROCESS]   Pattern Span (in original line): {pattern_content_span}")
            print(f"[CONTEXT_PROCESS]   Full Match Span (in original line): {full_match_start_index, full_match_end_index}")


            # Get the character *immediately* before and after the *full match* in the original line
            # These are the characters OUTSIDE the segment matched by the pattern (including \s*)
            actual_char_before_full_match = line[full_match_start_index - 1] if full_match_start_index > 0 else None
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
                      # Return the original text matched by the pattern (including original whitespace)
                      return match.group(0)
                 internal_start_char = param[0] if param else None
                 internal_end_char = param[-1] if param and len(param) > 0 else None
                 print(f"[CONTEXT_PROCESS]   Internal (Param) start='{internal_start_char!r}', end='{internal_end_char!r}'")

            elif is_link:
                link_text_match = re.match(r'(\[[^\]]+?\])(\([^)]+?\))', pattern_content)
                if link_text_match:
                    link_text = link_text_match.group(1)
                    text_inside = link_text[1:-1]
                    is_text_inside_valid = bool(text_inside)
                    if not is_text_inside_valid:
                         print("[CONTEXT_PROCESS]   Text inside link is empty.")
                    internal_start_char = text_inside[0] if is_text_inside_valid else None
                    internal_end_char = text_inside[-1] if is_text_inside_valid and len(text_inside) > 0 else None
                    print(f"[CONTEXT_PROCESS]   Internal (Link Text) start='{internal_start_char!r}', end='{internal_end_char!r}'")
                else:
                    print("[CONTEXT_PROCESS]   Link format invalid. Returning original match group(0).")
                    # Return the original text matched by the pattern (including original whitespace)
                    return match.group(0)


            # --- Determine required spacing ---
            # Logic based on: Punctuation => NO space. Otherwise, Chi-Chi => NO space. Others => ADD space.
            add_space_before = False
            add_space_after = False

            # Space BEFORE logic (check actual_char_before_full_match)
            print(f"[CONTEXT_PROCESS]   --- Space before logic (check char before full match: {actual_char_before_full_match!r}) ---")
            if actual_char_before_full_match is not None:
                 # Ignore whitespace before actual_char_before_full_match as the pattern's \s* should handle leading whitespace
                 # We only care about the non-whitespace char immediately before the *full* match or it being None.
                 # If the char immediately before is whitespace that wasn't consumed by leading_ws, something is wrong with pattern or logic.
                 # Assuming the pattern's leading \s* works, actual_char_before_full_match is the char *before* the consumed whitespace.
                 is_punct_before = is_chinese_punctuation(actual_char_before_full_match)
                 is_chinese_before = is_chinese(actual_char_before_full_match)
                 is_internal_start_chinese = is_chinese(internal_start_char) if internal_start_char is not None else False

                 # Add space before if actual_char_before_full_match is NOT punctuation AND NOT (Chinese char AND Internal start is Chinese)
                 # AND actual_char_before_full_match is NOT whitespace itself (the pattern handles removing leading whitespace)
                 if not actual_char_before_full_match.isspace() and not is_punct_before and not (is_chinese_before and is_internal_start_chinese):
                      add_space_before = True
                      print("[CONTEXT_PROCESS]     Decision: Add space before.")
                 else:
                      print("[CONTEXT_PROCESS]     Decision: No space before (whitespace, punct, or Chi+Chi).")
            else:
                 print("[CONTEXT_PROCESS]     Decision: No char before full match. No space before.")


            # Space AFTER logic (check actual_char_after_full_match)
            print(f"[CONTEXT_PROCESS]   --- Space after logic (check char after full match: {actual_char_after_full_match!r}) ---")
            if actual_char_after_full_match is not None:
                 # Same logic as before, but for the character after the *full* match.
                 is_punct_after = is_chinese_punctuation(actual_char_after_full_match)
                 is_chinese_after = is_chinese(actual_char_after_full_match)
                 is_internal_end_chinese = is_chinese(internal_end_char) if internal_end_char is not None else False

                 # Add space after if actual_char_after_full_match is NOT punctuation AND NOT (Chinese char AND Internal end is Chinese)
                 # AND actual_char_after_full_match is NOT whitespace itself (the pattern handles removing trailing whitespace)
                 if not actual_char_after_full_match.isspace() and not is_punct_after and not (is_chinese_after and is_internal_end_chinese):
                      add_space_after = True
                      print("[CONTEXT_PROCESS]     Decision: Add space after.")
                 else:
                      print("[CONTEXT_PROCESS]     Decision: No space after (whitespace, punct, or Chi+Chi).")
            else:
                 print("[CONTEXT_PROCESS]     Decision: No char after full match. No space after.")


            # --- Construct the replacement string ---
            # We replace the *full match* (including original leading/trailing whitespace)
            # with calculated_space + pattern_content + calculated_space
            # Note: This means original spaces matched by \s* are DISCARDED and replaced by our single calculated space or no space.

            final_replacement_segment = (" " if add_space_before else "") + pattern_content + (" " if add_space_after else "")

            print(f"[CONTEXT_PROCESS]   Original matched segment (group 0): {match.group(0)!r}")
            print(f"[CONTEXT_PROCESS]   Final replacement segment: {final_replacement_segment!r}")
            if is_macro: print("-" * 30)
            if is_link: print("=" * 30)

            return final_replacement_segment


        # Use re.sub with the combined pattern and the nested processing function
        # This might result in a line without its original ending if the pattern matched it.
        processed_line_intermediate = re.sub(combined_pattern_ws, process_match_with_context, line)

        print(f"[LINE {line_num + 1}] Intermediate result (before fixing ending): {processed_line_intermediate!r}")

        # --- Fix the newline issue ---
        # Ensure the processed line has the same ending as the original line.
        # Strip any trailing whitespace (including potential newline) from the intermediate result
        # and then append the original ending.

        processed_line_content = processed_line_intermediate.rstrip()

        # Append the original ending back
        processed_line = processed_line_content + original_ending

        print(f"[LINE {line_num + 1}] Final processed line (after fixing ending): {processed_line!r}")


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
