Scorecard: 4 work / 0 partial / 1 broken / 0 fabricated / 2 not exercised of 7; journey: stops at "Scan belt promotion queue"; surfaces unscored 0; closed-still-broken 0.

# Workflows audit — 2026-09-23

Audited fresh `stranske/Workflows` `main` at `864b6e3053ce5135e8bc56cfac308edd56fa0108`. The live deterministic core is healthy: current consumer-manifest compilation produced 238 copy entries and 17 removals; run-contract self-smoke accepted its valid fixture and rejected five malformed cases; capability selection varied correctly across matching/nonmatching repositories; and the metrics pipeline produced materially different alpha/beta figures. Focused regression gates also passed: 123 Python tests and 20 Node tests.

The primary belt-promotion journey is broken before discovery. Exact-tip scheduled Actions runs 35862732312, 35865818556, and 35868514826 all fail the scan with a JavaScript Proxy invariant error when `checkRateLimitStatus` reads the wrapped client's non-configurable `__getTokenSource`; the last 15 workflow runs contain 14 failures. The current `WORKFLOWS_APP` credential had 4,728 remaining calls, so this is not provider capacity. No existing issue matches the error.

Filed one verified P1 issue for the proxy metadata invariant, with an AGENT_ISSUE_FORMAT body, named Node test gate, deliberate-break/revert proof, and post-merge Actions observation. Consumer delivery and Gate-on-a-real-PR are intentionally marked not exercised because the audit did not mutate consumer repositories or fabricate a production event. Canonical scorecard and evidence live in `Code/Audits/Workflows/2026-09-23-*`.
