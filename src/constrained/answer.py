from pydantic import BaseModel, ConfigDict
from ..utils import FileManagement
from .constrained import Constrained
from ..utils import Parsing, ParsedData, PathData, Result
from ..cli import Display
import time
import json


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    io_path: PathData

    def generate(self) -> None:
        display: Display = Display()

        parsed_data: ParsedData = self.__get_data()
        gen: Constrained = Constrained(
            definitions=parsed_data.definitions
        )

        total: int = len(parsed_data.callings)
        fail: int = 0

        FileManagement.clear_file(self.io_path.result)
        print("\n")
        for i, c in enumerate(parsed_data.callings):
            try:
                display.start_process(c.prompt, i, total, fail)

                start: float = time.perf_counter()
                result: Result = gen.generate(c)
                end: float = time.perf_counter()

                FileManagement.write_json(
                    path=self.io_path.result,
                    data=result
                )
                display.end_process(result.model_dump(), end - start)

            except Exception as e:
                display.problem(c.prompt, str(e))
                pass

    def __get_data(self) -> ParsedData:
        pars: Parsing = Parsing(
            path_data=self.io_path
        )
        return pars.get_file_content()

    def __validate_output_json(self) -> bool:
        try:
            with self.io_path.result.open("r") as f:
                _ = json.load(f)

        except Exception:
            return False

        return True
