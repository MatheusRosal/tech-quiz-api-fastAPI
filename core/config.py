from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    ENVIRONMENT: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-5.6-luna"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

