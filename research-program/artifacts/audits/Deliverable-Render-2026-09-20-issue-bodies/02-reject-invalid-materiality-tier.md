## Why

`ChangeRow.__post_init__` in `src/deliverable_render/store/__init__.py:243-248` accepts every nonempty `tier`, while `src/deliverable_render/docx/memo.py:22-26` treats only `T1` and `T2` as material. A reproduced store whose changes all use `T9` loads successfully and then raises the indistinguishable message `No material T1/T2 changes to render` at `src/deliverable_render/docx/memo.py:44-46`. This is a current validation defect: malformed materiality labels are silently treated as an empty memo input instead of being rejected at the input boundary.

## Scope

Validate the documented materiality vocabulary for memo change rows at load time and distinguish malformed input from a legitimate store containing only `T3` changes.

## Non-Goals

- Do not change the current rule in `src/deliverable_render/docx/memo.py` that excludes valid `T3` rows from a material change memo.
- Do not infer or normalize an unknown tier such as `T9` into `T1`, `T2`, or `T3`.
- Do not alter HTML or PPTX rendering contracts in this issue.
- Scaffold-only completion does NOT count: accepting an unknown tier and later reporting only an empty material set is a failure of this issue.

## Tasks

- [ ] Add an explicit allowed materiality set and validation in `src/deliverable_render/store/__init__.py` for `ChangeRow.tier`.
- [ ] Ensure `StructuredStore.from_dict` in `src/deliverable_render/store/__init__.py` raises `StoreValidationError` that identifies the invalid tier before `render_change_memo` runs.
- [ ] Extend `tests/docx/test_validation_and_cli.py` with a `T9` fixture or mutation that asserts the named validation error, while retaining the existing valid-`T3` no-material test.
- [ ] Add a CLI regression in `tests/docx/test_validation_and_cli.py` confirming `render-docx-memo` exits nonzero for the invalid-tier input and does not create the requested DOCX file.

## Acceptance Criteria

- [ ] `python3 -m pytest tests/docx/test_validation_and_cli.py -q` passes with separate assertions for invalid `T9` and valid non-material `T3` input.
- [ ] `tests/docx/test_validation_and_cli.py` proves an invalid tier raises `StoreValidationError` before `src/deliverable_render/docx/memo.py` receives a `StructuredStore`.
- [ ] Deliberate-break gate: temporarily remove the tier-membership check in `src/deliverable_render/store/__init__.py`; the named invalid-tier test must fail, then revert the temporary change before review.

## Implementation Notes

The existing fixture already demonstrates `T1`, `T2`, and `T3` at `tests/fixtures/stores/consultant_change_minimal.json:7-23`. Keep the public exception type `StoreValidationError` so CLI callers receive an input-validation error rather than a false no-material result.
