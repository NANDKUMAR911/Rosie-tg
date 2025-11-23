from telethon import events
import re

# Prefix variable
PREFIX = r"[*#\$&@/?!]{1,2}"

def command_pattern(commands: str) -> re.Pattern:
    """
    Returns a compiled regex pattern for the given commands string.
    Accepts multiline rest of the message.
    
    Args:
        commands (str): Pipe-separated commands, e.g. "start|help|setlang"
    
    Returns:
        re.Pattern: Compiled regex pattern
    """
    pattern = re.compile(
        rf"^({PREFIX})"       # Group 1: prefix (1 or 2 chars)
        rf"({commands})"      # Group 2: exact command(s)
        r"(?:\s+(.*))?$",     # Group 3: rest of the message (optional)
        re.DOTALL             # Allows multiline text in group 3
    )
    return pattern