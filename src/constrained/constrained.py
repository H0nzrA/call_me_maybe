from pydantic import BaseModel, ConfigDict, PrivateAttr
from ..utils import Definition, Calling, Result, brackets_validator
from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any
from .get_prompt import FPrompt
import json


class Constrained(BaseModel):
    model_config = ConfigDict(extra="forbid")

    definitions: list[Definition]
    __model: Small_LLM_Model = PrivateAttr(default_factory=Small_LLM_Model)

    def generate(self, calling: Calling) -> Result:
        return self.__process_generation(calling)

    def __process_generation(self, calling: Calling) -> Result:
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
        input_ids = self.__model.encode(full_prompt)[0].tolist()
        definitions_token = [
            self.__model.encode(definition.name).tolist()[0]
            for definition in self.definitions
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

        res: str = self.__model.decode(generated)
        return big_dict[res]

    def __process_parameter(
        self,
        prompt: str,
        definition: Definition
    ) -> dict[str, Any]:
        res: dict[str, Any] = {}

        full_prompt: str = FPrompt.parameter_prompt(prompt, definition)
        input_ids = self.__model.encode(full_prompt)[0].tolist()
        # print(full_prompt, flush=True, end="")

        generated_text: str = ""

        while True:

            if brackets_validator(generated_text):
                break

            logits = self.__model.get_logits_from_input_ids(input_ids)
            next_token = logits.index(max(logits))

            text = self.__model.decode([next_token])
            generated_text += text

            input_ids.append(next_token)
            # print(text, flush=True, end="")

        res = self.__validate_parameter(generated_text, definition)
        return res

    def __validate_parameter(self, generated: str, definition: Definition) -> dict[str, Any]:
        tmp: dict[str, Any] = json.loads(generated)
        res: dict[str, Any] = {}

        for key, params in definition.parameters.items():
            if params.type in (
                "number",
                "numbers",
                "decimal",
                "decimals",
                "float"
            ):
                res[key] = float(tmp[key])

            elif params.type in (
                "integer",
                "integers",
                "int"
            ):
                res[key] = int(tmp[key])

            else:
                res[key] = tmp[key]

        return res
