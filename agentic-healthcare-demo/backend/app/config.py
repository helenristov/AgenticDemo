import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env if present (safe for local dev)
load_dotenv()

class Settings(BaseModel):
    # --------------------
    # LLM Provider Config
    # --------------------
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    # values: openai | azure | none

    # --------------------
    # OpenAI (public API)
    # --------------------
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # --------------------
    # Azure OpenAI (optional)
    # --------------------
    AZURE_OPENAI_ENDPOINT: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION: str = os.getenv(
        "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"
    )
    AZURE_OPENAI_CHAT_DEPLOYMENT: str | None = os.getenv(
        "AZURE_OPENAI_CHAT_DEPLOYMENT"
    )

    # --------------------
    # RAG / Demo Settings
    # --------------------
    ENABLE_LOCAL_FALLBACK_RAG: bool = (
        os.getenv("ENABLE_LOCAL_FALLBACK_RAG", "true").lower() == "true"
    )

    LIVE_API_BASE_URL: str = os.getenv("LIVE_API_BASE_URL", "http://localhost:8000/mock-live")
    LIVE_API_KEY: str | None = os.getenv("LIVE_API_KEY")

    def validate(self):
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        if self.LLM_PROVIDER == "azure" and not (
            self.AZURE_OPENAI_ENDPOINT
            and self.AZURE_OPENAI_API_KEY
            and self.AZURE_OPENAI_CHAT_DEPLOYMENT
        ):
            raise ValueError("Azure OpenAI credentials are incomplete")

settings = Settings()
settings.validate()
