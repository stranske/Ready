## Why (verified evidence)

`stranske/Doc-Lineage#35` merged the clause blackline engine for `#10`, but the issue requires a production-code deliberate break on the semantic-only path that is not evidenced in the squash diff or PR body.

- `src/doc_lineage/blackline.py::align_sections` pairs numbered sections by stable section IDs and fails closed to `manual_review` on low confidence (merge SHA `a58a60ed8351b7125c06c2d59cb8819db08b9da7`).
- `tests/blackline/test_section_id_pairing.py::test_pairs_by_section_id` passes on the golden LPA fixture pair.
- Issue `#10` requires forcing a semantic-only path that pairs wrong sections, confirming the named gate FAILS, reverting, and recording both outcomes in the PR.
- PR #35 includes `test_deliberate_break_semantic_only_pairs_wrong_sections`, which compares `align_sections` output against a test-local `_misaligned_pairs_for_test` helper without mutating `src/doc_lineage/blackline.py` or pasting RED/GREEN output.

## Tasks

- [ ] In a follow-up PR linked to `#10`, temporarily route pairing through a semantic-only branch in `src/doc_lineage/blackline.py::align_sections` that ignores section IDs.
- [ ] Run `pytest tests/blackline/test_section_id_pairing.py::test_pairs_by_section_id -q` and capture failing output.
- [ ] Revert and capture passing output; paste both blocks in the PR body.

## Acceptance Criteria

- Named test: `tests/blackline/test_section_id_pairing.py::test_pairs_by_section_id` passes on `main`.
- Deliberate-break → revert: semantic-only pairing in `src/doc_lineage/blackline.py::align_sections` → confirm the named test FAILS → revert and confirm it passes. Paste RED and GREEN blocks in the PR.

## Non-Goals

- Do not ship HTML renderer profiles or tracked-variable emission.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-13T01; verified by reading squash diff for PR #35 at merge SHA `a58a60ed`._
