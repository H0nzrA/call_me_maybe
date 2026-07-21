from llm_sdk import Small_LLM_Model  # type: ignore
from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from .tokenizer import Tokenizer


class LLM(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str

    __model: Small_LLM_Model = PrivateAttr()
    __tokenizer: Tokenizer = PrivateAttr()

    @model_validator(mode="after")
    def after_init(self) -> "LLM":
        self.__model = Small_LLM_Model(
            model_name=self.name
        )
        self.__tokenizer = Tokenizer(
            vocab_path=self.vocab_path()
        )

        return self

    def encode(self, text: str) -> list[int]:
        return self.__tokenizer.encode(text)

    def decode(self, ids: list[int]) -> str:
        return self.__tokenizer.decode(ids)

    def get_logits(self, input_ids: list[int]) -> list[float]:
        return list(self.__model.get_logits_from_input_ids(input_ids))

    def vocab_path(self) -> str:
        return str(self.__model.get_path_to_vocab_file())

    def get_vocab(self) -> dict[int, str]:
        return self.__tokenizer.get_vocab()
