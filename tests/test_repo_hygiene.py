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


def _git_ignore_pattern(rule: str) -> str:
    """Extract the matched pattern from ``git check-ignore -v`` output."""
    source, _separator, _path = rule.partition("\t")
    return source.rsplit(":", 1)[-1]


def test_generated_distribution_metadata_untracked_and_ignored() -> None:
    """Editable installs must not commit stale dependency metadata."""
    tracked = _git_ls_files(":(glob)**/*.egg-info/**")
    assert not tracked, (
        "*.egg-info/ is generated from pyproject.toml and must not be tracked; "
        f"found {len(tracked)} path(s): {tracked[:3]}"
    )

    probe = "src/install-probe.egg-info/PKG-INFO"
    rule = _git_ignore_rule(probe)
    assert rule, "*.egg-info/ must stay ignored so editable installs cannot dirty the tree."
    assert (
        _git_ignore_pattern(rule) == "*.egg-info/"
    ), "Generated distribution metadata must be covered by the canonical directory rule."


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
    assert root_rule and root_rule.startswith(
        ".gitignore:"
    ), "Root node_modules/ must be ignored by the repository .gitignore."
    assert _git_ignore_pattern(root_rule) in {"/node_modules/", "node_modules/"}, (
        "Root node_modules/ must be ignored by a directory rule; the synced template may "
        "use the broad form when it also explicitly preserves vendored workflow dependencies."
    )

    vendored_rule = _git_ignore_rule(".github/scripts/node_modules/minimatch/package.json")
    assert vendored_rule is None or _git_ignore_pattern(vendored_rule).startswith("!"), (
        "Vendored .github/scripts/node_modules/ must be unignored; verbose check-ignore "
        "may report the negation rule that preserves it."
    )
