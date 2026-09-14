## Why

Current failure-path break: `etl/edgar_flow.py:395` indexes raw text using a separate db_path connection before filing writes at `etl/edgar_flow.py:405`. `embeddings.py:131` commits that connection independently. Forced filing upsert failure left one indexed document and zero filings. The scheduled wrapper still routes through this code at `etl/edgar_flow.py:449`; the generic ingestion transaction fix did not cover it.

## Scope

Per-filing database transaction and connection lifetime in the scheduled EDGAR compatibility wrapper.

## Non-Goals

Do not require object-store rollback or change the filing parser. Scaffold-only completion does NOT count: adding try/finally while the document writer still commits separately is a failure of this issue.

## Tasks

- [ ] Extend the wrapper in `etl/edgar_flow.py` to pass its existing connection to document storage, using the connection-aware contract in `embeddings.py`.
- [ ] Put document, filing and holdings writes in one rollback boundary with unconditional connection cleanup in `etl/edgar_flow.py`; keep object-store retention separate.
- [ ] Add fault-injection tests to `tests/test_edgar_flow.py` that use the real document writer and force parsing, filing-upsert, and holdings-write failures after indexing.

## Acceptance Criteria

- [ ] pytest tests/test_edgar_flow.py must pass; each new post-index failure test must leave zero new document, filing, and holding rows and close the connection. A successful filing still writes all three database records and emits its event after commit.
- [ ] Deliberate-break gate: Restore db_path-only document storage in `etl/edgar_flow.py`; the new post-index rollback test in `tests/test_edgar_flow.py` must fail by observing an orphan document; revert and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Offline fault injection used a synthetic adapter, in-memory object-store stub, and real SQLite document writer; observed documents=1 and filings=0. Closed 1628 addressed generic ingestion, not this scheduled persistence fork.
