from .contrained.parsing import Parsing
from .contrained.cli import CLI

class Program:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        cli = CLI()
        pars = Parsing(
            definition=cli.get_io_file().definition,
            calling=cli.get_io_file().calling
        )
        val = pars.get_file_content()


if __name__ == "__main__":
    try:
        program: Program = Program()
        program.run()

    except Exception as e:
        print(f"Caught exception: {e}")

    except KeyboardInterrupt:
        print("=== Program Stopped ===")
