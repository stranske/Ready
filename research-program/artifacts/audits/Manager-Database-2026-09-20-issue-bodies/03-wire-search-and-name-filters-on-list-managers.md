## Why

Current break on tip 54e4f406: product contract MDB-2 expects `GET /managers` name/search filtering (`docs/PRODUCT_CONTRACT.md:14-22`), but `list_managers` in `api/managers.py:983-1007` accepts only `jurisdiction` and `tag`, and `_count_managers` / `_fetch_managers` in `api/managers.py:498-549` implement no text predicates. Verified: after creating managers "OnlyOne" and "Other", `GET /managers?search=OnlyOne` returns `total=2` with both names.

## Scope

Paginated manager list filtering for optional `search` and `name` query parameters on the REST route and its OpenAPI schema.

## Non-Goals

Do not change universal search at `api/search.py` or remove the existing jurisdiction and tag filters. Scaffold-only completion does NOT count: documenting ignored parameters without SQL filtering is a failure of this issue.

## Tasks

- [ ] Add optional `search` and `name` query parameters to `list_managers` in `api/managers.py:983-1007` and thread them through `_count_managers` and `_fetch_managers` in `api/managers.py:498-549`.
- [ ] Implement case-insensitive substring matching on `managers.name` and alias JSON for `search`, and exact or prefix match for `name`, with dialect-portable SQL consistent with the existing jurisdiction and tag filters.
- [ ] Extend `tests/test_manager_api.py` with two-manager fixtures asserting `search` and `name` each return one row while the unfiltered list returns two.

## Acceptance Criteria

- Named test: `tests/test_manager_api.py::test_list_managers_search_and_name_filters` must pass for both query parameters.
- Deliberate-break → revert: drop the new WHERE clauses in `api/managers.py:498-549`; the named test must fail because both filters return two managers; revert and rerun pytest tests/test_manager_api.py.

## Implementation Notes

Universal search already finds managers by text via `GET /api/search`, but the list route advertises pagination filters in the product contract and currently ignores the parameters entirely.
