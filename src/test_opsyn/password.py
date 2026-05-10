"""Secure password generator using cryptographically strong randomness."""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass


AMBIGUOUS_CHARS = "0O1lI"


@dataclass
class PasswordOptions:
    """Configuration for password generation."""

    length: int = 16
    upper: bool = True
    lower: bool = True
    digits: bool = True
    symbols: bool = True
    exclude_ambiguous: bool = False


def _build_alphabet(options: PasswordOptions) -> str:
    """Build the character alphabet from the given options."""
    chars = ""
    if options.upper:
        chars += string.ascii_uppercase
    if options.lower:
        chars += string.ascii_lowercase
    if options.digits:
        chars += string.digits
    if options.symbols:
        chars += string.punctuation
    if options.exclude_ambiguous:
        chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
    return chars


def generate_password(options: PasswordOptions | None = None) -> str:
    """Generate a cryptographically secure password.

    By default, the password includes uppercase, lowercase, digits, and
    symbols, and is 16 characters long. At least one character from each
    enabled class is guaranteed to appear.

    Raises:
        ValueError: If no character classes are enabled or length is too short.
    """
    if options is None:
        options = PasswordOptions()

    if not any([options.upper, options.lower, options.digits, options.symbols]):
        msg = "At least one character class must be enabled"
        raise ValueError(msg)

    enabled_classes: list[str] = []
    if options.upper:
        enabled_classes.append(
            "".join(
                c
                for c in string.ascii_uppercase
                if not options.exclude_ambiguous or c not in AMBIGUOUS_CHARS
            )
        )
    if options.lower:
        enabled_classes.append(
            "".join(
                c
                for c in string.ascii_lowercase
                if not options.exclude_ambiguous or c not in AMBIGUOUS_CHARS
            )
        )
    if options.digits:
        enabled_classes.append(
            "".join(
                c
                for c in string.digits
                if not options.exclude_ambiguous or c not in AMBIGUOUS_CHARS
            )
        )
    if options.symbols:
        enabled_classes.append(
            "".join(
                c
                for c in string.punctuation
                if not options.exclude_ambiguous or c not in AMBIGUOUS_CHARS
            )
        )

    # Remove any empty classes (e.g. symbols after ambiguous exclusion)
    enabled_classes = [cls for cls in enabled_classes if cls]

    if not enabled_classes:
        msg = "No characters available after applying options"
        raise ValueError(msg)

    min_length = len(enabled_classes)
    if options.length < min_length:
        msg = f"Length {options.length} is too short for {len(enabled_classes)} enabled classes (minimum {min_length})"
        raise ValueError(msg)

    # Guarantee at least one character from each enabled class
    password_chars = [secrets.choice(cls) for cls in enabled_classes]

    # Fill remaining slots from the full alphabet
    alphabet = _build_alphabet(options)
    remaining = options.length - len(password_chars)
    password_chars.extend(secrets.choice(alphabet) for _ in range(remaining))

    # Shuffle to avoid predictable positions of guaranteed characters
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)
