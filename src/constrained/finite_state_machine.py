from abc import ABC, abstractmethod


class FSM(ABC):
    @abstractmethod
    def start(self) -> int:
        ...

    @abstractmethod
    def step(self, state: int, char: str) -> int:
        ...

    @abstractmethod
    def is_valid(self, state: int) -> bool:
        ...

    @abstractmethod
    def is_terminal(self, state: int) -> bool:
        ...


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
