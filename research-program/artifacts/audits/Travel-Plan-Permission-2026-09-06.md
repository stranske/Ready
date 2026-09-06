# Travel-Plan-Permission Audit Report — 2026-09-06

**Unit ID:** `D-audit-Travel-Plan-Permission--2026-09-06T16-33-27Z`  
**Repository:** `stranske/Travel-Plan-Permission`  
**Target Tip SHA:** `8c046c91b94aa2aed58b50cd152c9ce4ece07611`  
**Trigger Context:** Track D Demand-Driven Refill Audit (open actionable supply was 2 <= 2)  
**Execution Environment:** Gemini via Antigravity (`agy`), macOS runner  
**Filing Summary:** 9 novel, machine-validated, adversarially-verified issues filed (#1539–#1547)

---

## 1. Executive Summary & Audit Posture

This audit executed a complete 8-dimension review and refill for `stranske/Travel-Plan-Permission` following the repository's open agent-ready supply depletion to 2 issues.

On the live remote tip `8c046c91b94aa2aed58b50cd152c9ce4ece07611`, 50 Python source modules (15,081 LOC) and 77 test suites (18,280 LOC) were systematically investigated. All candidate findings were subjected to independent adversarial proofs in isolated test harnesses, deduplicated against all open and closed issues in the repository, authored to strict `AGENT_ISSUE_FORMAT` specifications, and validated by `.github/scripts/issue_format.py` (9/9 pass, 0 advisories).

All 9 issues were successfully filed via GitHub CLI and verified against GitHub Actions CI (`Agents Issue Format Guard`), achieving 100% passing status with zero format errors or warnings.

---

## 2. 8-Dimension Assessment Overview

| Dimension | Scope Evaluated | Primary Findings & Health Status |
|---|---|---|
| **D1: Code Quality & Typing** | `src/travel_plan_permission/` (50 modules) | Ruff clean; identified non-finite float handling gaps in distance and spreadsheet rendering. |
| **D2: Duplication & Gaps** | Test suites vs source implementation | Identified missing test fixtures for European date formats and unescaped XML in ReportLab builders. |
| **D3: Core Functionality** | Policy engine, expense reconciliation | Discrepancy between gross category aggregation and net reimbursable totals in expense reports. |
| **D4: Policy & Logic** | `LocalOvernightRule`, `FareComparisonRule` | `LocalOvernightRule` fails open on NaN distances; canonical conversion omits roundtrip flight comparison values. |
| **D5: Architecture & State** | Review workflow state machines | Terminal state transitions permitted repeatedly without idempotency guards or conflict errors. |
| **D6: Security & Isolation** | Snapshot store, audit recovery | Missing path confinement on snapshot JSON operations; unhandled nulls in audit log deserialization. |
| **D7: Schema & Interop** | Canonical model converters, OOXML exports | Ground transport dropped from canonical models; OpenXML exports corrupting on non-finite floats. |
| **D8: Operations & Guardrails** | CI workflows, intake metrics | Format guard CI green across all newly filed issues; durable ledger fully synchronized. |

---

## 3. Inventory of Filed Issues

### #1539: [P1] LocalOvernightRule fails open when distance_from_office_miles is NaN
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1539
- **Labels:** `bug`, `risk:major`, `priority:high`, `type:policy`, `validation`
- **Target:** `src/travel_plan_permission/policy.py:349-354`
- **Reproduction:** When `context.distance_from_office_miles` is `float('nan')`, `nan < 50.0` evaluates to `False`, causing `LocalOvernightRule.evaluate()` to return `passed=True` without checking for a required local overnight waiver.
- **Remediation:** Guard distance evaluation with `math.isnan()` and fail closed unless a valid waiver exists.

### #1540: [P1] Escape unformatted user strings in ReportLab PDF generation
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1540
- **Labels:** `bug`, `risk:major`, `priority:high`
- **Target:** `src/travel_plan_permission/approval_packet.py:153-159`, `src/travel_plan_permission/prompt_flow.py:217-220`
- **Reproduction:** ReportLab `Paragraph` parses raw strings as XML markup. User strings containing `<` or `&` (e.g. `AT&T` or email headers) trigger `ValueError: paraparser: syntax error` in `generate_packet_pdf` or empty PDF bytes in `_build_summary_pdf`.
- **Remediation:** Sanitize user strings with `xml.sax.saxutils.escape()` prior to `Paragraph` instantiation.

### #1541: [P2] Reconcile third-party payment totals in ExpenseReport category breakdowns
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1541
- **Labels:** `enhancement`, `risk:minor`, `priority:normal`, `validation`
- **Target:** `src/travel_plan_permission/models.py:582-592`, `src/travel_plan_permission/policy_api.py:1732`
- **Reproduction:** `ExpenseReport.total_amount()` sums `e.reimbursable_amount()` (zeroing out third-party funded items), while `expenses_by_category()` sums raw amounts. `policy_api.reconcile()` outputs a `ReconciliationResult` where `actual_total` is 0 but category totals sum to non-zero.
- **Remediation:** Support reimbursable summation in `expenses_by_category()` and reconcile category breakdowns against net reimbursable totals.

### #1542: [P1] Map canonical flight fare comparisons and structured ground transport into TripPlan
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1542
- **Labels:** `bug`, `risk:major`, `priority:high`, `type:schema`, `validation`
- **Target:** `src/travel_plan_permission/canonical.py:168-185, 203-216`
- **Reproduction:** `canonical_trip_plan_to_model` parses `flight_pref_outbound.roundtrip_cost` and `lowest_cost_roundtrip` but omits setting `TripPlan.lowest_fare` and `selected_fare`, causing `check_trip_plan()` to always fail `FareComparisonRule`. It also ignores structured `CanonicalGroundTransport` entries.
- **Remediation:** Map roundtrip fare comparisons and ground transport items into the generated `TripPlan` model.

### #1543: [P1] Confine ValidationSnapshotStore file paths to prevent directory traversal
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1543
- **Labels:** `bug`, `risk:major`, `priority:high`, `security`
- **Target:** `src/travel_plan_permission/snapshots.py:143-145, 166-170`
- **Reproduction:** `ValidationSnapshotStore._trip_path(trip_id)` constructs paths with `self.base_path / trip_id` without checking if the resolved path is within `self.base_path`. Supplying `../../tmp/escaped` reads/writes snapshot JSON files outside `SNAPSHOT_DIR`.
- **Remediation:** Enforce `path.resolve().is_relative_to(self.base_path.resolve())` and raise `ValueError` on traversal attempts.

### #1544: [P2] Guard finalized manager review requests against illegal state mutations
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1544
- **Labels:** `enhancement`, `risk:minor`, `priority:normal`, `type:workflow`
- **Target:** `src/travel_plan_permission/review_workflow.py:108-145`, `src/travel_plan_permission/http_service.py:785-802`
- **Reproduction:** `apply_review_action` allows successive `APPROVED` or `REJECTED` transitions on finalized reviews, mutating audit records and flipping terminal decisions.
- **Remediation:** Guard state transitions from terminal states, raise `ValueError`, and map invalid transitions to HTTP 409 Conflict in `http_service.py`.

### #1545: [P2] Parse European slash-separated date formats in ReceiptProcessor
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1545
- **Labels:** `bug`, `risk:minor`, `priority:normal`
- **Target:** `src/travel_plan_permission/receipts.py:149-160`
- **Reproduction:** `ReceiptProcessor._parse_date` tests `%m/%d/%Y` and `%d-%m-%Y` but omits `%d/%m/%Y` and `%d/%m/%y`. Receipts with international date notation (e.g. `15/01/2026`) fail to parse and default to `None`.
- **Remediation:** Include `%d/%m/%Y` and `%d/%m/%y` in the `date_formats` sequence.

### #1546: [P2] Make audit.pending_event_from_state resilient to empty or null metadata_json
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1546
- **Labels:** `bug`, `risk:minor`, `priority:normal`, `security`
- **Target:** `src/travel_plan_permission/audit.py:556-570`, `src/travel_plan_permission/http_service.py:1048`
- **Reproduction:** `pending_event_from_state` parses `state["metadata_json"]` using `json.loads`. Empty strings or invalid JSON raise `json.JSONDecodeError`; JSON `"null"` results in `metadata=None`, causing crashes during audit log reconstitution.
- **Remediation:** Handle decoding errors and null values defensively by defaulting `event.metadata` to `{}`.

### #1547: [P2] Guard workbook_ooxml against corrupting XML on NaN and infinite numeric values
- **URL:** https://github.com/stranske/Travel-Plan-Permission/issues/1547
- **Labels:** `bug`, `risk:minor`, `priority:normal`, `validation`
- **Target:** `src/travel_plan_permission/workbook_ooxml.py:101-105`
- **Reproduction:** `WorkbookWriter._format_cell_value` emits `<v>NaN</v>` or `<v>Infinity</v>` into numeric cell elements, violating the OpenXML schema and corrupting exported workbooks.
- **Remediation:** Check for `math.isnan()` and `math.isinf()` and emit blank cells or string-tagged cells.

---

## 4. Verification & Format Guard Compliance

- **Local Validation:** 9/9 issue bodies passed `.github/scripts/issue_format.py` with zero errors and zero advisories.
- **Remote CI Guard:** `Agents Issue Format Guard` runs completed with `SUCCESS` across all 9 issues. No `agents:format` repair labels were attached.
- **Durable Storage:** Issue drafts saved in `Code/Audits/Travel-Plan-Permission/2026-09-06-refill-issue-bodies/` (01..09).
- **Measurement Intake:** Appended 9 rows to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Ledger Update:** Appended completion record to `Code/Audits/AUDIT_LEDGER.md`.
