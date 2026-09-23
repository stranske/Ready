## Why (verified evidence)

The repo README and `docs/contracts/mosaic-core-v1.md` describe user-facing capabilities, but there is no `docs/PRODUCT_CONTRACT.md` (or `CORE_FUNCTIONS.md`) listing core functions in **"a \<user\> can \<do X\> and sees \<Y\>"** form with entry points and probes. Fleet repo-audit scorecards (2026-09-20 onward) require that contract as the canonical core-function list; without it, each audit round re-derives scope from README fragments.

A draft contract from the 2026-09-23 Track D audit is ready at `Code/Audits/Manager-Mosaic/2026-09-23-product-contract.md` in the owner's audit store (six core functions + primary journey + probe command).

## Tasks

- [ ] Add `docs/PRODUCT_CONTRACT.md` by adapting the audit draft (six CF rows, primary journey, probe commands); adjust wording only where the repo's shipped API differs.
- [ ] Link `docs/PRODUCT_CONTRACT.md` from `README.md` in the "What it is" section (one sentence + relative link).
- [ ] In `tests/test_repo_hygiene.py`, add `test_product_contract_documents_core_functions` asserting the file exists and contains the strings `CF-1` through `CF-6`.

## Acceptance Criteria

- Named test: `tests/test_repo_hygiene.py::test_product_contract_documents_core_functions` passes.
- Deliberate-break → revert: remove `docs/PRODUCT_CONTRACT.md` → named test **FAILS** → restore file → test passes.
- `python3 -m pytest -q --no-cov tests/test_repo_hygiene.py::test_product_contract_documents_core_functions` passes.

## Non-Goals

- Do not change runtime behavior of `manager_mosaic` modules; documentation and hygiene test only.
- Do not duplicate full contract text inside `README.md` beyond a short link.
- No scaffolding / TODO-only placeholders in `PRODUCT_CONTRACT.md`.

_Surfaced by Track D repo-audit 2026-09-23; verified by absence of `docs/PRODUCT_CONTRACT.md` on tip e0fe240._
