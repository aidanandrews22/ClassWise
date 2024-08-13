# app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]
    LLM_API_URL: str = "https://api.openai.com/v1/chat/completions"
    LLM_API_KEY: str = os.getenv("LLM_API_URL")
    class Config:
        env_file = ".env"

settings = Settings()