from pydantic import BaseModel, ConfigDict
from typing import Any


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
