# Pydantic Settings
from pydantic_settings import BaseSettings, SettingsConfigDict


# Settings Class
class Settings(BaseSettings):
    postgres_url: str = ""
    secret: str = ""
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")


# Run settings
settings = Settings()
