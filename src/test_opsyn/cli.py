import typer

from test_opsyn.sudoku import Difficulty, format_grid, generate_puzzle

app = typer.Typer(help="test-opsyn CLI")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    hello_world: bool = typer.Option(
        False, "--hello-world", help="Print hello-world in English and Hebrew"
    ),
) -> None:
    if ctx.invoked_subcommand is not None:
        return
    if hello_world:
        typer.echo("Hello, World!")
        typer.echo("שלום, עולם!")
    else:
        typer.echo(ctx.get_help())


@app.command()
def sudoku(
    difficulty: Difficulty = typer.Option(
        Difficulty.medium, "--difficulty", "-d", help="Puzzle difficulty level"
    ),
    show_solution: bool = typer.Option(
        False, "--show-solution", "-s", help="Also print the solution"
    ),
    seed: int = typer.Option(0, "--seed", help="Random seed (0 = no seed)"),
) -> None:
    """Generate a sudoku puzzle."""
    if seed:
        import random as _random

        _random.seed(seed)

    puzzle, solution = generate_puzzle(difficulty)
    typer.echo(format_grid(puzzle))
    if show_solution:
        typer.echo()
        typer.echo("Solution:")
        typer.echo(format_grid(solution))


if __name__ == "__main__":
    app()
