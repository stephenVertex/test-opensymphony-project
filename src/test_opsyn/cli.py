import typer

from test_opsyn.password import PasswordOptions, generate_password

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
def password(
    length: int = typer.Option(16, "--length", "-l", help="Password length"),
    upper: bool = typer.Option(
        True, "--upper/--no-upper", help="Include uppercase letters"
    ),
    lower: bool = typer.Option(
        True, "--lower/--no-lower", help="Include lowercase letters"
    ),
    digits: bool = typer.Option(True, "--digits/--no-digits", help="Include digits"),
    symbols: bool = typer.Option(
        True, "--symbols/--no-symbols", help="Include symbols"
    ),
    exclude_ambiguous: bool = typer.Option(
        False, "--exclude-ambiguous", help="Exclude ambiguous characters (0O1lI)"
    ),
) -> None:
    """Generate a secure random password."""
    opts = PasswordOptions(
        length=length,
        upper=upper,
        lower=lower,
        digits=digits,
        symbols=symbols,
        exclude_ambiguous=exclude_ambiguous,
    )
    typer.echo(generate_password(opts))


if __name__ == "__main__":
    app()
