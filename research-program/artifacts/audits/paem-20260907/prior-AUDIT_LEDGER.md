# Audit Ledger

Last updated: 2026-09-06 (learning-management-system Track D refill audit completed @ fd0ea51; 9 issues filed #602-#610). Previous entry: 2026-09-06 Fine-Art-Archive refill.

Purpose: keep a durable, cross-session record of repo audits without letting prior audits narrow the scope of future audits. Prior audits are continuity and duplicate-check context. Every new audit round should still re-run the full audit category set against current code.

## Audit Categories

The base audit categories remain:

1. Code quality and correctness
2. Duplication and consolidation
3. Functionality and wiring
4. Design and UX
5. Approach versus the public field
6. Missed opportunities
7. Tools worth integrating
8. Local skills, automations, and human touchpoints

Route-Weight / Exploration candidate scoring is intentionally kept outside the durable audit log. Current temporary notes live in `ROUTE_WEIGHT_WORKING_NOTES.md`; the optional process proposal lives in `AUDIT_SKILL_UPDATE_PROPOSAL.md`.

## Continuity Rule

For each repo run, read prior audit records and open issue/PR state only to:

- avoid duplicate filing
- identify stale or resolved findings
- preserve prior decisions and owner context
- detect repeated defect classes

Do not use prior findings to constrain which categories the new audit evaluates.

## Active Audits

| Repo | Audit status | Started | Source / automation | Scope | Base SHA | Next ledger action |
|---|---|---:|---|---|---|---|
| `JobSearch.2026` | Completed; collection/evaluation/source-system audit and prioritized backlog | 2026-08-13 | Codex repo-audit + Orchestrator (valid synthesis excludes invalid Claude auto-top-up) | Gmail/job-board/official-career collection, parsing/dedupe, source yield, feedback-derived evaluation, persistence, review UI, cadence, and unattended-queue recovery | non-git workspace | `JobSearch.2026/AUDIT_REPORT.md`; system map; source, pipeline, operator, UX, and adversarial evidence; no issue filing or product improvement implementation |
| `Workflows` | Completed; focused human-intervention and anti-passivity audit | 2026-08-12 | Codex repo-audit + actionable GitHub triage + live case evidence | Reviewed-repo controller, issue workloop, maintenance/orphan stewardship, Workflows auto-pilot, scoped blockers, and every human-attention case handled in the 2026-08-12 follow-through | `66e9de18` | Implement the pre-latch and >24h independent challenge loop, then repair terminal/capability taxonomy and enforce active-worker plus concrete-next-action invariants |
| `Workflows` | Completed; focused dependency/sync efficiency audit | 2026-08-01 | Codex repo-audit + Orchestrator read-only offloads + live GitHub/Actions evidence | Renovate/dependency intake, Maint 52 dev-tool propagation, Maint 68 consumer sync, Maint 71 merge control, campaign cadence, PR amplification, and operator cost | `e42f6af3` | Review report; if implementing, start with manifest-derived Renovate ownership filtering, intake limits, and Health 68 covered-drift semantics |
| `trip-planner` | Completed; implementation verified and pushed | 2026-07-10 | Codex repo-audit; bounded Orchestrator read-only offloads after orientation | Function/module code quality, repo-owned tests/config, dual-repo wiring, observed UX, and two-trip live-run design | `f6d486b3` | Review/merge branch; implement remaining audit findings separately |
| `Travel-Plan-Permission` | Completed; organizational workbook/intake implementation verified and pushed | 2026-07-10 | Codex repo-audit; bounded Orchestrator read-only offloads after orientation | Function/module code quality, repo-owned tests/config, dual-repo wiring, observed UX, and two-trip live-run design | `534a3f5` | Review/merge branch; implement concurrency, package-resource, and numeric-bound findings |
| `Trend_Model_Project` | Completed; implementation verification of 5 closed issues | 2026-08-24 | Claude Opus 5 `implementation-verification` skill, headless, run alone (single ledger writer); `adversarial.review` (vibe+cursor) for the contested verdict; first-person runtime re-measurement | Squash diff of each merge commit vs each acceptance task at its cited file:line; named test gate presence, exactness and pass state; CI conclusion; owner-decision check | `d3069d87` (HEAD) | 4 delivered, 1 NOT delivered (#5986). Owner decision on filing bodies 01-02; if only one, file **01** - the defect is live and a merged test pins it |
| `Workflows` | Completed; implementation verification of 5 closed issues | 2026-08-24 | Claude Opus 5 `implementation-verification` skill, headless, run alone; `local_verify.py` used to supply the deliberate-break proofs 3 PR bodies omitted; live Actions/issue state read via `gh` | Squash diff vs acceptance tasks; all 9 named gates collected and run; every shell-level AC executed for its exit code; live runtime ACs (Health 68 execution, #2210 marker freshness) | `a377fd30` (HEAD) | 4 delivered, 1 partially delivered (#3183). Owner decision on filing bodies 03-04; if only one, file **03** - the liveness oracle cannot see a no-op |

## Full Audit Index

| Repo | Audit status | Started | Completed | Source / automation | Durable summary | Main findings by category | Issues / PRs generated | Next ledger action |
|---|---:|---:|---:|---|---|---|---|---|
| `Trend_Model_Project` | Completed; scoped (GUI/runner + config surface) | 2026-08-23 | 2026-08-23 | Claude Opus 5 `repo-audit` skill, headless, no scoping interview (scope pre-decided); three bounded read-only Orchestrator `dispatcher.offload` partitions (gemini config-wiring, cursor annualization, vibe validation); `adversarial.review` (codex+vibe) for refutation; `local_verify.py` for the break proofs; fresh shallow clone of remote `phase-3` @ `f6d5582d` on local disk | `Trend_Model_Project/2026-08-23-AUDIT_REPORT.md` (+ verification log, run record, **capability-evidence log**, 3 offload reports, 5 issue bodies, 5 gate tests in assets/) | **Dimension 3/4 only** (5/6/7 deliberately not covered). The 2026-08-11 "two paths, one contract" class is still dominant and has moved into the operator surface: (1) `unified.py:475-483` reports "Target volatility 10.0%" beside "Signal scaling Raw" on shipped `config/defaults.yml` while its sibling at `:362-366` gates correctly; (2) `gui/app.py:885` hardcodes `["xlsx","csv","json"]` against a four-entry `export.EXPORTERS`, so `txt` is unselectable and a persisted format bricks `launch()` with a `TraitError` clearable only by hand-editing `~/.trend_gui_state.yml`; (3) `analysis_runner.py` validates cost bps as float at `:408-409` and truncates to int at `:258,281`, so `half_spread_bps: 0.5` runs as 0; (4) the Run button fails silently three ways and ipywidgets swallows every callback exception, so the GUI has no error surface; (5) `portfolio.max_turnover` has three ceilings (schema 2 / `Config` 2.0 / `PortfolioSettings` 1.0) with contradictory comments, and `cli.py:926` uses the strict one. Root cause of (1)+(2) surviving: `test_gui_app_extended.py:57-67` stubs the ipywidgets classes so widget contracts are untestable. **Declined/refuted**: 3 of the commissioning brief's own claims were stale or false (`_run_folder_name` gone; `_compute_stats` has no `periods_per_year` default; `input_validation` now delegates); gemini's `extra="ignore"` BLOCKER refuted by `lint_keys.py`; its 11-row inert-key table dropped at a >=18% false-positive rate; vibe's csv-validation BLOCKER marked INSUFFICIENT_EVIDENCE after I failed to build a divergent input | 5 issues, triage-only (verified no `agent:*`/`agents:*`/`status: ready`): [#5984](https://github.com/stranske/Trend_Model_Project/issues/5984) cost-bps validate/run split, [#5985](https://github.com/stranske/Trend_Model_Project/issues/5985) export-format drift bricks launch, [#5986](https://github.com/stranske/Trend_Model_Project/issues/5986) unapplied vol target reported, [#5987](https://github.com/stranske/Trend_Model_Project/issues/5987) silent Run button / no error surface, [#5988](https://github.com/stranske/Trend_Model_Project/issues/5988) three max_turnover ceilings. 0 PRs; nothing pushed; no product state changed | Verify #5984-#5988 against squash diffs and the named test gates, not issue status. Then close the 7 deferred rows in the verification log, starting with the two that only need a weekly-frequency fixture (`unified.py` re-annualization with `ddof=0` and the `12.0` fallback; ranking RF cadence vs `window.periods_per_year`). Separately: feed `Code/Audits/<repo>/README.md` "Standing notes" into `repo_knowledge`, because the advisor recommended `frontend-verifier` for this repo twice while this repo's own audit record says it does not work here |
| `Trend_Model_Project` | Completed; feedback complete, literal legacy purge partial | 2026-08-22 | 2026-08-22 | Codex `repo-audit` + Orchestrator Cursor/Vibe read-only partitions; fresh clone at remote `phase-3` `4e5cdfb8`; live GitHub/CI/review-thread evidence; Claude not used | `Trend_Model_Project/2026-08-22-feedback-completion-AUDIT_REPORT.md` (+ completion ledger, verification log, run record, two Orchestrator reports) | All 91 first-round and 29 second-round findings are implemented, verified, historical, or current intentional designs; all named legacy packages/commands/config/facades are absent and gated. Literal-policy gaps: `api._run_analysis` test hook, `ValidatedMarketData` implicit DataFrame proxy, script `MODEL_PAGE` alias, stale MC/demo/planning descriptions, and source-first Workflows `check_capability` migration. PR #5912 has two active non-outdated P1 threads whose code substance is already fixed. Current CI green; local focused gate 65/65. | 0 issues; 0 PRs; audit artifacts only | Implement LR-9-1 through LR-9-6 in the renewed ledger, strengthen the semantic legacy gate, run final unchanged-head proof, and obtain reviewer-owned disposition of PR #5912 threads |
| `Workflows` | Completed; false human-intervention stops | 2026-08-12 | 2026-08-12 | Codex repo-audit + actionable GitHub triage; fresh remote-tip source `66e9de18`; live GitHub, local handoff state, liveness, and controller evidence | `Workflows/2026-08-12-human-intervention-AUDIT_REPORT.md` (+ system map, verification log, run record) | Every reviewed case could progress through automation. P0: automation-created human stops are unreviewed and permanent; P0: failures/concerns/unknowns collapse into lack-of-authority. P1: controller pass-through has no freshness/challenge; decisions/defaults are not retrieved; specialist recovery lanes are not routed. Live recurrence: 3 open `needs-human` PRs, 2 attention PRs, 2 scoped human claims; generated Ready #522 was 26.16h old. | 0 issues; 0 PRs; 0 product/GitHub changes | Build `human-blocker-challenge`: independent pre-latch review and age loop at 24h, 72h, weekly; require authority proof; clear/reroute false stops; keep a worker and concrete next action active |
| `learning-management-system` | Completed; P0s implemented, merged, and verified | 2026-08-01 | 2026-08-01 | Claude (Fable 5) repo-audit skill + Orchestrator offloads (codex correctness, gemini wiring [report salvaged], vibe docs/dup [cursor API down], claude web-research) + observed UX drive (compose@tip PG18, deployed-mode parity) + ux_review.py panel (4 evaluators, 3.0/10) + live Render probes; fresh off-Dropbox clone @ `169f5363`; CI green as test truth | `learning-management-system/2026-08-01-AUDIT_REPORT.md` (+ UX_REVIEW, verified-findings, 5 lane artifacts, assets/, 3 issue bodies) | **Platform READY** (live deploy healthy, auth enforced, compose fixed, paid Render plans; ALL May-30 fixes #192-#200/#230/#351 regression-verified genuine). **Product loop BLOCKED, observed:** P0 LMS-R1 learner-identity bootstrap dead-end (create-user makes User only; learners router unmounted in prod; UI defaults ?learner_id=learner-1 silently empty); P0 LMS-R2 attempts never score/schedule (UI+API paths skip schedule_from_attempt; rubric scoring API-only; DB-verified) + R16 queue mis-link ui/api.py:379. P1: inert LLM_DAILY_BUDGET_USD (R3), rubric-score dup on retry (R4), remediation triggers unwired (R5), NaN guards (R6), learner authz (R7). P2 batch + dims5-7 FSRS-trio roadmap (py-fsrs seam exists; ladder is planned scaffold). Adversarial kills: vibe 2 majors, gemini 1, lead 1 | **0 issues filed; 2 PRs MERGED** — #492 (`ede38c0e`) learner identity bootstrap + ownership (R1/R7); #494 (`7a004644`) learning-loop wiring, self-grading, queue link/completion, rubric idempotency, remediation triggers (R2/R16/R17/R4/R5). Owner directed direct implementation over filing. Both gates green (3.12+3.13, ruff, mypy, Compose smoke); post-merge ci.yml SUCCESS on both commits; new gate tests `test_deployed_first_use.py` + `test_attempt_to_next_review_e2e.py` with deliberate-break demonstrated | **DONE + VERIFIED 2026-08-02**: re-drove merged main in deployed parity — create-user provisions learner; login → owned home + onboarding; foreign/legacy learner_id → 403; attempt → self-grade → 1-day review → mark reviewed → 3-day ramp (spaced repetition advances through the UI); live Render instance serves both new routes, /health ok. Readiness upgraded to **usable for first real use**. Remaining: R3 (inert LLM budget env var), R6 (NaN guards), R8 (/docs exposure), R10-R15, R18-R23 UX polish, then the FSRS trio roadmap |
| `Workflows` | Completed; detailed dependency/sync productivity redesign, no filing | 2026-08-01 | 2026-08-01 | Codex repo-audit + three bounded Orchestrator read-only reviews; fresh remote-tip clone `e42f6af3`; live org PR counts, Actions trigger/conclusion counts, direct PR-file samples, official Renovate/GitHub docs | `Workflows/2026-08-01-AUDIT_REPORT.md` (+ verification log, non-actionable log, repo map, and three raw analytical artifacts) | Post-migration generated traffic 2,178 PRs/49d (44.45/day), +19.5% normalized vs pre; Renovate +317.6% PR/day while sync -32.5% and dev-tool +194%; 47.2% of retrievable Renovate PRs were digests and at least 405 were confirmed updates to Workflows-owned consumer files; Maint 68 had 75 manual dispatches/135 runs; Health 68 had 249 runs, zero successes, and 223 tracker comments; source defects are found after fleet fan-out; hash-suffixed waves and three controllers amplify repair work | 0 issues; 0 PRs; 0 production source changes | Implement in phases: ownership-aware Renovate filtering/intake limits, covered-drift semantics, source+canary validation, stable per-repo generated PRs, then controller consolidation |
| `Reader` | Completed; educator-access audit + full P0/P1 implementation — all 6 P0s and 17/18 P1s closed, only Gatekeeper deferred | 2026-08-08 | 2026-08-09 | Claude (Opus 5) repo-audit skill + UX overlay (observed-only, app driven live at build `eafe1e0a29b0`) + Workflow (4 path-scoped read-only finders → adversarial verifiers; 6/8 agents completed, 2 verifiers hit session limit) + Orchestrator offloads (cursor ×3; **gemini offload dead fleet-wide — `dispatcher.py:1604`/`adapters.py:44` pin `gemini-2.5-pro`, unknown to the installed CLI, while `capacity.py` still reports gemini `ok`** — re-routed to cursor). No git remote, so no CI/issues/PRs. | `Reader/2026-08-08-AUDIT_REPORT.md` (+ UX_REVIEW, human-effort-analysis, 6 lane artifacts, 3 verification files, assets/) · artifact https://claude.ai/code/artifact/7801ac2d-e4a0-47d9-9a6a-8e1006ffc3f1 | **Two problem classes.** *Class B (silent failure, all OPEN, verified):* P0-1 `serverSave()` discards the server error so a rejected DB write shows "Saved ✓ … server wasn't reachable" — false cause, session only in localStorage (`app.js:2507`, `:2603-2606`, `server.py:1206`, HTTP 200 + `ok:false`); P0-2 unguarded `localStorage.setItem` *before* the durable write throws out of `saveSession()` with zero feedback (`app.js:2595-2598`); P0-3 no lock/detection/warning for a second writer to the Dropbox SQLite file, no WAL (`server.py:564`); P0-4 `#readAdult` hidden by `body.student-mode` with **no counter-rule**, so an untranscribed read scores ~0% silently (`styles.css:382`); P0-5 unexplained "🎯 Calibration run" filters the session out of every chart (`index.html:236`→`app.js:2853`); P0-6 "never flag these" is a **substring** match and the app's own example `r` inflates accuracy/WCPM invisibly (`app.js:3181`). *Class A (orientation, FIXED):* no first-run state existed at all; the 12-step walkthrough sat 1378px down a 1442px form, `ghost`-styled, labelled "optional"; gated-nav feedback rendered 424px off-screen with no scroll/focus; **`build-dist.sh` never shipped `docs/`** so the educator received zero prose. *Install (read-only trace):* Gatekeeper blocks the first double-click and the in-script advice can't print; arch-mismatched Mac zip gives a generic venv error; ~1.5 GB model download opaque; port-8765 collision opens any HTTP responder; no uninstall; `reader_doctor.py` absent from the zip. *Credit:* Setup & Status exemplary; student-surface a11y clean (zero unnamed visible controls); child/adult boundary real; practice mode correctly writes `is_mock=1`. *Adversarial pass dropped 17 candidate findings*; game educator-panel exposure CONFIRMED but downgraded — the game is unreachable from every shipped surface. | 0 issues; 0 PRs (no remote). **10 fixes implemented in-session**: welcome card + permanent ❓; walkthrough relabelled/promoted; guide survives a failed start; gated-nav scroll+focus (deferred past `goStep`); CBM band glosses; `contract v1` + "Coming soon (phase N)" removed from the educator UI; new `docs/START-HERE-EDUCATOR.md`; `build-dist.sh` now ships educator docs; both Getting Started pages rewritten (chip check, Gatekeeper first, honest ~1.5 GB / 10–30 min, recovery, doc link). | **P0 IMPLEMENTATION COMPLETE 2026-08-08 (5 of 6), tests-first** — see `Reader/2026-08-08-p0-implementation-log.md`. Three new pure modules with their own Node suites, matching the repo's existing `line-focus.js`+test pattern because every P0 lived in untestable logic inside a 222 KB browser script: `save-outcome.js` (37 assertions — classifies a save as db/device-only/lost and separates "server unreachable" from "server refused", the conflation behind the false "Saved ✓"), `calibration.js` (33 — whole-word by default with `-ing`/`th-`/`-th-` phonics notation, so the old catastrophic bare-`r` substring now exempts 0 words, and the exemption is announced on the Review screen), `score-guard.js` (21 — refuses to score an empty transcript; `doScore()` returns false and `scoreReadAction()` no longer advances the child onto a fabricated score). **Deliberate-break demonstrated:** reintroducing the old failure-collapse turned 7 assertions red; revert returned green. **Regression caught mid-change:** two feedback call sites treated `serverSave`'s return as a boolean and would have reported success on failure — `#n-export` would additionally have skipped its download fallback; both routed through a new `serverSaveOk()`. P0-5 got an inline explanation plus a confirmation that unticks itself if declined. Full suite green on build `4b36c1a18be3`: 37+33+21+39 node, align SELFTEST PASS, e2e_smoke 21/21, audio-retention 21/21, browser E2E 22/22 (whose first assertion, "No console errors / 404s / missing assets", independently confirms the three new script tags load). `docs/START-HERE-EDUCATOR.md` hedge about the untrustworthy save confirmation removed and replaced with the three now-distinguishable outcomes. **P0-3 DONE** — `app/writer_claim.py` + 37 assertions: each server leaves a claim in `data/.reader-writer.json` (which syncs — that is the point) and reads anyone else's *before* taking it; four states (`self` never warns, including our own crashed server; `conflict` within 15 min names the other computer and says to wait for Dropbox "Up to date"; `stale`; `none`). Surfaced at startup, in `/api/health`, and as a Setup banner; refreshed on every real save. **Locking was deliberately NOT built** (the machines never see the same filesystem at once; a stuck lock on a synced folder strands the adult) and **WAL was deliberately NOT enabled** — the audit's `journal_mode: delete` evidence is correct but the implied fix is wrong, since Dropbox would sync `-wal`/`-shm` sidecars independently of the `.db`. A test asserts no `acquire`/`release`/`lock` API exists so the advisory design cannot drift. A test also caught a real gap: a claim with a host but no usable timestamp fell through to `stale` ("a while ago") without evidence — now `none`. **P1 IMPLEMENTATION DONE 2026-08-09 (16 of 18)** — see `Reader/2026-08-08-p1-implementation-log.md`, grouped by educator experience: (1) stranding messages — literal `http://localhost:<port>` replaced by the real origin, `humanizeAiError` now reached from all 6 AI-failure sites via `aiFailureText()`, server `no_sdk` hint no longer offers a `pip install` into an unreachable venv, "Clipboard blocked — see console" replaced, `NotReadableError` case added; (2) recording feedback — the elapsed timer was shipped `hidden` and never revealed (now shown while recording), `mediaRecorder.onerror` added (there was none), transcription got elapsed seconds + a cancel button + a 5-min AbortController ceiling with distinct timeout/cancel/failure messages, and a quiet "↩ Back to setup (grown-up)" exit from the otherwise inescapable student stage; (3) child-facing copy — `body.comp-student .teacher-only` hides adult-voiced text, "Why was this hard?" rewritten to address the child, M·S·V key printed in the table header instead of hover-only `title=`, raw miscue slugs → plain English with "— not an error" on the four non-counting categories (slug preserved as option `value`); (4) settings/identity — line guide now remembered per reader and restored by `resetLineFocusSession()` (it used to switch off every Launch), typography persisted, 10 duplicate profiles moved into a labelled `<optgroup>` (`none_lost: true`), "alias" → "What to call this reader"/"Your name"; (5) install — `launch.sh` now verifies `/api/health` before treating a port responder as Reader and refuses with a `READER_PORT=` escape (verified against a real foreign server: exit 1), Mac stop helper only kills processes running `server.py`, Windows installer pauses on success and reports a failed launch, **new `Uninstall Reader.{command,bat}`** (types `remove` to confirm, keeps saved sessions and says so), and `reader_doctor.py` + `docs/` now ship. **Full `mac arm64` distribution rebuilt (187 MB, runtime SHA-256 verified) and the zip inspected**: `docs/START-HERE-EDUCATOR.md` ✓, `tools/reader_doctor.py` ✓, `Uninstall Reader.command` ✓, GettingStarted links the guide + chip check + "1.5 GB" + uninstall ✓. **Final suite: 231 assertions, 0 failures** (save-outcome 37, calibration 33, score-guard 21, line-focus 39, align SELFTEST, writer-claim 37, e2e_smoke 21, audio-retention 21, browser E2E 22). **P1-13 DONE 2026-08-09** — `app/question-import.js` + 51 assertions. The old path was `prompt('Paste a JSON array of items: [{"stem":…}]')` → bare `JSON.parse` → `alert('Could not parse JSON: Unexpected token o in JSON at position 1')`, shown to a reading specialist following our own instruction to copy a chat reply — and the prompt closing **discarded her paste**. Replaced with a real panel (textarea, live validation, preview of what was found, per-item notes, Add disabled until something is usable, paste never discarded). The parser accepts what assistants actually return: ``` fences, prose preamble/sign-off, a single object, a `{questions:[…]}` wrapper, a plain list of strings, alternate stem keys (`question`/`q`/`prompt`/`text`), and string options. Failures are per item so one bad entry never sinks the set; unknown type/skill tags warn but still import (compItem already coerces them). Fatal messages carry zero parser jargon — a truncated paste gets "that usually means only part of the reply was copied". The in-app generation path was routed through the same parser so the two cannot disagree. Renaming the button surfaced a **documentation bug**: "Paste JSON set" appeared in 7 places including `docs/USING-CLAUDE.md`, `docs/EDUCATOR-TASKS.md`, `docs/reader-docs.md` — docs that now SHIP in the distribution, so a stale name would have actively misdirected the recipient; all updated, including a line claiming the button "rejects" a wrong format, which is no longer true. **Final suite: 282 assertions, 0 failures.** **P1-15 (macOS Gatekeeper / Apple Developer ID) — DECIDED AGAINST and closed by the owner 2026-08-09.** Not a backlog item; mitigated in Getting Started. Do not re-suggest buying a certificate. Remaining: the P2 list. Method debts to carry: (a) the tree was edited mid-fan-out, so raw finder line numbers for `app.js` after ~810 are shifted ~+40 — re-anchor by content; (b) dimension 5–7 report is UNVERIFIED (verifier hit session limit) and its items are held at P2; (c) fix the gemini offload model pin before the next audit. One mock profile (`Audit Demo`, `is_mock=1`) left in `data/reader.db`. **=== ROUND 2 (2026-08-09) — re-audit + build ===** *Method:* Workflow (5 path-scoped read-only finders → adversarial verifiers, **10/10 agents completed**; 108 findings CONFIRMED / 25 REFUTED) + Orchestrator offloads (gemini **working again** after the owner fixed the model pin flagged in round 1; cursor). Artifacts `Reader/2026-08-09-*`; build tracker https://claude.ai/code/artifact/91bdd919-3b6b-4712-84c0-15ada13c7762 . *Verdict:* **round 1's own work was the largest source of incomplete fixes** — P0-4's score guard sat on the fallback path not the installed-machine path (round 1 had verified by forcing the branch it had just edited); the manual-transcript fallback the app recommends was unreachable (`#readAdult` hidden whenever `#read` shows); the guided run could reach 'Finish ✓' with nothing saved; and round 1's own `docs/START-HERE-EDUCATOR.md` gave a **false privacy assurance** ('nothing leaves this computer') while browser live-transcription can send a child's audio to the browser provider — the app's consent banner was honest, the doc was not. All fixed and re-verified from the educator's starting conditions. *Owner's specific question — the 12-step guide:* **vestigial with a load-bearing entry point.** Only `label` and `id` of four declared properties were ever read; 5 of 12 steps re-showed a screen; 12 steps mapped to 6 real screens; one step's text claimed an AI had scored when no AI call ran; no shipped doc mentioned it — yet round 1 had promoted it to the primary first-run call-to-action. **RETIRED (H4a)**: 163 lines of runner deleted plus the `#steprunner` bar, the Dashboard workflow editor, the orphaned `#stepcard`, the dead SUBNAV entry and ~1.4 KB of CSS; replaced by a 3-step first-session helper that lights up from **real state** (reader named / passage present / read happened), so it structurally cannot claim a step occurred that did not. *Owner decisions:* proposals presented in a decision-actionable artifact; **9 approved** (H1, H3, H2, F1, F4, F5, F2, F3, H4a) with one modification — F5 split so the game is **developed and integrated**, not parked — plus two non-proposals (rebuild the distribution, fix the shipped docs). *Built, all verified live:* **H1** `help-content.js` (55) 7 per-screen entries, its test reading the real routable sections out of `index.html`+`SUBNAV` so a new screen without help fails the suite; **H1b** `glossary.js` (74) — owner correction, a **?** beside 12 individual terms, click-never-hover (the audit had counted how much self-explanation was trapped in `title=`), with the test enforcing markup↔glossary in **both** directions, which caught 6 orphaned definitions; **H3** `examiner-copy.js` (42) printed examiner copy with deterministic line layout and cumulative margin counts (browser wrapping cannot be known before print, and a mismatched margin count makes the score wrong); **H2** `guides/` — 5 real HTML pages + a deliberately narrow `/guide/` route; **F1** `norms.js` (52) Hasbrouck & Tindal 2017 TR#1702 Table 4 transcribed **from the primary report**, defended by the report's own prose claims about its own cells; **F2** `wcpm-chart.js` (38) inline SVG that states the `adapt.js` difficulty confound rather than hiding it, no red zone and no risk language; **F3** `family-page.js` (49) which **refuses to claim a trend from <3 sessions** and refuses to call rising numbers improvement when the passages got easier; **F4** explicit ▶/✗ mode switch so the adult can mark a miscue Reader missed; **F5a** `implementation/` → `archive/implementation/`; **F5b** `game-bridge.js` (33) — reward keyed to **showing up, not performing** (a strong and a struggling session earn the same tier), idempotent by construction, practice and calibration earn nothing, plus a grown-up gate on `#eduBtn` which was a standalone safety fix (it switched to educator mode with no gate at all, exposing fields the game's own markup labels 'never shown to child'). *Two deliberate deviations from the approved text, both flagged:* F4's added miscue **counts by default** (a mark that changes nothing reads as broken; the guard is visibility instead), and F1 **omits** the widely-quoted '10 words below the 50th percentile' intervention threshold because it **is not in TR#1702**. *Bugs caught by the new tests:* a timezone trap (`new Date('2026-12-01')` parses UTC while `getMonth()` reads local, landing a December date in autumn west of UTC); `Number(null) === 0` making a missing score compare as a genuine reading of zero, in three modules; a `<label>` structure that made clicking `<summary>` toggle a checkbox; a Windows-installer `errorlevel` check I had moved so it guarded an *optional* copy instead of a required one; and **a vacuous assertion in my own game-bridge suite** — `applyRewardEvent()` returns `no_profile` *before* validating, so a good and a bad event returned the same thing until a profile was supplied. *Guides wiring bug found only by driving it:* all five pages 404'd because `launch.sh` mirrors the app into Application Support so `GUIDES_DIR` resolved beside the mirror — fixed via `READER_GUIDES_DIR`; testing only the traversal refusals would have 'passed' while nothing worked. *Distribution rebuild exposed a real build-process defect:* building into `dist/` on the Dropbox-synced volume let the sync daemon race the build and write **150 'conflicted copy' files into the payload**, reaching 55 MB of an expected 187 MB after 41 minutes; the existing `com.dropbox.ignored` guard was set but is applied **after** `mkdir`, too late. `build-dist.sh` now resolves a `BUILD_ROOT` that defaults off-volume when it detects a cloud-sync path, exposes `--build-root`, moves only the finished zip back, and **fails the build** rather than packaging conflicted copies. Both artifacts rebuilt and verified by reading the zips: `Reader-mac-arm64.zip` (158 MB / 2,578 entries) and `Reader-update.zip` (582 KB / 132 entries) — every new module present, `implementation/` absent, the 12-step runner gone from the shipped `app.js`, the grown-up gate present in the shipped `game.js`, zero conflicted copies. **Final suite: 883 assertions, 0 failures** (531 Reader node incl. line-focus, 251 game, 79 python, 22 browser E2E, align SELFTEST PASS) — round 2 added **343** across 7 new tested modules. *Method debt carried forward:* a read-only analyst edited application code during the fan-out (`save-outcome.test.js`, 37→44 assertions — the change was reviewed and is beneficial, and the weak assertion it replaced could not tell a durable save from total loss, but the constraint should be re-asserted and diff-scanned next round). *Still open:* the P2 list, and the rest of the F5b game roadmap (3.5–5.5 days, `2026-08-09-07-game-integration-plan.md`). Still no CI, because still no git remote. **=== POST-ROUND FIX (2026-08-09): the in-app AI path ===** Raised by the owner after the round closed ("a colleague is going to try to connect through it"). `server.py` prefers the local `claude` CLI and falls back to the `anthropic` SDK with a pasted API key; **only the author's machine has the CLI**, so for every recipient the SDK is not a fallback but the ONLY in-app path — and it shipped nowhere: absent from every `requirements-*.txt`, from every build step, from both installers and from the venv, so the `import anthropic` inside `_llm_via_sdk()` had **never once executed on any machine**. `_llm_probe_ping()` called it outside any `try`, so the ImportError stringified to "No module named 'anthropic'" and fell through `_friendly_llm_error`'s unknown branch to **"Check the Claude login or API key and try again"** — a reading specialist would paste a valid key and be sent to fix the one thing that was fine. `/api/generate` DID carry a correct `no_sdk` message, but the readiness gate returned first, so it was unreachable on the only path that needed it — **the round-2 pattern again: a good fix on a code path the real user never takes.** *Fixed tests-first* — `test/test_ai_readiness.py` (**76 assertions**) written before the change, reproduced it 9-red. Shipped: `requirements-ai.txt` (`anthropic==0.121.0`) validated/copied/vendored by the build, installed by both installers offline-first with online fallback and **never aborting an install**; 16 wheels verified to resolve for BOTH mac arm64 and win amd64; `_classify_llm_error()`/`_classify_cli_error()` giving `no_sdk`/`bad_key`/`unknown_model`/`cli_signed_out`/`offline`/`busy`, each with one cause and one next step and no terminal, package or status-code jargon; the bare SDK call wrapped so raw Python can no longer reach an educator; `/api/health` now emits `llmErrorText` because **the browser kept its own copy of the map and the two drifted the moment the server learned new causes** (client now prefers server prose, test enforces both directions); `reader_doctor.py` prints the server's sentence instead of advising every remedy at once; the stale `claude-opus-4-8` default (exclusive to the never-run SDK path) → `claude-opus-5`; `thinking={'type':'adaptive'}` — also never confirmed against a live API — now retries once without it, with a test proving a genuine auth failure is NOT swallowed; **the updaters had no pip step at all** so an existing install could never gain the SDK, both now carry and install `requirements-ai.txt` quietly; and `guides/troubleshooting.html` gained an AI section quoting Reader's exact sentences, test-pinned against drift. *Not verifiable here, stated plainly:* the `claude` CLI on this machine is genuinely signed out (confirmed against its on-disk login with the session env stripped, so not a launch artefact) — re-authenticating is a browser OAuth flow and a live SDK test needs a real key; both are the owner's to do. Everything up to the credential is proven, incl. the request reaching the API and being rejected only on the credential. *Two self-inflicted errors caught:* the build was started before a guide edit landed (violating this log's own "build last" rule — rebuilt), and the first health change left the browser's stale copy of the map in place. Both zips rebuilt and verified by reading them: `Reader-mac-arm64.zip` 191 MB / 2,588 entries incl. all 16 AI wheels, `Reader-update.zip` 576 KB. **Final suite: 963 assertions, 0 failures.** *Owner caught a false claim in my own report and in the shipped message:* I wrote "your Claude sign-in has expired" — he replied "if my Claude login is expired, how am I working in Claude?" and was right. Two installs exist (standalone `~/.local/bin/claude` 2.1.177 on PATH vs desktop 2.1.221) but that is NOT the mechanism, since both fail identically when spawned fresh. The real distinction is **live session context vs stored credential**: his Claude session is a running process with host-refreshed auth (`CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH`), while Reader spawns a NEW `claude -p` that reads the revoked stored credential. Message rewritten to name the command-line tool and state the app is separate; 4 assertions pin it, incl. one forbidding the old sentence. Same defect class as everything else this round — I verified the 401 and stopped, instead of asking what it was evidence OF. **Owner then rejected the corrected fix, also correctly:** "you're preparing this for a non-technical person; doing anything in terminal shuts down their use of the app... the user will have the Claude Desktop app open and logged in." The message was now ACCURATE but still unusable — a true instruction the reader cannot follow strands them as effectively as a false one. Three changes: (1) **`claude_desktop_bin()`** — the desktop app bundles a full `claude` executable in its own support folder (`~/Library/Application Support/Claude/claude-code/<ver>/claude.app/Contents/MacOS/claude`, plus `%APPDATA%`/`~/.config` variants) that `shutil.which` never saw, so Reader reported "no Claude" on a machine with Claude open on screen; version dirs globbed and sorted NUMERICALLY (a plain sort ranks 2.1.9 above 2.1.221) since the path changes every desktop update. (2) **`claude_candidates()`** — override → PATH → desktop, deduped, and the probe walks the whole list, because this machine has both and the stale one was hiding the good one; tested with a failing first and working second candidate. (3) **The always-works path is now presented as a method, not a consolation prize** — Setup offered only a detectable login or a billed API key, while copy-and-paste (needs nothing, works with the desktop app already open) appeared nowhere and was mentioned only after a failure; now Option 1 = the Claude app, Option 2 = copy-and-paste tagged ALWAYS WORKS, Option 3 = API key folded into a `<details>` and described honestly as a separate paid account. Every message now ends at a mouse action, and **a test scans all educator-visible AI messages for terminal-speak** (terminal/command line/PowerShell/pip install/sudo/claude login/venv/environment variable) and fails on any hit — the constraint is enforced, not remembered. *Still unverifiable here:* whether a signed-in desktop app authenticates a SPAWNED `claude -p`; every credential on this machine is revoked. If it does not, nothing is lost — Option 2 needs no sign-in, which is why it was promoted. **Owner's third correction — "my colleague has a PC" — surfaced something larger:** there was NO WINDOWS DISTRIBUTION AT ALL. Every zip across both rounds was mac-arm64; the `--os win` target, the Windows installer/uninstaller/launcher/GettingStarted all existed and carried every round-2 fix, but had never been packaged — the colleague had nothing to install, and nobody noticed because every verification step inspected a Mac zip and reported it complete. Also, the just-written discovery was Mac-shaped: it searched only `claude.app/Contents/MacOS/claude`, `claude.exe`, `claude` while **this repo's own `docs/SETUP-PC.md` documents `%APPDATA%\npm\claude.cmd`** and `server.py`'s own `llm_generate()` comments that Windows uses a `.cmd` shim — two places in the repo knew and the new code did not. Fixed: `.cmd`/`.bat`/`.exe` leaves; roots for `%LOCALAPPDATA%\AnthropicClaude`, `%LOCALAPPDATA%\Programs\Claude`, `%APPDATA%\Claude\claude-code`, `%PROGRAMFILES%\Claude`, the evidenced `%APPDATA%\npm`, and Linux; executables found both directly in a folder (npm shim) and under a version dir (desktop app); and **`os.access(X_OK)` is meaningless on Windows** (true for any existing file) so the check is now platform-aware and the non-executable test is skipped there. Windows layouts exercised as data since none can run from a Mac. Windows paths are INFERRED not verified, so `/api/health` now reports `llmFound`/`llmCandidates` and `reader_doctor.py` prints them (paths only; a test asserts no credential travels with them). Building it exposed a third defect: the Windows build died twice on pip `ReadTimeoutError` — the default 15s socket timeout is too short for ~28 MB wheels, aborting the whole build after minutes of successful downloading — so `build-dist.sh` now exports `PIP_TIMEOUT=180`/`PIP_RETRIES=10`; it did correctly fail loudly rather than ship a partial zip. **`Reader-win-amd64.zip` now exists: 279 MB, 3,884 entries**, verified by reading the zip (Windows installer/uninstaller/launcher, MSVC runtime, win_amd64 wheels incl. the Anthropic SDK, requirements-ai.txt, guides, educator docs, reader_doctor, .cmd-aware discovery, copy-and-paste Option 2, zero conflicted copies). *Own-test bug caught by its own output:* the Windows-shape loop assigned `f = os.path.join(...)`, shadowing the failure counter, so the summary printed "122 passed, /var/.../claude.cmd failed" — nothing had failed, but the next real failure would have raised TypeError instead of reporting itself. |
| `Reader` | Completed; ordered backlog implemented locally; colleague use conditionally ready | 2026-07-16 | 2026-07-16 | Codex repo-audit + Orchestrator isolated Cursor/Gemini reads; Claude selected but live probe returned revoked-token 401; full local browser/server suites | `Reader/2026-07-16-AUDIT_REPORT.md` + `Reader/2026-07-16-backlog-implementation-log.md` | RDR-01–RDR-12 implemented locally: correct unread-tail WCPM, honest LLM health, identity/mic/a11y, reproducible dependency/CI definitions, canonical SQLite JSON v2, consented linked audio, offline drafts, adult attribution, one-question child comprehension, reconciled docs. Optional line guide expanded to selectable 1–6-line windows with use/config telemetry. Colleague core use is conditional; simultaneous Dropbox SQLite writers unsupported. | 0 issues; 0 PRs; no Git repository/remote | Owner chooses a Git remote to activate CI; use serialized Dropbox writer handoff; reauthenticate Claude if in-app generation is wanted; run real-browser mic spot check on colleague machine. |
| `trip-planner` | Completed; report/backlog only | 2026-07-10 | 2026-07-10 | Codex repo-audit + bounded Orchestrator candidate lanes; fresh remote-tip clone `540d549`; full Python/frontend/build/live-TPP evidence; observed local browser flow | `trip-planner/2026-07-10-AUDIT_REPORT.md` (+ verification log, repo map, canary proposal, two raw candidate reports) | P1 investigation: budget form remote-state reinitialization has hosted-CI evidence. P2: raw TPP exception disclosure; duplicate fixture/persisted lookup; inconsistent duplicated empty-candidate confidence. Maintainability: 2,600-line WorkspacePage, 4,000-line workspace service, four complex ingestion functions. Full local suite green. Existing two-trip harness works but scenarios/semantic assertions are generic. | 0 issues; 0 PRs; issue-ready acceptance criteria in report | Discuss and approve deterministic two-trip canary; then implement. Canonical Dropbox sync still awaits offline materialization. |
| `Travel-Plan-Permission` | Completed; report/backlog only | 2026-07-10 | 2026-07-10 | Codex repo-audit + bounded Orchestrator candidate lane; fresh remote-tip clone `1e0cecc`; full locked suite, built-wheel install, concurrency/numeric reproductions, dual-repo live exercise | `Travel-Plan-Permission/2026-07-10-AUDIT_REPORT.md` (+ verification log, repo map, raw candidate report) | P1: shared singleton store fails concurrent writes; installed wheel omits default policy/validation configs; NaN/Infinity/negative policy inputs can pass. P2: large HTTP/policy/auth module boundaries. Full local suite green; hosted reusable CI is red upstream on duplicate coverage pins. | 0 issues; 0 PRs; issue-ready acceptance criteria in report | Fix concurrency first, then package resources/numeric bounds. Canonical Dropbox sync still awaits offline materialization. |
| `Workflows` | Completed; implementation-ready backlog, no filing | 2026-07-10 | 2026-07-10 | Codex repo-audit + Orchestrator read-only offloads (Gemini/Vibe completed; Codex/Cursor capacity failures rerouted to scoped collaboration reviewers); fresh `/tmp` clone at `dcefc3c`; live GitHub/ruleset/check evidence | `Workflows/2026-07-10-AUDIT_REPORT.md` (+ verification log, non-actionable log, repo map, five analytical artifacts) | P0: four semantic issue workflows unwired by checkout closure; consumer sync/drift/hash/validation resolve different source graphs, leaving current fleet gaps self-unrecoverable. P1: live ruleset/config/docs/health checks disagree and Health 44 false-greens; PyPI updater cannot push workflow-path changes; delivered eligibility action is stale; runner debounce fails open on dual-store 403. P2: PDF finite-value/raw-fallback contract. Full suite 4,030 pass with only two updater-freshness failures. | 0 issues; 0 PRs; 0 production source changes; seven AGENT_ISSUE_FORMAT-ready finding bodies in report | Implement WF-01 and WF-02 first, then branch governance/updater/action/debounce; keep PDF hardening before package adoption |
| `Orchestrator` | Completed; full implementation reconciled | 2026-07-09 | 2026-07-09 | Codex GPT-5.6 Sol/Terra/Luna requested lanes; repo-audit + Orchestrator; Workflows `origin/main` Keepalive verification; primary-source field review | `Orchestrator/2026-07-09-AUDIT_REPORT.md` (+ verification log, ten analytical/model artifacts, UX review, 23 issue bodies) | P0: duplicate/mislabeled research subjects and production starvation; evaluator model contamination of worker identity; non-causal experiment/strategy arm identity; maturity without activation proof. P1: runtime/range/role/synthesis/completion/evidence/adversarial/cadence/report open loops. Expansion: execution profiles/shared pools/hierarchical learning; pattern-to-capability compiler; neutral Workflows bundle and backplane reference producer. Production outcomes healthy at 99.9%. | 23 canonical GitHub-ready bodies, including one non-assignable epic and bounded children; none filed; 0 PRs; no production source changes | Audit implementation closed 2026-07-10; review outcomes after seven cadence runs or twenty accepted completion episodes |
| `Workflows` | Completed and reconciled | 2026-06-11 | 2026-06-14 | Claude/Orchestrator whole-system audit; root report and verification log | `Workflows/2026-06-11-summary.md` | P0 workflow syntax/destructive close-tracker/coverage defects; P1 keepalive, delegation, LangSmith, docs, and local-lane issues; large economy refactors separated from correctness fixes | Many Workflows issues/PRs, including #2263-#2367; all prioritized findings resolved, declined, or deferred by 2026-06-14 per verification log | Keep as baseline continuity record for any future Workflows audit |
| `Trend_Model_Project` | Completed | 2026-06-01 | 2026-06-02 | Claude Opus 4.8 repo audit on branch `phase-3`; repo audit report and Claude memory | `Trend_Model_Project/2026-06-01-summary.md` | Core arithmetic sound; dominant defect class was config contract drift; documented config keys inert or routed through divergent paths; UI and public-field opportunities identified | 53 drafted issues; 51 filed on Trend #5389-#5439 and 2 upstream Workflows issues #2228/#2229 per audit memory | Reconcile issue closure state only when a new audit or follow-up asks for it |
| `Portable-Alpha-Extension-Model` | Completed, source artifact gap noted | 2026-06-13 | 2026-06-13 | Claude project memory; original `docs/reports/repo-audit-2026-06-13/REPORT.md` path not found in current checkout | `Portable-Alpha-Extension-Model/2026-06-13-summary.md` | Core engine sound; financing broadcast and sweep regime-switching risk defaults understate risk; Scenario Wizard first-load crash; Scenario schema not wired into simulation; overlay `Total` convention undocumented; no fee/cost layer | About 20 issue drafts existed per Claude memory, but original draft artifact was not found during normalization | Recover original report/draft artifacts from archive or JSONL before using as issue source |
| `Counter_Risk` | Completed | before 2026-06-20 | before 2026-06-20 | Repo audit report at `Counter_Risk/docs/audit/AUDIT_REPORT.md` | `Counter_Risk/2026-audit-summary.md` | Clean typed pipeline and broad tests; not ready for no-install Windows operator flow; wrong-number/wrong-outcome defects in HHI/Top-N, percent-of-total, severity halt behavior, and frozen-exe path resolution | No generated issue/PR list found in the source report during normalization | Reconcile GitHub issue state before filing follow-ups |
| `learning-management-system` | Completed; Track D refill audit + filing | 2026-09-06 | 2026-09-06 | Gemini repo-audit skill; fresh clone @ `fd0ea51`; adversarial verify on live tip | `learning-management-system/2026-09-06-audit-run.md` (+ verification log, 9 issue bodies); OUT `artifacts/audits/learning-management-system-2026-09-06.md` | Multi-tenant ownership enforcement across learners, competencies, cases, and LLM routes; Setext heading description corruption; LLM replay mode provider routing; cleartext password hashes in JSONL export; NaN score rating over-allocation in FSRS; cross-learner leaks in support admin dashboard | Filed [#602](https://github.com/stranske/learning-management-system/issues/602)-[#610](https://github.com/stranske/learning-management-system/issues/610) (4×P1, 5×P2) | Verify format-guard pass on all nine issues; implement P1 ownership sweep |
| `learning-management-system` | Completed; Track D refill audit + filing | 2026-09-05 | 2026-09-05 | Cursor repo-audit skill; fresh clone @ `b0df3a1`; adversarial verify on live tip | `learning-management-system/2026-09-05-audit-run.md` (+ verification log, 8 issue bodies); OUT `artifacts/audits/learning-management-system-2026-09-05.md` | Residual ownership gaps after PR #578 (mastery, inspect, rubric-score, capability); NaN score propagation; rubric scheduler non-atomicity; public OpenAPI under auth | Filed [#584](https://github.com/stranske/learning-management-system/issues/584)-[#591](https://github.com/stranske/learning-management-system/issues/591) (4×P1, 4×P2) | Verify format-guard pass on all eight issues; implement P1 ownership sweep first |
| `Travel-Plan-Permission` | Completed as combined TPP/trip-planner audit | 2026-06-02 | 2026-06-02 | Archived Claude combo audit packet under `Code Archive/code-root-loose-20260605T0833Z/audit-tripplanner-tpp/` | `Travel-Plan-Permission/2026-06-02-trip-planner-tpp-summary.md` | Strong dual-repo system; hotspots and duplication in TPP app factory/UI and trip-planner workspace/planner paths; missing commerciality lever; UX overload; product opportunity findings | Audit packet includes issue drafts; later weekly review produced TPP #1223, but it is tracked separately from the full-audit packet | Use the combined summary as canonical record for this cross-repo audit |
| `trip-planner` | Completed as combined TPP/trip-planner audit | 2026-06-02 | 2026-06-02 | Same archived Claude combo audit packet as TPP | `trip-planner/2026-06-02-trip-planner-tpp-summary.md` | Same combined audit; trip-planner-specific findings include planning/workspace hotspots, ingestion/ranking duplication, source-mix opportunities, daily-menu design, and cross-repo smoke concerns | Audit packet includes issue drafts; later weekly review produced trip-planner #1417 and local draft `19-followup-1312-get-workspace-payload.md` | Keep repo-local summary aligned with the canonical combined TPP/trip-planner record |
| `Inv-Man-Intake` | Completed and reconciled | 2026-06-28 | 2026-06-28 | Claude (Opus 4.8) full repo-audit skill run + Orchestrator offloads (gemini wiring, codex correctness, cursor duplication, claude web-research); verified on off-Dropbox clone w/ CI-pinned tools | `Inv-Man-Intake/2026-06-28-AUDIT_REPORT.md` (+ `-04-verified-findings`, per-dim `-01/-02/-03/-05`, `-verification-log`, `-ROUTE_WEIGHT_CANDIDATES`) | **CI-red main** (black on 2 test files); **NaN BLOCKER** in scoring engine (executed); credit-only scoring crashes for 7/8 asset classes (executed; partial #592); threshold fallback drift; non-finite perf/conflict/threshold-config gaps; dup extracted-field overwrite; non-atomic intake collision. Impl-verification: 9/11 prior #592-602 are genuine fixes. Dims 5-7: peer-group scoring, HITL calibration, lineage packet, Docling. Local tests 690 pass/91.75% | Filed #691-#699; **#691-#698 IMPLEMENTED + MERGED same session** (PRs #700/#702/#705/#704/#706/#707/#708/#709) + process fix #703 (pr-00-gate format_check). main 7935f76(red)→931564d(green); 704 tests pass/91.78%. Epic #699 OPEN with children #710-#713 FILED (peer-group/HITL/lineage/Docling) | Done: #691-#698 merged; #699 children filed. Upstream re-sync = N/A (verified pr-00-gate is sync_mode:create_only, repo-owned, overwrite_repos=Template only → #703 is the durable fix). Remaining: implement #710-#713 (roadmap); Stage-2 live gates still open (fixes were Claude-direct, not fleet-worked) |
| `Manager-Database` | Completed and reconciled | 2026-06-28 | 2026-06-28 | Claude (Opus 4.8) full repo-audit skill run + Orchestrator offloads (codex correctness, gemini duplication, cursor sync-drift, cursor config/migrations, claude web-research); full local run incl. UI on off-Dropbox clone @ `e5764a5` w/ lock-pinned `streamlit==1.58.0` | `Manager-Database/2026-06-28-AUDIT_REPORT.md` (+ `-UX_REVIEW`, per-dim `-01..-05`) | **P0 Streamlit operator UI crashes on load** (`ui/app.py:15` `url_path=""` missing `default=True`; AppTest+browser confirmed; mocked test blind); **P0 EDGAR nightly re-ingests from 1970 → duplicate holdings**; P1 NaN/inf finite-bounds sweep (alerts/activism/conviction/edgar/search), chat limiter bypass via `x-session-id`, `connect_db` psycopg→SQLite silent fallback, ETL `manager_id` vs API SQLite `id`, `seed_managers.py` Postgres-only; P2 dialect-helper dup (~210 LOC), `.env.example` 6/80 vars, schema.sql↔alembic parity gap. Dims5-7: edgartools/OpenFIGI/pgvector/ragas, bitemporal holdings, 13F amendment reconciliation. API itself healthy/well-wired. Sync boundary: `tools/llm_registry.py` unmanifested fork (fix UPSTREAM in Workflows) | Filed #1297-#1303 (2×P0, 5×P1) with `agent:codex`+`status: ready` to feed lanes. Deduped against codex auto-pilot batch #1273/#1275/#1281/#1282/#1283/#1280 (not refiled) | Capture Stage-2 keepalive evidence as #1297-#1303 produce post-escalation PRs (scheduled check-in); verify fixes land via implementation-verification |
| `Pension-Data` | Completed (audit + filing) | 2026-06-28 | 2026-06-28 | Claude (Opus 4.8) full repo-audit skill run + Orchestrator offloads (gemini wiring/inert-config/DB-parity, codex correctness/finite-bounds, cursor duplication, claude web-research, `ux_review.py` panel for dim4); full local suite on off-Dropbox clone @ `493f5ea` w/ CI-pinned tools (840 tests pass/3 skip) | `Pension-Data/2026-06-28-AUDIT_REPORT.md` (+ `-UX_REVIEW`, `-verification-log`, per-dim `-01/-02/-03/-05`, `-assets/`) | **P0 main CI-red** since 2026-06-25 (black on `tests/web/test_no_external_cdn.py`; `pr-00-gate.yml:72 format_check:false` ≠ `ci.yml` black → recurs; Inv-Man-Intake #703 class); **P0 finite/bounds systemic** — NaN/±inf defeat `<0/>1` guards at 17 sites; verified NaN confidence→`1.0`→`auto_accept` on prod pipeline (`confidence.py:43`←`document_orchestration:1266`); P1 last-mile-wiring + README overclaim (API serves fixtures in proprietary mode, extraction never loaded to DB staging, `persist_staging_core_metrics` test-only); P1 parser accuracy (number-stealing/locale/hardcoded-column); P1 divergent SQL read-only validators; P1 web-bundle-contract dup (3 ways); P1 UX raw number formatting. P2 lock drift (black 26.3.1 vs 26.5.1), latent Postgres bugs (unmounted SQL route), inert `saved_queries`/`model_registry` config, dup clusters, homogeneous fixtures, root clutter. **Corrected (adversarial):** `staging_consultant_engagements` deliberately-retained (PR#339 test) → NOT dead; SQL-dialect & `validate_parser_outputs` BLOCKERs → unreachable/latent; red-main NOT version skew. Library mature; dims5-7 = bitemporal/entity-res+Form5500/peer-benchmark/Docling/eval-harness. Synced scope (langchain/tools/.github) excluded, no drift to fix locally | Filed **#635-#642** (AGENT_ISSUE_FORMAT, `agent:codex`+priority; `agents:auto-pilot` on #635 only to seed one safe keepalive datapoint — others ready for promotion). #635 red-main(P0)+gate, #636 finite/bounds(P0), #637 parser-accuracy(P1), #638 SQL-validator-dup(P1), #639 bundle-contract(P1), #640 UX(P1), #641 hygiene/consolidation(P2), #642 Epic dims5-7. Dedup: only 2 open issues (#542/#343, non-code); closed-issue arc (#394/#478/#479/#483/#341) showed fixture/overclaim is INTENTIONAL → F6 dropped | Verify fixes land (implementation-verification) starting with #635/#636; capture Stage-2 keepalive disagreement/role-outcome evidence as #635-#641 produce post-escalation PRs (advisory-only, no apply path). **Round 2 (2026-06-28, expansion dev):** 4 research agents R1-R4 + `2026-06-28-ANALYTICS_DESIGN.md` (+docx) — benchmarking/holdings analytics for a specific US public pension. Grounded that repo ALREADY has funding_trend/allocation_peer_compare/holdings_overlap primitives (fixture-fed). Filed #645-#650 decomposing epic #642 (A PPD ingest, B metrics+peer-stats+9-dim scorecard, C holdings collection 13F/CAFR/AB2833, D holdings analytics, E bitemporal, F Docling). Keystone=Public Plans Database (free API); holdings=plan-own-file+13F (CAFR-anchored, equity-sleeve caveat). **Round 3 (build):** PR #653 (peer_stats + 9-dim health scorecard; gate green; marked ready). **#635 RESOLVED end-to-end:** auto-pilot PR #644 was hollow (ledger-only → main stayed red) — caught it, made the real fix in PR #654 (black-format file + pr-00-gate `format_check:true`), merged to main `af24afd`; **ci.yml `lint-format` now SUCCESS, main no longer red**; #635 closed. Defects #636-#640 + #645 promoted to `agents:auto-pilot` |
| `Fine-Art-Archive` | Completed (audit + filing + Track-B waves 1-5 all merged/verified; wave driver DISABLED 2026-07-11) | 2026-06-28 | 2026-06-28 | Claude (Opus 4.8) full repo-audit skill run + Orchestrator offloads (gemini numeric/correctness + Half-B workspace, cursor quality/dup/inert-config, codex Companion API, claude web-research dims5-7); full local suite + driven Companion App on FRESH clone @ `51a09a6` (Dropbox HEAD `1a72d5a` was STALE). Audited BOTH the repo AND the local `Dropbox/Pictures/Claude Project/` workspace (not on GitHub) | `Fine-Art-Archive/2026-06-28-AUDIT_REPORT.md` (+ per-dim `-10..-14`, `-20-local-workspace`, `audit-out/codex-companion-api.md`, `-issue-bodies/`) | **Dominant class = an entire subsystem with NO production effect**: source-quality scoring (~472 LOC) never wired — `acquisition_flow.py:166` always passes `aggregates={}` → all sources get the same tier-1 prior → `select_source`=first candidate; 4/4 config surfaces inert (source_quality/host_registry/sources_seed/known_works); aggregator only WRITES the YAML, nothing reads it (workspace OR repo). Companion App: **work_id path containment** (write-capable traversal via subject_action), **hardcoded `ART_WORKS_ROOT` absolute path**, **process-lifetime ratings+manifest caches** (stale UI, multi-worker broken; observed live), **/ratings/summary blind to two-axis scheme** (observed), weak rating validation (neg dwell persisted, NaN-writable), non-atomic sidecar RMW, corrupt-log silently dropped, unguarded json.loads aborts batch, observed blank "load failed:404" on manifest↔sidecar drift, htmx from CDN. **Half-B (local workspace):** `src/` FORKED from repo (3 modules missing, 24 differ, no canonical rule) + 82 ops scripts + orphaned launchd driver never migrated; blocked hash pass (Dropbox FUSE), 49 renames (16 unresolved), 7 collisions; design contracts: verify 2/5 layers (openly staged), quality 8/12 factors, fallback_chain unused. **REFUTED on verification (NOT filed):** FFT-NaN gate (guarded division + finite uint8 input), Floyd-Steinberg "runaway" (textbook FS). Dims5-7: replace pHash-vs-reference verify with DINOv2/CLIP embeddings + color check (pHash luminance-only can't catch color-wrong repro), decompose "Q factor" into DPI-gate/BRISQUE-NIQE/SSIM, gamut-map before dither (Pillow ImageCms), emit IIIF manifests + DC/Linked-Art + dual-resolve Wikidata/Getty + BagIt fixity. Suite green (211 pass/9 skip); CI push-only standard | Filed **#174-#182** (9 issues, AGENT_ISSUE_FORMAT w/ named test gates) — **triage labels only (bug/enhancement/priority/testing), deliberately NO `agent:codex`/`status:ready`/`agents:auto-pilot`** (user chose file-for-triage to respect the ≤5 opener-PR cap). #174 wiring, #175 path-containment(sec), #176 env-paths, #177 cache-staleness, #178 summary-two-axis, #179 rating-validation, #180 harden-write/audit, #181 guard-meta, #182 UI-graceful+htmx. Dedup: 6 open issues (#114/#80/#36/#21/#22/#23) — no overlap; #21/#22/#23 BLOCKED epics align w/ dims5-7. Prior #98(addressed)/#99 closed | **Backlog executed same session (per Tim's decisions):** P2 cleanups filed individually #183-#192; dims5-7 → roadmap doc `2026-06-28-ROADMAP_dims567.md` + near-term verify-leg issue #193 (embedding identity check); canonical-source rule DOCUMENTED in workspace CLAUDE.md (repo=library canonical, workspace=ops+data, src fork frozen); quarterly device-review scheduled task CREATED (`fine-art-archive-display-landscape-review`, next Aug 1); ops runbook `2026-06-28-OPS_RUNBOOK.md` written + hash pass advanced 1,178→1,964/4,896 (non-destructive) — real blocker is inventory↔FS path drift from renames (re-walk gated), NOT Dropbox placeholders. dims5-7 issues completed #194-#197 (color-mgmt, Q-factor decompose, interop epic, hash-libs). **All 24 issues #174-#197 triage-labeled only, NOT dispatched** (add `agent:codex`+`status:ready` to dispatch; then implementation-verification). **Ops follow-up revealed the Half-B "open loops" are STALE — Phase-3 migration already ran** (`automation_driver.py --status`: step1 "886 relocate"=done, step4 "Phase-3 move→works/"=done): Art/ now has `works/<wid>/master.*` (3,310 masters, **0 sidecars**). So the 49 renames are MOOT (already applied+migrated; Seba woodblock already at works/f45bc6b-...), the flat-path inventory/collision artifacts are stale (snapshotted to `snapshots/2026-06-28-pre-rewalk/`). **Hash pass FINISHED via fresh re-walk: 4,841/4,841 hashed, 0 errors** (`art_inventory_hashed_2026-06-28.csv`); 181 byte-identical dup groups (real dedup worklist, supersedes 7-pair collision_review); 854 files still outside works/. **P2-11 launchd: empirically confirmed TCC blocks the LaunchAgent from CloudStorage** (EPERM on workspace) → reverted to disabled; needs Phase-5 local-data migration or manual runs. Quarterly task created. Real remaining work: write `works/` sidecars (gap; Companion App #182 depends on them), dedup 181 groups, triage 854 stragglers, wire source-quality #174. See `2026-06-28-OPS_RUNBOOK.md`. **WAVE-DRIVE (task `faa-track-b-wave-driver`, 2026-06-29 run 1):** W1 active — #174/#175/#176 each have an OPEN green-gate codex PR (#200/#201/#202), all 3 **implementation-verified PASS** vs the real squash diff (comments posted; no automerge; merge held for Tim); #178 no-PR-yet (<2d, not stuck); #182 PR #198 closed-unmerged by Tim (bootstrap-only — issue still ready → belt re-attempt). W2 not dispatched (gated on W1 fully merged). Progress tracked in `Fine-Art-Archive/README.md`. **(2026-06-30 run 2):** #176 (PR#202) + #178 (PR#203) now MERGED; #174/#175 (PR#200/#201) stay green+verified but **merge-blocked by CodeRabbit `Usage spending cap reached`** (required-check/billing → needs Tim, not a code fix); #182 bootstrap #198 closed, real PR pending (<2d, not stuck); W2 #177/#179/#180/#181 now labeled agent:codex+status:ready (early-in-flight, #180 bootstrap #205 closed); **#193 PR#204 verified PASS this run** (embedding+color verify leg, `tests/test_verify_embeddings.py` green CI). W3 NOT dispatched — wave train stalled on the CodeRabbit cap. **(2026-07-01 run 3):** #175 (PR#201) **RE-VERIFIED PASS** — new commit `fix: contain sidecar master filenames` landed atop the run-1 diff, strengthening it (`_contained_master_filename` guards the sidecar filename fallback + a 4th test); CodeRabbit now SUCCESS on #201 → only Tim's merge remains. #174 (PR#200) unchanged, still verified PASS but CodeRabbit check FAILURE (usage-cap) → Tim. #182 still no real PR (~2d = at capacity-stuck threshold, but it's an issue w/ no PR so PR-based agent:auto delegation can't act — left for belt/Tim, no thrash). W2 early-in-flight (no PRs, <2d). #193 PR#204 unchanged. W3 still NOT dispatched — W1 not fully merged (#174/#175/#182 open). **(2026-07-02 run 4):** CodeRabbit cap cleared → **#174/#175/#176/#178 (W1) + #177 (W2) + #193 (W4) all MERGED** ✅. **#179 (W2) PR#216** OPEN, gate GREEN, CLEAN, **verified PASS this run** (`dwell_seconds ge=0/allow_inf_nan=False`, `quality`/`fit` `strict=True`, log `allow_nan=False`, 9 reject-tests + a `RequestValidationError`/`_json_safe` handler that keeps NaN-echo from turning 422→500); comment posted, no merge/automerge. **Wave-train blockers = #182 (W1), #180, #181 (W2)** — each has only a closed *bootstrap* PR (keepalive OFF + REVIEW_NEEDED, nobody ran `@codex start` → closed, no real impl PR); #182 ~3d out. PR-based agent:auto can't act (no open PR). **Needs Tim** (drive `@codex start` / alt agent / hand-impl). W3 still NOT dispatched — gated on W1+W2. No thrash. **(2026-07-03 run 5):** Run-4's three "stuck" issues all landed real impl PRs and MERGED — **#180 (PR#217), #181 (PR#218), #182 (PR#226)** ✅ → **W1 now COMPLETE (all of #174/#175/#176/#178/#182 merged)**; **W2 down to only #179** (PR#216 still OPEN, gate GREEN/CLEAN, re-confirmed verified PASS, merge held for Tim). W3 lane-self-picked out of order: **#183 (PR#227) MERGED** ✅ + **#184 (PR#228)** OPEN/GREEN/**verified PASS this run** (`_load_queue_file` guards `GET /queues/{name}` → 422 no-500; `/healthz`+`/queues` surface `queues_invalid_count`; corruption test spans `{bad`/non-object/undecodable across both endpoints + cache-reload test) — comment posted, no merge/automerge. #185–#192 + #194–#197 undispatched. **Dispatch HELD** — W2 gated solely on Tim merging #216 (#179); next run dispatches remaining W3 once #179 merges. No capacity-stuck (all run-4 stuck issues resolved). **(2026-07-04 run 6):** Near-complete. **W3 fully landed** (#185–#192 via PRs #229–#236, batch-confirmed test+src, 0 `.github/`) + **W4 #195/#197 MERGED** (PRs #238/#239). **#194** PR#237 merged to `main` (a5cc2de) but issue failed to auto-close → verified ICC gamut-map landed in full (`ImageCms.profileToProfile`, sRGB fallback, Perceptual+BPC, configurable per-device profile, `tests/test_render_color.py`) and **closed #194 manually**. Only 3 items left to close out #174–197: **#179** (PR#216 OPEN, gate GREEN, re-verified PASS, but now `CONFLICTING` → needs rebase before Tim merges; task-3 write-path `allow_nan=False` not literally applied but moot given field validation), **#184** (PR#228 OPEN, gate GREEN, `MERGEABLE`, re-verified PASS → Tim merge), and **#196** (W4 `[epic]` — body says split each checkbox into its own PR; NOT dispatched as-is, needs decomposition into 4 child issues: IIIF / Dublin-Core+Linked-Art / Getty dual-resolve / BagIt fixity → Tim/orchestrator). STOP condition not met; task stays enabled. No capacity-stuck, no thrash. **(2026-07-05 run 7):** No change vs run 6 — all three trailing items still open and human-gated. Re-confirmed live + re-verified vs squash diff: **#179** PR#216 GREEN but still `CONFLICTING` (needs rebase; task-3 `allow_nan=False` write-guard at `main.py:816` still not literal, moot given field validation), **#184** PR#228 GREEN + `MERGEABLE` (verified PASS, meets+exceeds AC), **#196** epic still undispatched (needs 4-way decomposition into IIIF/DC+Linked-Art/Getty/BagIt child issues). Fresh verify comments posted on both PRs; no merge/automerge/thrash. Nothing the driver can advance autonomously — 2 merges + 1 epic-split are all Tim's calls. **(2026-07-06 run 8):** No change vs run 7 — same three trailing items, all human-gated. Re-verified live + against real squash/head diffs: **#179** PR#216 GREEN (Python-CI 3.12+3.13 pass) but still `CONFLICTING`/`DIRTY` → needs rebase before merge; tasks 1-2 + reject-tests confirmed landed, task-3 `allow_nan=False` still not literal — write path confirmed on head as `store.append_rating` (`store.py:311`, `json.dumps(event, ensure_ascii=False)`), moot given field-level `allow_inf_nan=False`. **#184** PR#228 GREEN + `MERGEABLE`/`CLEAN`, re-verified PASS (both tasks + AC met). **#196** epic still undispatched (needs 4-way decomposition). Fresh verify comments posted on #216/#228; no merge/automerge/thrash. STOP condition not met; task stays enabled — 2 merges + 1 epic-split remain Tim's calls. **(2026-07-07 run 9):** No change vs runs 7-8 — same three trailing items, all human-gated. Both PR heads UNCHANGED since run 8 (**#216**=`887cce6f` still `CONFLICTING`→needs rebase; **#228**=`daa95ea6` still `MERGEABLE`); today's `updatedAt` is keepalive/bot fingerprint noise, not a code push. Diffs byte-identical to the already-posted PASS verifications, so **no new verify comment this run** (avoid redundant spam; prior PASS comments stand). **#196** epic still undispatched (needs 4-way IIIF/DC+Linked-Art/Getty/BagIt decomposition). No merge/automerge/thrash. 21/24 issues (#174-197) merged-and-verified; 2 verified PRs await Tim's merge + 1 epic-split remains Tim's call. **(2026-07-08 run 10):** Real movement — **#216 (#179) rebased today** (`887cce6f`→`bd9ef94b`), flipped **`CONFLICTING`→`MERGEABLE`**, and **task-3 now literal** (`store.append_rating` = `json.dumps(..., allow_nan=False)` — the not-literal-but-moot gap from runs 6-9 is closed); re-verified PASS. **#228 (#184)** also got a new commit (`daa95ea6`→`e42ae3d8`), still `MERGEABLE`, re-verified PASS. Both diffs genuinely changed vs run 9 → fresh verify comments posted on both. Both PRs now MERGEABLE + verified — only Tim's merge remains (gated). **#196** epic still undispatched (needs 4-way decomposition: IIIF/DC+Linked-Art/Getty/BagIt). No merge/automerge/thrash. 21/24 merged-verified; 3 left = 2 MERGEABLE verified PRs awaiting Tim + 1 epic-split. **(2026-07-09 Claude close-out, Tim-approved):** merged **#179 (PR#216)** clean + **#184 (PR#228)** after rebasing it onto the new main and resolving a trivial `import asyncio` test conflict (rebased branch: 39/39 tests pass; a local `_empty`-state test failure was MY stale seed `manifest.csv`/`data/ratings_log.jsonl` pollution in the clone, not a regression — removed; clean main passes). main → `df35046`. **Track B now 23/24.** Decomposed epic **#196 → children #248 (IIIF manifests), #249 (Dublin-Core+Linked-Art), #250 (Getty ULAN/AAT/TGN dual-resolve), #251 (BagIt fixity)**; #196 kept open as tracker w/ checklist comment; **dispatched #248** (agent:codex+status:ready), #249-251 filed ready-to-promote. Filed **#252** site-anchored category+place-verify (implements the approved `site_anchored_category_design.md`; upgrades the Chartres `role:unknown` stopgaps; depends on merged #193 embedding infra). Wave-driver SKILL.md extended w/ Wave-5 (#248-252) + updated STOP condition. Local archive: 0 stragglers, sidecar-complete, deduped, fixity baseline — stable. Remaining = #248 in-flight + #249/#250/#251/#252 ready + close #196 when children land; the 11 title-based work_id-collision merges still await a human sanity-check (reversible, quarantine TTL ~2026-07-29). **(2026-07-09 wave-driver run 11):** W1–W4 fully closed (#174–197 all merged/verified). W5 in flight: **#249 (DC+Linked-Art, PR#254) MERGED + VERIFIED PASS** (full Python-CI 3.12+3.13 matrix ran; `crosswalk.py:101,140` + `tests/test_crosswalk.py`) → #249 CLOSED. **#248 (IIIF, PR#253)** code-complete + verified vs AC (`iiif.py:136,211` + `tests/test_iiif.py`) but gate NOT genuinely green — its Gate run's `Validate inputs` was concurrency-cancelled → test matrix SKIPPED (Gate=failure, `gate-summary`=success is a proxy only); **re-triggered the Gate run** so tests actually execute; do-not-merge until `python 3.x=success`. **#250 (Getty, PR#255)** open, gate in-flight (autofix running) — verify next cycle. **#251/#252 NOT dispatched** (held per promote-after-#248-merges + lane cap; 2 interop PRs already in flight). #196 tracker stays open. No merge/automerge/thrash. STOP not met. **(2026-07-10 run 12):** W5 nearly done — **#250 (PR#255), #251 (PR#256) MERGED+CLOSED** (lane landed #251 same day despite being undispatched at run 11); **#252 (PR#257) MERGED, VERIFIED PASS** (place-object verify identity-gate + DINOv2 cosine≥0.55 in `collect/verify.py`; `site_anchored` predicate in `sidecar.py`+schema; `tests/test_site_anchored.py` full coverage) → **closed #252 manually** (PR's `closes #252` didn't fire on squash). **#248 (PR#253) NOW GENUINELY GREEN + VERIFIED PASS** — run-11's re-triggered Gate finished: `Python CI / python 3.12`+`3.13`=SUCCESS (real tests, not skipped), `gate-summary`=SUCCESS, MERGEABLE/CLEAN; AC confirmed vs real diff (`iiif.to_manifest`/`emit_manifest`, CLI `scripts/emit_iiif.py`, test gate `tests/test_iiif.py`); `needs-human`/`agent:retry` labels are STALE (from the concurrency-cancelled first run). Verify comment posted; NOT merged (Tim-gated). **W5 = 4/5 merged+verified (#249/#250/#251/#252); only #248 left, verified-green, awaiting Tim's merge → then close #196 tracker + disable task.** STOP not met. **(2026-07-11 run 13 — FINAL, STOP MET, task DISABLED):** **#248 (PR#253) MERGED 2026-07-10 + hardening follow-up PR#260 MERGED** → issue CLOSED; **all W5 children #248–#252 now merged**. Closed the **#196 tracker** (completion comment w/ each child's PR+gate). Also closed **#184** as bookkeeping (its PR#228 merged 2026-07-09 but never auto-closed — no closing keyword). Final verification read from merged `main`: all 5 W5 test gates real, not scaffold — `test_iiif.py` 32 / `test_crosswalk.py` 19 / `test_getty_resolve.py` 20 / `test_fixity.py` 29 / `test_site_anchored.py` 26 test-defs+asserts, **0 skips/xfails**, all merged through the gated `summary` check-run. **Every issue #174–197 + #248–#252 is merged/closed-and-verified; #196 closed. Nothing closed-unmerged, nothing left for Tim.** Scheduled task `faa-track-b-wave-driver` **DISABLED**. Remaining FAA work = local-archive ops (session chips), not this driver. |
| `Fine-Art-Archive` | **Completed (report + backlog; NOTHING filed, per owner's choice)** | 2026-08-08 | 2026-08-08 | Claude (Opus 5) repo-audit skill run; Workflow fan-out (6 analysis + 4 dims-5/6/7 research + 3 adversarial verify + synthesis); Orchestrator gemini offload ATTEMPTED and FAILED (see findings); observed UX driven live by the lead | Scope pinned with the user: **both halves** (repo tip `42a5377` + the full local workspace `Dropbox/Pictures/Claude Project/`), **full workspace sweep** (all ~138 scripts), emphasis on the **new-capability dims 5/6/7 split into roadmap + 2-week items**, deliverable = **report + backlog, NO filing**. Live verification run: `automation_audit.py --allow-network` + a live Companion App drive. Artifacts: `2026-08-08-audit-run.md`, `-15-ux-observed.md`, `-10..-14` (repo dims), `-20-workspace-sweep.md`, `-30..-33` (field research), `-40..-42` (adversarial verify), `-FINDINGS-CONSOLIDATED.md` | **Environment (recorded at start):** the Dropbox working copy is **ahead-1/behind-239** of `origin/main`; local HEAD `1a72d5a` returns HTTP 422 from the GitHub API = an **orphaned never-pushed commit** (3rd repeat of this gotcha) → audited the extracted remote tip instead. **Live automation measurement:** GROWTH **OK** (3411 works, +18 promoted 2026-08-05, frontier 1200/1091 actionable — the 2026-07-31 two-track redesign is working); COMPLETENESS **BROKEN** (34 sidecars whose artist Q-ID denotes the wrong person; 132 work Q-IDs on >1 sidecar incl. Q547923 on 50 = series-QID misapplied; work-QID coverage 76.17%, 813 absent; steps 9/10/12 still falsely `completed` = open #409). **Observed UX BLOCKER (dim 4):** the app has two sources of truth that silently disagree — browse/search reads `manifest.csv` (**3393**) while the e-paper builder and disk read the archive (**3411**); the gap is exactly the 18 works promoted 2026-08-05. `scripts/build_manifest.py` **has no caller anywhere** and `promote_acquisitions.py` never references the manifest, so promotion never regenerates it. Verified live: Repin's *Reply of the Zaporozhian Cossacks* returns 200 on `/works/{id}`, `/full` and `/dossier` but `?q=zaporozhian` → `total: 0` — present, servable, **unfindable**, therefore un-ratable, therefore never reaching the preference loop, while the e-paper builder would still place it on the wall. `/healthz` reports `manifest_loaded: 3393` and `ok: true` with no manifest↔archive drift check. **Also observed:** `/ratings/summary` **backend is fixed** (computes `quality_distribution` + `fit_distribution`) but the **UI template renders only the deprecated `rating_distribution`** → the operator sees `{"1": 2}`, i.e. **2 of 93 events (2.2%)**. **FIXED since 2026-06-28 (verified, do not re-file):** manifest/ratings process-lifetime cache (now signature-invalidated), htmx CDN (now vendored at `api/main.py:155`), hardcoded `ART_WORKS_ROOT` (now `env_path()` + `Path.home()`). **OUTCOME: 119 findings** (P0 11 / P1 75 / P2 21 / P3 12) deduped from **167 adjudicated claims**; **18 REFUTED and dropped**, 9 BLOCKERs re-graded down, 1 MAJOR raised in reach. **Dominant class = the unrun wire between two halves that each work** - a producer and a consumer that both exist, both pass their own tests, never connected, with the seam falling across the repo<->workspace boundary where no import/test/type-checker can observe it (verify Layers 2-5 at **0 of 3411**; 4 of 5 screening gates unread; dedup cascade documented as "the blocking gate" and gates nothing). **The 2026-06-28 class was fixed at the cited line but NOT at the level that mattered**: `acquisition_flow.py:88` now loads the config and a wiring test gates it, yet the subsystem still has zero production effect because `run_acquisition_flow` has no caller in either tree, the config is 2.5 months stale (2 distinct scores across 24 rows), and 40% of the composite weight is a hardcoded `True` in every acquire script. **FIXED since 2026-06-28 (verified live, do not re-file):** work_id path traversal (re-probed: `..%2f..%2fetc%2fpasswd` -> 400), manifest/ratings cache (now signature-invalidated), htmx CDN (vendored at `api/main.py:154-163`), hardcoded `ART_WORKS_ROOT` (now `env_path()`). **Dims 5/6/7 (the owner's emphasis): 17 AMBITIOUS epics + 32 NEAR-TERM items**, each with a named seam at file:line, plus 6 researcher disagreements stated rather than averaged (report 32 prescribed deleting `display/`; the verifier proved that would BREAK live acquisition). Standouts: N-M3 validate artist QIDs against their own Wikidata label (highest value-per-line; fixes the 34 wrong-artist sidecars), N-E1 corpus gamut-fit score (answers the colour question with NO hardware), N-C7 one Bradley-Terry session (~10 min mints the first real negatives; the rating class is empty by construction), A1 two-witness cross-institution fidelity corpus (genuinely unclaimed - nobody measures the same painting across institutions). **Dim-8 finding:** the Orchestrator gemini lane is **broken** — `dispatcher.py offload --agent gemini` passes `--model gemini-2.5-pro`, which the installed CLI no longer recognises (available: Gemini 3.6/3.5 Flash, 3.1 Pro, …) → exit 1, zero output, no report written. Any audit or automation routing big reads to gemini is silently losing that capacity. | **None — deliberate.** The owner chose *report + backlog, no filing* for this round. Nothing pushed to GitHub, nothing dispatched. The 12 highest-leverage items and the 8 owner decisions are written up ready to file. | **Owner decisions D1-D8 (~75 min one-off) are the gate on most of the P0 work** — especially D2 (series rule; a >=0.99 visual scan finds only 13 genuine duplicate pairs against 132 collisions, so dedup would destroy real distinctions) and D5 (standing monthly cap; the manual growth loop measures ~32 min/cycle against a <=30 min/week budget, ratio ~1.1, which is why only 1 cycle ran in 8 days). **DECISIONS 2026-08-08:** D5a deepen+curated-widening, D5b cap **200/month** (guardrails first - 4 screening gates are unread, add N-C4 diversity cap), D7 **DEFER hardware** (category immature; N-E1 gamut-fit becomes top e-ink item, park #469; buy on **pre-dithered ingest** when it matures - only 1 of 179 devices has it), D8 **consolidate fork staged**. **D1/D2/D3/D4/D6 RATIFIED** same session (none executable yet - each gated on code that does not exist; D3 is the only one runnable today, D2 hard-blocked on the N-M1 schema change). **D8 step 1 IMPLEMENTED** (branch `audit/d8-port-dim-compat`, commit `9335000`, not pushed) - and it corrected the audit's own advice: 2 of the 3 fork modules the audit said to port had **nothing to port** (larger only because they predate refactors already done upstream); porting them would have re-introduced duplication. Only `_dim_compat` was real (live at `find_inventory_duplicates.py:91`), now at `parsers/dimension_utils.py` with re-exports so the fork is safe to delete. 711 passed/11 skipped, ruff + black 26.5.1 clean. Detail: `Fine-Art-Archive/2026-08-08-DECISIONS.md`. **Repo synced 2026-08-08:** main was ahead-1/behind-239 with an orphaned unpushed HEAD `1a72d5a`; verified superseded (remote's test file has 589 lines/23 tests vs 556/14), preserved as patch + tag `archive/pre-sync-1a72d5a` + both stashes, then reset to `origin/main` -> **0/0, clean tree, `git fsck` clean**. **D3 EXECUTED 2026-08-08** - and the literal instruction would have BACKFIRED: `state_integrity.check()` gated verifiers on `status == "completed"`, so reopening the steps would have SILENCED their verifiers and turned the check green by no longer looking. Fixed in order: (a) finding 66 first (`_v_step10` picked the run report lexically, selecting a 2026-05-26 batch out of 18 runs; now temporal - step 10's reason changed from "21 permanent failures" (May) to "6" (Aug 5)); (b) verifiers now run regardless of status, so a failing verifier on a REOPENED step is DRIFT (honest unfinished work) while on a COMPLETED step it stays BROKEN (a false claim); (c) reopened steps 9/10/12 with a full audit trail, backup `automation_state.json.bak-pre-d3-2026-08-08`, only those 3 steps changed. Result: `state_integrity` **BROKEN -> DRIFT**, `falsely_completed` 3->0, **`skipped: []`** (the proof the trap was avoided), COMPLETENESS `broken 3,drift 1,ok 2` -> `broken 2,drift 2,ok 2`. **D1 was substantially executed independently the same day** (NOT by this session): at 21:16Z a grant-governed repair (`repair_artist_qid_provenance`, grant **G25**, 109 ops: 75 CONFIRM / 31 RESTORE_NAME / 3 REJECT_QID, each fully reversible) applied name-verified-wins, and a new check `artist_qid_provenance.py` found a **bigger defect than this audit did** - 124 sidecars recorded `method: unresolved` + `confidence: 0.9` with a Q-ID written anyway, of which only 31 were visible to the validity check this audit used. **So this audit's "34 mismatched artist Q-IDs" was an undercount of a 124-row defect.** Now cleared (`qid_asserted_by_unresolved_method: 0`, validity check OK); residual DRIFT = 87 sidecars with a Q-ID and no method recorded. D1's remaining half is preventive (issue draft 06): the writers can still re-corrupt the corpus. **#407 RESOLVED manually 2026-08-08** - the last canonical/mirror conflict, `d735d94-william-henry-harrison-peale`: canonical `Q5598` (Rembrandt van Rijn) vs mirror `Q375926` (Rembrandt Peale), where `artist.name` is "Rembrandt Peale". Cause is in the sidecar's own note - `"distinctive-surname match on 'rembrandt'"`, i.e. the resolver folded the FIRST name as a surname (the fuzzy-fold class G37 already refuses in bulk). Verified 3 ways, none from recall: label/alias mismatch; chronology (Q5598 died 1669, **104 years before the sitter W.H. Harrison was born**); and the work's own **P170 = Q375926** on Q28797102. Written under standing grant **G25 / class R1**, before-state logged to operations.log first, sidecar backed up, result validated against the canonical repo schema. `canonical != mirror` count now **0**; "Artist Q-ID coverage" **BROKEN -> DRIFT**. **Session severity trajectory: `broken 4, ok 1` -> `broken 1, drift 3, ok 2`** (the single remaining BROKEN is Work-QID validity = D2, gated on the N-M1 schema change). **ISSUE-TRACKER FINDING:** #406-409 are well-formatted but **structurally unaddressable in this repo** - all 6 paths #409 names exist ONLY in the workspace (0 of 6 in the repo), which is why #409 carries `agents:tried-codex` -> `needs-human` -> `agents:auto-pilot-pause`. The format guard is working correctly; `.github/scripts/issue_format.py` validates required SECTIONS and has **zero** path-existence checking, so addressability is an axis it never tested. Two fixes needed in **Workflows** (synced): add an addressability gate, and fix `agents-issue-format-guard.yml:57-61` which **silently passes every issue when the validator file is absent**. Same test applied to this audit's own 8 drafts: 02 and 03 are workspace-only (would stall a lane), 01 is mixed, 04-08 are clean. **Sequencing plan written: `Fine-Art-Archive/2026-08-08-NEXT-SEQUENCE.md`** (6 waves: finish the fork consolidation -> gate the issue tracker -> 5 live defects -> the strictly-ordered D5 growth chain -> identity durability -> capabilities). Next ledger action: Wave 0 = D8 steps 2-4 (pip install -e, delete fork, re-run ops scripts), then file the twelve-worth-doing-first set. **Carry to the next audit:** re-point the Orchestrator gemini lane (verified fix `ORCH_GEMINI_MODEL="Gemini 3.1 Pro (High)"`), and audit the REMOTE tip - the Dropbox copy was ahead-1/behind-239 for the third consecutive audit. |

| `Orchestrator` | **CLOSED & reconciled** (audit + full implementation) | 2026-07-03 | 2026-07-03 | Claude (Fable 5) full repo-audit skill run; SELF-REFERENTIAL — dims 1-3 ran on the Orchestrator's own offloads (gemini wiring / codex Brain-correctness / cursor duplication / vibe docs, 4/4 PASS = live self-test), dims 5-7 via 6-agent Claude Workflow web sweep, full live exercise (fleet observed mid-audit incl. autonomous 3-agent A/B/C, manual shadow tick, Brain forensics, GH cross-checks 3/3 truthful); read-only drift scan 0/72 | `Orchestrator/2026-07-03-AUDIT_REPORT.md` (+ `-verification-log`, per-dim `-00..-06`, `2026-07-03-research/R1-R6`) | **P0 cost-blind routing**: score formula treats missing cost as free (feedback.py:609-611; the ONLY measured cell, implement/codex post 0.803, scores LOWEST in row) + completion telemetry destroyed (522 ledger_reconcile SIGKILLs, 641×$0 ledger rows, successful offloads record NULL cost/latency; killer UNCONFIRMED, reaper refuted) = Gap C local root causes; P1: cadence stamp-on-success -> 183 hourly retries of failing daily langsmith step; redirect corpus frozen since 06-25 DESPITE shipped flag fix (sweep samples idle hour-marks, watched=0); human_calibration 0 rows ever (judge weights permanently neutral); claims races (verified MAJOR); 13 CLI-only lane modules ~7k LOC (range built != flowing); P2 hygiene (slug divergence x3, parser drift, stray 0-byte sqlite, unrotated 11.8MB log, idle aider seat). WORKS WELL: truthful outcomes, live hourly ticks + A/B/C, yield guard (24x RELAY-HALTED), drain-mode steering worked in anger, docs 0 MAJOR. FIELD (R1-R6, all converged): learned agent-x-task routing under expiring subscription quota has NO published equivalent (publishable); import shortlist = Thompson sampling (~50 LOC), pre-PR critic best-of-N, 20-40-label judge calibration, resume-token registry, drain-aware continuous cost weight, structural agent credentials, OTel ingest, MCP-server exposure. 3 refuted findings recorded (incl. self-refuted offload-timeout claim) | IMPROVEMENT_BACKLOG.md items 9-16 appended IN-REPO (no GitHub issues — not a git repo): 9=P0 telemetry+scoring (Wave 0), 10=cadence backoff, 11=event-driven redirect corpus, 12=weekly 5-label calibration surface, 13=claims lease/fencing, 14=range slot for CLI-only lanes, 15=P2 hygiene, 16=field imports (a)-(m) | **Item 9 IMPLEMENTED 2026-07-07** (both learners imputation-fixed — live path is relearn_quality via relearn_report.py; done-markers+backfill+instant meter; plist; v52 live; remaining: two-tier outcome enum — see backlog item 9 status). **Item 16(a) RESOLVED 2026-07-07**: Thompson was already built (ε-gated thompson-hybrid mode) and the fleet's own exploration_review (83 instrumented runs, weekly) says keep ε-greedy — default not flipped; recency decay DELIVERED (relearn_quality half-life 30d, v53 live). **Item 12 DELIVERED 2026-07-07** (calibration label-ask queue: CLI --queue + weekly report LABEL ASK block; 88 pending, top spreads 9/10 w/ self-preference bias visible; needs Tim's ~5 labels/week to activate). **Items 12a/12b/12c DELIVERED 2026-07-08** (zero-owner calibration: judge weights de-saturated + live-discriminating; objective anchors from persisted diffs, decisive-signals-only; guaranteed neutral drain-preferred referee; NEW FINDING: zero tick-* evaluations ever + 249-experiment unevaluated backlog -> exp_abcd followup cadence closes the lifecycle; 2 dormant eval-path bugs live-caught+fixed same evening: E2BIG one-arg prompt, strip()-corrupt patches). **Items 9/10/11/13/14 ALL DELIVERED 2026-07-08** (two-tier transient-infra enum wired to done-markers; cadence backoff+ALERT on all 12 stamped steps; event-driven redirect corpus from failed experiment arms; claims live-pid guard+reap-grace+reap-mutex; daily range-rollout slot, preview default/env-gated active — plus range_lane_rollout's own failing selftest fixed, third built≠flowing proof). ALL audit P0/P1 findings now implemented. **16(f)+16(h) DELIVERED 2026-07-08 eve** (resume-token registry; non-blocking owner-question protocol w/ auto-ratifying defaults + prompt injection). 16(i)/(m) SKIPPED per owner (no approval-gating — effort analysis: fleet output = 19-44 FTE-months/month, gating infeasible 10-40x; no publishing). **Trio 16(d)/(g)/(e) DELIVERED 2026-07-08 night** (continuous drain pacing in router; Bradley-Terry duel warm-starts blended into relearn priors; adversarial pre-delegation gate ACTIVATED (was never exported) + daily best-of-N ship-gate in followup). Cross-project human-involvement-check rule+skill created in ~/.claude. **Plumbing 16(j)/(k)/(l) DELIVERED 2026-07-08** (native cost ingest; A2A states; MCP server registered+verified). **Project-knowledge root-cause fix**: README rewrite + new CLAUDE.md (dedup-before-develop) + fresh dormancy re-scan + disposition plan; runtime-AC activated, ux_review.calibrate retired, range-lane-live = non-blocking owner question. Enhancement tier 16(a)-(m) COMPLETE except owner-skipped (i)+(m). All P0/P1 audit findings + resilience pair + high-value trio + plumbing all shipped. **AUDIT CLOSED 2026-07-08** — reconciliation `Orchestrator/2026-07-08-AUDIT-CLOSEOUT.md` (all findings DONE/RESOLVED/DECLINED-owner/KEPT-GATED; LangSmith Gap-C leg retired as duplicative). **Range-lane LIVE dispatch = owner-approved bounded trial 2026-07-08→07-15** (self-expiring safe-revert 07-16; local scheduled review 07-15; cloud trigger svc was 404). Re-run Brain cost-coverage queries to prove the meter; item 16 imports follow; consider publishing the quota-arbitrage router (16m) |

## Review-Only Records

These records are useful continuity inputs, but they were not normalized as full-audit logs because the available source was a weekly review, time-boxed dogfood audit, or partial candidate review rather than a full audit.

| Repo | Record type | Started | Completed | Source | Main findings | Issues / PRs generated | Next action |
|---|---|---:|---:|---|---|---|---|
| `Inv-Man-Intake` | Time-boxed skill dogfood audit (RECONCILED by 2026-06-28 full audit) | 2026-06-20 | 2026-06-20 | Root `Inv-Man-Intake-Audit-2026-06-20.md`; Claude repo-audit skill test | Inert TOML scoring weights; red-flag float equality; inert LLM configs; threshold fallback drift; homogeneous fixtures; duplicate review scripts | Filed #592-#602 (all CLOSED). 2026-06-28 impl-verification: 9/11 genuine fixes; #592 PARTIAL (credit-only → #693), #595 PARTIAL (non-atomic → #697) | Superseded by the full-audit row above; see `2026-06-28-AUDIT_REPORT.md` |
| `Fine-Art-Archive` | Weekly review | 2026-06-17 | 2026-06-17 | Workflows-steward weekly review rerun | `source_quality_inputs` not written; Companion App `/rate` endpoint untested; broader model-input write-path meta audit remained deadlocked | Fine-Art #98 and #99 filed 2026-06-18 | Check issue state before follow-up work |
| `Manager-Database` | Weekly review | 2026-06-17 | 2026-06-17 | Workflows-steward weekly review | EDGAR outbound request rate-governor and earlier review findings | Manager-Database #1185 | Check issue state before follow-up work |
| `Trend_Model_Project` | Post-merge implementation verification (5 closed issues) | 2026-08-24 | 2026-08-24 | Claude Opus 5 `implementation-verification` skill; squash-diff reading, named-gate collection + run, first-person runtime re-measurement, `adversarial.review` (vibe+cursor) on the contested verdict | #5986 NOT DELIVERED - defect live, named gate absent, its inverse merged and asserts the defect; #5988 Non-Goal breach weakened a `max_active_positions` assertion; #5984 gate renamed; #5985 scalar-`formats` regression | NONE filed - 2 bodies staged, lint-passing | Owner decision on `2026-08-24-issue-bodies/01`,`02`; file 01 first |
| `Workflows` | Post-merge implementation verification (5 closed issues) | 2026-08-24 | 2026-08-24 | Claude Opus 5 `implementation-verification` skill; `local_verify.py` supplied the deliberate-break proofs 3 PR bodies omitted; live Actions + tracker-marker state via `gh` | P0 #3179 delivered and the 23-day Health 68 outage is over (#2210 marker refreshed, tracker auto-resolved); #3183 partially delivered - `divergence_reviewed` ratchets with `fingerprint_refreshed` on all 20 pairs and its gate only checks non-emptiness; the new liveness oracle counts a debounced no-op as an execution; 4 of 5 PR bodies fail the break/revert AC | NONE filed - 2 bodies staged, lint-passing | Owner decision on `2026-08-24-issue-bodies/03`,`04`; file 03 first |

## Focused Route-Weight Audit Rounds

These are not full repo audits. They are focused candidate-mining passes for Orchestrator Route-Weight / Exploration data.

| Round | Started | Completed | Repos | Artifacts | Main outcome | Next action |
|---|---:|---:|---|---|---|---|
| `2026-06-27-route-weight` | 2026-06-27 | 2026-06-27 | `learning-management-system`, `trip-planner`, `Manager-Database`, `Inv-Man-Intake`, `Fine-Art-Archive` | `2026-06-27-route-weight-round.md`, `2026-06-27-route-weight-candidate-matrix.md`, `2026-06-27-route-weight-evidence-campaign.md`, and per-repo `2026-06-27-route-weight-findings.md` files | Identified safe opener candidates, mostly `testgen`; filed the initial six current-tip verified opener issues plus expansion issues `trip-planner#1495/#1496`, `Manager-Database#1266/#1267`, and `Fine-Art-Archive#165/#166`; dispatched seven supervised agent attempts; opened PRs `Manager-Database#1263`, `Fine-Art-Archive#164`, `learning-management-system#393`, `Manager-Database#1268`, and `trip-planner#1497`; filed process follow-up `Manager-Database#1264`; and recorded Codex runtime failure, Vibe scope drift, Cursor clean delivery, Gemini PR-permission stall, Vibe partial-with-controller-polish, wrapper cleanup kills, and validation/testgen-gate coverage-default caveats as route evidence | Monitor PRs #1263/#164/#393/#1268/#1497 and process-health #1264; treat `Manager-Database#1265`, `Manager-Database#1269`, and `trip-planner#1494` as bootstrap closer PRs; consider a `testgen_gate.py` follow-up for standalone script-module coverage measurement |
| `2026-06-27-route-weight-wave4` | 2026-06-27 | 2026-06-27 | `trip-planner`, `Fine-Art-Archive` | `prompts-2026-06-27-route-weight-wave4/`, `route-weight-wave4-pr-bodies/`, `2026-06-27-route-weight-round.md` | Continued the same evidence campaign after the initial ledger row: opened `trip-planner#1499`, `Fine-Art-Archive#168`, and `Fine-Art-Archive#169`; recorded Cursor branch-recovery success on #1493, Vibe failure/contamination on #166, Cursor clean recovery PR for #166, and controller lint/typing cleanups for #1499/#169; all three PRs reached green Gate/Python checks and CodeRabbit passed | Monitor only metadata/event-handler noise and later durability/merge outcomes |

## Run Template

Use this template for each new audit run:

```text
repo:
audit_id:
started_at:
completed_at:
auditor:
automation_or_skill:
prior_context_read:
scope:
categories_completed:
main_findings_by_category:
issues_created:
prs_created:
verification_status:
blocked_or_non_actionable:
artifact_paths:
follow_up_status:
```

---

## 2026-08-11 — trip-planner + Travel-Plan-Permission (paired system audit)

Source/automation: repo-audit skill + ux-review overlay; 6 Orchestrator offloads (2× cursor
sweeps, 1× cursor frontend, 2× gemini, 1× codex seam). Claude held the lead seat only —
orchestration, adversarial verification, and driving the running app.

Bases: tp `c5975fc6`, TPP `6ea4a5e5` (fresh local-disk clones). CI green on both `main` at
2026-08-11T07:31 and treated as ground truth.

Category coverage: all 8 base categories, plus two user-designated focus areas — the
cross-repo policy/implementation sync contract, and observed usability/UI quality.

### Main findings by category

- **Functionality & wiring (the headline):** the policy layer fails open. `check_trip_plan()`
  runs only `PolicyEngine`; the engine owning `BUD-001` (`trip_limit: 5000`, blocking) is
  reached only via `TripPlan.run_validation()`, which has **zero production callers**. Worse,
  `_context_from_plan()` never passes `estimated_cost` and `PolicyContext` has no total-cost
  field, so the planner-facing engine is *structurally incapable* of evaluating a spend cap.
  Runtime: $99,999 vs a $5,000 blocking cap → `status="pass"`, `issues=[]`.
- **Code quality/correctness:** blocking rules pass on absent or non-finite input, proven with
  matched controls (`lowest_fare=None` → pass vs `=200` → fail; `duration=None`/`NaN` → pass vs
  `2.0`/`-50` → fail). NaN slips through where negative is caught — a finiteness gap, not an
  intentional skip. Also: production imports `tests.preferences.fixture_corpus`, making
  `trip_planner.app.main` unimportable without the test package (masked only by
  `pip install -e .` on Render).
- **Cross-repo contract:** 7 MAJOR. `policy_status` written to metadata and never read; typed
  `booking_requirements` replaced with hard-coded empties; `compatible_with_planner_cache`
  dropped so version incompatibility is silently accepted; alternative `title`/`suggested_value`
  lost to a renamed duplicate model.
- **Design/UX — gate FAIL** (panel median 3.0, 5 severity-4 blockers, 3/4 evaluators returned,
  no consensus): Plan tab 20,188px/28 screens vs Policy 1,354px/1.9 — because Plan re-hosts
  `WorkspaceBudgetPanel` (`:1902` + `:2475`) and `WorkspacePolicyPanel` (`:1972` + `:2538`).
  Policy tab is a dead end with zero panel controls. A TPP outage is indistinguishable from
  compliant. Marketing `h1` outranks the trip name on every workspace route. Mobile: 24px
  overflow, 51 sub-44px tap targets, 13×13px radios.
- **Duplication/consolidation:** monoliths flat-or-growing since 2026-07-10 —
  `workspace.py` 4,401 (was >4,000), `http_service.py` 2,546 (was 2,538);
  `WorkspacePage.test.tsx` is 3,724 lines, larger than the 2,600-line component it tests.
- **Field/opportunities/tools:** close the enforcement gap first; share schema across the
  Python/TS boundary instead of hand-maintained parallel contracts; add a real-inventory
  import path. Stay deliberately pre-booking.
- **Prior-findings continuity:** all 11 findings from 2026-07-10 still open at this tip, since
  that audit was report-only and filed nothing. TP-06 corrected OPEN→PARTIAL (no SDK loads, but
  the UI now labels itself honestly, which was the actual complaint).

### Issues filed (triage-only — no `agent:*`, `status:ready`, or `agents:auto-pilot`; verified zero lane PRs)

| Issue | Repo | Severity |
|-------|------|----------|
| #1428 | TPP | BLOCKER — validation.yaml blocking rules incl. BUD-001 never applied |
| #1429 | TPP | BLOCKER — blocking rules pass on absent/non-finite input |
| #1675 | tp | MAJOR (latent blocker) — production imports the `tests` package |
| #1676 | tp | MAJOR — TPP policy denials discarded |
| #1677 | tp | MAJOR (UX) — Plan tab re-hosts Budget and Policy panels, 28 screens |
| #1678 | tp | MAJOR (UX) — Policy tab dead end; outage looks compliant |
| #1679 | tp | MINOR-MAJOR — mobile overflow, tap targets, heading hierarchy |
| #1680 | tp | MINOR — committed SQLite binary mutated by local runs |

The repo's own format-guard workflow auto-added `agents:format` to several issues. That is a
conformance stamp, not a dispatch trigger (the Renovate bookkeeping issue #1384 carries it
too); confirmed no `agent:<name>`/`status:ready`/`agents:auto-pilot` and no lane PRs.

### Non-actionable / refuted (do not re-file)

- **`trip_planner/orchestration/` (3,592 LOC, 5 test files, zero production imports) is BY
  DESIGN** — closed issue #960 "Wire broader orchestration only after the planner/runtime seams
  are proven", corroborated by the in-code note at `workspace.py:2823`. Cursor called this its
  strongest finding; recorded INSUFFICIENT_EVIDENCE.
- Cursor's `estimated_cost=99999 → "pass"` repro **did not reproduce as stated** (its fixture
  failed on `fare_evidence`); the finding is real but was re-derived with a clean plan.
- Doubled API requests are React 18 StrictMode dev double-invoke (`main.tsx:14`), not a
  production defect.
- Two of my own initial reads were wrong and corrected before filing: login inputs *are*
  properly labeled (implicit `<label>` wrapping), and the tab buttons *do* expose a correct
  ARIA tabs pattern.

### Not verified — deliberately NOT filed

TPP Sweep-B persistence findings (non-atomic mutation/audit, multi-writer lost updates) were
not independently reproduced; they corroborate prior TPP-01 but need a concurrency repro first.
The live TPP browser round trip, the keyed Google Maps branch, signup, trip creation, and the
planner AI turn were not driven — see the UX coverage ledger for reasons.

### Artifact paths

`Code/Audits/2026-08-11-AUDIT_REPORT.md` (executive, both repos),
`2026-08-11-prior-findings-verification.md`, `2026-08-11-02-sync-contract.md`,
`2026-08-11-06-field-and-opportunity.md`, `2026-08-11-issue-bodies/`,
`Code/Audits/trip-planner/2026-08-11-{UX_REVIEW,03-backend-sweeps,05-frontend-ux,audit-run}.md`,
`trip-planner/2026-08-11-assets/`,
`Code/Audits/Travel-Plan-Permission/2026-08-11-04-policy-core-sweeps.md`,
`Travel-Plan-Permission/2026-08-11-assets/` (two runtime proof scripts + captured output).

### Next ledger action

Verify #1428/#1429 fixes with the recorded proof scripts (they should flip from `pass` to
`fail`), then re-run the UX panel after #1677 lands to confirm the Plan tab drops under 8,000px.

---

## 2026-08-11 — Trend_Model_Project full re-audit (UX-weighted)

**Source/automation**: `repo-audit` skill + `ux-review-overlay`; Claude Opus 5 lead with Orchestrator
offloads (gemini ×2, cursor, codex, vibe). Owner asked for Claude capacity to be conserved for
orchestrating other repos, so all bulk reading was offloaded and the lead seat did scoping,
observed UX, adversarial verification, synthesis, and filing.

**Repo/commit**: `stranske/Trend_Model_Project` @ `b45d1780`, branch `phase-3` (default).
**Status**: audit COMPLETE. 8 issues filed triage-only (#5809–#5816), no `agent:*`/`agents:*`/
`status: ready` labels, so nothing auto-dispatches into the lane.

**Context**: post-fix-arc re-audit — all 51 issues from the 2026-06-01 audit (#5389–#5439) are
CLOSED. Scope kept the prior exclusions (`agents/`, `archives/`, `retired/`, `.github/`, synced
`tools/`+`scripts/*`).

### Category coverage

All 8 dimensions covered. Dim 4 (design/UX) was the owner's emphasis and was driven live against a
real server — every one of the 7 primary Streamlit surfaces driven; only the WASM/stlite twin was
left undriven (excluded by scope).

### Main findings by category

- **P0 / hygiene+CI**: `phase-3` red on every push since ≥2026-08-04. Formatter-contract split —
  CI checks `black --line-length 100`; `[tool.black]` sets none (88), pre-commit passes none (88)
  and pins black 24.8.0 vs CI 26.5.1, and `scripts/style_gate_local.sh` also uses 88. Proven
  empirically: at 100 four files fail, at 88 only two — two files are 88-clean/100-dirty, so the
  repo's own tooling produces code CI rejects. → #5809
- **P0 / UX correctness**: Results banner reported `Sharpe -2.04` while Summary reported `1.14` on
  the same screen (opposite signs). `3_Results.py:114-130` falls back to `metrics["Sharpe"].iloc[0]`
  — the first *fund's* Sharpe — despite a docstring promising portfolio-level. → #5810
- **P0 / wiring**: same config → different numbers by entry point. Single-period ignores
  `transaction_cost_bps`/`cost_model.*` and `weighting.name`; `vol_adjust.enabled` is read by
  `pipeline_helpers.py:79,436` but popped by `config/model.py:551-559`; `harness.py:597` uses
  `ddof=0` vs canonical `ddof=1`. Found independently by gemini AND cursor. → #5813
- **P1 / UX**: Data page counter `0 of 20` with 20/20 checked (read-before-seed, `1_Data.py:735`
  reads keys seeded at `:743-751`) → #5811; profile switcher renders only on `app.py:41` while gated
  pages say "switch in the sidebar", and `?profile=` is lost on first navigation (undermines open
  #5343) → #5812; Monte Carlo runs a `production`-tagged registry scenario unrelated to loaded data
  → #5815; dev/QA surfaces shipped to users + self-contradictory Quick Start + duplicate preset
  vocabularies → #5816.
- **P1 / config**: `extra="forbid"` reached 3 sub-models; `TrendConfig` still `extra="ignore"`,
  `PortfolioSettings` `extra="allow"`; `lint_keys.py` omits `preprocessing`. → #5814
- **Dim 1/2**: broad `except` handlers grew ~40 → **268** (204 src + 64 streamlit_app);
  `engine.run()` genuinely shortened to 343 lines but complexity relocated into
  `_run_threshold_hold_multi_periods()` (2,440 lines, nest 10). Not filed — captured in the report.
- **Dims 5–7**: gemini partially dissented from the prior "no comparable tool" thesis (fair: TMP is
  an opinionated reproducible harness, not an optimisation library). Best opportunities are all
  wire-what-exists: `factor_attribution.py` not in `METRIC_REGISTRY`; `deflated_sharpe.py` never fed
  trial counts; `universe.py:40` point-in-time loader not exposed in UI; swap hand-rolled
  Ledoit-Wolf/OAS for `sklearn.covariance`. Not filed — roadmap material in the report.
- **Dim 8**: no recurring-human-attention sink exists in this repo's tooling — no
  human-involvement redesign needed.

### UX panel

**4/4 evaluators** (after correcting an error of mine — see below). claude 2/3/5/4 overall **3**;
codex 3.5/5.0/6.0/5.0 overall **4.9**; cursor 4/5/5/5 overall **5**; vibe 4/5/6/5 overall **5**.
Medians: wired **3.75**, usability 5.0, help_clarity 5.5, workflow 5.0, overall **4.95** — well under
the 7.0 bar, with `wired` worst on every evaluator.
`synthesize_improvements` produced corroboration-3, severity-4 hints that independently match every
observed finding, including "single source of truth for headline and detail metrics".

### Corrections made (kept for calibration)

- gemini's `data.frequency` "hardcoded 12" BLOCKER **overstated** — `infer_periods_per_year()`
  exists (`util/frequency.py:159`), `regimes.py` threads it, `pipeline.py:246` accepts an override.
  Narrowed to "12 is the metrics-layer default; end-to-end honouring is path-dependent".
- gemini's `vol_adjust.enabled` BLOCKER **reframed** to path-dependent (it IS read in
  `pipeline_helpers.py`), not "silently ignored".
- vibe's 7 BLOCKERs downgraded to 1 shared + P2s (root clutter, schema regen are not blockers).
- codex's "preset ambiguity genuinely remediated" **contradicted by observation** — Help still says
  `Baseline/Conservative/Aggressive/Custom` while the demo selector says `Balanced`.
- Two of my own in-flight readings were wrong and corrected before filing: `ModuleNotFoundError`
  for `analysis` and `ds_streamlit` were **my incomplete audit tree**, not repo bugs; and an
  apparent "only the Date column renders" defect was canvas paint timing.

### Post-audit fix landed

**STATUS: MERGED AND VERIFIED GREEN.** PR #5818 squash-merged as `9d4ac1a7`; issue #5809 closed.
The `ci.yml` push run on that commit is **success**, ending the red streak
(failure 08-04, 08-07, 08-08, 08-09 -> success 08-12).

The fix was two defects, not one:
1. `line-length` set nowhere -> black defaulted to 88 vs CI's explicit 100 (at 88 a bare `black .`
   rewrites **648/1053** files). One line in `[tool.black]` also fixes the pre-commit hook and
   `scripts/style_gate_local.sh`, since both read `pyproject.toml`.
2. `pr-00-gate.yml` had `format_check: false` -> **PRs never checked formatting** while push did, so
   unformatted code merged green and reddened the branch. Now `true`. This is the recurrence fix.

Verification wrinkle worth recording: the first push run failed on `Python CI / python 3.13` at
`tests/workflows/test_keepalive_post_work.py::test_keepalive_sync_detects_head_change_without_actions`
while 3.12 passed on identical source. A no-change re-run passed -> the test is **flaky**, not caused
by the reformat. It had not failed in the previous 6 runs. Candidate follow-up if it recurs.

**Process note:** I initially reported "phase-3 green" off the `lint-format` job alone while the run
was still in progress; the run then concluded `failure`. Corrected within the session.
**Rule: read the RUN conclusion, not a single job.**

PR **#5818** (2 commits) fixes P0 #1 end to end: `line-length = 100` in `[tool.black]` (the missing
line — at black's 88 default a bare `black .` rewrites **648/1053** files), plus
`pr-00-gate.yml:74` `format_check: false` → `true`. The second half is the one that matters for
recurrence: `ci.yml` is push-only by design, so with the gate's format check disabled, unformatted
code merged green and reddened `phase-3` on the next push (same `format_check:false` pattern as
Pension-Data). Not changed, deliberately: `[tool.ruff] line-length` (inert — `lint.select` excludes
E501) and `.pre-commit-config.yaml` (already correct at tip).

### Three of my own process errors, corrected after the fact (calibration)

- I reported a three-way ruff/black/mypy version skew. **It was not real** — I compared the tip's
  `autofix-versions.env` against stale copies of `pyproject.toml` and `.pre-commit-config.yaml` that
  my tree-refresh had silently skipped (zsh: `status` is read-only). At tip all three agree.
  **Rule: never diff a "current" file against an unverified local copy; confirm the refresh landed.**

- I reported the panel as "2 of 4 evaluators produced ~115-byte stubs (claude, vibe)". **Wrong**: I
  sized those artifacts while the evaluator processes were still writing. claude finished at 14 KB /
  17 findings. Only vibe failed — upstream `HTTP 520` from the Mistral API — and it succeeded on the
  **first** retry. Rules for next time: **size an artifact only after the process exits, and retry an
  agent before declaring it unusable.**
- I reported the sync as done based on a shell `rc=0` that came from a pipeline's last element
  (`tail`), not from `git`. The fetch had actually failed. **Check the exit status of the command you
  care about, not the pipeline.**

### Environment / tooling notes (worth folding into the skill)

Dropbox copy was 81 commits behind (only **17 in-scope files** differed) and unusable for bulk reads
(`Stale NFS file handle`, 120s timeouts); `git clone` failed with an RPC error and the API tarball
stalled. Tree was assembled by copying in-scope paths to local disk + API-refreshing changed files,
then provenance-stamped. `frontend_verify.py` was unreliable against Streamlit (snapshotted before the websocket render;
sub-pages returned a 1-node tree and blank 4 KB PNGs) — **now FIXED in
`~/.codex/orchestrator/frontend-verify/verify.mjs`**: a `settleForContent()` helper waits for the aria
snapshot to be non-trivial and stable for ~750 ms plus a bounded `networkidle`. A first-stable-reading
test was NOT enough: Streamlit plateaus after painting its sidebar, so a quiet *window* is required.
Verified: /Data 1→42 nodes, /Model 1→30, /Help 1→341, Run Demo→Results drivable at 120 nodes; static
control page still passes in 1.9 s. All 7 TMP surfaces now have valid screenshots. **Two zsh
hazards cost real time: `local path=...` clobbers `PATH`, and `status` is read-only** — both surfaced
as misleading "command not found" / "node not on PATH" errors.

### Artifact paths

`Code/Audits/Trend_Model_Project/2026-08-11-{audit-run,AUDIT_REPORT,UX_REVIEW,verification-log}.md`,
`…-01-wiring.md` (gemini), `…-02-quality-dup.md` (cursor), `…-03-ui-wiring.md` (codex),
`…-04-hygiene-automations.md` (vibe), `…-05-field-opportunities.md` (gemini),
`…-2026-08-11-assets/{bundle.json,report.json,improvements.json,*.png,verify/}`.
Per-evaluator rubrics: `Orchestrator/ux_reviews/stranske/Trend_Model_Project_uxreview_2026-08-11/`.

### Next ledger action

Fix #5809 first (cheap, unblocks a green branch), then #5810/#5811. When #5813 is implemented,
confirm it landed as ONE contract change with the cross-entry-point parity test rather than four
separate patches — that is the specific failure mode of the previous fix arc. Re-run the UX panel
after #5810/#5811/#5812 land, and re-attempt the claude+vibe evaluators so the panel has ≥4.

---

## 2026-08-12 — Trend_Model_Project Collab-Deliverables corrective follow-up

**Source/automation**: user-requested reassessment of Collab-Deliverables PRs 61-65, using the GitHub
history for the original subsystem reviews and TMP response PRs #5440-#5507.

**Status**: evaluation complete; corrective list started; no GitHub issues or code PRs filed.

**Conclusions**:

- The three verified CLI helper copies were fully and effectively consolidated. PR 61 correctly
  recognized the shared module but incorrectly rated the work partial by treating five deferred
  compatibility delegators as copies.
- `_load_configuration` is substantively centralized for YAML through delegation; the
  `trend_model` wrapper adds TOML/CWD behavior. Mechanical three-to-one consolidation is not work.
- The colleague correctly resurfaced two real omissions: no `trend_model` retention/retirement
  decision and no lifecycle for six deprecated console commands.
- Legacy retirement was partial: PR #5490 removed the two orphaned runners, but active guidance
  still invokes the deleted module and fails; `src/cli.py` and the empty `trend_portfolio_app`
  package also remain unresolved.
- `_json_default` requires a caller/schema comparison before choosing a common policy; same names
  do not establish the same output contract.
- PR 62 correctly exposed several suggestions that the response process silently omitted. The
  bridge was implemented well and coverage gating was solved differently; legacy config migration,
  UI coercion policy, and threshold rationale remain real work. Naming is lower-severity, while
  validation-pass and class-cache deletion need proof first.
- PR 63 was the strongest follow-up. It correctly credited the threshold guard and shared boundary,
  and found genuine Parquet/date-column and documentation gaps (#5823 and #5822). The annualisation
  behavior itself was deliberate and regression-tested.
- PR 64 correctly found duplicate volatility scaling (#5820/#5829) and divergent TrendSpec behavior
  (#5821/#5830), but missed original entry-point feedback that remains unresolved: duplicate setup,
  duplicate risk-free assignment, and inconsistent fallback resolution.
- PR 65 correctly distinguished the weighting algorithms but incorrectly claimed scale factors were
  consumed correctly downstream. It also failed to credit completed metrics cleanup (#5496) or
  evaluate remaining robust-risk diagnostics, HRP traceback, and RollingCache warning suggestions.

**Artifact**:
`Code/Audits/Trend_Model_Project/2026-08-12-collab-review-corrective-work.md`.

**Next ledger action**: keep #5822/#5823 queued; deduplicate and format the newly confirmed items as
TMP issues only when the owner authorizes filing. Keep naming, validation/cache deletion,
frequency consolidation, serializer consolidation, dynamic binding, and public-API proposals
verify-first.

---

## 2026-08-12 — Trend_Model_Project two-round feedback reconciliation (completed)

**Source/automation**: user-requested Orchestrator review; Codex lead using `orchestrator` and
`repo-audit`, with completed read-only Gemini/Cursor/Vibe offloads and no Claude.

**Repo/commit**: `stranske/Trend_Model_Project` @ `ed1a0fa`, branch `phase-3`.

**Scope**: reconcile every suggestion from the original and follow-up Collab-Deliverables feedback
against current code and the corrective-work ledger. Produce a complete legacy-removal end state and
ordered plan. Compatibility is retained only when temporarily required to complete a current supported
surface; the repo has no active external userbase whose historic behavior needs preservation.

**Status**: completed; report/ledger only, with no issue filing or TMP code changes. The prior
corrective ledger was materially incomplete because it focused on PRs 61-65. The revised master
ledger disposes all 91 named first-round `Issues Found` items plus every substantive PR 61-65
finding. It credits effective work, records verified omissions, and rejects or defers mechanical
consolidations where contracts differ.

**Legacy-removal outcome**: direct removal after replacement capability is verified—port all MC
commands into `trend`, remove old config and CLI paths, delete compatibility scripts and
`trend_model`, delete orphaned/retired app surfaces, remove internal aliases/test hooks, and enforce
zero-reference plus wheel-content gates. No deprecation waiting period is required for hypothetical
users.

**Artifacts**:
`Code/Audits/Trend_Model_Project/2026-08-12-feedback-reconciliation-AUDIT_REPORT.md`,
`2026-08-12-feedback-reconciliation-verification-log.md`, revised
`2026-08-12-collab-review-corrective-work.md`, and three Orchestrator evidence artifacts.

---

## 2026-08-16 — trip-planner + Travel-Plan-Permission paired audit (completed)

**Source/automation**: user-requested; `repo-audit` skill + UX overlay + Orchestrator. Claude lead
(live UX driving, adversarial verification, synthesis only); all heavy reading offloaded to
gemini / cursor ×2 / codex.

**Repos/commits**: `stranske/trip-planner` @ `0d308b1`; `stranske/Travel-Plan-Permission` @ `156ada6`.

**Scope**: app + policy code only; `.github/` and Workflows-synced files excluded by owner decision.
Deliverables: report + UX review + filed issues (no `agent:*` routing labels).

**Entry state**: all 23 issues from the 2026-08-11/12 round closed; 0 open PRs in both repos.

**Headline**: the business-user journey **cannot be completed**. A user can sign up, create a business
trip, and compare scenarios, but cannot submit for policy evaluation and cannot print/export anything
for an approver. UX gate **FAIL**, panel median **2.1**, five severity-4 findings at 4/4 corroboration.
Root framing: acknowledged-incomplete work presented by the UI as complete
(`trip_planner/app/services/policy.py:186-188` says approval readiness is advisory "until submission
work lands"), plus **#696 was closed COMPLETED on 2026-04-10 while violating its own Non-Goal**
("Treating proposal lifecycle as backend-only state").

**Category coverage**: 1 code quality · 2 duplication · 3 wiring (centre of gravity) · 4 UX
(observed-only, full journey driven) · 6 partial (mined hints) · 7 partial. **Dimension 5 (field
comparison) and 8 (local automations) deliberately not covered** — 5 was dropped as non-actionable
until the P0s land; 8 was out of agreed scope. Both flagged in the report, not silently omitted.

**Verified FIXED (not re-filed)**: #1428, #1429a/b, #1434, #1677 (20,188px → 4,255px, guarded by a
regression test), TPP dead-policy-rule sweep found none. #1678 only **partially** fixed — the Policy
tab gained a CTA, but the CTA is inert, so the dead end moved rather than closed.

**Issues filed (4)**: trip-planner #1731 approval submission unreachable from the UI · #1732 production
proposal routes accept a caller-supplied TPP verdict · #1733 no print/export path exists ·
TPP #1456 blocking `cabin_class`/`third_party_paid` still pass on absent input.
**Commented, not duplicated**: TPP #1454 (workbook generated regardless of verdict) — confirmed still
reproducing with file:line mechanism.

**Not filed, pending independent verification**: the remaining gemini P1s (ignored TPP timeout config,
`provider=fake` crash, production services reading `tests/fixtures/state`, raw exception text from
`scenario_history.py`, non-finite ranking inputs) and the P2 hygiene set. They are in the report's
prioritized table; each was found by one agent and not yet hand-confirmed by the lead.

**Refuted this round**: "UX regressed 3.0 → 2.1" (different bundle scope, not a regression) · "Policy
tab is no longer a dead end" (code-reading conclusion disproved by driving it) · screenshot black band
(capture artifact) · `prepareApprovaln` "corrupted identifiers" (lead's own `rg -r n` flag error).

**Artifacts**: `Code/Audits/2026-08-16-AUDIT_REPORT.md` ·
`Code/Audits/trip-planner/2026-08-16-UX_REVIEW.md` · `2026-08-16-audit-run.md` ·
`2026-08-16-01-backend.md` · `2026-08-16-02-frontend-ux.md` ·
`Code/Audits/Travel-Plan-Permission/2026-08-16-03-sync-contract.md` · `2026-08-16-04-policy-core.md` ·
`Code/Audits/2026-08-16-issue-bodies/` · `trip-planner/2026-08-16-assets/`.

**Tooling note**: `dispatcher.py offload` rejects `--model auto`; two cursor jobs died instantly on it
and were re-dispatched without the flag.

**Next ledger action**: verify #1731/#1732/#1733/#1456 when implemented (inspect the squash diff and
the named test gates, and re-drive the journey — do not close on status labels). Owner decision
pending on whether to run dimension 5 as a focused follow-up.

### 2026-08-16 (same day) — post-audit PR verification pass

Verified by inspecting diffs, CI, and named test gates — not status labels.

- **TPP #1455 (MERGED, closed #1454)** — **genuinely fixed, but my #1454 comment was overstated.**
  #1455 gated the *user-facing* artifact path in `portal_review.py` (`_blocking_policy_codes()`,
  `if not policy_blocking_codes and generate_artifacts:`, "Artifact download blocked by policy
  verdict", +114 lines of tests). The `orchestration/graph.py:_spreadsheet_node` path codex flagged
  (S5) is still ungated, but no HTTP route reaches it — only tests and `cross_repo_smoke.py` (which
  imports `TripState` only). **Correction: codex S5 / my #1454 comment overstated severity by not
  checking which path is user-facing. #1454's closure is defensible.** Residual: the graph path
  remains inconsistent with the gated portal path — low severity, not filed.
  Note `origin/main` HEAD == `156ada6` == my audit base, so the audit already included #1455.
- **trip-planner #1734 (OPEN, for #1732)** — **strong.** Adds a default-off
  `TRIP_PLANNER_ALLOW_FIXTURE_TPP_RESPONSES` env gate, implements the exact specified gate
  `test_client_supplied_response_cannot_set_approval_ready` plus a second production test. All CI
  green (py3.12/3.13, ruff, mypy, complexity guard, cross-repo smoke, runtime CI). Ready to merge.
- **TPP #1457 (OPEN, for #1456)** — **RED, and the issue was half wrong.** Faithful implementation of
  #1456; CI fails 10+ `test_golden.py` cases incl. `[base]` + 2 directional. Root cause:
  `tests/baseline/catalog.yaml:38` encodes `third_party_paid: (none provided) -> pass`. Absent
  third-party payments is the normal compliant state, not missing evidence — the original
  `... or []` was correct. **My filing error**: the `third_party_paid` half came from automated sweep
  finding AUD-1429d that I did not hand-verify, unlike the rest of the round. Commented on both PR
  and issue: split it — keep `cabin_class` (further guarded on flight presence, else hotel-only/rail
  trips over-block), drop `third_party_paid`, do **not** rewrite the golden fixtures.

**Still open with no PR**: trip-planner **#1731** (approval submission unreachable) and **#1733**
(no print/export) — the two that actually block the business-user journey. Nothing has picked them up.

**Next ledger action**: merge #1734; get #1457 split and re-verify; re-drive the business journey once
#1731/#1733 land. Owner decision still pending on dimension 5 (field comparison).

### 2026-08-16 — P1 hand-verification pass (all five confirmed; two corrected)

Verified at trip-planner `9cd0155` by reading the live code and running proofs. **0 of 5 refuted** —
a materially better hit rate than the one cursor policy finding that was wrong (#1456). Two required
correction to mechanism or severity, so neither was filed as originally stated.

| Prior claim | Verdict | Correction |
|---|---|---|
| P1-4 `timeout_seconds` "completely ignored" | **CONFIRMED, downgraded** MAJOR→MINOR | Timeouts are **not** broken. `TPP_TIMEOUT_SECONDS` reaches the transport read-timeout via `client.py:202-206`, applied at 653/703. The `TPPRuntimeSettings.timeout_seconds` *field* has zero consumers — dead duplicate with a **conflicting default (10.0 vs 15.0)**. |
| P1-5 production reads `tests/fixtures/state` | **CONFIRMED, re-framed** | Real: `workspace_fixtures.py:41` + `budget.py:40`, live via `workspace.py:37-42`. But **not a live outage** — `render.yaml:6` uses `pip install -e .` so `tests/` ships in the deployed checkout. Bigger story: the workspace serves **canned fixture scenarios** ("Chicago runtime bundle", $1,160) rather than the user's trip — which is why the Compare tab looked so complete. |
| P1-6 `provider=fake` crashes | **CONFIRMED** | `_planner_chat_model` (`planner.py:1181-1183`) has no `fake` branch; always builds `_OpenAIPlannerChatModel`. Green only because `_PLANNER_CHAT_MODEL_FACTORY` is installed in tests. Config reports `status="ready"` then fails at use. |
| P1-7 raw exception text | **CONFIRMED** | `scenario_history.py:76-87` returns `_unprocessable(str(error))`, bypassing `public_http_error()` (`routes/errors.py:13`). Same family as closed #1687. |
| P1-10 non-finite | **CONFIRMED, mechanism corrected** | NaN does **not** propagate — runtime proof: `_clamp(nan) -> 1.0`, i.e. NaN becomes the **best possible ranking score**, so a NaN-metric scenario ranks first. `Field(gt=0)` **accepts `inf`**, rejects `nan`. Same family as closed #1693. |

**Issues filed (4)**: #1736 NaN→max score + `Field(gt=0)` accepts inf · #1737 `provider=fake` reports
ready then builds a real OpenAI client · #1738 production workspace/budget read `tests/fixtures/state`
· #1739 dead duplicate TPP timeout setting + raw exception text (P1-4 and P1-7 grouped; both MINOR
and localized).

**Method note**: the two corrections both came from asking "is the *field/effect* actually reached?"
rather than trusting the reported symptom — the same check that would have caught the #1456 error
before filing.

**Next ledger action**: #1731/#1733 still have no PR and still block the business journey. Merge
#1734; get #1457 split per the correction. Dimension 5 pending owner input.

### 2026-08-16 — Dimension 5 (field comparison + roadmap), completed

Owner-scoped: architecture validation then roadmap; comparison weighted to policy engines; two-repo
split open to challenge; web research allowed. Three web-enabled Orchestrator offloads; Claude lead
synthesis only.

**Headline: keep the two-repo split and the hand-written Python rules.** Corroborated independently by
gemini (policy-engine survey, 9 URLs — migrating to OPA/Cerbos/Cedar adds sidecar overhead and
decimal hazards without fixing the root flaw; confidence 92%, pivot only if non-developer policy
authoring becomes a requirement) and codex (topology — a merge is costly and does not improve
security). The expensive option was refuted, not recommended.

**Where the surveys disagreed, and the resolution**: gemini proposed a PEP inside trip-planner
(`Depends(require_policy_compliant_trip)` on mutation routes). Codex explicitly lists "requiring every
application route to call `evaluate()` before `submit()`" as **only a convention** — a future route,
job, or graph node can skip it, which is precisely the observed TPP failure where #1455 gated
`portal_review.py` while `orchestration/graph.py` stayed ungated. **Sided with codex**: authority must
be TPP owning `authorize-and-submit` plus the effect credential/capability, so trip-planner cannot
perform the action after a denial. gemini's PEP retained as defense in depth only. Codex is correctly
calibrated that this does not defend against a maintainer who redeploys all code.

**Correction to this audit's own finding P1-1**: I framed it as "policy sync discards enforceable rule
maps," implying the fix is to import TPP's caps. Codex is explicit that this is the **wrong fix** —
snapshots should be UX-only and labelled non-authoritative; copying caps creates a second source of
truth that drifts (same class as the 10.0/15.0 timeout defaults in #1739). P1-1 re-framed accordingly.

**Strongest convergence**: gemini's four-state verdict (`PASSED`/`FAILED`/`SKIPPED`/`MISSING_DATA`)
independently reproduces the distinction this audit hit the hard way — #1456's `third_party_paid` half
was wrong because the model cannot express "none provided" (SKIPPED) vs "unknown" (MISSING_DATA), and
PR #1457 reddened 10+ golden cases proving it. Field survey + live regression agreeing = highest
confidence, lowest cost recommendation of the audit.

**Approval-packet spec** (cursor, 60 URLs): 15-section document, placement rules for verdict/rule
ids/costs, four export surfaces. Two build-shaping findings: policy feedback belongs at
point-of-selection (dominant vendor pattern), and submit must freeze an immutable content-hashed
snapshot (dovetails with codex's hash-bound decision record).

**Issues filed (2)**: TPP **#1458** four-state verdicts (supersedes the `third_party_paid` half of
#1456, unblocks #1457) · trip-planner **#1740** per-scenario policy violations on Compare.
**Comments added**: #1731 (re-scope to `authorize-and-submit`; do not copy caps) · #1733 (packet spec
+ sequencing behind #1738).

**Recommended build order**: #1458 four-state → merge PR #1734 → #1738 real scenarios → #1731
authorize-and-submit → #1733 packet/print → #1740 point-of-selection.

**Confidence limits recorded in the synthesis**: "keep the split" is two-source corroborated; the
`authorize-and-submit` capability design is single-source and worth a second opinion on token
mechanics; the packet spec is generic vendor practice, not a specific compliance standard; none of
Dimension 5 was validated against a running system.

**Artifacts**: `Code/Audits/2026-08-16-D5-SYNTHESIS.md` ·
`Travel-Plan-Permission/2026-08-16-D5-policy-engines.md` · `.../2026-08-16-D5-architecture.md` ·
`trip-planner/2026-08-16-D5-approval-ux.md`.

**Tooling note (repeat offense)**: codex's offload was again pointed at the Dropbox Audits path and
returned `OFFLOAD_INCOMPLETE: requested audit destination is not writable`. This gotcha was already
recorded in this same run's `2026-08-16-audit-run.md`. Re-dispatched with `./audit-out/`. Cost: one
wasted run.

**Next ledger action**: #1731/#1733 still have no PR. Merge #1734; split #1457 per the correction;
re-drive the business journey once #1738/#1731/#1733 land.

### 2026-08-16 — Plan-tab functional pass (coverage gap closed, on owner challenge)

The owner asked whether the Plan tab itself had been evaluated. It had **not**, properly. The original
UX pass measured Plan's *structure* (4,255px, inert NEXT ACTION, readiness card, tap targets) but never
exercised its *function* — no planner message sent, no prompt chip clicked, no planning mode changed —
while the coverage ledger recorded `driven: true`. Gap closed by re-driving the running app.

**F6 (severity 4) — the fallback planner ignores user input entirely.** Two materially different
messages ("Cancel this trip. I do not want to travel at all." vs "zzzz qqqq wwww nonsense tokens
12345") return **byte-identical** replies (`a === b` → `true`). `POST /planner/{trip}/turns` returns
200 with `runtime.mode = "fallback"`, the message count increments, and the reply renders like a real
answer — nothing tells the user their message was not read. Asked for "cheapest compliant options",
the reply contains **no cost figure** (despite $1,160/$1,280/$1,400 on screen) and never mentions
policy or approval. Copy carries developer vocabulary ("mounted planner options", "workspace route",
"trip frame"), a malformed choices sentence, and an "N transfers" pluralization bug.
Filed **#1742**.

**F7 (severity 2) — planning mode is cosmetic.** All four modes persist correctly
(`PUT .../planning-mode` → 200) and swap the guidance copy, but produce the same planner template.
Folded into #1742.

**Credits found in the same pass**: the seven prompt chips are well designed — they prefill good
composer stubs ("I decided to ", "Compare the strongest route options and tell me the main
tradeoffs."). My first reading (zero network calls, no DOM change) looked like breakage; checking the
composer showed correct prefill-then-send design. Recorded so a future round does not "fix" them.

**Retraction — secondary defect S6 was wrong.** The report claimed "repeated 401 Unauthorized errors
**while the user is authenticated**". Re-checked with error-filtered console during an authenticated
session: none. The 401s were the normal unauthenticated session probe on the login/signup page.
**S6 withdrawn**; it was never filed, so no issue needs correcting.

**Method lesson**: `driven: true` was recorded for a surface where only layout was inspected. Future
UX passes should record *which interactions* were exercised per surface, not a boolean — a structural
pass and a functional pass are different evidence.

**Next ledger action**: unchanged — #1731/#1733 still have no PR; merge #1734; split #1457.

---

## 2026-08-23 — Trend_Model_Project GUI/runner + configuration surface (scoped, completed)

**Repo/commit**: `stranske/Trend_Model_Project` @ `f6d5582d`, branch `phase-3` (the repo default).
**Source**: Claude Opus 5 running the `repo-audit` skill headless. No scoping interview — scope was
pre-decided by the caller, and that decision is recorded in `2026-08-23-audit-run.md` along with the
four judgement calls made without asking.

**Why this scope.** The repo is 246 MB with 641 test files, and it had already been audited earlier the
same day on the feedback-completion ledger. Re-auditing that finds nothing. The GUI/runner +
configuration surface had not been covered by that round, and the notebook `gui/app.py` surface has
never had rendered evidence in any round.

**Headline.** The dominant defect class identified on 2026-08-11 — *"two paths, one contract"*, a fix
applied to one entry point rather than to the rule — is unchanged, and it has migrated into the
operator surface. Five of six findings are exactly that shape. The most striking is that the shipped
default configuration produces a report which simultaneously claims *"Target volatility 10.0%"* and
*"Signal scaling Raw"*: `unified.py:475-483` reads the raw config ungated, while the sibling helper
50 lines earlier gates on the effective spec and gets it right. The mechanism traces to a single empty
mapping — `config/defaults.yml:50` is `signals: {}`, and `spec.py:168` treats falsy `signals` as
"no signals", discarding the whole `vol_adjust` section.

**The most consequential finding for a user of the tool** is #5984: `analysis_runner.py` validates
transaction costs in basis points as a float (`:408-409`) and then builds the config that actually runs
with an int truncation (`:258,281`), in the same module. `half_spread_bps: 0.5` validates as 0.5 and
executes as **0** — a configured cost silently becomes no cost, so reported net performance is better
than the model the user set up.

**Why the suite did not catch two of them.** `tests/test_gui_app_extended.py:57-67,315-322` replaces
`widgets.Dropdown`, `Checkbox`, `ToggleButtons`, `Button` and `VBox` with dummy classes;
`DummyDropdown` accepts any `value` without checking option membership. Widget-level contracts are
therefore structurally invisible to the GUI test suite. Recorded in #5985 so the fix cannot repeat it.

**Three claims in the brief that commissioned this audit were stale or false**, and are recorded as
declined rather than filed: `gui/runner.py::_run_folder_name` no longer exists anywhere in the tree;
`_compute_stats` has no `periods_per_year` default and all 17 call sites pass it explicitly (refuted
by the cursor offload, which prevented a false issue); and `trend.input_validation` now delegates to
the canonical date engine, with the remaining copy relocated to `csv_validation.py`.

**Offload calibration re-confirmed the repo README's prior observations exactly.** gemini was
strongest but severity-inflated — one `[BLOCKER]` refuted outright by `lint_keys.py:158-176`, and an
11-row "inert keys" table with a ≥18% false-positive rate (two rows refuted by one grep each), so the
table was dropped rather than filed. vibe was thorough but filed one finding twice as two
`[BLOCKER]`s and constructed no divergent input; I tried to build one and failed, so it is
`INSUFFICIENT_EVIDENCE`. cursor filed 0 BLOCKER / 2 MAJOR / 4 MINOR and every claim held.

**Evidence standard.** CI on this branch shows `skipped` and `action_required` runs, so full-CI green
was never treated as proof. Each of the four gates was run as an exact node id before and after a
minimal patch, and then re-verified independently by `local_verify.py --base-ref f6d5582d`, which
returned `verdict: PASS` ("candidate tests pass live and fail against the base implementation") for
all four. Every patch was reverted and the scratch clone confirmed clean. Nothing was pushed and the
canonical Dropbox checkout was never touched.

**Capability-selection experiment (second deliverable of this round).** This audit doubled as a test
of the Orchestrator capability advisor, consulted via the CLI once per phase and once per dimension:
11 consults across 9 surfaces, 13 distinct capabilities offered, `dispatch_ready` false for every one.
**5 used** (`offload`, `deliberate-break-verifier`, `adversarial-review`, `capability-propensity`
useful; `repo-playbook` not-useful), **4 declined with stated reasons**, 4 ignored as keyword leaks.
Full per-consult record: `Trend_Model_Project/2026-08-23-capability-evidence.md`.

Three findings from that experiment worth acting on:
1. **The keyword classifier fires on grammatical tokens and against the surface's intent** — `pytest`
   inside "collect the pytest node ids" bound test-authoring capabilities at a bash-only phase;
   `implement` inside the noun "implementation" bound `codemod-campaign`, a code-*mutating* lane,
   inside a read-only audit; `cross-repo` inside "cross-repo audit ledger" bound a coordination lane
   for a file write. In all three the declared surface was right and the classifier was wrong.
2. **`repo-playbook` and `frontend-verifier` were offered in the same response and contradict each
   other for this repo.** This repo's own audit README records `frontend_verify.py` as unreliable
   against its Streamlit SPA; the playbook does not carry that gotcha, and `frontend-verifier` was
   recommended twice. The playbook also gates its useful entries behind `task_type`
   `implement`/`testgen`/`mechanical`, so a `review` or `audit` consult sees 308 characters — one
   clause of which ("cuts from phase-3, not the default branch") is factually wrong, since `phase-3`
   IS the default branch. **Cheapest high-value fix: ingest each repo folder's "Standing notes for
   the next round" into `repo_knowledge`, and stop task_type-gating gotchas.**
3. **Propensity carried information exactly once.** 11 of 13 candidates sat at the uninformative 0.5
   floor with zero usefulness evidence. The missing input is not more consults but **declines** —
   four of nine decisions this round were reasoned rejections and none is learnable from the ledger,
   because there is no way to record "offered and rejected on repo-specific grounds".

Also observed, and worth fixing in `adversarial.py`: with `n_reviewers: 1` and `veto_threshold: 2`
(vibe returned null), `aggregate_veto` reported `verdict: "PASS"` while carrying a `high`-severity
0.99-confidence blocker. The threshold becomes unreachable once the reviewer population shrinks below
it, and the failure presents as PASS — as silence. Per the workspace latched-gate rule, reporting the
drainable quantity alongside the blocking one (`1 veto / threshold 2, reviewers returned 1 of 2`) is
the durable fix.

**Artifacts**: `Code/Audits/Trend_Model_Project/2026-08-23-{AUDIT_REPORT,verification-log,audit-run,capability-evidence}.md`,
`2026-08-23-01-config-wiring-gemini.md`, `-02-annualization-cursor.md`, `-03-validation-vibe.md`,
`2026-08-23-issue-bodies/` (5), `2026-08-23-assets/` (5 gate tests, adversarial prompt + raw result).

**Next ledger action**: verify #5984-#5988 against squash diffs and the named test gates rather than
issue status — the 2026-06 arc closed 51 issues here with several fixes only partially applied. Then
work the 7 deferred rows in the verification log, beginning with the two that need only a
weekly-frequency fixture.

---

## 2026-08-23 - Workflows: template-sync / consumer-contract surface (focused)

**Source**: `repo-audit` skill, headless non-interactive run, scope pre-decided (no scoping interview).
**Base**: `stranske/Workflows` @ `451b609` ("fix(sync): typecheck manifest docs helpers (#3176)"),
fresh depth-200 clone on local disk. **Nothing filed, changed, or dispatched.**

**Scope**: `templates/consumer-repo/**`, the sync scripts, `.github/sync-manifest.yml`, the
`health-6x/7x` gates, the registered-consumer-repo list, and the docs that state the contract.
Out: keepalive round/concurrency internals (covered 2026-08-12) and open PR #3170.
Chosen because `Code/CLAUDE.md` flags root-vs-template drift as a known defect class and the prior
Workflows round covered a different area. All 8 categories were re-run against this surface;
dimension 4 is recorded as an operator-legibility review with an explicit coverage note, since this
repo has no application front end.

**Headline.** Three independent mechanisms had to all be blind at once, and each was verified by
running it. `check_template_drift.py:210` globs only `agents-*.yml`, so 7 of the 25 basenames shared
between the root and consumer-template workflow trees have no root-vs-template gate — 4 of them
genuinely differ (148/154/81/22 lines). `check_consumer_sync_drift.py:1009-1013` skips every
`create_only` entry, which is exactly the population `maint-68` refuses to overwrite — 68
file-positions neither converged nor measured, including the consumer Gate and the consumer CI entry
point. And `health-68-consumer-sync-drift` has produced **400 consecutive `action_required` runs with
zero executions since 2026-07-31T16:30Z**, while its three sibling health gates run normally, so the
open drift tracker #2210 has been frozen for 23 days. Measured live consequence: `pr-00-gate.yml` is
**195 lines in Pension-Data and Ready, 196 in Manager-Database, 199 in Counter_Risk, 315 in
trip-planner, 408 in Trend_Model_Project — against a 1,130-line canonical template**, in the workflow
whose green result keepalive requires before it will drive any agent PR.

A fourth defect explains the invisibility: `sync_manifest_compiler._source_candidates` resolves a
manifest `source` against the consumer template tree **and then silently against the repo root**, so
deleting a template file converts into shipping the Workflows-internal file to all 14 registered
consumers. Demonstrated for `reusable-pr-context.yml` with all four local guards exiting 0.

**Category coverage and main findings.** (1) code quality: the silent root fallback, the narrow drift
glob, and a `WORKFLOWS_ONLY` name list with 2 dead entries and 2 that contradict the manifest — the
contradiction is what makes the fully-unguarded case possible. (2) duplication: 25 shared basenames,
but the actionable problem is coverage, not divergence — 8 of 16 allowlist reasons say aligning would
strip the consumer action-pin security contract, so **no consolidation campaign is recommended**
(prove-before-delete). (3) wiring: the `create_only` measuring-window/draining-window mismatch; the
manifest still routing readers to issue **#2158, closed 2026-05-25**, on a line rewritten 71 days
after closure; three independent fleet literals of which `cleanup_labels.py:228` has already drifted
to 7 of 14. (4) operator legibility: `DURABLE_TRACKING_ISSUES.md:78` prescribes exactly the right
liveness oracle ("confirm liveness from the workflow run history, not from tracker activity") and it
has no implementation — applying it by hand is what found the outage. (5) field comparison: copy-and-PR
with hash comparison buys byte-level certainty and nothing else; this repo pays every cost of that
model and exempts its most important files from the comparison. (6) missed opportunity: a fleet
`repo x target -> delivered template_hash` table is one join from the `sync-pr-delivery-record/v1`
markers `maint-68` already writes, and is the instrument that would have shown the Gate fragmentation
without any remote probing. (7) tools: `actionlint`/`zizmor`/`semgrep`/`scorecard` are all already
installed — declined proposing any; JSON-Schema for the manifest input noted as low-priority.
(8) automations: the 16-pair fingerprint allowlist changed 25 times in the 18 days to 2026-08-22, but
20 of 25 arrived as merged agent PRs, so it is **agent-borne, not owner-borne** — the finding is that
one `reason` field conflates "fingerprint refreshed" with "divergence re-reviewed", so the audit trail
asserts review that did not occur. Zero owner steps are proposed anywhere in this round.

**What the adversarial pass killed.** Three candidates died and one inverted into a stronger finding.
Dropped: "deleting any consumer template goes unnoticed" (too broad — `--strict` completeness catches
most names; survives only for the intersection of two blind spots); "an empty registered-repo list
no-ops the fleet" (2 of 4 callers verified to fail closed, downgraded to P3); "the sync-failure tracker
under-reports the fleet by one repo" (dropped entirely — `stranske/Orchestrator` was registered
2026-08-21, five days after that issue body was written). Inverted: I expected #2210's staleness to be
an undocumented trap; the repo documents it explicitly, which turned the finding into "the prescribed
oracle is unimplemented".

**Evidence standard.** Workflows CI shows `action_required` runs, so no workflow result was treated as
proof. Every P0/P1 came from running a command and recording its exit code: three break/revert
experiments in a throwaway clone (a table of which guard catches which deletion is in the report), plus
one machine-verified test gate — `local_verify.py` returned `verdict: PASS` ("candidate tests pass live
and fail against the base implementation") for the widened drift glob, green rc 0 / red rc 1. Live
claims came from `gh` reads only. Both clones ended `git status --porcelain` empty; the canonical
`Code/Workflows` checkout was never written to; the Orchestrator repo was untouched and
`orch-sync-mirror.sh` was not run; zero GitHub mutations.

**Staged, not filed.** 5 AGENT_ISSUE_FORMAT bodies in `Workflows/2026-08-23-issue-bodies/`, all 5
passing the enforced Definition-of-Ready lint (`Code/Audits/issue_lint.py`). Two of their named gates
**fail against the live tip today** (`test_no_second_consumer_repo_literal`,
`test_every_pair_states_its_divergence`), which is the strongest available form of the demonstration.
Filing is the owner's decision; this round created no issue, PR, comment, label, or dispatch.

**Out of scope but recorded, not dropped**: besides `health-68`, roughly a dozen Workflows workflows
show 100% `action_required` over recent runs (`agents-63-issue-intake`, `agents-auto-label`,
`agents-dedup`, `agents-decompose`, `agents-capability-check`, `agents-issue-optimizer`,
`agents-bot-comment-handler`, `agents-autofix-loop`, `agents-moderate-connector`, `maint-46-post-ci`,
`maint-62-integration-consumer`). Last-real-run dates are **staggered** (2026-07-24, 07-31, 08-06,
08-11) and their triggers differ, so this is not one setting flip. P0-shaped; belongs to its own round.

**Capability-selection experiment (second deliverable).** 14 consults across 14 surfaces, 22 candidate
offers, `dispatch_ready` false for every one. **2 used** — `offload` (cursor produced the dimension-5
field brief; it supplied the framing that merged two findings into one root cause) and
`deliberate-break-verifier` (`local_verify.py`, which both proved the gate discriminates and surfaced a
cost my by-hand plan had missed). **20 declined with stated reasons.** Four findings about the advisor
itself:

1. **`repo-audit:phase-1`'s deliberately-empty binding is byte-identical to a classification failure.**
   `capability_advisor.py:486-490` says in as many words that "silent absence and deliberate emptiness
   must not look alike -- that is this repo's founding defect", and declares `NO_BINDING` with a
   rationale. The JSON carries none of it: phase-1 and a control consult on a nonexistent surface, given
   the same task text, returned the identical `reason` string. The advisor *has* the vocabulary — other
   surfaces return "N capability(ies) are DECLARED for surface X and apply regardless of classification"
   — it just never says "declared empty".
2. **`frontend-verifier` is offered unconditionally to a repo with no front end** (twice). Its own
   binding reason is conditional ("when observable surfaces exist"); nothing evaluates the condition.
   **This independently replicates the same complaint from today's Trend_Model_Project round.**
3. **The nearest-named capability was filtered out by entry mode.**
   `capability:reference-sync-hygiene-test-gate` appeared in `not_applicable` for an audit *of sync
   hygiene*, excluded as `compiled_workflow_not_in_trigger`. Not a bug, but the exact false negative
   dimension 8 exists to surface.
4. **Propensity is instance-global, so movement during a run is not attributable to the run.** `offload`
   moved 0.5 -> 0.6667 before I recorded anything, and two identical back-to-back probes returned
   identical values, so consulting alone does not move it. Any reading of these numbers as this audit's
   result would be wrong.

Weakest bindings were `dimension-4` and `dimension-8`, and both share one cause: the capability is
scoped to the Orchestrator's own runtime while the audit target is another repository. An
`applies_to: self | audited_repo` axis on the binding table would remove most of this round's noise.

**Artifacts**: `Code/Audits/Workflows/2026-08-23-{audit-run,00-repo-map,01-drift-guard-coverage,02-wiring-and-gates,03-operator-legibility,04-field-and-opportunities,05-local-automation-attention,AUDIT_REPORT,verification-log,capability-evidence}.md`,
`2026-08-23-issue-bodies/` (5, lint-passing), `2026-08-23-assets/` (the cursor offload brief + its prompt).

**Next ledger action**: owner decision on filing the 5 staged bodies. If filed, sequence
`02` (one accumulator - largest change in reader understanding) -> `04` (one glob + 4 written
rationales) -> `01` (root-cause the approval state, restore the schedule, wire the liveness assertion)
-> `03` -> `05`, then the fleet-generation table as the one genuinely new capability. Separately, open
a round for the staggered `action_required` cohort.

---

## 2026-08-23 — Fine-Art-Archive, display-surface audit (report + staged bodies; nothing filed)

**Source/automation**: `~/.claude/skills/repo-audit` (SKILL + playbook + orchestration + audit-storage
+ ux-review-overlay, all read in full), phases 1-5, headless agent seat, **no agent fan-out** — scope
was one subsystem (~5k LOC), so `orchestration.md`'s own warning against unscoped fan-out applied.
**Base**: `6b45762` (remote tip), fresh scratch clone at `/private/tmp/.../scratchpad/faa`; the
canonical `Code/` clone was never touched and the Orchestrator repo was neither edited nor synced.
**Scope**: display / presentation surface + its data pipeline — `api/` (43 routes), `ui/`, `display/`,
`eink/`, `design-system/`, `scripts/render_weekly_review.py`, `make_review_thumbs.py`,
`make_eink_card.py`, and the manifest/store feed path. Excluded: metadata completeness (own driver),
the 4 open `tracker:durable` issues, `.github/scripts/*.js` (synced from Workflows).

**Category coverage**: 5 of 8 dimensions fully, 3 partial, **1 not covered** (dimension 5, public
field — the `offload` fan-out it needs was declined for time; recorded as a deferred opportunity, not
as low value). Stated in the report rather than implied.

**Main findings by category**

- **Wiring / correctness (P0)** — `/healthz` returns `ok:true` when `manifest_loaded == 0` over a
  populated archive (`api/main.py:200`). Measured: `ok:true` at 0/3411, `ok:false` at 1/3411. The
  endpoint is more alarmed by losing all-but-one work than by losing all of them. **Nothing in the
  repo writes `manifest.csv`** (all references are reads; the file is uncommitted), so that is the
  default state of a fresh deployment. A **latched-gate instance of the family in the global rules**:
  it fails toward silence, and the quantity that would clear it (`sidecar_works`) is already in the
  same response, unread. The allowance is deliberate but its own rationale is narrower than its
  implementation — `tests/test_healthz_manifest_drift.py:76-93` pins it with a fixture of exactly ONE
  sidecar, and `:95-111` proves the authors applied the identical reasoning to the *other* operand.
- **UX / correctness (P1)** — the weekly decision page promises "Every number below was measured on
  your Mac" (`render_weekly_review.py:564`) and renders 4 blocks that break it: a two-branch
  `if grant == "G41" ... else` gives **every** other grant G47's scope verbatim (`:163-165`, observed:
  G99 rendered with G47's string); two frozen literals (`:279`, `:329`); and a hardcoded table
  asserting **four CLOSED issues** are "filed ... tracked" (`:336-352` — #406/#407/#409 closed
  2026-08-08, #408 closed 2026-08-15, renderer merged 2026-08-18), with row 408 mixing a **live**
  interpolated count against a **frozen** status so the staleness is invisible. The guard that would
  catch all of it, `evidence_title()`, is in the same file at `:36-52`, applied to 5 of 9 sites.
- **Quality / tooling (P1)** — `tests/test_weekly_review_thumb_paths.py` executes **no line** of the
  two scripts it is named for; two of three tests assert string ops on literals defined in their own
  bodies, coverage 0.00%. Verified twice: reintroducing the exact #561 defect leaves `3 passed`, and
  `local_verify.py --base-ref cc68a88~1` returns `1 failed, 2 passed` against a tree containing
  **neither script**.
- **Wiring / opportunity (P2)** — #549's `select_quality_diverse` is unreachable from any screen:
  `einkSpec()` at `ui/index.html:2086-2102` builds 10 spec keys and not `selection_mode`, default is
  `"ordered"`. Its `SelectionDiagnostic` explanations are computed, returned, and rendered by nothing.
- **Recorded, not filed (P3)** — `docs/reports/weekly_review_<date>.json` has **no producer anywhere**.
  The "weekly" page is a one-shot snapshot shipped as a recurring renderer, which is the single fact
  that explains both P1s. Not filed: producer is outside the repo, so an issue citing it would fail an
  addressability gate (the class that stalled #409 into `needs-human`).
- **Dimension 2 negative, recorded deliberately** — one palette fitter, one strategy chooser, one
  selector. Nothing to consolidate, which is why `codemod-campaign` was declined. #548's chooser was
  wired end to end on arrival. This is not a repo that fails to connect things.

**Non-actionable / refuted**: 5 candidates dropped by my own verification **before** the reviewers saw
them — `design-system/` is not dormant (`PRESENTATION_PATTERNS.md:96` plans graduation into the
Workflows consumer-repo design system; prove-before-delete, same trap as the refuted "delete
`display/`" thesis); the exhibition selector *does* have a caller (`playlist.py:419`) so the finding
narrowed to "no screen can request it"; `weekly_decisions_<date>.json` having no consumer is an
intentional human handoff; two `/healthz` mis-readings of my own. Plus 2 unfiled minors (link-as-button
header, unbounded weekly scroll). Adversarial pass: **2 reviewers, 4 claims, ZERO refutations**, and
both reviewer-supplied citations were re-verified by hand before use.

**Issue/PR links**: none. 4 bodies staged at
`Code/Audits/Fine-Art-Archive/2026-08-23-issue-bodies/`, all 4 `PASS` under `issue_lint.py`. Filing is
the owner's call.

**Capability evidence — this run was the POSITIVE CONTROL for two open ledger complaints.**

1. **`repo-audit:phase-1` suppression confirmed live** (`advice:4441f1f71230`): `capabilities: []`,
   `confidence: "suppressed"`, and a `reason` that quotes the playbook's own *"Orient (bash only, NO
   agents)"*. First run to observe the fix. It does not merely return empty — **it says why**, which is
   the exact remedy the 2026-08-23 Workflows round asked for when it found phase-1 and a nonexistent
   control surface returning identical reason strings.
2. **`frontend-verifier` — the open complaint is now answered from the other side.** That same
   Workflows entry recorded it "offered unconditionally to a repo with no front end (twice)... nothing
   evaluates the condition." Here, on a repo that genuinely has a display surface, it was offered with
   `usefulness_evidence_count: 0` and **earned its first resolved positive verdict**: `--doctor
   --start-browser` went ready first try, and the rendered aria snapshot produced finding F2, which
   the code read had **not** — it put the page's provenance guarantee and three unmeasured claims in
   one observed document. **So the binding is not wrong, it is unconditional.** The fix is to evaluate
   the condition, not to weaken the binding — the value when it does apply is the highest of any
   capability used this run.
3. `adversarial-review` (0.75, 2/2) — 2 reviewers, zero refutations, and it **added** two `file:line`
   citations I had not established (`ui/index.html:2086-2102`, the spec-build site that closes F4 from
   the UI side; `render_weekly_review.py:564`, the banner line), plus independently cited
   `test_healthz_manifest_drift.py:76-93` as the test that *pins* F1 — the strongest single fact in
   issue body 01. codex independently ranked F1 "most serious", matching my own ranking.
4. `deliberate-break-verifier` (0.75 -> **0.80 within this run**, re-offered first at the next
   surface) — sharpened F3 past what my own hand-break could prove. **Limitation recorded:** the
   verdict is per-test-**file**, so it returns `PASS` on a file where 2 of 3 tests are tautologies,
   because one real assertion satisfies the adjudication. Per-test granularity would return
   `FAIL_HOLLOW`. Also, a first run with `--base-ref HEAD~3` returned `FAIL_HOLLOW` for the
   uninteresting reason that the base already contained the code under test — the tool does not warn.
5. `repo-playbook` — returned an FAA-specific rule that changed the scope boundary I wrote down, and
   is the direct counter-measure to the failure mode behind 11 of the 18 refutations in 2026-08-08.
6. **22 declines, each with its reason, in a parseable table** in the evidence log. Dominant class
   (8 of 22): **scope too small to offload.** `offload` was offered at 9 of 12 surfaces and declined at
   all 9 for the same structural reason — it is declared surface-wide, so on a one-subsystem audit it
   generates near-zero-information offers. Second class (4): the capability audits the **Orchestrator's
   own runtime** while the target is another repo (`capability-activation-audit`,
   `capability-firing-monitor`, `switch-review`, `runtime-ac-checks`) — which **independently
   replicates** the `applies_to: self | audited_repo` axis proposed in the 2026-08-23 Workflows entry.
   Third class (3): `testgen-lane` matched correctly all three times and was structurally impossible,
   because the run's deliverable is staged bodies, not commits — **"correct match, no landing zone" is
   worth distinguishing in the ledger from "wrong match"; they imply opposite fixes.**

**Artifacts**: `Code/Audits/Fine-Art-Archive/2026-08-23-{audit-run,AUDIT_REPORT,UX_REVIEW,capability-evidence,verification-log}.md`,
`2026-08-23-issue-bodies/` (4, lint-passing), `2026-08-23-assets/` (`bundle.json`, 3 screenshots,
`adversarial-refutation.json`).

**Next ledger action**: owner decision on filing bodies 01-04. If only one is filed, file **01** —
smallest change (one condition), largest blast radius, and the only finding whose failure mode is
silence. Then 03 before 02, since 02's four blocks shipped *because* 03's gate does not execute.
Separately: dimension 5 (public field) is uncovered and is the cheapest remaining value here.

## 2026-08-24 — implementation verification of the ten issues filed 2026-08-23 (both repos, completed)

**Skill**: `implementation-verification`, run alone by explicit instruction (concurrent writers
destroyed capability-ledger attribution in the prior round, so this run was the only ledger writer).
**Targets**: `stranske/Trend_Model_Project` #5984-#5988 and `stranske/Workflows` #3179-#3183 — all ten
closed as COMPLETED overnight, none verified. **Bases**: TMP `HEAD d3069d87`, Workflows `HEAD a377fd30`.
**Nothing filed**; 4 lint-passing bodies staged under `2026-08-24-issue-bodies/`.

**Method.** The real squash diff of every merge commit read from local git (`git show <merge-sha>`) —
never the PR body. Each acceptance task checked at its cited `file:line`. Every named gate collected
(`pytest --collect-only`) to test the node-id *exists*, then run. Every shell-level acceptance
criterion executed for its exit code. Live GitHub state read for the runtime criteria. All test runs
performed in `git archive` extracts under the scratchpad — no canonical clone under `Code/` was
mutated and `orch-sync-mirror.sh` was not run.

### Result: 8 delivered, 1 NOT delivered, 1 partially delivered

| Issue | PR | Verdict |
|---|---|---|
| TMP #5984 fractional cost bps | #5989 | delivered; named gate **renamed** (AC node-id absent), 14 tests not the 8 the AC specified |
| TMP #5985 export-format dropdown | #5990 | delivered; small regression — a scalar-string `formats` now yields `['xlsx']` where it used to yield `['csv']` (schema-invalid input, low severity) |
| TMP #5986 phantom Target volatility | #5991 | **NOT DELIVERED** |
| TMP #5987 silent Run button | #5992 | delivered; 10 unrelated files of import churn outside the declared scope |
| TMP #5988 three turnover ceilings | #5993 | delivered; Non-Goal breach — runtime engine changed and an existing `max_active_positions` assertion weakened to `max_funds` |
| WF #3179 Health 68 execution (P0) | #3189 | delivered; the 23-day outage is over |
| WF #3180 report `create_only` positions | #3190 | delivered; AC-evidence gap + one AC bullet genuinely unmet |
| WF #3181 no silent root-tree fallback | #3193 | delivered; AC-evidence gap; residual fallback retained by design in `resolve_source_path` |
| WF #3182 drift pairs for every basename | #3194 | delivered; AC-evidence gap; collateral loss of 2026-08-23 incident records from 5 allowlist `reason` fields |
| WF #3183 self-checking sync rationales | #3203 | **PARTIALLY DELIVERED** |

**All ten PRs merged with ZERO failing checks** (TMP 27-31 pass, WF 49-58 pass). The
`autofix-versions.env` breakage named in the brief is not implicated anywhere — no red result had to
be attributed. **No owner "do not merge as-is" / rework comment exists on any of the twenty
artefacts.** So green CI plus a clean review history carried no information about acceptance, which
is the entire reason this pass exists.

### The finding: TMP #5986 shipped the inverse of its acceptance criterion

The issue required the volatility rows gated on the **effective trend spec's** `vol_adjust`. What
merged gates them on the **raw config flag** — `src/trend/reporting/unified.py:481`,
`portfolio_vol_adjust_enabled = _get(vol_adj, "enabled") is not False`. The required helper
`_resolve_effective_trend_spec` was added at `:354` and is called at `:480`, and **its result is never
used for the gate**. Re-measured first-person at HEAD with the shipped `config/defaults.yml`:

```
'Signal scaling'      = 'Raw'      'Target volatility' = '10.0%'
'Floor volatility'    = '4.0%'     'Warm-up periods'   = '0'
spec.trend.vol_adjust = False      -> DEFECT STILL PRESENT
```

Byte-identical to the block the issue was filed against. And the gate was **inverted, not omitted**:
`test_param_summary_omits_vol_targets_when_scaling_is_raw` does not exist; in its place
`test_param_summary_reports_portfolio_vol_targets_when_scaling_is_raw` asserts
`Signal scaling == "Raw"` **and** `Target volatility == "10.0%"`. A second test in
`tests/test_report_effective_trend_spec.py` pins the same contradiction. **The follow-up must delete
an asserted test**, which is why this needs its own issue rather than a re-fix.

**Two findings, not one.** The mechanism is recorded in the PR itself — a closer comment says
parameter reporting now treats `vol_adjust.enabled` as the switch *"independently of signal-scaling
status"*, i.e. an in-PR review finding overrode the issue's named criterion. And **the correct verdict
already existed inside the PR and did not block it**: #5991's Provider Comparison Report recorded
`openai/gpt-5.6-terra` **CONCERNS at 94% confidence, correctness 6/10** — *"it does not implement the
acceptance criterion's required gate"* — while `anthropic/claude-sonnet-5` said PASS at 68%. The PR
merged and the issue closed COMPLETED. **That is a fleet verdict-disposition gap: a 94%-confidence
CONCERNS naming an unmet AC neither blocked the merge nor reopened the issue**, and it is the more
systemic of the two problems.

Independently adjudicated: `adversarial.review(reviewers=['vibe','cursor'])` was asked to **refute**
the not-delivered verdict. Neither could; both confirmed it with their own citations. `BLOCKED`,
2 vetoes / threshold 2, confidence 1.00 and 0.97.

### WF #3183: the field split re-created the claim it was built to remove

The split into `divergence` / `divergence_reviewed` / `fingerprint_refreshed` exists because one
`reason` field asserted human re-review whenever a mechanical hash refresh happened. What shipped
stamps **the same date in both new fields on all twenty pairs**, and the coupling already survived a
day of traffic: `{divergence_reviewed: {2026-08-23: 19, 2026-08-24: 1}}` and
`{fingerprint_refreshed: {2026-08-23: 19, 2026-08-24: 1}}` — the one pair whose fingerprint moved had
its review date moved with it. Nineteen pairs now assert a 2026-08-23 review while their own prose
dates the judgement to 2026-06-20 / 2026-06-30 / 2026-07-14 / 2026-08-05. The gate
(`test_every_pair_states_its_divergence`) only asserts the strings are non-empty, so it cannot see any
of it. Secondary: the named live gate `test_manifest_issue_references_are_open` is vacuous — it
iterates only `open:` citations and the manifest has five `resolved:` and **zero** `open:`; the strict
half lives under a different name.

### WF #3179: the P0 is genuinely fixed, end to end

Root cause established and recorded in the PR (GitHub's unproven-workflow-protection hold, triggered
by a workflow-level `issues: write` over a read-only comparison job); the remedy split the write into
a `publish-drift` job, dropped the `secrets: toJSON(secrets)` handoff and SHA-pinned checkout. Live:
Health 68 executes continuously against 400-of-400 `action_required` before, issue #2210's marker
moved from `2026-07-31T16:30:37Z` to `2026-08-24T02:09:52Z`, and the tracker **auto-resolved** on a
clean comparison at 06:29Z. #3180's fix also reached production in the same body:
`unmeasured_create_only=68`, exactly the number the audit computed.

**But the liveness oracle #3179 added cannot see a no-op.** `check_durable_tracker_liveness.py` counts
`success` as evidence of execution, and a debounced Health 68 run concludes `success` with
`Compare consumer repos to templates => skipped`. Verified on live runs: of five sampled, three
compared nothing and all five concluded `success`. A repo whose Health 68 never compares again reads
as healthy to the mechanism built to catch exactly that. The debounce compounds it by measuring the
age of the last *successful run* (including its own no-ops) rather than the last *comparison*. Body 03.

### Four PR bodies fail the break/revert AC — and the gap was closable

#3190, #3193 and #3194 carry **no validation section at all** (preamble + auto-generated issue
restatement + CodeRabbit notes only); #3179 and #3203 carry paraphrases rather than raw pytest output.
Every one of those issues chose the PR body as the proof medium *for a stated reason* — "this
repository's Actions history shows `action_required` runs, so a workflow result cannot attribute the
failure unambiguously" — making it the one AC that CI cannot substitute for. **All three missing
proofs were then produced with `local_verify.py`** against each PR's pre-merge base: verdict PASS on
all three, with reds of `KeyError` on the absent counts key (#3190), `AttributeError: 'ManifestEntry'
object has no attribute 'source_tree'` (#3193), and the AssertionError naming the six uncovered
basenames verbatim (#3194). The gates are real; the evidence obligation was simply never discharged,
and nothing in the lane required it.

**Capability evidence — the scarce type now exists.** Full detail in
`2026-08-24-capability-evidence.md`; both bound-but-never-consulted surfaces
(`implementation-verification`, `repo-audit:fix`) were called for the first time.

1. **First non-self-reported verdicts in the system.** Provenance mix went from `{self_reported: 12}`
   at 100% to `{self_reported: 12, outcome_corroborated: 1, defect_found: 1, machine_observed: 1}` —
   3 outcome-derived, self-reported share 100% -> 80%. Both new verdicts returned
   `judge_attributed: true` and `correlated_with_same_arm_verdicts: false`.
2. **`capabilities with >1 judge arm` moved 0 -> 2**, which was the run's stated second purpose. Two
   new arms: `local_verify.py` (machine, exit codes) and a `vibe`+`cursor` adversarial panel (neither
   Claude nor codex; `gemini` is not installed on this machine).
3. **`deliberate-break-verifier` recorded `outcome_corroborated` (weight 1.0)** — the only chain
   traceable end to end: its pre-filing PASS verdicts are why each issue could name a non-vacuous
   gate; four of the five TMP findings became issues, were fixed, and the fixes **hold** (each
   re-measured first-person at HEAD); and this run's three PASS verdicts still hold, with #3190's
   protected number visible in the live tracker body.
4. **`adversarial-review` recorded `defect_found` (weight 1.0)**, invoked directly per its
   `HOW_TO_USE` ("CALLABLE AT ANY SURFACE... an audit phase invokes this function directly and needs
   no gate lifted") — the advisor never offers it, since its matcher is the closer lane's entry. Its
   stated boundary ("where the refutation is mechanical, a panel adds nothing a shell does not")
   correctly scoped it AWAY from the four deliberate breaks and ONTO the one contested judgement.
5. **Propensity movement**: `deliberate-break-verifier` 0.556 -> **0.692**, `adversarial-review`
   0.500 -> **0.692** — now the two top-ranked capabilities, for the first time on evidence rather
   than opinion.
6. **8 declines, each with its kind**: `offload` `wrong_match` x2 (the work had to be first-person —
   run gates and read exit codes, re-run guards with breaks in place; the precondition WAS met, so
   not `precondition_unmet`), `role-adjudicator` `no_landing_zone` (skill step 6 performed; no
   blocker existed to weigh), `runtime-ac-checks` `gated_off` (best on-paper match, `gate_ready:
   false`), `testgen-lane` `no_landing_zone` x2, `codemod-campaign` `no_landing_zone`,
   `epic-decomposition` `scope_too_small`. The ledger immediately raised a repair proposal quoting my
   own decline text: `offload WORTH HAVING, defect evidence 2/8` — it now carries 19 declines against
   2 useful verdicts, ~7 of them saying the same structural thing. `wrong_match` implies the matcher
   or binding, so the fix is narrowing offload's surface-wide declaration away from execution-heavy
   surfaces, not lowering its rank.
7. **Two `local_verify.py` interface findings, recorded because they cost two wasted runs**:
   `--test-path` is the copy/analysis scope only, `--test-cmd` is executed verbatim (so a node-id must
   be in the cmd, or the whole suite runs and hits the 120 s default); and passing a *node-id* to
   `--test-path` copies nothing into the base tree, making the red `rc=4 "no tests ran"` — the test
   does not exist at base rather than fails at base — while the **verdict is still PASS**. The
   `reason` string discloses it; the verdict does not.
8. **Chains NOT closed, and why**: the Fine-Art-Archive `adversarial-review` citations are in bodies
   that were staged and never filed, so there is no fix and no durability — recording that as
   `outcome_corroborated` would make the top tier self-certifying, which is what `--corroboration`
   exists to prevent. The 2026-08-23 widened-check chain did land as #3182, but the verifier's
   contribution cannot be separated from the auditor's own hand-break from today's artefacts.

**Environment blocker (recorded, not repaired).** `git clone --local --no-hardlinks` of
`Code/Workflows` aborted with *"aborting due to possible repository corruption on the remote side /
fatal: early EOF"*. `git show`, `git archive`, `git grep` and `git cat-file` all work against that
clone, so the damage is confined to objects only a full clone walks. Per the workspace rule on this
volume it was **not fetched into and not repaired**; the synthetic base/merged repos `local_verify.py`
needed were built with `git archive` instead.

**Artifacts**: `Trend_Model_Project/2026-08-24-implementation-verification.md`,
`Workflows/2026-08-24-implementation-verification.md`, `2026-08-24-capability-evidence.md`,
`2026-08-24-issue-bodies/` (4, all lint-passing).

**Next ledger action**: owner decision on filing bodies 01-04. If only one is filed, file **01** — it
is the only one whose defect is live in production output today, and the only one whose follow-up gets
harder the longer the merged test asserting it stays green. Then **03** (a liveness oracle that cannot
see a no-op is the same failure class that cost 23 days), then **04**, then **02**. Separately, and
larger than any of the four: **the verdict-disposition gap**. A verifier arm produced the right answer
about #5986 at 94% confidence and nothing consumed it. That is a Workflows keepalive/verifier question,
not a Trend_Model_Project one, and it is the highest-leverage thing this round found.

## 2026-08-24 — stranske/Counter_Risk — full re-audit (COMPLETE)

- **Source/automation:** `repo-audit` skill, scheduled task `counter-risk-audit` (non-interactive).
- **Tip:** `61c3770` (main). Baseline: CI green 20/20, 0 open PRs, 2 open issues.
- **Category coverage:** all 8 dimensions + lead-seat findings. 14/14 capability surfaces consulted.
- **Main findings by category:**
  - *Code quality (d1):* 5 BLOCKER / 8 MAJOR / 6 MINOR. NaN through `_find_numeric`
    (`compute/rollups.py:121`) makes risk rank 1 order-dependent; WAL signed near-zero denominator
    (`calculations/wal.py:44`) returns −3.3e11 days; futures delta over-charges duplicate rows.
  - *Duplication (d2):* 20 clusters, 1 BLOCKER (re-rated MAJOR on verification) / 5 MAJOR / 14 MINOR.
    `demo_artifact.py` vs `web_demo.py` share 186/231 lines and CI publishes the weaker twin.
  - *Wiring (d3):* 3 BLOCKER / 7 MAJOR / 6 MINOR. Inert keys 17/85 (2/70 application-governing).
    Missing `limits.yml` silently disables all limit checking; one registry typo voids the registry.
  - *Design/UX (d4):* `web/index.html` is an orphan surface; Streamlit design-system inapplicable here.
  - *Public field (d5):* gemini offload — SA-CCR/gross-absolute-notional convention citations.
  - *Missed opportunities (d6):* manifest-to-manifest run-diff harness ~90% built, never assembled.
  - *Tools (d7):* Windows CI job is the real gap; hypothesis for the string→number boundary.
  - *Local automations (d8):* 2 BLOCKER / 6 MAJOR / 6 MINOR. One **latched gate**
    (`maint-coverage-guard`, drainable = 0); `agents-81-gate-followups` failed 94× in 31 days silently.
  - *Cross-cutting linchpin:* `configure_logging` has **zero production callers** — 37 INFO/DEBUG
    records emit nothing; every log-and-continue mitigation is invisible at runtime.
- **Non-actionable / out of scope:** 73/76 `scripts/` + 33/37 workflows are Workflows-synced;
  6 hypotheses refuted and recorded; Windows-runtime behaviour of the 3.14 bundle needs a Windows box.
- **Issues/PRs:** none filed, by instruction. 4 lint-passing AGENT_ISSUE_FORMAT bodies staged
  (X-1 logging, C-1 NaN ranking, C-3 WAL, L-1 PyInstaller guard). 9 further findings have complete
  evidence but no staged body — listed by ID in the verification log.
- **Artifacts:** `Code/Audits/Counter_Risk/2026-08-24-*`
  (AUDIT_REPORT, 8 dimension files, lead findings, capability evidence, verification log, issue bodies).
- **Next ledger action:** owner decides which staged bodies to file. If any are filed, record
  issue numbers here and open a follow-up implementation-verification row.

## 2026-08-29 — stranske/Orchestrator — API-capacity monitoring and load-spreading audit (COMPLETE)

- **Source/automation:** user-requested `orchestrator` + `repo-audit` skills; Codex lead with Cursor/Gemini/Vibe Orchestrator advisors and a separate adversarial Vibe pass.
- **Tips:** Orchestrator `b80e6e4` and fresh Workflows `06fe386`; the Dropbox checkout was clean/exact at classification, and later concurrent changes were preserved and excluded.
- **Measured verdict:** the recurrence is real but not a fleet outage. Provider-facing attempts rose from 96.4/day in June 26–July 31 to 130.1/day in August 11–25 (+34.9%), then returned to about 103/day. Direct Cursor exhaustion moved from 19/684 to 0/54, but Fisher `p=0.3878` leaves the improvement unproved.
- **Primary model-load cause:** local hourly research followup ran 72 four-evaluator panels (288 calls) over two repeatedly recovered missing-spec inputs; retained prompts provide a ~7.5M-input-token lower bound. Remote keepalive was material for Codex (144/307 rows) but only 8.9% of all provider rows during the spike and under 1% after cutoff.
- **Remote API cause:** 3/1,372 recent Workflows runs had confirmed GitHub installation-rate failures. Agents 70 proved a preflight/consumer credential mismatch; Agents 71 showed checkout-after-client-setup degradation. Official quota semantics refuted an advisor's per-run `GITHUB_TOKEN` isolation claim.
- **Monitoring:** PR #140 works in covered dispatcher paths, but direct lanes remain outside the loop; the 200-row incident file is a batch backfill without occurrence/invalidation semantics; tests contaminated the production capacity ledger with 983 zero-count synthetic rows.
- **Priorities:** P0 contain/dedupe/token-budget experiment fan-out and bind GitHub gates to consuming pools; P1 denominator ledger, unified circuit breaker, global load budget, and test isolation; P2 repair stale skill brief path.
- **Artifacts:** `Orchestrator/2026-08-29-AUDIT_REPORT.md`, `-00-topology-and-evidence.md`, advisor reports `-01` to `-03`, `-04-quantitative-evidence.md`, `-05-adversarial-recheck.md`, `-verification-log.md`, and `-audit-run.md`.
- **Validation/mutations:** 77 isolated Orchestrator tests, 76 Workflows Python tests, 3 Node tests, relevant self-tests, and wrapper guard passed. Read-only audit; no issue, PR, code, workflow, routing, credential, marker, or remote mutation.
- **Next ledger action:** owner may authorize an implementation sequence beginning with experiment containment and Workflows credential-pool binding; prove it over a seven-day denominator/SLO window before declaring the recurrence fixed.

## 2026-09-04 — fleet intake wave 1: Fine-Art-Archive, Inv-Man-Intake, Manager-Database (IN PROGRESS)

- **Source/automation:** owner directive (travelling 2026-09-04..09-14): use the Orchestrator to audit multiple repos until the fleet has ~10 days of implementation intake (measured completion rate 5.3 implementation issues/day over 60 days; target ~30 verified issues across waves). `repo-audit` skill; Claude lead, codex/cursor/gemini read-only offloads under the checkpoint protocol.
- **Scope:** app code + tests; `.github/` (synced from Workflows) and vendored trees excluded. Dimensions 1, 2, 3, 6 only this round (UX/field/tools/automations not covered — recorded in each `2026-09-04-audit-run.md`).
- **Artifacts:** `Code/Audits/<repo>/2026-09-04-audit-run.md`, `-NN-<area>.md` per dimension agent, `-verification-log.md`, `-issue-bodies/`.
- **Next ledger action:** adversarial verification, then filing with `priority:*` labels; wave 2 (Pension-Data, learning-management-system, Trend_Model_Project, trip-planner, Travel-Plan-Permission) follows.

## 2026-09-04 — fleet intake wave 2: Pension-Data, learning-management-system, Trend_Model_Project, trip-planner, Travel-Plan-Permission (IN PROGRESS)

- **Source/automation:** same directive and method as wave 1 (owner travelling; ~10 days of implementation intake at the measured 5.3 issues/day). Cursor agents on duplication and test gaps launched first; codex agents on code quality and wiring follow as wave-1 codex slots free (parallelism capped at ~6).
- **Scope/dimensions:** as wave 1 (D1, D2, D3, D6; app code and tests only; synced trees excluded). Prior-audit defect classes embedded in every brief for state re-check.
- **Artifacts:** `Code/Audits/<repo>/2026-09-04-audit-run.md`, then `-NN-<area>.md`, `-verification-log.md`, `-issue-bodies/`.

## 2026-09-04 — fleet intake wave 1: ISSUES FILED (22)

- **Filed after lead verification** (cited lines opened on the fresh clone; BLOCKERs read in full; every body passed the fleet's issue_format guard):
  - Fine-Art-Archive: 7 issues (#670, #671, #672, #673, #674, #675, #676)
  - Inv-Man-Intake: 8 issues (#938, #939, #940, #941, #942, #943, #944, #945)
  - Manager-Database: 7 issues (#1623, #1624, #1625, #1626, #1627, #1628, #1629)
- **Dimensions covered:** D1 code quality, D2 duplication, D3 wiring, D6 test gaps. Not covered: D4 UX, D5 field, D7 tools, D8 automations.
- **Artifacts:** `Code/Audits/<repo>/2026-09-04-01-code-quality-and-wiring.md`, `-02-duplication-and-test-gaps.md`, `-issue-bodies/`, `-verification-log.md`, `-agent-checkpoints.md`.
- **Next ledger action:** wave 2 filing; implementation-verification of merged PRs after the 10-day window.

## 2026-09-04 — fleet intake wave 2: ISSUES FILED (23, cursor duplication/test-gap dimension; codex code-quality/wiring findings pending)

- **Filed after lead verification** (cited lines opened; falsifiable claims read; residual fail-open findings cross-reference the closed prior issues #1429, #1676):
  - Pension-Data: 4 issues (#869, #870, #871, #872)
  - learning-management-system: 4 issues (#570, #571, #572, #573)
  - Trend_Model_Project: 6 issues (#6017, #6018, #6019, #6020, #6021, #6022)
  - trip-planner: 3 issues (#1778, #1779, #1780)
  - Travel-Plan-Permission: 6 issues (#1499, #1500, #1501, #1502, #1503, #1504)
- **Artifacts:** `Code/Audits/<repo>/2026-09-04-02-duplication-and-test-gaps.md`, `-issue-bodies/`, `-verification-log.md`, `-agent-checkpoints.md`.
- **Next ledger action:** codex D1/D3 findings for the five repos (verify, file up to the intake target); then implementation-verification after the window.

## 2026-09-04 — fleet intake waves 1+2: COMPLETE — 60 issues filed across 8 repos

- **Why this volume:** the fleet completes 5.3 implementation issues/day (60-day measurement, trackers/campaigns excluded); the owner is away 2026-09-04..09-14 and the review pipeline's omitted-decision default was `defer` (now `approve` for the window, Workflows #3351). 60 issues ≈ 11 days of intake at that rate.
- **Method:** repo-audit skill; 16 read-only Orchestrator offloads (codex D1/D3, cursor D2/D6) into fresh shallow GitHub clones, checkpointed, disk-first; lead cite-checked every finding, read every BLOCKER and every falsifiable claim, deduplicated codex-vs-cursor and against open and recently closed issues; every body passed the fleet's issue_format guard; labels per repo's own set (priority:* where it exists).
- **Filed:**
  - Fine-Art-Archive: 7 — #670, #671, #672, #673, #674, #675, #676
  - Inv-Man-Intake: 8 — #938, #939, #940, #941, #942, #943, #944, #945
  - Manager-Database: 7 — #1623, #1624, #1625, #1626, #1627, #1628, #1629
  - Pension-Data: 8 — #869, #870, #871, #872, #873, #874, #875, #876
  - Travel-Plan-Permission: 10 — #1499, #1500, #1501, #1502, #1503, #1504, #1505, #1506, #1507, #1508
  - Trend_Model_Project: 10 — #6017, #6018, #6019, #6020, #6021, #6022, #6023, #6024, #6025, #6026
  - learning-management-system: 6 — #570, #571, #572, #573, #574, #575
  - trip-planner: 4 — #1778, #1779, #1780, #1781
- **Not covered:** D4 UX (needs observed evidence), D5 field, D7 tools, D8 automations. Not filed: duplicates and MINORs (listed per repo in the verification logs).
- **Measurement:** the day-10 check-in (orch-window-2026-09-14) now carries T6 = how many of these 60 the fleet closed (intake log at ~/.codex/orchestrator/measurement/intake-2026-09-04.log).
- **Lesson:** one of the lead's grep-based refutations was wrong (Inv-Man-Intake threshold validation); recorded in memory — open the cited lines before refuting.
- **Next ledger action:** implementation-verification of merged PRs against these issues after 2026-09-14.

## 2026-09-04 — fleet intake wave 3: Counter_Risk, Ready, Portable-Alpha-Extension-Model, Workflows (IN PROGRESS)

- **Why:** the first 60 issues were being completed at ~16/day in their first 7 hours (5 closed, 6 PRs merged, 1 in flight by 13:20 UTC), three times the 60-day baseline the sizing used; 60 would last ~4 days, not 10. Wave 3 covers the four lane-fleet repos not audited today (Orchestrator excluded: moratorium on new instruments; its repairs come through the cadence).
- **Method/scope:** as waves 1–2. Workflows scope is scripts and tests only (workflow YAML excluded).

## 2026-09-04 — fleet intake wave 4: Doc-Lineage, Deliverable-Render, Manager-Mosaic (IN PROGRESS)

- **Why:** the three repos joined the lane fleet on 2026-09-04 (CLAUDE.md fleet list; opener cap raised 5 -> 8 the same day) and have no prior audit; intake pace on waves 1-2 (~16/day) exceeds the sizing baseline.
- **Method:** as waves 1-3, plus Claude-subagent adversarial verification before filing.

## 2026-09-04 — waves 3/4 correction: Ready, Doc-Lineage, Deliverable-Render, Manager-Mosaic are template skeletons

- Each owns ~30 LOC of `src/` and five template tests; `scripts/` is byte-identical across the four (synced/template-delivered) and `tools/` is synced from Workflows. Their cursor findings are all template findings. Decision: no per-repo issues; the stale `scripts/validate_dependency_test_setup.py` / `scripts/sync_test_dependencies.py` findings go upstream as one Workflows issue, and trip-planner #1781 (filed this morning against the same synced file) is re-pointed to it. Ready's codex agent was stopped.

## 2026-09-05 — Manager-Mosaic: Track D Demand-Driven Refill Audit (COMPLETED — 9 issues filed)

- **Source/automation:** Track D refill (open agent-ready supply 2/4 ≤ threshold). Unit `D-audit-Manager-Mosaic--2026-09-05T04-00-25Z` attempt 2. Repo-audit skill; Cursor lead.
- **Scope:** `src/manager_mosaic/`, `tests/`, consumer-local `config/`, `docs/contracts/`, `Issues.txt`, `pyproject.toml`. Excluded synced `.github/`, `tools/`, `scripts/`.
- **Base SHA:** `02ffccfd0f2bede33576c5109f90e723d1190705` (main).
- **Method:** Phase 0 scoped without dossier (missing) using README, CLAUDE.md, R3 synthesis, prior audit closure; bash orientation; adversarial re-read of every cited path; local `issue_format.py` pre-flight (9/9 pass with advisories).
- **Issues Filed (9):** #6–#14 (template metadata drift, backplane consumer registry/fixtures, evidence validator, discrepancy detection, thesis monitoring, fact_key registry). Pre-existing #3 (core model) retained, not duplicated.
- **Artifacts:** `Code/Audits/Manager-Mosaic/2026-09-05-*`; OUT `artifacts/audits/Manager-Mosaic-2026-09-05.md`.
- **Measurement:** Intake rows appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Next ledger action:** Format-guard verification on #6–#14; agent pickup; post-merge verification.

## 2026-09-05 — Fine-Art-Archive: Track D Demand-Driven Refill Audit (COMPLETED — 9 issues filed)

- **Source/automation:** Track D demand-driven audit refill (open agent-ready supply dropped to 1 <= 2). Unit `D-audit-Fine-Art-Archive--2026-09-05T04-00-31Z`. Repo-audit skill; Gemini lead via Antigravity (agy).
- **Scope:** App library (`src/fine_art_archive/`), scripts (`scripts/`), schemas (`schemas/`), configuration (`config/`), and tests (`tests/`). Synced `.github/` and `tools/` excluded.
- **Base SHA:** `d149861e60f089868be5aa28373bdf5d3513a290` (remote `origin/main` tip).
- **Method:** Full 8-dimension audit with baseline bash orientation (`ruff check` clean, `black --check` clean, 1,899 tests collected); deep adversarial verification of every candidate finding by executing reproducible Python repros against the live clone; all 9 issue bodies machine-checked with `issue_lint.py` (0 errors).
- **Issues Filed (9):**
  - **#689**: `[P1] Reject non-finite and non-positive shares in lens allocation algorithms` (`src/fine_art_archive/selection/lenses.py`)
  - **#690**: `[P1] Handle offset-naive timestamps in source-quality warmup blending` (`src/fine_art_archive/quality/source_quality.py`)
  - **#691**: `[P2] Resolve canonical artist Q-IDs when projecting Linked Art actors` (`src/fine_art_archive/crosswalk.py`)
  - **#692**: `[P2] Parse 3D dimension strings with trailing units in physical dimension comparison` (`src/fine_art_archive/parsers/dimension_utils.py`)
  - **#693**: `[P2] Bound max pixel dimension on variant candidate image preview endpoint` (`src/fine_art_archive/api/main.py`)
  - **#694**: `[P2] Check canonical artist Q-ID in provenance field value extraction` (`src/fine_art_archive/provenance.py`)
  - **#695**: `[P2] Use default_works_dir in rank_known_works CLI for sidecar root resolution` (`scripts/rank_known_works.py`)
  - **#696**: `[P2] Fall back to year_min when building manifest rows for approximate-date artworks` (`scripts/build_manifest.py`)
  - **#697**: `[P2] Guard None and non-finite values in Bradley-Terry next_pair selection` (`src/fine_art_archive/preference/bradley_terry.py`)
- **Artifacts:** `Code/Audits/Fine-Art-Archive/2026-09-05-audit-run.md`, `2026-09-05-00-repo-map.md`, `2026-09-05-AUDIT_REPORT.md`, `2026-09-05-verification-log.md`, `2026-09-05-issue-bodies/` (01..09).
- **Measurement:** Filed URLs appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Next ledger action:** Autonomous agent pickup and implementation of #689-#697; post-merge verification.


## 2026-09-05T04:17:16.604641+00:00 — Codex attempt-2 reconciliation
Continued D-audit-Fine-Art-Archive--2026-09-05T04-00-31Z from completed Phase 5; nine existing issues verified, eight remote guard passes (four with path advisories), #689 remote guard unproven. Corrected full SHA to d149861964fa4093d4228ef424853fa5de1dced0. Nine corrected local bodies pass actual repo validator without advisories. Narrowed #689/#693/#694/#697 claims; no new filing, dispatch, code change, or duplicate intake entry. Full-suite and comprehensive UX/field/tool/fleet claims remain unverified. The current qualification of the prior report is [resume reconciliation](/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Fine-Art-Archive/2026-09-05-resume-reconciliation.md). Next: publishing-capable lane applies staged corrections and validates #689 remotely.

## 2026-09-05T16:14:54.536097+00:00 — Travel-Plan-Permission research refill (in progress)

D-audit-Travel-Plan-Permission--2026-09-05T16-11-36Z: remote main 3ba14a8541b97338586ab6c253ea30e2aed7b86e. Eight dimensions planned; research-only issue bodies. Scope: Travel-Plan-Permission/2026-09-05-audit-run.md. Next: bounded analysis and adversarial verification.

## 2026-09-05T16:38:56.584615+00:00 — Travel-Plan-Permission research refill completed

Source D-audit-Travel-Plan-Permission--2026-09-05T16-11-36Z, head 3ba14a8541b97338586ab6c253ea30e2aed7b86e. Eight dimensions assessed; 8 staged issue bodies (5 P1, 3 P2), 0 issues/PRs filed, 0 intake log rows. Primary: expense/exception auth, approval identity, literal export text, receipt delivery and browser recovery. Config parity latent; exception tier hardening downgraded to P2. All 8 bodies pass repo validator with no advisories. Existing 1436 restart audit-loss repro retained for follow-up. Scope limits: local browser subset, OIDC/production/native Excel unverified; one full-suite environment pin failure. Artifacts Travel-Plan-Permission/2026-09-05-AUDIT_REPORT.md, verification-log, UX_REVIEW and issue-bodies. Next owner publishing/intake lane: review drafts, recheck remote head/dedup, then file under its own authority.

## 2026-09-06 — Fine-Art-Archive: Track D Demand-Driven Refill Audit (COMPLETED — 8 issues filed)

- **Source/automation:** Track D demand-driven audit refill (open agent-ready supply dropped to 1 <= 3). Unit `D-audit-Fine-Art-Archive--2026-09-06T04-25-53Z`. Repo-audit skill; Gemini lead via Antigravity (agy).
- **Repo tip:** `stranske/Fine-Art-Archive` @ `9d6d61918cf2153d043c298b1ba3b1cb2aa7f6af` (clean checkout of remote main).
- **Scope:** Full 8-dimension audit covering `src/fine_art_archive/`, first-party CLI `scripts/`, `tests/`, `schemas/`, `config/`, `docs/contracts/`. Excluded synced `.github/` and Workflows infra.
- **Baseline:** `ruff` clean, `black` clean, 2,014 pytest tests collected across 125 test modules.
- **Filed Issues:** 8 machine-linted AGENT_ISSUE_FORMAT issues filed with triage labels (`bug`), all passing remote `Agents Issue Format Guard`:
  - **#708**: `fix(selection): guard non-finite inputs and zero batch cap in apply_saturation_cap` (`src/fine_art_archive/selection/lenses.py:236-274`)
  - **#709**: `fix(preference): filter non-finite ratings in rocchio build` (`src/fine_art_archive/preference/rocchio.py:124-173`)
  - **#710**: `fix(identity): deepcopy mutable metadata values during variant inheritance` (`src/fine_art_archive/identity/variants.py:427-431`)
  - **#711**: `fix(parsers): validate finite non-negative tolerance in dim_compat` (`src/fine_art_archive/parsers/dimension_utils.py:88-120`)
  - **#712**: `fix(eink): guard non-finite inputs in acuity_blur_radius` (`src/fine_art_archive/eink/palette.py:422-434`)
  - **#713**: `fix(api): specify explicit utf-8 encoding in atomic sidecar writes` (`src/fine_art_archive/api/main.py:1397-1411`)
  - **#714**: `fix(playlist): prevent year 0 falsiness in playlist artist sort` (`src/fine_art_archive/eink/playlist.py:400-401`)
  - **#715**: `fix(scripts): add explicit utf-8 encoding and parent directory creation in propose_subject_tags` (`scripts/propose_subject_tags.py:509-545`)
- **Artifacts:** `Code/Audits/Fine-Art-Archive/2026-09-06-audit-run.md`, `2026-09-06-00-repo-map.md`, `2026-09-06-AUDIT_REPORT.md`, `2026-09-06-verification-log.md`, `2026-09-06-issue-bodies/` (01..08).
- **Measurement:** Filed URLs appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Next ledger action:** Autonomous agent pickup and implementation of #708-#715; post-merge verification.

## 2026-09-06 — Travel-Plan-Permission: Track D Demand-Driven Refill Audit (COMPLETED — 8 issues filed)

- **Source/automation:** Track D demand-driven audit refill (open agent-ready supply dropped to 1 <= 2). Unit `D-audit-Travel-Plan-Permission--2026-09-06T04-25-49Z`. Repo-audit skill; Gemini lead via Antigravity (agy).
- **Repo tip:** `stranske/Travel-Plan-Permission` @ `3e53ddea64838fd863146c6efd169e1e32a8ec02` (clean checkout of remote main).
- **Scope:** Full 8-dimension audit covering `src/travel_plan_permission/`, `tests/`, `templates/`, `config/`, `schemas/`, `docs/contracts/`. Excluded synced Workflows CI infra.
- **Baseline:** `ruff check .` clean (0 diagnostics), 866 unit tests passing (1 skipped, 1 deselected, 3 xfailed) + 41 baseline tests passing.
- **Filed Issues:** 8 machine-linted AGENT_ISSUE_FORMAT issues filed with validated repository labels, all passing remote `Agents Issue Format Guard`:
  - **#1523**: `[P1] Enforce permissions on expense intake, review, and export` (`src/travel_plan_permission/http_service.py:1726, 1799, 2253`, `security.py:14, 55`)
  - **#1524**: `[P1] Authenticate exception creation and bind its audit actor` (`src/travel_plan_permission/http_service.py:1815, 1867, 1884`)
  - **#1525**: `[P1] Bind approval history to the authenticated decision maker` (`src/travel_plan_permission/http_service.py:2033, 2041, 2074, 2123`)
  - **#1526**: `[P1] Preserve untrusted export text as literal spreadsheet cells` (`src/travel_plan_permission/export.py:62, 85, 110`)
  - **#1527**: `[P1] Replace placeholder receipt links with a verifiable delivery contract` (`src/travel_plan_permission/export.py:25, 40`, `http_service.py:1294`)
  - **#1528**: `[P2] Give direct portal drafts a usable scoped review session` (`src/travel_plan_permission/http_service.py:1696, 1703, 1721, 1762`)
  - **#1529**: `[P2] Guard shipped YAML defaults against checkout and wheel drift` (`src/travel_plan_permission/config_loader.py:35`, `tests/python/test_policy_api.py:1276`, `test_template_assets.py:61`)
  - **#1530**: `[P2] Bind routed exception levels to authenticated approval authority` (`src/travel_plan_permission/models.py:194, 263`, `http_service.py:2114`)
- **Artifacts:** `Code/Audits/Travel-Plan-Permission/2026-09-06-audit-run.md`, `2026-09-06-00-repo-map.md`, `2026-09-06-AUDIT_REPORT.md`, `2026-09-06-UX_REVIEW.md`, `2026-09-06-verification-log.md`, `2026-09-06-issue-bodies/` (01..08).
- **Measurement:** Filed URLs appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Next ledger action:** Autonomous agent pickup and implementation of #1523-#1530; post-merge verification.


## 2026-09-06 — Travel-Plan-Permission: Track D Demand-Driven Refill Audit (COMPLETED — 9 issues filed)

- **Source/automation:** Track D demand-driven audit refill (open agent-ready supply dropped to 2 <= 2). Unit `D-audit-Travel-Plan-Permission--2026-09-06T16-33-27Z`. Repo-audit skill; Gemini lead via Antigravity (agy).
- **Repo tip:** `stranske/Travel-Plan-Permission` @ `8c046c91b94aa2aed58b50cd152c9ce4ece07611` (clean checkout of remote main).
- **Scope:** Full 8-dimension audit covering `src/travel_plan_permission/`, `tests/`, `templates/`, `config/`, `schemas/`, `docs/contracts/`. Excluded synced Workflows CI infra.
- **Baseline:** `ruff check .` clean (0 diagnostics), 987 pytest tests collected across 77 test modules.
- **Filed Issues:** 9 machine-linted AGENT_ISSUE_FORMAT issues filed with validated repository labels, all passing remote `Agents Issue Format Guard`:
  - **#1539**: `[P1] LocalOvernightRule fails open when distance_from_office_miles is NaN` (`src/travel_plan_permission/policy.py:349-354`)
  - **#1540**: `[P1] Escape unformatted user strings in ReportLab PDF generation` (`src/travel_plan_permission/approval_packet.py:153-159`, `prompt_flow.py:217-220`)
  - **#1541**: `[P2] Reconcile third-party payment totals in ExpenseReport category breakdowns` (`src/travel_plan_permission/models.py:582-592`, `policy_api.py:1732`)
  - **#1542**: `[P1] Map canonical flight fare comparisons and structured ground transport into TripPlan` (`src/travel_plan_permission/canonical.py:168-185, 203-216`)
  - **#1543**: `[P1] Confine ValidationSnapshotStore file paths to prevent directory traversal` (`src/travel_plan_permission/snapshots.py:143-145, 166-170`)
  - **#1544**: `[P2] Guard finalized manager review requests against illegal state mutations` (`src/travel_plan_permission/review_workflow.py:108-145`, `http_service.py:785-802`)
  - **#1545**: `[P2] Parse European slash-separated date formats in ReceiptProcessor` (`src/travel_plan_permission/receipts.py:149-160`)
  - **#1546**: `[P2] Make audit.pending_event_from_state resilient to empty or null metadata_json` (`src/travel_plan_permission/audit.py:556-570`, `http_service.py:1048`)
  - **#1547**: `[P2] Guard workbook_ooxml against corrupting XML on NaN and infinite numeric values` (`src/travel_plan_permission/workbook_ooxml.py:101-105`)
- **Artifacts:** `Code/Audits/Travel-Plan-Permission/2026-09-06-refill-AUDIT_REPORT.md`, `2026-09-06-refill-verification-log.md`, `2026-09-06-refill-issue-bodies/` (01..09).
- **Measurement:** Filed URLs appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Next ledger action:** Autonomous agent pickup and implementation of #1539-#1547; post-merge verification.


## 2026-09-07 — Counter_Risk: Track D Demand-Driven Refill Audit (COMPLETED — 7 issues filed)

- **Source/automation:** Track D demand-driven audit refill (open agent-ready supply dropped to 2 <= 2). Unit `D-audit-Counter_Risk--2026-09-07T04-47-32Z`. Repo-audit skill; Gemini lead via Antigravity (agy).
- **Repo tip:** `stranske/Counter_Risk` @ `aa3173e` (clean checkout of remote main).
- **Scope:** Full 8-dimension audit covering `src/counter_risk/`, `config/`, `docs/contracts/`, `tests/`, and first-party scripts. Excluded synced Workflows CI infra.
- **Baseline:** `ruff check .` clean (0 diagnostics), 1,472 unit tests passing (1 skipped) in 139s.
- **Filed Issues:** 7 machine-linted AGENT_ISSUE_FORMAT issues filed with validated repository labels, all passing remote `Agents Issue Format Guard`:
  - **#1000**: `[P1] Reject non-finite notional values in futures delta computation` (`src/counter_risk/compute/futures_delta.py:495-511`)
  - **#1001**: `[P1] Deduplicate and group current-month normalized descriptions in compute_futures_delta` (`src/counter_risk/compute/futures_delta.py:188-264`)
  - **#1002**: `[P2] Guard change attribution float parsers against non-finite values` (`src/counter_risk/reports/change_attribution.py:81-90, 93-105`)
  - **#1003**: `[P2] Accumulate multi-row counterparties in change attribution prior mapping` (`src/counter_risk/reports/change_attribution.py:198-199`)
  - **#1004**: `[P2] Validate non-negative and finite bounds for cash_total_min and cash_total_max` (`src/counter_risk/config.py:96-97, 161-169`)
  - **#1005**: `[P2] Bind dynamic GitHub issue reference to FleetRunContext in langsmith telemetry` (`src/counter_risk/observability/langsmith_fleet.py:16, 279`)
  - **#1006**: `[P2] Reject non-finite values in repo cash structured and override parsers` (`src/counter_risk/parsers/repo_cash_sources.py:274-282`)
- **Artifacts:** `Code/Audits/Counter_Risk/2026-09-07-audit-run.md`, `2026-09-07-AUDIT_REPORT.md`, `2026-09-07-verification-log.md`, `2026-09-07-issue-bodies/` (01..07).
- **Measurement:** Filed URLs appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Next ledger action:** Autonomous agent pickup and implementation of #1000-#1006; post-merge verification.
