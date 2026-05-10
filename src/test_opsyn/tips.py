"""Tip of the day data and retrieval."""

from __future__ import annotations

import random

TIPS: list[str] = [
    "Use keyboard shortcuts to speed up your workflow.",
    "Break large tasks into smaller, manageable sub-tasks.",
    "Write tests before you write code (TDD).",
    "Commit early and often – small commits are easier to review.",
    "Read the error message carefully before debugging.",
    "Document why, not what – code explains what, comments explain why.",
    "Rubber-duck debugging: explain the problem out loud.",
    "Keep functions short and focused on one responsibility.",
    "Version-control your dotfiles for portable setups.",
    "Automate repetitive tasks – invest time to save time.",
    "Use descriptive variable names – future you will thank you.",
    "Take regular breaks; fresh eyes spot bugs faster.",
    "Review your own diff before requesting a code review.",
    "Learn your editor's search-and-replace with regex.",
    "Prefer composition over inheritance for flexible design.",
]


def get_tip(index: int | None = None) -> str:
    """Return a tip string.

    If *index* is given, return that specific tip (modulo the list length).
    Otherwise pick a random tip.
    """
    if index is not None:
        return TIPS[index % len(TIPS)]
    return random.choice(TIPS)