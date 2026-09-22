## Why (verified evidence)

`validate-structured-store` accepts a mention whose `entry_id` names a different entry than the enclosing `entries[]` object, then every render CLI fails during adaptation.

- `src/deliverable_render/store/validate.py:256-263` checks that `mentions[].entry_id` resolves in `entries`, but never requires it to match the enclosing entry's `id`.
- `src/deliverable_render/store/communication.py:104-107` rejects the mismatch with `names another entry` only after validation succeeded.
- `tests/store/test_communication_render_profile.py:423-434` already documents the seam: `validate_store` returns valid while `adapt_store` raises.

User-facing consequence: a store that passes the documented validator still cannot render HTML, PPTX, or DOCX, and the validator gives no warning about the cross-entry attribution error.

## Reproduction

```bash
cd /path/to/Deliverable-Render
python3 - <<'PY'
import json
from copy import deepcopy
from pathlib import Path
from deliverable_render.store.validate import validate_store
from deliverable_render.cli.render_html import main as html_main

store = Path("tests/fixtures/stores/communication_render.json")
paths = Path("tests/fixtures/stores/communication_paths.json")
data = json.loads(store.read_text())
second = deepcopy(data["entries"][0])
second["id"] = "other"
second["mentions"] = []
data["entries"].append(second)
data["entries"][0]["mentions"][0]["entry_id"] = "other"
p = Path("/tmp/cross-entry.json")
p.write_text(json.dumps(data))
assert validate_store(p).valid
rc = html_main(["--store", str(p), "--document-paths", str(paths), "--out", "/tmp/hub.html"])
assert rc == 2
print("validate=pass render=fail OK")
PY
```

## Tasks

- [ ] In `src/deliverable_render/store/validate.py:256-263`, when `mentions[].entry_id` is present, require it to equal the enclosing entry's `id` (use the `entry_id` variable already read at `:247`).
- [ ] Report code `cross-entry-mention` at path `/entries/<index>/mentions/<mention_index>/entry_id` with message naming both IDs when they differ.
- [ ] Add `test_validator_rejects_cross_entry_mention_id` in `tests/store/test_communication_render_profile.py` beside the existing adapter seam test at `:423-434`.

## Acceptance Criteria

- Named test: `test_validator_rejects_cross_entry_mention_id` in `tests/store/test_communication_render_profile.py` asserting `validate_store(...).valid` is false when a mention's `entry_id` names another entry.
- Deliberate-break → revert: remove the new equality check → confirm the named test FAILS → revert.
- `python3 -m pytest tests/store/test_communication_render_profile.py -q` passes.

## Non-Goals

- Do not silently reassign mentions to the enclosing entry during adaptation.
- Do not change orphan-reference checks for `mentions[].q` or evidence `source_id`.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by Track D repo-audit 2026-09-22 (tip 2360128); verified by live validate/render reproduction._
