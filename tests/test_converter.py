"""Tests for the unit converter module."""

from __future__ import annotations

import pytest

from test_opsyn.converter import (
    convert_length,
    convert_temperature,
    convert_weight,
)


# ── Temperature ────────────────────────────────────────────────────────


class TestTemperatureConversions:
    def test_celsius_to_fahrenheit(self) -> None:
        assert convert_temperature(100, "C", "F") == pytest.approx(212.0)

    def test_fahrenheit_to_celsius(self) -> None:
        assert convert_temperature(32, "F", "C") == pytest.approx(0.0)

    def test_celsius_to_kelvin(self) -> None:
        assert convert_temperature(0, "C", "K") == pytest.approx(273.15)

    def test_kelvin_to_celsius(self) -> None:
        assert convert_temperature(273.15, "K", "C") == pytest.approx(0.0)

    def test_fahrenheit_to_kelvin(self) -> None:
        assert convert_temperature(-459.67, "F", "K") == pytest.approx(0.0, abs=0.01)

    def test_kelvin_to_fahrenheit(self) -> None:
        assert convert_temperature(0, "K", "F") == pytest.approx(-459.67, abs=0.01)

    def test_celsius_identity(self) -> None:
        assert convert_temperature(42, "C", "C") == pytest.approx(42.0)

    def test_fahrenheit_identity(self) -> None:
        assert convert_temperature(98.6, "F", "F") == pytest.approx(98.6)

    def test_kelvin_identity(self) -> None:
        assert convert_temperature(300, "K", "K") == pytest.approx(300.0)

    def test_negative_celsius_to_fahrenheit(self) -> None:
        assert convert_temperature(-40, "C", "F") == pytest.approx(-40.0)

    def test_case_insensitive(self) -> None:
        assert convert_temperature(100, "c", "f") == pytest.approx(212.0)

    def test_unknown_unit_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported temperature unit"):
            convert_temperature(100, "C", "X")


# ── Length ──────────────────────────────────────────────────────────────


class TestLengthConversions:
    def test_meters_to_feet(self) -> None:
        assert convert_length(1, "m", "ft") == pytest.approx(3.28084, rel=1e-4)

    def test_feet_to_meters(self) -> None:
        assert convert_length(1, "ft", "m") == pytest.approx(0.3048, rel=1e-4)

    def test_meters_to_inches(self) -> None:
        assert convert_length(1, "m", "in") == pytest.approx(39.3701, rel=1e-4)

    def test_inches_to_meters(self) -> None:
        assert convert_length(1, "in", "m") == pytest.approx(0.0254, rel=1e-4)

    def test_meters_to_centimeters(self) -> None:
        assert convert_length(1, "m", "cm") == pytest.approx(100.0)

    def test_centimeters_to_meters(self) -> None:
        assert convert_length(100, "cm", "m") == pytest.approx(1.0)

    def test_feet_to_inches(self) -> None:
        assert convert_length(1, "ft", "in") == pytest.approx(12.0, rel=1e-4)

    def test_inches_to_centimeters(self) -> None:
        assert convert_length(1, "in", "cm") == pytest.approx(2.54, rel=1e-4)

    def test_centimeters_to_feet(self) -> None:
        assert convert_length(30.48, "cm", "ft") == pytest.approx(1.0, rel=1e-4)

    def test_identity(self) -> None:
        assert convert_length(5, "m", "m") == pytest.approx(5.0)

    def test_case_insensitive(self) -> None:
        assert convert_length(1, "M", "FT") == pytest.approx(3.28084, rel=1e-4)

    def test_unknown_unit_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported unit"):
            convert_length(1, "m", "mi")


# ── Weight ──────────────────────────────────────────────────────────────


class TestWeightConversions:
    def test_kg_to_lb(self) -> None:
        assert convert_weight(1, "kg", "lb") == pytest.approx(2.20462, rel=1e-4)

    def test_lb_to_kg(self) -> None:
        assert convert_weight(1, "lb", "kg") == pytest.approx(0.453592, rel=1e-4)

    def test_kg_to_oz(self) -> None:
        assert convert_weight(1, "kg", "oz") == pytest.approx(35.274, rel=1e-3)

    def test_oz_to_kg(self) -> None:
        assert convert_weight(1, "oz", "kg") == pytest.approx(0.0283495, rel=1e-4)

    def test_kg_to_g(self) -> None:
        assert convert_weight(1, "kg", "g") == pytest.approx(1000.0)

    def test_g_to_kg(self) -> None:
        assert convert_weight(1000, "g", "kg") == pytest.approx(1.0)

    def test_lb_to_oz(self) -> None:
        assert convert_weight(1, "lb", "oz") == pytest.approx(16.0, rel=1e-3)

    def test_oz_to_g(self) -> None:
        assert convert_weight(1, "oz", "g") == pytest.approx(28.3495, rel=1e-3)

    def test_g_to_lb(self) -> None:
        assert convert_weight(453.592, "g", "lb") == pytest.approx(1.0, rel=1e-3)

    def test_identity(self) -> None:
        assert convert_weight(5, "kg", "kg") == pytest.approx(5.0)

    def test_case_insensitive(self) -> None:
        assert convert_weight(1, "KG", "LB") == pytest.approx(2.20462, rel=1e-4)

    def test_unknown_unit_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported unit"):
            convert_weight(1, "kg", "ton")
