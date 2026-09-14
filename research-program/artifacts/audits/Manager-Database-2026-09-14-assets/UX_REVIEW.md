# Observed UX review — 2026-09-14

Baseline 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Synthetic fixture only; local browser servers closed after capture. Screenshots and DOM: [LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-assets.

Observed: Dashboard and two managers; Elliott portfolio; filing history expansion; Crowd, News Pulse, Activism, and Signals tabs; Daily Report; Search; Upload form; Research disabled-state copy; configured credentials fail before a login form. Five main navigation entries exist, and Alerts management is absent. Empty tabs were recorded as empty synthetic-data states, not presumed backend failures.

The shared ux_review panel ran codex, cursor, gemini, and vibe plus a cursor critic. Raw reported medians: wired 2.5, usability 4.5, help 5, productivity 4.5, overall 3.0. The machine gate returns done=false for gate1_not_ok, overall_median_below_7.0, and blockers_present. These subjective scores are advisory, not measured product correctness or audit-completion scores. All rubric outputs and the critic file are nonempty; parsed adversarial aggregation did not expose findings, so it is not counted as a clean independent approval.

Adjudication: retain configured-auth crash (F01) and unreachable Alerts management (F07). Collapse overlapping navigation and recovery suggestions into those bodies. Reject claims that Upload is broken or requires the Research backend: no upload was performed and source writes directly to the database. Reject disabled Send as a defect when the question is empty. Reject a missing portfolio selector: manager selection and portfolio rendering were observed. Defer same-date nearest-date messaging and richer links as optional product polish. Do not infer production Postgres failures from a SQLite fixture.

Coverage limits: no actual file upload, alert CRUD, answer submission, provider calls, production data, or work-endpoint WASM trial. Browser used Streamlit 1.63.0; actual locked 1.60.0 tests separately pass while pinned configured-auth reproduction still fails. Product readiness remains failed; audit research is complete.
