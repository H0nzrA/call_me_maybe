from pathlib import Path
import json
from .finite_state_machine import FSM


class VocabError(Exception):
    pass


class Vocab:
    def __init__(
        self,
        vocab_path: str
    ) -> None:
        self.__ids_to_text: dict[int, str] = {}

        path: Path = Path(vocab_path)

        try:
            with path.open("r") as f:
                vocab = json.load(f)

                self.__ids_to_text = {
                    token_id: token_text
                    for token_text, token_id in vocab.items()
                }

        except json.JSONDecodeError as e:
            raise VocabError(f"Cannot read vocab file {vocab_path!r}: {e}")

        if not self.__ids_to_text:
            raise VocabError(f"Vocab file {vocab_path!r} produce no tokens")

        self.__grammar_cache: dict[tuple[int, int], set[int]] = {}

    def valid_token_ids(self, fsm: FSM, state: int) -> set[int]:
        cache_key = (id(fsm), state)
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
