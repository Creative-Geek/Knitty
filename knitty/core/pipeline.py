"""Main processing pipeline that orchestrates all components."""

import json
import logging
from typing import Optional, Dict, Any
from ..config.settings import Settings, get_settings
from ..config.prompts import PromptManager
from .llm_clients import LLMClients
from .cv_processor import CVProcessor
from .job_processor import JobProcessor
from .similarity import SimilarityCalculator
from .enhancer import CVEnhancer

logger = logging.getLogger(__name__)


class EnhancementPipeline:
    """Main pipeline for CV enhancement."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize pipeline with settings."""
        self.settings = settings or get_settings()
        self.prompt_manager = PromptManager(self.settings.config_dir)
        self.llm_clients = LLMClients(self.settings)
        self.cv_processor = CVProcessor(self.llm_clients, self.prompt_manager)
        self.job_processor = JobProcessor(
            self.llm_clients, self.prompt_manager, self.settings
        )
        self.similarity_calculator = SimilarityCalculator(self.llm_clients)
        self.enhancer = CVEnhancer(
            self.llm_clients, self.prompt_manager, self.similarity_calculator
        )
    
    async def process(
        self,
        cv_pdf_path: str,
        job_posting_url: Optional[str] = None,
        job_posting_text: Optional[str] = None,
        additional_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process CV enhancement pipeline.
        
        Args:
            cv_pdf_path: Path to CV PDF file
            job_posting_url: Optional URL to job posting
            job_posting_text: Optional direct job posting text
            additional_info: Optional additional CV information
        
        Returns:
            Dictionary with enhanced CV and metrics
        """
        try:
            # Step 1: Process CV
            logger.info("Step 1: Processing CV...")
            cv_raw_text = self.cv_processor.extract_text_from_pdf(cv_pdf_path)
            cv_text = self.cv_processor.combine_cv_content(cv_raw_text, additional_info)
            cv_keywords = self.cv_processor.extract_keywords(cv_text)
            
            # Step 2: Process Job Posting
            logger.info("Step 2: Processing job posting...")
            if job_posting_url:
                job_posting_data = await self.job_processor.extract_job_posting_from_url(
                    job_posting_url
                )
                # Convert to string if it's a dict
                if isinstance(job_posting_data, dict):
                    job_posting_text = json.dumps(job_posting_data, indent=2)
                else:
                    job_posting_text = str(job_posting_data)
            elif job_posting_text:
                pass  # Use provided text
            else:
                raise ValueError("Either job_posting_url or job_posting_text must be provided")
            
            job_keywords = self.job_processor.extract_keywords(job_posting_text)
            
            # Step 3: Calculate baseline similarity
            logger.info("Step 3: Calculating baseline similarity...")
            baseline_similarity = self.similarity_calculator.calculate_similarity(
                cv_raw_text, job_keywords
            )
            
            # Step 4: Enhance CV
            logger.info("Step 4: Enhancing CV...")
            enhanced_cv, final_similarity = self.enhancer.enhance_with_retry(
                cv_template=self.prompt_manager.cv_template,
                cv_text=cv_text,
                job_posting_text=job_posting_text,
                cv_keywords=cv_keywords,
                job_keywords=job_keywords,
                current_similarity=baseline_similarity,
                job_keywords_text=job_keywords,
                max_retries=self.settings.max_retries
            )
            
            improvement = final_similarity - baseline_similarity
            
            result = {
                "enhanced_cv": enhanced_cv,
                "baseline_similarity": baseline_similarity,
                "final_similarity": final_similarity,
                "improvement": improvement,
                "cv_keywords": cv_keywords,
                "job_keywords": job_keywords,
            }
            
            logger.info("Pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            raise

