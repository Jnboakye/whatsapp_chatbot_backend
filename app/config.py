from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # AI Provider: "claude" or "openai"
    ai_provider: str = "claude"

    # Anthropic (Claude)
    anthropic_api_key: str = ""

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_number: str = ""  # e.g. whatsapp:+14155238886

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()