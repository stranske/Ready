# Existing Ready #574 owns the research-local allowlist repair

Research-only disposition, not a new issue body to file.

Original issue: https://github.com/stranske/Ready/issues/554
Partial merged PR: https://github.com/stranske/Ready/pull/569
Existing repair: https://github.com/stranske/Ready/pull/574

At merge `2dd52d56932de83b4f0f5c02c4274802ebd7dd31`, `scripts/check_publication_safety.py:29` defaults to the parent policy. Source #554 explicitly requires `research-program/.publication-allow`. The corresponding default-location criterion remains unmet despite 169 passing focused scanner/exporter tests and successful required Gate.

Live #574 state during this run: OPEN, head `767af106c8d52555286b9d41828294e935834736`, mergedAt null. The earlier closer comment identifies six discriminating policy-path regressions. This run checked the defect and repair state, not the repair implementation; do not claim #574 merged or verified. The existing delivery owner should finish its normal review, checks, merge and post-merge acceptance. Do not duplicate the repair.
