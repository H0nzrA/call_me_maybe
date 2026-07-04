import json
from pathlib import Path
from typing import Any
from .models import Result


class FileManagementError(Exception):
    pass


class FileManagement:
    @classmethod
    def clear_file(cls, path: Path) -> None:
        path.unlink(missing_ok=True)

    @classmethod
    def read_json(cls, path: Path) -> list[dict[str, Any]]:
        res: list[dict[str, Any]] = []

        try:
            with path.open("r") as f:
                res = json.load(f)
        except Exception:
            return []

        return res

    @classmethod
    def write_json(cls, path: Path, data: Result) -> None:
        full_content: list[dict[str, Any]] = FileManagement.read_json(path)

        try:
            data_cast: dict[str, Any] = FileManagement.transform_result(data)
            full_content.append(data_cast)

            with path.open("w") as f:
                json.dump(full_content, f, indent=4)

        except Exception as e:
            raise FileManagementError(f"Cannot write json output: {e}")

    @classmethod
    def write_full_json(cls, path: Path, data: list[Result]) -> None:
        try:
            data_cast: list[dict[str, Any]] = []
            for d in data:
                d_cast: dict[str, Any] = FileManagement.transform_result(d)
                data_cast.append(d_cast)

            with path.open("w") as f:
                json.dump(data_cast, f, indent=4)

        except Exception as e:
            raise FileManagementError(f"Cannot write json output: {e}")

    @classmethod
    def transform_result(cls, data: Result) -> dict[str, Any]:
        data_cast: dict[str, Any] = {
            "prompt": data.prompt,
            "name": data.name,
            "parameters": data.parameters
        }

        return data_cast
