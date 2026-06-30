from pydantic import BaseModel, ConfigDict, PrivateAttr
from pathlib import Path
from .model_json import Definition, Calling
import json
from typing import Any


class Parsing(BaseModel):
    ConfigDict(extra="forbid")

    definition: Path
    calling: Path

    _content_definition: list[Definition] = PrivateAttr(default_factory=list)
    _content_calling: list[Calling] = PrivateAttr(default_factory=list)


    def __parsing(self) -> None:
        data: dict[str, Any] = {}

        with self.definition.open("r") as f:
            data = json.load(f)

        for d in data:
            self._content_definition.append(Definition(**d))

        with self.calling.open("r") as f:
            data = json.load(f)

        for d in data:
            self._content_calling.append(Calling(**d))

    def get_file_content(self) -> dict[
        str,
        list[Any]
    ]:
        self.__parsing()

        return {
            "definition": self._content_definition,
            "calling": self._content_calling
        }
