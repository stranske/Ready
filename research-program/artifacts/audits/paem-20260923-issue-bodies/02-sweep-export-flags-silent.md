## Why (verified evidence)

Most shipped example configs (including `examples/scenarios/my_first_scenario.yml`) set `analysis_mode: returns`, which routes the CLI into the parameter-sweep branch (`pa_core/cli.py:1268-1272`). That branch writes Excel via `export_sweep_results` and returns at `:1445-1446` **before** the single-run export block that honors `--png` / `--pdf` / `--pptx` (`:1967-1970`). Sweep mode only handles `--packet` (`:1367-1405`), not the individual image flags documented in the module docstring (`pa_core/cli.py:7`). Users who run the documented integration shape therefore get sweep output with **no PNG** and no error:

```bash
python -m pa_core.cli --config examples/scenarios/my_first_scenario.yml \
  --index data/sp500tr_fred_divyield.csv --seed 42 --png --output out.xlsx
```

Observed on tip `a1a872e7`: exit 0, `out.xlsx` created, **zero** `*.png` files in the output directory. Expected: either a PNG beside the workbook or an explicit failure explaining sweep-mode limitations.

## Tasks

- [ ] In the sweep branch (`pa_core/cli.py:1268-1446`), honor `--png` / `--pdf` / `--pptx` / `--html` consistently with single-run mode — e.g. build the same summary figure used for `--packet` and call `write_figure_image` / packet helpers — or refuse early with a clear error when those flags are set without `--packet`.
- [ ] Add an integration test under `tests/` that runs the reproduction command in a temporary directory and asserts a PNG is created (or a non-zero exit with an explicit message if you choose the refuse path).
- [ ] Document the chosen behavior in `README.md` CLI export section if it differs from today’s implicit assumption.

## Acceptance Criteria

- Named test: `tests/test_cli_sweep_png_export.py::test_sweep_mode_honors_png_flag` (new) asserting PNG creation (or explicit error text) for `my_first_scenario.yml` with `--png`.
- Deliberate-break → revert: remove the sweep-branch PNG handling (or re-enable silent return) → named test FAILS → revert.

## Non-Goals

- Do not change Plotly/Kaleido version pins beyond what export already requires (#2287 scope).
- No unrelated CLI refactors or synced workflow edits.

_Surfaced by Track D audit 2026-09-23; verified on clone tip a1a872e7._
