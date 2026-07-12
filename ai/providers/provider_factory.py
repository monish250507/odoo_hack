from ai.providers.openrouter_provider import OpenRouterLLMProvider
from config.settings import settings

class LLMProviderFactory:
    _provider = None

    @classmethod
    def get_provider(cls) -> OpenRouterLLMProvider:
        if cls._provider is None:
            # Validate config before instantiating
            settings.validate_ai_config()
            cls._provider = OpenRouterLLMProvider(
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL
            )
        return cls._provider
