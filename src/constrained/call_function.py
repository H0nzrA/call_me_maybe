from llm_sdk import Small_LLM_Model  # type: ignore


class LLM:
    def __init__(
        self,
        model: str = "Qwen/Qwen3-0.6B",
    ) -> None:
        self.__model: Small_LLM_Model = Small_LLM_Model(
            model_name=model
        )

    def encode(self, text: str) -> list[int]:
        return list(self.__model.encode(text)[0].tolist())

    def decode(self, ids: list[int]) -> str:
        return str(self.__model.decode(ids))

    def get_logits(self, input_ids: list[int]) -> list[float]:
        return list(self.__model.get_logits_from_input_ids(input_ids))

    def vocab_path(self) -> str:
        return str(self.__model.get_path_to_vocab_file())
