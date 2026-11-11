"""The build-system setuptools floor is 82.0.1, matching the fleet standard.

#638 lowered it to >=69.0.0 and later syncs did not restore it; no automated
writer owns this line, so this guard fails if it drifts below the floor again.
"""

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FLOOR = (82, 0, 1)
SETUPTOOLS_REQUIREMENT = re.compile(r"setuptools\s*>=\s*(\d+)\.(\d+)\.(\d+)")


def _assert_build_requires(requires: list[object]) -> None:
    entries = [str(entry).strip() for entry in requires]
    assert "wheel" in entries, f"build requires must include 'wheel': {entries}"
    setuptools = [entry for entry in entries if entry.startswith("setuptools")]
    assert len(setuptools) == 1, f"expected one setuptools requirement: {entries}"
    match = SETUPTOOLS_REQUIREMENT.fullmatch(setuptools[0])
    assert match, f"setuptools must use a >= floor, got {setuptools[0]!r}"
    version = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    assert version >= FLOOR, f"setuptools floor {version} is below {FLOOR}"


def test_build_system_requires_setuptools_floor() -> None:
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    build_system = config["build-system"]
    assert build_system["build-backend"] == "setuptools.build_meta"
    _assert_build_requires(build_system["requires"])
    # Pin the exact restored line the acceptance grep checks for.
    assert build_system["requires"] == ["setuptools>=82.0.1", "wheel"]


@pytest.mark.parametrize(
    "requires,accepted",
    [
        (["setuptools>=82.0.1", "wheel"], True),
        (["setuptools>=84.2.1", "wheel"], True),
        (["setuptools>=69.0.0", "wheel"], False),
        (["setuptools>=82.0.0", "wheel"], False),
        (["setuptools==82.0.1", "wheel"], False),
        (["setuptools>=82.0.1"], False),
        (["wheel"], False),
        (["setuptools>=82.0.1", "setuptools>=82.0.1", "wheel"], False),
    ],
)
def test_build_requires_bounds(requires: list[str], accepted: bool) -> None:
    if accepted:
        _assert_build_requires(requires)
    else:
        with pytest.raises(AssertionError):
            _assert_build_requires(requires)
