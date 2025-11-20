"""LLM client initialization and management."""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Optional
from ..config.settings import Settings


class LLMClients:
    """Manages LLM client instances."""
    
    def __init__(self, settings: Settings):
        """Initialize LLM clients with settings."""
        self.settings = settings
        self._fast_llm: Optional[ChatOpenAI] = None
        self._smart_llm: Optional[ChatOpenAI] = None
        self._embed_llm: Optional[OpenAIEmbeddings] = None
    
    @property
    def fast_llm(self) -> ChatOpenAI:
        """Get or create Fast LLM client."""
        if self._fast_llm is None:
            self._fast_llm = ChatOpenAI(
                model=self.settings.fast_llm_model_name,
                api_key=self.settings.fast_llm_api_key,
                base_url=self.settings.fast_llm_api_base,
                temperature=0.3,
            )
        return self._fast_llm
    
    @property
    def smart_llm(self) -> ChatOpenAI:
        """Get or create Smart LLM client."""
        if self._smart_llm is None:
            self._smart_llm = ChatOpenAI(
                model=self.settings.smart_llm_model_name,
                api_key=self.settings.smart_llm_api_key,
                base_url=self.settings.smart_llm_api_base,
                temperature=0.7,
            )
        return self._smart_llm
    
    @property
    def embed_llm(self) -> OpenAIEmbeddings:
        """Get or create Embedding LLM client."""
        if self._embed_llm is None:
            self._embed_llm = OpenAIEmbeddings(
                model=self.settings.embed_llm_model_name,
                api_key=self.settings.embed_llm_api_key,
                base_url=self.settings.embed_llm_api_base,
            )
        return self._embed_llm

