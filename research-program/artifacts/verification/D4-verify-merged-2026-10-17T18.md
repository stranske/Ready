# D4 — verify merged PRs against issue acceptance criteria

Run: 2026-10-17 (36-hour window ending ~18:27 UTC; **20 PRs** verified, oldest merged first)

## Result

Two hundred thirty-four non-chore merges fell in the window; this pass audited the **first twenty** scoped candidates (explicit issue reference, excluding template-sync / dependency / release merges). Eleven are identical consumer deliveries of the Workflows#3925 N806 fix; nine are Muse runner/routing deliveries (one upstream Workflows#3934 plus eight consumer syncs).

| Repo | PR | Issue | Verdict | Unmet criteria / diff evidence | Follow-up filed |
|---|---:|---:|---|---|---|
| Ready | [#617](https://github.com/stranske/Ready/pull/617) | [Workflows#3925](https://github.com/stranske/Workflows/issues/3925) | VERIFIED | Single-file squash diff on `scripts/langchain/pr_verifier.py`: two `# noqa: N806` lines on the `ChatOpenAI` / `ChatAnthropic` import fallbacks (lines ~6088–6092), matching the fixed Workflows template from [#3927](https://github.com/stranske/Workflows/pull/3927). No ledger-only bookkeeping. Consumer repos do not host the named Workflows gate test; upstream #3927 carries it. | N/A |
| Portable-Alpha-Extension-Model | [#2354](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2354) | Workflows#3925 | VERIFIED | Same two-line `noqa: N806` change in synced `pr_verifier.py` (1 file). | N/A |
| Manager-Database | [#1776](https://github.com/stranske/Manager-Database/pull/1776) | Workflows#3925 | VERIFIED | Same pattern (1 file, noqa on both fallbacks). | N/A |
| Inv-Man-Intake | [#1013](https://github.com/stranske/Inv-Man-Intake/pull/1013) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| Pension-Data | [#954](https://github.com/stranske/Pension-Data/pull/954) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| Fine-Art-Archive | [#795](https://github.com/stranske/Fine-Art-Archive/pull/795) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| Doc-Lineage | [#102](https://github.com/stranske/Doc-Lineage/pull/102) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| Deliverable-Render | [#86](https://github.com/stranske/Deliverable-Render/pull/86) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| Manager-Mosaic | [#93](https://github.com/stranske/Manager-Mosaic/pull/93) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| Counter_Risk | [#1155](https://github.com/stranske/Counter_Risk/pull/1155) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| learning-management-system | [#754](https://github.com/stranske/learning-management-system/pull/754) | Workflows#3925 | VERIFIED | Same pattern. | N/A |
| Workflows | [#3934](https://github.com/stranske/Workflows/pull/3934) | [#3918](https://github.com/stranske/Workflows/issues/3918), [#3919](https://github.com/stranske/Workflows/issues/3919) | PARTIAL | **Substantive (not scaffold):** 30-file diff adds `muse` registry entries (root + template), `reusable-muse-run.yml`, `PROVIDERS`/`PROMPT_PROVIDERS` includes `"muse"`, keepalive/autofix routing, and new `tests/workflows/test_muse_runner_routing.py` with falsifiable YAML/workflow assertions (META_API_KEY secret, `run-muse` twins, autofix-muse, sandbox guard before `muse exec`). **Not met vs issue text:** #3918 acceptance names `agent-registry.test.js` (`muse registry entry declares…`), `tests/workflows/test_reusable_muse_run.py::test_muse_runner_passes_isolation_flags_and_never_logs_key`, and `tests/scripts/test_runner_lib.py::test_muse_is_a_known_provider` with deliberate-break pairing — none appear in the squash diff (substitute routing tests only). **Pending (deadline not yet due):** both issues require a labelled `agent:muse` keepalive canary with ≥2 commits and non-null durability by **2026-10-22**; run date is 2026-10-17. | Not filed — offload rules prohibit issue creation; #3918/#3919 remain open trackers. |
| Travel-Plan-Permission | [#1666](https://github.com/stranske/Travel-Plan-Permission/pull/1666) | #3918, #3919, #3934 | VERIFIED | Six-file consumer sync: `registry.yml` `muse:` block, delegation/bot-comment/keepalive JS, `agents-81-gate-followups.yml` / `agents-auto-pilot.yml` with `run-muse` calling `stranske/Workflows/.github/workflows/reusable-muse-run.yml@main` (no local reusable file required). Matches upstream #3934 consumer template slice. Runtime canary acceptance remains on Workflows issues. | N/A |
| Counter_Risk | [#1156](https://github.com/stranske/Counter_Risk/pull/1156) | #3918, #3919, #3934 | VERIFIED | Same six-file muse routing sync as #1666. | N/A |
| learning-management-system | [#755](https://github.com/stranske/learning-management-system/pull/755) | #3918, #3919, #3934 | VERIFIED | Same pattern. | N/A |
| Trend_Model_Project | [#6090](https://github.com/stranske/Trend_Model_Project/pull/6090) | #3918, #3919, #3934 | VERIFIED | Same pattern. | N/A |
| Portable-Alpha-Extension-Model | [#2356](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2356) | #3918, #3919, #3934 | VERIFIED | Seven files (adds `docs/LABELS.md`); muse registry + routing sync as above. | N/A |
| Manager-Database | [#1777](https://github.com/stranske/Manager-Database/pull/1777) | #3918, #3919, #3934 | VERIFIED | Six-file muse routing sync. | N/A |
| Inv-Man-Intake | [#1014](https://github.com/stranske/Inv-Man-Intake/pull/1014) | #3918, #3919, #3934 | VERIFIED | Six-file muse routing sync. | N/A |
| Pension-Data | [#955](https://github.com/stranske/Pension-Data/pull/955) | #3918, #3919, #3934 | VERIFIED | Six-file muse routing sync. | N/A |

## Test-gate, belt-ledger, and reproduction disposition

- **Belt ledger:** No audited PR was ledger-only; rule 3b not triggered.
- **#3925 rename tasks:** Issue tasks asked lowercase renames; upstream [#3927](https://github.com/stranske/Workflows/pull/3927) (merged later in the window, not in this batch) chose `# noqa: N806` instead. Consumer PRs correctly deliver that upstream fix; I do not treat the rename wording as unmet on consumers.
- **Reproduction:** No linked issue in this set contained a runnable `Reproduction:` block.
- **GitHub writes:** Unit instructions authorize follow-ups, comments, and reopens; **OFFLOAD WORKSPACE RULES** forbid them this run. No issues filed or reopened.

## Resume pointer

234 in-window merges remain; next run should continue from the checkpoint ledger (oldest unverified: merges after Pension-Data#955, e.g. Workflows#3928 chore — skip — then #3932 without issue — skip — then further issue-linked merges including Workflows#3927, Fine-Art-Archive#797, etc.).

**Confidence:** High for the eleven N806 consumer syncs and eight muse consumer syncs (diffs are tiny and homogeneous). Moderate for Workflows#3934 PARTIAL — the substitute `test_muse_runner_routing.py` is real, but literal acceptance test names from #3918 are absent from the squash diff; finding would change if those named files exist on `main` from a different merge outside this PR (not observed in `gh pr diff 3934`).
