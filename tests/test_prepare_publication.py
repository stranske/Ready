"""Publication export must preserve originals and keep the safety guard binding."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


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
