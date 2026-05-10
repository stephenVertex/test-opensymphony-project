import typer

app = typer.Typer(help="test-opsyn CLI")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, hello_world: bool = typer.Option(False, "--hello-world", help="Print hello-world in English and Hebrew")) -> None:
    if hello_world:
        typer.echo("Hello, World!")
        typer.echo("שלום, עולם!")
    else:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()