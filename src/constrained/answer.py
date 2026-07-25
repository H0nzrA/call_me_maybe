"""
Application orchestration.

Coordinated data loading, constrained generation, result
serealization and output validation.
"""

from pydantic import BaseModel, ConfigDict, PrivateAttr
from ..utils import FileManagement
from .constrained import Constrained
from ..utils import Parsing, ParsedData, PathData, Result
from ..cli import Display
import time
import json
import sys


class Answer(BaseModel):
    """
    Exectute the complete function calling pipeline.

    Loads the input data, initialize the constrained generator,
    processes each prompt one by one, write the generated results,
    and validate the output file.
    """

    model_config = ConfigDict(extra="forbid")

    io_path: PathData
    __display: Display = PrivateAttr(default_factory=Display)

    def generate(self) -> None:
        """Run the complete function calling pipeline."""
        self.__display.introduction()
        model_name: str = self.__display.menu(
            "Small LLM Model to use",
            [
                "Qwen/Qwen3-0.6B",
                "HuggingFaceTB/SmolLM2-360M-Instruct"
            ]
        )

        parsed_data: ParsedData = self.__get_data()
        self.__evaluate_data(parsed_data)

        gen: Constrained = Constrained(
            model_name=model_name,
            definitions=parsed_data.definitions
        )

        total: int = len(parsed_data.callings)
        fail: list[str] = []

        FileManagement.clear_file(self.io_path.result)
        print("\n")
        for i, c in enumerate(parsed_data.callings):
            try:
                self.__display.start_process(c.prompt, i, total, len(fail))

                start: float = time.perf_counter()
                result: Result = gen.generate(c)
                end: float = time.perf_counter()

                FileManagement.write_json(
                    path=self.io_path.result,
                    data=result
                )
                self.__display.end_process(result.model_dump(), end - start)

            except Exception as e:
                self.__display.problem(c.prompt, str(e))
                fail.append(c.prompt)

        self.__display.full_stats(total, fail)

        self.__validate_output_json()

    def __get_data(self) -> ParsedData:
        """
        Load and parse the input files.

        Return:
            The parsed function definition and calling requests.
        """
        pars: Parsing = Parsing(
            path_data=self.io_path
        )
        return pars.get_file_content()

    def __validate_output_json(self) -> None:
        """
        Validate that the generated output file contains valid JSON.

        Display an appropriate message is the file is missing or
        contains invalid JSON.
        """
        try:
            with self.io_path.result.open("r") as f:
                _ = json.load(f)

        except FileNotFoundError as e:
            self.__display.invalid_print(f"Output File not Generated: {e}")
            return

        except json.JSONDecodeError:
            self.__display.invalid_print("Invalid JSON Format Generated!!!!")
            return

        except Exception as e:
            self.__display.invalid_print(f"Unknown Error: {e}")
            return

        self.__display.valid_print("Output valid JSON confirm")

    def __evaluate_data(self, data: ParsedData) -> None:
        """
        Validate the parse input data before generation.

        Args:
            data (ParsedData): Parse input data, definition and calling.

        Raises:
            SystemExit: If the function definition or calling requests
            are empty.
        """
        valid: bool = True
        if not data.definitions:
            self.__display.invalid_print(
                "Function Definition Empty. Can't continue the process!"
            )
            valid = False
        if not data.callings:
            self.__display.invalid_print(
                "Function Calling Empty. Can't continue the process!"
            )
            valid = False

        if not valid:
            sys.exit(1)
