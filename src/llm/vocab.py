"""
Vocabulary management.

Loads the model vocabulary and provides mapping between token
IDs and their textual representations.
"""

from pathlib import Path
import json
from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator


class VocabError(Exception):
    """Raised when vocabulary cannot be load or is invalid."""

    pass


class Vocab(BaseModel):
    """
    Vocabulary used by the tokenizer.

    Loads vocabulary file and provides bidirectional mappings
    between token IDs and token strings.
    """

    model_config = ConfigDict(extra="forbid")

    vocab_path: Path

    __ids_to_token: dict[int, str] = PrivateAttr(default_factory=dict)
    __token_to_ids: dict[str, int] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def after_init(self) -> "Vocab":
        """
        Load and validate the vocabulary.

        Build the token-to-ID and ID-to-token mapping from the
        vocabulary file.

        Raised:
            VocabError: If the vocabulary file is invalid of contains
                no token.
        """
        self.__ids_to_token = {}
        self.__token_to_ids = {}

        try:
            with self.vocab_path.open("r") as f:
                vocab = json.load(f)

                self.__ids_to_token = {
                    token_id: token_text
                    for token_text, token_id in vocab.items()
                }

        except json.JSONDecodeError as e:
            raise VocabError(
                "Cannot read vocab file "
                f"{self.vocab_path!r}: {e}"
            )

        if not self.__ids_to_token:
            raise VocabError(
                "Vocab file "
                f"{self.vocab_path!r} produce no tokens"
            )

        self.__token_to_ids = {
            v: k
            for k, v in self.__ids_to_token.items()
        }

        return self

    def get_ids_to_token(self) -> dict[int, str]:
        """
        Return the vocabulary mapping from token IDs to token strings.

        Returns:
            A mapping from token IDs to token strings.
        """
        return self.__ids_to_token

    def text(self, idx: int) -> str:
        """
        Return the text associated with the token ID.

        Args:
            idx (int): Token ID.

        Returns:
            The corresponding token string.
        """
        return self.__ids_to_token[idx]

    def ids(self, text: str) -> int:
        """
        Return the token ID associated with a token string.

        Args:
            text (str): Token string.

        Returns:
            The corresponding token ID.
        """
        return self.__token_to_ids[text]

    @staticmethod
    def get_bytes_to_unicode() -> dict[int, str]:
        """
        Build the byte-to-Unicode mapping used by byte-level BPE.

        Returns:
            A mapping from byte values to Unicode characters.
        """
        all_char: list[int] = (
            list(range(ord("!"), ord("~") + 1)) +
            list(range(ord("¡"), ord("¬") + 1)) +
            list(range(ord("®"), ord("ÿ")))
        )
        copy: list[int] = all_char[:]

        n = 0
        for c in range(256):
            if c not in all_char:
                all_char.append(c)
                copy.append(256 + n)
                n += 1

        return dict(zip(all_char, [chr(c) for c in copy]))
