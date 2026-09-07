## Why

`pa_core/sweep.py:610` and `pa_core/sleeve_suggestor.py:281` copy convenience fields without rebuilding the compiled agents consumed at `pa_core/agents/registry.py:57`. Compilation lives at `pa_core/config.py:674`. In deterministic probes, theta 0 versus 1 produces identical sweep returns while validated single-run controls differ by 0.268241794563. Two materially different cached sleeve allocations likewise have zero return delta versus 0.795856326022 in controls. This combines N1 and N5 as one shared root cause; closed issue #1915 covered round-trip revalidation, which these consumers bypass.

## Scope

Recompile derived agents for sweep and allocation overrides. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] In `pa_core/config.py`, expose or reuse a derived-agent refresh that preserves explicit custom agents and avoids converting already-monthly inputs twice.
- [ ] In `pa_core/sweep.py` and `pa_core/sleeve_suggestor.py`, refresh derived agents after changing capital and share fields before simulation; preserve the sweep policy allowing over-margin candidate exploration.
- [ ] Extend `tests/test_sweep_config.py` and `tests/test_sleeve_suggestor.py` with deterministic unequal-allocation controls for cached and uncached paths.

## Acceptance Criteria

- [ ] Theta endpoints and distinct capital candidates produce the corresponding validated-control metrics, and explicit custom-agent configurations retain their documented behavior.
- [ ] Run `pytest tests/test_sweep_config.py tests/test_sleeve_suggestor.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Bypass the derived-agent refresh using the original model_copy behavior; the new endpoint and candidate tests must fail; revert the deliberate break.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
