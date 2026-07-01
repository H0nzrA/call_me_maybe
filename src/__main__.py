from .cli import Argument
from .constrained import Answer
from typing import Any


class Program:
    def __init__(self) -> None:
        self.__args = Argument()
        self.__answer = Answer(
            io_path=self.__args.get_io_file(),
        )

    def run(self) -> None:
        self.__answer.generate()


if __name__ == "__main__":
    try:
        program: Program = Program()
        program.run()

    except Exception as e:
        print(f"Caught exception: {e}")

    except KeyboardInterrupt:
        print("=== Program Stopped ===")
