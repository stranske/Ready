# Deliverable-Render audit — 2026-09-20

## Verdict

The September 4 template-skeleton closure is stale. Current `main` contains functioning renderer modules, and the local suite passes 133/133 tests (87.41% coverage) at `3adc29fdd019b08a96cdbc4694c06a043b00fcd9`.

Two findings meet the evidence bar. I did not invent a 6–10 issue set: this compact repository does not support that volume of independently verified, non-duplicate work at the current tip.

| Priority | Finding | Evidence | Status |
| --- | --- | --- | --- |
| P1 | A store accepted by the new communication-synthesis validator cannot be consumed by any renderer; only DOCX has a public command. | `README.md:10,27`; `pyproject.toml:30-32`; `src/deliverable_render/store/__init__.py:155-197,281-315`; `src/deliverable_render/store/validate.py:176-263` | Staged, format-valid |
| P2 | An unknown memo tier such as `T9` passes loading and is later mistaken for an empty material set. | `src/deliverable_render/store/__init__.py:243-248`; `src/deliverable_render/docx/memo.py:22-26,44-46` | Staged, format-valid |

## Reproductions and verification

- `tests/fixtures/stores/valid_evidence_store.json` is valid under `validate_store`, but `Store.from_json` fails with `stable_id must be a string (nonempty)` and `StructuredStore.from_json` fails with `changes must be an array`.
- A synthetic memo store whose rows all use `T9` loads, then raises `No material T1/T2 changes to render`, rather than an invalid-tier input error.
- `python3 -m pytest -q` passed: 133 passed in 8.90 seconds.
- `python3 -m ruff check src tests` passed.
- Public Actions data shows current-head scheduled health/keepalive runs succeeding.
- Open public issues #1 and #10, and closed feature issues #2–#6, do not duplicate either finding.

## Filing boundary

The two issue bodies are staged at:

- `artifacts/audits/Deliverable-Render-2026-09-20-issue-bodies/01-canonical-store-rendering.md`
- `artifacts/audits/Deliverable-Render-2026-09-20-issue-bodies/02-reject-invalid-materiality-tier.md`

Both were checked from a clone of the target repository with `.github/scripts/issue_format.py`; body 01 is agent-processable with expected create-path advisories, and body 02 conforms without advisories. Their citations are repository-relative and every existing cited line was reopened at the audited SHA.

No issue was filed and no intake row was added. `gh` reports no authenticated account, so creating an issue and checking the remote Agents Issue Format Guard would falsely imply credential authority. The required Dropbox `Code/Audits` ledger/index writes are also outside this workspace's permitted write roots; this report and the append-only checkpoints preserve the local audit record.

Confidence: high for both retained defects. The P1 finding would be refuted only by a documented, working adapter/CLI path from the validated store to each renderer; the P2 finding would be refuted only if `T9` is a documented valid tier (no such vocabulary exists in the current repo).

## Attempt 2 revalidation — 2026-09-20T09:39:22Z

The remote tip is still `3adc29fdd019b08a96cdbc4694c06a043b00fcd9`. I created a temporary detached worktree at that exact tip because the supplied clone remains on `codex/issue-2` and does not contain the audited renderer files. In the fresh worktree:

- the semantic validator accepted `tests/fixtures/stores/valid_evidence_store.json`, while `Store.from_json` failed on missing `stable_id` and `StructuredStore.from_json` failed on missing `changes`;
- a synthetic `T9` memo row loaded, then raised `No material T1/T2 changes to render`;
- `python3 -m pytest -q` passed 133 tests (87.41% coverage) and `python3 -m ruff check src tests` passed;
- the current issue formatter found body 01 agent-processable with only the three expected new-file advisories, and body 02 fully conforming.

Fresh public-API deduplication still finds only open issues #1 (Dependency Dashboard) and #10 (Agent metrics weekly summary); closed #2–#6 cover the individual HTML, PPTX, DOCX, and validator features but not either verified integration/input-boundary defect. GitHub Actions runs on the exact head are successful. `gh auth status` is still unauthenticated, so the two bodies cannot be filed and no remote format-guard verdict exists. This is a hard authority blocker, not evidence that either issue passed remotely.

## Attempt 3 reconciliation — 2026-09-20T10:00Z

The live remote tip remains `3adc29fdd019b08a96cdbc4694c06a043b00fcd9`. Directly reopening the cited repository-relative lines confirms both defects are still present. A clean detached checkout at that SHA passed `python3 -m pytest -q` (133 passed; 87.41% coverage) and `python3 -m ruff check src tests`.

Both staged bodies were again checked using the target repository's `.github/scripts/issue_format.py`: issue body 01 is agent-processable with only three expected advisories for paths it asks the implementer to add; issue body 02 conforms. Fresh public API inventory contains open #1, #10, and #26 only; #26 is workflow-template synchronization, so it does not duplicate either finding. Public Actions on the exact SHA are successful.

No issues were filed: `gh auth status` says no GitHub host is logged in, and `gh run list -R stranske/Deliverable-Render` refuses for the same reason. Thus the required intake log and remote format-guard check cannot be performed; recording either as completed would be false. The Dropbox `Code/Audits` ledger is also outside the configured writable roots. The two verified, repository-relative bodies remain ready for a credentialed filing run.
