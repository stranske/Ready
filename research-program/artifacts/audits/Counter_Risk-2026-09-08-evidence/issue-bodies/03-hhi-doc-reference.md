# [P3] Correct the dated HHI threshold attribution in operator guidance

## Why

`docs/concentration_metrics.md:77` attributes the 0.18/0.25 concentration labels to DOJ conventions without a date. The current official DOJ HHI explainer describes a market above 1,800 as highly concentrated under the 2023 Merger Guidelines, so the 2,500 attribution is dated and the text mixes regimes. The document already calls these orientation heuristics, not policy limits. Preserve that distinction: this is a documentation correction, not a request to impose antitrust thresholds on counterparty risk.

## Scope

Correct or remove the external threshold analogy in the concentration guide, preserving the arithmetic scale explanation and configured portfolio limits.

## Non-Goals

No unrelated source or upstream-synced workflow changes. Scaffold-only or partial completion does NOT count as done; complete the observable gates below.

## Tasks

- [ ] Revise `docs/concentration_metrics.md` operator interpretation paragraph to label any historical threshold with its year or replace it with a dated current official reference.
- [ ] Keep `docs/concentration_metrics.md` explicit that merger-market heuristics do not set portfolio counterparty limits; point operators to the existing limit-monitoring guide.

## Acceptance Criteria

- [ ] Documentation verification: the changed paragraph links to the official DOJ HHI explainer, identifies the guideline vintage, and does not describe 2,500 as the undated current highly-concentrated threshold.
- [ ] Deliberate-break verification: temporarily restore the old undated 2,500 attribution in `docs/concentration_metrics.md`; the documented source-comparison checklist must fail; restore the correction and record the comparison in the PR.
- [ ] The documented fractional-to-10,000 conversion and actual calculation and configuration behavior remain unchanged.

## Implementation Notes

Official source checked 2026-09-08: https://www.justice.gov/atr/herfindahl-hirschman-index . No policy approval is required to correct a citation; any portfolio threshold change is outside scope.
