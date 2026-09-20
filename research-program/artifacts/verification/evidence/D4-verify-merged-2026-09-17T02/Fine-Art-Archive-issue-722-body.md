Continuing the fleet coverage initiative -- this round was opened automatically by coverage-autopilot.py after the previous round on this repo closed.

Prioritize identity resolution / enrichment / API-surface modules.

Same contract as every round in this initiative:
1. Pick the next target by the repo's own coverage-gap ranking (escaped-defect priority, then
   churn, then uncovered mass), not by file size.
2. Every new test must FAIL when the code it covers is deliberately broken and PASS when
   reverted -- run that break/revert for real and report it, don't assert it.
3. Real bugs found while writing tests get fixed with a minimal, targeted diff in the same PR,
   not worked around. Watch for the negative-cache pattern (cache.get(key) is None used as a 'not yet cached' check, which can't tell 'never queried' from 'queried and got nothing') -- it has recurred independently four separate times fleet-wide already.
4. Low blast radius only -- test-only or tightly-scoped fixes, no refactors.
5. One PR per logical chunk of work.

The goal is to improve the code, not a metric. If you measure this repo at or above 90% before
starting, say so in a comment on this issue and close it without opening a PR -- do not
manufacture a fix just because a round was requested.

