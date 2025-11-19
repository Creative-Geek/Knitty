"""Tests for similarity calculation."""

import pytest
import numpy as np
from unittest.mock import Mock, MagicMock
from knitty.core.similarity import SimilarityCalculator


@pytest.fixture
def mock_llm_clients():
    """Create mock LLM clients."""
    clients = Mock()
    clients.embed_llm = Mock()
    clients.embed_llm.embed_query = Mock(return_value=np.random.rand(3072).tolist())
    return clients


@pytest.fixture
def similarity_calculator(mock_llm_clients):
    """Create similarity calculator instance."""
    return SimilarityCalculator(mock_llm_clients)


def test_cosine_similarity_identical(similarity_calculator):
    """Test cosine similarity with identical vectors."""
    vector = np.array([1.0, 0.0, 0.0])
    result = similarity_calculator.cosine_similarity(vector, vector)
    assert result == pytest.approx(1.0)


def test_cosine_similarity_orthogonal(similarity_calculator):
    """Test cosine similarity with orthogonal vectors."""
    vector_a = np.array([1.0, 0.0, 0.0])
    vector_b = np.array([0.0, 1.0, 0.0])
    result = similarity_calculator.cosine_similarity(vector_a, vector_b)
    assert result == pytest.approx(0.0)


def test_embed_text(similarity_calculator, mock_llm_clients):
    """Test text embedding."""
    text = "test text"
    embedding = similarity_calculator.embed_text(text)
    assert isinstance(embedding, np.ndarray)
    mock_llm_clients.embed_llm.embed_query.assert_called_once_with(text)


def test_calculate_similarity(similarity_calculator, mock_llm_clients):
    """Test similarity calculation between texts."""
    text_a = "Python developer"
    text_b = "Software engineer"
    
    # Mock embeddings
    mock_llm_clients.embed_llm.embed_query.side_effect = [
        np.random.rand(3072).tolist(),
        np.random.rand(3072).tolist()
    ]
    
    result = similarity_calculator.calculate_similarity(text_a, text_b)
    assert isinstance(result, float)
    assert -1.0 <= result <= 1.0

