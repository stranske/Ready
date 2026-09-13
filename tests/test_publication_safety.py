"""Exercise the publication guard through its dependency-free command line."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/check_publication_safety.py"


def run_guard(root):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    ("content", "rule"),
    [
        ("/Users/example/file", "home-path"),
        *[
            (prefix + "SENSITIVE_SENTINEL", "credential")
            for prefix in ("sk-ant-", "sk-proj-", "ghp_", "github_pat_", "lsv2_", "crsr_", "AIza")
        ],
        ("-----BEGIN RSA PRIVATE KEY-----", "private-key"),
        ("-----BEGIN OPENSSH PRIVATE KEY-----", "private-key"),
        ("clones/Repo/file.py", "scratch-path"),
        ("/private/tmp/draft", "scratch-path"),
        ("scratchpad/notes", "scratch-path"),
        ("worker.local:8080", "internal-host"),
        ("http://localhost:8000/", "internal-host"),
    ],
)
def test_each_rule_reports_location_without_content(tmp_path, content, rule):
    (tmp_path / "report.bin").write_bytes(b"\xff\x00first line\n" + content.encode())
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert f"report.bin:2: {rule}" in result.stdout
    assert "files_scanned=1" in result.stdout
    assert content not in result.stdout
    assert "SENSITIVE_SENTINEL" not in result.stdout + result.stderr


def test_all_hits_and_rule_totals_are_reported(tmp_path):
    (tmp_path / "one").write_text("ghp_fake ghp_fake\nclones/project\n")
    (tmp_path / "two").write_text("localhost:8000\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    for expected in (
        "one:1: credential (2 hit(s))",
        "one:2: scratch-path",
        "two:1: internal-host",
        "files_scanned=2",
        "credential=2",
        "home-path=0",
        "private-key=0",
    ):
        assert expected in result.stdout


def test_clean_tree_and_zeros(tmp_path):
    (tmp_path / "report.md").write_text("Public research report.\n")
    result = run_guard(tmp_path)
    assert result.returncode == 0
    for expected in (
        "files_scanned=1",
        "home-path=0",
        "credential=0",
        "private-key=0",
        "scratch-path=0",
        "internal-host=0",
        "errors=0",
    ):
        assert expected in result.stdout


@pytest.mark.parametrize("missing", [False, True])
def test_empty_or_missing_tree_fails(tmp_path, missing):
    result = run_guard(tmp_path / "missing" if missing else tmp_path)
    assert result.returncode == 1
    assert "zero files scanned" in result.stdout


def test_allowlist_is_exact_and_rule_specific(tmp_path):
    (tmp_path / "fixture").write_text("ghp_synthetic\n")
    (tmp_path / ".publication-allow").write_text(
        "fixture:credential # Synthetic scanner regression example.\n"
    )
    result = run_guard(tmp_path)
    assert result.returncode == 0
    assert "allowed_hits=1" in result.stdout
    (tmp_path / "fixture").write_text("ghp_synthetic\nclones/example\n")
    (tmp_path / "other").write_text("ghp_synthetic\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "fixture:2: scratch-path" in result.stdout
    assert "other:1: credential" in result.stdout


@pytest.mark.parametrize(
    "entry",
    [
        "fixture:credential",
        "fixture:credential # ",
        "fixture:unknown # reason",
        "../fixture:credential # reason",
        "/fixture:credential # reason",
        "*:credential # reason",
        "missing:credential # reason",
    ],
)
def test_invalid_allowlist_fails(tmp_path, entry):
    (tmp_path / "fixture").write_text("Public content\n")
    (tmp_path / ".publication-allow").write_text(entry + "\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "ERROR: .publication-allow:1:" in result.stdout


def test_allowlist_itself_is_scanned(tmp_path):
    (tmp_path / "fixture").write_text("Public content\n")
    (tmp_path / ".publication-allow").write_text("fixture:credential # ghp_synthetic\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert ".publication-allow:1: credential" in result.stdout


@pytest.mark.parametrize("directory", [False, True])
def test_symlinks_cannot_hide_or_import_content(tmp_path, directory):
    root = tmp_path / "research"
    root.mkdir()
    target = tmp_path / "outside"
    if directory:
        target.mkdir()
    else:
        target.write_text("Public content")
    (root / "link").symlink_to(target, target_is_directory=directory)
    result = run_guard(root)
    assert result.returncode == 1
    assert "symlinks are not allowed" in result.stdout


@pytest.mark.parametrize(
    "result,expected",
    [
        ("success", "success"),
        ("failure", "failure"),
        ("cancelled", "failure"),
        ("skipped", "failure"),
    ],
)
def test_gate_summary_enforces_publication_even_when_python_skips(tmp_path, result, expected):
    # Execute the actual Gate aggregation script; no duplication of its logic.
    workflow = (REPO / ".github/workflows/pr-00-gate.yml").read_text()
    block = workflow.split("      - name: Summarize results\n", 1)[1]
    block = block.split("        run: |\n", 1)[1].split("\n      - name:", 1)[0]
    script = "\n".join(line[10:] for line in block.splitlines())
    output = tmp_path / "output"
    env = {
        **os.environ,
        "GITHUB_OUTPUT": str(output),
        "DETECT_RESULT": "success",
        "PYTHON_RESULT": "skipped",
        "PUBLICATION_RESULT": result,
    }
    subprocess.run(["bash", "-c", script], env=env, check=True, capture_output=True)
    assert f"state={expected}\n" in output.read_text()
    assert "needs: [detect, python-ci, publication-safety]" in workflow
