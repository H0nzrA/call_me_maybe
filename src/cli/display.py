from .syntax import Syntax
import time
from typing import Any


def print_flush(s: str) -> None:
    print(s, flush=True)


class Display:
    LOGO: list[str] = [
        (
            "    mmmm         mmmm   mmmm                "
            "           mmm  mmm                mm               "
        ),
        (
            "  ##\"\"\"\"#        \"\"##   \"\"##          "
            "                 ###  ###                ##               "
        ),
        (
            " ##\"      m#####m  ##     ##       ####m##"
            "m m####m     ######## m#####m\"##  #####m###m  m####m  "
        ),
        (
            " ##       \" mmm##  ##     ##       ## ##"
            " ####mmmm##    ## ## ## \" mmm## ##m "
            "## ##\"  \"####mmmm## "
        ),
        (
            " ##m     m##\"\"\"##  ##     ##      "
            " ## ## ####\"\"\"\"\"\"    ## \"\" ##m#"
            "#\"\"\"##  ####\" ##    ####\"\"\"\"\"\" "
        ),
        (
            "  ##mmmm###mmm###  ##mmm  ##mm"
            "m    ## ## ##\"##mmmm#    ##   "
            " ####mmm###   ###  ###mm##\"\"##mmmm# "
        ),
        (
            "    \"\"\"\"  \"\"\"\" \"\" "
            "  \"\"\"\"   \"\"\"\"  "
            "  \"\" \"\" \"\"  \"\"\"\"\"  "
            "   \"\"    \"\" \"\"\"\" \"\"   #"
            "#   \"\" \"\"\"    \"\"\"\"\"  "
        ),
        (
            "                               "
            "                                "
            "         ###                     "
        )
    ]

    def __init__(self) -> None:
        print(Syntax.CLEAR.value, flush=True)
        for logo in Display.LOGO:
            print(
                f"{Syntax.BOLD.value}{Syntax.ITALIC.value}"
                f"{Syntax.CYAN.value}"
                f"{logo}"
                f"{Syntax.RESET.value}"
            )
            time.sleep(0.008)

    def start_process(self, prompt: str) -> None:
        res: str = Syntax.YELLOW.value + ">>> Processing: "
        res += Syntax.WHITE.value + Syntax.BOLD.value
        res += f"{prompt!r}"
        res += Syntax.RESET.value

        print_flush(res)

    def end_process(self, result: dict[str, Any], t: float) -> None:
        res: str = Syntax.CURSOR_UP.value + Syntax.CLEAR_LINE.value

        res += Syntax.BOLD.value + Syntax.GREEN.value
        res += "(~.~) Completed in " + Syntax.RESET.value

        res += Syntax.DIM.value + Syntax.MAGENTA.value
        res += f"{t:.2f}s" + Syntax.RESET.value

        res += Syntax.BOLD.value + Syntax.GREEN.value
        res += ":\n" + Syntax.RESET.value

        for key, value in result.items():
            res += Syntax.BLUE.value + key + Syntax.RESET.value
            res += f": {value}\n"

        res += Syntax.RESET.value + "\n"

        print_flush(res)
