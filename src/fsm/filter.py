from ..fsm import FSM
from pydantic import BaseModel, ConfigDict, PrivateAttr


class FilterError(Exception):
    pass


class Filter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vocab: dict[int, str]
    __grammar_cache: dict[
        tuple[type[FSM], int], set[int]
    ] = PrivateAttr(default={})

    def valid_token_ids(self, fsm: FSM, state: int) -> set[int]:
        cache_key = (type(fsm), state)
        cache = self.__grammar_cache.get(cache_key)
        if cache is not None:
            return cache

        valid: set[int] = set()
        for token_id, token_text in self.vocab.items():
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
        return self.vocab[ids]
