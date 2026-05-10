import typer

from test_opsyn.ascii_art import generate_ascii_art, list_fonts, DEFAULT_FONT

app = typer.Typer(help="test-opsyn CLI")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    hello_world: bool = typer.Option(
        False, "--hello-world", help="Print hello-world in English and Hebrew"
    ),
    ascii_art: str = typer.Option(
        "", "--ascii-art", help="Render TEXT as ASCII art"
    ),
    font: str = typer.Option(
        DEFAULT_FONT, "--font", help="Font for ASCII art (use --list-fonts to see options)"
    ),
    list_fonts_flag: bool = typer.Option(
        False, "--list-fonts", help="List available ASCII art fonts"
    ),
    width: int = typer.Option(
        0, "--width", help="Max line width for ASCII art (0 = unlimited)"
    ),
) -> None:
    if list_fonts_flag:
        for f in list_fonts():
            typer.echo(f)
        return
    if ascii_art:
        art_text = generate_ascii_art(ascii_art, font=font, width=width or None)
        typer.echo(art_text)
        return
    if hello_world:
        typer.echo("Hello, World!")
        typer.echo("שלום, עולם!")
    else:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
