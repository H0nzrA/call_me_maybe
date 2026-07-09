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

        prompt = f"""
You are a function parameter extraction system.

Your ONLY task is to extract the parameters from the user's request.

IMPORTANT RULES:
- Do NOT execute the function.
- Do NOT calculate anything.
- Do NOT generate the function result.
- Do NOT transform, reverse, modify, or process values.
- Extract only the values provided by the user.
- Return ONLY the parameters required by the function.
- Do NOT add extra keys.
- Do NOT remove required keys.

Function definition:
{definition.name}: {definition.description}

Parameters:
{params}

User request:
{original_prompt}

OUTPUT RULES:
- Return exactly ONE valid JSON object.
- The JSON must contain only the function parameters.
- Do NOT use Markdown.
- Do NOT write ```json.
- Do NOT write explanations.
- Do NOT write any text before or after the JSON.
- The response must start with '{{' and end with '}}'.

JSON: """

        return prompt
