## Why

`pyproject.toml:58-60` publishes both `Homepage` and `Repository` as `https://github.com/stranske/Template`, although this package is Doc-Lineage. This is a current distribution metadata defect: the wheel's installed `Project-URL` metadata reports Template for both links, sending package users and release tooling to the wrong repository.

## Scope

Correct Doc-Lineage project metadata and make the built distribution's project URLs regression-tested.

## Non-Goals

- Do not rename the distribution, package, or console command in this issue.
- Do not change the Workflows-derived automation URLs under `.github/`.
- Scaffold-only completion does NOT count: changing README hyperlinks without making the built package metadata report `https://github.com/stranske/Doc-Lineage` is a failure of this issue.

## Tasks

- [ ] Replace the Template URLs at `pyproject.toml:58-60` with the canonical `https://github.com/stranske/Doc-Lineage` homepage and repository URLs.
- [ ] Add a distribution-metadata assertion in `tests/test_package_identity.py` that builds or inspects package metadata and checks both project URLs identify Doc-Lineage.
- [ ] Keep the installed package identity checks in `tests/test_package_identity.py:1-22` passing without changing the `doc-lineage` distribution or import name.

## Acceptance Criteria

- [ ] `python -m build --wheel` followed by inspection of the wheel metadata reports `Homepage, https://github.com/stranske/Doc-Lineage` and `Repository, https://github.com/stranske/Doc-Lineage`; `pytest tests/test_package_identity.py` passes.
- [ ] Deliberate-break gate: temporarily restore `https://github.com/stranske/Template` at `pyproject.toml:59`; the new metadata assertion must fail. Restore the Doc-Lineage URL before requesting review.

## Implementation Notes

- Verified current evidence at `pyproject.toml:58-60`.
- Current wheel metadata contains `Project-URL: Homepage, https://github.com/stranske/Template` and `Project-URL: Repository, https://github.com/stranske/Template`.
