from pydantic import BaseModel, ConfigDict
from typing import Any


class Type(BaseModel):
    ConfigDict(extra="forbid")

    type: str


class Calling(BaseModel):
    ConfigDict(extra="forbid")

    prompt:str


class Definition(BaseModel):
    ConfigDict(extra="forbid")

    name: str
    parameters: dict[str, Type]
    returns: Type
    description: str


class Result(BaseModel):
    ConfigDict(extra="forbid")

    prompt: str
    name: str
    parameters: dict[str, Any]
