"""Publication export must preserve originals and keep the safety guard binding."""

from __future__ import annotations

import importlib
import json
import os
import shutil
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def module(name):
    return importlib.import_module(f"scripts.{name}")


prepare = module("prepare_publication")
guard = module("check_publication_safety")


def test_export_preserves_source_and_json_and_removes_entire_token(tmp_path, capsys):
    source = tmp_path / "source"
    source.mkdir()
    original = {
        "path": "/Users/example/clones/Repo/src/a.py",
        "token": "sk-proj-SYNTHETIC_ONLY_NOT_A_REAL_TOKEN",
        "private": "-----BEGIN RSA PRIVATE KEY-----\nSYNTHETIC\n-----END RSA PRIVATE KEY-----",
        "host": "http://example.local:1234 and localhost:5678",
        "scratch": "/private/tmp/task and scratchpad/example",
        "number": 42,
        "ok": True,
    }
    path = source / "evidence.json"
    path.write_text(json.dumps(original))
    before = path.read_bytes()
    stage = tmp_path / "stage"
    shutil.copytree(source, stage)
    assert guard.scan(stage) == 1
    counts = prepare.prepare_copy(stage)
    assert counts["files_redacted"] == 1
    assert path.read_bytes() == before
    exported = json.loads((stage / path.name).read_text())
    assert exported["number"] == 42 and exported["ok"] is True
    assert exported["token"] == "[REDACTED_CREDENTIAL]"
    assert exported["private"] == "[REDACTED_PRIVATE_KEY]"
    assert guard.scan(stage) == 0
    once = (stage / path.name).read_bytes()
    assert prepare.prepare_copy(stage)["files_redacted"] == 0
    assert (stage / path.name).read_bytes() == once
    assert "SYNTHETIC_ONLY" not in capsys.readouterr().out


def test_jsonl_and_clean_binary_preserved(tmp_path):
    (tmp_path / "queue.jsonl").write_text(
        json.dumps({"path": "clones/Repo/file"}) + "\n" + json.dumps({"n": 1}) + "\n"
    )
    binary = b"\xff\x00\xfe"
    (tmp_path / "artifact.bin").write_bytes(binary)
    prepare.prepare_copy(tmp_path)
    assert [json.loads(x) for x in (tmp_path / "queue.jsonl").read_text().splitlines()][1] == {
        "n": 1
    }
    assert (tmp_path / "artifact.bin").read_bytes() == binary
    assert guard.scan(tmp_path) == 0


def test_binary_findings_still_block_after_preparation(tmp_path):
    (tmp_path / "artifact.bin").write_bytes(b"\xffghp_SYNTHETIC")
    prepare.prepare_copy(tmp_path)
    assert guard.scan(tmp_path) == 1


@pytest.mark.parametrize("content", ['{"clones/a": 1, "scratchpad/a": 2}', '{"path": "clones/a"'])
def test_invalid_or_colliding_json_fails_without_partial_write(tmp_path, content):
    (tmp_path / "a.txt").write_text("clones/a")
    (tmp_path / "bad.json").write_text(content)
    with pytest.raises(ValueError):
        prepare.prepare_copy(tmp_path)
    assert (tmp_path / "a.txt").read_text() == "clones/a"


def test_symlink_and_empty_copy_fail(tmp_path):
    with pytest.raises(ValueError, match="empty"):
        prepare.prepare_copy(tmp_path)
    (tmp_path / "link").symlink_to(tmp_path.parent, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        prepare.prepare_copy(tmp_path)


def test_named_legacy_process_capture_is_wrapped_without_losing_output(tmp_path):
    path = tmp_path / sorted(prepare.TEXT_CAPTURE_JSON)[0]
    path.parent.mkdir(parents=True)
    path.write_text("process warning\n" + json.dumps({"path": "clones/Repo/file"}))
    prepare.prepare_copy(tmp_path)
    value = json.loads(path.read_text())
    assert value["capture_format"] == "raw-process-output"
    assert value["text"].startswith("process warning\n")
    assert "[LOCAL_WORKSPACE]/Repo/file" in value["text"]
    assert guard.scan(tmp_path) == 0


@pytest.mark.parametrize(
    "prefix", ["sk-ant-", "sk-proj-", "ghp_", "github_pat_", "lsv2_", "crsr_", "AIza"]
)
def test_every_credential_prefix_is_redacted_without_leaving_a_suffix(tmp_path, prefix):
    path = tmp_path / "evidence.txt"
    path.write_text(prefix + "SYNTHETIC_ONLY")
    prepare.prepare_copy(tmp_path)
    assert path.read_text() == "[REDACTED_CREDENTIAL]"
    assert guard.scan(tmp_path) == 0


def test_unreadable_traversal_stops_export_before_writes(tmp_path, monkeypatch):
    path = tmp_path / "a.txt"
    path.write_text("clones/a")

    def walk(self, *, on_error, **kwargs):
        yield self, [], ["a.txt"]
        on_error(OSError("injected"))

    monkeypatch.setattr(Path, "walk", walk)
    with pytest.raises(OSError):
        prepare.prepare_copy(tmp_path)
    assert path.read_text() == "clones/a"


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
def test_encoded_json_is_redacted_before_clean_shortcut(tmp_path, suffix, capsys):
    path = tmp_path / ("evidence" + suffix)
    path.write_text(
        r'{"ghp\u005fSYNTHETIC_KEY": [{"path": "\/Users\/example", "token": "ghp\u005fSYNTHETIC_ONLY", "number": 42}]}'
    )
    counts = prepare.prepare_copy(tmp_path)
    value = json.loads(path.read_text())
    assert list(value) == ["[REDACTED_CREDENTIAL]"]
    assert value["[REDACTED_CREDENTIAL]"][0] == {
        "path": "[LOCAL_HOME]/",
        "token": "[REDACTED_CREDENTIAL]",
        "number": 42,
    }
    assert counts["credential"] == 2
    assert counts["files_redacted"] == 1
    assert guard.scan(tmp_path) == 0
    assert "SYNTHETIC_ONLY" not in capsys.readouterr().out


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
def test_clean_structured_bytes_preserved(tmp_path, suffix, monkeypatch):
    path = tmp_path / ("clean" + suffix)
    original = b'{ "example": "ghp\\\\u005fEXAMPLE", "public": "caf\\u00e9", "n": 42 }\n'
    path.write_bytes(original)
    examined = []
    real_read = Path.read_bytes

    def record_read(self):
        examined.append(self)
        return real_read(self)

    monkeypatch.setattr(Path, "read_bytes", record_read)
    counts = prepare.prepare_copy(tmp_path)
    assert examined == [path]
    assert counts["files_scanned"] == 1
    assert counts["files_redacted"] == 0
    assert path.read_bytes() == original


def test_malformed_json_with_escaped_findings_fails_before_any_write(tmp_path):
    path = tmp_path / "a.txt"
    path.write_text("ghp_SYNTHETIC_ONLY")
    (tmp_path / "invalid.json").write_text(r'{"token": "ghp\u005fSYNTHETIC_ONLY"')
    with pytest.raises(ValueError, match="structured data"):
        prepare.prepare_copy(tmp_path)
    assert path.read_text() == "ghp_SYNTHETIC_ONLY"


def test_clean_historical_process_capture_is_preserved(tmp_path, monkeypatch):
    path = tmp_path / "capture.json"
    original = b'[ {"ok": true} ]\n[ {"public": "caf\\u00e9"} ]\n'
    path.write_bytes(original)
    examined = []
    real_read = Path.read_bytes

    def record_read(self):
        examined.append(self)
        return real_read(self)

    monkeypatch.setattr(Path, "read_bytes", record_read)
    counts = prepare.prepare_copy(tmp_path)
    assert examined == [path]
    assert counts["files_scanned"] == 1
    assert counts["files_redacted"] == 0
    assert path.read_bytes() == original


@pytest.mark.parametrize("suffix", [".txt", ".json", ".jsonl"])
@pytest.mark.parametrize("kind", ["", "ENCRYPTED ", "RSA ", "OPENSSH ", "EC ", "DSA "])
@pytest.mark.parametrize("footer", ["", "\n-----END OTHER PRIVATE KEY-----"])
def test_incomplete_private_key_fails_before_any_write(tmp_path, monkeypatch, suffix, kind, footer):
    content = f"-----BEGIN {kind}PRIVATE KEY-----\nSYNTHETIC_KEY_MATERIAL{footer}"
    if suffix != ".txt":
        content = json.dumps({"key": content})
    first = tmp_path / "a.txt"
    first.write_text("clones/example")
    invalid = tmp_path / ("z" + suffix)
    invalid.write_text(content)
    monkeypatch.setattr(
        Path, "walk", lambda self, **kwargs: iter([(self, [], [first.name, invalid.name])])
    )
    with pytest.raises(ValueError):
        prepare.prepare_copy(tmp_path)
    assert first.read_text() == "clones/example"
    assert invalid.read_text() == content


@pytest.mark.parametrize("suffix", [".txt", ".json", ".jsonl"])
def test_documented_private_key_fixture_can_survive_publication_copy(tmp_path, suffix):
    path = tmp_path / ("historical-evidence" + suffix)
    content = "-----BEGIN PRIVATE KEY-----\nSYNTHETIC_TEST_MARKER"
    if suffix != ".txt":
        content = json.dumps({"fixture": content})
    path.write_text(content)
    allowlist = tmp_path / ".publication-allow"
    allowlist.write_text(
        f"{path.name}:private-key # Reviewed synthetic historical evidence.\n"
    )

    counts = prepare.prepare_copy(tmp_path, allowlist)

    assert counts["files_redacted"] == 0
    assert path.read_text() == content
    assert guard.scan(tmp_path, allowlist) == 0


def test_invalid_publication_allowlist_fails_before_any_write(tmp_path):
    path = tmp_path / "evidence.txt"
    path.write_text("clones/example")
    allowlist = tmp_path / ".publication-allow"
    allowlist.write_text("evidence.txt:private-key\n")

    with pytest.raises(ValueError, match="allowlist"):
        prepare.prepare_copy(tmp_path, allowlist)

    assert path.read_text() == "clones/example"


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
@pytest.mark.parametrize(
    "number",
    ["NaN", "Infinity", "-Infinity", "1e400"],
)
def test_non_finite_json_numbers_fail_before_any_write(tmp_path, monkeypatch, suffix, number):
    first = tmp_path / "a.txt"
    first.write_text("clones/example")
    invalid = tmp_path / ("z" + suffix)
    payload = f'{{"path": "clones/example", "value": {number}}}'
    if suffix == ".jsonl":
        payload = '{"path": "clones/earlier-record"}\n' + payload + "\n"
    invalid.write_text(payload)
    monkeypatch.setattr(
        Path, "walk", lambda self, **kwargs: iter([(self, [], [first.name, invalid.name])])
    )
    with pytest.raises(ValueError, match="structured data"):
        prepare.prepare_copy(tmp_path)
    assert first.read_text() == "clones/example"
    assert invalid.read_text() == payload


@pytest.mark.parametrize("suffix", [".json", ".jsonl"])
@pytest.mark.parametrize(
    "content",
    [
        '{"duplicate": 1, "duplicate": 2, "path": "clones/example"}',
        r'{"duplicate": "ghp\u005fSYNTHETIC", "duplicate": "public"}',
        '{"nested": [{"duplicate": 1, "duplicate": 2}], "path": "clones/example"}',
        r'{"duplicate": 1, "dupli\u0063ate": 2, "path": "clones/example"}',
    ],
)
def test_duplicate_json_keys_fail_before_any_write(tmp_path, monkeypatch, suffix, content):
    first = tmp_path / "a.txt"
    first.write_text("clones/example")
    invalid = tmp_path / ("z" + suffix)
    if suffix == ".jsonl":
        content = '{"path": "clones/earlier-record"}\n' + content + "\n"
    invalid.write_text(content)
    monkeypatch.setattr(
        Path, "walk", lambda self, **kwargs: iter([(self, [], [first.name, invalid.name])])
    )
    with pytest.raises(ValueError, match="structured data"):
        prepare.prepare_copy(tmp_path)
    assert first.read_text() == "clones/example"
    assert invalid.read_text() == content


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
def test_full_private_key_blocks_are_removed(tmp_path, label, suffix):
    path = tmp_path / ("evidence" + suffix)
    content = f"before\n-----BEGIN {label}-----\nSYNTHETIC_MATERIAL\n-----END {label}-----\nafter"
    if suffix != ".txt":
        content = json.dumps({"key": content}).replace("PRIVATE", r"PRIV\u0041TE")
    path.write_text(content)
    assert guard.scan(tmp_path) == 1
    counts = prepare.prepare_copy(tmp_path)
    assert counts["files_scanned"] == 1
    assert counts["private-key"] == 1
    exported = path.read_text() if suffix == ".txt" else json.loads(path.read_text())["key"]
    assert exported == "before\n[REDACTED_PRIVATE_KEY]\nafter"
    assert guard.scan(tmp_path) == 0


def test_nested_private_key_header_cannot_hide_incomplete_block(tmp_path):
    path = tmp_path / "evidence.txt"
    original = "-----BEGIN PRIVATE KEY-----\n-----BEGIN RSA PRIVATE KEY-----\nSYNTHETIC\n-----END PRIVATE KEY-----"
    path.write_text(original)
    with pytest.raises(ValueError):
        prepare.prepare_copy(tmp_path)
    assert path.read_text() == original


def test_preparation_rejects_a_named_pipe_instead_of_hanging(tmp_path):
    """A FIFO in the staging tree must fail closed, not block preparation forever.

    `read_bytes()` on a FIFO waits for a writer that never arrives, so without a
    regular-file check this hangs rather than refusing. The scanner already rejects
    non-regular files; preparation disagreeing with it means the stricter of the two is
    the one that never gets to run.
    """
    stage = tmp_path / "stage"
    stage.mkdir()
    (stage / "clean.txt").write_text("nothing sensitive here\n", encoding="utf-8")
    os.mkfifo(stage / "capture")

    with pytest.raises(ValueError, match="not a regular file"):
        prepare.prepare_copy(stage)
