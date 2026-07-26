"""
Abstract finite-state machine interface.

Defined the common interface implemented by all
finite-state machine used for constrained decoding.
"""

from abc import ABC, abstractmethod


class FSM(ABC):
    """
    Abstract base class for finite-state machine.

    Defines the interface required to validate generated tokens
    during constrained decoding.
    """

    @abstractmethod
    def start(self) -> int:
        """Ruturn the initial state the finite-state machine."""
        ...

    @abstractmethod
    def step(self, state: int, char: str) -> int:
        """
        Compute the next state for a giving input character.

        Args:
            state (int): Current state of the FSM.
            char (str): Input character.

        Returns:
            The next FSM state.
        """
        ...

    @abstractmethod
    def is_valid(self, state: int) -> bool:
        """
        Check whether a state represent a valid value.

        Args:
            state (int): FSM state.

        Returns:
            True if the state is valid, False otherwise.
        """
        ...

    @abstractmethod
    def is_terminal(self, state: int) -> bool:
        """
        Check whether a state is terminal.

        Args:
            state (int): FSM state.

        Returns:
            True if the state is terminal, False otherwise.
        """
        ...
