# Libs
from pydantic_settings import BaseSettings, SettingsConfigDict  # Pydantic Settings


# Settings Class
class Settings(BaseSettings):
    postgres_url: str = ""
    secret: str = ""
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")


# Run settings
settings = Settings()
