## Why
In `src/fine_art_archive/api/main.py:1717`, the endpoint `variant_candidate_image` defines parameter `max: int = 900` without FastAPI `Query(..., ge=64, le=12288)` validation bounds. In contrast, companion image endpoints `work_image` (`src/fine_art_archive/api/main.py:2380`) and `modality_image` (`src/fine_art_archive/api/main.py:2393`) enforce `Query(1600, ge=64, le=12288)`. When a client passes `max=0`, negative values, or huge dimensions (e.g. `max=100000000`), `_serve_resized()` passes invalid dimensions to `Pillow` thumbnailing, with max=0 producing HTTP 500 (division by zero) in a synthetic-image reproduction. The declared OpenAPI schema has no minimum or maximum. A huge requested max does not upscale a smaller source: a 100 by 100 input remains 100 by 100. Do not claim request-sized memory allocation from this parameter alone.

## Scope
- `src/fine_art_archive/api/main.py`
- `tests/test_companion_app_api.py`

## Non-Goals
- Scaffold-only completion does NOT count: catching exceptions inside `_serve_resized()` without adding FastAPI request validation on the endpoint signature is a failure of this issue.
- Do not modify path containment checks in `VARIANT_CANDIDATE_ROOTS`.

## Tasks
- [ ] Add `Query(900, ge=64, le=12288, description="Longest side in pixels")` to `variant_candidate_image` in `src/fine_art_archive/api/main.py`.
- [ ] Add API validation tests in `tests/test_companion_app_api.py` verifying `/variant_upgrades/{existing_wid}/candidate_image?max=10` returns HTTP 422 Unprocessable Entity.

## Acceptance Criteria
- `pytest tests/test_companion_app_api.py` passes with all tests green.
- Sending a request to `/variant_upgrades/test-wid/candidate_image?max=10` or `?max=20000` returns HTTP 422 status code.
- Deliberate break: remove `Query(ge=64, le=12288)` from `src/fine_art_archive/api/main.py`, run `pytest tests/test_companion_app_api.py`, and verify the bounds validation test fails; revert to pass.

## Implementation Notes
- Use `Query(900, ge=64, le=12288)` from `fastapi` in `src/fine_art_archive/api/main.py`.
