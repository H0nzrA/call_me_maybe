"""
Input parsing utilities.

Loads and validates the application's input files
into stucture Pydantic models.
"""

from pydantic import BaseModel, ConfigDict, PrivateAttr
from .models import Definition, Calling, ParsedData, PathData
from typing import Any
from .file_management import read_json


class Parsing(BaseModel):
    """
    Parse the application input files.

    Loads the function definition and function-calling prompts
    from the configured input files.
    """

    model_config = ConfigDict(extra="forbid")

    path_data: PathData

    _content_definition: list[Definition] = PrivateAttr(default_factory=list)
    _content_calling: list[Calling] = PrivateAttr(default_factory=list)

    def __parsing(self) -> None:
        """
        Load and validate the application's input files.

        Reads the fucntion definition and function calling prompts,
        converts them into Pydantic models, and ensure that the output
        directory exists.
        """
        data: list[dict[str, Any]] = []

        # Parsing Definition
        data = read_json(self.path_data.definition)
        for d in data:
            self._content_definition.append(Definition(**d))

        # Parsing Calling Test
        data = read_json(self.path_data.calling)
        for d in data:
            self._content_calling.append(Calling(**d))

        # Make sure Parent output dir is created
        path = self.path_data.result.parent
        path.mkdir(parents=True, exist_ok=True)

    def get_file_content(self) -> ParsedData:
        """
        Parse the congigure input files.

        Returns:
            The parse function definitions and calling prompts.
        """
        self.__parsing()

        return ParsedData(
            definitions=self._content_definition,
            callings=self._content_calling
        )
