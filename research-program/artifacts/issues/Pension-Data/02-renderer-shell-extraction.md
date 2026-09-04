## Why

`apps/web/` is the embryonic fleet renderer (`apps/web/README.md:1-17`) but lives only in Pension-Data. **Depends on:** Workflows B2-028 `output-substrate/v1`.

## Scope

Extract `apps/web/static` shell to `packages/renderer-shell/` consumable by Template repo sync.

## Non-Goals

- Do NOT add external CDN deps (`tests/web/test_no_external_cdn.py` must stay green).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Create `packages/renderer-shell/` with `index.html`, `app.js` entrypoints from `apps/web/`.
- [ ] Keep Pension-Data `apps/web/` as thin wrapper importing shell.
- [ ] Ensure `tests/web/test_no_external_cdn.py:6` `WEB_ROOT` still passes.
- [ ] Add `tests/renderer/test_shell_import_smoke.py`.

## Acceptance Criteria

- [ ] Named test: `tests/web/test_no_external_cdn.py` passes unchanged behavior.
- [ ] **Deliberate-break gate:** reintroduce external CDN script tag → test **must FAIL** → revert.

_Surfaced by B2-029._
