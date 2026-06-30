from pydantic import BaseModel, ConfigDict
from pathlib import Path


class Parsing(BaseModel):
    ConfigDict(extra="forbid")

    definition: Path
    calling: Path
    result: Path
