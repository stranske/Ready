## Why
In `src/fine_art_archive/crosswalk.py:117`, `to_linked_art()` constructs the `Production` `carried_out_by` actor using `[_linked_art_actor(_artist_name(meta), artist.get("wikidata_q"))]`. In the archive sidecar schema, resolved artists record their verified Wikidata Q-ID under `artist.canonical.wikidata_q`, leaving `artist.wikidata_q` absent. When projecting sidecars to Linked Art JSON-LD, `to_linked_art()` receives `None` as the Q-ID, omitting the Wikidata entity URI (`id: "https://www.wikidata.org/entity/Q..."`) from the `Actor` entity.

## Scope
- `src/fine_art_archive/crosswalk.py`
- `tests/test_crosswalk.py`

## Non-Goals
- Scaffold-only completion does NOT count: hardcoding specific artist QIDs or modifying the underlying archive sidecar files instead of reading `canonical.wikidata_q` in `to_linked_art()` is a failure of this issue.
- Do not alter the Dublin Core output structure in `to_dublin_core()`.

## Tasks
- [ ] Update `to_linked_art()` in `src/fine_art_archive/crosswalk.py` to check `artist.get("canonical", {}).get("wikidata_q")` before falling back to `artist.get("wikidata_q")`.
- [ ] Add unit tests in `tests/test_crosswalk.py` verifying Linked Art actor records include the Wikidata URI when the sidecar carries a canonical artist QID.

## Acceptance Criteria
- `pytest tests/test_crosswalk.py` passes with all tests green.
- Calling `to_linked_art()` on a sidecar dictionary with `artist={"name": "Vincent van Gogh", "canonical": {"wikidata_q": "Q5582"}}` produces an `Actor` in `carried_out_by` containing `"id": "https://www.wikidata.org/entity/Q5582"`.
- Deliberate break: revert artist QID resolution in `src/fine_art_archive/crosswalk.py` to `artist.get("wikidata_q")`, run `pytest tests/test_crosswalk.py`, and observe test failure; revert to pass.

## Implementation Notes
- Import and use `artist_qid(meta)` or check `artist.get("canonical", {}).get("wikidata_q")` in `src/fine_art_archive/crosswalk.py`.
