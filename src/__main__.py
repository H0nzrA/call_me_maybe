from .cli import Argument, Display
from .constrained import Answer
from .utils import timer_func


class Program:
    def __init__(self) -> None:
        self.__args = Argument()
        self.__answer = Answer(
            io_path=self.__args.get_io_file(),
        )

    @timer_func
    def run(self) -> None:
        self.__answer.generate()


if __name__ == "__main__":
    try:
        display = Display()
        program: Program = Program()
        program.run()

    except Exception as e:
        print(f"Caught exception: {e}")

    except KeyboardInterrupt:
        print("=== Program Stopped ===")
