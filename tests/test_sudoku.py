"""Tests for the sudoku puzzle generator."""

from __future__ import annotations

import random

from test_opsyn.sudoku import (
    CLUE_COUNTS,
    Difficulty,
    _fill_grid,
    _has_unique_solution,
    _is_valid_placement,
    format_grid,
    generate_puzzle,
    generate_solved_grid,
)


def _count_in_row(grid: list[list[int]], row: int, num: int) -> int:
    return sum(1 for c in range(9) if grid[row][c] == num)


def _count_in_col(grid: list[list[int]], col: int, num: int) -> int:
    return sum(1 for r in range(9) if grid[r][col] == num)


def _count_in_box(grid: list[list[int]], row: int, col: int, num: int) -> int:
    br, bc = 3 * (row // 3), 3 * (col // 3)
    return sum(
        1 for r in range(br, br + 3) for c in range(bc, bc + 3) if grid[r][c] == num
    )


class TestIsValidPlacement:
    def test_valid_in_empty_grid(self) -> None:
        grid = [[0] * 9 for _ in range(9)]
        assert _is_valid_placement(grid, 0, 0, 5) is True

    def test_rejects_duplicate_in_row(self) -> None:
        grid = [[0] * 9 for _ in range(9)]
        grid[0][3] = 5
        assert _is_valid_placement(grid, 0, 8, 5) is False

    def test_rejects_duplicate_in_col(self) -> None:
        grid = [[0] * 9 for _ in range(9)]
        grid[3][0] = 5
        assert _is_valid_placement(grid, 8, 0, 5) is False

    def test_rejects_duplicate_in_box(self) -> None:
        grid = [[0] * 9 for _ in range(9)]
        grid[0][0] = 5
        assert _is_valid_placement(grid, 2, 2, 5) is False

    def test_allows_in_different_box(self) -> None:
        grid = [[0] * 9 for _ in range(9)]
        grid[0][0] = 5
        assert _is_valid_placement(grid, 3, 3, 5) is True


class TestGenerateSolvedGrid:
    def test_grid_is_fully_filled(self) -> None:
        grid = generate_solved_grid()
        for r in range(9):
            for c in range(9):
                assert 1 <= grid[r][c] <= 9

    def test_no_duplicates_in_rows(self) -> None:
        grid = generate_solved_grid()
        for r in range(9):
            assert set(grid[r]) == set(range(1, 10))

    def test_no_duplicates_in_cols(self) -> None:
        grid = generate_solved_grid()
        for c in range(9):
            col = {grid[r][c] for r in range(9)}
            assert col == set(range(1, 10))

    def test_no_duplicates_in_boxes(self) -> None:
        grid = generate_solved_grid()
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box = {grid[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)}
                assert box == set(range(1, 10))


class TestGeneratePuzzle:
    def test_puzzle_has_empties(self) -> None:
        random.seed(42)
        puzzle, solution = generate_puzzle(Difficulty.medium)
        has_zero = any(puzzle[r][c] == 0 for r in range(9) for c in range(9))
        assert has_zero

    def test_puzzle_matches_solution_where_filled(self) -> None:
        random.seed(42)
        puzzle, solution = generate_puzzle(Difficulty.medium)
        for r in range(9):
            for c in range(9):
                if puzzle[r][c] != 0:
                    assert puzzle[r][c] == solution[r][c]

    def test_puzzle_has_unique_solution(self) -> None:
        random.seed(42)
        puzzle, _ = generate_puzzle(Difficulty.medium)
        assert _has_unique_solution(puzzle)

    def test_easy_has_more_clues_than_hard(self) -> None:
        random.seed(42)
        puzzle_easy, _ = generate_puzzle(Difficulty.easy)
        random.seed(42)
        puzzle_hard, _ = generate_puzzle(Difficulty.hard)
        clues_easy = sum(
            1 for r in range(9) for c in range(9) if puzzle_easy[r][c] != 0
        )
        clues_hard = sum(
            1 for r in range(9) for c in range(9) if puzzle_hard[r][c] != 0
        )
        assert clues_easy > clues_hard

    def test_clue_counts_near_targets(self) -> None:
        for diff in Difficulty:
            random.seed(42)
            puzzle, _ = generate_puzzle(diff)
            clues = sum(1 for r in range(9) for c in range(9) if puzzle[r][c] != 0)
            target = CLUE_COUNTS[diff]
            # Allow some slack because unique-solution constraint may prevent
            # exact target from being reached.
            assert clues >= target - 5, f"{diff.value}: expected ~{target}, got {clues}"


class TestFormatGrid:
    def test_shows_dots_for_empties(self) -> None:
        grid = [[0] * 9 for _ in range(9)]
        grid[0][0] = 5
        output = format_grid(grid)
        lines = output.split("\n")
        assert lines[0].startswith("5")
        assert "." in lines[1]

    def test_has_box_separators(self) -> None:
        grid = [[0] * 9 for _ in range(9)]
        output = format_grid(grid)
        assert "------+-------+------" in output


class TestFillGrid:
    def test_fill_grid_produces_valid_grid(self) -> None:
        grid: list[list[int]] = [[0] * 9 for _ in range(9)]
        result = _fill_grid(grid)
        assert result is True
        for r in range(9):
            assert set(grid[r]) == set(range(1, 10))
