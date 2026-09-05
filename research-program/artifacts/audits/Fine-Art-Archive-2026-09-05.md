# Track D Audit Run Report: stranske/Fine-Art-Archive (2026-09-05)

- **Unit**: `D-audit-Fine-Art-Archive--2026-09-05T04-00-31Z`
- **Repo**: `stranske/Fine-Art-Archive`
- **Base SHA**: `d149861e60f089868be5aa28373bdf5d3513a290` (tip of `origin/main`)
- **Auditor**: Gemini via Antigravity (agy)
- **Status**: Completed — 9 verified AGENT_ISSUE_FORMAT issues filed on GitHub.

## Summary of Results
A multi-dimensional repository audit was conducted across all 8 dimensions following the `repo-audit` protocol. Baseline checks confirmed clean repository hygiene (`ruff check .` with 0 errors, `black --check .` with 331 files unchanged, and 1,899 test cases passing across 126 test modules).

Adversarial verification was performed by live Python execution of reproduction test scripts against the live tip. 9 high-impact issues were verified, formatted strictly to AGENT_ISSUE_FORMAT standards, passed through the `issue_lint.py` validator with 0 errors, and filed on GitHub.

## Filed Issues

| # | Priority | Title | Target File | GitHub URL |
|---|---|---|---|---|
| 1 | P1 | [P1] Reject non-finite and non-positive shares in lens allocation algorithms | `src/fine_art_archive/selection/lenses.py` | https://github.com/stranske/Fine-Art-Archive/issues/689 |
| 2 | P1 | [P1] Handle offset-naive timestamps in source-quality warmup blending | `src/fine_art_archive/quality/source_quality.py` | https://github.com/stranske/Fine-Art-Archive/issues/690 |
| 3 | P2 | [P2] Resolve canonical artist Q-IDs when projecting Linked Art actors | `src/fine_art_archive/crosswalk.py` | https://github.com/stranske/Fine-Art-Archive/issues/691 |
| 4 | P2 | [P2] Parse 3D dimension strings with trailing units in physical dimension comparison | `src/fine_art_archive/parsers/dimension_utils.py` | https://github.com/stranske/Fine-Art-Archive/issues/692 |
| 5 | P2 | [P2] Bound max pixel dimension on variant candidate image preview endpoint | `src/fine_art_archive/api/main.py` | https://github.com/stranske/Fine-Art-Archive/issues/693 |
| 6 | P2 | [P2] Check canonical artist Q-ID in provenance field value extraction | `src/fine_art_archive/provenance.py` | https://github.com/stranske/Fine-Art-Archive/issues/694 |
| 7 | P2 | [P2] Use default_works_dir in rank_known_works CLI for sidecar root resolution | `scripts/rank_known_works.py` | https://github.com/stranske/Fine-Art-Archive/issues/695 |
| 8 | P2 | [P2] Fall back to year_min when building manifest rows for approximate-date artworks | `scripts/build_manifest.py` | https://github.com/stranske/Fine-Art-Archive/issues/696 |
| 9 | P2 | [P2] Guard None and non-finite values in Bradley-Terry next_pair selection | `src/fine_art_archive/preference/bradley_terry.py` | https://github.com/stranske/Fine-Art-Archive/issues/697 |

## Artifacts & Logs
- Canonical audit report: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Fine-Art-Archive/2026-09-05-AUDIT_REPORT.md`
- Verification log: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Fine-Art-Archive/2026-09-05-verification-log.md`
- Issue bodies: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Fine-Art-Archive/2026-09-05-issue-bodies/`
- Ledger update: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/AUDIT_LEDGER.md`
- Measurement intake log: `~/.codex/orchestrator/measurement/intake-2026-09-04.log`
