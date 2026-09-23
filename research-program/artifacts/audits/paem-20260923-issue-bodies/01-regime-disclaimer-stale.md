## Why (verified evidence)

After regime support was wired into `run_parameter_sweep` (`pa_core/sweep.py:661-691` builds `regime_paths` and passes them to `draw_joint_returns`), the single source of truth for committee-facing caveats still tells analysts the opposite. `pa_core/reporting/disclaimers.py:20` states **"Regimes are ignored in parameter sweeps."** The same line is copied into `README.md:87` via `limitations_markdown()`, and `tests/test_model_limitations_1923.py:30` asserts the false phrase must remain. On tip `a1a872e7`, a sweep with two-state regimes (`idx_sigma_multiplier=3.0` on the stress state) versus an identical config without `regimes` yields `Total` `terminal_AnnReturn` **0.02357** vs **0.03127** (Δ **0.0077**) for the first grid point — regimes clearly move sweep outcomes. Board packs and README therefore mislead users configuring crisis regimes for grid exploration.

**Reproduction:**

```bash
pip install -e .
python - <<'PY'
import pandas as pd
from pa_core.config import load_config, RegimeConfig
from pa_core import sweep as sweep_module
from pa_core.random import spawn_agent_rngs, spawn_rngs
from pa_core.contracts import SUMMARY_AGENT_COLUMN, SUMMARY_ANN_RETURN_COLUMN
idx = pd.Series([0.01, -0.02, 0.015] * 4)
base = load_config("examples/scenarios/my_first_scenario.yml").model_copy(
    update={"N_SIMULATIONS": 400, "N_MONTHS": 12, "analysis_mode": "returns"}
)
with_reg = base.model_copy(update={
    "regimes": [RegimeConfig(name="calm"), RegimeConfig(name="stress", idx_sigma_multiplier=3.0)],
    "regime_transition": [[0.5, 0.5], [0.5, 0.5]],
    "regime_start": "calm",
})
def total_ann(cfg):
    rr = spawn_rngs(42, 1)[0]; fin = spawn_agent_rngs(42, ["internal", "external_pa", "active_ext"])
    s = sweep_module.run_parameter_sweep(cfg, idx, rr, fin, seed=42)[0]["summary"]
    return float(s[s[SUMMARY_AGENT_COLUMN]=="Total"].iloc[0][SUMMARY_ANN_RETURN_COLUMN])
print("plain", total_ann(base), "regime", total_ann(with_reg))
PY
```

Expected: documentation states regimes are honored in sweeps when configured. Observed: disclaimer/README still say they are ignored.

## Tasks

- [ ] Replace the stale bullet at `pa_core/reporting/disclaimers.py:20` with accurate text (e.g. regimes apply in sweeps when `regimes`/`regime_transition` are configured; cite `pa_core/sweep.py:661-691`).
- [ ] Regenerate the README limitations section from `limitations_markdown()` so `README.md:87` matches (`tests/test_readme_documents_limitations` already enforces inclusion).
- [ ] Update `tests/test_model_limitations_1923.py:26-40` to require the corrected caveat wording instead of `"regimes are ignored"`.
- [ ] Align `docs/guides/PARAMETER_GUIDE.md` regime/sweep language if it still repeats the old claim.

## Acceptance Criteria

- Named test: `tests/test_model_limitations_1923.py::test_limitations_cover_required_caveats` (updated assertions) plus a new test `test_regime_sweep_changes_metrics_when_configured` that runs the reproduction snippet above and asserts `abs(regime - plain) > 1e-4`.
- Deliberate-break → revert: restore the old `"Regimes are ignored in parameter sweeps."` string at `disclaimers.py:20` → the new metric-difference test must FAIL → revert.

## Non-Goals

- Do not remove or weaken regime simulation logic in `pa_core/sweep.py`.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by Track D audit 2026-09-23; verified on clone tip a1a872e7 with live sweep comparison._
