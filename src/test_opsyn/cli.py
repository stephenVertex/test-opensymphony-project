import typer

from test_opsyn.converter import convert_length, convert_temperature, convert_weight

app = typer.Typer(help="test-opsyn CLI")
convert_app = typer.Typer(help="Unit conversion commands")
app.add_typer(convert_app, name="convert")


@convert_app.command("temperature")
def convert_temperature_cmd(
    value: float = typer.Argument(help="Value to convert"),
    from_unit: str = typer.Argument(help="Source unit (C, F, K)"),
    to_unit: str = typer.Argument(help="Target unit (C, F, K)"),
) -> None:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    result = convert_temperature(value, from_unit, to_unit)
    typer.echo(f"{value} {from_unit.upper()} = {result:.2f} {to_unit.upper()}")


@convert_app.command("length")
def convert_length_cmd(
    value: float = typer.Argument(help="Value to convert"),
    from_unit: str = typer.Argument(help="Source unit (m, cm, ft, in)"),
    to_unit: str = typer.Argument(help="Target unit (m, cm, ft, in)"),
) -> None:
    """Convert length between meters, centimeters, feet, and inches."""
    result = convert_length(value, from_unit, to_unit)
    typer.echo(f"{value} {from_unit.lower()} = {result:.2f} {to_unit.lower()}")


@convert_app.command("weight")
def convert_weight_cmd(
    value: float = typer.Argument(help="Value to convert"),
    from_unit: str = typer.Argument(help="Source unit (kg, g, lb, oz)"),
    to_unit: str = typer.Argument(help="Target unit (kg, g, lb, oz)"),
) -> None:
    """Convert weight between kilograms, grams, pounds, and ounces."""
    result = convert_weight(value, from_unit, to_unit)
    typer.echo(f"{value} {from_unit.lower()} = {result:.2f} {to_unit.lower()}")


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
    else:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
