## Why

The work-environment response ranks the learning platform as **blocked on hosting** for the same reason as the travel policy engine: it is described as running as an internal web service and additionally needs a database, but the confirmed target environment runs only local scripts, COM-driven Office files, and static HTML pages — nothing server-hosted ([INFORMATION-REQUEST-RESPONSE.md §F item 17, learning platform](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). learning-management-system's implementation target is explicitly *"an API-first backend"* with FastAPI + PostgreSQL (`README.md:16`, `render.yaml:1-5`, `src/lms/main.py:43-50`). Verified: `docker-compose.yml` and `render.yaml` provision Postgres + Uvicorn; no documented local-first alternative exists for the target environment. **Missing behavior:** no documented delivery shape that works without a hosted service and database.

## Scope

Document and verify a local-first delivery alternative — local script and/or static HTML export — for a bounded subset of LMS value (e.g., course manifest export, offline review packet) without requiring Postgres or a running web service, quoting the hosting constraint from the response.

## Non-Goals

- Do NOT remove FastAPI, Postgres, or Render deployment paths — they remain valid for hosted environments.
- Do NOT re-architect the full LMS onto SQLite in this issue.
- Do NOT implement LLM study loops (Milestone 4 scope).
- Scaffold-only completion does NOT count: documentation without a runnable offline command and smoke test is a failure.

## Tasks

- [ ] Add `docs/development/local-first-delivery.md` quoting the hosting constraint: *"the travel policy engine and the learning platform are each described as running as an internal web service (the learning platform additionally needs a database). Nothing built in this environment today runs that way — every tool here is a local script, a COM-driven Office file, or a static HTML page opened locally; there is no server-hosted, database-backed application running anywhere I've seen."* ([response §F item 17](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)).
- [ ] Add `scripts/export_offline_review_packet.py` that reads a committed fixture course graph (JSON/SQLite seed under `tests/fixtures/`) and writes a static HTML review packet to disk — no Uvicorn, no Postgres connection required.
- [ ] Add `tests/test_local_first_delivery.py` asserting the offline packet is self-contained HTML with course/lesson titles present.
- [ ] Link `docs/development/local-first-delivery.md` from `README.md` after the Product Vision section (`README.md:16-17`).
- [ ] Perform deliberate-break verification (see Acceptance Criteria), capture evidence, then revert.

## Acceptance Criteria

- [ ] Named test: `tests/test_local_first_delivery.py::test_offline_packet_is_self_contained_html` passes — generated HTML includes lesson titles from the fixture without external API calls.
- [ ] Documented live-verification gate: `python scripts/export_offline_review_packet.py --fixture tests/fixtures/offline_course_minimal.json --out /tmp/lms-review.html && test -s /tmp/lms-review.html` exits 0; capture command output in the PR.
- [ ] **Deliberate-break gate:** temporarily edit `scripts/export_offline_review_packet.py` to write an empty `<html></html>` shell. `tests/test_local_first_delivery.py::test_offline_packet_is_self_contained_html` **must FAIL**. Revert after capturing the failure.

## Implementation Notes

- Hosting constraint: [response §F item 17](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).
- Confirmed capabilities in target environment: local Python ([response §A Q1](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)), static HTML opened from shared folder ([response §A Q3, §E Q15](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)).
- Confirmed-green local reproduction: `python -m pytest tests/test_database_baseline.py -q` → passes today (hosted DB path unchanged).
