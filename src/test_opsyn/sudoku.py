"""Sudoku puzzle generator with configurable difficulty."""

from __future__ import annotations

import random
from enum import Enum
from typing import Optional


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


# Number of clues (filled cells) to leave for each difficulty level.
CLUE_COUNTS: dict[Difficulty, int] = {
    Difficulty.easy: 38,
    Difficulty.medium: 30,
    Difficulty.hard: 25,
}

Grid = list[list[int]]


def _shuffled(seq: list[int]) -> list[int]:
    """Return a shuffled copy of *seq*."""
    s = seq.copy()
    random.shuffle(s)
    return s


def _is_valid_placement(grid: Grid, row: int, col: int, num: int) -> bool:
    """Check whether *num* can be placed at (row, col) without breaking rules."""
    if num in grid[row]:
        return False
    for r in range(9):
        if grid[r][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                return False
    return True


def _fill_grid(grid: Grid) -> bool:
    """Fill *grid* in-place using backtracking with randomised candidates."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for num in _shuffled(list(range(1, 10))):
                    if _is_valid_placement(grid, r, c, num):
                        grid[r][c] = num
                        if _fill_grid(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True


def generate_solved_grid() -> Grid:
    """Return a completely filled, valid 9x9 sudoku grid."""
    grid: Grid = [[0] * 9 for _ in range(9)]
    _fill_grid(grid)
    return grid


def _count_solutions(grid: Grid, limit: int = 2) -> int:
    """Count solutions for *grid*, stopping as soon as *limit* is reached."""
    count = 0

    def _solve(g: Grid) -> None:
        nonlocal count
        if count >= limit:
            return
        for r in range(9):
            for c in range(9):
                if g[r][c] == 0:
                    for num in range(1, 10):
                        if _is_valid_placement(g, r, c, num):
                            g[r][c] = num
                            _solve(g)
                            g[r][c] = 0
                            if count >= limit:
                                return
                    return
        count += 1

    _solve(grid)
    return count


def _has_unique_solution(grid: Grid) -> bool:
    """Return True if *grid* has exactly one solution."""
    return _count_solutions([row.copy() for row in grid], limit=2) == 1


def generate_puzzle(
    difficulty: Difficulty = Difficulty.medium,
    solved_grid: Optional[Grid] = None,
) -> tuple[Grid, Grid]:
    """Generate a sudoku puzzle and return (puzzle, solution).

    The *puzzle* has 0 for every empty cell.  The *solution* is the
    fully-filled grid.
    """
    if solved_grid is None:
        solved_grid = generate_solved_grid()

    target_clues = CLUE_COUNTS[difficulty]
    cells_to_remove = 81 - target_clues

    puzzle = [row.copy() for row in solved_grid]
    positions = _shuffled([(r, c) for r in range(9) for c in range(9)])

    removed = 0
    for r, c in positions:
        if removed >= cells_to_remove:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if _has_unique_solution(puzzle):
            removed += 1
        else:
            puzzle[r][c] = backup

    return puzzle, solved_grid


def format_grid(grid: Grid) -> str:
    """Pretty-print a sudoku grid with box separators and dots for empties."""
    lines: list[str] = []
    for r in range(9):
        row_parts: list[str] = []
        for c in range(9):
            val = grid[r][c]
            row_parts.append(str(val) if val else ".")
            if c in (2, 5):
                row_parts.append("|")
        lines.append(" ".join(row_parts))
        if r in (2, 5):
            lines.append("------+-------+------")
    return "\n".join(lines)
