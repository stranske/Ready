# Fine-Art-Archive Audit Run Report — 2026-09-06

- **Unit ID:** `D-audit-Fine-Art-Archive--2026-09-06T04-25-53Z`
- **Title:** Audit stranske/Fine-Art-Archive and file issues (supply 1 <= 3)
- **Repository:** `stranske/Fine-Art-Archive`
- **Target Git SHA:** `9d6d61918cf2153d043c298b1ba3b1cb2aa7f6af` (clean tip of `main`)
- **Timestamp:** 2026-09-06T04:35:00Z
- **Auditor:** Gemini via Antigravity (agy)

---

## 1. Executive Summary

This demand-driven refill audit was triggered for `stranske/Fine-Art-Archive` after open agent-ready supply dropped to 1 (threshold <= 3). The audit conducted a comprehensive multi-dimensional analysis across the core application library (`src/fine_art_archive/`), companion API, CLI scripts, schemas, and test suite.

All 8 candidate findings were directly reproduced and adversarially validated on the live commit `9d6d61918cf2153d043c298b1ba3b1cb2aa7f6af`. Each finding was authored as an `AGENT_ISSUE_FORMAT` Markdown issue body and verified against the repository definition of ready using `issue_lint.py` (8/8 PASS). All 8 issues were successfully filed to GitHub with triage label `bug` and confirmed to pass the remote GitHub Actions `Agents Issue Format Guard` workflow with 100% success.

---

## 2. Inventory of Filed Issues

| # | Title | Target File:Line | Priority | Filed URL | Remote Guard Run |
|---|---|---|---|---|---|
| 1 | `fix(selection): guard non-finite inputs and zero batch cap in apply_saturation_cap` | `src/fine_art_archive/selection/lenses.py:236-274` | P1 | [#708](https://github.com/stranske/Fine-Art-Archive/issues/708) | `34011724169` (SUCCESS) |
| 2 | `fix(preference): filter non-finite ratings in rocchio build` | `src/fine_art_archive/preference/rocchio.py:124-173` | P1 | [#709](https://github.com/stranske/Fine-Art-Archive/issues/709) | `34011724909` (SUCCESS) |
| 3 | `fix(identity): deepcopy mutable metadata values during variant inheritance` | `src/fine_art_archive/identity/variants.py:427-431` | P2 | [#710](https://github.com/stranske/Fine-Art-Archive/issues/710) | `34011725658` (SUCCESS) |
| 4 | `fix(parsers): validate finite non-negative tolerance in dim_compat` | `src/fine_art_archive/parsers/dimension_utils.py:88-120` | P2 | [#711](https://github.com/stranske/Fine-Art-Archive/issues/711) | `34011725959` (SUCCESS) |
| 5 | `fix(eink): guard non-finite inputs in acuity_blur_radius` | `src/fine_art_archive/eink/palette.py:422-434` | P2 | [#712](https://github.com/stranske/Fine-Art-Archive/issues/712) | `34011726625` (SUCCESS) |
| 6 | `fix(api): specify explicit utf-8 encoding in atomic sidecar writes` | `src/fine_art_archive/api/main.py:1397-1411` | P2 | [#713](https://github.com/stranske/Fine-Art-Archive/issues/713) | `34011727103` (SUCCESS) |
| 7 | `fix(playlist): prevent year 0 falsiness in playlist artist sort` | `src/fine_art_archive/eink/playlist.py:400-401` | P2 | [#714](https://github.com/stranske/Fine-Art-Archive/issues/714) | `34011728411` (SUCCESS) |
| 8 | `fix(scripts): add explicit utf-8 encoding and parent directory creation in propose_subject_tags` | `scripts/propose_subject_tags.py:509-545` | P2 | [#715](https://github.com/stranske/Fine-Art-Archive/issues/715) | `34011728948` (SUCCESS) |

---

## 3. Detailed Finding Breakdown & Adversarial Reproduction

### Finding 1: Saturation Cap Non-Finite and Zero-Cap Bypass ([#708](https://github.com/stranske/Fine-Art-Archive/issues/708))
- **File & Lines:** `src/fine_art_archive/selection/lenses.py:236-274`
- **Defect:** `apply_saturation_cap()` calculates bucket limits via `int(round(batch_cap * float(share) * tolerance))`. When `share` or `tolerance` is `NaN` or `inf`, this raises `ValueError` or `OverflowError`. Furthermore, when `batch_cap <= 0`, `allowed[bucket] = max(1, 0) = 1` forces at least one item to be selected, ignoring the batch cap request of 0.
- **Reproduction:** Calling `apply_saturation_cap(pool, batch_cap=0, archive_shares={"landscape": 0.5}, bucket_of=lambda x: x["bucket"])` returns a non-empty candidate list. Calling with `archive_shares={"landscape": float("nan")}` raises `ValueError: cannot convert float NaN to integer`.
- **Test Gate:** `pytest tests/test_selection_lenses.py`

### Finding 2: Rocchio Rating NaN Filtering ([#709](https://github.com/stranske/Fine-Art-Archive/issues/709))
- **File & Lines:** `src/fine_art_archive/preference/rocchio.py:124-173`
- **Defect:** `build()` collects scored works with `[(features_of(sc), s) for sc, s in rated if s is not None]`. When a score `s` is `NaN`, comparisons `s > split` and `s < split` evaluate to `False`, treating all ratings as ties at median `NaN` and producing an empty `PreferenceVector` with `split_value=nan`.
- **Reproduction:** Passing `[(work_a, float("nan")), (work_b, 9.0), (work_c, 3.0)]` to `build()` calculates `split = nan`, `pos = []`, `neg = []`, emitting a corrupted empty preference model.
- **Test Gate:** `pytest tests/test_rocchio_preference.py`

### Finding 3: Variant Metadata Deepcopy During Inheritance ([#710](https://github.com/stranske/Fine-Art-Archive/issues/710))
- **File & Lines:** `src/fine_art_archive/identity/variants.py:427-431`
- **Defect:** `inherit()` fills empty metadata fields from parent sidecar using direct reference assignment `meta[field] = parent_value`. For mutable containers (e.g., `artist`, `holder`, `site`, `rights`), in-place modifications to the child sidecar mutate parent metadata in memory.
- **Reproduction:** `meta, filled, conflicts = inherit(parent_meta, child_meta)`; mutating `child_meta["artist"]["name"] = "Modified"` alters `parent_meta["artist"]["name"]`.
- **Test Gate:** `pytest tests/test_variants.py`

### Finding 4: Dimension Utils Finite Tolerance Guard ([#711](https://github.com/stranske/Fine-Art-Archive/issues/711))
- **File & Lines:** `src/fine_art_archive/parsers/dimension_utils.py:88-120`
- **Defect:** `dim_compat()` compares dimensions against `tolerance` with `difference <= tolerance`. When `tolerance` is `NaN` or negative, `difference <= tolerance` evaluates to `False` even for identical dimensions (`dim_compat("50 x 50 cm", "50 x 50 cm", tolerance=float("nan"))` returns `('mismatch', 0.0)`).
- **Reproduction:** Calling `dim_compat("50 x 50 cm", "50 x 50 cm", tolerance=float("nan"))` returns `('mismatch', 0.0)`.
- **Test Gate:** `pytest tests/test_dimension_utils.py`

### Finding 5: Eink Palette Acuity Blur Radius Non-Finite Validation ([#712](https://github.com/stranske/Fine-Art-Archive/issues/712))
- **File & Lines:** `src/fine_art_archive/eink/palette.py:422-434`
- **Defect:** `acuity_blur_radius()` validates inputs with `if ppi <= 0 or viewing_distance_cm <= 0: raise ValueError(...)`. When `ppi` or `viewing_distance_cm` is `NaN`, `nan <= 0` evaluates to `False`, bypassing the guard and returning `nan` silently instead of raising `ValueError`.
- **Reproduction:** Calling `acuity_blur_radius(float("nan"), 50.0)` returns `nan` without raising `ValueError`.
- **Test Gate:** `pytest tests/test_dither_metric_discriminates.py`

### Finding 6: API Atomic Sidecar UTF-8 Encoding ([#713](https://github.com/stranske/Fine-Art-Archive/issues/713))
- **File & Lines:** `src/fine_art_archive/api/main.py:1397-1411`, `1413-1417`
- **Defect:** `_write_sidecar_atomic()` and `_append_subject_tag_event()` open file handles with `os.fdopen(fd, "w")` and `open(SUBJECT_TAG_EVENTS, "a")` without specifying `encoding="utf-8"`. On environments where default locale encoding is ASCII or non-UTF-8, serializing sidecars containing non-ASCII artist names or titles raises `UnicodeEncodeError`.
- **Reproduction:** Writing sidecars with Unicode strings (e.g. `Albrecht Dürer`) when `LC_ALL=C` raises `UnicodeEncodeError: 'ascii' codec can't encode character '\xfc'`.
- **Test Gate:** `pytest tests/test_eink_feed_endpoints.py`

### Finding 7: Playlist Artist Sort Year 0 Coercion ([#714](https://github.com/stranske/Fine-Art-Archive/issues/714))
- **File & Lines:** `src/fine_art_archive/eink/playlist.py:400-401`
- **Defect:** `sort_value()` implements artist sorting as `return (row["artist"].lower(), row["year"] or 9999)`. Because `0` is falsy in Python, artworks dated to astronomical year `0` (1 BC) are coerced to `9999` and sorted after modern works instead of before year 1.
- **Reproduction:** Sorting playlist items with `year=0` and `year=1500` under artist sort places `year=0` at `(artist, 9999)`, ordering it after `1500`.
- **Test Gate:** `pytest tests/test_eink_pipeline.py`

### Finding 8: Propose Subject Tags Encoding & Directory Creation ([#715](https://github.com/stranske/Fine-Art-Archive/issues/715))
- **File & Lines:** `scripts/propose_subject_tags.py:509-545`
- **Defect:** Sidecar reading, sidecar writing, and `PREVIEW_CSV` writing use `read_text()`, `write_text()`, and `open(PREVIEW_CSV, "w", newline="")` without `encoding="utf-8"`, and `PREVIEW_CSV` writing fails if `PREVIEW_CSV.parent` does not already exist.
- **Reproduction:** Running `propose_subject_tags` with `FAA_WORKSPACE` pointing to a new path raises `FileNotFoundError` when attempting to open `PREVIEW_CSV`.
- **Test Gate:** `pytest tests/test_propose_subject_tags.py`

---

## 4. Verification & Linting Evidence

- **Pre-Submit Linter:** `issue_lint.py` evaluated all 8 markdown files:
  - `01-saturation-cap-non-finite-and-zero-cap.md`: **PASS**
  - `02-rocchio-nan-rating-filtering.md`: **PASS**
  - `03-variant-inherit-deepcopy-mutable-metadata.md`: **PASS**
  - `04-dimension-utils-finite-tolerance-guard.md`: **PASS**
  - `05-acuity-blur-radius-finite-validation.md`: **PASS**
  - `06-api-sidecar-atomic-utf8-encoding.md`: **PASS**
  - `07-playlist-artist-sort-year-zero-falsiness.md`: **PASS**
  - `08-propose-subject-tags-utf8-and-dir-creation.md`: **PASS**

- **Remote GitHub Actions Status:**
  - `Agents Issue Format Guard` workflow executed for each issue on creation and achieved terminal conclusion `completed success` on all 8 issues.

---

## 5. Artifacts and Audit Trail

- **Target Checkout:** `clones/Fine-Art-Archive` @ `9d6d61918cf2153d043c298b1ba3b1cb2aa7f6af`
- **Durable Ledger:** `Code/Audits/AUDIT_LEDGER.md` (updated)
- **Repo History:** `Code/Audits/Fine-Art-Archive/README.md` (updated)
- **Repo Map:** `Code/Audits/Fine-Art-Archive/2026-09-06-00-repo-map.md`
- **Audit Run Log:** `Code/Audits/Fine-Art-Archive/2026-09-06-audit-run.md`
- **Verification Log:** `Code/Audits/Fine-Art-Archive/2026-09-06-verification-log.md`
- **Canonical Report:** `Code/Audits/Fine-Art-Archive/2026-09-06-AUDIT_REPORT.md`
- **Issue Bodies:** `Code/Audits/Fine-Art-Archive/2026-09-06-issue-bodies/` (01..08)
- **Intake Log:** `~/.codex/orchestrator/measurement/intake-2026-09-04.log` (8 entries added)
- **Unit Checkpoint:** `artifacts/audits/D-audit-Fine-Art-Archive--2026-09-06T04-25-53Z.CHECKPOINT.md`
- **Global Checkpoint:** `artifacts/audits/CHECKPOINT.md`
