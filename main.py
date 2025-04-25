import argparse
import re
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="DLP Regex Tester: Highlights matches in a text file based on a regex.")
    parser.add_argument("regex", help="The regular expression to test.")
    parser.add_argument("file_path", help="The path to the text file to scan.")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Perform case-insensitive matching.")
    parser.add_argument("-l", "--log-level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help="Set the logging level.")
    return parser


def highlight_matches(text, regex, ignore_case=False):
    """
    Highlights all matches of the regex in the text.
    Uses ANSI escape codes to highlight the matches.
    """
    flags = re.IGNORECASE if ignore_case else 0
    try:
        matches = list(re.finditer(regex, text, flags=flags))
    except re.error as e:
        logging.error(f"Invalid regular expression: {e}")
        return None  # Indicate an error

    highlighted_text = ""
    last_end = 0
    for match in matches:
        start, end = match.span()
        highlighted_text += text[last_end:start]
        highlighted_text += f"\033[1;31m{text[start:end]}\033[0m"  # Red and bold highlight
        last_end = end
    highlighted_text += text[last_end:]
    return highlighted_text


def main():
    """
    Main function to execute the DLP Regex Tester.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Set logging level
    logging.getLogger().setLevel(args.log_level)

    # Input Validation: Check if the file exists.
    try:
        with open(args.file_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        logging.error(f"File not found: {args.file_path}")
        sys.exit(1)
    except IOError as e:
        logging.error(f"Error reading file: {e}")
        sys.exit(1)

    # Core Functionality: Highlight matches and print to console.
    highlighted_text = highlight_matches(text, args.regex, args.ignore_case)

    if highlighted_text is not None:
        print(highlighted_text)


if __name__ == "__main__":
    """
    Entry point of the script.
    """
    main()

# Usage Examples:
# 1. Basic usage: python dlpsim_DLPRegexTester.py "\d{3}-\d{2}-\d{4}" test.txt
# 2. Case-insensitive: python dlpsim_DLPRegexTester.py "[a-z]+@[a-z]+\.com" test.txt -i
# 3. Change the logging level: python dlpsim_DLPRegexTester.py "\d+" test.txt -l DEBUG