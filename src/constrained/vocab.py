from pathlib import Path
import json
from .finite_state_machine import FSM
from pydantic import BaseModel, ConfigDict, model_validator, PrivateAttr


class VocabError(Exception):
    pass


class Vocab(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vocab_path: Path
    __grammar_cache: dict[tuple[type[FSM], int], set[int]] = PrivateAttr()

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

        self.__grammar_cache = {}

        return self

    def valid_token_ids(self, fsm: FSM, state: int) -> set[int]:
        cache_key = (type(fsm), state)
        cache = self.__grammar_cache.get(cache_key)
        if cache is not None:
            return cache

        valid: set[int] = set()
        for token_id, token_text in self.__ids_to_text.items():
            cursor: int = state
            is_valid: bool = bool(token_text)  # if the token_text is not None
            for c in token_text:
                cursor = fsm.step(cursor, c)
                if cursor == -1:
                    is_valid = False
                    break

            if is_valid:
                valid.add(token_id)

        self.__grammar_cache[cache_key] = valid
        return valid

    def text(self, ids: int) -> str:
        return self.__ids_to_text[ids]

    @staticmethod
    def normalize(text: str) -> str:
        return text.replace("Ġ", " ")
