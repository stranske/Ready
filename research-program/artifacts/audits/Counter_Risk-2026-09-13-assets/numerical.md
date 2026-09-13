# Counter_Risk numerical audit

Unit: `D-audit-Counter_Risk--2026-09-13T18-41-41Z`  
Repository: `stranske/Counter_Risk`  
Frozen SHA: `6e2a87b27be9a23d388155e37ed01675b1e27dc7`  
Scope: `src/counter_risk/compute/`, `calculations/`, `parsers/`, `reports/`, `limits_config.py`, `name_matching.py`, `name_registry.py`, and associated tests/docs.  
Audit dimensions: `repo-audit:dimension-1` (numeric correctness) and `repo-audit:dimension-3` (config-to-consumer wiring).

## Executive result

Three new, reproducible defects survived the adversarial pass. They are not
duplicates of the September finite-number, boolean, alias-fallthrough, mixed-sign
HHI, or limit-denominator issues. The strongest problem is that a configured
canonical-key limit can be skipped for a known registry alias; its default path
only warns and produces no breach record.

Focused regression baseline passed: `92 passed` in the concentration, limits,
maturity-parser, and WAL test modules. That is expected: none covers the
three failing seams below.

## Findings

### N-1 [P1 / MAJOR] Aggregate concentration by counterparty before Top-N and HHI

**Dimension:** 1.  **Confidence:** high.

**Evidence.** `src/counter_risk/compute/rollups.py:575-581` groups values only by
`group_by` and appends each notional as a separate element; it never reads or
groups the required `counterparty` field. `src/counter_risk/compute/rollups.py:583-595`
then ranks those row values and squares their individual shares. The documented
contract says Top-N and HHI describe counterparties (`docs/concentration_metrics.md:26-30`,
`docs/concentration_metrics.md:38-45`). The production reshaper emits exactly
`variant`, `segment`, `counterparty`, and `notional` rows (`src/counter_risk/pipeline/run.py:2250-2287`)
and passes them straight to this function (`src/counter_risk/pipeline/run.py:2291-2301`).

**Reachable trigger.** A totals source can contain two rows for the same
counterparty in one variant/segment (split accounts, legal-entity detail, or a
duplicate source record). The production reshaper retains both rows. This is
especially material for `total`, which operators are instructed to use as the
whole-portfolio concentration view (`docs/concentration_metrics.md:71-76`).

**Expected versus actual.** For Alpha split into 60 + 60 and ten other
counterparties at 10 each, the 11 counterparty exposures are Alpha=120 and ten
Betas=10. Correct counterparty-level Top-5 is `1.0` and HHI is `0.3181818`.
Current code treats Alpha as two names, giving Top-5 `0.6818182` and HHI
`0.1694215`, materially understating concentration.

**Executable proof.** `numerical-proofs.py::proof_duplicate_counterparty_concentration`
reproduces these exact values with the frozen clone.

**Required fix/test gate.** Accumulate magnitude by a stable normalized
counterparty key within each group before sorting/calculating shares; preserve
the existing gross-exposure sign convention. Add a split-counterparty regression
in `tests/compute/test_concentration_metrics.py`, plus a pipeline-seam test
through `_build_concentration_exposure_rows`. The test must prove the split and
pre-aggregated forms produce identical Top-5, Top-10, and HHI.

**Disconfirming evidence.** Existing tests cover mixed signs, zero totals,
and distinct counterparties but no repeated counterparty in a group. This is
not the already-fixed mixed-sign HHI issue: current `rollups.py:585` correctly
uses magnitudes; the missing aggregation happens before that line.

**Overlap check.** Closed #475 introduced concentration output; #1023 corrects
operator threshold attribution; #1032 rejects non-finite pipeline inputs. None
requires counterparties to be consolidated before metric calculation. The
dedup corpus has no “duplicate counterparty” concentration finding.

### N-2 [P1 / MAJOR] Resolve configured canonical limit keys against registry aliases

**Dimension:** 3.  **Confidence:** high.

**Evidence.** Limits are documented/configured with a canonical entity key
(`config/limits.yml:13-17`; `docs/limit_monitoring.md:13-16`). The registry
maps the alias `Bank of America, NA` to canonical key `bank_of_america`
(`config/name_registry.yml:21-26`), and `resolve_counterparty` returns that key
(`src/counter_risk/normalize.py:164-197`). But pipeline parsing keeps the raw
display label (`src/counter_risk/parsers/cprs_fcm.py:160-194`) and passes it
unmodified to the limit builder (`src/counter_risk/pipeline/run.py:1645-1672`,
`src/counter_risk/pipeline/run.py:2316-2334`). `check_limits` and
`find_missing_limit_entities` compare `_normalize_entity_key` text only
(`src/counter_risk/compute/limits.py:88-89`, `src/counter_risk/compute/limits.py:201-220`,
`src/counter_risk/compute/limits.py:259-266`); neither calls the registry.

**Reachable trigger.** Configure the documented `bank_of_america` canonical key
with an absolute cap, then receive a CPRS-FCM total whose counterparty label is
the registry alias `Bank of America, NA`. This normal vendor-name variation is
already an explicit registry alias.

**Expected versus actual.** A $200 exposure against a $100
`bank_of_america` cap should create a fail/warning breach for that known entity.
Current code reports `bank_of_america` as missing and returns no breach. With
the default `strict_missing_entities: false` (`config/limits.yml:7-10`), the
pipeline continues after adding only a warning (`src/counter_risk/pipeline/run.py:2383-2393`).

**Executable proof.** `numerical-proofs.py::proof_limit_registry_bypass` proves
the registry resolves the alias to `bank_of_america`, while the actual limit
functions return a missing entity and `[]` breaches.

**Required fix/test gate.** Convert limit-target matching and missing-entity
checks to the same stable resolver/key used by the name registry (with an
explicit fallback rule for non-counterparty dimensions). Add a pipeline-seam
test that feeds a raw registered alias into `_build_limit_exposure_rows` and
proves a canonical-key limit breaches; retain a test for an unknown raw label
that must still warn/fail under the configured strictness.

**Disconfirming evidence.** Case and whitespace-only spelling changes do work
through `_normalize_entity_key`; this finding requires aliases whose canonical
key differs from normalized display text. The present `citibank` and `cme`
sample limits happen to match their display names, which masks the defect.

**Overlap check.** Closed #479 established the registry for parsing/header
matching and #468 added reconciliation. Neither routes the limit-monitoring
consumer through the registry; the current no-registry calls above verify that
the canonical-key contract remains incomplete specifically at this consumer.
Closed #1047 concerns numeric field aliases, not entity aliases.

### N-3 [P2 / MAJOR] Reject malformed maturity totals rather than silently treating them as zero

**Dimension:** 1.  **Confidence:** high.

**Evidence.** The maturity parser documents that only blank Total cells are
zero-filled (`src/counter_risk/parsers/exposure_maturity_schedule.py:220-228`).
However, it catches *every* `ValueError` or `TypeError` from accounting numeric
coercion and assigns `0.0` (`src/counter_risk/parsers/exposure_maturity_schedule.py:247-256`).
`calculate_wal` consumes every returned row as an exposure weight
(`src/counter_risk/calculations/wal.py:70-75`, `src/counter_risk/calculations/wal.py:91-105`).

**Reachable trigger.** A TIPS maturity schedule has a date but the Total cell
contains an accounting-formatting mistake, a text token, or a non-finite token.
`coerce_accounting_float` rejects it, then the broad exception handler converts
the row into a legitimate-looking zero exposure.

**Expected versus actual.** An invalid nonblank total should fail with the row
and source context, because the resulting WAL cannot be trusted. A one-row
schedule with `not-a-number` currently parses as a 0.0 leg; a malformed large
near-term or long-dated leg can therefore bias WAL, and an all-invalid schedule
can become the valid-looking `0.0` “wound down” result.

**Executable proof.** `numerical-proofs.py::proof_invalid_maturity_total_becomes_zero`
calls the frozen parser with a dated nonnumeric total and obtains
`ExposureMaturityRow(..., total=0.0)`.

**Required fix/test gate.** Keep zero-fill for genuinely blank cells only;
raise `ExposureMaturityScheduleError` (or a specific subclass) for nonblank
unparseable/non-finite totals, naming workbook/sheet/row/column where available.
Add cases in `tests/parsers/test_exposure_maturity_schedule.py` for blank,
malformed text, NaN/Infinity, and accounting-formatted valid values. Add a WAL
integration assertion that malformed nonblank total data cannot return a number.

**Disconfirming evidence.** Blank cells are intentionally zero and are covered
by `tests/parsers/test_exposure_maturity_schedule.py:24-65`; the proof does not
challenge that contract. Current WAL denominator checks correctly reject
mixed-sign cancellation after parsing, but cannot detect a source value already
discarded as zero.

**Overlap check.** Closed #963 covers signed near-cancellation in
`calculations/wal.py`; closed #1022 validates a computed WAL at workbook-write
time. Both occur after this parser has silently changed malformed input to zero,
and neither covers parser error handling.

## Refuted, duplicate, and insufficient candidates

| Candidate | Disposition | Evidence |
| --- | --- | --- |
| Mixed-sign concentration HHI | Refuted / fixed | `src/counter_risk/compute/rollups.py:585-595` converts notionals to magnitudes before shares; this is the dossier-confirmed fix. |
| Mixed-granularity percent limit denominator | Refuted / fixed | `src/counter_risk/compute/limits.py:138-160` scopes tagged rows to the limit entity granularity before calculating denominator. |
| Non-finite/boolean numeric coercion in reviewed helpers | Duplicate/fixed | Closed #1046, #1047, #1048, #1000, #1002, #1006, #1018, #1032–#1035 cover the named trust boundaries; current code has finite/bool guards at the inspected sites. |
| Risk-top-mover prior value uses current volatility | Insufficient evidence | The behavior is explicitly documented as an inferred proxy in `docs/risk_proxy_outputs.md:41-50`; a true prior-volatility contract would be a model change, not a demonstrated code violation. |
| Signed `compute_notional_breakdown` denominator | Insufficient evidence | It has no production caller in the frozen repository and no documented gross-exposure contract, so it is not an actionable reachable wrong-output finding. |

## Verification record

- Frozen clone HEAD: `6e2a87b27be9a23d388155e37ed01675b1e27dc7`; only pre-existing `dossier-out/` and `uv.lock` were untracked before analysis.
- Reproduction: `PYTHONPATH="$PWD/src" .venv/bin/python /Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/numerical-proofs.py` from the clone. All three current-code proofs reproduced.
- Focused baseline: `PYTHONPATH="$PWD/src" .venv/bin/python -m pytest tests/compute/test_concentration_metrics.py tests/compute/test_limits.py tests/parsers/test_exposure_maturity_schedule.py tests/test_wal.py -q -m 'not slow and not release'` -> `92 passed in 1.42s`.
- No source, test, clone, issue, git, or remote changes were made.
