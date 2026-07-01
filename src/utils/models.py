from pydantic import BaseModel, ConfigDict
from typing import Any
from pathlib import Path


class Type(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str


class Calling(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str


class Definition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    parameters: dict[str, Type]
    returns: Type
    description: str


class Result(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str
    name: str
    parameters: dict[str, Any]


class ParsedData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definitions: list[Definition]
    callings: list[Calling]


class PathData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definition: Path
    calling: Path
    result: Path
