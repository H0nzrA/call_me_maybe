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
    ) -> str:
        params: str = ""
        for key, value in definition.parameters.items():
            params += f'- "{key}": {value.type}\n'

        prompt: str = "Extraction of function definition parameter from user's prompt.\n\n"

        prompt += "Function Definition:\n"
        prompt += f"{definition.name}: {definition.description}.\n"
        prompt += f"Parameters:\n{params}\n"

        prompt += f"User's prompt: {original_prompt}\n\n"

        prompt += "Extract all the function definition parameters values from the user's prompt.\n"
        prompt += "Valid JSON object only.\n"
        prompt += "For regex (regular expression) follow the regex syntax, the regular expression grammar.\n"

        prompt += "JSON: "

        return prompt
