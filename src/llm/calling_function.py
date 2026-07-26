"""
Language model wrapper.

Provides a high-level interface for tokenization and
text generation using a small language model.
"""

from llm_sdk import Small_LLM_Model  # type: ignore
from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from .tokenizer import Tokenizer


class LLM(BaseModel):
    """
    Wrapper around the small language model.

    Provides an unified interface for tokenization,
    vocabulary access, and next-token prediction.
    """

    model_config = ConfigDict(extra="forbid")

    name: str

    __model: Small_LLM_Model = PrivateAttr()
    __tokenizer: Tokenizer = PrivateAttr()

    @model_validator(mode="after")
    def after_init(self) -> "LLM":
        """Initialize the language model and tokenizer."""
        self.__model = Small_LLM_Model(
            model_name=self.name
        )
        self.__tokenizer = Tokenizer(
            vocab_path=self.vocab_path(),
            merge_path=self.__model.get_path_to_merges_file()
        )

        return self

    def encode(self, text: str) -> list[int]:
        """
        Encode text into token IDs.

        Args:
            text (str): Input text.

        Returns:
            The encoded token IDs.
        """
        return self.__tokenizer.encode(text)

    def decode(self, ids: list[int]) -> str:
        """
        Decode token IDs into text.

        Args:
            ids (list[int]): Token IDs.

        Returns:
            The decoded text.
        """
        return self.__tokenizer.decode(ids)

    def get_logits(self, input_ids: list[int]) -> list[float]:
        """
        Compute the logits for the next token.

        Args:
            input_ids (list[int]): Input token IDs.

        Return:
            The logits for the next token prediction.
        """
        return list(self.__model.get_logits_from_input_ids(input_ids))

    def vocab_path(self) -> str:
        """
        Return the path to the model vocabulary.

        Returns:
            The vocabulary file path.
        """
        return str(self.__model.get_path_to_vocab_file())

    def get_vocab(self) -> dict[int, str]:
        """
        Return the tokenizer vocabulary.

        Returns:
            A mapping from token IDs to token strings.
        """
        return self.__tokenizer.get_vocab()
