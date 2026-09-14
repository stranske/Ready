## Why

Current conditional break: `etl/news_flow.py:334` checks each candidate only against preexisting rows, while `etl/news_flow.py:375` saves that candidate list before persistence. The unique insert at `etl/news_flow.py:302` removes an intra-batch duplicate, but alert aggregation at `etl/news_flow.py:202` counts both candidates. Offline reproduction produced one stored row and an alert payload with news_count=2 for two copies of the same URL/publication time.

## Scope

Identity alignment between news persistence and alert aggregation within a source batch.

## Non-Goals

Do not broaden source fetching, change count thresholds, or collapse distinct articles. Scaffold-only completion does NOT count: a unique database row without an accurate emitted event is a failure of this issue.

## Tasks

- [ ] Deduplicate pending non-null URL and publication time identities in `inserted_news_items` in `etl/news_flow.py`, or derive alert candidates from successful inserts using the same persistence identity.
- [ ] Preserve existing handling of already-stored rows and nullable keys in `etl/news_flow.py`.
- [ ] Add intra-batch duplicate and already-persisted duplicate cases to `tests/test_news_flow.py`, capturing the actual news_spike event payload.

## Acceptance Criteria

- [ ] pytest tests/test_news_flow.py must pass; the new intra-batch identity test must store one news row and emit news_count=1 for two identical items; already-stored input must emit no new event.
- [ ] Deliberate-break gate: Restore the pre-batch database-only candidate scan in `etl/news_flow.py`; the new duplicate-batch event test in `tests/test_news_flow.py` must fail with news_count=2; revert and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Proof used task.fn to avoid Prefect server startup and a captured alert sink; no external feeds or notifications were called.
