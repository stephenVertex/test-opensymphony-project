from test_opsyn.tips import TIPS, get_tip


def test_get_tip_returns_non_empty_string():
    tip = get_tip()
    assert isinstance(tip, str)
    assert len(tip) > 0


def test_get_tip_returns_from_known_list():
    tip = get_tip()
    assert tip in TIPS


def test_get_tip_with_index():
    assert get_tip(index=0) == TIPS[0]
    assert get_tip(index=1) == TIPS[1]


def test_get_tip_index_wraps():
    assert get_tip(index=len(TIPS)) == TIPS[0]


def test_tips_list_not_empty():
    assert len(TIPS) > 0


def test_tip_cli_command(cli_runner):
    from test_opsyn.cli import app

    result = cli_runner.invoke(app, ["tip"])
    assert result.exit_code == 0
    assert "Tip of the Day:" in result.output
