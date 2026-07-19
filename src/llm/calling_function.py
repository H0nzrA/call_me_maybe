from llm_sdk import Small_LLM_Model  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from pathlib import Path
from .tokenizer import Vocab


class Tokenizer(BaseModel):
    vocab_path: Path


class LLM(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_choice: str = Field(default="Qwen/Qwen3-0.6B")

    __model: Small_LLM_Model = PrivateAttr()
    __vocab: Vocab = PrivateAttr()
    # __tokenizer: Tokenizer = PrivateAttr()

    @model_validator(mode="after")
    def after_init(self) -> "LLM":
        self.__model = Small_LLM_Model(
            model_name=self.model_choice
        )
        self.__vocab = Vocab(
            vocab_path=Path(self.__model.get_path_to_vocab_file())
        )

        return self

    # TODO: Using tokenizer encode
    def encode(self, text: str) -> list[int]:
        return list(self.__model.encode(text)[0].tolist())

    # TODO: Using tokenizer decode
    def decode(self, ids: list[int]) -> str:
        return str(self.__model.decode(ids))

    def get_logits(self, input_ids: list[int]) -> list[float]:
        return list(self.__model.get_logits_from_input_ids(input_ids))

    def vocab_path(self) -> str:
        return str(self.__model.get_path_to_vocab_file())

    def get_vocab(self) -> dict[int, str]:
        return self.__vocab.ids_to_text()
