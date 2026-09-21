## Why (verified evidence)

`validate-structured-store` accepts communication-synthesis entries whose `thesis` or `pub.src` blocks are present but neither `first` nor `last` resolves to a store period, then every render CLI fails during adaptation.

- `src/deliverable_render/store/validate.py:270-278` validates `first`/`last` only when those keys are present and nonempty; it does not require a resolvable period when `thesis` or `pub` needs one.
- `src/deliverable_render/store/communication.py:123-147` builds thesis and publication records using `entry.get("last") or entry.get("first")` and raises when that period is missing or empty.
- The render failure message (`thesis period must be a nonempty string` / `pub period must be a nonempty string`) appears only after validation succeeded.

User-facing consequence: a store that passes the documented validator still cannot render HTML, PPTX, or DOCX.

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
for entry in data["entries"]:
    entry.pop("first", None)
    entry.pop("last", None)
p = Path("/tmp/no-period.json")
p.write_text(json.dumps(data))
assert validate_store(p).valid
rc = html_main(["--store", str(p), "--document-paths", str(paths), "--out", "/tmp/hub.html"])
assert rc == 2
print("validate=pass render=fail OK")
PY
```

## Tasks

- [ ] In `src/deliverable_render/store/validate.py` inside the entries loop (after `entry_path` is known, near `:270-278`), when an entry has a nonempty `thesis` string or a `pub` object with `src`, require that `last` or `first` is a nonempty string referencing a declared period ID.
- [ ] In `src/deliverable_render/store/validate.py:41-42` (`ValidationReport.fail`), report code `missing-entry-period` with path `/entries/<index>/thesis` or `/entries/<index>/pub` when the period cannot be resolved.
- [ ] Add `test_validator_rejects_thesis_or_pub_without_resolvable_period` in `tests/store/test_communication_render_profile.py` covering thesis-only and pub-only cases.

## Acceptance Criteria

- Named test: `test_validator_rejects_thesis_or_pub_without_resolvable_period` in `tests/store/test_communication_render_profile.py` asserting `validate_store(...).valid` is false when `first`/`last` are absent but `thesis` or `pub.src` is present.
- Deliberate-break → revert: remove the new validator branch → confirm the named test FAILS → revert.
- `python3 -m pytest tests/store/test_communication_render_profile.py -q` passes.

## Non-Goals

- Do not infer a default period from `mentions[].q` or other fields.
- Do not change how blank unsourced mentions are skipped (`tests/store/test_communication_render_profile.py:313-324`).
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by Track D repo-audit 2026-09-21 (attempt 2, tip 3e479ba); verified by live validate/render reproduction._
