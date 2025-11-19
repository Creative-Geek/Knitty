"""Application settings and configuration."""

import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Fast LLM Configuration
    fast_llm_api_key: str
    fast_llm_api_base: str
    fast_llm_model_name: str = "llama3-8b-8192"
    
    # Smart LLM Configuration
    smart_llm_api_key: str
    smart_llm_api_base: str
    smart_llm_model_name: str = "gemini-2.5-pro"
    
    # Embedding LLM Configuration
    embed_llm_api_key: str
    embed_llm_api_base: str
    embed_llm_model_name: str = "text-embedding-ada-002"
    
    # Optional: HTML Generation API
    special_sauce_api_url: Optional[str] = None
    special_sauce_api_key: Optional[str] = None
    
    # Application Settings
    config_dir: str = "config"
    log_level: str = "INFO"
    max_retries: int = 3
    chunk_size: int = 2000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

