from pydantic import BaseModel, ConfigDict, model_validator
from .vocab import Vocab
from pathlib import Path
import regex


class Tokenizer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vocab_path: str
    merge_path: str

    @model_validator(mode="after")
    def after_init(self) -> "Tokenizer":
        self.__vocab = Vocab(vocab_path=Path(self.vocab_path))
        self.__byte_unicode: dict[int, str] = self.__vocab.get_bytes_to_unicode()
        self.__byte_encoder: dict[str, int] = {
            v: k
            for k, v in self.__byte_unicode.items()
        }
        self.__split_regex = regex.compile(
            r"""
            (?i:'s|'t|'re|'ve|'m|'ll|'d)|
            [^\\r\\n\\p{L}\\p{N}]?\\p{L}+|
            \\p{N}|
            [^\\s\\p{L}\\p{N}]+[\\r\\n]*|
            \\s*[\\r\\n]+|
            \\s+(?!\\S)
            |\\s+
            """,
            regex.VERBOSE
        )

        self.__merge_data: dict[tuple[str, str], int] = {}
        with Path(self.merge_path).open("r") as f:
            dt = f.read().split("\n")
            n = 0

            for d in dt:
                if d.startswith("#") or not d:
                    continue
                tmp = d.split()
                self.__merge_data[(tmp[0], tmp[1])] = n
                n += 1

        return self

    def encode(self, text: str) -> list[int]:
        ids: list[int] = []

        pieces: list[str] = self.__split_regex.findall(text)
        for p in pieces:
            res: bytes = p.encode("utf-8")
            symboles = "".join(
                self.__byte_unicode[b]
                for b in res
            )

            tokens: list[str] = self.__bpe(symboles)

            for t in tokens:
                ids.append(self.__vocab.ids(t))

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
        return self.__vocab.get_ids_to_token()

    def __bpe(self, symbols: str) -> list[str]:
        l_symbols: list[str] = list(symbols)

        while True:
            pairs: list[tuple[str, str]] = self.__adjacent(l_symbols)

            valid = [
                pair
                for pair in pairs
                if pair in self.__merge_data
            ]

            if not valid:
                break

            best = min(
                valid,
                key=lambda p: self.__merge_data[p]
            )
            l_symbols = self.__merge(l_symbols, best)

        return l_symbols

    def __adjacent(self, token: list[str]) -> list[tuple[str, str]]:
        return [
            (token[i], token[i + 1])
            for i in range(len(token) - 1)
        ]

    def __merge(self, token: list[str], pairs: tuple[str, str]) -> list[str]:
        merged: list[str] = []

        i = 0
        while i < len(token):
            if (
                i < len(token) - 1 and
                token[i] == pairs[0] and
                token[i + 1] == pairs[1]
            ):
                merged.append(token[i] + token[i + 1])
                i += 2
            else:
                merged.append(token[i])
                i += 1

        return merged
