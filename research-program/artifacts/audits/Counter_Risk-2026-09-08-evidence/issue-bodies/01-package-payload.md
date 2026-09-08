# [P1] Preserve the complete PyInstaller directory in assembled releases

## Why

`release.spec:40` creates an executable with excluded binaries and `release.spec:66` collects its runtime and data files into a directory. The spec sets `contents_directory="."` at `release.spec:57`. But `src/counter_risk/build/release.py:268` copies only the executable at line 284; `assemble_release` registers only that path at line 374. A lead-seat synthetic COLLECT-tree probe copied the executable but omitted both a companion-library sentinel and config. The installed Python runtime cannot rescue a distributed PyInstaller bootloader missing its bundled libraries. This is a verified assembly omission; a real Windows execution remains a required gate, not a claimed local result.

## Scope

Preserve runtime dependencies and config/templates of the existing one-directory build through assembly and exercise the assembled output.

## Non-Goals

No unrelated source or upstream-synced workflow changes. Scaffold-only or partial completion does NOT count as done; complete the observable gates below.

## Tasks

- [ ] In `src/counter_risk/build/release.py`, preserve the full output tree selected by `release.spec` when assembling the executable and include copied files in the release manifest.
- [ ] Extend `tests/test_release_bundle.py` with a fake COLLECT tree containing a companion library and nested config; assert these survive release assembly.
- [ ] Extend `.github/workflows/release.yml` to run the assembled executable from an unrelated working directory before upload, with a fixture or headless smoke that verifies actual output artifacts.

## Acceptance Criteria

- [ ] `python -m pytest tests/test_release_bundle.py -q` passes with a new payload-preservation regression that asserts library and data-file contents, not only executable existence.
- [ ] Deliberate-break gate: temporarily restore the single-file `shutil.copy2` behavior in `src/counter_risk/build/release.py`; the new payload-preservation test must fail for missing companions; revert the break and rerun.
- [ ] The Windows release smoke runs the assembled binary without a repository checkout or Python PATH dependency, returns success, and produces a schema-valid manifest from synthetic fixtures. Archive captured logs with the release build.

## Implementation Notes

Related closed issue #78 introduced packaging, but the concrete full-tree preservation gap persists. Do not expand this into changing runtime formats. Modern generic PyInstaller layouts may use an internal folder; this spec explicitly places companions alongside the executable. See https://pyinstaller.org/en/stable/operating-mode.html .
