from .syntax import Syntax
import time


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
