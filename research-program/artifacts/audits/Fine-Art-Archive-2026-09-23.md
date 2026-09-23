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
