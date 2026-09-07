# PAEM numerical correctness and config-consumer audit

**Unit:** `D-audit-Portable-Alpha-Extension-Model--2026-09-07T04-47-31Z`  
**Repository / base:** `stranske/Portable-Alpha-Extension-Model`, `main` `59cb12be9d4b06434d41bc1b71612167ea6d9cfc`  
**Scope read:** `pa_core/config.py`, `pa_core/facade.py`, `pa_core/sweep.py`, `pa_core/sleeve_suggestor.py`, `pa_core/fees.py`, `pa_core/sim/`, `pa_core/agents/`, and corresponding tests only.  
**Verdict:** five verified defects. Confidence is high for all five: each has a deterministic executable trigger and a matched control. The supplied current-head CI is green (`34015303572`); focused current-head tests also passed: 56 passed, 1 skipped (`numeric_pytest.out`). Green tests do not exercise these cross-consumer paths.

## Reproduction

Run the non-mutating proof exactly from this artifact directory:

```sh
PYTHONPATH=<target-repository-root> \
  /tmp/paem-audit-20260907-venv/bin/python numeric_repro.py
```

Recorded output is in `numeric_repro.out`. It uses only synthetic zero index returns, fixed seeds, and no repo writes.

## Findings

### N1 — Alpha-share sweeps report unchanged economics while their displayed parameters change

**Severity:** High  
**Evidence:** `pa_core/sweep.py:606-611` creates each case with `model_copy`, while the actual agent weights and lever extras are compiled only by `ModelConfig`'s validation pipeline at `pa_core/config.py:551-558` and `pa_core/config.py:674-704`. The sweep then builds agents from the stale compiled list at `pa_core/sweep.py:714-725`. The normal revalidation path is correct (`pa_core/facade.py:256-258`), and the existing regression only covers that route (`tests/test_config.py:102-141`).

**Trigger / expected / actual:** A monthly `alpha_shares` sweep with `theta_extpa=0` and `theta_extpa=1`, zero volatility, and fixed seed should change ExternalPA's annual return because `ExternalPAAgent` applies `theta_extpa` at `pa_core/agents/external_pa.py:10-25`. The sweep instead reports an exact `0.000000000000` difference; matched `run_single` controls made through model validation differ by `0.268241794563`.

**Impact:** A user can see distinct alpha-share rows and choose among them even though the evaluated agent exposures are identical. Capital-allocation, `active_share`, and benchmark-share convenience-field sweeps use the same stale-agent mechanism.

**Test gate:** Add `tests/test_sweep_config.py::test_alpha_share_sweep_recompiles_agents_for_each_override`: assert fixed-seed `theta_extpa=0` and `1` have unequal ExternalPA returns; deliberately replace the recompile with `model_copy` and assert that test fails, then revert.

**Dedup:** Related to closed #1915, but **not a duplicate**. #1915 fixed `model_dump` → `ModelConfig` revalidation; this is a separate `model_copy` bypass in the sweep consumer.

### N2 — Fee schedules disappear on the parameter-sweep path

**Severity:** High  
**Evidence:** `run_single` passes `run_cfg.fee_schedule` to the simulator at `pa_core/facade.py:472-484`. In contrast, the sweep invokes the same simulator without that argument at `pa_core/sweep.py:714-725`. The fee model itself correctly scales drag (`pa_core/fees.py:74-99`) and is covered only for direct simulation/single-run usage (`tests/test_fee_layer.py:151-225`).

**Trigger / expected / actual:** With a 10% InternalPA sleeve, 120 annual management bps, one fixed-seed grid point, and zero underlying returns, the sweep should lower InternalPA's annualized return. Actual sweep drag is `0.000000000000`; matched `run_single` control drag is `0.001199340220`.

**Impact:** Sweep results are gross while the supplied configuration and single-run comparison are net of configured fees, changing ranking/constraint decisions.

**Test gate:** Add `tests/test_fee_layer.py::test_run_sweep_applies_configured_fee_schedule`: assert the one-point sweep's InternalPA metric equals the corresponding fixed-seed `run_single` metric; deliberately omit `fee_schedule` from the sweep call and assert the test fails, then revert.

**Dedup:** Related to closed #1904, but **not a duplicate**. #1904 added the fee layer; this is an unconnected, actively used consumer.

### N3 — InternalPA financing is charged at full-fund size regardless of sleeve size

**Severity:** High  
**Evidence:** `pa_core/sim/internal_pa_financing.py:39-91` returns the configured monthly financing rate without a sleeve-weight transformation. `pa_core/agents/internal_pa.py:15-24` documents that contribution scaling is handled elsewhere, but subtracts that full matrix after scaling alpha by `alpha_share`. The normal agent compiler sets `alpha_share = internal_pa_capital / total_fund_capital` at `pa_core/config.py:696-704`; no later contribution layer scales the financing matrix.

**Trigger / expected / actual:** Set zero alpha and a deterministic 1% monthly internal-PA financing cost. A 100mm sleeve inside a 1000mm fund should contribute −0.1% per month if the configuration is a sleeve financing rate; a 1000mm sleeve should contribute −1%. Actual output is −1% for both (`small_sleeve_return=-0.010000000000`, `full_sleeve_return=-0.010000000000`).

**Impact:** Financing can be overstated by 10x for a 10% InternalPA allocation, distorting total return, CVaR, and sleeve optimization. This follows the code's explicit contribution-scaling contract; it would be a non-defect only if the configuration were intentionally redefined as a full-fund contribution drag, which conflicts with that contract and the field's sleeve wording.

**Test gate:** Add `tests/test_agents.py::test_internal_pa_financing_scales_with_alpha_share`: with zero alpha and 1% financing, assert 10%-share output is −0.001 and 100%-share output is −0.01; deliberately remove the share factor and assert failure, then revert.

**Dedup:** Related to closed #1849, but **not a duplicate**. #1849 introduced InternalPA financing; its current scaling is numerically wrong at partial allocations.

### N4 — Stochastic InternalPA financing breaks the sweep's common-random-number guarantee

**Severity:** Medium  
**Evidence:** The sweep states it resets all financing RNGs per combination at `pa_core/sweep.py:483-499`, but does so only when `financing_series is None` (`pa_core/sweep.py:598-604`). The standard financing streams are precomputed from clones at `pa_core/sweep.py:576-591`, so the condition is false. InternalPA financing is instead drawn from the original advancing `internal` RNG for each row at `pa_core/sweep.py:703-712`. The current CRN tests use configurations without stochastic InternalPA financing (`tests/test_sweep_common_random_numbers.py:8-63`).

**Trigger / expected / actual:** Hold InternalPA's economics constant while sweeping ExternalPA theta from 0.2 to 0.8. Its fixed-seed outcome should be equal across rows because CRN is promised and theta does not enter InternalPA. With `internal_pa_financing_sigma_month=0`, observed delta is `0.000000000000` (control). With 1% sigma, observed delta is `-0.000139485503`: row order changes the InternalPA draw.

**Impact:** Comparisons confound a swept parameter with unrelated financing noise; an optimizer or analyst can infer a theta effect that is only an RNG-order effect.

**Test gate:** Add `tests/test_sweep_common_random_numbers.py::test_internal_pa_stochastic_financing_uses_common_random_numbers`: duplicate otherwise identical rows with nonzero InternalPA financing sigma and assert frame equality; deliberately stop resetting the `internal` RNG and assert failure, then revert.

**Dedup:** Related to closed #1849 for the input surface, but **not a duplicate**; this is a sweep reproducibility/experimental-design error.

### N5 — Sleeve suggestions evaluate the original allocation, not their candidate allocation

**Severity:** High  
**Evidence:** `_evaluate_allocation` replaces the three capital fields with `model_copy` at `pa_core/sleeve_suggestor.py:264-287`, then builds agents from that stale compiled configuration at `pa_core/sleeve_suggestor.py:295-298`. Compiled capital shares live in `agents` (`pa_core/config.py:674-704`), so the candidate values do not reach agent returns. Existing sleeve tests verify rows/bounds and stream-cache reuse but not that a candidate changes its evaluated return (`tests/test_sleeve_suggestor.py:98-141`, `tests/test_sleeve_suggestor.py:402-444`).

**Trigger / expected / actual:** Compare cached candidate allocations of 100% InternalPA versus 100% ExternalPA under fixed synthetic streams. The candidate evaluator reports an exact `0.000000000000` total-return delta. Matched revalidated `run_single` controls differ by `0.795856326022`.

**Impact:** `suggest_sleeves` can rank or accept allocations using metrics from the input allocation, giving a false optimization result.

**Test gate:** Add `tests/test_sleeve_suggestor.py::test_candidate_allocation_is_recompiled_before_cached_stream_evaluation`: assert two materially different candidate allocations produce distinct Total return under the same cached streams; deliberately use `model_copy` without revalidation and assert failure, then revert.

**Dedup:** Related to closed #1915, but **not a duplicate**. It is a second production consumer that bypasses the closed issue's revalidation fix.

## Refuted candidates

- **Management-fee notional scaling is not defective.** `pa_core/fees.py:91-99` multiplies the computed full-sleeve drag by `notional_share`; `tests/test_fee_layer.py:74-83` covers the 25% control. The defect is only its omission from sweeps (N2).
- **Regime switching is not silently dropped from current sweeps.** `pa_core/sweep.py:661-691` constructs regime parameters and paths and passes both into `draw_joint_returns`; closed #1910 is implemented at this head.
- **The ordinary facade override path is not stale.** `pa_core/facade.py:256-258` revalidates the dumped configuration, unlike the two `model_copy` consumers above.

## Dedup summary

| Finding | Related closed issue | Duplicate? |
| --- | --- | --- |
| N1 | #1915 | No — sweep bypass |
| N2 | #1904 | No — fee consumer omitted |
| N3 | #1849 | No — partial-allocation scaling |
| N4 | #1849 | No — CRN/RNG-state handling |
| N5 | #1915 | No — sleeve-suggestor bypass |

Closed #1909–#1914 and #1916–#1919 were checked as supplied dedup context; no finding above repeats their financing-mode warning, regime implementation, annual-unit conversion, summary-statistic, spike validation, or numerical-edge-case scopes. Closed #1924 is not repeated: this audit did not challenge the active-share diminishing-return model.
