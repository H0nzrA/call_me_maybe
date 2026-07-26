"""
General utility functions.

Provides helper functions for execution timing and token repetition
handling.
"""

from collections.abc import Callable
from typing import Any
from functools import wraps
import time
from .syntax import Syntax
from datetime import timedelta


def timer_func(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Measure and display the execution time of a function.

    Args:
        func (Callable[..., Any]): Function to decorate.

    Returns:
        A wrapper function that print it's execution time.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Execute the wrapper function and measure its runtime.

        Args:
            *args (Any): Positional arguments passed to the wrapped function.
            **kwargs (Any): Keyword arguments passed to the wrapper function.

        Returns:
            The return value of the wrapper function.
        """
        start: float = time.perf_counter()
        res: Any = func(*args, **kwargs)
        end: float = time.perf_counter()

        t: timedelta = timedelta(seconds=(end - start))
        print(
            f"{Syntax.YELLOW.value}{Syntax.DIM.value}"
            f">>> Function Execution: {t}<<<"
            f"{Syntax.RESET.value}"
        )

        return res

    return wrapper


def check_repetition(content: list[int], generated: int) -> int:
    """
    Count the occurence of a token in a sequence.

    Args:
        content (list[int]): Sequence of generated token IDs.
        generated (int): Token ID to count.

    Returns:
        The number of occurences of the token.
    """
    count: int = 0
    for c in content:
        if c == generated:
            count += 1
    return count


def remove_repetition(content: list[int], repetition: int) -> list[int]:
    """
    Truncate a sequence after the first repeated token.

    Keeps the first occurence of the repeated token and discards
    all subsequence elements.

    Args:
        content (list[int]): Sequence of generated token IDs.
        repetition (int): Token ID that marks the repetition.
    """
    res: list[int] = []

    for c in content:
        if c == repetition:
            res.append(c)
            break
        res.append(c)

    return res
