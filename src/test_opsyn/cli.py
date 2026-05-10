import typer

from test_opsyn.tips import get_tip

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
def tip() -> None:
    """Show a tip of the day."""
    typer.echo(f"💡 Tip of the Day: {get_tip()}")


if __name__ == "__main__":
    app()
