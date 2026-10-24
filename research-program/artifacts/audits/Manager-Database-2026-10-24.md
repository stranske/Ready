Scorecard: 8 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 19; closed-still-broken 0.

Issues filed: 2 — https://github.com/stranske/Manager-Database/issues/1848, https://github.com/stranske/Manager-Database/issues/1849

REFUTED: https://github.com/stranske/Manager-Database/issues/1790 — `etl/data_quality_flow.py` calls `fire_data_quality_alerts` → `build_data_quality_alert_event` on tip f93770b; title claim "has no caller" is false.

## Run report (Track D — 2026-10-24)

**Trigger:** Audit refill queue (`Manager-Database` scorecard 2026-09-23 >30d old; open agent-ready supply ≤25% of last set per `artifacts/audit-refill.md`).

**Tip:** `f93770b` (`fix: deliver tool pins without invalidating archived evidence`, #1847). Large tooling/verifier delta since prior scorecard tip `c68194a`; product code paths for all eight contract core functions re-probed via focused pytest (manager API/list filters, diff_holdings golden, activism/signals APIs, search, chat/RAG, dashboard loaders, document upload, alerts UI).

**Scorecard:** All eight MDB core functions **WORKS** with varying-input evidence in named tests; primary journey (register → ingest/search → research → dashboard/alerts) passes at API/test layer. **19** new REST paths vs 2026-09-22 inventory remain unscored interior surfaces (activism detail, alert history/ack, manager stats/similar/tags, signals attribution).

**Dimensions (summary):** D1/D3 wiring reviewed on changed activism/chat/dashboard modules; no new reproducible functional defect beyond contract gaps. D8 continuity: open fleet issues (#1784 activism lifecycle, #1791 alert dispatch audit) retained; #1790 headline refuted on live tip.

**Filed:**
| Issue | Finding |
|---|---|
| #1848 | `chains.Evidence` omits required `evidence-object/v1` fields; RAG `method` values outside schema enum |
| #1849 | Missing `scripts/emit_reference_run.sh` leaves backplane run-contract CI skipping |

**Artifacts:** `Code/Audits/Manager-Database/2026-10-24-SCORECARD.md`, surface inventory delta (19 paths), checkpoint `D-audit-Manager-Database--2026-10-24T04-03-28Z.CHECKPOINT.md`.

**UX panel:** not measured this round (API/test-driven scorecard only).
