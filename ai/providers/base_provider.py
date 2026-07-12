from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel
from langchain_core.language_models import BaseChatModel

class BaseLLMProvider(ABC):
    @abstractmethod
    def get_llm(self, model_name: str, temperature: float = 0.2) -> BaseChatModel:
        """
        Return a configured standard ChatModel.
        """
        pass

    @abstractmethod
    def get_structured_llm(
        self,
        model_name: str,
        output_schema: Type[BaseModel],
        temperature: float = 0.2
    ) -> BaseChatModel:
        """
        Return a ChatModel with a structured output schema configured.
        """
        pass
