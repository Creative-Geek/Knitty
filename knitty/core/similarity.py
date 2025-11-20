"""Similarity calculation using cosine similarity."""

import logging
import numpy as np
from .llm_clients import LLMClients

logger = logging.getLogger(__name__)


class SimilarityCalculator:
    """Calculates cosine similarity between CV and job posting."""
    
    def __init__(self, llm_clients: LLMClients):
        """Initialize similarity calculator."""
        self.llm_clients = llm_clients
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for text."""
        try:
            embedding_vector = self.llm_clients.embed_llm.embed_query(text)
            return np.array(embedding_vector)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise ValueError(f"Failed to generate embedding: {e}")
    
    def cosine_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            dot_product = np.dot(vector_a, vector_b)
            norm_a = np.linalg.norm(vector_a)
            norm_b = np.linalg.norm(vector_b)
            
            if norm_a == 0 or norm_b == 0:
                logger.warning("Zero vector norm detected")
                return 0.0
            
            similarity = dot_product / (norm_a * norm_b)
            logger.info(f"Calculated cosine similarity: {similarity:.6f}")
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            raise ValueError(f"Failed to calculate similarity: {e}")
    
    def calculate_similarity(self, text_a: str, text_b: str) -> float:
        """Calculate similarity between two texts."""
        embedding_a = self.embed_text(text_a)
        embedding_b = self.embed_text(text_b)
        return self.cosine_similarity(embedding_a, embedding_b)

