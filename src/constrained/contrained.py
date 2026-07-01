from pydantic import BaseModel, ConfigDict, PrivateAttr
from ..utils import Definition, ParsedData, Result
from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any


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

            self.__result.append(res)

    def __process_function(
        self,
        prompt: str,
        big_dict: dict[str, Definition]
    ) -> Definition:
        full_prompt: str = self.__get_function_prompt(prompt)
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

        res: str = self.__model.decode(generated)
        return big_dict[res]

    def __get_function_prompt(self, prompt: str) -> str:
        res: str = ""
        func_dict = {
            d.name: d.description
            for d in self.parsed_data.definitions
        }
        func_desc = "\n".join(
            f"{key}: {value}"
            for key, value in func_dict.items()
        )

        res += f"Functions definition: {func_desc}\n\n"
        res += f"Select the best function for this prompt: {prompt}\n"
        res += "Function: "

        return res

    def __process_parameter(
        self,
        prompt: str,
        definition: Definition
    ) -> dict[str, Any]:
        return {
            "Teddy": "Andrianina"
        }
