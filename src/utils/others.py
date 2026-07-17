from collections.abc import Callable
from typing import Any
from functools import wraps
import time


def timer_func(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start: float = time.perf_counter()
        res: Any = func(*args, **kwargs)
        end: float = time.perf_counter()

        print(f"Timer: {end - start:.3f} seconds")

        return res

    return wrapper

def check_repetition(content: list[int], generated: int) -> int:
    count: int = 0
    for c in content:
        if c == generated:
            count += 1
    return count

def remove_repetition(content: list[int], repetition: int) -> list[int]:
    res: list[int] = []

    for c in content:
        if c == repetition:
            res.append(c)
            break
        res.append(c)

    return res
