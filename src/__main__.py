from .cli import Argument


class Program:
    def __init__(self) -> None:
        self.__args: Argument = Argument()

    def run(self) -> None:
        print(self.__args.get_io_file())


if __name__ == "__main__":
    try:
        program: Program = Program()
        program.run()

    except Exception as e:
        print(f"Caught exception: {e}")

    except KeyboardInterrupt:
        print("=== Program Stopped ===")
