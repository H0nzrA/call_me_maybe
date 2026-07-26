"""
Finite-state Machine package.

Provides finite-state machine implementation and vocabulary
filtering utilities for constrained decoding.
"""

from .base import FSM
from .literals import BooleanFSM, StringFSM
from .numbers import NumberFSM, IntegerFSM
from .filter import Filter

__all__: list[str] = [
    "FSM",
    "BooleanFSM",
    "StringFSM",
    "NumberFSM",
    "IntegerFSM",
    "Filter"
]
