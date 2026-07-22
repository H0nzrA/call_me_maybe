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
        self.__byte_encoder: dict[str, int] = {
            v: k
            for k, v in self.__vocab.bytes_to_unicode.items()
        }
        return self

    def encode(self, text: str) -> list[int]:
        return []

    def decode(self, ids: list[int]) -> str:
        text: str = "".join(
            self.__vocab.text(i) for i in ids
        )

        raw_text: bytearray = bytearray()
        for ch in text:
            byte: int = self.__byte_encoder[ch]
            raw_text.append(byte)

        return raw_text.decode("utf-8", errors="replace")

    def get_vocab(self) -> dict[int, str]:
        return self.__vocab.ids_to_text()
