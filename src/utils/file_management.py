"""
JSON file management utilities.

Provides helper function for reading, writing, and clearing JSON file
used by the application.
"""

import json
from pathlib import Path
from typing import Any
from .models import Result


class FileManagementError(Exception):
    """Raised when JSON file operation fails."""

    pass


def clear_file(path: Path) -> None:
    """
    Delete a file if it exists.

    Args:
        path (Path): Path to the file.
    """
    path.unlink(missing_ok=True)


def read_json(path: Path) -> list[dict[str, Any]]:
    """
    Read the contents of a JSON file.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        The parsed JSON content.
    """
    res: list[dict[str, Any]] = []
    with path.open("r") as f:
        res = json.load(f)

    return res


def write_json(path: Path, data: Result) -> None:
    """
    Append a result to a JSON output file.

    Create the file if it does not exist.

    Args:
        path (Path): Path to the JSON file.
        data (Result): Result to write.

    Raises:
        FileManagementError: If the output file cannot be written.
    """
    full_content: list[dict[str, Any]] = []
    try:
        full_content = read_json(path)
    except FileNotFoundError:
        full_content = []

    try:
        data_cast: dict[str, Any] = transform_result(data)
        full_content.append(data_cast)

        with path.open("w") as f:
            json.dump(full_content, f, indent=4)

    except Exception as e:
        raise FileManagementError(f"Cannot write json output: {e}")


def write_full_json(path: Path, data: list[Result]) -> None:
    """
    Write a collection of result into a JSON file.

    Args:
        path (Path): Path to the JSON file.
        data (list[Result]): Results to write.

    Raises:
        FileManagementError: If the output file cannot be written.
    """
    try:
        data_cast: list[dict[str, Any]] = []
        for d in data:
            d_cast: dict[str, Any] = transform_result(d)
            data_cast.append(d_cast)

        with path.open("w") as f:
            json.dump(data_cast, f, indent=4)

    except Exception as e:
        raise FileManagementError(f"Cannot write json output: {e}")


def transform_result(data: Result) -> dict[str, Any]:
    """
    Convert a result model into a JSON serealizable dictionary.

    Args:
        data (Result): Result to convert.

    Returns:
        A dictionary representation of the result.
    """
    data_cast: dict[str, Any] = {
        "prompt": data.prompt,
        "name": data.name,
        "parameters": data.parameters
    }

    return data_cast
