# Doc-Lineage audit — 2026-09-19

## Outcome

The prior template-only conclusion is obsolete. Remote `main` was refreshed to `278defcb35c212d6dc1fce204e70580c3fb7d28e` and now contains a 3,682-line repo-owned Doc-Lineage application with 4,255 lines of tests. I retained five agent-ready findings. They are not filed: `gh auth status` reports no authenticated GitHub host, so `gh issue create`, labels, and post-file format-guard verification cannot be performed without credentials.

This is a real delivery blocker, not a reason to fabricate issue URLs. The five bodies pass the repository's actual `.github/scripts/issue_format.py` validator with no advisories and are staged beside this report.

## Scope and baseline

- Scope: repo-owned `src/doc_lineage/`, `tests/`, `data/`, package metadata, and app-facing docs.
- Excluded: `.github/` and `tools/` fleet infrastructure, except for the target repository's existing issue-format validator.
- The named dossier and verification table were absent. I used `artifacts/audit-refill.md`, the prior 2026-09-04 Doc-Lineage audit record, the Audit ledger, and current repository evidence.
- `python -m ruff check src tests` passed.
- `pytest --collect-only -q` collected 306 tests. The full local run was 305 passed / 1 failed: its console-script test attempts editable installation into a sandbox-denied user site-packages path. An isolated virtualenv successfully installed the editable package and ran the console command, so I rejected this as an environment failure rather than a source finding.
- The same-head CI and GitHub issue inventory could not be obtained with `gh`; unauthenticated GitHub REST readback found only three open product audit items (#36–#38), none overlapping the retained findings.

## Verified findings

| Priority | Finding | Evidence | Reproduction | Body |
|---|---|---|---|---|
| P1 | Source distribution omits a fixture required by its included fact-key-map export tests | `MANIFEST.in:1`; `tests/export/test_fact_key_map.py:11-15`; `tests/export/test_fact_key_map_cli.py:13-18` | Current sdist contains the export test files but not `tests/fixtures/fact_key_map/tracked_variables.json`; selected export pytest run: 20 failed, 7 passed | `01-sdist-export-fixture.md` |
| P1 | Manifest scan attributes an out-of-root symlink target to an in-library path | `src/doc_lineage/manifest.py:64-74`, `src/doc_lineage/manifest.py:147-159`, `src/doc_lineage/identity.py:73-75` | A temporary PDF symlink inside the library returned a lexical library row carrying the external target SHA-256 | `02-manifest-symlink-containment.md` |
| P2 | Manifest and ingest have incompatible document-size policies | `src/doc_lineage/manifest.py:147-159`; `src/doc_lineage/identity.py:73`; `src/doc_lineage/ingest.py:176`; `src/doc_lineage/adapters/docling_segmenter.py:21,96-104` | A 104,857,601-byte PDF is indexed, then ingest rejects it as beyond the 104,857,600-byte limit | `03-manifest-ingest-size-policy.md` |
| P2 | A failed multi-exhibit EDGAR harvest leaves published partial files | `src/doc_lineage/harvest/edgar_ex10.py:190-216`, `src/doc_lineage/harvest/edgar_ex10.py:290-305` | A two-exhibit fixture with its second content missing leaves the first output file and no final manifest | `04-atomic-harvest-publication.md` |
| P3 | Published package metadata links both project URLs to Template | `pyproject.toml:58-60` | A wheel built from current main reports Template for both installed `Project-URL` entries | `05-package-project-urls.md` |

## Adversarial dispositions

Rejected rather than filed:

- The local console-script test failure: isolated editable and wheel installations work; only the sandbox's user site-packages write was denied.
- Missing `doc_lineage._contracts` and `_vocab` package claims: non-editable wheel installation successfully loaded contract schemas, vocabulary, and executed `doc-lineage ingest`.
- Duplicate console-script declarations: current wheel builds and console invocation succeed; this is non-canonical metadata, not a demonstrated defect.
- Entity-reference validation: `src/doc_lineage/export/fact_key_map.py` matches the tracked-variable contract regex exactly.
- Unbounded generic extraction and live-harvest reads: concern class noted, but no product limit or concrete failed behavior establishes a ready issue yet.

The repository has no browser-observable product UI; the Phase 4 UX coverage row is `not_applicable` rather than a code-only UX score.

## Filing and reconciliation

- Candidate dedup: public REST readback of all issues found #36–#38 open; their deliberate-break transcript scopes do not overlap these five defects. Closed issues #8, #11, #13, #14, and #15 cover earlier ingest, harvest, export, link, and DOCX lanes but not these retained gaps.
- Ready bodies: [issue bodies directory](Doc-Lineage-2026-09-19-issue-bodies/), all 5/5 validator conformant.
- Filing, labels, `gh run list`, format-guard verdicts, and `~/.codex/orchestrator/measurement/intake-2026-09-04.log` rows: not performed because GitHub CLI is unauthenticated. No remote issue or sink URL is claimed.
- The required durable `Code/Audits` ledger/index is outside this unit's writable roots; no out-of-scope write was claimed. This OUT report, the staged bodies, and the append-only checkpoint preserve the resumption state.

## Attempt 2 reconciliation — 2026-09-20

- `git pull --ff-only` confirmed the audited clone is still at `278defcb35c212d6dc1fce204e70580c3fb7d28e`; no source or candidate evidence changed.
- The repository's actual issue validator again accepted all five staged bodies with no advisories. A fresh public issue inventory still contains only open #36–#38 in the relevant audit stream, with non-overlapping deliberate-break scopes.
- The required post-file guard command, `gh run list -R stranske/Doc-Lineage --workflow 'Agents Issue Format Guard'`, remains unavailable because `gh` has no authenticated host. Consequently, no issue body was submitted, no labels or URLs were invented, and there can be no format-guard verdict or intake-sink row.

The correct disposition is **publication blocked**, not done: an authenticated GitHub CLI session (or `GH_TOKEN`) is required. Once available, re-run live deduplication immediately before creation, submit the unchanged five bodies, then read the guard runs and append only returned issue URLs to the intake sink.

## Confidence

High for all five retained findings: each was re-opened at the final unchanged commit, locally reproduced, deduplicated against the public issue inventory, and formatted with the repository's own validator. Filing needs a logged-in `gh` client; restoring that authentication and re-reading current open/recently closed issues is what would allow a follow-up to publish the staged bodies.

## Attempt 3 publication — 2026-09-20

- GitHub authentication was restored. The clone advanced to `35a357123e33402066d1f1f3d039208d7a91e274`, but the five cited application and test paths were unchanged from the audited revision; each body was revalidated from the target clone and all passed. Targeted regression coverage passed: 53 tests across identity/manifest, EDGAR harvest, and package identity; the fact-key-map selection still collects 27 tests.
- Fresh open/recent-closed issue readback found no title or scope duplicate of these five findings. Filed without dispatch labels: [#47](https://github.com/stranske/Doc-Lineage/issues/47), [#48](https://github.com/stranske/Doc-Lineage/issues/48), [#49](https://github.com/stranske/Doc-Lineage/issues/49), [#50](https://github.com/stranske/Doc-Lineage/issues/50), and [#51](https://github.com/stranske/Doc-Lineage/issues/51).
- The Agents Issue Format Guard recorded a successful run for each issue: 35501768509, 35501768546, 35501769541, 35501770141, and 35501770772. Companion duplicate trigger runs were skipped or cancelled; the successful runs are the same-head validation evidence.
