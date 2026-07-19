from .base import FSM


class NumberFSM(FSM):
    def start(self) -> int:
        return 0

    def step(self, state: int, char: str) -> int:
        """
        0=start
        1=after '-'
        2=integer
        3=after '.'
        4=fraction
        """
        if state == 0:
            if char == "-":
                return 1
            if char.isdigit():
                return 2

        elif state == 1:
            if char.isdigit():
                return 2

        elif state == 2:
            if char.isdigit():
                return 2
            if char == ".":
                return 3

        elif state == 3:
            if char.isdigit():
                return 4

        elif state == 4:
            if char.isdigit():
                return 4

        return -1

    def is_valid(self, state: int) -> bool:
        return state in (2, 4)

    def is_terminal(self, state: int) -> bool:
        return False


class IntegerFSM(FSM):
    def start(self) -> int:
        return 0

    def step(self, state: int, char: str) -> int:
        """
        0=start
        1=after '-'
        2=integer
        """
        if state == 0:
            if char == "-":
                return 1
            if char.isdigit():
                return 2

        elif state in (1, 2):
            if char.isdigit():
                return 2

        return -1

    def is_valid(self, state: int) -> bool:
        return state == 2

    def is_terminal(self, state: int) -> bool:
        return False
