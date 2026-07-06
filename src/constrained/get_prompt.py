from ..utils import Definition


class FPrompt:
    @classmethod
    def function_prompt(
        cls,
        original_prompt: str,
        definitions: list[Definition]
    ) -> str:
        res: str = ""
        func_dict = {
            d.name: d.description
            for d in definitions
        }
        func_desc = "\n".join(
            f"- {key}: {value}"
            for key, value in func_dict.items()
        )

        res += "Functions definition:\n"
        res += f"{func_desc}\n\n"
        res += f"Select the best function for this prompt: {original_prompt}\n"
        res += "Function: "

        return res

    @classmethod
    def parameter_prompt(
        cls,
        original_prompt: str,
        definition: Definition,
        to_extract: str
    ) -> str:
        res: str = "Extract exactly one parameter from the user's prompt.\n\n"

        res += "Function definition:\n"
        res += f"- {definition.name}: {definition.description}\n"
        res += "- Parameters:\n"
        for key, value in definition.parameters.items():
            res += f"\t- {key}: {value.type}\n"
        res += "\n\n"

        res += f"Prompt: {original_prompt}\n"
        res += f"Parameter to extract {to_extract!r}: "

        return res
