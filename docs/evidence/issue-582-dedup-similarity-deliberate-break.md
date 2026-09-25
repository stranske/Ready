# Deliberate-break evidence: non-finite dedup similarity gate (#582 / #561)

Linked issue: `stranske/Ready#582` (parent verification gap `#561`, landed in merged PR #577).

## Mutation (temporary, reverted before merge)

In `scripts/langchain/issue_dedup.py`, the `math.isfinite` guard in `_format_similarity` was temporarily removed so the named test could observe NaN/`inf` failures.

Production code on this branch still includes the guard; this file records the RED/GREEN transcript only.

## RED — remove guard, then `pytest tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback -q --no-cov`

```
tests/test_main.py FF.

=================================== FAILURES ===================================
______ test_format_similarity_non_finite_scores_return_safe_fallback[nan] ______

score = nan
...
>       assert _format_similarity(score) == "0%"
...
E       ValueError: cannot convert float NaN to integer

scripts/langchain/issue_dedup.py:227: ValueError
______ test_format_similarity_non_finite_scores_return_safe_fallback[inf] ______

>       assert _format_similarity(score) == "0%"
E       AssertionError: assert '100%' == '0%'

=========================== short test summary info ============================
FAILED tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback[nan]
FAILED tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback[inf]
========================= 2 failed, 1 passed in 19.51s =========================
```

## GREEN — restore guard, same command

```
tests/test_main.py ...

============================== 3 passed in 9.09s ===============================
```

## Verification command (this PR)

`pytest tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback -q --no-cov`
