"""
Finite-state machine for numeric values.

Provides FSM implementation used to constrained
the generation of JSON integer and floating-point values.
"""

from .base import FSM


class NumberFSM(FSM):
    """
    Finite-state Machine for JSON numbers.

    Accepts optional leading minus signs and decimal values.
    """

    def start(self) -> int:
        """Return the initial state of the Machine."""
        return 0

    def step(self, state: int, char: str) -> int:
        """
        Advance the FSM with the given character.

        States:
            0: Initial state.
            1: Minus sign read.
            2: Integer part.
            3: Decimal point read.
            4: Fractional part

        Args:
            state (int): Current FSM state.
            char (str): Input character.

        Returns:
            The next FSM state, ``-1`` if the  transition is invalid.
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
        """
        Check whether a state represents a valid number.

        Args:
            state (int): FSM state.

        Returns:
            True the state represents a complete numeric value.
        """
        return state in (2, 4)

    def is_terminal(self, state: int) -> bool:
        """
        Check whether the current state is terminal.

        Args:
            state (int): FSM state.

        Returns:
            Always ``False`` because the numeric generation it terminated
            externally.
        """
        return False


class IntegerFSM(FSM):
    """
    Finite-state Machine for JSON integers.

    Accepts optional leading minus signs followed by digits.
    """

    def start(self) -> int:
        """Return the initial state of the Machine."""
        return 0

    def step(self, state: int, char: str) -> int:
        """
        Advance the FSM with the given character.

        States:
            0: Initial state.
            1: Minus sign read.
            2: Integer part.

        Args:
            state (int): Current FSM state.
            char (str): Input character.

        Returns:
            The next FSM state, ``-1`` if the  transition is invalid.
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
        """
        Check whether the current state represents a valid integer.

        Args:
            state (int): FSM state.

        Return:
            True if the state represents a complete integer.
        """
        return state == 2

    def is_terminal(self, state: int) -> bool:
        """
        Check whether the current state is terminal.

        Args:
            state (int): FSM state.

        Returns:
            Always ``False`` because the numeric generation it terminated
            externally.
        """
        return False
