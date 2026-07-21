from pathlib import Path
import json
from pydantic import BaseModel, ConfigDict, model_validator


class VocabError(Exception):
    pass


class Vocab(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vocab_path: Path

    @model_validator(mode="after")
    def after_init(self) -> "Vocab":
        self.__ids_to_text: dict[int, str] = {}

        try:
            with self.vocab_path.open("r") as f:
                vocab = json.load(f)

                self.__ids_to_text = {
                    token_id: Vocab.normalize(token_text)
                    for token_text, token_id in vocab.items()
                }

        except json.JSONDecodeError as e:
            raise VocabError(
                "Cannot read vocab file "
                f"{self.vocab_path!r}: {e}"
            )

        if not self.__ids_to_text:
            raise VocabError(
                "Vocab file "
                f"{self.vocab_path!r} produce no tokens"
            )

        return self

    def ids_to_text(self) -> dict[int, str]:
        return self.__ids_to_text

    @staticmethod
    def normalize(text: str) -> str:
        return text.replace("Ġ", " ")
