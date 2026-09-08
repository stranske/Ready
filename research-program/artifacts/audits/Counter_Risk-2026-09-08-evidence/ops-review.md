# Counter_Risk ops/packaging/chat review — 2026-09-08

- **Clone tip**: `e2a1bacf37503217e00e467aa72198988777afa4`
- **Scope**: `src/counter_risk/{io,gui,build,chat,integrations}`, `runner_launch.py`, `runtime_paths.py`, `docs/gui_runner.md`, release scripts/workflows/tests
- **Dimensions**: 1 (correctness), 3 (wiring), 4 (function-level UX/operator path), 6 (missed opportunities), 8 (local tooling)
- **Mode**: research-only (no filing)
- **Dedup**: searched `issue-index.md` / `issues.txt` (120-issue snapshot) and prior audit `Counter_Risk-2026-09-07.md` (#1000–#1006). None of the findings below duplicate those seven compute/config/parser/telemetry defects.

---

## Verified findings (4)

### F1 — [BLOCKER] Release assembly copies only the PyInstaller stub, not the one-dir payload

**Severity**: BLOCKER  
**Reachability**: Every operator bundle from `python -m counter_risk.build.release` / `.github/workflows/release.yml`  
**Confidence**: High (spec + copy code; would revise if CI artifact inspection shows a full COLLECT tree inside `bin/`)

**Evidence**

`release.spec` builds a **one-dir** bundle (`EXE` with `exclude_binaries=True` + `COLLECT`), not a self-contained one-file exe:

```40:75:release.spec
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="counter-risk",
    ...
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    ...
    name="counter-risk",
)
```

`assemble_release` runs PyInstaller then copies **only** the bare executable into `bin/`, discarding the rest of `dist/counter-risk/` (binaries, zipfiles, bundled `config/`/`templates/` datas):

```268:285:src/counter_risk/build/release.py
def _copy_bundled_executable(root: Path, bundle_dir: Path) -> Path:
    spec_path = root / "release.spec"
    ...
    _run_pyinstaller(root, spec_path)
    built_executable = _expected_pyinstaller_output(root)
    ...
    bundle_bin_dir = bundle_dir / "bin"
    bundle_bin_dir.mkdir(parents=True, exist_ok=True)
    destination = bundle_bin_dir / built_executable.name
    shutil.copy2(built_executable, destination)
    return destination
```

**Why this breaks operators**: PyInstaller one-dir exes are bootloaders that load libraries and datas from sibling files (modern builds use an `_internal/` directory). Shipping the stub alone yields a non-functional `bin/counter-risk.exe` even before config-path logic is considered.

**Local tooling gap (dim 8)**: `tests/test_release_bundle.py` fakes `_run_pyinstaller` with a shell-script stub (`test_release_bundle_executable_runs_fixture_replay…`) and never asserts that COLLECT artifacts land beside the copied exe. `scripts/validate_release_bundle.sh` only checks that `bin/counter-risk(.exe)` exists as a file, not that it is runnable.

**Repro note**: Full PyInstaller build not run on this host (no `pyinstaller` in clone venv). Structural proof is from `release.spec` + `_copy_bundled_executable` (above). Windows CI uploads the bundle but does not execute the packaged exe (`release.yml:59-81`).

---

### F2 — [MAJOR] `run_counter_risk_gui.cmd` cannot launch the release-layout executable

**Severity**: MAJOR  
**Reachability**: Operators double-clicking `run_counter_risk_gui.cmd` inside `release/<version>/` (the path README and release workflow ship)  
**Confidence**: High

**Evidence**

Release places the executable at `bin/counter-risk.exe` (`src/counter_risk/build/release.py:281-284`). The CLI fallback launcher correctly targets that path (`src/counter_risk/build/release.py:163-168` in `_create_runner_file`).

The GUI launcher never probes `bin/`:

```19:26:run_counter_risk_gui.cmd
if exist "%~dp0dist\counter-risk\counter-risk.exe" (
    call :run_and_log "%~dp0dist\counter-risk\counter-risk.exe" gui
    goto :after_run
)

if exist "%~dp0counter-risk.exe" (
    call :run_and_log "%~dp0counter-risk.exe" gui
    goto :after_run
)
```

It then falls through to dev/source heuristics (`src/`, `.venv`, global `counter-risk`) and usually exits **9009** on a clean operator PC (`run_counter_risk_gui.cmd:64-72`).

**Matched-control repro** (probe output in `probes-ops-review.txt`):

```
Contains 'dist\\counter-risk\\counter-risk.exe': True
Contains 'bin\\counter-risk.exe': False
release._create_runner_file uses bin\\counter-risk.exe: True
```

**Declared vs consumed (dim 3)**: `docs/RELEASE_CHECKLIST.md:47-53` and `README_HOW_TO_RUN.md` (via `_write_readme`) tell operators to double-click `run_counter_risk_gui.cmd`, but the launcher targets dev-tree layouts, not the assembled `bin/` layout.

**Dedup**: no open/closed issue in the 120-issue snapshot mentions `run_counter_risk_gui` + `bin/counter-risk`.

---

### F3 — [MAJOR] Frozen GUI config resolution fails when bundle metadata lives beside `bin/`, not inside it

**Severity**: MAJOR (even if F1 is fixed by copying the full COLLECT tree into `bin/`, the hook still points at `bin/` while release copies operator `config/` to bundle root)  
**Reachability**: `counter-risk gui` / packaged exe with `sys.frozen=True` on the release folder layout  
**Confidence**: High on path logic; medium on end-to-end Windows GUI click (Tk not exercised here)

**Evidence**

Release copies workflow YAML to **`release/<version>/config/`** (bundle root):

```368:373:src/counter_risk/build/release.py
    config_src = root / "config"
    copied["config"] = _copy_tree_filtered(
        config_src,
        bundle_dir / "config",
        suffixes={".yml", ".yaml", ".json"},
    )
```

Runtime hook pins `COUNTER_RISK_BUNDLE_ROOT` to the **executable directory** (`bin/`), not the release root:

```10:17:pyinstaller_runtime_hook.py
def _resolve_bundle_root() -> Path:
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass).resolve()
    return Path(sys.executable).resolve().parent

os.environ.setdefault("COUNTER_RISK_BUNDLE_ROOT", str(_resolve_bundle_root()))
```

Frozen resolution searches only under those roots (`src/counter_risk/runtime_paths.py:49-60`). GUI resolves mode configs through this path **before** invoking the CLI:

```105:109:src/counter_risk/gui/runner.py
def _resolve_config_path(state: GuiRunState) -> Path:
    if state.config_path is not None:
        return resolve_runtime_path(state.config_path)
    run_mode = _normalize_run_mode(state.run_mode)
    return resolve_runtime_path(_RUN_MODE_TO_CONFIG[run_mode])
```

**Repro** (`probes-ops-review.txt`, simulated frozen layout):

```
COUNTER_RISK_BUNDLE_ROOT=<bundle>/bin
config at <bundle>/config/all_programs.yml
→ RuntimePathResolutionError: Searched locations: <bundle>/bin/config/all_programs.yml
Control: COUNTER_RISK_BUNDLE_ROOT=<bundle> → resolves successfully
```

**Secondary wiring hazard (dim 3)**: when frozen resolution fails, reconciliation/normalize fall back to source-tree paths derived from `__file__` (`src/counter_risk/pipeline/reconciliation.py:38-42`, `src/counter_risk/normalize.py:126-132`). In a real frozen process those parents point outside the operator bundle, not at the shipped `config/name_registry.yml`.

**Test blind spot (dim 8)**: `tests/pipeline/test_frozen_runtime_config.py:39` sets `COUNTER_RISK_BUNDLE_ROOT` to a synthetic `bundle-root/` that **contains** `config/`, not to `bin/` as the hook does — so CI green does not model the shipped release layout.

---

### F4 — [P2] Chat exposure parsing accepts non-finite manifest numerics and renders `"nan"` to operators

**Severity**: P2  
**Reachability**: Optional chat/Q&A when manifest `top_exposures` records contain non-finite floats (bad upstream data or future parser gaps)  
**Confidence**: High

**Evidence**

```700:714:src/counter_risk/chat/session.py
def _parse_float(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    ...
```

No `math.isfinite` guard. Formatted into operator-visible text:

```577:581:src/counter_risk/chat/session.py
    formatted = [
        f"{row['variant']}: {row['name']} ({_format_exposure_value(cast(float, row['value']))})"
        for row in top_rows
    ]
```

**Repro** (clone venv, `PYTHONPATH=src`):

```python
from counter_risk.chat import session as s
s._parse_float(float('nan'))  # → nan
s._format_exposure_value(float('nan'))  # → 'nan'
```

**Dedup**: distinct from filed #1000/#1002/#1006 (compute/parsers paths). Related pattern to closed #962 (risk ranking) but new surface: chat answers, not CSV ranking. No coverage in `tests/test_chat_session.py` (grep: no `nan`/`isfinite` cases).

---

## Rejected / downgraded candidates

| Candidate | Disposition | Reason |
|---|---|---|
| GUI worker-thread freeze / stdin `input()` discover | **Rejected (already fixed)** | `_DiscoveryPromptBridge` at `gui/runner.py:338-428`; dossier §8 confirms prior audit BLOCKER is stale |
| Runner.xlsm inert buttons | **Rejected (already fixed)** | VBA bindings present; outside today's new-defect bar |
| Frozen reconciliation `Path(__file__).parents[3]` crash | **Rejected as separate new issue** | `reconciliation.py:38-42` now routes through `resolve_runtime_path` with fallback; primary failure mode on release layout is F1/F3, not the pre-#cc8b73c crash |
| `docs/gui_runner.md` describes `dist/counter-risk/` operator install | **Downgraded doc drift** | True mismatch with assembled `release/<version>/bin/` layout (`docs/gui_runner.md:9-17`), but secondary to F1–F3 executable defects; fold into F2/F3 fix docs pass |
| Shipping `fixtures/` in release bundle | **Rejected** | Explicitly documented expected content (`docs/RELEASE_CHECKLIST.md:130`); operator mis-use risk noted but not a verified code defect |
| Chat transcript writes full guarded prompt to disk | **Rejected for this pass** | Policy/minor logging concern; no incorrect numeric output demonstrated |
| `validate_release_bundle.sh` requires `gh` on operator machines | **Rejected** | Maintainer-side script only |

---

## Summary table

| ID | Sev | Operator path? | Key paths | New vs dedup |
|---|---|---|---|---|
| F1 | BLOCKER | Yes — packaged exe | `release.spec:40-75`, `build/release.py:268-285` | NEW |
| F2 | MAJOR | Yes — GUI double-click | `run_counter_risk_gui.cmd:19-26`, `build/release.py:281-284` | NEW |
| F3 | MAJOR | Yes — frozen GUI/config | `pyinstaller_runtime_hook.py:10-17`, `gui/runner.py:105-109`, `runtime_paths.py:49-60` | NEW (related to F1 layout) |
| F4 | P2 | Yes — chat answers | `chat/session.py:700-714`, `:577-581` | NEW (chat surface) |

---

## Local tooling gaps (dimension 8)

1. **`tests/test_windows_gui_launcher.py`** asserts substring presence only; does not require a `bin\counter-risk.exe` probe matching release layout.
2. **`scripts/validate_release_bundle.sh`** checks artifact existence, not launcher→executable wiring or exe runnability (`:105-132`).
3. **`tests/pipeline/test_frozen_runtime_config.py`** models bundle root with embedded `config/`, not release’s split `bin/` exe + root-level `config/`.

---

## Probe artifact

See `probes-ops-review.txt` in this directory for command output backing F2–F4 simulations.
