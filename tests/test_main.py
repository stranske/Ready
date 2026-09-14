"""Tests for my_project module."""

import sys
from types import ModuleType
from unittest.mock import Mock

import pytest

from my_project import __version__, add, greet


def test_version() -> None:
    """Version should be a string."""
    assert isinstance(__version__, str)
    assert __version__ == "0.1.0"


def test_greet() -> None:
    """Greet should return proper greeting."""
    assert greet("World") == "Hello, World!"
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty() -> None:
    """Greet should handle empty string."""
    assert greet("") == "Hello, !"


def test_add() -> None:
    """Add should return sum of two numbers."""
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0


def test_add_negative() -> None:
    """Add should handle negative numbers."""
    assert add(-5, -3) == -8
    assert add(-10, 5) == -5


def test_local_fallback_embedding_preserves_empty_string_positions() -> None:
    """Empty and whitespace-only inputs keep index-aligned vectors."""
    from tools.embedding_provider import LocalFallbackEmbeddingProvider

    provider = LocalFallbackEmbeddingProvider()
    response = provider.embed(["a", "", "b", "   "])

    dimensions = response.metadata.dimensions
    assert dimensions is not None
    assert len(response.vectors) == 4
    assert all(len(vector) == dimensions for vector in response.vectors)
    assert response.vectors[0] != response.vectors[2]
    assert response.vectors[1] == [0.0] * dimensions
    assert response.vectors[3] == [0.0] * dimensions


def test_local_fallback_embedding_all_empty_inputs_stay_aligned() -> None:
    from tools.embedding_provider import LocalFallbackEmbeddingProvider

    provider = LocalFallbackEmbeddingProvider()
    response = provider.embed(["", " "])

    dimensions = response.metadata.dimensions
    assert dimensions is not None
    assert len(response.vectors) == 2
    assert all(vector == [0.0] * dimensions for vector in response.vectors)


def test_openai_embedding_preserves_blank_positions_and_normalization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reconstruct aligned vectors while retaining the existing text stripping."""
    from tools.embedding_provider import OpenAIEmbeddingProvider

    client = Mock()
    client.embed_documents.return_value = [[1.0, 2.0], [3.0, 4.0]]
    factory = Mock(return_value=client)
    sdk = ModuleType("langchain_openai")
    monkeypatch.setattr(sdk, "OpenAIEmbeddings", factory, raising=False)
    monkeypatch.setitem(sys.modules, "langchain_openai", sdk)
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-placeholder")

    response = OpenAIEmbeddingProvider().embed(iter(["", "  a  ", " \t", "b", ""]))

    client.embed_documents.assert_called_once_with(["a", "b"])
    assert response.vectors == [[0.0, 0.0], [1.0, 2.0], [0.0, 0.0], [3.0, 4.0], [0.0, 0.0]]
    assert response.metadata.dimensions == 2
    assert response.metadata.provider == "openai"
    assert not response.metadata.is_fallback


@pytest.mark.parametrize("texts", [["", " \t", "\n"], []])
def test_openai_embedding_all_blank_inputs_do_not_call_sdk(
    monkeypatch: pytest.MonkeyPatch, texts: list[str]
) -> None:
    """Blank-only input preserves slots without requiring credentials or the SDK."""
    from tools.embedding_provider import OpenAIEmbeddingProvider

    factory = Mock(side_effect=AssertionError("Blank inputs must not initialize the SDK"))
    sdk = ModuleType("langchain_openai")
    monkeypatch.setattr(sdk, "OpenAIEmbeddings", factory, raising=False)
    monkeypatch.setitem(sys.modules, "langchain_openai", sdk)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    response = OpenAIEmbeddingProvider().embed(iter(texts))

    factory.assert_not_called()
    assert response.vectors == [[] for _ in texts]
    assert response.metadata.dimensions is None
