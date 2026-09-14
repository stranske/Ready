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
    """Give each synthetic research tree an isolated parent directory."""
    root = tmp_path / "research"
    root.mkdir()
    return root


def allowlist_for(root: Path) -> Path:
    return root / ".publication-allow"


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
            for prefix in (
                "sk-ant-",
                "sk-proj-",
                "ghp_",
                "github_pat_",
                "lsv2_",
                "crsr_",
                "AIza",
            )
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


def test_hidden_nested_files_are_scanned_alongside_root_findings(tmp_path):
    nested = tmp_path / ".archive" / "exports"
    nested.mkdir(parents=True)
    (nested / ".report.bin").write_bytes(
        b"\xff\x00Public introduction\nclones/example localhost:8000\n"
    )
    (tmp_path / "report.md").write_text("Public introduction\n/Users/example/report\n")
    (nested / "clean.md").write_text("Public content\n")

    result = run_guard(tmp_path)

    assert result.returncode == 1
    for expected in (
        ".archive/exports/.report.bin:2: scratch-path (1 hit(s))",
        ".archive/exports/.report.bin:2: internal-host (1 hit(s))",
        "report.md:2: home-path (1 hit(s))",
        "files_scanned=3",
        "home-path=1 credential=0 private-key=0 scratch-path=1 internal-host=1",
        "allowed_hits=0 errors=0",
    ):
        assert expected in result.stdout
    assert "example" not in result.stdout + result.stderr
    assert not result.stderr


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

    # The unselected local policy is still scanned as publication content.
    assert "files_scanned=2" in result.stdout
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


@pytest.mark.parametrize("explicit", [False, True])
def test_invalid_utf8_policy_fails_and_preserves_all_findings(tmp_path, explicit):
    (tmp_path / "report.md").write_text("Public introduction\nclones/example\n")
    policy = tmp_path.parent / "reviewed-policy" if explicit else allowlist_for(tmp_path)
    policy.write_bytes(
        b"report.md:scratch-path # Reviewed example.\n"
        b"# Invalid UTF-8: \xff\n"
        b"# scratchpad/POLICY_SENTINEL\n"
    )

    result = run_guard(tmp_path, policy if explicit else None)

    assert result.returncode == 1
    assert "ERROR: .publication-allow: cannot read UTF-8 allowlist" in result.stdout
    assert "report.md:2: scratch-path (1 hit(s))" in result.stdout
    assert ".publication-allow:3: scratch-path (1 hit(s))" in result.stdout
    assert "files_scanned=1" in result.stdout
    assert "scratch-path=2" in result.stdout
    assert "allowed_hits=0" in result.stdout
    assert "errors=1" in result.stdout
    assert "POLICY_SENTINEL" not in result.stdout + result.stderr
    assert not result.stderr


@pytest.mark.parametrize("has_hit", [False, True])
def test_missing_explicit_allowlist_fails_and_continues_scan(tmp_path, has_hit):
    content = "clones/example\n" if has_hit else "Public content\n"
    (tmp_path / "report.md").write_text(content)
    allowlist_for(tmp_path).write_text("report.md:scratch-path # Reviewed fixture.\n")

    result = run_guard(tmp_path, tmp_path.parent / "missing-policy")

    assert result.returncode == 1
    assert "explicitly selected allowlist does not exist" in result.stdout
    assert "files_scanned=2" in result.stdout
    assert "allowed_hits=0" in result.stdout
    assert "errors=1" in result.stdout
    if has_hit:
        assert "report.md:1: scratch-path (1 hit(s))" in result.stdout


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


@pytest.mark.parametrize("location", ["local", "explicit"])
@pytest.mark.parametrize("kind", ["pipe", "directory"])
def test_nonregular_allowlist_fails_without_blocking_scan(tmp_path, location, kind):
    (tmp_path / "report.md").write_text("Public introduction\nclones/example\n")
    policy = {
        "local": tmp_path / ".publication-allow",
        "explicit": tmp_path.parent / "reviewed-policy",
    }[location]
    if kind == "pipe":
        os.mkfifo(policy)
    else:
        policy.mkdir()
    cmd = [sys.executable, str(SCRIPT), "--root", str(tmp_path)]
    if location == "explicit":
        cmd.extend(["--allowlist", str(policy)])

    result = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=5)

    assert result.returncode == 1
    assert "ERROR: .publication-allow: not a regular file" in result.stdout
    assert "report.md:2: scratch-path (1 hit(s))" in result.stdout
    assert "files_scanned=1" in result.stdout
    assert "allowed_hits=0" in result.stdout
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


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
@pytest.mark.parametrize("malformed", [r'"bad\q"', '"unfinished'])
def test_allowlisted_findings_do_not_suppress_structured_errors(tmp_path, suffix, malformed):
    path = tmp_path / ("report" + suffix)
    path.write_text(r'{"example": "clones\/SYNTHETIC_ONLY", "invalid": ' + malformed + "\n")
    allowlist_for(tmp_path).write_text(
        f"{path.name}:scratch-path # Reviewed synthetic path example.\n"
    )

    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert f"ERROR: {path.name}:1: invalid structured string" in result.stdout
    assert result.stdout.splitlines()[-1] == (
        "files_scanned=1 home-path=0 credential=0 private-key=0 "
        "scratch-path=0 internal-host=0 allowed_hits=1 errors=1"
    )
    assert "SYNTHETIC_ONLY" not in result.stdout + result.stderr
    assert not result.stderr


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
def test_invalid_json_string_does_not_hide_other_findings(tmp_path, suffix):
    path = tmp_path / ("report" + suffix)
    path.write_text(
        "\n"
        r'{"before": "clones\u002fexample", "invalid": "\q", '
        r'"after": "localhost\u003a8000", "raw": "scratchpad/example"}'
        "\n"
    )

    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert f"ERROR: {path.name}:2: invalid structured string" in result.stdout
    assert f"{path.name}:2: scratch-path (2 hit(s))" in result.stdout
    assert f"{path.name}:2: internal-host (1 hit(s))" in result.stdout
    assert "files_scanned=1" in result.stdout
    assert "errors=1" in result.stdout
    assert "example" not in result.stdout + result.stderr
    assert not result.stderr


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


@pytest.mark.parametrize("reason", [" # Reviewed synthetic fixture.", "", " # "])
def test_research_allowlist_contract_overrides_legacy(tmp_path, reason):
    (tmp_path / "fixture").write_text("ghp_SYNTHETIC\n")
    # The supported research-local policy wins, even when invalid; the legacy
    # policy must never silently rescue a missing justification.
    (tmp_path.parent / ".publication-allow").write_text("fixture:credential # Legacy fixture.\n")
    (tmp_path / ".publication-allow").write_text(f"fixture:credential{reason}\n")
    result = run_guard(tmp_path)
    assert "files_scanned=1" in result.stdout
    assert result.returncode == (0 if reason.strip() == "# Reviewed synthetic fixture." else 1)
    if result.returncode:
        assert "expected exact path:rule # reason" in result.stdout
    else:
        assert "allowed_hits=1" in result.stdout


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
@pytest.mark.parametrize("unfinished", ['"', '"Public text', '"trailing' + "\\", r'"escaped\"'])
def test_unterminated_json_string_fails_closed(tmp_path, suffix, unfinished):
    path = tmp_path / ("report" + suffix)
    path.write_text(unfinished)

    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert f"ERROR: {path.name}:1: invalid structured string" in result.stdout
    assert "files_scanned=1" in result.stdout
    assert "errors=1" in result.stdout
    assert not result.stderr


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
def test_unterminated_json_preserves_findings_on_other_strings_and_lines(tmp_path, suffix):
    path = tmp_path / ("report" + suffix)
    path.write_text(
        r'{"earlier": "clones\/EXAMPLE", "unfinished": "localhost:8000'
        + "\n"
        + r'{"later": "scratchpad\/EXAMPLE"}'
        + "\n"
    )

    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert f"{path.name}:1: scratch-path (1 hit(s))" in result.stdout
    assert f"{path.name}:1: internal-host (1 hit(s))" in result.stdout
    assert f"{path.name}:2: scratch-path (1 hit(s))" in result.stdout
    assert f"ERROR: {path.name}:1: invalid structured string" in result.stdout
    assert "scratch-path=2 internal-host=1" in result.stdout
    assert "errors=1" in result.stdout
    assert "EXAMPLE" not in result.stdout + result.stderr
    assert not result.stderr


def test_explicit_policy_overrides_research_local_policy(tmp_path):
    (tmp_path / "fixture").write_text("ghp_SYNTHETIC\n")
    (tmp_path / ".publication-allow").write_text("fixture:credential # Local fixture.\n")
    explicit = tmp_path.parent / "explicit-policy"
    explicit.write_text("# No exceptions.\n")
    result = run_guard(tmp_path, explicit)
    assert result.returncode == 1
    assert "fixture:1: credential" in result.stdout
    assert "allowed_hits=0" in result.stdout


def test_research_allowlist_is_scanned_once(tmp_path):
    (tmp_path / "fixture").write_text("Public content\n")
    (tmp_path / ".publication-allow").write_text("# ghp_SYNTHETIC\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert result.stdout.count(".publication-allow:1: credential") == 1
    assert "credential=1" in result.stdout
    assert "files_scanned=1" in result.stdout


def test_policy_only_is_not_publication_content(tmp_path):
    (tmp_path / ".publication-allow").write_text("# No exceptions.\n")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "zero files scanned" in result.stdout


@pytest.mark.parametrize("has_report", [False, True])
def test_explicit_policy_parent_components_do_not_count_as_content(tmp_path, has_report):
    (tmp_path / "nested").mkdir()
    (tmp_path / ".publication-allow").write_text("# Reviewed policy.\n")
    if has_report:
        (tmp_path / "report.md").write_text("Public content\n")

    result = run_guard(tmp_path, tmp_path / "nested" / ".." / ".publication-allow")

    assert result.returncode == (0 if has_report else 1)
    assert f"files_scanned={int(has_report)}" in result.stdout
    if not has_report:
        assert "zero files scanned" in result.stdout


def test_dangling_research_policy_does_not_fall_back(tmp_path):
    (tmp_path / "fixture").write_text("ghp_SYNTHETIC\n")
    (tmp_path.parent / ".publication-allow").write_text("fixture:credential # Legacy fixture.\n")
    (tmp_path / ".publication-allow").symlink_to(tmp_path.parent / "missing-policy")
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "symlinks are not allowed" in result.stdout
    assert "allowed_hits=0" in result.stdout


@pytest.mark.parametrize("nested", [False, True])
def test_custom_root_does_not_inherit_parent_exceptions(tmp_path, nested):
    root = tmp_path / "export" if nested else tmp_path
    root.mkdir(exist_ok=True)
    (root / "report.md").write_text("clones/example\n")
    parent_policy = root.parent / ".publication-allow"
    parent_policy.write_text("report.md:scratch-path # Reviewed for the parent tree only.\n")

    result = run_guard(root)

    assert result.returncode == 1
    assert "report.md:1: scratch-path (1 hit(s))" in result.stdout
    assert "allowed_hits=0" in result.stdout
    assert "errors=0" in result.stdout
    # The operator can still deliberately select a policy for an exported tree.
    assert run_guard(root, parent_policy).returncode == 0


@pytest.mark.parametrize("kind", ["valid", "pipe", "directory", "invalid-local", "linked-local"])
def test_canonical_root_retains_legacy_policy_validation(tmp_path, monkeypatch, capsys, kind):
    scanner = load_scanner()
    monkeypatch.setattr(scanner, "DEFAULT_ROOT", tmp_path)
    monkeypatch.setattr(scanner, "REPO_ROOT", tmp_path.parent)
    (tmp_path / "report.md").write_text("clones/example\n")
    legacy = tmp_path.parent / ".publication-allow"
    if kind == "pipe":
        os.mkfifo(legacy)
    elif kind == "directory":
        legacy.mkdir()
    else:
        legacy.write_text("report.md:scratch-path # Reviewed canonical research example.\n")
    if kind == "invalid-local":
        (tmp_path / ".publication-allow").write_text("report.md:scratch-path\n")
    elif kind == "linked-local":
        (tmp_path / ".publication-allow").symlink_to(tmp_path.parent / "missing-policy")

    result = scanner.scan(tmp_path)
    output = capsys.readouterr().out

    assert result == (0 if kind == "valid" else 1)
    assert "files_scanned=1" in output
    assert f"allowed_hits={int(kind == 'valid')}" in output
    if kind != "valid":
        assert "report.md:1: scratch-path (1 hit(s))" in output
        assert "ERROR: .publication-allow:" in output
