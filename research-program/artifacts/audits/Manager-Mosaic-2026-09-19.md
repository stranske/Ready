# Manager-Mosaic audit run report — 2026-09-19

## Outcome

The audit identified and independently reproduced three agent-ready correctness defects on current `main` `fd8c63ad3b2b70c7535ca9647ad0f8b114364d27`. All three issue bodies conform to the repository's `AGENT_ISSUE_FORMAT` validator and use repository-relative citations.

**No GitHub issues were filed.** This is an execution blocker, not a no-op: `gh issue create` stopped before submission because this seat has no GitHub CLI authentication. I did not fabricate URLs, format-guard verdicts, intake rows, or ledger filing records.

## Verified backlog (maximum three)

| Priority | Finding | Evidence | Staged body |
|---|---|---|---|
| P1 | Inverted entry period ranges validate cleanly and make `derive_gaps()` return no gaps. | `src/manager_mosaic/model.py:349-364`, `src/manager_mosaic/model.py:443-452` | `01-reject-inverted-entry-period-ranges.md` |
| P1 | Same-period conflicting facts can flip a thesis verdict solely by changing evidence-ID strings. | `src/manager_mosaic/thesis.py:58-75` | `02-handle-same-period-thesis-conflicts.md` |
| P2 | Accepted but unparsed period labels rank below any parsed quarter, silently selecting an older fact. | `src/manager_mosaic/discrepancy.py:13-23`, `src/manager_mosaic/thesis.py:25-34,72-75` | `03-validate-or-parse-period-labels-before-thesis-selection.md` |

The staged bodies are in `artifacts/audits/Manager-Mosaic-2026-09-19-issue-bodies/`.

## Verification

- Fresh clone fast-forwarded from `dd62060` to `fd8c63a` before analysis.
- `python3 -m pytest -q --no-cov` — **58 passed**.
- `python3 -m ruff check src tests` — **passed**.
- Every issue body passed `[LOCAL_WORKSPACE]/Manager-Mosaic/.github/scripts/issue_format.py` when evaluated from the target repository root; cited source/test paths were reopened and exist in the clone.
- Public GitHub REST inventory found five open non-PR issues, only two product follow-ups (#31 and #32), and no semantic duplicate of the three retained defects. Closed #3 and #11–#14 cover the older core-model/evidence/discrepancy/thesis/registry surface, not these deeper cases.
- Public REST Actions data shows current-tip scheduled health and keepalive sweeps succeeding. A current-tip Agents Gate Followups failure was not filed because `.github` workflow machinery is synced infrastructure and outside this repo-local audit scope.

## Risks and unknowns

- The strongest blocker is GitHub write authentication. `gh repo view` and the subsequent `gh issue create` both report that `gh auth login` or `GH_TOKEN` is required. With authentication restored, file the three prepared bodies using existing `bug` plus `priority:high` (P1) or `priority:normal` (P2) labels, append the returned URLs to the intake log, and inspect the new issue-format guard runs.
- The required canonical records under `Code/Audits/Manager-Mosaic/` and `Code/Audits/AUDIT_LEDGER.md` could not be created: this executor's filesystem policy rejects writes outside the project and offers no approval path. The unit checkpoint and this report preserve the completion record instead.
- Confidence: high for all three retained defects; each has a direct broken/control reproduction. The conclusion would change if a documented period-order or same-period conflict policy establishes that silently dropping ranges or using evidence-ID order is intentional; no such policy was found in the audited repository.

## Audit method

Phase 0 reconstructed scope from the missing dossier's approved substitutes: the prior Manager-Mosaic report, canonical audit index/ledger, README, CLAUDE.md, owner notes, and current refill table. Phase 1 used bash orientation. Phase 2 used one Cursor read-only offload; a Vibe offload stalled and was interrupted without output, so it was excluded from evidence. Phase 3 re-ran direct broken/control probes at the current tip and rejected the weaker package-root-export observation. UX is not applicable: the repository currently provides model/validation modules only, with no runnable browser or operator surface.
