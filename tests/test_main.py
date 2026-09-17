"""Tests for my_project module and backplane contract validation."""

import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest
from scripts.validate_run_contract import (
    INGEST_SCHEMA_FILES,
    _self_smoke,
    validate_envelope,
)

from my_project import __version__, add, greet

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "docs" / "contracts" / "schemas"
REGISTRY_PATH = REPO_ROOT / "config" / "backplane_participants.json"


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


def test_ingest_schema_files_includes_capability_bundle() -> None:
    """Consumer ingest map must include capability-bundle/v1."""
    assert "capability-bundle/v1" in INGEST_SCHEMA_FILES
    assert INGEST_SCHEMA_FILES["capability-bundle/v1"] == "capability-bundle-v1.schema.json"


def _capability_bundle_consumer_registry() -> dict[str, object]:
    return {
        "participants": [
            {
                "repo": "stranske/Ready",
                "role": "consumer",
                "status": "emitting",
                "ingests": ["capability-bundle/v1"],
            }
        ]
    }


def _valid_capability_bundle() -> dict[str, object]:
    return {
        "schema_version": "capability-bundle/v1",
        "capability_id": "test.capability",
        "version": "1",
        "content_hash": ("sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
        "selector": {},
        "owner": "test-owner",
        "fragments": {"task": "validate capability-bundle consumer path"},
        "gates": ["gate1"],
        "rollback": "revert",
    }


def test_validate_envelope_accepts_valid_capability_bundle_consumer() -> None:
    """Consumer path must accept a schema-valid capability-bundle document."""
    report = validate_envelope(
        envelope=_valid_capability_bundle(),
        schema_dir=SCHEMA_DIR,
        registry=_capability_bundle_consumer_registry(),
        repo="stranske/Ready",
        manifest=None,
    )
    assert report.conformant
    assert not report.skipped
    assert report.role == "consumer"


def test_validate_envelope_rejects_invalid_capability_bundle_consumer() -> None:
    """Consumer path must reject capability-bundle documents missing required fields."""
    invalid = _valid_capability_bundle()
    del invalid["content_hash"]
    report = validate_envelope(
        envelope=invalid,
        schema_dir=SCHEMA_DIR,
        registry=_capability_bundle_consumer_registry(),
        repo="stranske/Ready",
        manifest=None,
    )
    assert not report.conformant
    assert report.violations


def test_self_smoke_validates_all_schema_files(capsys: pytest.CaptureFixture[str]) -> None:
    """Self-smoke must load every bundled Draft 2020-12 schema."""
    expected = sorted(p.name for p in SCHEMA_DIR.glob("*.schema.json"))
    assert expected, "expected at least one schema under docs/contracts/schemas"
    assert _self_smoke(SCHEMA_DIR, REGISTRY_PATH) == 0
    prefix = "PASS schema loads + valid Draft202012: "
    validated = [
        line.removeprefix(prefix)
        for line in capsys.readouterr().out.splitlines()
        if line.startswith(prefix)
    ]
    assert validated == expected


def test_self_smoke_fails_when_schema_dir_empty(tmp_path: Path) -> None:
    """Self-smoke must fail when no bundled schemas are present."""
    empty_dir = tmp_path / "schemas"
    empty_dir.mkdir()
    assert _self_smoke(empty_dir, REGISTRY_PATH) == 1


def test_ingest_schema_files_requires_capability_bundle_mapping() -> None:
    """Deliberate-break guard: capability-bundle mapping is required."""
    assert "capability-bundle/v1" in INGEST_SCHEMA_FILES


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


@pytest.mark.parametrize(
    "score",
    [float("nan"), float("inf"), float("-inf")],
)
def test_format_similarity_non_finite_scores_return_safe_fallback(score: float) -> None:
    """Non-finite similarity scores must not crash duplicate-comment formatting."""
    from scripts.langchain.issue_dedup import _format_similarity

    assert _format_similarity(score) == "0%"


@pytest.mark.parametrize(
    "raw",
    ["nan", "inf", "-inf", "NaN", "INF"],
)
def test_verdict_policy_coerce_confidence_rejects_non_finite_strings(raw: str) -> None:
    """Non-finite confidence strings must clamp to 0.0 before policy evaluation."""
    from scripts.langchain.verdict_policy import _coerce_confidence

    assert _coerce_confidence(raw) == 0.0


@pytest.mark.parametrize(
    "value",
    [float("nan"), float("inf"), float("-inf")],
)
def test_verdict_policy_normalize_confidence_rejects_non_finite_floats(value: float) -> None:
    """Non-finite confidence floats must clamp to 0.0 before threshold checks."""
    from scripts.langchain.verdict_policy import _normalize_confidence

    assert _normalize_confidence(value) == 0.0


def test_verdict_policy_split_pass_concerns_with_inf_confidence_does_not_trigger_human() -> None:
    """Split pass/concerns with infinite concerns confidence must clamp before threshold check."""
    from scripts.langchain.verdict_policy import ProviderVerdict, evaluate_verdict_policy

    verdicts = [
        ProviderVerdict(provider="a", model="m1", verdict="pass", confidence=0.9),
        ProviderVerdict(provider="b", model="m2", verdict="concerns", confidence=float("inf")),
    ]
    result = evaluate_verdict_policy(verdicts)
    assert result.split_verdict is True
    assert result.concerns_confidence == 0.0
    assert result.needs_human is False


def test_ci_failure_triage_playbook_urls_resolve_to_existing_docs() -> None:
    """All DEFAULT_TRIAGE_PATTERNS playbook_url paths must exist under docs/."""
    from tools.ci_failure_triage import DEFAULT_TRIAGE_PATTERNS

    repo_root = Path(__file__).resolve().parents[1]
    for pattern in DEFAULT_TRIAGE_PATTERNS:
        if not pattern.playbook_url:
            continue
        doc_path = pattern.playbook_url.split("#", 1)[0]
        assert (repo_root / doc_path).is_file(), (
            f"{pattern.error_type} playbook_url {pattern.playbook_url!r} missing file {doc_path}"
        )
