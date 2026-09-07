## Why

`pa_core/agents/internal_pa.py:24` subtracts the full financing rate after scaling alpha. Its docstring at line 18 assigns later scaling to contribution machinery, but `pa_core/portfolio/core.py:34` says inputs are already scaled and line 44 only sums them. With zero alpha and a 1% monthly financing rate, both a 10% sleeve and a 100% sleeve contribute -1%; the partial sleeve should contribute -0.1% under that contract. Related closed #1849 introduced this financing path.

## Scope

Scale InternalPA financing by sleeve contribution share. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] In `pa_core/agents/internal_pa.py`, apply the sleeve contribution weight to financing consistently with alpha; align the docstring with the actual scaling location.
- [ ] Extend `tests/test_agents.py` to cover 10%, 100% and zero shares with positive costs and negative carry, and confirm `simulate_agents` Total sums the corrected contributions.

## Acceptance Criteria

- [ ] At 1% financing and zero alpha, 10% and 100% shares contribute -0.001 and -0.01 monthly, respectively; negative carry keeps its sign.
- [ ] Run `pytest tests/test_agents.py tests/test_fee_layer.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Restore unscaled financing subtraction; the partial-allocation regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
