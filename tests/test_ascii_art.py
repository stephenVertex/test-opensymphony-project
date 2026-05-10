"""Tests for the ASCII art generator module."""

from test_opsyn.ascii_art import generate_ascii_art, list_fonts, DEFAULT_FONT


def test_generate_ascii_art_default_font():
    result = generate_ascii_art("Hi")
    assert isinstance(result, str)
    assert len(result) > 0
    # "Hi" in standard font should contain pipe and underscore characters
    assert "|" in result
    assert "_" in result


def test_generate_ascii_art_block_font():
    result = generate_ascii_art("Hi", font="block")
    assert isinstance(result, str)
    assert len(result) > 0
    # Block font uses box-drawing characters
    assert "." in result or "|" in result


def test_generate_ascii_art_empty_string():
    result = generate_ascii_art("")
    assert result == ""


def test_generate_ascii_art_returns_multiline():
    result = generate_ascii_art("A")
    lines = result.strip().split("\n")
    assert len(lines) >= 2, "ASCII art should span multiple lines"


def test_generate_ascii_art_with_width():
    result = generate_ascii_art("Hello World", width=40)
    assert isinstance(result, str)
    assert len(result) > 0


def test_list_fonts_returns_nonempty():
    fonts = list_fonts()
    assert isinstance(fonts, list)
    assert len(fonts) > 0


def test_list_fonts_contains_standard():
    fonts = list_fonts()
    assert "standard" in fonts


def test_list_fonts_contains_multiple_fonts():
    fonts = list_fonts()
    assert len(fonts) >= 2, "Should have at least 2 available fonts"


def test_default_font_is_standard():
    assert DEFAULT_FONT == "standard"


def test_generate_ascii_art_different_fonts_produce_different_output():
    standard = generate_ascii_art("A")
    block = generate_ascii_art("A", font="block")
    assert standard != block, "Different fonts should produce different output"