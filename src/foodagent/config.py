from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    llm_api_key: str = ""
    llm_model: str = "gemini-2.0-flash"

    taxa_entrega_fixa: float = 5.00
    taxa_entrega_por_km: float = 1.20


def load_settings() -> Settings:
    return Settings()
