# D3 unblock sweep — 2026-10-03T08

**Coverage (14 fleet repos, Orchestrator excluded):** Attempt 1 — Workflows → Pension-Data (8). Attempt 2 — Ready → Manager-Mosaic (7). **Deferred:** none.

| Repository | Frozen issues | Stalled PR reroutes | Default-branch state | Agent-ready supply |
|---|---|---:|---|---:|
| Workflows | Repaired [#3713](https://github.com/stranske/Workflows/issues/3713) (removed `agents:auto-pilot-pause`; paths verified in clone). Left [#3123](https://github.com/stranske/Workflows/issues/3123) (`needs-human`, durable LangSmith tracker). | 0 ([#3689](https://github.com/stranske/Workflows/pull/3689) already `agent:auto`). | Tip `5825890`: Gate Fork Status Publisher passed. | 10 |
| Travel-Plan-Permission | None | 0 | Tip `1bb993e`: CI and Gate passed. | 18 |
| Trend_Model_Project | None | 0 | Tip `f8c8e37`: CI **in progress** on current head (not yet pass/fail). | 0 |
| Portable-Alpha-Extension-Model | None | 0 | Tip `e071657`: **red** — CI `lint-format` fails (black on `tests/conftest.py`); Gate Fork Status Publisher failed (no open PR at stale gate head). Mechanical format fix; offload cannot open PR. | 0 |
| Counter_Risk | None | 0 | Tip `5934040`: CI passed. | 0 |
| Manager-Database | None | 0 | Tip `a628992`: CI passed. | 0 |
| Inv-Man-Intake | None | 0 | Tip `7e79a9c`: CI passed. | 1 |
| Pension-Data | None | 0 | Tip `0b6e104`: CI passed. | 0 |
| Ready | None (open issues are `tracker:durable` only) | 0 | Tip `40956a7`: CI passed. | 0 |
| trip-planner | None | 0 | Tip `1ecf3ff`: CI and Gate passed. | 1 |
| learning-management-system | None | 0 | Tip `4d192e9`: CI passed. | 0 |
| Fine-Art-Archive | None | 0 | Tip `70a78cd`: CI passed. | 0 |
| Doc-Lineage | Left [#1](https://github.com/stranske/Doc-Lineage/issues/1) Dependency Dashboard (`agents:auto-pilot-pause`; bot-maintained tracker). | 0 | Tip `e9a125d`: CI passed. | 1 |
| Deliverable-Render | Left [#1](https://github.com/stranske/Deliverable-Render/issues/1) Dependency Dashboard (`agents:auto-pilot-pause`; bot-maintained tracker). | 0 | Tip `63b0a48`: CI passed. | 1 |
| Manager-Mosaic | None | 0 | Tip `3287e9e`: CI passed. | 2 |

**Silent claims (reviewed, not released):** [#3691](https://github.com/stranske/Workflows/issues/3691) — deliberate post-merge acceptance / sync-review hold. [#2329](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2329) — post-merge `verify:compare` reconciliation. Attempt 2 found no stale `status:in-progress` / `agent:*` claims without an open PR in Ready → Manager-Mosaic.

**Priority-label gap** (open / `priority:*`): Workflows 23/3; Travel-Plan-Permission 22/0; Trend_Model_Project 2/0; Portable-Alpha-Extension-Model 3/0; Counter_Risk 2/0; Manager-Database 2/0; Inv-Man-Intake 3/1; Pension-Data 2/0; Ready 3/0; trip-planner 3/1; learning-management-system 3/0; Fine-Art-Archive 4/0; Doc-Lineage 2/0; Deliverable-Render 2/0; Manager-Mosaic 3/1.

## Genuinely needs the owner

- [#3123](https://github.com/stranske/Workflows/issues/3123) — LangSmith observability health tracker: needs a product/ops decision on publication and conformance thresholds.

## Offload note

Attempt 1 applied GitHub label actions on Workflows #3713. Attempt 2 used live `gh` API checks only (no new label/PR actions). Default-branch repair for Portable-Alpha-Extension-Model remains mechanical (`black tests/conftest.py` on `main`); opener lane should land that fix.
