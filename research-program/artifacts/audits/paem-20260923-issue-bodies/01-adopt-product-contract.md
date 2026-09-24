## Why (verified evidence)

Fleet repo-audit scorecards (2026-09-20 onward) score core functions from `docs/PRODUCT_CONTRACT.md` or `CORE_FUNCTIONS.md`. This repository has neither file on tip `43a86ec`; the only draft lives in fleet audit storage (`Code/Audits/Portable-Alpha-Extension-Model/2026-09-20-product-contract.md`). Without an in-repo contract, each audit round re-derives F1–F6 from README fragments and risks unscored new surfaces.

## Tasks

- [ ] Add `docs/PRODUCT_CONTRACT.md` by adapting the audit draft (six core functions, primary journey, probe commands); update status column to match current tip (F1–F2 WORKS, F3 PARTIAL on sweep `--png`, F4–F6 not exercised until Streamlit probes exist).
- [ ] Link `docs/PRODUCT_CONTRACT.md` from `README.md` near the product overview (one sentence + relative link).

## Acceptance Criteria

- Named test: `tests/test_product_contract.py::test_product_contract_exists_and_lists_core_functions` asserting the file exists and contains at least six `F*` core-function rows with entry points.
- Deliberate-break → revert: delete `docs/PRODUCT_CONTRACT.md` → named test **FAILS** → restore file → test passes.

## Non-Goals

- Do not change simulation logic or CLI behavior in this issue.
- No scaffolding / TODO-only placeholders in `PRODUCT_CONTRACT.md`.

_Surfaced by Track D repo-audit 2026-09-23; verified by `Glob`/`grep` showing no `docs/PRODUCT_CONTRACT.md` in the repository._
