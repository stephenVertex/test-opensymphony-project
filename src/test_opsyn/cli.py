import typer

from test_opsyn.calculator import add, divide, multiply, subtract

app = typer.Typer(help="test-opsyn CLI")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    hello_world: bool = typer.Option(
        False, "--hello-world", help="Print hello-world in English and Hebrew"
    ),
) -> None:
    if hello_world:
        typer.echo("Hello, World!")
        typer.echo("שלום, עולם!")
    elif ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


@app.command()
def calculate(
    operation: str = typer.Argument(help="Operation: add, subtract, multiply, divide"),
    a: float = typer.Argument(help="First operand"),
    b: float = typer.Argument(help="Second operand"),
) -> None:
    """Perform a basic arithmetic calculation."""
    ops = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }
    if operation not in ops:
        typer.echo(
            f"Unknown operation: {operation}. Choose from: add, subtract, multiply, divide"
        )
        raise typer.Exit(code=1)
    try:
        result = ops[operation](a, b)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(result)


if __name__ == "__main__":
    app()
