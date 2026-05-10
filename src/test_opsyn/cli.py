import typer

from test_opsyn.fortunes import get_random_fortune

app = typer.Typer(help="test-opsyn CLI")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    hello_world: bool = typer.Option(
        False, "--hello-world", help="Print hello-world in English and Hebrew"
    ),
    fortune: bool = typer.Option(
        False, "--fortune", help="Print a random fortune cookie quote"
    ),
) -> None:
    if fortune:
        typer.echo(get_random_fortune())
    elif hello_world:
        typer.echo("Hello, World!")
        typer.echo("שלום, עולם!")
    else:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
