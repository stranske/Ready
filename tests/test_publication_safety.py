"""Exercise the publication guard through its dependency-free command line."""

import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

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
        ("-----BEGIN PRIVATE KEY-----", "private-key"),
        ("-----BEGIN ENCRYPTED PRIVATE KEY-----", "private-key"),
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


def test_all_rules_on_one_line_are_reported_even_with_an_exception(tmp_path):
    (tmp_path / "report.txt").write_text(
        "Public introduction\n"
        "/Users/example clones/example localhost:8000 "
        "BEGIN RSA PRIVATE KEY ghp_SYNTHETIC\n"
    )
    expected_rules = ("home-path", "credential", "private-key", "scratch-path", "internal-host")

    result = run_guard(tmp_path)

    assert result.returncode == 1
    for rule in expected_rules:
        assert result.stdout.count(f"report.txt:2: {rule} (1 hit(s))") == 1
    assert result.stdout.splitlines()[-1] == (
        "files_scanned=1 home-path=1 credential=1 private-key=1 "
        "scratch-path=1 internal-host=1 allowed_hits=0 errors=0"
    )

    allowlist_for(tmp_path).write_text(
        "report.txt:home-path # Reviewed synthetic documentation example.\n"
    )
    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert "report.txt:2: home-path" not in result.stdout
    for rule in expected_rules[1:]:
        assert result.stdout.count(f"report.txt:2: {rule} (1 hit(s))") == 1
    assert result.stdout.splitlines()[-1] == (
        "files_scanned=1 home-path=0 credential=1 private-key=1 "
        "scratch-path=1 internal-host=1 allowed_hits=1 errors=0"
    )
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert not result.stderr


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


def test_publication_guard_workflow_runs_prepare_then_scan():
    workflow = (REPO / ".github/workflows/publication-guard.yml").read_text()
    assert "prepare_publication.py" in workflow
    assert "check_publication_safety.py --root" in workflow
    assert "resolve_allowlist" in workflow
    assert "policy_scope" in workflow
    assert workflow.count('--allowlist "$selected_allowlist"') == 2
    assert workflow.index("prepare_publication.py") < workflow.index(
        "check_publication_safety.py --root"
    )


def _run_publication_workflow_shell(root: Path) -> list[subprocess.CompletedProcess[str]]:
    """Execute actual blocks with the runner's output-expression substitution."""

    repo = root.parent
    workflow_root = repo / "research-program"
    root.rename(workflow_root)
    shutil.copytree(REPO / "scripts", repo / "scripts")
    workflow = yaml.safe_load((REPO / ".github/workflows/publication-guard.yml").read_text())
    steps = workflow["jobs"]["publication-safety"]["steps"]
    runnable = {step["name"]: step for step in steps if "run" in step}
    output = repo / "github-output"
    env = {**os.environ, "GITHUB_OUTPUT": str(output)}
    results = [
        subprocess.run(
            ["bash", "-c", runnable["Resolve publication policy"]["run"]],
            cwd=repo,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    ]
    outputs = dict(line.split("=", 1) for line in output.read_text().splitlines())

    def render(value: str) -> str:
        for key, output_value in outputs.items():
            value = value.replace(
                "${{ steps.publication-policy.outputs." + key + " }}", output_value
            )
        return value

    for name in ("Check published research", "Prepare publication staging copy"):
        step = runnable[name]
        step_env = {**env, **{key: render(value) for key, value in step.get("env", {}).items()}}
        results.append(
            subprocess.run(
                ["bash", "-c", render(step["run"])],
                cwd=repo,
                env=step_env,
                capture_output=True,
                text=True,
                check=False,
            )
        )
    return results


@pytest.mark.parametrize("scope", ["local", "root"])
def test_publication_workflow_treats_output_paths_as_data(tmp_path, scope):
    repo = tmp_path / "literal$(touch injected)"
    root = repo / "content"
    root.mkdir(parents=True)
    (root / "evidence.txt").write_text("Public content\n")
    policy = root / ".publication-allow" if scope == "local" else repo / ".publication-allow"
    policy.write_text("# Reviewed empty policy.\n")

    results = _run_publication_workflow_shell(root)

    assert not (repo / "injected").exists(), "workflow output became shell code"
    assert [result.returncode for result in results] == [0, 0, 0], [
        result.stderr for result in results
    ]


def test_publication_guard_actual_workflow_shell_preserves_policy_parity(tmp_path):
    fixture = tmp_path / "evidence.txt"
    fixture.write_text("-----BEGIN PRIVATE KEY-----\nSYNTHETIC_TEST_MARKER")
    (tmp_path.parent / ".publication-allow").write_text("# Root policy denies the fixture.\n")
    (tmp_path / ".publication-allow").write_text(
        "evidence.txt:private-key # Reviewed synthetic incomplete-key fixture.\n"
    )

    results = _run_publication_workflow_shell(tmp_path)

    assert [result.returncode for result in results] == [0, 0, 0]


def test_publication_guard_actual_workflow_shell_uses_root_fallback(tmp_path):
    fixture = tmp_path / "evidence.txt"
    fixture.write_text("-----BEGIN PRIVATE KEY-----\nSYNTHETIC_TEST_MARKER")
    (tmp_path.parent / ".publication-allow").write_text(
        "evidence.txt:private-key # Reviewed synthetic root fallback fixture.\n"
    )

    results = _run_publication_workflow_shell(tmp_path)

    assert [result.returncode for result in results] == [0, 0, 0]


@pytest.mark.parametrize("target", ["root-policy", "missing-policy"])
def test_publication_guard_actual_workflow_shell_rejects_local_policy_symlinks(tmp_path, target):
    (tmp_path / "evidence.txt").write_text("Public content\n")
    (tmp_path.parent / ".publication-allow").write_text("# Root fallback policy.\n")
    if target == "root-policy":
        (tmp_path / ".publication-allow").symlink_to(tmp_path.parent / ".publication-allow")
    else:
        (tmp_path / ".publication-allow").symlink_to(target)

    results = _run_publication_workflow_shell(tmp_path)

    assert results[0].returncode == 0
    assert results[1].returncode == 1
    assert results[2].returncode == 1


def test_publication_guard_actual_workflow_shell_rejects_invalid_local_policy(tmp_path):
    """Malformed local policy must fail closed; a permissive root policy is not used."""
    (tmp_path / "evidence.txt").write_text("clones/SYNTHETIC_ONLY\n")
    (tmp_path.parent / ".publication-allow").write_text(
        "evidence.txt:scratch-path # Reviewed root fallback that must not apply.\n"
    )
    (tmp_path / ".publication-allow").write_text("evidence.txt:scratch-path\n")

    results = _run_publication_workflow_shell(tmp_path)

    assert results[0].returncode == 0
    assert results[1].returncode == 1
    assert "ERROR: .publication-allow:" in results[1].stdout
    assert "allowed_hits=0" in results[1].stdout
    assert results[2].returncode == 1


def test_publication_staging_reuses_selected_local_or_root_policy(tmp_path, monkeypatch):
    scanner = load_scanner()
    prepare = importlib.import_module("scripts.prepare_publication")
    repo = tmp_path.parent
    monkeypatch.setattr(scanner, "REPO_ROOT", repo)
    monkeypatch.setattr(scanner, "DEFAULT_ROOT", tmp_path)
    root_policy = repo / ".publication-allow"
    fixture = "evidence.txt"
    content = "-----BEGIN PRIVATE KEY-----\nSYNTHETIC_TEST_MARKER"

    def stage_and_check() -> tuple[Path, Path]:
        selected = scanner.resolve_allowlist(tmp_path, None)
        staging = repo / "staging"
        shutil.copytree(tmp_path, staging)
        staged_policy = (
            staging / ".publication-allow"
            if selected == tmp_path / ".publication-allow"
            else selected
        )
        prepare.prepare_copy(staging, staged_policy)
        assert scanner.scan(staging, staged_policy) == 0
        return selected, staged_policy

    (tmp_path / fixture).write_text(content)
    root_policy.write_text("# Root policy intentionally does not approve the fixture.\n")
    (tmp_path / ".publication-allow").write_text(
        f"{fixture}:private-key # Reviewed synthetic incomplete-key fixture.\n"
    )
    selected, staged_policy = stage_and_check()
    assert selected == tmp_path / ".publication-allow"
    assert staged_policy == repo / "staging" / ".publication-allow"

    shutil.rmtree(repo / "staging")
    (tmp_path / ".publication-allow").unlink()
    root_policy.write_text(f"{fixture}:private-key # Reviewed synthetic fallback fixture.\n")
    selected, staged_policy = stage_and_check()
    assert selected == root_policy
    assert staged_policy == root_policy


def test_dangling_local_policy_never_falls_back_to_root_policy(tmp_path, monkeypatch):
    scanner = load_scanner()
    prepare = importlib.import_module("scripts.prepare_publication")
    repo = tmp_path.parent
    monkeypatch.setattr(scanner, "REPO_ROOT", repo)
    monkeypatch.setattr(scanner, "DEFAULT_ROOT", tmp_path)
    (tmp_path / "evidence.txt").write_text("Public content\n")
    (repo / ".publication-allow").write_text("# Root fallback policy.\n")
    (tmp_path / ".publication-allow").symlink_to("missing-policy")

    selected = scanner.resolve_allowlist(tmp_path, None)
    assert selected == tmp_path / ".publication-allow"
    assert scanner.scan(tmp_path) == 1
    with pytest.raises(ValueError, match="allowlist"):
        prepare.prepare_copy(tmp_path, selected)


@pytest.mark.parametrize(
    "result,expected",
    [
        ("success", "success"),
        ("failure", "failure"),
        ("cancelled", "failure"),
        ("skipped", "failure"),
    ],
)
@pytest.mark.parametrize("seal_result", ["success", "failure", "cancelled", "skipped"])
def test_gate_summary_enforces_publication_even_when_python_skips(
    tmp_path, result, expected, seal_result
):
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
        "DELIVERY_SEAL_RESULT": seal_result,
    }
    subprocess.run(["bash", "-c", script], env=env, check=True, capture_output=True)
    # Failed publication remains a failure even when the seal is unavailable.
    # A passed publication cannot waive an unsuccessful generated-delivery seal.
    verdict = (
        expected
        if expected == "failure" or seal_result == "success"
        else {"failure": "failure", "cancelled": "error", "skipped": "pending"}[seal_result]
    )
    assert f"state={verdict}\n" in output.read_text()
    summary = yaml.safe_load(workflow)["jobs"]["summary"]
    assert {"detect", "python-ci", "publication-safety", "generated-delivery-seal"} <= set(
        summary["needs"]
    )
    assert summary["steps"][1]["env"]["PUBLICATION_RESULT"] == (
        "${{ needs.publication-safety.result || 'skipped' }}"
    )
    assert summary["steps"][1]["env"]["DELIVERY_SEAL_RESULT"] == (
        "${{ needs.generated-delivery-seal.result || 'skipped' }}"
    )


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


@pytest.mark.parametrize("failed_name", ["a-unreadable.md", "z-unreadable.md"])
def test_unreadable_file_preserves_other_findings(tmp_path, monkeypatch, capsys, failed_name):
    scanner = load_scanner()
    (tmp_path / failed_name).write_text("Public content\n")
    (tmp_path / "report.md").write_text("Public introduction\nclones/PRIVATE_SENTINEL\n")
    (tmp_path / "second.md").write_text("localhost:8000 localhost:9000\n")
    real_read_bytes = Path.read_bytes

    def read_bytes_with_error(self):
        if self.name == failed_name:
            raise OSError(13, "PRIVATE_ERROR_SENTINEL")
        return real_read_bytes(self)

    monkeypatch.setattr(Path, "read_bytes", read_bytes_with_error)
    result = scanner.scan(tmp_path)
    captured = capsys.readouterr()
    output = captured.out
    assert result == 1
    assert f"ERROR: {failed_name}: cannot read file" in output
    assert "report.md:2: scratch-path (1 hit(s))" in output
    assert "second.md:1: internal-host (2 hit(s))" in output
    assert output.splitlines()[-1] == (
        "files_scanned=2 home-path=0 credential=0 private-key=0 "
        "scratch-path=1 internal-host=2 allowed_hits=0 errors=1"
    )
    assert "PRIVATE_SENTINEL" not in output + captured.err
    assert "PRIVATE_ERROR_SENTINEL" not in output + captured.err
    assert not captured.err


@pytest.mark.parametrize("explicit", [False, True])
@pytest.mark.parametrize("read_method", ["read_text", "read_bytes"])
def test_policy_read_failure_preserves_findings(
    tmp_path, monkeypatch, capsys, explicit, read_method
):
    scanner = load_scanner()
    (tmp_path / "report.md").write_text("Public introduction\nclones/example\n")
    policy = tmp_path.parent / "reviewed-policy" if explicit else allowlist_for(tmp_path)
    policy.write_text("# No exceptions.\n")
    original_read = getattr(Path, read_method)

    def fail_policy_read(self, *args, **kwargs):
        if self == policy:
            raise PermissionError("PRIVATE_ERROR_SENTINEL")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(Path, read_method, fail_policy_read)

    result = scanner.scan(tmp_path, policy if explicit else None)
    captured = capsys.readouterr()

    assert result == 1
    error = "cannot read UTF-8 allowlist" if read_method == "read_text" else "cannot read file"
    assert f"ERROR: .publication-allow: {error}" in captured.out
    assert "report.md:2: scratch-path (1 hit(s))" in captured.out
    assert captured.out.splitlines()[-1] == (
        "files_scanned=1 home-path=0 credential=0 private-key=0 "
        "scratch-path=1 internal-host=0 allowed_hits=0 errors=1"
    )
    assert "PRIVATE_ERROR_SENTINEL" not in captured.out + captured.err
    assert not captured.err


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


def write_docx(path, paragraphs, *, member="word/document.xml"):
    import zipfile
    from xml.sax.saxutils import escape

    body = "".join(
        "<w:p>" + "".join("<w:r><w:t>" + escape(run) + "</w:t></w:r>" for run in runs) + "</w:p>"
        for runs in paragraphs
    )
    xml = (
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
        + body
        + "</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "word/document.xml",
            (
                xml
                if member == "word/document.xml"
                else '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'
            ),
        )
        if member != "word/document.xml":
            archive.writestr(member, xml)


@pytest.mark.parametrize(
    ("runs", "rule"),
    [
        (["/Us", "ers/SYNTHETIC/report"], "home-path"),
        (["gh", "p_SYNTHETIC"], "credential"),
        (["-----BEGIN RSA PRI", "VATE KEY-----SYNTHETIC"], "private-key"),
        (["worker.lo", "cal:8080/SYNTHETIC"], "internal-host"),
        (["scratch", "pad/SYNTHETIC"], "scratch-path"),
    ],
)
@pytest.mark.parametrize(
    "member", ["word/document.xml", "word/header1.xml", "word/footer1.xml", "word/footnotes.xml"]
)
def test_compressed_docx_visible_text_and_split_runs_fail(tmp_path, runs, rule, member):
    path = tmp_path / "report.docx"
    write_docx(path, [runs], member=member)
    scanner = load_scanner()
    assert not any(pattern.search(path.read_bytes()) for pattern in scanner.RULES.values())
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "report.docx:" in result.stdout and rule in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert "errors=0" in result.stdout
    allowlist_for(tmp_path).write_text(f"report.docx:{rule} # Reviewed synthetic fixture.\n")
    assert run_guard(tmp_path).returncode == 0


def test_clean_compressed_docx_passes(tmp_path):
    write_docx(tmp_path / "report.docx", [["Public", " report"]])
    result = run_guard(tmp_path)
    assert result.returncode == 0 and "errors=0" in result.stdout


@pytest.mark.parametrize("hexadecimal", [False, True])
@pytest.mark.parametrize("unsafe", [False, True])
@pytest.mark.parametrize(
    "member", ["word/document.xml", "word/header1.xml", "word/footer1.xml", "word/footnotes.xml"]
)
def test_docx_numeric_character_references_are_decoded(tmp_path, member, unsafe, hexadecimal):
    import zipfile

    scanner = load_scanner()
    path = tmp_path / "report.docx"
    text = "ghp_SYNTHETIC" if unsafe else "Public report"
    references = "".join(
        f"&#x{ord(char):x};" if hexadecimal else f"&#{ord(char)};" for char in text
    )
    xml = (
        f'<w:document xmlns:w="{scanner.WORD_NS[1:-1]}"><w:p><w:r><w:t>'
        + references
        + "</w:t></w:r></w:p></w:document>"
    ).encode()
    assert not any(pattern.search(xml) for pattern in scanner.RULES.values())
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        if member != "word/document.xml":
            archive.writestr("word/document.xml", "<document/>")
        archive.writestr(member, xml)
    original = path.read_bytes()
    assert not any(pattern.search(original) for pattern in scanner.RULES.values())

    result = run_guard(tmp_path)

    assert result.returncode == int(unsafe)
    assert f"credential={int(unsafe)}" in result.stdout
    assert "errors=0" in result.stdout
    if unsafe:
        assert "report.docx:1: credential (1 hit(s))" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert member not in result.stdout + result.stderr
    assert not result.stderr
    assert path.read_bytes() == original


def test_docx_does_not_join_text_across_paragraphs(tmp_path):
    write_docx(tmp_path / "report.docx", [["gh"], ["p_SYNTHETIC"]])

    result = run_guard(tmp_path)

    assert result.returncode == 0
    assert "credential=0" in result.stdout and "errors=0" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr


@pytest.mark.parametrize(
    "namespace",
    [
        "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "http://purl.oclc.org/ooxml/wordprocessingml/main",
    ],
)
@pytest.mark.parametrize(
    ("before", "inside", "after", "hits"),
    [
        (["gh"], ["p_SYNTHETIC"], [], 0),
        (["gh"], ["Public text box"], ["p_SYNTHETIC"], 1),
        (["Public paragraph"], ["gh", "p_SYNTHETIC"], [], 1),
    ],
)
def test_docx_text_box_paragraphs_are_scanned_independently(
    tmp_path, namespace, before, inside, after, hits
):
    import zipfile

    def runs(parts):
        return "".join(f"<w:r><w:t>{part}</w:t></w:r>" for part in parts)

    path = tmp_path / "report.docx"
    xml = (
        f'<w:document xmlns:w="{namespace}" '
        'xmlns:v="urn:schemas-microsoft-com:vml"><w:body><w:p>'
        + runs(before)
        + "<w:r><w:pict><v:shape><v:textbox><w:txbxContent><w:p>"
        + runs(inside)
        + "</w:p></w:txbxContent></v:textbox></v:shape></w:pict></w:r>"
        + runs(after)
        + "</w:p></w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", xml)
    original = path.read_bytes()
    assert not any(pattern.search(original) for pattern in load_scanner().RULES.values())

    result = run_guard(tmp_path)

    assert result.returncode == int(bool(hits))
    assert f"credential={hits}" in result.stdout
    assert "errors=0" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert "word/document.xml" not in result.stdout + result.stderr
    assert not result.stderr
    assert path.read_bytes() == original


def test_compressed_docx_contiguous_marker_counts_once(tmp_path):
    """Joined w:t text must not also re-count the same marker from raw XML lines."""
    path = tmp_path / "report.docx"
    write_docx(path, [["ghp_SYNTHETIC"]])
    scanner = load_scanner()
    assert not any(pattern.search(path.read_bytes()) for pattern in scanner.RULES.values())
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert result.stdout.count("report.docx:") == 1
    assert "credential=1" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr


@pytest.mark.parametrize(
    "kind", ["not-zip", "bad-xml", "entity", "size", "members", "total", "duplicate"]
)
def test_docx_fail_closed_without_xml_disclosure(tmp_path, capsys, monkeypatch, kind):
    import zipfile

    scanner = load_scanner()
    path = tmp_path / "report.docx"
    if kind == "not-zip":
        path.write_bytes(b"SYNTHETIC invalid zip")
    else:
        write_docx(path, [["Public report"]])
        if kind in {"bad-xml", "entity"}:
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr(
                    "word/document.xml",
                    (
                        "<SYNTHETIC"
                        if kind == "bad-xml"
                        else '<!DOCTYPE x [<!ENTITY e "SYNTHETIC">]><x>&e;</x>'
                    ),
                )
        elif kind == "duplicate":
            with (
                pytest.warns(UserWarning, match="Duplicate"),
                zipfile.ZipFile(path, "a") as archive,
            ):
                archive.writestr("word/document.xml", "SYNTHETIC")
        else:
            monkeypatch.setattr(
                scanner,
                {
                    "size": "DOCX_MAX_MEMBER_BYTES",
                    "members": "DOCX_MAX_MEMBERS",
                    "total": "DOCX_MAX_TOTAL_BYTES",
                }[kind],
                0 if kind == "members" else 1,
            )
    assert scanner.scan(tmp_path) == 1
    output = capsys.readouterr().out
    assert "ERROR: report.docx: invalid or oversized DOCX" in output
    assert "SYNTHETIC" not in output


@pytest.mark.parametrize(
    "member", ["word/document.xml", "word/header1.xml", "word/footer1.xml", "word/footnotes.xml"]
)
def test_malformed_word_part_is_not_allowlisted_and_scan_continues(tmp_path, member):
    import zipfile

    path = tmp_path / "a-report.docx"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        if member != "word/document.xml":
            archive.writestr("word/document.xml", "<document/>")
        archive.writestr(member, '<broken hidden="ghp_SYNTHETIC"')
    allowlist_for(tmp_path).write_text("a-report.docx:credential # Reviewed synthetic fixture.\n")
    (tmp_path / "z-report.md").write_text("Public introduction\nclones/SYNTHETIC\n")
    original = path.read_bytes()

    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert set(result.stdout.splitlines()) == {
        "ERROR: a-report.docx: invalid or oversized DOCX",
        "z-report.md:2: scratch-path (1 hit(s))",
        "files_scanned=2 home-path=0 credential=0 private-key=0 "
        "scratch-path=1 internal-host=0 allowed_hits=0 errors=1",
    }
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert member not in result.stdout + result.stderr
    assert not result.stderr
    assert path.read_bytes() == original


@pytest.mark.parametrize("limit", ["members", "member-bytes", "expanded-bytes"])
@pytest.mark.parametrize("overflow", [False, True])
def test_docx_resource_limit_boundaries(tmp_path, capsys, monkeypatch, limit, overflow):
    import zipfile

    scanner = load_scanner()
    path = tmp_path / "report.docx"
    write_docx(path, [["Public report"]])
    with zipfile.ZipFile(path, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        # An auxiliary member must count toward both size budgets, even though
        # it contains no Word XML. Compression keeps the ZIP below either cap.
        archive.writestr("custom/data.bin", b"SYNTHETIC" * 1024)
        members = archive.infolist()
    setting, boundary = {
        "members": ("DOCX_MAX_MEMBERS", len(members)),
        "member-bytes": ("DOCX_MAX_MEMBER_BYTES", max(m.file_size for m in members)),
        "expanded-bytes": ("DOCX_MAX_TOTAL_BYTES", sum(m.file_size for m in members)),
    }[limit]
    if limit != "members":
        assert path.stat().st_size < boundary - 1
    monkeypatch.setattr(scanner, setting, boundary - int(overflow))
    original = path.read_bytes()

    assert scanner.scan(tmp_path) == int(overflow)

    output = capsys.readouterr().out
    if overflow:
        assert "ERROR: report.docx: invalid or oversized DOCX" in output
    assert f"errors={int(overflow)}" in output
    assert "files_scanned=1" in output
    assert "SYNTHETIC" not in output
    assert "custom/data.bin" not in output
    assert path.read_bytes() == original


@pytest.mark.parametrize("overflow", [False, True])
def test_expanded_docx_member_reads_are_bounded(tmp_path, capsys, monkeypatch, overflow):
    import zipfile

    scanner = load_scanner()
    path = tmp_path / "report.docx"
    write_docx(path, [["Public report"]])
    with zipfile.ZipFile(path, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        xml = archive.read("word/document.xml")
        for member in ("word/header1.xml", "word/footer1.xml", "word/footnotes.xml"):
            archive.writestr(member, xml)
        # The largest expanded member is not XML; it must obey the same cap.
        archive.writestr("custom/data.bin", b"Public data. " * 1024)
        members = archive.infolist()
    limit = max(member.file_size for member in members) - int(overflow)
    monkeypatch.setattr(scanner, "DOCX_MAX_MEMBER_BYTES", limit)
    original = path.read_bytes()
    real_read = zipfile.ZipExtFile.read
    reads = []

    def bounded_read(stream, size=-1):
        assert 0 <= size <= limit + 1, "Expanded DOCX member read exceeded its budget"
        reads.append(stream.name)
        return real_read(stream, size)

    monkeypatch.setattr(zipfile.ZipExtFile, "read", bounded_read)

    assert scanner.scan(tmp_path) == int(overflow)

    output = capsys.readouterr()
    assert reads == [member.filename for member in members if member.file_size <= limit]
    assert f"errors={int(overflow)}" in output.out
    assert "files_scanned=1" in output.out
    if overflow:
        assert "ERROR: report.docx: invalid or oversized DOCX" in output.out
    assert not output.err
    assert path.read_bytes() == original


@pytest.mark.parametrize("overflow", [False, True])
def test_outer_docx_read_is_bounded(tmp_path, capsys, monkeypatch, overflow):
    import io

    scanner = load_scanner()
    path = tmp_path / "report.DOCX"
    write_docx(path, [["Public report"]])
    limit = path.stat().st_size
    if overflow:
        with path.open("ab") as stream:
            stream.write(b"\x00" * 64)
    original = path.read_bytes()
    monkeypatch.setattr(scanner, "DOCX_MAX_TOTAL_BYTES", limit)
    (tmp_path / "z-report.md").write_text("Public report.\n")
    real_open = Path.open
    bytes_read = 0

    class BudgetedInput(io.BytesIO):
        def read(self, size=-1):
            nonlocal bytes_read
            assert 0 <= size <= limit + 1 - bytes_read, "DOCX input read exceeded its budget"
            chunk = super().read(size)
            bytes_read += len(chunk)
            return chunk

    def budgeted_open(self, *args, **kwargs):
        if self == path:
            return BudgetedInput(original)
        return real_open(self, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "open", budgeted_open)
        assert scanner.scan(tmp_path) == int(overflow)

    output = capsys.readouterr()
    assert bytes_read <= limit + 1
    if not overflow:
        assert bytes_read == len(original)
    assert f"errors={int(overflow)}" in output.out
    assert "files_scanned=2" in output.out
    if overflow:
        assert "ERROR: report.DOCX: invalid or oversized DOCX" in output.out
    assert not output.err
    assert path.read_bytes() == original


def test_strict_word_namespace_split_runs_are_guarded(tmp_path):
    import zipfile

    path = tmp_path / "report.docx"
    xml = '<w:document xmlns:w="http://purl.oclc.org/ooxml/wordprocessingml/main"><w:p><w:r><w:t>gh</w:t></w:r><w:r><w:t>p_SYNTHETIC</w:t></w:r></w:p></w:document>'
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", xml)
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "SYNTHETIC" not in result.stdout + result.stderr


def test_utf16_dtd_is_rejected_without_entity_expansion(tmp_path, capsys):
    import zipfile

    path = tmp_path / "report.docx"
    xml = '<!DOCTYPE x [<!ENTITY e "SYNTHETIC">]><x>&e;</x>'
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", xml.encode("utf-16"))
    assert load_scanner().scan(tmp_path) == 1
    output = capsys.readouterr().out
    assert "ERROR: report.docx: invalid or oversized DOCX" in output
    assert "SYNTHETIC" not in output


@pytest.mark.parametrize("encoding", ["utf-16-le", "utf-16-be"])
@pytest.mark.parametrize(
    "member", ["word/document.xml", "word/header1.xml", "word/footer1.xml", "word/footnotes.xml"]
)
@pytest.mark.parametrize("unsafe", [False, True])
def test_utf16_docx_visible_text_is_decoded(tmp_path, encoding, member, unsafe):
    import codecs
    import zipfile

    scanner = load_scanner()
    path = tmp_path / "report.docx"
    write_docx(path, [["Public report"]])
    runs = ("scratch", "pad/SYNTHETIC") if unsafe else ("Public", " report")
    xml = (
        '<?xml version="1.0" encoding="UTF-16"?>'
        f'<w:document xmlns:w="{scanner.WORD_NS[1:-1]}"><w:body><w:p>'
        + "".join(f"<w:r><w:t>{run}</w:t></w:r>" for run in runs)
        + "</w:p></w:body></w:document>"
    )
    bom = codecs.BOM_UTF16_LE if encoding == "utf-16-le" else codecs.BOM_UTF16_BE
    # UTF-16 hides markers even in decompressed bytes; only parsed, joined text
    # exposes the unsafe marker. Clean UTF-16 must not be rejected wholesale.
    payload = bom + xml.encode(encoding)
    assert not any(pattern.search(payload) for pattern in scanner.RULES.values())
    with zipfile.ZipFile(path) as archive:
        parts = {part.filename: archive.read(part) for part in archive.infolist()}
    parts[member] = payload
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in parts.items():
            archive.writestr(name, content)
    original = path.read_bytes()
    assert not any(pattern.search(original) for pattern in scanner.RULES.values())

    result = run_guard(tmp_path)

    assert result.returncode == int(unsafe)
    assert f"scratch-path={int(unsafe)}" in result.stdout
    assert "errors=0" in result.stdout
    if unsafe:
        assert "report.docx:1: scratch-path (1 hit(s))" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert member not in result.stdout + result.stderr
    assert not result.stderr
    assert path.read_bytes() == original


@pytest.mark.parametrize("location", ["zip-comment", "xml-attribute", "auxiliary"])
def test_docx_preserves_raw_byte_and_member_scans(tmp_path, location):
    import zipfile

    path = tmp_path / "report.docx"
    write_docx(path, [["Public report"]])
    with zipfile.ZipFile(path, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        if location == "zip-comment":
            archive.comment = b"ghp_SYNTHETIC"
        elif location == "xml-attribute":
            archive.writestr("word/header1.xml", '<x hidden="ghp_SYNTHETIC"/>')
        else:
            archive.writestr("custom/data.bin", b"ghp_SYNTHETIC")
    original = path.read_bytes()
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "credential=1" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert path.read_bytes() == original


@pytest.mark.parametrize("member", ["word/charts/chart1.xml", "word/diagrams/data1.xml"])
@pytest.mark.parametrize(
    "namespace",
    [
        "http://schemas.openxmlformats.org/drawingml/2006/main",
        "http://purl.oclc.org/ooxml/drawingml/main",
    ],
)
def test_docx_drawingml_split_text_is_scanned(tmp_path, member, namespace):
    import zipfile

    path = tmp_path / "report.docx"
    write_docx(path, [["Public report"]])
    with zipfile.ZipFile(path, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            member,
            f'<a:root xmlns:a="{namespace}"><a:p><a:r><a:t>gh</a:t></a:r>'
            "<a:r><a:t>p_SYNTHETIC</a:t></a:r></a:p></a:root>",
        )
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "credential=1" in result.stdout and "errors=0" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr


def test_docx_corrupt_auxiliary_member_fails_closed(tmp_path):
    import struct
    import zipfile

    path = tmp_path / "report.docx"
    write_docx(path, [["Public report"]])
    with zipfile.ZipFile(path, "a", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("media/image.bin", b"SYNTHETIC image bytes")
        member = archive.getinfo("media/image.bin")
    content = bytearray(path.read_bytes())
    name_size, extra_size = struct.unpack_from("<HH", content, member.header_offset + 26)
    offset = member.header_offset + 30 + name_size + extra_size
    content[offset] ^= 1
    path.write_bytes(content)
    result = run_guard(tmp_path)
    assert result.returncode == 1
    assert "ERROR: report.docx: invalid or oversized DOCX" in result.stdout
    assert "SYNTHETIC" not in result.stdout + result.stderr


@pytest.mark.parametrize("kind", ["missing-document", "encrypted", "unsupported-compression"])
def test_unreadable_docx_structure_fails_closed_through_cli(tmp_path, kind):
    import struct
    import zipfile

    path = tmp_path / "a-report.docx"
    member = "word/header1.xml" if kind == "missing-document" else "word/document.xml"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member, "<document>SYNTHETIC</document>")
    if kind != "missing-document":
        content = bytearray(path.read_bytes())
        central = content.index(b"PK\x01\x02")
        # Keep the local and central ZIP headers consistent. Bit 0 declares
        # encryption; compression method 99 is unsupported by zipfile.
        local_field, central_field, value = (6, 8, 1) if kind == "encrypted" else (8, 10, 99)
        for offset in (local_field, central + central_field):
            struct.pack_into("<H", content, offset, value)
        path.write_bytes(content)
    original = path.read_bytes()
    (tmp_path / "z-report.md").write_text("Public report.\n")

    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert result.stdout.splitlines() == [
        "ERROR: a-report.docx: invalid or oversized DOCX",
        "files_scanned=2 home-path=0 credential=0 private-key=0 "
        "scratch-path=0 internal-host=0 allowed_hits=0 errors=1",
    ]
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert member not in result.stdout + result.stderr
    assert not result.stderr
    assert path.read_bytes() == original


def test_corrupt_zip_lzma_docx_continues_scanning_through_cli(tmp_path):
    import struct
    import zipfile

    path = tmp_path / "a-report.docx"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_LZMA) as archive:
        archive.writestr("word/document.xml", "<document>SYNTHETIC</document>")
        member = archive.getinfo("word/document.xml")
    content = bytearray(path.read_bytes())
    name_size, extra_size = struct.unpack_from("<HH", content, member.header_offset + 26)
    offset = member.header_offset + 30 + name_size + extra_size
    # ZIP-LZMA stores a four-byte prefix before its LZMA filter properties.
    # An invalid properties byte raises LZMAError before ZIP CRC validation.
    content[offset + 4] = 0xFF
    path.write_bytes(content)
    original = path.read_bytes()
    (tmp_path / "z-report.md").write_text("Public report.\n")

    result = run_guard(tmp_path)

    assert result.returncode == 1
    assert result.stdout.splitlines() == [
        "ERROR: a-report.docx: invalid or oversized DOCX",
        "files_scanned=2 home-path=0 credential=0 private-key=0 "
        "scratch-path=0 internal-host=0 allowed_hits=0 errors=1",
    ]
    assert not result.stderr
    assert "SYNTHETIC" not in result.stdout + result.stderr
    assert path.read_bytes() == original
