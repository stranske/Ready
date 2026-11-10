"""Ensure the lock file captures every dependency declared in pyproject.toml."""

from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path

import pytest

_OPERATORS = ("==", ">=", "<=", "~=", "!=", ">", "<", "===")


def _split_spec(raw: str) -> str:
    entry = raw.strip().strip(",").strip('"')
    for operator in _OPERATORS:
        if operator in entry:
            name, _ = entry.split(operator, 1)
            return name.strip().split("[")[0]
    return entry.strip().split("[")[0]


def _load_lock_versions(path: Path) -> dict[str, str]:
    versions: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("--"):
            continue
        if "==" not in stripped:
            continue
        name, version = stripped.split("==", 1)
        versions[name.lower()] = version
    return versions


def test_all_pyproject_dependencies_are_in_lock() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject.get("project", {})

    declared = set()
    for entry in project.get("dependencies", []):
        declared.add(_split_spec(entry).lower())

    for group in project.get("optional-dependencies", {}).values():
        for entry in group:
            declared.add(_split_spec(entry).lower())

    lock_versions = _load_lock_versions(Path("requirements.lock"))

    missing = []
    for dependency in sorted(declared):
        normalised = dependency.replace("-", "_")
        if dependency not in lock_versions and normalised not in lock_versions:
            missing.append(dependency)

    assert not missing, "requirements.lock is missing pinned versions for: " + ", ".join(missing)


def test_setuptools_build_requirement_matches_restored_floor() -> None:
    """Catch a repeat of the setuptools build floor regression from PR #638."""
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    assert pyproject["build-system"]["requires"] == ["setuptools>=82.0.1", "wheel"]


@pytest.mark.parametrize("regressed", [False, True])
def test_setuptools_verification_command(tmp_path: Path, regressed: bool) -> None:
    """The acceptance command must reject the previous build requirement."""
    source = Path(__file__).resolve().parents[1] / "pyproject.toml"
    contents = source.read_text(encoding="utf-8")
    if regressed:
        assert "setuptools>=82.0.1" in contents
        contents = contents.replace("setuptools>=82.0.1", "setuptools>=69.0.0")
    (tmp_path / "pyproject.toml").write_text(contents, encoding="utf-8")

    result = subprocess.run(
        ["grep", "-n", "setuptools>=82.0.1", "pyproject.toml"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == (1 if regressed else 0)
    expected = "" if regressed else '2:requires = ["setuptools>=82.0.1", "wheel"]\n'
    assert result.stdout == expected
    assert result.stderr == ""
