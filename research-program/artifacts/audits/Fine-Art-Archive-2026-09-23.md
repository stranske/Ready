Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 9; closed-still-broken 0.

**Issues filed:** 1. https://github.com/stranske/Fine-Art-Archive/issues/741 (C4: `build_weekly_review.py` defaults its four workspace inputs to paths that never exist and ignores `FAA_WORKSPACE`). Agents Issue Format Guard: success (run 2026-09-23T23:11:25Z). Intake log and ledger recorded.

## Run report — round 2 (unit `D-audit-Fine-Art-Archive--2026-09-23T22-11-18Z`, tip `24c1fe9`)

**Why this unit fired.** Round 1 (earlier today) put its scorecard line in this OUT but not in `Code/Audits/Fine-Art-Archive/2026-09-23-SCORECARD.md`, and that file is the only place the refill engine reads a headline from. The repo was therefore re-queued as "no parseable headline". The tip had also moved: #740 merged `scripts/build_weekly_review.py`, which targets the C4 BROKEN row.

**What changed for the owner.** C4 went from BROKEN to PARTIAL. I built weekly reviews from a 5-work and a 2-work synthetic archive. Every measured figure moved: `live_works` 5/2, promotions 4/0, ungranted 2/0, frontier 4/0, unpromoted 2/1. The rendered decision page's text diff matches those changes. The figures are derived from the archive, not fabricated. The contract's own entry point, `build_weekly_review.py --date DATE`, still cannot run on the owner's machine. Three inputs default to the repo root, the staging root defaults to `Pictures/Art/staging_acquisitions`, none of those exist (the real files sit in `Pictures/Claude Project/`), and the README's documented `FAA_WORKSPACE` is ignored. The failure is loud (exit 2), so no wrong numbers are produced. Filed as #741, with a reproduction and a deliberate-break test gate.

**Interior coverage.** Every one of the 49 OpenAPI paths was probed through TestClient with all `FAA_*` data variables pointed at the scratchpad: 44 GETs and 17 POST/DELETE calls. Mutating routes ran against copies of three real, schema-valid sidecars with synthetic masters. Results:
- No 5xx on schema-valid input.
- Path traversal refused, both on `work_id` and on the export path (`/etc/evil` → 400).
- Playlist create → preview → export (3 PNG, `.m3u`, `playlist.json`) → feed `next`/`current`/`manifest.json` → delete all work, and so does the feed going 404 after the delete.
- `subject_action` persists into `subject.content_tags`, and `freetext_review` into `subject.reviewer_notes`.
- The acquisition review/undo round-trip works.

Unscored surfaces went from 42 to 9. The 9 were reached but only answered no-data 404/503/422 (deepzoom tiles, modality image, candidate images, named queue/gate, tagger, `POST /works/{work_path}`, `/debug/log`). They are listed in `2026-09-23-SCORECARD-r2.md` §6 with the seeding needed next round.

**Refuted or not filed (my own mistakes, caught in verification).**
- An early 500 on `POST /eink/playlists` came from my fixture's dict-shaped `title`. `schemas/meta.schema.json` requires a string, and 327 of 327 sampled real sidecars use one.
- A 500 on `acquisition_review` was the validator refusing to write my schema-invalid fixture, which is correct.
- `eink_preview?target=spectra6` → 400 is correct, because spectra6 is a palette, not a target. Round 1's C2 row cited that parameter. C2 re-verified with the default target: three distinct hashes.

**Closed issues.** #739 (closed by #740): its producer exists and works. Its `Reproduction:` block still raises `FileNotFoundError`, but only because it renders without building first, so the block is stale, not a live defect. Counted as closed-still-broken 0. #741 cites #739. No REFUTED line: no open issue's claim was found false.

**System finding: the refill trigger is latched on a template omission. Worth the owner's attention.** `program.py` `refill_trigger_for` reads the headline from the newest `Code/Audits/<repo>/<date>-SCORECARD*.md`. The skill's scorecard-file template (`~/.claude/skills/repo-audit/reference/product-scorecard.md`, "The scorecard file") listed a title and seven headings and no headline line. Rounds that follow the template exactly therefore always read as "no parseable headline" and re-queue a full audit every refill cycle. At 23:20Z this was **10 of 14 repos**: Workflows, Travel-Plan-Permission, Trend_Model_Project, PAEM, Counter_Risk, Inv-Man-Intake, Pension-Data, Doc-Lineage, Deliverable-Render and Manager-Mosaic. Deliverable-Render's evening "headline repair" unit put the line in its OUT, not the scorecard file, so it is still latched.
- Fixed here: the template now carries the headline line under the title, with a note on why it is load-bearing. This is a skill doc edit, not program.py or a brief.
- FAA's two scorecard files now carry headlines, and `refill_trigger_for('Fine-Art-Archive')` returns `False, 'scorecard 2026-09-23 healthy (0B/0F, 0d old)'`, which is the drained output, now actually produced.
- Not done: backfilling the other nine repos' scorecard files from their ledger headlines. Their already-queued units will run regardless. The future-proof fix is a parser fallback to the ledger entry, which would live in `program.py` and is out of scope for an executor.

**Confidence.** High on the C4 PARTIAL verdict and #741 (reproduced twice, cited lines opened on tip `24c1fe9`). High that no interior route 5xxs on schema-valid data (every path probed). Medium on the 9 no-data surfaces (their logic is unexercised). Dimensions 1–2 and 5–8 were not re-run: round 1 covered them on the same day and only #740 changed since.

**Artifacts:** `Code/Audits/Fine-Art-Archive/2026-09-23-SCORECARD-r2.md`, `2026-09-23-assets/evidence-r2/` (sweep script and output, C4 A/B JSON, page diff), `2026-09-23b-issue-bodies/01-weekly-review-builder-workspace-defaults.md`, the round-2 sections in `2026-09-23-AUDIT_REPORT.md` and `2026-09-23-audit-run.md`, and the `AUDIT_LEDGER.md` entry.

---

# Round 1 (preserved)

Scorecard: 4 work / 0 partial / 1 broken / 0 fabricated / 0 not exercised of 5; journey: stops at "generate weekly_review JSON from live archive"; surfaces unscored 42; closed-still-broken 0.

**Issues filed:** 3 — https://github.com/stranske/Fine-Art-Archive/issues/737 https://github.com/stranske/Fine-Art-Archive/issues/738 https://github.com/stranske/Fine-Art-Archive/issues/739 (attempt 1; intake + ledger recorded; format guard success per attempt 2; attempt 3 could not re-poll `gh run list` — CLI not authenticated in this seat).

## Run report

Track D refill for `stranske/Fine-Art-Archive` at `5fb9a7d`. The 2026-09-20 round left a product contract in `docs/PRODUCT_CONTRACT.md` but **no parseable scorecard headline** in the audit ledger; this round supplies that line and live exercises all five contract core functions.

**What works:** manifest build + `/works` on `staging_sidecars` (C1); distinct e-ink previews for different master colours (C2); mood-filtered playlists via API/tests (C3); companion health + feed tests (C5).

**What is broken:** end-to-end weekly review generation (C4) — `render_weekly_review.py` requires a JSON file nothing in `scripts/` produces.

**What was filed:** merge year-0 sort in `known_works/fetchers.py`, backplane validator fixtures gap, weekly-review producer (#737–#739). Bodies under `Code/Audits/Fine-Art-Archive/2026-09-23-issue-bodies/`.

**Not filed:** healthz empty-manifest class (fixed 2026-08-25); Dropbox ops conflict (#735 already open); interior review/dossier/deepzoom routes (42 unscored surfaces, not probed live).

**Attempt 3 (resume):** `git pull` on clone — still `5fb9a7d`. Re-ran C1 (`build_manifest` → `/works` total 1), C4 (`render_weekly_review.py --date 2026-09-23` → `FileNotFoundError` on `docs/reports/weekly_review_2026-09-23.json`), #737 repro (`merge_works` order `['Year one', 'Year zero']`), #738 evidence (`tests/fixtures/backplane/` absent; `validate_run_contract.py --self-smoke` cannot load missing `config/backplane_participants.json`). `pytest tests/test_eink_feed_endpoints.py` — 49 passed. No additional filable defect found on tip; no new issues (prior filing intact). Dedup against closed issues: not re-run via API (gh unauth); prior round had no closed-still-broken rows.

**Confidence:** High on scorecard and three filed defects (reproduced again on attempt 3). Medium on “no additional filable defects” — dimensions 5–7 were not re-researched. Low confidence that format guard still passes today (not re-checked without `gh` auth).

**Artifacts:** `~/Library/CloudStorage/Dropbox/Learning/Code/Audits/Fine-Art-Archive/2026-09-23-AUDIT_REPORT.md`, `2026-09-23-SCORECARD.md`.
