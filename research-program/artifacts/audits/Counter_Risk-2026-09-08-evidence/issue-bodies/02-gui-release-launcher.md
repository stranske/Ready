# [P1] Launch the GUI executable from the assembled bin directory

## Why

`src/counter_risk/build/release.py:281` places the release executable in the bin directory and `src/counter_risk/build/release.py:303` tells operators to double-click the GUI launcher. The shipped `run_counter_risk_gui.cmd:19` checks the development dist layout and line 24 checks the release root, then falls through to source/venv/global commands at lines 30–60. No branch checks the assembled bin directory. Static matched controls confirm the CLI launcher generator knows the bin path while the GUI launcher does not. On a machine with only the documented assembled tree, no existing branch reaches the packaged executable. Windows execution was not available locally.

## Scope

Align GUI launcher lookup with the assembled release layout while preserving source-checkout fallbacks and exit reporting.

## Non-Goals

No unrelated source or upstream-synced workflow changes. Scaffold-only or partial completion does NOT count as done; complete the observable gates below.

## Tasks

- [ ] Add an explicit assembled-bin executable lookup to `run_counter_risk_gui.cmd` before development and global fallbacks, passing the gui subcommand and preserving failure logs.
- [ ] Extend `tests/test_windows_gui_launcher.py` to cover the assembled-bin branch and retain the source and dist branches.
- [ ] Add a Windows execution gate in `.github/workflows/release.yml` that exercises the launcher selection with a controlled executable or command recorder in the assembled layout.

## Acceptance Criteria

- [ ] `python -m pytest tests/test_windows_gui_launcher.py -q` passes, including a regression requiring the bin branch before fallback lookup.
- [ ] A Windows smoke with only the assembled-bin command recorder available captures exactly one invocation with the gui argument; a nonzero controlled child result is reported as failure.
- [ ] Deliberate-break gate: remove the new bin branch in `run_counter_risk_gui.cmd`; the named launcher test and Windows command-recorder smoke must fail; restore the branch.

## Implementation Notes

Independent from payload preservation: a complete runnable binary still needs a launcher branch that selects it. Existing closed packaging issues address the CLI launcher, not this missing GUI path.
