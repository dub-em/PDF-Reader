from pydantic import BaseSettings

class Settings(BaseSettings):
    weaviate_apikey: str
    weaviate_url: str
    openai_key: str

    class Config:
        env_file = ".env"

settings = Settings()