## Why (verified evidence)

`validate-structured-store` accepts an entry `pub` object with `src` evidence but neither `detail` nor `state`, then every render CLI fails during adaptation.

- `src/deliverable_render/store/validate.py:273-282` validates `pub.src` evidence pointers only; it does not require publication text.
- `src/deliverable_render/store/communication.py:136-145` builds a publication record and calls `_text(detail, f"{fact_ref} detail")` where `detail = publication.get("detail") or publication.get("state")`, raising when both are absent.
- The render failure (`entries/entry-1/pub detail must be a nonempty string`) appears only after validation succeeded.

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
    if isinstance(entry.get("pub"), dict):
        entry["pub"].pop("detail", None)
        entry["pub"].pop("state", None)
p = Path("/tmp/pub-no-detail.json")
p.write_text(json.dumps(data))
assert validate_store(p).valid
rc = html_main(["--store", str(p), "--document-paths", str(paths), "--out", "/tmp/hub.html"])
assert rc == 2
print("validate=pass render=fail OK")
PY
```

## Tasks

- [ ] In `src/deliverable_render/store/validate.py` inside the entries loop (near `:273-282`), when `pub` is an object with `src`, require that `detail` or `state` is a nonempty string.
- [ ] Report code `missing-pub-detail` at path `/entries/<index>/pub` when both fields are absent or blank.
- [ ] Add `test_validator_rejects_pub_without_detail_or_state` in `tests/store/test_communication_render_profile.py` covering `pub.src` present with both text fields removed.

## Acceptance Criteria

- Named test: `test_validator_rejects_pub_without_detail_or_state` in `tests/store/test_communication_render_profile.py` asserting `validate_store(...).valid` is false when `pub.src` exists but `detail` and `state` are both absent.
- Deliberate-break → revert: remove the new validator branch → confirm the named test FAILS → revert.
- `python3 -m pytest tests/store/test_communication_render_profile.py -q` passes.

## Non-Goals

- Do not invent default publication text from `mentions` or `thesis`.
- Do not require `pub` when only `thesis` is present.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by Track D repo-audit 2026-09-22 (tip 2360128); verified by live validate/render reproduction._
