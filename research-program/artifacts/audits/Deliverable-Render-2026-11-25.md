Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 1 — [#155](https://github.com/stranske/Deliverable-Render/issues/155) (interior: console integration test PATH resolution).

## Run summary

| Field | Value |
| --- | --- |
| Repo | stranske/Deliverable-Render |
| Tip | `4b8cf9758580ca85b9ff3cc37a614dc1c7e848a6` (`main`) |
| Prior scorecard | 2026-10-25 @ `57d443c` (31d stale → refill) |
| Auditor | Track D unit `D-audit-Deliverable-Render--2026-11-25T04-28-12Z` |
| CI | Latest `CI` workflow success (`45334496175`) |

## Phase 1.5 — Product scorecard

All seven core functions from the 2026-10-25 contract re-exercised on Python 3.13 with isolated fixture data. Varying-input diff on HTML hub mention text confirmed outputs track store content. Primary journey (validate communication store → HTML hub + PPTX + DOCX) completes without error. Surface inventory identical to prior round (four public CLIs; no unscored surfaces).

Closed-issue reproductions: #89 (native page conflict) still refuted; #148/#149 delivered and covered by tests.

## Dimensions (abbreviated)

| Dim | Outcome |
| --- | --- |
| 1 Quality | Ruff clean; no new logic defects in `src/deliverable_render/` |
| 2 Duplication | No actionable drift vs prior round |
| 3 Wiring | Validator→renderer seams from 2026-09 remain aligned; 31 tier/conflict tests pass |
| 4 UX | No observable UI; CLI-only product |
| 5–7 Field / opportunities / tools | No filable gaps this round |
| 8 Automations | N/A |

## Verified finding filed

**#155** — `test_installed_console_commands_render_all_three_outputs` uses `shutil.which` and can invoke a stale global `render-html-hub` (e.g. `/opt/anaconda3/bin/...`) that predates the `>=3.13` package install, producing `ModuleNotFoundError` while CI stays green. Interior test hygiene, not a core-function defect.

## Dedup / refutation

- No open agent-ready defect issues besides trackers #1 and #10.
- No `REFUTED:` lines required (no false claims on open issues).

## Artifacts

- Canonical scorecard: `Code/Audits/Deliverable-Render/2026-11-25-SCORECARD.md`
- Checkpoint: `artifacts/audits/D-audit-Deliverable-Render--2026-11-25T04-28-12Z.CHECKPOINT.md`
- Issue body source: `/tmp/dr-issue-console-path.md`

## Environment

Python 3.13.13 venv; 425/426 tests pass in venv when PATH prefers venv `bin` (one local failure documents #155). No `docs/PRODUCT_CONTRACT.md` in repo; README continues to anchor core functions — adoption issue deferred (not a defect).