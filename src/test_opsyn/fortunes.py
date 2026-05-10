"""Fortune cookie quotes for the test-opsyn CLI."""

import random

FORTUNES: list[str] = [
    "A fresh start will put you on your way.",
    "Don't just think, act!",
    "Your ability to juggle many tasks will take you far.",
    "A stranger is a friend you have not spoken to yet.",
    "Your shoes will make you happy today.",
    "Change can hurt, but it leads to new beginnings.",
    "Your creativity will lead you to great success.",
    "The best prediction for the future is the past.",
    "A smile is your passport into the hearts of others.",
    "Good things come to those who wait.",
    "Your heart is pure and your mind is clear.",
    "Fortune favors the brave.",
    "An unexpected journey opens new doors.",
    "Your talents will be recognized and rewarded.",
    "A pleasant surprise is waiting for you.",
]


def get_random_fortune() -> str:
    """Return a random fortune cookie quote."""
    return random.choice(FORTUNES)
