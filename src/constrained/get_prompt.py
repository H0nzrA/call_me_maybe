from ..utils import Definition


class FPrompt:
    @classmethod
    def function_prompt(cls, original_prompt: str, definitions: list[Definition]) -> str:
        res: str = ""
        func_dict = {
            d.name: d.description
            for d in definitions
        }
        func_desc = "\n".join(
            f"{key}: {value}"
            for key, value in func_dict.items()
        )

        res += f"Functions definition: {func_desc}\n\n"
        res += f"Select the best function for this prompt: {original_prompt}\n"
        res += "Function: "

        return res

    @classmethod
    def parameter_prompt(cls, original_prompt: str, definition: Definition) -> str:
        res: str = "Extraction of parameter from prompt.\n\n"

        res += f"User prompt: {original_prompt!r}.\n\n"

        res += "Function:\n"
        res += f"- name: {definition.name!r}\n"
        res += f"- description: {definition.description!r}\n"
        res += f"- parameter:\n"
        for key, value in definition.parameters.items():
            res += f" - {key}: {value.type}\n"
        res += "\n"

        res += "Extract the parameter values from the user prompt.\n"
        res += "Return ONLY a valid JSON object.\n"
        res += "- No explanation\n"
        res += "- No markdown\n"
        res += "- No code fences\n"
        res += "- Do NOT output anything except JSON\n\n"
        res += "JSON:\n"

        return res
