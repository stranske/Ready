# D4 verification — 2026-11-13

Checked 2026-11-13. Discovery covered the 36-hour window beginning
2026-11-12T11:28:54Z across the supported fleet, excluding Orchestrator and
the owner-excluded `stranske/Collab-Admin`. Six merged PRs were found; one
release chore was skipped. No GitHub secondary-rate-limit response occurred.

| Repo | PR | Issue / relationship | Verdict | Unmet criteria / evidence | Follow-up |
|---|---:|---|---|---|---|
| Portable-Alpha-Extension-Model | [#2505](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2505) | [#2504](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2504) | **PARTIAL** | `pa_core/schema.py` now renders unions and `tests/test_schema_export.py` adds meaningful Optional/PEP-604 assertions; local Python 3.12 ran 18 passing focused tests. But commit `f8f6951` neither changes `docs/guides/PARAMETER_DICTIONARY.md` nor evidences the required Python 3.13 and 3.14 runs and byte-identical generated output. | Filed [#2507](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2507). |
| Workflows | [#4675](https://github.com/stranske/Workflows/pull/4675) | PR-local request (no separate source issue) | **VERIFIED** | `scripts/stage_agent_changes.py` excludes root `.local`, `.config`, and `.cache`; `test_cli_tool_state_in_the_workspace_is_never_staged` asserts those remain unstaged while `docs/.config` remains eligible. Required CI summary succeeded. The local combined Python rerun did not finish within the 30-second bounded check, so this is CI-backed rather than a fresh local pass. | — |
| Workflows | [#4676](https://github.com/stranske/Workflows/pull/4676) | [#4523](https://github.com/stranske/Workflows/issues/4523) cited as a parser fixture, not an implementation link | **VERIFIED (stated parser scope)** | Both source and consumer-template `acceptance_gate.py` normalize only pinned pytest interpreters; tests cover path/version forms, bare forms, and non-pytest scripts. `#4523` is not claimed as completed, so judging this PR against all of #4523 would be a category error. Required CI summary succeeded. | — |
| Workflows | [#4678](https://github.com/stranske/Workflows/pull/4678) | [#4454](https://github.com/stranske/Workflows/issues/4454) and Counter_Risk#1183 cited as fixtures, not implementation links | **VERIFIED (stated parser scope)** | The diff supplies real checkbox-first/plain-bullet fallback logic in both copies and tests plain bullets, mixed sections, and nested bullets. It does not claim to implement either cited source issue. Required CI summary succeeded. | — |
| Workflows | [#4627](https://github.com/stranske/Workflows/pull/4627) | [#4636](https://github.com/stranske/Workflows/issues/4636) | **SKIPPED** | Release-please manifest/changelog chore; excluded by scope. | — |
| Workflows | [#4680](https://github.com/stranske/Workflows/pull/4680) | [#4679](https://github.com/stranske/Workflows/issues/4679) | **PARTIAL** | Source work is substantive: `original_command` travels through Python extraction/results and both JS renderers use it to uncheck the authored criterion; regression tests cover pinned forms, colliding normalized commands, source/template behavior, and failures. However, at check time `maint-71-merge-sync-prs.yml` run `43527859837` was **in progress**, and consumer PR [Portable-Alpha #2506](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2506) remained open/unmerged. Thus the issue's downstream-live criterion is not proved. | Existing authorized follow-up: [Workflows #4681](https://github.com/stranske/Workflows/issues/4681). |

## Critical findings

- A passing generic CI summary is not proof of #2504's interpreter-specific
  acceptance criteria. The only fresh local execution was Python 3.12, which
  cannot establish the required 3.13/3.14 parity.
- #4676 and #4678 cite issues solely to embed real acceptance-text fixtures.
  Treating those citations as a claim that the PR implemented every criterion
  of the cited issue would create false NOT IMPLEMENTED findings.
- #4680 is not scaffold-only. Its remaining risk is operational propagation:
  source changes are merged, while the required downstream merge/sync outcome
  has not reached a terminal success state.

## Test and CI evidence

- Portable-Alpha default tip equals #2505 merge commit `f8f695111c4fb11a0ee97e749f8f7fca1e1af74b`; `/opt/anaconda3/bin/python3 -m pytest -q tests/test_schema_export.py` reported **18 passed** (Python 3.12).
- Workflows default tip equals #4680 merge commit `1061fa7bff0960256c645cca425baae770d0569c`.
- Each implementation PR's required GitHub check summary was successful. The
  bounded local Workflows pytest attempt did not produce a terminal result
  within 30 seconds because of the repository's test environment; no passing
  local result is claimed for it.
- No issue contained a `Reproduction:` block, and no issue designated a core
  product-contract function, so neither a verbatim reproduction nor a product
  scorecard rerun applied.

Confidence: high on the diff-level verdicts; medium on CI/test-gate adequacy
where GitHub exposes a summary rather than the named command transcript. A
completed successful maint-71 run and merged consumer PR #2506 would change
#4680 from PARTIAL to VERIFIED for its remaining live criterion.
