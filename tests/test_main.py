"""Tests for my_project module."""

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

    assert len(response.vectors) == 4
    assert all(len(vector) == response.metadata.dimensions for vector in response.vectors)
    assert response.vectors[0] != response.vectors[2]
    assert response.vectors[1] == [0.0] * response.metadata.dimensions
    assert response.vectors[3] == [0.0] * response.metadata.dimensions


def test_local_fallback_embedding_all_empty_inputs_stay_aligned() -> None:
    from tools.embedding_provider import LocalFallbackEmbeddingProvider

    provider = LocalFallbackEmbeddingProvider()
    response = provider.embed(["", " "])

    assert len(response.vectors) == 2
    assert all(vector == [0.0] * response.metadata.dimensions for vector in response.vectors)
