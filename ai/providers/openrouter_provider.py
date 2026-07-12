from typing import Type
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from ai.providers.base_provider import BaseLLMProvider

class OpenRouterLLMProvider(BaseLLMProvider):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_llm(self, model_name: str, temperature: float = 0.2) -> BaseChatModel:
        return ChatOpenAI(
            model=model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=temperature,
            default_headers={
                "HTTP-Referer": "https://ecosphere-esg.com",
                "X-Title": "EcoSphere ESG Platform"
            }
        )

    def get_structured_llm(
        self,
        model_name: str,
        output_schema: Type[BaseModel],
        temperature: float = 0.2
    ) -> BaseChatModel:
        llm = self.get_llm(model_name=model_name, temperature=temperature)
        return llm.with_structured_output(output_schema)
