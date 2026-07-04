from pydantic import BaseModel, ConfigDict
from ..utils import FileManagement
from .constrained import Constrained
from ..utils import Parsing, ParsedData, PathData, Result
from ..cli import Display
import time


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    io_path: PathData

    def generate(self) -> None:
        display: Display = Display()

        parsed_data: ParsedData = self.__get_data()
        gen: Constrained = Constrained(
            definitions=parsed_data.definitions
        )

        FileManagement.clear_file(self.io_path.result)
        print("\n")
        for c in parsed_data.callings:
            display.start_process(c.prompt)

            start: float = time.perf_counter()
            result: Result = gen.generate(c)
            end: float = time.perf_counter()

            FileManagement.write_json(
                path=self.io_path.result,
                data=result
            )
            display.end_process(result.model_dump(), end - start)

    def __get_data(self) -> ParsedData:
        pars: Parsing = Parsing(
            path_data=self.io_path
        )
        return pars.get_file_content()
