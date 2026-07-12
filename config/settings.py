from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, PostgresDsn
from typing import List

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "EcoSphere ESG Management Platform"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development" # development, staging, production
    DEBUG: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./ecosphere.db"
    
    # Security / JWT
    SECRET_KEY: str = "a-very-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # Rate Limiting
    RATE_LIMIT_GLOBAL: str = "100/minute"
    
    # AI Subsystem / LangGraph
    # AI Subsystem / LangGraph (OpenRouter Gateway)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    CARBON_MODEL: str = "openai/gpt-4o-mini"
    REPORT_MODEL: str = "openai/gpt-4o-mini"
    ANOMALY_MODEL: str = "openai/gpt-4o-mini"
    RECOMMENDATION_MODEL: str = "openai/gpt-4o-mini"
    
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "EcoSphere_AI"

    def validate_ai_config(self) -> None:
        import os
        # Required configuration check
        if not self.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not set or is empty. Please verify your environment settings.")
        if not self.OPENROUTER_BASE_URL:
            raise ValueError("OPENROUTER_BASE_URL is not set or is empty.")
        if not self.CARBON_MODEL:
            raise ValueError("CARBON_MODEL is not set.")
        if not self.REPORT_MODEL:
            raise ValueError("REPORT_MODEL is not set.")
        if not self.ANOMALY_MODEL:
            raise ValueError("ANOMALY_MODEL is not set.")
        if not self.RECOMMENDATION_MODEL:
            raise ValueError("RECOMMENDATION_MODEL is not set.")

        # LangSmith integration
        if self.LANGCHAIN_TRACING_V2 == "true":
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_ENDPOINT"] = self.LANGCHAIN_ENDPOINT
            os.environ["LANGCHAIN_API_KEY"] = self.LANGCHAIN_API_KEY
            os.environ["LANGCHAIN_PROJECT"] = self.LANGCHAIN_PROJECT
        else:
            os.environ["LANGCHAIN_TRACING_V2"] = "false"
            # Ensure any empty keys are popped to prevent LangChain error triggers
            os.environ.pop("LANGCHAIN_API_KEY", None)


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
