from ..utils import Definition


def function_prompt(
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


def parameter_prompt(
    original_prompt: str,
    definition: Definition,
) -> str:
    params: str = "\n".join(
        f'- "{name}": {ptype.type}\n'
        for name, ptype in definition.parameters.items()
    )

    prompt: str = (
        "Extraction of function definition"
        " parameter from user's prompt.\n\n"
    )
    prompt += (
        "Function Definition: "
        f"{definition.name} - {definition.description}.\n"
    )
    prompt += f"Parameters:\n{params}\n"
    prompt += f"User's prompt: {original_prompt!r}\n\n"
    prompt += (
        "Fill in the value for each parameter"
        " based on the user's prompt.\n"
    )
    prompt += "Arguments: "

    return prompt
