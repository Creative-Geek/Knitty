"""CV processing and text extraction."""

import logging
from pathlib import Path
from typing import Optional
from langchain_community.document_loaders import PyPDFLoader
from ..config.prompts import PromptManager
from .llm_clients import LLMClients

logger = logging.getLogger(__name__)


class CVProcessor:
    """Processes CV files and extracts content."""
    
    def __init__(self, llm_clients: LLMClients, prompt_manager: PromptManager):
        """Initialize CV processor."""
        self.llm_clients = llm_clients
        self.prompt_manager = prompt_manager
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            cv_raw_text = "\n".join([page.page_content for page in pages])
            logger.info(f"Extracted {len(cv_raw_text)} characters from PDF")
            return cv_raw_text
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    def combine_cv_content(self, cv_raw_text: str, additional_info: Optional[str] = None) -> str:
        """Combine CV text with additional information."""
        if additional_info and additional_info.strip():
            cv_text = f"""
------------
CV Raw Text:
------------
{cv_raw_text}
---------------
Additional Info:
---------------
{additional_info.strip()}
"""
        else:
            cv_text = cv_raw_text
        
        return cv_text
    
    def extract_keywords(self, cv_text: str) -> str:
        """Extract keywords from CV using Fast LLM."""
        try:
            prompt = self.prompt_manager.format_cv_keywords_prompt(cv_text)
            response = self.llm_clients.fast_llm.invoke([("human", prompt)])
            
            # Clean JSON response (remove code blocks if present)
            content = response.content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            logger.info(f"Extracted keywords from CV")
            return content
        except Exception as e:
            logger.error(f"Error extracting CV keywords: {e}")
            raise ValueError(f"Failed to extract CV keywords: {e}")

