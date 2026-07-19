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
