import importlib
import pkgutil
from .font_style import to_smallcaps

# Main replies store
replies = {}


def load_replies():
    """
    Dynamically load all reply modules in core/replies.
    Merge their 'replies' dict.
    """
    global replies
    replies.clear()

    for module_info in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{__name__}.{module_info.name}")

        if hasattr(module, "replies") and isinstance(module.replies, dict):
            replies.update(module.replies)


def safe_replace(text: str, placeholders: dict):
    """
    Safely replace placeholders in the reply text.

    Example:
        text = "Hello {user}!"
        placeholders = {"user": "Daisy"}
        result = "Hello Daisy!"

    Does NOT use .format() to avoid errors.
    """
    result = text

    for key, value in placeholders.items():
        placeholder = "{" + str(key) + "}"
        result = result.replace(placeholder, str(value))

    return result


def get_reply(key: str, **kwargs):
    """
    Get reply by key.
    Replace placeholders if kwargs provided.

    Example:
        get_reply("welcome", user="Daisy")
    """
    msg = replies.get(key)

    if msg is None:
        return f"Reply not found: {key}"

    if kwargs:
        msg = safe_replace(msg, kwargs)

    return to_smallcaps(msg)


# Load replies on import
load_replies()