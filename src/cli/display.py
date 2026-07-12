from ..utils import Syntax
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

    def start_process(self, prompt: str, count: int, total: int, fail: int) -> None:
        res: str = ""

        res += Syntax.YELLOW.value + ">>> Processing: "
        res += Syntax.WHITE.value + Syntax.BOLD.value
        res += f"{prompt!r}\n"
        res += Syntax.RESET.value

        res += self.__calculate_loading(count, total)
        res += Syntax.BOLD.value + f" ({count}/{total})"
        if fail:
            res += f" | Fail: {fail}"

        res +=Syntax.RESET.value

        print_flush(res)

    def end_process(self, result: dict[str, Any], t: float) -> None:
        res: str = (Syntax.CURSOR_UP.value + Syntax.CLEAR_LINE.value) * 2

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

    def problem(self, prompt: str, motif: str) -> None:
        res: str = (Syntax.CURSOR_UP.value + Syntax.CLEAR_LINE.value) * 2

        res += Syntax.BOLD.value + Syntax.RED.value
        res += "!!! Problem encountered with: " + Syntax.RESET.value

        res += Syntax.WHITE.value + Syntax.BOLD.value
        res += f"{prompt!r}\n"
        res += Syntax.RESET.value

        res += Syntax.YELLOW.value + "Motif: " + Syntax.RESET.value
        res += Syntax.WHITE.value + Syntax.BOLD.value
        res += f"{motif!r}\n"
        res += Syntax.RESET.value

        res += Syntax.RESET.value + "\n"

        print_flush(res)

    def __calculate_loading(self, count: int, total: int) -> str:
        if total <= 0:
            return "█" * 20

        filled = min(20, max(0, (20 * count) // total))

        return (
            (Syntax.BLUE.value + "█" + Syntax.RESET.value) * filled
            + "█" * (20 - filled)
        )
