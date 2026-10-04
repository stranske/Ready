#!/usr/bin/env python3
"""Repair frozen issue bodies for D3 pass2; validate then gh edit."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

GH = ["[LOCAL_HOME]/.codex/bin/detached-net.sh", "gh"]
CLONE = Path("[LOCAL_HOME]/.codex/automations/research-program/clones")

REPAIRS: dict[tuple[str, int], str] = {
    (
        "trip-planner",
        1837,
    ): """## Why

The approval packet is the one document this product hands an employer, and on the 2026-09-22 audit tip (8a7d81ad), driven in a browser against a live TPP service, it states things that are not true:

- **"Budget cap: $0 … Scenario total is $1,238 above the budget cap."** No cap was ever set. `frontend/src/components/workspace/ApprovalPacket.tsx:70-74` formats `budget_state.summary.planned_total`, whose unset default is `0.0` (`trip_planner/app/services/workspace.py`, resolved_budget_state default), and computes `planned_total - scenarioAmount`. TPP's real cap (BUD-001, $5,000) would leave $3,762 of headroom.
- **"Compliance score 15%"** (`ApprovalPacket.tsx:58`) is `0.15` hard-mapped from the outcome `non_compliant` in `trip_planner/integrations/tpp/client.py:1072-1074` (`1.0 if compliant else 0.45 if exception_required else 0.15`). TPP returns no score. It is a relabelled verdict shown as a measurement.
- **"itinerary: Chicago, IL runtime bundle from tpp — $1,238"** (`ApprovalPacket.tsx:92`) names the policy engine as the vendor. The per-component prices the traveller entered (United.com $486, Hyatt $612, meals $140) and their sources never reach the packet, although `GET /api/workspace/{id}/prices` serves them with `price_source`.
- **No traveller name, no origin, no itinerary, no approval area.** The packet prints trip, purpose, dates and destination only.
- **After a fresh sign-in the printed verdict reads "Not evaluated"** beside "Policy blocked this proposal: fare_comparison, …", because the evaluation result fetched in the browser session is not persisted.
- **A one-page packet prints three Letter pages; pages 2–3 are blank.** `frontend/src/styles.css:180-202` hides the app with `visibility: hidden`, which keeps its 2,047px of layout.

## Scope

`frontend/src/components/workspace/ApprovalPacket.tsx`, its print rules in `frontend/src/styles.css`, `trip_planner/integrations/tpp/client.py` (compliance score), and whatever backend change is needed for the packet to read persisted verdict detail and the entered prices.

## Non-Goals

- Do not invent a cap, a score or a figure to fill a gap. Absent means printed as absent ("No budget cap set", "Not scored by the policy service").
- Do not build a PDF service; the browser print path is the deliverable here.
- Scaffold-only work (new fields that render nothing, TODO sections) does not count as done.

## Tasks

- [ ] In `frontend/src/components/workspace/ApprovalPacket.tsx`, stop printing an unset cap as `$0`, and stop comparing the trip total against it; show "No budget cap set" when no cap exists; drop the nine "cap $0; remaining -$0" category lines when no category cap exists.
- [ ] In `trip_planner/integrations/tpp/client.py`, remove the fabricated `compliance_score` mapping at lines 1072-1074 (emit `None`), and render the packet row in `ApprovalPacket.tsx` only when a real score exists.
- [ ] In `frontend/src/components/workspace/ApprovalPacket.tsx`, print the entered cost breakdown from `/api/workspace/{id}/prices`: one line per component with amount, the traveller's source note, "entered by <name> on <date>"; remove the `from tpp` vendor attribution for traveller-entered totals.
- [ ] In `frontend/src/components/workspace/ApprovalPacket.tsx`, add the requester (traveller display name), origin → destination, and a date-prepared line; add an approver block (name, decision, signature, date) as blank fields.
- [ ] In `trip_planner/app/services/workspace.py` (or the proposal persistence layer), persist the evaluation result the Policy tab fetches so a printed packet after reload shows the same verdict and reasons as the screen; never print "Not evaluated" next to policy-block reasons.
- [ ] In `frontend/src/styles.css`, replace `visibility: hidden` print isolation with rules that remove the app from layout (`display: none` on the app shell siblings), so a one-page packet prints one page.

## Acceptance Criteria

- [ ] Run `cd frontend && npm test -- src/components/workspace/ApprovalPacket.test.tsx` and confirm the suite passes: with `planned_total: 0` and no cap, the text contains "No budget cap set" and matches neither `/\\$0\\b/` nor `/above the budget cap/`; with entered prices it lists each component with its source and "entered by"; the traveller name is present; no "Compliance score" row when the score is null.
- [ ] Run `pytest tests/integrations/tpp/test_client_compliance_score.py` (or the focused backend test added for this issue) and confirm `compliance_score` is `None` for every outcome.
- [ ] Run `cd frontend && npm run test:e2e` with the print-media packet scenario (or the documented Playwright gate) and confirm a one-page Letter print for the audit trip.

## Reproduction

```bash
# live TPP on :8100 (see Code/Audits/trip-planner/2026-09-22-audit-run.md), backend :8000, vite :5173
# sign up; create business trip Seattle -> Chicago 2026-10-05..07; Budget tab: enter 486 / 612 / 140;
# Policy tab: Submit for approval; Print / Export approval packet
```
Evidence: `Code/Audits/trip-planner/2026-09-22-assets/screens/packet-print-layout.png`, `packet-print.pdf`.
""",
    (
        "trip-planner",
        1838,
    ): """## Why

When TPP refuses a proposal on policy grounds, the Policy tab tells the traveller the service is down.
Observed 2026-09-22 against a live TPP service: the response was `queue_state: blocked_by_policy` with `blocking_codes: [fare_comparison, fare_evidence, non_reimbursable]`, and the page showed:

- heading **"Policy service unavailable"** in an otherwise empty card (`frontend/src/components/workspace/panels/PolicyPanel.tsx:192-202`);
- **"Retry policy check"**, which cannot change a policy verdict;
- **"Review the live transport failure — Validate the remote TPP configuration and retry posture before asking travelers to treat this workspace as approval-ready"** (`frontend/src/routes/WorkspacePage.tsx:2768`) — operator copy, shown to a traveller, and false.

Cause: `derivePolicyPanelView` (`PolicyPanel.tsx:91-99`) maps every `submission_status == "failed"` to `service-unavailable` before it reaches the existing `non-compliant` branch (`:116`). The backend already distinguishes the two since PR #1835 (`summary.submission_outcome == "blocked_by_policy"`, `summary.submission_blocking_codes`); the frontend never reads them.

The remedy text the page does show ("Attach the supporting fare comparison before requesting evaluation again") has no control behind it: nothing in the UI can attach evidence.

## Scope

`frontend/src/components/workspace/panels/PolicyPanel.tsx`, the approval-details cards in `frontend/src/routes/WorkspacePage.tsx` (~2700-2780), `frontend/src/api/workspace.ts` summary types.

## Non-Goals

- Do not build evidence upload in this issue (file separately if wanted); but do not tell the traveller to attach something they cannot attach — say what TPP needs and where to send it.
- Do not relabel genuine transport failures; `submission_outcome == "failed"` must still show the service state.

## Tasks

- [ ] In `frontend/src/components/workspace/panels/PolicyPanel.tsx`, check `summary.submission_outcome === "blocked_by_policy"` first in `derivePolicyPanelView` and return `kind: "non-compliant"` with `issueCodes = summary.submission_blocking_codes`.
- [ ] In `frontend/src/components/workspace/panels/PolicyPanel.tsx`, map each known TPP code to a plain sentence and a next step (at least `fare_comparison`, `fare_evidence`, `non_reimbursable`, `BUD-001`), keeping the code visible.
- [ ] In `frontend/src/routes/WorkspacePage.tsx`, remove "Retry policy check" and the "transport failure" card for policy blocks; keep them for `submission_outcome === "failed"`.
- [ ] In `frontend/src/routes/WorkspacePage.tsx`, remove the duplicate "Approval packet" card so one card states the outcome.
- [ ] In `frontend/src/routes/WorkspacePage.tsx`, replace "Attach the supporting fare comparison" with guidance the traveller can act on until an attach control exists.

## Acceptance Criteria

- [ ] Run `cd frontend && npm test -- src/components/workspace/panels/PolicyPanel.test.tsx` and confirm: a summary with `submission_status: "failed"`, `submission_outcome: "blocked_by_policy"`, `submission_blocking_codes: ["fare_comparison"]` renders `policy-state-non-compliant` containing `fare_comparison`, and renders neither "Policy service unavailable" nor "Retry policy check"; the inverse case (`submission_outcome: "failed"`) still renders the service-unavailable state.

## Reproduction

```bash
curl -s -b cookies http://127.0.0.1:8000/api/workspace/<trip>/proposal | jq '.summary | {submission_status, submission_outcome, submission_blocking_codes}'
```
""",
    (
        "trip-planner",
        1842,
    ): """## Why

The journey ends at "print a packet and hand it over". Travel-Plan-Permission already exposes draft-scoped portal handoffs and a manager review queue; trip-planner never calls them (no `/portal` usage under `trip_planner/` or `frontend/src/`).

## Scope

A "Send to my approver" action on the Policy tab that performs the TPP hand-off with the trip, entered prices and verdict; show the resulting request / review status back in the workspace.

## Non-Goals

- No changes to TPP's review queue.
- Printing stays available.

## Tasks

- [ ] In `trip_planner/integrations/tpp/client.py`, read TPP's hand-off contract (`_PORTAL_REQUIRED_FIELDS`, `_canonical_payload_from_answers`) and map trip-planner's trip, prices and verdict onto it.
- [ ] In `frontend/src/routes/WorkspacePage.tsx`, add the "Send to my approver" action and a status line ("Sent to approver on <date>; awaiting decision").
- [ ] In `frontend/src/api/workspace.ts` and `frontend/src/routes/WorkspacePage.tsx`, surface the manager decision when TPP records one.

## Acceptance Criteria

- [ ] Run `pytest tests/integration/test_portal_handoff.py` (or the integration test added for this issue) against TPP's app (in-process or the local service) and confirm a trip sent through `/portal/handoff/draft` appears in `/portal/manager/reviews`.

## Implementation Notes

TPP reference implementation lives in the Travel-Plan-Permission repository (`travel_plan_permission/portal_handoff.py`, `http_service.py` portal routes); this issue wires trip-planner to that contract only.
""",
    (
        "trip-planner",
        1844,
    ): """## Why

Observed across the workspace on 2026-09-22 — developer vocabulary a business traveller cannot use (runtime bundle titles, missing origin, duplicated Compare panels, non-functional "View route", developer-only Trip detail and Status nav).

## Scope

Traveller-facing copy and navigation in `frontend/src/routes/WorkspacePage.tsx`, `frontend/src/routes/TripDetailPage.tsx`, `frontend/src/components/workspace/RouteOptionWorkbench.tsx`, and related workspace components.

## Tasks

- [ ] In `frontend/src/routes/WorkspacePage.tsx` and `frontend/src/components/workspace/RouteOptionWorkbench.tsx`, display names from the trip ("Seattle → Chicago") instead of bundle titles and slug ids; remove the title-casing of sentences.
- [ ] In `frontend/src/routes/WorkspacePage.tsx` and map/route panels, show origin as the first stop everywhere a route is drawn or described.
- [ ] In `frontend/src/routes/WorkspacePage.tsx`, collapse Compare to one comparison view.
- [ ] In `frontend/src/components/workspace/RouteOptionWorkbench.tsx` and `frontend/src/routes/WorkspacePage.tsx`, make "View route" switch to the Map with that route selected, or remove it; persist the editorial slider in workspace state or remove it.
- [ ] In `frontend/src/routes/TripDetailPage.tsx`, replace the data dump with a readable summary and "Open plan"; move "Status" out of the primary nav in `frontend/src/App.tsx` (or the nav config it uses).

## Acceptance Criteria

- [ ] Run `cd frontend && npm test -- src/routes/WorkspacePage.test.tsx` and confirm the Seattle→Chicago fixture asserts no rendered text matches `/runtime bundle|persisted|Dest-[A-Z]|\\(S\\)/` and that the first stop shown is "Seattle".

## Non-Goals

Re-opening product work already delivered on `main` via merged PR #1862 is out of scope for a new implementation pass; this issue remains the audit record unless a regression is reproduced on tip.
""",
    (
        "learning-management-system",
        718,
    ): """## Why

D4 implementation verification (`D4-verify-merged-2026-09-24T03`) read the squash merge for PR #711 (merge commit `3bdd840da6dd9d658dc6f6da2d599def00b3a936`). Production code and the named gate test(s) are present in the diff, but the PR body does **not** include the issue-required deliberate-break fail→revert transcript.

## Scope

Recover or document disposition evidence for PR #711 only; do not reopen merged product code without a reproduced defect.

## Tasks

- [ ] Run `gh pr view 711 -R stranske/learning-management-system --json body,comments` and extract any deliberate-break transcript sections for linked issue #580.
- [ ] Run `gh pr checks 711 -R stranske/learning-management-system` to capture the final check state at merge time.
- [ ] Run `gh pr comment 711 -R stranske/learning-management-system --body-file docs/verification/pr-711-disposition.md` with the evidence-backed disposition (create `docs/verification/pr-711-disposition.md` in this repo if missing).

## Acceptance Criteria

- [ ] `gh pr view 711 -R stranske/learning-management-system --json body,comments` shows the disposition or a linked follow-up stating evidence cannot be recovered.
- [ ] `gh pr checks 711 -R stranske/learning-management-system` reports the final check state.
- [ ] Verification comment on PR #711 cites sourced command output or documents recovery impossibility.

## Non-Goals

- Fabricating historical test output or merging new product changes under this follow-up.

Related: #580
""",
    (
        "Fine-Art-Archive",
        735,
    ): """## Why

Dropbox conflict resolution on the synced archive workspace forks `operations.log`, `discovery_frontier.json`, and lock files when two hosts run the scheduled tick against the same tree. Measured on the Mac workspace 2026-09-21 (nine conflicted copies; G55 budget undercount; discovery cycle rolled back).

## Scope

Repository-owned guards and lock placement for Track A automation (`scripts/build_weekly_review.py`, `src/fine_art_archive/api/gates.py`). Data merge of forked workspace files is out of scope here.

## Non-Goals

- Do not merge or delete owner workspace conflict copies without an explicit relocation grant.
- Do not change image bytes under `data/` or work sidecars.

## Tasks

- [ ] In `src/fine_art_archive/api/gates.py`, document and enforce a non-synced lock path (or host-aware lease) instead of a lock file on the Dropbox-synced workspace root.
- [ ] In `scripts/build_weekly_review.py`, add a preflight that fails when any `*conflicted copy*` filename exists beside `operations.log` or `discovery_frontier.json` defaults.
- [ ] Add `tests/test_workspace_conflict_guard.py` with `pytest` coverage for the conflicted-copy detector and lock-path policy.

## Acceptance Criteria

- [ ] Run `pytest tests/test_workspace_conflict_guard.py` and confirm conflicted-copy filenames fail the guard and a fixture without conflicted-copy names passes.
- [ ] Run `python scripts/build_weekly_review.py --help` and confirm the new preflight flag or default behavior is documented in the CLI help text.

## Implementation Notes

Evidence in the issue body references Dropbox workspace paths that are not checked into git; agents implement guards in this repository and leave fork reconciliation to the owner.
""",
}


def validate(repo: str, body: str) -> str:
    root = CLONE / repo
    fmt = root / ".github/scripts/issue_format.py"
    py = root / ".venv/bin/python"
    interpreter = str(py) if py.exists() else "python3"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        fpath = f.name
    p = subprocess.run([interpreter, str(fmt), fpath], cwd=root, capture_output=True, text=True)
    os.unlink(fpath)
    return (p.stdout + p.stderr).strip()


def apply(repo: str, number: int, body: str) -> None:
    full = f"stranske/{repo}"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        fpath = f.name
    subprocess.run(GH + ["issue", "edit", str(number), "-R", full, "--body-file", fpath], check=True)
    os.unlink(fpath)
    subprocess.run(
        GH + ["issue", "edit", str(number), "-R", full, "--remove-label", "agents:auto-pilot-pause"],
        check=True,
    )


def main() -> None:
    results = []
    for (repo, num), body in REPAIRS.items():
        msg = validate(repo, body)
        ok = "not yet agent-processable" not in msg.lower()
        results.append((repo, num, ok, msg))
        print(f"{repo} #{num}: {'OK' if ok else 'FAIL'}")
        if not ok:
            print(msg[:1200])
            continue
        apply(repo, num, body)
        print(f"  -> applied and removed agents:auto-pilot-pause")
    Path("[LOCAL_HOME]/.codex/automations/research-program/artifacts/sweeps/_d3_pass2_repair_results.json").write_text(
        json.dumps([{"repo": r, "num": n, "ok": o, "msg": m} for r, n, o, m in results], indent=2)
    )


if __name__ == "__main__":
    main()
