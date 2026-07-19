from enum import Enum
from typing import Any
import json


class TypeEval(Enum):
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
    return (
        res in (
            *TypeEval.NUMBER.value,
            *TypeEval.INTEGER.value
        )
    )


def is_boolean(res: str) -> bool:
    return (
        res in TypeEval.BOOLEAN.value
    )


def separator_literal(last: bool) -> str:
    return "}" if last else ","


def cast_value(value: str, ptype: str) -> Any:
    if is_numeric(ptype):
        return (
            int(value) if ptype in TypeEval.INTEGER.value
            else float(value)
        )

    if is_boolean(ptype):
        return value == "true"

    return json.loads(f"{value}")
