# Travel-Plan-Permission audit refill — 2026-09-07 (17:01 unit)

Unit: `D-audit-Travel-Plan-Permission--2026-09-07T17-01-43Z`; attempt 1; executor claude.
Repo head audited: `5be7204f9494ca75fe915123adb55c5ed97e309b`
("fix: keep non-finite numbers out of workbook numeric cells (#1563)").
The earlier 04:47 unit's reconciliation report was archived to
`tpp-20260907-recovery/PRIOR-REPORT-0447-unit.md` before this file was rewritten — the engine assigns
both units the same OUT path.

## Why a refill was due

`artifacts/audit-refill.md` recorded TPP at 1 open agent-ready issue against a last-filed set of 4
(threshold 2). Confirmed live: the three issues the 04:47 unit had reverified — #1557, #1558, #1559 —
were all **closed** by 2026-09-07, leaving only #1513 plus four durable trackers. This was a genuine
empty queue, not a stale count.

## What was filed — 9 issues, all adversarially verified against the live tip

Every finding below was reproduced by executing the repository's own code at `5be7204`, not inferred
from reading. All nine bodies pass `.github/scripts/issue_format.py` with zero errors and zero
advisories, and cite repo-relative paths only.

| # | Sev | Finding | Anchor |
|---|---|---|---|
| [1564](https://github.com/stranske/Travel-Plan-Permission/issues/1564) | P1 | Shipped ADV-001 never treats a real foreign destination as international | `src/travel_plan_permission/validation.py:110-114` + `config/validation.yaml:11-13` |
| [1565](https://github.com/stranske/Travel-Plan-Permission/issues/1565) | P1 | Every shipped provider contract expired; PROV-001 warns on all providers | `config/providers.yaml`, `src/travel_plan_permission/providers.py:74-82` |
| [1566](https://github.com/stranske/Travel-Plan-Permission/issues/1566) | P1 | `TPP_AUDIT_RETENTION_DAYS=0` clamps to one day and deletes the audit trail | `src/travel_plan_permission/audit.py:486-495,512-518` |
| [1567](https://github.com/stranske/Travel-Plan-Permission/issues/1567) | P1 | Validation snapshots recompute their hashes on load, so the chain is not tamper-evident | `src/travel_plan_permission/snapshots.py:79-95,169-171` |
| [1568](https://github.com/stranske/Travel-Plan-Permission/issues/1568) | P1 | A trip whose return precedes departure is accepted and costed as one night | `src/travel_plan_permission/models.py:463-465`, `policy_api.py:226-227` |
| [1569](https://github.com/stranske/Travel-Plan-Permission/issues/1569) | P2 | Audit CSV export writes untrusted values as live spreadsheet formulas | `src/travel_plan_permission/audit.py:454-462` vs `export.py:44-57` |
| [1570](https://github.com/stranske/Travel-Plan-Permission/issues/1570) | P2 | Role-change decisions are not terminal — approve/reject replay indefinitely | `src/travel_plan_permission/security.py:462-467,509-514` |
| [1571](https://github.com/stranske/Travel-Plan-Permission/issues/1571) | P2 | A high-precision expense amount crashes export and is misreported as invalid input | `src/travel_plan_permission/export.py:97-98` |
| [1572](https://github.com/stranske/Travel-Plan-Permission/issues/1572) | P2 | Policy version comparison ignores config drift; `requires_downtime` is a constant | `src/travel_plan_permission/policy_versioning.py:33-45,71-74,100-122` |

### Reproductions on record

- **#1564** — with the shipped keyword list `["international","overseas"]` and a departure 10 days out:
  `Toronto, Canada`, `London, United Kingdom` and `Tokyo, Japan` all classify **domestic** (7-day
  notice, no ADV-001), while `International Falls, MN` classifies **international** and is blocked.
  The 14-day international control fires on exactly one input, and that input is in Minnesota.
- **#1565** — the shipped registry's four contracts expired 2023-12-31 through 2024-12-31.
  `active_providers()` is `[]` today; `is_approved()` is False even for an exact, correctly-cased name.
- **#1566** — five events aged 0/2/30/400/2000 days, `TPP_AUDIT_RETENTION_DAYS=0`: **4 of 5 pruned**.
  `max(1, value)` at `:495` makes the `days <= 0` guard at `:514` unreachable from the env path.
- **#1567** — appended a snapshot, edited `input_data.purpose` from "Client meeting" to "Vacation in
  Maui" leaving both stored hashes untouched, reloaded: returned the edited purpose with a freshly
  minted `snapshot_hash`, no error.
- **#1568** — `TripPlan(departure_date=2026-02-03, return_date=2026-02-01)` validates;
  `duration_days()` returns `-1`; `policy_api.py:227` clamps it to a 1-night trip for costing.
- **#1569** — an event with `target_id="=HYPERLINK(...)"` exports as a live formula cell.
- **#1570** — approve → reject → approve on one request all succeed, 4 contradictory audit events.
- **#1571** — `Decimal("1E+40")` is accepted by `ExpenseItem` and raises `decimal.InvalidOperation`
  inside `to_csv`/`to_excel`; `expense_review.py:135` then reports it as "not a valid decimal value".
- **#1572** — two `1.0.0` versions with different budget caps: `change_type` says `config-drift`,
  `is_backward_compatible_with` says True; `requires_downtime` is False for a breaking major change;
  `2.0.0-rc1` parses to `0.1.0`.

### Why the existing suite is green on all nine

Three tests actively enshrine the defect rather than catching it — `tests/python/test_audit.py:203-204`
asserts `configured_retention_days() == 1` for `"0"`, and `tests/python/test_policy_versioning.py:48`
asserts `requires_downtime is False` for a breaking change. Three more are blind by fixture:
`tests/python/test_providers.py:14,19` pin `reference_date` inside 2024 so the shipped expiry can never
be noticed; `tests/python/test_validation.py:50,76,93,254` substitute city-name keywords for the
shipped `["international","overseas"]`; `tests/python/test_export_service.py:45,62` never exceed a
two-decimal amount. The rest are gaps: no CSV-injection test in
`tests/python/test_audit_export_and_schema.py`, no on-disk tamper test in `tests/python/test_snapshots.py`,
no second decision in `tests/python/test_security_model.py:58`, no inverted date pair anywhere.

## Findings refuted during verification — not filed

- **NaN/infinite expense amount.** `ExpenseItem.amount` already rejects both (pydantic finite check).
- **`portal_review._blocking_policy_codes` fail-open.** The `severity` branch does match, because
  `Severity.BLOCKING` is a plain `str` equal to `"blocking"`. The classifier and the sibling one at
  `policy_api.py:1239-1241` disagree only on shapes nothing currently produces; noted, not filed.
- **Silent `summary.pdf` → `summary.txt` downgrade** at `prompt_flow.py:178,223-224`. The bare
  `except Exception: return b""` is real, but no reachable trigger was found (reportlab handled a
  20k-character token, NUL, VT and BEL). Not filed without a failing input.
- **Question flow leaking optional prompts on a complete draft.** `generate_questions` returns `[]`.
- **Caller-supplied `admin_role` as a P0 auth bypass** (offload candidate 1). Overstated:
  `approve_role_change`/`reject_role_change` have no callers outside `security.py`, so there is no
  route. Folded into #1570's context.

## Coverage — what this unit did and did not establish

This is a **correctness/wiring refill**, not a comprehensive eight-dimension audit, and it should not
be read as one. D1 (code quality/correctness) and D3 (functionality and wiring) have fresh
first-person runtime evidence. D2 surfaced one real instance (the duplicated CSV-escaping rule,
#1569). D4 (observed design/UX) was **not exercised** — no browser capture, no `ux_review.py` panel,
no UX score is claimed. D5, D6, D7 and D8 have no fresh evidence in this unit.

### Unverified carry-forward from the offload

The codex offload returned 10 candidates; 3 were accepted, 1 was downgraded and folded in, and 6 were
**not verified this round** and therefore not filed. They remain open leads for the next refill, not
findings:

- sqlite: read/write serialization on the shared connection (`persistence/sqlite_store.py:74-85,98-106`)
- postgres: `_select_all`'s unguarded `conn.commit()` racing a writer's transaction (`persistence/postgres_store.py:90-104`)
- approval-packet cost breakdowns that disagree with the plan total (`approval_packet.py:219-260`)
- canonical submission ID collision resistance (`canonical.py:121-127,198-205`)
- override revalidation in the deprecated minimal-conversion adapter (`conversion.py:33-50`)
- provider approval evaluated against the server date rather than the trip date (`policy_api.py:1447-1454`)

The two persistence candidates both require a real concurrent backend to demonstrate; the brief's rule
is that a finding needs a failing input, so they were held rather than filed on code shape alone.

## Delivery evidence

- Issue bodies: `Code/Audits/Travel-Plan-Permission/2026-09-07-refill/01..09-*.md`.
- Offload output: `artifacts/audits/tpp-20260907-refill/AGENT-FINDINGS.md` (codex, 10 candidates).
- Local format validation: 9/9 PASS, zero advisories, against the repo's own
  `.github/scripts/issue_format.py` at the audited head.
- Intake log: 9 rows appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- Remote `Agents Issue Format Guard`: 2 runs completed **success**, 3 **cancelled** and 2 **skipped**
  by the repo's issue-event concurrency group. No issue carries `needs-human` and no issue has any
  comment, so there were zero guard rejections; the cancelled runs are concurrency, not verdicts.
- Labels applied: `bug` on all nine, plus `risk:major`+`priority:high` on the five P1s and `risk:minor`
  on the four P2s, with `security` on #1567/#1569/#1570, `type:policy` on #1564/#1565/#1572 and
  `type:schema` on #1568 — all drawn from the repo's own label set.
