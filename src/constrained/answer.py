from pydantic import BaseModel, ConfigDict
from ..utils import FileManagement
from .contrained import Constrained
from ..utils import Parsing, ParsedData, PathData, Result


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    io_path: PathData

    def generate(self) -> None:
        print("Begin generation")

        parsed_data: ParsedData = self.__get_data()
        gen: Constrained = Constrained(
            definitions=parsed_data.definitions
        )
        FileManagement.clear_file(self.io_path.result)
        for c in parsed_data.callings:
            result: Result = gen.generate(c)
            FileManagement.write_json(
                path=self.io_path.result,
                data=result
            )

        print("Finish")

    def __get_data(self) -> ParsedData:
        pars: Parsing = Parsing(
            path_data=self.io_path
        )
        return pars.get_file_content()
