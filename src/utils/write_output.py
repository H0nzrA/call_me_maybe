import json
from pathlib import Path
from typing import Any
from .models import Result


class OutputError(Exception):
    pass


class Output:
    @classmethod
    def write_json(cls, path: Path, data: list[Result]) -> None:
        try:
            data_cast: list[dict[str, Any]] = Output.transform_result(data)

            with path.open("w") as f:
                json.dump(data_cast, f, indent=4)

        except Exception as e:
            raise OutputError(f"Cannot write json output: {e}")

    @classmethod
    def transform_result(cls, data: list[Result]) -> list[dict[str, Any]]:
        data_cast: list[dict[str, Any]] = []

        for d in data:
            tmp: dict[str, Any] = {
                "prompt": d.prompt,
                "name": d.name,
                "parameters": d.parameters
            }
            data_cast.append(tmp)

        return data_cast
