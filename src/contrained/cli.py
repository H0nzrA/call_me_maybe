import sys
from collections.abc import Iterator
from enum import Enum

from pydantic import BaseModel


class CLIError(Exception):
    pass


class IOFile(BaseModel):
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


class CLI:
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
                raise CLIError(f"Unknown flag {arg}")

            try:
                value: str = next(it)
                if value in self.__flags_map:
                    raise CLIError(
                        "Having another flag "
                        f"{value!r} not argument"
                    )

                field: IOFlags = self.__flags_map[arg]
                setattr(self.io_file, field.name, value)

            except StopIteration:
                raise CLIError(f"No value given for flag {arg!r}")
        print(self.io_file)

    def get_io_file(self) -> IOFile:
        return self.io_file
