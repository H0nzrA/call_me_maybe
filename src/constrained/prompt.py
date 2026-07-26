"""
Prompt generation utilities.

Provides helper function for building prompt use during
constrained function and parameter generation.
"""

from ..utils import Definition


def function_prompt(
    original_prompt: str,
    definitions: list[Definition]
) -> str:
    """
    Build the prompt used to select the target function.

    Args:
        original_prompt (str): User's input prompt.
        definitions (list[Definition]): Avaliable function definitions.

    Returns:
        A prompt instructing the language model to choose the most
        appropriate function.
    """
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
    """
    Build the prompt used to generate function paramters.

    Args:
        original_prompt (str): User's input prompt.
        definitions (Definition): Selected function definition.

    Returns:
        A prompt instructing the language model to extract the
        parameter value for the selected function.
    """
    params: str = "\n".join(
        f'- "{name}": {ptype.type}'
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
