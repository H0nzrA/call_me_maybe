from pydantic import BaseModel, ConfigDict, PrivateAttr
from ..utils import Definition, Calling, Result
from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any
from .get_prompt import FPrompt


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
        print(f"\nPrompt: {res.prompt}", flush=True)
        print(f"Name: {res.name}", flush=True)
        print("Parameters: ", flush=True)
        for key, value in res.parameters.items():
            print(f"- {key}: {value}", flush=True)
        print()

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
            print(self.__model.decode([next_token]), flush=True, end="")

        res: str = self.__model.decode(generated)
        return big_dict[res]

    def __process_parameter(
        self,
        prompt: str,
        definition: Definition
    ) -> dict[str, Any]:
        return {}
