"""
Command-line interface packages.

Provides argument parsing and terminal display utilities
for the application.
"""

from .args import Argument, ArgsError
from .display import Display


__all__: list[str] = [
    "Argument",
    "ArgsError",
    "Display"
]
