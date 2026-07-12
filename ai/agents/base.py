import json
from typing import Any, Type
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential

from ai.providers.provider_factory import LLMProviderFactory

class BaseAgent:
    def __init__(self, system_prompt: str, output_schema: Type[BaseModel], model_name: str):
        self.system_prompt = system_prompt
        self.output_schema = output_schema
        self.model_name = model_name
        
        # Centralized provider initialization
        provider = LLMProviderFactory.get_provider()
        self.llm = provider.get_structured_llm(
            model_name=self.model_name,
            output_schema=self.output_schema,
            temperature=0.2
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def invoke(self, input_context: dict) -> BaseModel:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=json.dumps(input_context))
        ]
        response = await self.llm.ainvoke(messages)
        return response
