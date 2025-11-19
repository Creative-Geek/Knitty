"""Tests for CV processor."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from knitty.core.cv_processor import CVProcessor


@pytest.fixture
def mock_llm_clients():
    """Create mock LLM clients."""
    clients = Mock()
    clients.fast_llm = Mock()
    response = Mock()
    response.content = '["Python", "React", "Node.js"]'
    clients.fast_llm.invoke = Mock(return_value=response)
    return clients


@pytest.fixture
def mock_prompt_manager():
    """Create mock prompt manager."""
    manager = Mock()
    manager.format_cv_keywords_prompt = Mock(return_value="Extract keywords from: {cvText}")
    return manager


@pytest.fixture
def cv_processor(mock_llm_clients, mock_prompt_manager):
    """Create CV processor instance."""
    return CVProcessor(mock_llm_clients, mock_prompt_manager)


def test_combine_cv_content_with_additional_info(cv_processor):
    """Test combining CV with additional info."""
    cv_text = "Original CV text"
    additional = "Additional information"
    
    result = cv_processor.combine_cv_content(cv_text, additional)
    assert "Original CV text" in result
    assert "Additional information" in result


def test_combine_cv_content_without_additional_info(cv_processor):
    """Test combining CV without additional info."""
    cv_text = "Original CV text"
    result = cv_processor.combine_cv_content(cv_text, None)
    assert result == cv_text


def test_extract_keywords(cv_processor, mock_llm_clients):
    """Test keyword extraction."""
    cv_text = "Python developer with React experience"
    keywords = cv_processor.extract_keywords(cv_text)
    
    assert isinstance(keywords, str)
    mock_llm_clients.fast_llm.invoke.assert_called_once()

