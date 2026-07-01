from pydantic import BaseModel, ConfigDict
from .model_json import Definition, Calling, ParsedData, Result


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    parsed_data: ParsedData

    def generate(self) -> None:
        ds = self.parsed_data.definitions
        cs = self.parsed_data.callings

        for d in ds:
            print(d)

        print()

        for c in cs:
            print(c)
