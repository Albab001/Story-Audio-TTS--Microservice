"""Text cleaning utilities."""
import re


def remove_extra_spaces(text: str) -> str:
    """Remove excessive whitespace."""
    return re.sub(r'\s+', ' ', text.strip())


def clean_quotes(text: str) -> str:
    """Normalize quote characters."""
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace("'", "'").replace("'", "'")
    return text
