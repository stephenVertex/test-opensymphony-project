import pytest
from typer.testing import CliRunner

from test_opsyn.calculator import add, divide, multiply, subtract
from test_opsyn.cli import app

runner = CliRunner()


# --- Unit tests for core arithmetic ---


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -2) == -3

    def test_mixed_signs(self):
        assert add(-5, 10) == 5

    def test_zero(self):
        assert add(0, 0) == 0

    def test_floats(self):
        assert add(1.5, 2.5) == 4.0


class TestSubtract:
    def test_positive_numbers(self):
        assert subtract(10, 3) == 7

    def test_negative_result(self):
        assert subtract(3, 10) == -7

    def test_negative_numbers(self):
        assert subtract(-5, -3) == -2

    def test_zero(self):
        assert subtract(5, 0) == 5

    def test_floats(self):
        assert subtract(5.5, 2.5) == 3.0


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(3, 4) == 12

    def test_negative_numbers(self):
        assert multiply(-2, -3) == 6

    def test_mixed_signs(self):
        assert multiply(-2, 3) == -6

    def test_zero(self):
        assert multiply(5, 0) == 0

    def test_floats(self):
        assert multiply(2.5, 4) == 10.0


class TestDivide:
    def test_positive_numbers(self):
        assert divide(10, 2) == 5.0

    def test_negative_result(self):
        assert divide(-10, 2) == -5.0

    def test_float_result(self):
        assert divide(7, 2) == 3.5

    def test_division_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_zero_numerator(self):
        assert divide(0, 5) == 0.0


# --- CLI integration tests ---


class TestCalculateCommand:
    def test_add(self):
        result = runner.invoke(app, ["calculate", "add", "2", "3"])
        assert result.exit_code == 0
        assert "5" in result.output

    def test_subtract(self):
        result = runner.invoke(app, ["calculate", "subtract", "10", "4"])
        assert result.exit_code == 0
        assert "6" in result.output

    def test_multiply(self):
        result = runner.invoke(app, ["calculate", "multiply", "3", "7"])
        assert result.exit_code == 0
        assert "21" in result.output

    def test_divide(self):
        result = runner.invoke(app, ["calculate", "divide", "10", "2"])
        assert result.exit_code == 0
        assert "5" in result.output

    def test_divide_by_zero(self):
        result = runner.invoke(app, ["calculate", "divide", "5", "0"])
        assert result.exit_code == 1
        assert "Cannot divide by zero" in result.output

    def test_unknown_operation(self):
        result = runner.invoke(app, ["calculate", "modulo", "5", "3"])
        assert result.exit_code == 1
        assert "Unknown operation" in result.output

    def test_float_operands(self):
        result = runner.invoke(app, ["calculate", "add", "1.5", "2.5"])
        assert result.exit_code == 0
        assert "4" in result.output

    def test_negative_operands(self):
        result = runner.invoke(app, ["calculate", "add", "--", "-3", "7"])
        assert result.exit_code == 0
        assert "4" in result.output
