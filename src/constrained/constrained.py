from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from ..utils import (
    Definition,
    Calling,
    Result,
    Type,
    check_repetition,
    remove_repetition
)
from .call_function import LLM
from typing import Any
from .get_prompt import FPrompt
from .finite_state_machine import (
    FSM,
    NumberFSM,
    IntegerFSM,
    StringFSM,
    BooleanFSM
)
from .vocab import Vocab
from enum import Enum
import json
from pathlib import Path


class TypeEval(Enum):
    NUMBER = (
        "numbers",
        "number",
        "num",
        "float",
        "floats",
        "decimals",
        "decimal"
    )
    INTEGER = (
        "integers",
        "integer",
        "int"
    )

    BOOLEAN = (
        "boolean",
        "booleans",
        "bool"
    )


class Constrained(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definitions: list[Definition]
    __model: LLM = PrivateAttr(default_factory=LLM)
    __vocab: Vocab = PrivateAttr()

    __max_token_repetition: int = PrivateAttr(default=3)

    @model_validator(mode="after")
    def after_init(self) -> "Constrained":
        path: str = self.__model.vocab_path()
        self.__vocab = Vocab(vocab_path=Path(path))
        return self

    def generate(self, calling: Calling) -> Result:
        definition_dict: dict[str, Definition] = {
            d.name: d
            for d in self.definitions
        }

        selected_func: Definition = self.__process_function(
            calling.prompt,
            definition_dict
        )
        parameters: dict[str, Any] = self.__process_parameter(
            calling.prompt,
            selected_func
        )

        res: Result = Result(
            prompt=calling.prompt,
            name=selected_func.name,
            parameters=parameters
        )
        return res

    def __process_function(
        self,
        prompt: str,
        big_dict: dict[str, Definition]
    ) -> Definition:
        full_prompt: str = FPrompt.function_prompt(
            prompt,
            self.definitions
        )
        input_ids = self.__model.encode(full_prompt)
        definitions_token = [
            self.__model.encode(definition.name)
            for definition in self.definitions
        ]
        generated: list[int] = []

        while True:
            if generated in definitions_token:
                break

            logits = self.__model.get_logits(input_ids)
            valid_token = set()

            for token in definitions_token:
                if (
                    token[:len(generated)] == generated and
                    len(token) > len(generated)
                ):
                    valid_token.add(token[len(generated)])

            next_token = Constrained.max_token(logits, valid_token)
            input_ids.append(next_token)
            generated.append(next_token)

        res: str = self.__model.decode(generated)
        return big_dict[res]

    def __process_parameter(
        self,
        prompt: str,
        definition: Definition
    ) -> dict[str, Any]:
        full_prompt: str = FPrompt.parameter_prompt(prompt, definition)

        input_ids: list[int] = self.__model.encode(full_prompt)
        input_ids += self.__model.encode("{")

        items: list[tuple[str, Type]] = list(definition.parameters.items())
        res: dict[str, Any] = {}

        for idx, (key, ptype) in enumerate(items):
            last_param: bool = (idx == len(items) - 1)
            input_ids += self.__model.encode(f'"{key}":')

            val: list[int] = self.__field_generation(
                input_ids,
                ptype.type,
                last_param
            )
            input_ids += val

            input_ids += self.__model.encode(
                Constrained.separator_literal(
                    last_param
                )
            )

            res[key] = self.__cast_value(self.__model.decode(val), ptype.type)

        return res

    def __field_generation(
        self,
        input_ids: list[int],
        param_type: str,
        is_last: bool
    ) -> list[int]:
        if Constrained.is_numeric(param_type):
            fsm: FSM = (
                IntegerFSM() if param_type in TypeEval.INTEGER.value
                else NumberFSM()
            )
            return self.__field_numeric(
                input_ids, fsm, Constrained.separator_literal(is_last)
            )

        if Constrained.is_boolean(param_type):
            return self.__field_value(input_ids, BooleanFSM())

        open_ids: list[int] = self.__model.encode('"')
        body_ids: list[int] = self.__field_value(
            input_ids + open_ids, StringFSM()
        )

        return open_ids + body_ids

    def __field_value(self, input_ids: list[int], fsm: FSM) -> list[int]:
        state = fsm.start()
        generated: list[int] = []
        working_ids = list(input_ids)

        while True:
            candidates: set[int] = self.__vocab.valid_token_ids(fsm, state)

            if not candidates:
                raise ValueError("No candidates found")

            logits = self.__model.get_logits(working_ids)
            next_token = Constrained.max_token(logits, candidates)
            token_text = self.__vocab.text(next_token)

            if (
                check_repetition(generated, next_token) >
                self.__max_token_repetition
            ):
                return (
                    remove_repetition(generated, next_token) +
                    self.__model.encode('"')
                )

            for c in token_text:
                next_state = fsm.step(state, c)
                if next_state == -1:
                    raise ValueError("Step For the FSM not Valid")
                state = next_state

            generated.append(next_token)
            working_ids.append(next_token)

            if fsm.is_terminal(state):
                break

        return generated

    def __field_numeric(
        self,
        input_ids: list[int],
        fsm: FSM,
        next_literal: str
    ) -> list[int]:
        state = fsm.start()
        generated: list[int] = []
        end_ids = self.__first_token_id(next_literal)
        working_ids = list(input_ids)

        while True:
            candidates: set[int] = self.__vocab.valid_token_ids(fsm, state)
            accept: bool = fsm.is_valid(state)

            if not candidates and not accept:
                raise ValueError(
                    "No candidated found or FSM state not accepted"
                )

            end_active: bool = accept and end_ids is not None
            if end_active and end_ids is not None:
                candidates.add(end_ids)

            logits = self.__model.get_logits(working_ids)
            next_token = Constrained.max_token(logits, candidates)

            if end_active and next_token == end_ids:
                break

            token_text = self.__vocab.text(next_token)
            accepted = ""
            if token_text:
                for c in token_text:
                    next_state = fsm.step(state, c)
                    if next_state == -1:
                        break
                    accepted += c
                    state = next_state

            if not accepted:
                break

            next_token = self.__model.encode(accepted)[0]
            generated.append(next_token)
            working_ids.append(next_token)

        if not fsm.is_valid(state):
            raise ValueError("FSM State not accepted")

        return generated

    def __first_token_id(self, text: str) -> int | None:
        ids = self.__model.encode(text)
        return ids[0] if ids else None

    def __cast_value(self, value: str, ptype: str) -> Any:
        if Constrained.is_numeric(ptype):
            return (
                int(value) if ptype in TypeEval.INTEGER.value
                else float(value)
            )

        if Constrained.is_boolean(ptype):
            return value == "true"

        return json.loads(f"{value}")

    @staticmethod
    def is_numeric(res: str) -> bool:
        return (
            res in (
                *TypeEval.NUMBER.value,
                *TypeEval.INTEGER.value
            )
        )

    @staticmethod
    def is_boolean(res: str) -> bool:
        return (
            res in TypeEval.BOOLEAN.value
        )

    @staticmethod
    def separator_literal(last: bool) -> str:
        return "}" if last else ","

    @staticmethod
    def max_token(logits: list[float], candidates: set[int]) -> int:
        for ids in range(len(logits)):
            if ids not in candidates:
                logits[ids] = float("-inf")

        return logits.index(max(logits))
