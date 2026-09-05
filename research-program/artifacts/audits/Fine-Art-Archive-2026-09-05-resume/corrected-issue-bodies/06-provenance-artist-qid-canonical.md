## Why
In `src/fine_art_archive/provenance.py:212-216`, helper `_field_value(sidecar, "artist_qid")` extracts the artist QID from a sidecar dictionary using `artist.get("wikidata_q") if isinstance(artist, Mapping) else None`. In the archive schema, canonical resolved artists store their Wikidata identifier under `artist.canonical.wikidata_q`. As a result, `_conflict()` records a missing kept_value for canonical-only artist identifiers when generating the conflict detail in `completeness_report()`. Status counts still come from field_provenance and are unaffected; mirror-populated records also remain readable.

## Scope
- `src/fine_art_archive/provenance.py`
- `tests/test_provenance.py`

## Non-Goals
- Scaffold-only completion does NOT count: modifying the sidecar schema or mutating sidecar dictionaries in memory during report generation is a failure of this issue.
- Do not modify the status taxonomy in `STATUS_ORDER`.

## Tasks
- [ ] Update `_field_value()` in `src/fine_art_archive/provenance.py` to inspect `artist.get("canonical", {}).get("wikidata_q")` when `artist.get("wikidata_q")` is absent.
- [ ] Add unit tests in `tests/test_provenance.py` verifying `_field_value()` returns the canonical Wikidata QID when stored under `artist.canonical`.

## Acceptance Criteria
- `pytest tests/test_provenance.py` passes with zero errors.
- Calling `_field_value({"artist": {"name": "Vermeer", "canonical": {"wikidata_q": "Q41264"}}}, "artist_qid")` returns `"Q41264"`.
- Deliberate break: revert `_field_value()` in `src/fine_art_archive/provenance.py` to read `artist.get("wikidata_q")` only, run `pytest tests/test_provenance.py`, and verify test failure; revert to pass.

## Implementation Notes
- Match the resolver fallback pattern from the artist_qid resolver in `src/fine_art_archive/api/store.py:611`.
