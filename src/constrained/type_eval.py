"""
Parameter type utilities.

Provides helper function for identifying parameter type,
casting generated values, and formatting JSON separators.
"""

from enum import Enum
from typing import Any
import json


class TypeEval(Enum):
    """
    Supported parameter type aliases.

    Groups equivalent type name used during constrained parameter
    generation.
    """

    NUMBER = (
        "numbers",
        "number",
        "num",
        "float",
        "floats",
        "decimals",
        "decimal"
    )
    INTEGER = (
        "integers",
        "integer",
        "int"
    )

    BOOLEAN = (
        "boolean",
        "booleans",
        "bool"
    )


def is_numeric(res: str) -> bool:
    """
    Check whether a parameter type is numeric.

    Args:
        res (str): Parameter type name.

    Returns:
        True if the type represents an integer or
        a floating-point number, False otherwise.
    """
    return (
        res in (
            *TypeEval.NUMBER.value,
            *TypeEval.INTEGER.value
        )
    )


def is_boolean(res: str) -> bool:
    """
    Check whether a parameter type is boolean.

    Args:
        res (str): Parameter type name.

    Returns:
        True if the type represents a boolean,
        False otherwise.
    """
    return (
        res in TypeEval.BOOLEAN.value
    )


def separator_literal(last: bool) -> str:
    """
    Return a JSON separator following a parameter value.

    Args:
        last (bool): Whether the parameter is the last one.

    Returns:
        "}" if the parameter is the last one otherwise ",".
    """
    return "}" if last else ","


def cast_value(value: str, ptype: str) -> Any:
    """
    Convert a generated string into its corresponding Python type.

    Args:
        value (str): Generated parameter value.
        ptype (str): Expected parametr type

    Returns:
        The converted python value.
    """
    if is_numeric(ptype):
        return (
            int(value) if ptype in TypeEval.INTEGER.value
            else float(value)
        )

    if is_boolean(ptype):
        return value == "true"

    return json.loads(value)
