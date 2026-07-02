from pydantic import BaseModel, ConfigDict, PrivateAttr
from ..utils import Definition, ParsedData, Result
from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any
from .get_prompt import FPrompt
from .finite_state_machine import State, FSM


class Constrained(BaseModel):
    model_config = ConfigDict(extra="forbid")

    parsed_data: ParsedData
    __model: Small_LLM_Model = PrivateAttr(default_factory=Small_LLM_Model)
    __result: list[Result] = PrivateAttr(default_factory=list)

    def generate(self) -> list[Result]:
        self.__process_generation()
        return self.__result

    def __process_generation(self) -> None:
        definition_dict: dict[str, Definition] = {
            d.name: d
            for d in self.parsed_data.definitions
        }

        for c in self.parsed_data.callings:
            selected_func: Definition = self.__process_function(
                c.prompt,
                definition_dict
            )
            parameters: dict[str, Any] = self.__process_parameter(
                c.prompt,
                selected_func
            )

            res: Result = Result(
                prompt=c.prompt,
                name=selected_func.name,
                parameters=parameters
            )
            print(f"\nPrompt: {res.prompt}", flush=True)
            print(f"Name: {res.name}", flush=True)
            print(f"Parameters: ", flush=True)
            for key, value in res.parameters:
                print(f"- {key}: {value}", flush=True)
            print()

            self.__result.append(res)

    def __process_function(
        self,
        prompt: str,
        big_dict: dict[str, Definition]
    ) -> Definition:
        full_prompt: str = FPrompt.function_prompt(prompt, self.parsed_data.definitions)
        input_ids = self.__model.encode(full_prompt)[0].tolist()
        definitions_token = [
            self.__model.encode(definition.name).tolist()[0]
            for definition in self.parsed_data.definitions
        ]
        generated: list[int] = []

        while True:
            if generated in definitions_token:
                break

            logits = self.__model.get_logits_from_input_ids(input_ids)
            valid_token = set()

            for token in definitions_token:
                if (
                    token[:len(generated)] == generated and
                    len(token) > len(generated)
                ):
                    valid_token.add(token[len(generated)])

            for ids in range(len(logits)):
                if ids not in valid_token:
                    logits[ids] = float("-inf")

            next_token = logits.index(max(logits))
            input_ids.append(next_token)
            generated.append(next_token)
            print(self.__model.decode([next_token]), flush=True, end="")

        res: str = self.__model.decode(generated)
        return big_dict[res]

    def __process_parameter(
        self,
        prompt: str,
        definition: Definition
    ) -> dict[str, Any]:
        # full_prompt: str = FPrompt.parameter_prompt(prompt, definition)
        # input_ids = self.__model.encode(full_prompt).tolist()[0]
        #
        # state: State = State.START
        # text: str = ""
        #
        # while True:
        #     logits = self.__model.get_logits_from_input_ids(input_ids)
        #     allowed_token = FSM.allowed_key(state, definition)
        #
        #     for i in range(len(logits)):
        #         token_str = self.__model.decode([i])
        #
        #         if token_str not in allowed_token:
        #             logits[i] = float("-inf")
        #
        #     next_token = logits.index(max(logits))
        #     input_ids.append(next_token)
        #
        #     piece: str = self.__model.decode([next_token])
        #     text += piece
        #
        #     state = FSM.update_state(state, piece)
        #
        #     if state == State.DONE:
        #         break
        #
        # return FSM.json_loads(text)
        return {}
