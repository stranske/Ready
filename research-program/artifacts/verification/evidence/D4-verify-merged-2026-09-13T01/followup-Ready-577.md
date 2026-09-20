## Why (verified evidence)

`stranske/Ready#577` merged the non-finite similarity guard for `#561`, but the issue requires a deliberate-break demonstration that is absent from the squash diff and PR body.

- `scripts/langchain/issue_dedup.py::_format_similarity` returns `"0%"` when `math.isfinite(score)` is false (merge SHA `b6a648e63e1cb476d589ac8ba5df11abfbacfcb1`).
- `tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback` parametrizes `nan`, `inf`, and `-inf`.
- Issue `#561` requires removing the `math.isfinite` guard, confirming `pytest tests/test_main.py` fails on the NaN case, reverting, and recording both outcomes in the PR.
- PR #577 leaves the deliberate-break acceptance checkbox unchecked and provides no RED/GREEN transcript.

## Tasks

- [ ] In a follow-up PR linked to `#561`, temporarily remove the `math.isfinite` guard from `scripts/langchain/issue_dedup.py::_format_similarity`.
- [ ] Run `pytest tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback -q` and capture failing output on the NaN case.
- [ ] Revert and capture passing output; paste both blocks in the PR body.

## Acceptance Criteria

- Named test: `tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback` passes on `main`.
- Deliberate-break → revert: remove the `math.isfinite` guard in `_format_similarity` → confirm the named test FAILS on NaN → revert and confirm it passes. Paste RED and GREEN blocks in the PR.

## Non-Goals

- Do not change FAISS index construction or similarity thresholds.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-13T01; verified by reading squash diff for PR #577 at merge SHA `b6a648e6`._
