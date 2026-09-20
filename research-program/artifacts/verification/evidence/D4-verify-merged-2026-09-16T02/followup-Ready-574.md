## Why (verified evidence)

Post-merge verification (D4-verify-merged-2026-09-16T02) of stranske/Ready#574 (merge `e97c029f5a3e983e1838dec636fd773ed04f232b`) against #554 repaired the research-local allowlist location, but several adversarial publication-safety items from the issue remain unmet in the squash diff.

- `scripts/check_publication_safety.py` / `tests/test_publication_safety.py` expanded, but PKCS#8 and `ENCRYPTED PRIVATE KEY` PEM headers are not covered in `test_credential_patterns` / `test_all_private_key_formats_are_rejected` (diff shows RSA/OPENSSH only).
- No shared header constant wired between scanner and `scripts/prepare_publication.py` exporter in the diff.
- `prepare_publication.py` is documented in README but not wired into `.github/workflows/publication-guard.yml` (workflow unchanged in diff).

## Tasks

- [ ] Add PKCS#8 and ENCRYPTED PRIVATE KEY detection to `scripts/check_publication_safety.py` (shared with exporter if applicable).
- [ ] Extract one shared private-key header set used by both `check_publication_safety.py` and `scripts/prepare_publication.py`.
- [ ] Add one pytest per key format in `tests/test_publication_safety.py`.
- [ ] Wire `scripts/prepare_publication.py` into the publication guard workflow so preparation failures block merge.

## Acceptance Criteria

- Named test: `pytest tests/test_publication_safety.py -k private_key` exits 0 with PKCS#8 and ENCRYPTED fixtures rejected.
- Deliberate-break → revert: remove PKCS#8 header from scanner set → `test_all_private_key_formats_are_rejected` FAILS → restore → passes.

## Non-Goals

- Do NOT revert the research-local allowlist path fix from #574.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-16T02; verified against squash diff `Ready-574.diff` and issue #554. Related: #554, merged PR #574._
