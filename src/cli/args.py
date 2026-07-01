import sys
from collections.abc import Iterator
from enum import Enum
from pydantic import BaseModel, ConfigDict
from pathlib import Path
from ..utils import PathData


class ArgsError(Exception):
    pass


class IOFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definition: str
    calling: str
    result: str


class IOFlags(Enum):
    definition = [
        "--functions_definition",
        "-d"
    ]
    calling = [
        "--input",
        "-i"
    ]
    result = [
        "--output",
        "-o"
    ]


class Argument:
    def __init__(self) -> None:
        self.io_file: IOFile = IOFile(
            definition="data/input/functions_definition.json",
            calling="data/input/function_calling_tests.json",
            result="data/output/function_calling_results.json"
        )

        self.__flags_map: dict[str, IOFlags] = {
            flag: member
            for member in IOFlags
            for flag in member.value
        }

        self.__parse_arguments()

    def __parse_arguments(self) -> None:
        args: list[str] = sys.argv[1::]
        it: Iterator[str] = iter(args)

        for arg in it:
            if arg not in self.__flags_map:
                raise ArgsError(f"Unknown flag {arg}")

            try:
                value: str = next(it)
                if value in self.__flags_map:
                    raise ArgsError(
                        "Having another flag "
                        f"{value!r} not argument"
                    )

                field: IOFlags = self.__flags_map[arg]
                setattr(self.io_file, field.name, value)

            except StopIteration:
                raise ArgsError(f"No value given for flag {arg!r}")

    def get_io_file(self) -> PathData:
        return PathData(
            definition=Path(self.io_file.definition),
            calling=Path(self.io_file.calling),
            result=Path(self.io_file.result)
        )
