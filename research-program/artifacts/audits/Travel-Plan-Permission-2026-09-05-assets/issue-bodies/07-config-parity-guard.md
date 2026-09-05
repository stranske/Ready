# [P2] Guard shipped YAML defaults against checkout and wheel drift

## Why

Latent fragility, not a current configuration divergence: all five paired YAML files are byte-identical at this head. `src/travel_plan_permission/config_loader.py:35` chooses a filesystem path or packaged fallback, so checkout and wheel execution can consume different copies. `tests/python/test_policy_api.py:1188` checks packaged file existence, but does not compare content. `tests/python/test_template_assets.py:61` separately reads the root mapping. The goal is that checked-in default policy, validation, provider, approval and mapping configuration agree across installation modes; operator-supplied overrides remain intentional.

## Scope

A default-config parity regression gate in existing tests, limited to tracked repository defaults and their packaged copies.

## Non-Goals

Deleting either configuration tree, changing override precedence, or reopening shared-loader refactoring from issue 1151. Scaffold-only completion does NOT count: testing existence of both files while different contents still pass is a failure of this issue.

## Tasks

- [ ] In `tests/python/test_package_data.py`, add `test_packaged_yaml_matches_repo_defaults` parameterized over the five tracked YAML pairs, comparing bytes and naming both files on failure.
- [ ] In `tests/python/test_package_data.py`, add `test_config_parity_guard_detects_one_sided_change` against temporary paired files so a one-sided content change is demonstrably detected.
- [ ] Update `docs/validation-rules.md` to distinguish synchronized checked-in defaults from explicit operator override files and name the parity test command.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_package_data.py::test_packaged_yaml_matches_repo_defaults`; all five default pairs match and a mismatch report identifies the two paths.
- [ ] Deliberate-break gate: temporarily change only `config/policy.yaml`; `tests/python/test_package_data.py::test_packaged_yaml_matches_repo_defaults` must fail the policy pair; revert the break.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

Root and packaged files were independently byte-compared. Existing packaged-default tests protect presence and construction; this adds content equivalence. Retain intentional editable defaults and packaged fallback behavior.
