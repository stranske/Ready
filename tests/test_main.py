"""Tests for my_project module and backplane contract validation."""

from pathlib import Path

import pytest
from scripts.validate_run_contract import INGEST_SCHEMA_FILES, _self_smoke

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
