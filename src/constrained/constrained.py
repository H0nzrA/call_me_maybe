"""
Constrained function calling generation.

Provides the constrained decoding pipeline used to generate
function name, function parameters value conform to the
provided function definitions.
"""

from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from ..utils import (
    Definition,
    Calling,
    Result,
    Type,
    check_repetition,
    remove_repetition
)
from ..llm import LLM
from typing import Any
from .prompt import function_prompt, parameter_prompt
from ..fsm import (
    FSM,
    NumberFSM,
    IntegerFSM,
    StringFSM,
    BooleanFSM,
    Filter
)
from .type_eval import (
    TypeEval,
    is_boolean,
    is_numeric,
    cast_value,
    separator_literal
)


class Constrained(BaseModel):
    """
    Generate structured function calls using Constrained Decoding.

    This class selects the most approprite function for a prompt
    and generates valid parameter values by restricting the model's
    output with a finite-state machines.
    """

    model_config = ConfigDict(extra="forbid")

    model_name: str
    definitions: list[Definition]

    __model: LLM = PrivateAttr()
    __max_token_repetition: int = PrivateAttr(default=3)
    __max_token_number: int = PrivateAttr(default=64)
    __filter: Filter = PrivateAttr()

    @model_validator(mode="after")
    def after_init(self) -> "Constrained":
        """Initialize the language model and token filter."""
        self.__model = LLM(
            name=self.model_name
        )
        self.__filter = Filter(
            vocab=self.__model.get_vocab()
        )
        return self

    def generate(self, calling: Calling) -> Result:
        """
        Generate a constrained function call for a prompt.

        Args:
            calling (Calling): Function Calling request.

        Return:
            The Generate function call and its parameter in
            'Result' instance.
        """
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
        """
        Generate the function name matchin the input prompt.

        Args:
            prompt (str): User prompt.
            big_dict (dict[str, Definition]): Mapping the function name
            to their definition.

        Returns:
            The selected function definition.
        """
        full_prompt: str = function_prompt(
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
        """
        Generate all parameter value for a function.

        Args:
            prompt (str): User prompt.
            definition (Definition): Selected function defintion.

        Returns:
            A mapping of parameter name to generated value.
        """
        full_prompt: str = parameter_prompt(prompt, definition)

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
                separator_literal(
                    last_param
                )
            )

            res[key] = cast_value(self.__model.decode(val), ptype.type)

        return res

    def __field_generation(
        self,
        input_ids: list[int],
        param_type: str,
        is_last: bool
    ) -> list[int]:
        """
        Generate a parameter value according to its type.

        Args:
            input_ids (list[int]): Prompt token IDs.
            param_type (str): Expected parameter type.
            is_last (bool): Whether this is the final parameter.

        Return:
            The generated token IDs respecting the parameter value.
        """
        if is_numeric(param_type):
            fsm: FSM = (
                IntegerFSM() if param_type in TypeEval.INTEGER.value
                else NumberFSM()
            )
            return self.__field_numeric(
                input_ids, fsm, separator_literal(is_last)
            )

        if is_boolean(param_type):
            return self.__field_value(input_ids, BooleanFSM())

        open_ids: list[int] = self.__model.encode('"')
        body_ids: list[int] = self.__field_value(
            input_ids + open_ids, StringFSM()
        )

        return open_ids + body_ids

    def __field_value(self, input_ids: list[int], fsm: FSM) -> list[int]:
        """
        Generate the constrained non-numeric value.

        The generated token is restricted by the finite-state
        machine untile a terminal state is reached.

        Args:
            input_ids (list[int]): Prompt token IDs.
            fsm (FSM): Finite-State Machine defining valid values.

        Return:
            The generated token IDs.

        Raises:
            ValueError: If no valid token can be generated,
            if the FSM reach an invalid transition.
        """
        state = fsm.start()
        generated: list[int] = []
        working_ids = list(input_ids)

        while True:
            candidates: set[int] = self.__filter.valid_token_ids(fsm, state)

            if not candidates:
                raise ValueError("No candidates found")

            logits = self.__model.get_logits(working_ids)
            next_token = Constrained.max_token(logits, candidates)
            token_text = self.__filter.text(next_token)

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
        """
        Generate the constrained numeric value.

        Args:
            input_ids (list[int]): Prompt token IDs.
            fsm (FSM): Finite-State Machine defining the valid numeric values.
            next_literal (str): Litteral marking the end of the value.

        Returns:
            The generated numeric token IDs.

        Raises:
            ValueError: If no valid numeric value can be generated.
        """
        state = fsm.start()
        generated: list[int] = []
        end_ids = self.__first_token_id(next_literal)
        working_ids = list(input_ids)

        while True:
            candidates: set[int] = self.__filter.valid_token_ids(fsm, state)
            accept: bool = fsm.is_valid(state)

            if len(generated) > self.__max_token_number:
                break

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

            token_text = self.__filter.text(next_token)
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
        """
        Return the first token of a text.

        Args:
            text (str): Text to tokenized.

        Returns:
            The first token Ids, or ``None`` if the text produces no
            tokens.
        """
        ids = self.__model.encode(text)
        return ids[0] if ids else None

    @staticmethod
    def max_token(logits: list[float], candidates: set[int]) -> int:
        """
        Select the highest-scoring token among the candidates.

        Args:
            logits (list[float]): Model logits.
            candidates (set[int]): Allowed token ids.

        Returns:
            The selected token IDs.
        """
        for ids in range(len(logits)):
            if ids not in candidates:
                logits[ids] = float("-inf")

        return logits.index(max(logits))
