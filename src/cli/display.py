from ..utils import Syntax
import time
from typing import Any
from pydantic import BaseModel, ConfigDict, PrivateAttr


def print_flush(*args: Any, **kwargs: Any) -> None:
    print(*args, **kwargs, flush=True)


class Display(BaseModel):
    model_config = ConfigDict(extra="forbid")

    __logo: list[str] = PrivateAttr(
        default=[
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
    )

    def introduction(self) -> None:
        print(Syntax.CLEAR.value, flush=True)
        for logo in self.__logo:
            print(
                f"{Syntax.BOLD.value}{Syntax.ITALIC.value}"
                f"{Syntax.CYAN.value}"
                f"{logo}"
                f"{Syntax.RESET.value}"
            )
            time.sleep(0.008)

    def start_process(
        self,
        prompt: str,
        count: int,
        total: int,
        fail: int
    ) -> None:
        res: str = ""

        res += Syntax.YELLOW.value + ">>> Processing: "
        res += Syntax.WHITE.value + Syntax.BOLD.value
        res += f"{prompt!r}\n"
        res += Syntax.RESET.value

        res += self.__calculate_loading(count, total)
        res += Syntax.BOLD.value + f" ({count}/{total})"
        if fail:
            res += f" | Fail: {fail}"

        res += Syntax.RESET.value

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

    def full_stats(self, total: int, fails: list[str]) -> None:
        res: str = Syntax.BOLD.value

        res += Syntax.CYAN.value + Syntax.BOLD.value
        res += Syntax.DIM.value
        res += "All Calling function processed!!\n"
        res += Syntax.RESET.value

        if fails:
            res += Syntax.RED.value
            res += "Calling Function FAILED:\n"
            res += Syntax.RESET.value
            for f in fails:
                res += f"- {f!r}\n"

        print_flush(res)

    def __calculate_loading(self, count: int, total: int) -> str:
        block: int = 60
        if total <= 0:
            return "█" * block

        filled = min(block, max(0, (block * count) // total))

        return (
            (Syntax.BLUE.value + "█" + Syntax.RESET.value) * filled
            + f"{Syntax.DIM.value}█{Syntax.RESET.value}" * (block - filled)
        )

    def valid_print(self, text: str) -> None:
        res: str = Syntax.GREEN.value + Syntax.BOLD.value
        res += text
        res += Syntax.RESET.value
        print_flush(res)

    def invalid_print(self, text: str) -> None:
        res: str = Syntax.RED.value + Syntax.BOLD.value
        res += text
        res += Syntax.RESET.value
        print_flush(res)

    def menu(self, title: str, choices: list[str]) -> str:
        print_flush(title)

        for i, val in enumerate(choices):
            print_flush(f"({i + 1}) - {val}", end="\n")

        while True:
            try:
                n: int = int(input("Choices: "))
                if n <= 0 or n > len(choices):
                    raise ValueError(f"Choice out of range: {n}")

                res: str = choices[n - 1]
                self.valid_print(f"Your choices: {res}")
                return res

            except ValueError as e:
                self.invalid_print(str(e))
                pass
