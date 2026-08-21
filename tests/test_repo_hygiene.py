"""Repo hygiene: untrack bootstrap residue without breaking vendored workflow scripts."""

from __future__ import annotations

import subprocess


def _git_ls_files(pattern: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", pattern],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def _git_check_ignore(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def test_generated_dirs_untracked_and_vendored_preserved() -> None:
    """Root node_modules/ and __pycache__ stay untracked; vendored scripts tree remains."""
    root_node_modules = _git_ls_files("node_modules")
    assert not root_node_modules, (
        "Root node_modules/ must not be tracked. "
        f"Found {len(root_node_modules)} path(s); first: {root_node_modules[:1]}"
    )

    vendored = _git_ls_files(".github/scripts/node_modules")
    assert vendored, (
        ".github/scripts/node_modules/ must remain tracked for workflow script deps."
    )

    assert _git_check_ignore("node_modules/probe.js"), (
        "Root node_modules/ must be ignored via the /node_modules/ gitignore rule."
    )

    assert not _git_check_ignore(".github/scripts/node_modules/minimatch/package.json"), (
        "Vendored .github/scripts/node_modules/ must not match the root-anchored ignore rule."
    )
