from enum import Enum


class Syntax(Enum):
    RESET = "\033[0m"
    CLEAR = "\033[H\033[J"
    CLEAR_LINE = "\033[2K"

    CURSOR_HOME = "\r"
    CURSOR_UP = "\033[1A"

    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
