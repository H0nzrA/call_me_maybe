from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from .vocab import Vocab
from pathlib import Path


class Tokenizer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vocab_path: str
    __vocab: Vocab = PrivateAttr()

    @model_validator(mode="after")
    def after_init(self) -> "Tokenizer":
        self.__vocab = Vocab(vocab_path=Path(self.vocab_path))
        return self

    def encode(self, text: str) -> list[int]:
        return []

    def decode(self, ids: list[int]) -> str:
        return ""

    def get_vocab(self) -> dict[int, str]:
        return self.__vocab.ids_to_text()
