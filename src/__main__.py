"""
Command-line entry point for the Call-Me-Maybe application.

This module initializes the application and starts the function
calling pipeline.
"""

from .cli import Argument
from .constrained import Answer
from .utils import timer_func


@timer_func
def main() -> None:
    """Parse arguments and generate the constrained answer."""
    args: Argument = Argument()
    answer = Answer(
        io_path=args.get_io_file()
    )

    answer.generate()


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print("\n\n=== Program Stopped ===\n\n")

    except Exception as e:
        print(f"Unexpected Error: {e}")
