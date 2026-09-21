## Why (verified evidence)

`validate-structured-store` reports success for evidence pointers whose `page` is zero, missing, or a JSON float, but every render CLI rejects those stores during adaptation.

- `src/deliverable_render/store/validate.py:149-180` projects and schema-checks pointers but never enforces a positive one-based page.
- `src/deliverable_render/store/communication.py:69-72` requires `type(page) is int and page >= 1` and raises `positive one-based evidence page required`.
- `tests/store/test_communication_render_profile.py:293-310` already documents the missing-page seam: validation passes, `render-html-hub` exits 2.

User-facing consequence: operators trust a passing validator, then all three synthesis commands fail at render with adapter errors instead of actionable validation diagnostics.

## Reproduction

```bash
cd /path/to/Deliverable-Render
python3 - <<'PY'
import json
from pathlib import Path
from deliverable_render.store.validate import validate_store
from deliverable_render.cli.render_html import main as html_main

store = Path("tests/fixtures/stores/communication_render.json")
paths = Path("tests/fixtures/stores/communication_paths.json")
data = json.loads(store.read_text())

for label, mutate in [
    ("page=0", lambda d: d["entries"][0]["mentions"][0]["src"].update({"page": 0})),
    ("page=3.0", lambda d: d["entries"][0]["mentions"][0]["src"].update({"page": 3.0})),
    ("missing page", lambda d: d["entries"][0]["mentions"][0]["src"].pop("page")),
]:
    payload = json.loads(json.dumps(data))
    mutate(payload)
    p = Path(f"/tmp/evidence-{label.replace(' ', '-')}.json")
    p.write_text(json.dumps(payload))
    assert validate_store(p).valid, label
    rc = html_main(["--store", str(p), "--document-paths", str(paths), "--out", "/tmp/hub.html"])
    assert rc == 2, label
    print(label, "validate=pass render=fail OK")
PY
```

## Tasks

- [ ] In `src/deliverable_render/store/validate.py:149-180`, after `project_evidence`, reject evidence pointers whose resolved page is not a strict positive `int` (cover `page` on the pointer and `locator.page` after projection).
- [ ] In `src/deliverable_render/store/validate.py:41-42` (`ValidationReport.fail`), report code `invalid-evidence-page` with the pointer JSON path when page validation fails.
- [ ] Add validator tests in `tests/store/test_communication_render_profile.py` covering `page: 0`, missing page, and float `page: 3.0` — each must make `validate_store(...).valid` false before render is attempted.

## Acceptance Criteria

- Named test: `test_validator_rejects_invalid_evidence_page_values` in `tests/store/test_communication_render_profile.py` asserting `validate_store` fails for zero, missing, and float pages on both `mentions[].src` and `pub.src` pointers.
- Deliberate-break → revert: temporarily restore the pre-fix validator (no page check) → confirm the named test FAILS → revert.
- `python3 -m pytest tests/store/test_communication_render_profile.py -q` passes.

## Non-Goals

- Do not relax the render adapter rules in `src/deliverable_render/store/communication.py:69-72`.
- Do not change evidence-object schema minimums in `src/deliverable_render/store/evidence-object-v1.schema.json` without matching validator semantics.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by Track D repo-audit 2026-09-21 (attempt 2, tip 3e479ba); verified by live validate/render reproduction._
