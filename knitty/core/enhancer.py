"""CV enhancement using Smart LLM."""

import logging
from typing import Optional
from ..config.prompts import PromptManager
from .llm_clients import LLMClients
from .similarity import SimilarityCalculator

logger = logging.getLogger(__name__)


class CVEnhancer:
    """Enhances CV to better match job posting."""
    
    def __init__(
        self,
        llm_clients: LLMClients,
        prompt_manager: PromptManager,
        similarity_calculator: SimilarityCalculator
    ):
        """Initialize CV enhancer."""
        self.llm_clients = llm_clients
        self.prompt_manager = prompt_manager
        self.similarity_calculator = similarity_calculator
    
    def generate_enhanced_cv(
        self,
        cv_template: str,
        cv_text: str,
        job_posting_text: str,
        cv_keywords: str,
        job_keywords: str,
        current_similarity: float
    ) -> str:
        """Generate enhanced CV."""
        try:
            prompt = self.prompt_manager.format_cv_enhance_prompt(
                cv_template=cv_template,
                cv_text=cv_text,
                job_posting_text=job_posting_text,
                cv_keywords=cv_keywords,
                job_keywords=job_keywords,
                current_cosine_similarity=current_similarity
            )
            
            response = self.llm_clients.smart_llm.invoke([("human", prompt)])
            enhanced_cv = response.content.strip()
            
            logger.info("Generated enhanced CV")
            return enhanced_cv
        except Exception as e:
            logger.error(f"Error generating enhanced CV: {e}")
            raise ValueError(f"Failed to generate enhanced CV: {e}")
    
    def enhance_with_retry(
        self,
        cv_template: str,
        cv_text: str,
        job_posting_text: str,
        cv_keywords: str,
        job_keywords: str,
        current_similarity: float,
        job_keywords_text: str,
        max_retries: int = 3
    ) -> tuple[str, float]:
        """Enhance CV with iterative improvement."""
        enhanced_cv = self.generate_enhanced_cv(
            cv_template, cv_text, job_posting_text,
            cv_keywords, job_keywords, current_similarity
        )
        
        # Calculate new similarity
        new_similarity = self.similarity_calculator.calculate_similarity(
            enhanced_cv, job_keywords_text
        )
        
        logger.info(f"Initial enhancement similarity: {new_similarity:.6f} (baseline: {current_similarity:.6f})")
        
        # Retry if no improvement
        if new_similarity <= current_similarity and max_retries > 0:
            logger.info("No improvement detected, retrying with feedback...")
            
            similarity_string = (
                f"New Cosine Similarity: {new_similarity:.6f}; "
                f"Improvement over previous: {float(new_similarity - current_similarity):+.6f}"
            )
            
            prompt = self.prompt_manager.format_cv_enhance_prompt(
                cv_template, cv_text, job_posting_text,
                cv_keywords, job_keywords, current_similarity
            )
            
            messages = [
                ("human", prompt),
                ("assistant", enhanced_cv),
                ("human", similarity_string),
            ]
            
            response = self.llm_clients.smart_llm.invoke(messages)
            enhanced_cv = response.content.strip()
            
            # Recalculate similarity
            new_similarity = self.similarity_calculator.calculate_similarity(
                enhanced_cv, job_keywords_text
            )
            
            logger.info(f"Retry enhancement similarity: {new_similarity:.6f}")
        
        improvement = new_similarity - current_similarity
        logger.info(f"Final similarity: {new_similarity:.6f}, Improvement: {improvement:+.6f}")
        
        return enhanced_cv, new_similarity

