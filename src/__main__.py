from .cli import Argument
from .constrained import Parsing, Answer
from typing import Any


class Program:
    def __init__(self) -> None:
        self.__args: dict[str, Any] = Argument().get_io_file()
        self.__parser: Parsing = Parsing(**self.__args)
        self.__gen: Answer = Answer(
            parsed_data=self.__parser.get_file_content()
        )

    def run(self) -> None:
        self.__gen.generate()


if __name__ == "__main__":
    try:
        program: Program = Program()
        program.run()

    except Exception as e:
        print(f"Caught exception: {e}")

    except KeyboardInterrupt:
        print("=== Program Stopped ===")
