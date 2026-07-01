from pydantic import BaseModel, ConfigDict, PrivateAttr
from pathlib import Path
from .model_json import Definition, Calling, ParsedData
import json
from typing import Any


class Parsing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definition: Path
    calling: Path
    result: Path

    _content_definition: list[Definition] = PrivateAttr(default_factory=list)
    _content_calling: list[Calling] = PrivateAttr(default_factory=list)

    def __parsing(self) -> None:
        data: list[dict[str, Any]] = []

        # Parsing Definition
        with self.definition.open("r") as f:
            data = json.load(f)
        for d in data:
            self._content_definition.append(Definition(**d))

        # Parsing Calling Test
        with self.calling.open("r") as f:
            data = json.load(f)
        for d in data:
            self._content_calling.append(Calling(**d))

        # Make sure Parent output dir is created
        path = self.result.parent
        path.mkdir(parents=True, exist_ok=True)

    def get_file_content(self) -> ParsedData:
        self.__parsing()

        return ParsedData(
            definitions=self._content_definition,
            callings=self._content_calling
        )
