import json
from typing import Any, Type
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseAgent:
    def __init__(self, system_prompt: str, output_schema: Type[BaseModel]):
        self.system_prompt = system_prompt
        self.output_schema = output_schema
        # Use GPT-4o or latest available
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2).with_structured_output(self.output_schema)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def invoke(self, input_context: dict) -> BaseModel:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=json.dumps(input_context))
        ]
        response = await self.llm.ainvoke(messages)
        return response
