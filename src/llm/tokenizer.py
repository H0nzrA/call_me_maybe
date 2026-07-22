from pydantic import BaseModel, ConfigDict, model_validator
from .vocab import Vocab
from pathlib import Path
import regex


class Tokenizer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vocab_path: str

    @model_validator(mode="after")
    def after_init(self) -> "Tokenizer":
        self.__vocab = Vocab(vocab_path=Path(self.vocab_path))
        self.__byte_unicode: dict[int, str] = self.__vocab.get_bytes_to_unicode()
        self.__byte_encoder: dict[str, int] = {
            v: k
            for k, v in self.__byte_unicode.items()
        }
        self.__SPLIT_REGEX = regex.compile(
            r"""
            (?i:'s|'t|'re|'ve|'m|'ll|'d)|
            [^\\r\\n\\p{L}\\p{N}]?\\p{L}+|
            \\p{N}|
            ?[^\\s\\p{L}\\p{N}]+[\\r\\n]*|
            \\s*[\\r\\n]+|
            \\s+(?!\\S)
            |\\s+
            """
        )
        return self

    def encode(self, text: str) -> list[int]:
        ids: list[int] = []

        pieces: list[str] = self.__SPLIT_REGEX.findall(text)
        for p in pieces:
            res: bytes = p.encode("utf-8")
            symboles = "".join(
                self.__byte_unicode[b]
                for b in res
            )

            tokens: list[str] = self.__bpe(symboles)

            for t in tokens:
                ids.append(self.__byte_encoder[t])

        return ids

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

    # TODO: Need to understand what BPE is and
    # how to implement it.
    def __bpe(self, symboles: str) -> list[str]:
        ...
