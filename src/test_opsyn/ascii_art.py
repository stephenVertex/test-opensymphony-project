"""ASCII art generation utilities."""

from art import text2art, FONT_NAMES, ASCII_FONTS


AVAILABLE_FONTS = sorted(set(ASCII_FONTS) & set(FONT_NAMES))
DEFAULT_FONT = "standard"


def generate_ascii_art(text: str, font: str = DEFAULT_FONT, width: int | None = None) -> str:
    """Convert text to ASCII art.

    Args:
        text: The text to render as ASCII art.
        font: Font name to use. Use ``list_fonts()`` to see available options.
        width: Optional maximum line width. Lines exceeding this are wrapped.

    Returns:
        The ASCII art string.
    """
    if not text:
        return ""
    result = text2art(text, font=font)
    if width and width > 0:
        result = _wrap_ascii_art(result, width)
    return result


def list_fonts() -> list[str]:
    """Return available ASCII font names."""
    return list(AVAILABLE_FONTS)


def _wrap_ascii_art(art_text: str, max_width: int) -> str:
    """Wrap ASCII art lines that exceed max_width.

    Each line is split at or before ``max_width``; the wrapped pieces are
    stacked vertically with a blank line separator.
    """
    lines = art_text.split("\n")
    wrapped_chunks: list[list[str]] = []
    current_chunk: list[str] = []

    for line in lines:
        if len(line) > max_width:
            if current_chunk:
                wrapped_chunks.append(current_chunk)
                current_chunk = []
            # Split the line into chunks of max_width
            for i in range(0, len(line), max_width):
                chunk_lines: list[str] = []
                for other_line in lines:
                    chunk_lines.append(other_line[i : i + max_width])
                wrapped_chunks.append(chunk_lines)
            break  # All lines handled at once
        else:
            current_chunk.append(line)

    if current_chunk:
        wrapped_chunks.append(current_chunk)

    if not wrapped_chunks:
        return art_text

    return "\n\n".join("\n".join(chunk) for chunk in wrapped_chunks)