"""Exercise the publication guard through its dependency-free command line."""

import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/check_publication_safety.py"


@pytest.fixture
def tmp_path(tmp_path):
    """Give each synthetic research tree its own repo-root allowlist directory."""
    root = tmp_path / "research"
    root.mkdir()
    return root


def allowlist_for(root: Path) -> Path:
    return root.parent / ".publication-allow"


def run_guard(root, allowlist=None):
    cmd = [sys.executable, str(SCRIPT), "--root", str(root)]
    if allowlist is not None:
        cmd.extend(["--allowlist", str(allowlist)])
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )


def load_scanner():
    return importlib.import_module("scripts.check_publication_safety")


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
    allowlist_for(tmp_path).write_text(
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


@pytest.mark.parametrize("reason", [" # Synthetic regression fixture.", "", " # "])
def test_explicit_allowlist_overrides_default_and_requires_reason(tmp_path, reason):
    (tmp_path / "fixture").write_text("clones/example\n")
    # A valid default must not mask an invalid explicitly selected allowlist.
    allowlist_for(tmp_path).write_text("fixture:scratch-path # Default fixture exception.\n")
    explicit = tmp_path.parent / "reviewed-allowlist"
    explicit.write_text(f"fixture:scratch-path{reason}\n")

    result = run_guard(tmp_path, explicit)

    assert "files_scanned=1" in result.stdout
    if reason.strip() == "# Synthetic regression fixture.":
        assert result.returncode == 0
        assert "allowed_hits=1" in result.stdout
        assert "scratch-path=0" in result.stdout
    else:
        assert result.returncode == 1
        assert "expected exact path:rule # reason" in result.stdout
        assert "fixture:1: scratch-path" in result.stdout
        assert "allowed_hits=0" in result.stdout


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
    allowlist_for(tmp_path).write_text(entry + "\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "ERROR: .publication-allow:1:" in result.stdout


def test_allowlist_itself_is_scanned(tmp_path):
    (tmp_path / "fixture").write_text("Public content\n")
    allowlist_for(tmp_path).write_text("fixture:credential # ghp_synthetic\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert ".publication-allow:1: credential" in result.stdout


def test_allowlist_cannot_self_allow(tmp_path):
    allowlist_for(tmp_path).write_text(
        ".publication-allow:credential # attempt to bypass self-scan\n"
    )
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert (
        "ERROR: .publication-allow:1: cannot allowlist the allowlist file itself" in result.stdout
    )


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


def test_named_pipe_fails_without_blocking_other_findings(tmp_path):
    os.mkfifo(tmp_path / "a-pipe")
    (tmp_path / "report.md").write_text("Public introduction\nclones/example\n")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=5,
    )

    assert result.returncode == 1
    assert "ERROR: a-pipe: not a regular file" in result.stdout
    assert "report.md:2: scratch-path (1 hit(s))" in result.stdout
    assert "files_scanned=1" in result.stdout
    assert "errors=1" in result.stdout


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


def test_unreadable_directory_fails_closed(tmp_path, monkeypatch, capsys):
    scanner = load_scanner()
    (tmp_path / "report.md").write_text("Public content\n")
    real_walk = Path.walk

    def walk_with_error(self, *, on_error=None, follow_symlinks=True):
        if self == tmp_path and on_error is not None:
            on_error(OSError(13, "Permission denied"))
            return iter(())
        return real_walk(self, on_error=on_error, follow_symlinks=follow_symlinks)

    monkeypatch.setattr(Path, "walk", walk_with_error)
    allowlist = tmp_path / "allowlist"
    result = scanner.scan(tmp_path, allowlist)
    output = capsys.readouterr().out
    assert result == 1
    assert "ERROR: research tree contains an unreadable directory" in output


def test_unreadable_file_fails_closed(tmp_path, monkeypatch, capsys):
    scanner = load_scanner()
    (tmp_path / "report.md").write_text("Public content\n")
    real_read_bytes = Path.read_bytes

    def read_bytes_with_error(self):
        if self.name == "report.md":
            raise OSError(13, "Permission denied")
        return real_read_bytes(self)

    monkeypatch.setattr(Path, "read_bytes", read_bytes_with_error)
    allowlist = tmp_path / "allowlist"
    result = scanner.scan(tmp_path, allowlist)
    output = capsys.readouterr().out
    assert result == 1
    assert "ERROR: report.md: cannot read file" in output


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
@pytest.mark.parametrize(
    "encoded,rule",
    [
        (r"ghp\u005fSYNTHETIC_ONLY", "credential"),
        (r"\/Users\/example/file", "home-path"),
        (r"BEGIN RSA\u0020PRIVATE KEY", "private-key"),
        (r"clones\u002fRepo/file", "scratch-path"),
        (r"worker\u002elocal:8080", "internal-host"),
    ],
)
def test_encoded_json_strings_report_physical_location(tmp_path, suffix, encoded, rule):
    root = tmp_path / "research"
    root.mkdir()
    tmp_path = root
    path = tmp_path / ("report" + suffix)
    # Include a visible hit too: semantic scanning must not double-count it.
    line = r'{"visible": "ghp_VISIBLE", "nested": [{"' + encoded + r'": "' + encoded + r'"}]}'
    path.write_text("\n" + line + "\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    expected = 3 if rule == "credential" else 2
    assert f"{path.name}:2: {rule} ({expected} hit(s))" in result.stdout
    assert "SYNTHETIC_ONLY" not in result.stdout + result.stderr
    allowlist_for(tmp_path).write_text(
        f"{path.name}:{rule} # Synthetic escaped fixture.\n"
        + (f"{path.name}:credential # Synthetic visible fixture.\n" if rule != "credential" else "")
    )
    assert run_guard(tmp_path).returncode == 0


def test_json_literal_escape_is_not_decoded_twice(tmp_path):
    (tmp_path / "safe.json").write_text(
        r'{"example": "ghp\\u005fEXAMPLE", "quote": "say \"hello\"", "n": 42}'
    )
    assert run_guard(tmp_path).returncode == 0


@pytest.mark.parametrize(
    "label",
    [
        "PRIVATE KEY",
        "ENCRYPTED PRIVATE KEY",
        "RSA PRIVATE KEY",
        "OPENSSH PRIVATE KEY",
        "EC PRIVATE KEY",
        "DSA PRIVATE KEY",
        "FUTURE PRIVATE KEY",
    ],
)
@pytest.mark.parametrize("suffix", [".txt", ".json", ".jsonl"])
def test_all_private_key_formats_are_rejected(tmp_path, label, suffix):
    import json

    content = f"-----BEGIN {label}-----\nSYNTHETIC_MATERIAL\n-----END {label}-----"
    if suffix != ".txt":
        content = json.dumps({"key": content}).replace("PRIVATE", r"PRIV\u0041TE")
    (tmp_path / ("evidence" + suffix)).write_text(content)
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert f"evidence{suffix}:1: private-key (1 hit(s))" in result.stdout
    assert "files_scanned=1" in result.stdout
    assert "SYNTHETIC_MATERIAL" not in result.stdout + result.stderr
