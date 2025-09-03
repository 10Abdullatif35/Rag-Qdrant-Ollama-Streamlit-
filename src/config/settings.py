# src/config/settings.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    qdrant_url: str
    qdrant_api_key: str
    collection_name: str = "my_rag_data"
    embedding_model_name: str = "BAAI/bge-m3"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
