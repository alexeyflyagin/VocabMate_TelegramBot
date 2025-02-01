import re
import textwrap

MARKDOWN_CHARS = r"_*[]"


def esc_md(text: str) -> str:
    """
    It allows escaping MARKDOWN V1.
    """
    if not isinstance(text, str):
        raise ValueError(f"The value types is incorrect (text={type(text)})")

    for char in MARKDOWN_CHARS:
        text = text.replace(char, f"\\{char}")

    text = re.sub(r"(?<=\[)([\(\)])", r"\\\1", text)

    return text


def add_counter(text: str, count: int, pattern: str = '{text} ({count})') -> str:
    """
    It adds `count` into the `text`.

    **Default pattern**: `{text} ({count})`

    Example:
        >> add_counter("Some text", 23)\n
        << "Some text (23)"
    """

    if not (isinstance(text, str) and isinstance(count, int) and isinstance(pattern, str)):
        raise ValueError(
            f"The value types is incorrect (text={type(text)}, count={type(count)}, pattern={type(pattern)})")

    if not ('{text}' in pattern and '{count}' in pattern):
        raise ValueError(f"The pattern is incorrect (pattern=\"{pattern}\")")

    return pattern.format(text=text, count=count)


def shorten(text: str, width: int = 24, placeholder: str = "...") -> str:
    """
    Trims the text and adds an ellipsis if it exceeds the specified width.

    :param text: The input text
    :param width: Maximum allowed width of the text
    :param placeholder: The string used to indicate truncation (default is "...")
    :return: The truncated text with an ellipsis if necessary

    Example:
        >>> shorten("This is a very long text that needs to be shortened.", 30)
        Result: 'This is a very long text,...'
    """

    if not isinstance(text, str) or not isinstance(width, int) or not isinstance(placeholder, str):
        raise ValueError(
            f"Invalid argument types: text={type(text)}, width={type(width)}, placeholder={type(placeholder)}")

    short_text = textwrap.shorten(text, width=width, placeholder=placeholder)

    return short_text
