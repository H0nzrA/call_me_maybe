"""
Application data models.

Defines the pydantic models used to represent function definitions,
prompts, generated results, and application paths.
"""

from pydantic import BaseModel, ConfigDict
from typing import Any
from pathlib import Path


class Type(BaseModel):
    """Represents the type of a function parameters or return value."""

    model_config = ConfigDict(extra="forbid")

    type: str


class Calling(BaseModel):
    """Represents a user prompt requiring function calling."""

    model_config = ConfigDict(extra="forbid")

    prompt: str


class Definition(BaseModel):
    """
    Represents the definition of an avaliable function.

    Store the function name, description, parameter specifications
    and return type
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    parameters: dict[str, Type]
    returns: Type
    description: str


class Result(BaseModel):
    """
    Represents a generated function call.

    Store the original prompt, the selected function name
    and the extracted parameter values.
    """

    model_config = ConfigDict(extra="forbid")

    prompt: str
    name: str
    parameters: dict[str, Any]


class ParsedData(BaseModel):
    """
    Container for parsed input data.

    Groups the function definitions and function-calling prompts
    loaded from the input files.
    """

    model_config = ConfigDict(extra="forbid")

    definitions: list[Definition]
    callings: list[Calling]


class PathData(BaseModel):
    """Store the application's input and output files."""

    model_config = ConfigDict(extra="forbid")

    definition: Path
    calling: Path
    result: Path
