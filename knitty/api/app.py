"""FastAPI application setup and routes."""

import logging
import tempfile
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ..core.pipeline import EnhancementPipeline
from ..config.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancementRequest(BaseModel):
    """Request model for CV enhancement."""
    job_posting_url: Optional[str] = Field(None, description="URL to job posting")
    job_posting_text: Optional[str] = Field(None, description="Direct job posting text")
    additional_info: Optional[str] = Field(None, description="Additional CV information")


class EnhancementResponse(BaseModel):
    """Response model for CV enhancement."""
    enhanced_cv: str = Field(..., description="Enhanced CV in markdown format")
    baseline_similarity: float = Field(..., description="Initial similarity score")
    final_similarity: float = Field(..., description="Final similarity score after enhancement")
    improvement: float = Field(..., description="Improvement in similarity")
    cv_keywords: str = Field(..., description="Extracted CV keywords")
    job_keywords: str = Field(..., description="Extracted job keywords")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Knitty API",
        description="An intelligent CV tailoring system that optimizes resumes for specific job postings",
        version="0.1.0",
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize pipeline
    pipeline = EnhancementPipeline()
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "knitty"}
    
    @app.post("/api/v1/enhance-cv", response_model=EnhancementResponse)
    async def enhance_cv(
        background_tasks: BackgroundTasks,
        cv_file: UploadFile = File(..., description="CV PDF file"),
        job_posting_url: Optional[str] = None,
        job_posting_text: Optional[str] = None,
        additional_info: Optional[str] = None,
    ):
        """
        Enhance CV to better match job posting.
        
        Requires either job_posting_url or job_posting_text.
        """
        try:
            # Validate input
            if not job_posting_url and not job_posting_text:
                raise HTTPException(
                    status_code=400,
                    detail="Either job_posting_url or job_posting_text must be provided"
                )
            
            if cv_file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=400,
                    detail="File must be a PDF"
                )
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                content = await cv_file.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                # Process enhancement
                result = await pipeline.process(
                    cv_pdf_path=tmp_path,
                    job_posting_url=job_posting_url,
                    job_posting_text=job_posting_text,
                    additional_info=additional_info
                )
                
                return EnhancementResponse(
                    enhanced_cv=result["enhanced_cv"],
                    baseline_similarity=result["baseline_similarity"],
                    final_similarity=result["final_similarity"],
                    improvement=result["improvement"],
                    cv_keywords=result["cv_keywords"],
                    job_keywords=result["job_keywords"],
                )
            finally:
                # Clean up temporary file
                background_tasks.add_task(lambda: Path(tmp_path).unlink(missing_ok=True))
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Error enhancing CV: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    @app.post("/api/v1/extract-keywords")
    async def extract_keywords(
        cv_file: UploadFile = File(..., description="CV PDF file"),
    ):
        """Extract keywords from CV."""
        try:
            if cv_file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="File must be a PDF")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                content = await cv_file.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                cv_raw_text = pipeline.cv_processor.extract_text_from_pdf(tmp_path)
                cv_text = pipeline.cv_processor.combine_cv_content(cv_raw_text)
                keywords = pipeline.cv_processor.extract_keywords(cv_text)
                
                return {"keywords": keywords}
            finally:
                Path(tmp_path).unlink(missing_ok=True)
        
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    class SimilarityRequest(BaseModel):
        """Request model for similarity calculation."""
        text_a: str = Field(..., description="First text")
        text_b: str = Field(..., description="Second text")
    
    @app.post("/api/v1/calculate-similarity")
    async def calculate_similarity(request: SimilarityRequest):
        """Calculate cosine similarity between two texts."""
        try:
            similarity = pipeline.similarity_calculator.calculate_similarity(
                request.text_a, request.text_b
            )
            return {"similarity": similarity}
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

