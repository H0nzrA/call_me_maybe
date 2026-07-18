from pydantic import BaseModel, ConfigDict, PrivateAttr

from ..utils import FileManagement
from .constrained import Constrained
from ..utils import Parsing, ParsedData, PathData, Result
from ..cli import Display
import time
import json


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    io_path: PathData
    __display: Display = PrivateAttr(default_factory=Display)

    def generate(self) -> None:
        self.__display.introduction()

        parsed_data: ParsedData = self.__get_data()
        gen: Constrained = Constrained(
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
                pass

        self.__display.full_stats(total, fail)

        self.__validate_output_json()

    def __get_data(self) -> ParsedData:
        pars: Parsing = Parsing(
            path_data=self.io_path
        )
        return pars.get_file_content()

    def __validate_output_json(self) -> None:
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
