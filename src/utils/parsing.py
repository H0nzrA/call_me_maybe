from pydantic import BaseModel, ConfigDict, PrivateAttr
from .models import Definition, Calling, ParsedData, PathData
from typing import Any
from .file_management import FileManagement


class Parsing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path_data: PathData

    _content_definition: list[Definition] = PrivateAttr(default_factory=list)
    _content_calling: list[Calling] = PrivateAttr(default_factory=list)

    def __parsing(self) -> None:
        data: list[dict[str, Any]] = []

        # Parsing Definition
        data = FileManagement.read_json(self.path_data.definition)
        for d in data:
            self._content_definition.append(Definition(**d))

        # Parsing Calling Test
        data = FileManagement.read_json(self.path_data.calling)
        for d in data:
            self._content_calling.append(Calling(**d))

        # Make sure Parent output dir is created
        path = self.path_data.result.parent
        path.mkdir(parents=True, exist_ok=True)

    def get_file_content(self) -> ParsedData:
        self.__parsing()

        return ParsedData(
            definitions=self._content_definition,
            callings=self._content_calling
        )
