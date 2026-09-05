## Why
In `scripts/rank_known_works.py:128-146`, the CLI argument parser defaults `--staging-dir` using `Path(os.environ["FAA_STAGING_DIR"]).expanduser() if os.environ.get("FAA_STAGING_DIR") else None` and raises an error if `--staging-dir` is not set when running with `--missing-only`. The codebase recently extracted `default_works_dir()` in `scripts/_paths.py` to standardize sidecar root resolution across maintenance scripts (checking `FAA_WORKS_DIR`, `FAA_STAGING_DIR`, and `DEFAULT_ART_WORKS_ROOT`). `scripts/rank_known_works.py` was not migrated, causing `--missing-only` to fail unnecessarily when `$FAA_STAGING_DIR` is unset even though `$FAA_WORKS_DIR` or the canonical archive directory exists.

## Scope
- `scripts/rank_known_works.py`
- `tests/test_rank_known_works.py`

## Non-Goals
- Scaffold-only completion does NOT count: inlining duplicate environment checks instead of importing `default_works_dir` from `scripts._paths` is a failure of this issue.
- Do not modify the ranking formula in `rank_by_display_worthiness()`.

## Tasks
- [ ] Update `scripts/rank_known_works.py` to import and use `default_works_dir()` from `scripts._paths` as the default for `--staging-dir`.
- [ ] Add CLI tests in `tests/test_rank_known_works.py` verifying `--missing-only` uses `default_works_dir()` when `--staging-dir` is omitted.

## Acceptance Criteria
- `pytest tests/test_rank_known_works.py` passes.
- Running `scripts/rank_known_works.py --artist-qid Q5582 --missing-only` with `FAA_WORKS_DIR` set in the environment executes without requiring `--staging-dir` or `FAA_STAGING_DIR`.
- Deliberate break: revert `--staging-dir` default in `scripts/rank_known_works.py` to `None`, run `pytest tests/test_rank_known_works.py`, and verify the default path test fails; revert to pass.

## Implementation Notes
- Import `default_works_dir` from `scripts._paths` in `scripts/rank_known_works.py`.
