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

def brackets_validator(text: str) -> bool:
    if not text:
        return False

    pairs: dict[str, str] = {
        "}":"{",
    }
    stack: list[str] = []

    for c in text:
        if c in "{":
            stack.append(c)
        elif c in pairs:
            if not stack:
                return False
            if stack.pop() != pairs[c]:
                return False

    return len(stack) == 0
