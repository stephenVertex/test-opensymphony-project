from typer.testing import CliRunner

from test_opsyn.cli import app
from test_opsyn.fortunes import FORTUNES, get_random_fortune

runner = CliRunner()


def test_fortunes_list_not_empty():
    assert len(FORTUNES) >= 10


def test_get_random_fortune_returns_known_quote():
    result = get_random_fortune()
    assert result in FORTUNES


def test_all_fortunes_are_strings():
    for fortune in FORTUNES:
        assert isinstance(fortune, str)
        assert len(fortune) > 0


def test_fortunes_are_unique():
    assert len(FORTUNES) == len(set(FORTUNES))


def test_cli_fortune_option():
    result = runner.invoke(app, ["--fortune"])
    assert result.exit_code == 0
    assert result.output.strip() in FORTUNES


def test_cli_fortune_in_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--fortune" in result.output
