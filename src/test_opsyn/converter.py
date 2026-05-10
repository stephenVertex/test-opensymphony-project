"""Unit converter supporting temperature, length, and weight conversions."""

from __future__ import annotations

# Temperature uses formulas rather than simple factors, so we convert through
# Celsius as the pivot unit.

TEMPERATURE_TO_CELSIUS: dict[str, float | None] = {
    "C": None,  # identity
    "F": None,  # formula
    "K": None,  # formula
}


def _to_celsius(value: float, unit: str) -> float:
    if unit == "C":
        return value
    if unit == "F":
        return (value - 32) * 5 / 9
    if unit == "K":
        return value - 273.15
    raise ValueError(f"Unknown temperature unit: {unit!r}")


def _from_celsius(value: float, unit: str) -> float:
    if unit == "C":
        return value
    if unit == "F":
        return value * 9 / 5 + 32
    if unit == "K":
        return value + 273.15
    raise ValueError(f"Unknown temperature unit: {unit!r}")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a temperature value between C, F, and K."""
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    if from_unit not in TEMPERATURE_TO_CELSIUS or to_unit not in TEMPERATURE_TO_CELSIUS:
        raise ValueError(
            f"Unsupported temperature unit(s): {from_unit!r}, {to_unit!r}. "
            f"Supported: C, F, K"
        )
    celsius = _to_celsius(value, from_unit)
    return _from_celsius(celsius, to_unit)


# Length and weight use multiplicative factors relative to a base unit.

LENGTH_FACTORS: dict[str, float] = {
    "m": 1.0,
    "cm": 0.01,
    "ft": 0.3048,
    "in": 0.0254,
}

WEIGHT_FACTORS: dict[str, float] = {
    "kg": 1.0,
    "g": 0.001,
    "lb": 0.453592,
    "oz": 0.0283495,
}


def _convert_factor(
    value: float, from_unit: str, to_unit: str, factors: dict[str, float]
) -> float:
    """Convert *value* from *from_unit* to *to_unit* using multiplicative factors."""
    if from_unit not in factors:
        raise ValueError(
            f"Unsupported unit: {from_unit!r}. Supported: {', '.join(factors)}"
        )
    if to_unit not in factors:
        raise ValueError(
            f"Unsupported unit: {to_unit!r}. Supported: {', '.join(factors)}"
        )
    base = value * factors[from_unit]
    return base / factors[to_unit]


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a length value between m, cm, ft, and in."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    return _convert_factor(value, from_unit, to_unit, LENGTH_FACTORS)


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a weight value between kg, g, lb, and oz."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    return _convert_factor(value, from_unit, to_unit, WEIGHT_FACTORS)
