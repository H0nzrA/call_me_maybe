from enum import Enum, auto
from ..utils import Definition
from typing import Any
import json


class State(Enum):
    START = auto()
    AFTER_BRACE = auto()
    AFTER_KEY = auto()
    VALUE = auto()
    AFTER_VALUE = auto()
    DONE = auto()


class FSM:
    @classmethod
    def allowed_key(cls, state: State, definition: Definition) -> set[str]:
        if state == State.START:
            return {"{"}

        if state == State.AFTER_BRACE:
            return {f"'{k}'" for k in definition.parameters.keys()}

        if state == State.AFTER_KEY:
            return {":"}

        if state == State.AFTER_VALUE:
            return {",", "}"}

        return set()

    @classmethod
    def update_state(cls, state: State, piece: str) -> State:
        return state

    @classmethod
    def json_loads(cls, text: str) -> dict[str, Any]:
        return json.loads(text)
