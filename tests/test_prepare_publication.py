"""Publication export must preserve originals and keep the safety guard binding."""

from __future__ import annotations

import importlib
import json
import os
import re
import shutil
import zipfile
from html import escape
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
    allowlist.write_text(f"{path.name}:private-key # Reviewed synthetic historical evidence.\n")

    counts = prepare.prepare_copy(tmp_path, allowlist)

    assert counts["files_redacted"] == 0
    assert path.read_text() == content
    assert guard.scan(tmp_path, allowlist) == 0


@pytest.mark.parametrize("suffix", [".txt", ".json", ".jsonl"])
def test_reviewed_incomplete_pem_still_redacts_complete_blocks_and_other_rules(tmp_path, suffix):
    source = tmp_path / "source"
    source.mkdir()
    incomplete = "-----BEGIN PRIVATE KEY-----\nSYNTHETIC_REVIEWED_FIXTURE"
    text = (
        "-----BEGIN RSA PRIVATE KEY-----\nSYNTHETIC_COMPLETE_BLOCK\n"
        "-----END RSA PRIVATE KEY-----\n"
        "ghp_SYNTHETIC_SUFFIX /Users/SYNTHETIC_USER/notes\n" + incomplete
    )
    expected = "[REDACTED_PRIVATE_KEY]\n[REDACTED_CREDENTIAL] [LOCAL_HOME]/notes\n" + incomplete
    path = source / ("reviewed" + suffix)
    path.write_text(text if suffix == ".txt" else json.dumps({"note": text}) + "\n")
    policy = source / ".publication-allow"
    policy.write_text(f"{path.name}:private-key # Reviewed synthetic incomplete fixture.\n")
    originals = {p.name: p.read_bytes() for p in source.iterdir()}
    stage = tmp_path / "stage"
    shutil.copytree(source, stage)
    allowlist = stage / policy.name
    assert guard.scan(stage, allowlist) == 1

    counts = prepare.prepare_copy(stage, allowlist)

    exported = (stage / path.name).read_text()
    assert (exported if suffix == ".txt" else json.loads(exported)["note"]) == expected
    assert counts["private-key"] == counts["credential"] == counts["home-path"] == 1
    assert counts["files_redacted"] == 1
    assert (stage / policy.name).read_bytes() == originals[policy.name]
    assert guard.scan(stage, allowlist) == 0
    prepared = (stage / path.name).read_bytes()
    assert prepare.prepare_copy(stage, allowlist)["files_redacted"] == 0
    assert (stage / path.name).read_bytes() == prepared
    assert {p.name: p.read_bytes() for p in source.iterdir()} == originals


@pytest.mark.parametrize("suffix", [".txt", ".json", ".jsonl"])
@pytest.mark.parametrize("exception_rule", ["private-key", "scratch-path"])
def test_incomplete_pem_exception_requires_exact_path_and_rule(
    tmp_path, monkeypatch, suffix, exception_rule
):
    first = tmp_path / "a.txt"
    first.write_text("clones/public-note")
    reviewed = tmp_path / ("reviewed" + suffix)
    text = "-----BEGIN PRIVATE KEY-----\nSYNTHETIC_REVIEWED_FIXTURE"
    reviewed.write_text(text if suffix == ".txt" else json.dumps({"note": text}) + "\n")
    sibling_dir = tmp_path / "unreviewed"
    sibling_dir.mkdir()
    sibling = sibling_dir / reviewed.name
    sibling.write_bytes(
        reviewed.read_bytes() if exception_rule == "private-key" else b"Public sibling\n"
    )
    allowlist = tmp_path / ".publication-allow"
    allowlist.write_text(f"{reviewed.name}:{exception_rule} # Reviewed exact-file fixture.\n")
    originals = {p: p.read_bytes() for p in (first, reviewed, sibling, allowlist)}
    # Queue a supported rewrite before encountering the unapproved incomplete
    # block. A same-basename file in a subdirectory must not inherit approval.
    monkeypatch.setattr(
        Path,
        "walk",
        lambda self, **kwargs: iter(
            [
                (self, [sibling_dir.name], [first.name, reviewed.name, allowlist.name]),
                (sibling_dir, [], [sibling.name]),
            ]
        ),
    )

    with pytest.raises(ValueError) as error:
        prepare.prepare_copy(tmp_path, allowlist)

    assert "incomplete private-key block" in str(error.value.__cause__)
    assert {p: p.read_bytes() for p in originals} == originals
    assert guard.scan(tmp_path, allowlist) == 1


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


def test_compressed_docx_preserved_then_guarded(tmp_path, capsys):
    import zipfile

    path = tmp_path / "report.docx"
    xml = '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:r><w:t>gh</w:t></w:r><w:r><w:t>p_SYNTHETIC</w:t></w:r></w:p></w:document>'
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", xml)
    original = path.read_bytes()
    assert not any(pattern.search(original) for pattern in guard.RULES.values())
    prepare.prepare_copy(tmp_path)
    assert path.read_bytes() == original
    assert guard.scan(tmp_path) == 1
    assert "SYNTHETIC" not in capsys.readouterr().out


# Independent synthetic witnesses, including bare marker fallbacks. Expected
# output checks the entire value so a scanner-clean suffix is not mistaken for
# complete redaction. This table must grow if the shared vocabulary changes.
PUBLICATION_ALTERNATIVES = {
    "home-path": {
        "/Users/": [
            ("/Users/SYNTHETIC_USER/notes", "[LOCAL_HOME]/notes"),
            ("/Users/", "[LOCAL_HOME]/"),
        ],
    },
    "credential": {
        prefix: [(prefix + "SYNTHETIC_SUFFIX-123_abc", "[REDACTED_CREDENTIAL]")]
        for prefix in ("sk-ant-", "sk-proj-", "ghp_", "github_pat_", "lsv2_", "crsr_", "AIza")
    },
    "scratch-path": {
        marker: [(marker + "public-note", "[LOCAL_WORKSPACE]/public-note")]
        for marker in ("clones/", "/private/tmp/", "scratchpad/")
    },
    "internal-host": {
        ".local:": [("SYNTHETIC_HOST.local:8080", "[LOCAL_HOST]"), (".local:", "[LOCAL_HOST]")],
        # Scanner and replacement both require port digits after localhost:; bare
        # `localhost:` is intentionally asymmetric with the bare `.local:` marker.
        "localhost:": [("localhost:8080", "[LOCAL_HOST]")],
    },
}


def test_scanner_vocabulary_has_explicit_preparation_dispositions():
    patterns = module("publication_patterns")
    assert guard.RULES is patterns.SCANNER_RULES
    assert prepare.REPLACEMENTS is patterns.TEXT_REPLACEMENTS
    assert set(guard.RULES) == set(patterns.VOCABULARY) == set(patterns.PREPARATION_DISPOSITIONS)
    assert {rule for rule, _, _ in prepare.REPLACEMENTS} == set(guard.RULES)
    for rule, alternatives in patterns.VOCABULARY.items():
        assert patterns.PREPARATION_DISPOSITIONS[rule]
        if rule == "private-key":
            # The grammar is open to qualified labels; complete/incomplete,
            # exact-file exception and binary controls are exercised separately.
            assert alternatives == (patterns.PRIVATE_KEY_HEADER_TEXT,)
            continue
        assert set(alternatives) == set(PUBLICATION_ALTERNATIVES[rule])
        # Do not require scanner/redactor regex equality, but every declared
        # lexical alternative must still appear in the full-value redactor.
        redactor_sources = [
            pattern.pattern for name, pattern, _ in patterns.TEXT_REPLACEMENTS if name == rule
        ]
        for alternative in alternatives:
            escaped = re.escape(alternative)
            assert any(
                alternative in source or escaped in source for source in redactor_sources
            ), f"{rule} alternative {alternative!r} missing from redactor"


@pytest.mark.parametrize(
    ("suffix", "escaped"),
    [(".txt", False), (".json", False), (".json", True), (".jsonl", False), (".jsonl", True)],
)
@pytest.mark.parametrize(
    ("rule", "original", "expected"),
    [
        (rule, original, expected)
        for rule, alternatives in PUBLICATION_ALTERNATIVES.items()
        for cases in alternatives.values()
        for original, expected in cases
    ],
)
def test_shared_vocabulary_through_real_preparation_and_scan(
    tmp_path, rule, original, expected, suffix, escaped
):
    source = tmp_path / "source"
    source.mkdir()
    path = source / ("evidence" + suffix)
    text = "Public before | " + original + " | Public after"
    expected_text = "Public before | " + expected + " | Public after"
    content = text
    if suffix != ".txt":
        # Exercise both object keys and nested values for every alternative.
        content = json.dumps({text: [{"note": text}], "public": 42})
        if escaped:
            # Hide every marker from the raw-byte scan to require JSON decoding.
            encoded_text = '"' + "".join(rf"\u{ord(char):04x}" for char in text) + '"'
            content = content.replace(json.dumps(text), encoded_text)
            assert not any(pattern.search(content.encode()) for pattern in guard.RULES.values())
        if suffix == ".jsonl":
            content += '\n\n{"public": true}\n'
    path.write_text(content)
    before = path.read_bytes()
    stage = tmp_path / "stage"
    shutil.copytree(source, stage)
    assert guard.RULES[rule].search(original.encode())
    assert guard.scan(stage) == 1
    prepare.prepare_copy(stage)
    exported = (stage / path.name).read_text()
    if suffix == ".txt":
        assert exported == expected_text
    else:
        expected_record = {expected_text: [{"note": expected_text}], "public": 42}
        if suffix == ".json":
            assert json.loads(exported) == expected_record
        else:
            assert [json.loads(line) for line in exported.splitlines() if line.strip()] == [
                expected_record,
                {"public": True},
            ]
            assert exported.splitlines()[1] == ""
    # Full-value checks: suffixes, usernames, and host names must be gone, not
    # merely that a marker stops matching after a partial rewrite.
    for fragment in (
        "SYNTHETIC_SUFFIX",
        "SYNTHETIC_USER",
        "SYNTHETIC_HOST",
        "SYNTHETIC_ONLY",
    ):
        assert fragment not in exported
    assert path.read_bytes() == before
    assert guard.scan(stage) == 0


@pytest.mark.parametrize("suffix", [".txt", ".json", ".jsonl"])
@pytest.mark.parametrize(
    ("original", "expected", "expected_counts"),
    [
        pytest.param(
            "-----BEGIN PRIVATE KEY-----\n"
            "ghp_SYNTHETIC_SUFFIX /Users/SYNTHETIC_USER/clones/report "
            "SYNTHETIC_HOST.local:8080\n-----END PRIVATE KEY-----",
            "[REDACTED_PRIVATE_KEY]",
            {"private-key": 1},
            id="pem-before-contained-markers",
        ),
        pytest.param(
            "/Users/SYNTHETIC_USER/clones/report",
            "[LOCAL_HOME]/[LOCAL_WORKSPACE]/report",
            {"home-path": 1, "scratch-path": 1},
            id="full-home-before-bare-marker",
        ),
    ],
)
def test_overlapping_vocabulary_preserves_replacement_order(
    tmp_path, suffix, original, expected, expected_counts
):
    source = tmp_path / "source"
    source.mkdir()
    path = source / ("evidence" + suffix)
    text = "Public before | " + original + " | Public after"
    expected_text = "Public before | " + expected + " | Public after"
    path.write_text(text if suffix == ".txt" else json.dumps({"note": text}) + "\n")
    before = path.read_bytes()
    stage = tmp_path / "stage"
    shutil.copytree(source, stage)
    assert guard.scan(stage) == 1

    counts = prepare.prepare_copy(stage)

    exported = (stage / path.name).read_text()
    assert (exported if suffix == ".txt" else json.loads(exported)["note"]) == expected_text
    # PEM must consume its contents before other rules count them. The full
    # home rule must remove the username before the bare-prefix fallback runs.
    assert {rule: count for rule, count in counts.items() if count} == {
        **expected_counts,
        "files_scanned": 1,
        "files_redacted": 1,
    }
    assert guard.scan(stage) == 0
    prepared_bytes = (stage / path.name).read_bytes()
    assert prepare.prepare_copy(stage)["files_redacted"] == 0
    assert (stage / path.name).read_bytes() == prepared_bytes
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "marker",
    [
        original
        for alternatives in PUBLICATION_ALTERNATIVES.values()
        for cases in alternatives.values()
        for original, _ in cases
    ],
)
def test_shared_vocabulary_binary_outcome_is_preserve_and_scan(tmp_path, marker):
    path = tmp_path / "evidence.bin"
    original = b"\xff" + marker.encode("ascii")
    path.write_bytes(original)
    counts = prepare.prepare_copy(tmp_path)
    assert counts["files_redacted"] == 0
    assert path.read_bytes() == original
    assert guard.scan(tmp_path) == 1


@pytest.mark.parametrize(
    ("rule", "marker"),
    [
        (rule, original)
        for rule, alternatives in PUBLICATION_ALTERNATIVES.items()
        for cases in alternatives.values()
        for original, _ in cases
    ]
    + [
        ("private-key", "-----BEGIN PRIVATE KEY-----\nSYNTHETIC_MATERIAL"),
        (
            "private-key",
            "-----BEGIN RSA PRIVATE KEY-----\nSYNTHETIC_MATERIAL\n-----END RSA PRIVATE KEY-----",
        ),
    ],
)
def test_packaged_vocabulary_is_preserved_then_scan_rejected(tmp_path, capsys, rule, marker):
    source = tmp_path / "source"
    source.mkdir()
    path = source / "report.docx"
    # No lexical marker exists in raw XML: Word may split it across text runs.
    runs = "".join(f"<w:r><w:t>{escape(char)}</w:t></w:r>" for char in marker)
    xml = (
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body><w:p>{runs}</w:p></w:body></w:document>"
    )
    assert not guard.RULES[rule].search(xml.encode())
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", xml)
    originals = {path.name: path.read_bytes(), "note.txt": b"clones/public-note\n"}
    (source / "note.txt").write_bytes(originals["note.txt"])
    assert not guard.RULES[rule].search(originals[path.name])
    stage = tmp_path / "stage"
    shutil.copytree(source, stage)

    counts = prepare.prepare_copy(stage)

    assert counts["files_scanned"] == 2
    assert counts["files_redacted"] == 1
    assert (stage / path.name).read_bytes() == originals[path.name]
    assert (stage / "note.txt").read_bytes() == b"[LOCAL_WORKSPACE]/public-note\n"
    assert guard.scan(stage) == 1
    output = capsys.readouterr()
    assert f"report.docx:1: {rule} (1 hit(s))" in output.out
    assert "errors=0" in output.out
    assert marker not in output.out + output.err
    assert "SYNTHETIC" not in output.out + output.err
    assert not output.err
    assert {p.name: p.read_bytes() for p in source.iterdir()} == originals


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
@pytest.mark.parametrize("footer", ["matching", "missing", "mismatched"])
def test_binary_pem_is_preserved_and_scan_rejected(tmp_path, capsys, label, footer):
    source = tmp_path / "source"
    source.mkdir()
    content = f"-----BEGIN {label}-----\nSYNTHETIC_MATERIAL\n"
    if footer != "missing":
        end_label = label if footer == "matching" else "OTHER PRIVATE KEY"
        content += f"-----END {end_label}-----\n"
    originals = {
        "evidence.bin": b"\xff" + content.encode("ascii"),
        "report.txt": b"clones/public-note\n",
    }
    for name, original in originals.items():
        (source / name).write_bytes(original)
    stage = tmp_path / "stage"
    shutil.copytree(source, stage)

    counts = prepare.prepare_copy(stage)

    # Binary PEM remains a scanner finding even when its text equivalent would
    # be redacted or rejected. Other supported text in the copy still prepares.
    assert counts["files_scanned"] == 2
    assert counts["files_redacted"] == 1
    assert counts["private-key"] == 0
    assert (stage / "evidence.bin").read_bytes() == originals["evidence.bin"]
    assert (stage / "report.txt").read_bytes() == b"[LOCAL_WORKSPACE]/public-note\n"
    assert guard.scan(stage) == 1
    output = capsys.readouterr()
    assert "evidence.bin:1: private-key (1 hit(s))" in output.out
    assert "private-key=1" in output.out
    assert "SYNTHETIC_MATERIAL" not in output.out + output.err
    assert not output.err
    assert {path.name: path.read_bytes() for path in source.iterdir()} == originals
