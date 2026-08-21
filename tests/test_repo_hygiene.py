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


def _git_ignore_rule(path: str) -> str | None:
    result = subprocess.run(
        ["git", "check-ignore", "-v", "--no-index", "--", path],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or None


def test_generated_dirs_untracked_and_vendored_preserved() -> None:
    """Root node_modules/ and __pycache__ stay untracked; vendored scripts tree remains."""
    root_node_modules = _git_ls_files("node_modules")
    assert not root_node_modules, (
        "Root node_modules/ must not be tracked. "
        f"Found {len(root_node_modules)} path(s); first: {root_node_modules[:1]}"
    )

    for generated_dir in ("src/my_project/__pycache__", "tests/__pycache__"):
        assert not _git_ls_files(
            generated_dir
        ), f"{generated_dir}/ must not be tracked once ignored bootstrap residue is removed."
        assert _git_ignore_rule(
            f"{generated_dir}/probe.py"
        ), f"{generated_dir}/ must stay ignored so cleaned bytecode cannot return."

    for generated_file in ("module.pyc", "module.pyo", "module.pyd"):
        assert _git_ignore_rule(generated_file), f"{generated_file} must stay ignored."

    vendored = _git_ls_files(".github/scripts/node_modules")
    assert vendored, ".github/scripts/node_modules/ must remain tracked for workflow script deps."

    root_rule = _git_ignore_rule("node_modules/probe.js")
    assert (
        root_rule and root_rule.startswith(".gitignore:") and "/node_modules/\t" in root_rule
    ), "Root node_modules/ must be ignored specifically by .gitignore's /node_modules/ rule."

    assert not _git_ignore_rule(
        ".github/scripts/node_modules/minimatch/package.json"
    ), "Vendored .github/scripts/node_modules/ must not match the root-anchored ignore rule."
