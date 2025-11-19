"""Pytest configuration and fixtures."""

import pytest
import os
from unittest.mock import Mock
from knitty.config.settings import Settings


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    return Settings(
        fast_llm_api_key="test-fast-key",
        fast_llm_api_base="https://test-fast.com",
        fast_llm_model_name="test-fast-model",
        smart_llm_api_key="test-smart-key",
        smart_llm_api_base="https://test-smart.com",
        smart_llm_model_name="test-smart-model",
        embed_llm_api_key="test-embed-key",
        embed_llm_api_base="https://test-embed.com",
        embed_llm_model_name="test-embed-model",
    )

