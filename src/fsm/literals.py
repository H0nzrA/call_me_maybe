from .base import FSM


class BooleanFSM(FSM):
    """
    state depend on the litteral "true" "false"
    """

    def __init__(self) -> None:
        super().__init__()
        self.__litteral: tuple[str, str] = ("true", "false")

    def start(self) -> int:
        return 0

    def step(self, state: int, char: str) -> int:
        for lt in self.__litteral:
            if len(lt) > state and lt[state] == char:
                return state + 1

        return -1

    def is_valid(self, state: int) -> bool:
        for lt in self.__litteral:
            if len(lt) == state:
                return True

        return False

    def is_terminal(self, state: int) -> bool:
        return self.is_valid(state)


class StringFSM(FSM):
    """
    1=body
    2=escape
    3=done
    """

    _ESCAPE: set[str] = {'"', "\\", "/", "b", "f", "n", "r", "t"}

    def start(self) -> int:
        return 1

    def step(self, state: int, char: str) -> int:
        if state == 1:
            if char == '"':
                return 3

            if char == "\\":
                return 2

            if ord(char) < 32:
                return -1

            return 1

        if state == 2:
            if char in StringFSM._ESCAPE:
                return 1
            return -1

        return -1

    def is_valid(self, state: int) -> bool:
        return state != 3

    def is_terminal(self, state: int) -> bool:
        return state == 3
