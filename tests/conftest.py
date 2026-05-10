import pytest
import typer.testing


@pytest.fixture
def cli_runner():
    return typer.testing.CliRunner()
