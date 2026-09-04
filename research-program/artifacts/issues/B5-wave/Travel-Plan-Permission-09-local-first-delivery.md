## Why

The work-environment response ranks the travel policy engine as **blocked by a hosting gap**: it is described as running as an internal web service, but nothing built in that environment runs that way — every working tool is a local script, a COM-driven Office file, or a static HTML page opened locally; there is no server-hosted, database-backed application ([INFORMATION-REQUEST-RESPONSE.md §F item 17, travel policy engine](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Travel-Plan-Permission's primary surface today is `tpp-planner-service` (FastAPI + Uvicorn) at `src/travel_plan_permission/http_service.py:2298-2359` with a hosted Render blueprint at `render.yaml:7-33`. Verified: the repo already ships a headless CLI (`fill-spreadsheet` at `README.md:35-41`) but no documented **local-first delivery shape** that avoids standing up the HTTP service. **Missing behavior:** operators in the target environment have no documented path to policy evaluation without hosting.

## Scope

Document and verify a local-first delivery alternative — local script and/or static HTML page — that delivers policy evaluation value without a hosted service, quoting the hosting constraint from the response.

## Non-Goals

- Do NOT remove or deprecate `tpp-planner-service` — the hosted path remains for environments that support it.
- Do NOT implement new policy rules in this issue.
- Scaffold-only completion does NOT count: a README paragraph without a runnable command and a smoke test is a failure.

## Tasks

- [ ] Add `docs/local-first-delivery.md` quoting the hosting constraint: *"Nothing built in this environment today runs that way — every tool here is a local script, a COM-driven Office file, or a static HTML page opened locally; there is no server-hosted, database-backed application running anywhere I've seen."* ([response §F item 17](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)) and mapping it to this repo's surfaces.
- [ ] Document the `fill-spreadsheet` CLI path (`README.md:35-41`) as the primary local-first workflow for trip-plan JSON → Excel output without `tpp-planner-service`.
- [ ] Add `scripts/render_policy_report.py` (or extend an existing CLI) that evaluates a `TripPlan` JSON file via `PolicyEngine` and writes a static HTML report to disk (no Uvicorn), suitable for `file://` opening per [response §A Q3](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).
- [ ] Add `tests/python/test_local_first_delivery.py` smoke-testing the static HTML generator against `tests/fixtures/sample_trip_plan_minimal.json`.
- [ ] Link `docs/local-first-delivery.md` from `README.md` under a new "Local-first delivery (no hosted service)" section after the Planner HTTP Service heading (`README.md:49`).
- [ ] Perform deliberate-break verification (see Acceptance Criteria), capture evidence, then revert.

## Acceptance Criteria

- [ ] Named test: `tests/python/test_local_first_delivery.py::test_static_policy_report_is_self_contained_html` passes — output HTML contains policy verdict text and requires no network fetch to render.
- [ ] Documented live-verification gate: `python scripts/render_policy_report.py tests/fixtures/sample_trip_plan_minimal.json /tmp/policy-report.html && test -s /tmp/policy-report.html` exits 0 with a non-empty file; capture command output in the PR.
- [ ] **Deliberate-break gate:** temporarily edit `scripts/render_policy_report.py` to emit a placeholder without calling `PolicyEngine.evaluate`. `tests/python/test_local_first_delivery.py::test_static_policy_report_is_self_contained_html` **must FAIL**. Revert after capturing the failure.

## Implementation Notes

- Hosting constraint source: [response §F item 17](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).
- Local-file deep links confirmed working in [response §A Q3](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) — static HTML should link to local policy evidence files where applicable.
- Confirmed-green local reproduction: `python -m pytest tests/python/test_http_service.py -q` → passes today (HTTP path unchanged).
