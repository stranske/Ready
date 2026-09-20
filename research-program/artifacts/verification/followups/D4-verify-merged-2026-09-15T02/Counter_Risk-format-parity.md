# Align Counter_Risk PR and push formatting gates and restore green main

Status: research-only draft, not filed. One defect affects both merged PRs; deduplicate against current CI repair work before publication.

## Why

PR #1069 delivered source #1061's registered-alias behavior, but its exact merge `9c6cd8962536c7d1159e5d45c2a0d36b919322c4` fails main CI. Run 34827221311 says Black 26.5.1 would reformat `src/counter_risk/compute/limits.py`. PR #1071 / source #1062 inherits the identical failure on its merge (full SHA in the verification report), run 34899128332. The numerical tests pass. PR Gate sets `format_check: false` at `.github/workflows/pr-00-gate.yml:73`, while `.github/workflows/ci.yml` uses the reusable formatting default. A required post-merge check is therefore missing from pre-merge acceptance.

## Scope

Restore the pinned formatter's expected layout in `src/counter_risk/compute/limits.py` and make the existing PR and push formatting contract consistent. Route any managed-template change through the existing Workflows source owner.

## Non-Goals

Do not change limits/concentration semantics, weaken the post-merge format check, or file two copies of this same failure.

## Tasks

- Apply only the pinned Black formatting correction to the affected source.
- Ensure PR validation executes the same format requirement as push CI.
- Preserve the alias and concentration numerical regression tests.

## Acceptance Criteria

- `black --check --line-length 100 --exclude '(\.venv|\.workflows-lib|node_modules)' .` with Black 26.5.1 passes.
- `python -m pytest tests/compute/test_limits.py tests/compute/test_concentration_metrics.py -q` passes.
- Exact-head PR checks and the resulting main push CI both execute and pass formatting.
- An intentional formatting violation causes the pre-merge check to fail, then passes after restoration.

## Evidence

- https://github.com/stranske/Counter_Risk/actions/runs/34827221311
- https://github.com/stranske/Counter_Risk/actions/runs/34899128332
- https://github.com/stranske/Counter_Risk/issues/1061
- https://github.com/stranske/Counter_Risk/issues/1062

Full relevant merge SHA: `215978393d213ce5a3bdc0ff48f9647c43b5569e`.
