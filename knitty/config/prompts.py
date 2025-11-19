"""Prompt management for loading and formatting prompts."""

import os
from pathlib import Path
from typing import Optional


class PromptManager:
    """Manages loading and formatting of prompts from config files."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize prompt manager with config directory."""
        self.config_dir = Path(config_dir)
        self._cache = {}
    
    def _load_file(self, filename: str) -> str:
        """Load a configuration file."""
        if filename in self._cache:
            return self._cache[filename]
        
        file_path = self.config_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        
        self._cache[filename] = content
        return content
    
    @property
    def cv_template(self) -> str:
        """Get CV template."""
        return self._load_file('cvTemplate.txt')
    
    @property
    def cv_keywords_prompt(self) -> str:
        """Get CV keywords extraction prompt template."""
        return self._load_file('cvKeywordsPrompt.txt')
    
    @property
    def job_keywords_prompt(self) -> str:
        """Get job keywords extraction prompt template."""
        return self._load_file('jobKeywordsPrompt.txt')
    
    @property
    def job_rag_prompt(self) -> str:
        """Get job RAG extraction prompt."""
        return self._load_file('jobRagPrompt.txt')
    
    @property
    def cv_enhance_prompt(self) -> str:
        """Get CV enhancement prompt template."""
        return self._load_file('cvEnhancePrompt.txt')
    
    def format_cv_keywords_prompt(self, cv_text: str) -> str:
        """Format CV keywords extraction prompt."""
        return self.cv_keywords_prompt.format(cvText=cv_text)
    
    def format_job_keywords_prompt(self, job_posting_text: str) -> str:
        """Format job keywords extraction prompt."""
        return self.job_keywords_prompt.format(jobPostingText=job_posting_text)
    
    def format_cv_enhance_prompt(
        self,
        cv_template: str,
        cv_text: str,
        job_posting_text: str,
        cv_keywords: str,
        job_keywords: str,
        current_cosine_similarity: float
    ) -> str:
        """Format CV enhancement prompt."""
        return self.cv_enhance_prompt.format(
            cvTemplate=cv_template,
            cvText=cv_text,
            jobPostingText=job_posting_text,
            cvKeywords=cv_keywords,
            jobKeywords=job_keywords,
            currentCosineSimilarity=current_cosine_similarity
        )

