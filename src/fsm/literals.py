"""
Finite-state machine for boolean and string values.

Provides FSM implementations used to constrained the
generation of JSON boolean and string values.
"""

from .base import FSM


class BooleanFSM(FSM):
    """
    Finite-state Machine for JSON boolean literals.

    Accepting the literals ``true`` ``false``.
    """

    def __init__(self) -> None:
        """Initialize the accpeted boolean literals."""
        super().__init__()
        self.__literals: tuple[str, str] = ("true", "false")

    def start(self) -> int:
        """Return the initial FSM state."""
        return 0

    def step(self, state: int, char: str) -> int:
        """
        Advance the FSM state with the given character.

        Args:
            state (int): Current FSM state.
            char (str): Input character.

        Returns:
            The next FSM state, or ``-1`` if the transition is invalid.
        """
        for lt in self.__literals:
            if len(lt) > state and lt[state] == char:
                return state + 1

        return -1

    def is_valid(self, state: int) -> bool:
        """
        Check whether the current state forms a valid boolean literal.

        Args:
            state (int): FSM state.

        Returns:
            True if the current state represents a complete literal.
        """
        for lt in self.__literals:
            if len(lt) == state:
                return True

        return False

    def is_terminal(self, state: int) -> bool:
        """
        Check whether the current state is terminal.

        Args:
            state (int): Current FSM state.

        Return:
            True is the state is valid, False otherwise.
        """
        return self.is_valid(state)


class StringFSM(FSM):
    """
    Finite-state Machine for JSON string values.

    States:
        1: Reading the string body.
        2: Reading an escape sequence.
        3: Closing quotation marck reach.
    """

    def __init__(self) -> None:
        """Initialize the escape sequence literals."""
        super().__init__()
        self.__escape: set[str] = {
            '"', "\\",
            "/", "b",
            "f", "n",
            "r", "t"
        }

    def start(self) -> int:
        """Return the initial FSM state."""
        return 1

    def step(self, state: int, char: str) -> int:
        """
        Advance the FSM state with the given character.

        Args:
            state (int): Current FSM state.
            char (str): Input character.

        Returns:
            The next FSM state, or ``-1`` if the transition is invalid.
        """
        if state == 1:
            if char == '"':
                return 3

            if char == "\\":
                return 2

            if ord(char) < 32:
                return -1

            return 1

        if state == 2:
            if char in self.__escape:
                return 1
            return -1

        return -1

    def is_valid(self, state: int) -> bool:
        """
        Check whether the current state allow additional input.

        Args:
            state (int): FSM state.

        Returns:
            True if the generation may continue.
        """
        return state != 3

    def is_terminal(self, state: int) -> bool:
        """
        Check whether the string has been completely generated.

        Args:
            state (int): FSM state.

        Returns:
            True if the closing quotation mark has been reached.
        """
        return state == 3
