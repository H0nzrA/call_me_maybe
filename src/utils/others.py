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
