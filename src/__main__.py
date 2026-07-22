from .cli import Argument, Display
from .constrained import Answer
from .utils import timer_func
from pydantic import BaseModel, PrivateAttr, ConfigDict


class Program(BaseModel):
    model_config = ConfigDict(extra="forbid")

    __args: Argument = PrivateAttr()
    __answer: Answer = PrivateAttr()

    @timer_func
    def run(self) -> None:
        self.__args = Argument()
        self.__answer = Answer(
            io_path=self.__args.get_io_file(),
        )

        self.__answer.generate()


if __name__ == "__main__":
    try:
        display = Display()
        program: Program = Program()
        program.run()

    except (KeyboardInterrupt, EOFError):
        print("\n\n=== Program Stopped ===\n\n")

    except Exception as e:
        print(f"Caught exception: {e}")
