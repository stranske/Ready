# Ready CI Repair Specification
**Failure**: Black check scans mirrored `research-program/artifacts/audits/` python scripts.
**Tracking**: Existing open issue #557 (`[P1] Exclude research-program artifacts from black formatting in pyproject.toml`).
**Fix**: Add exclusion regex in `pyproject.toml` for `research-program/artifacts/` or audit folders.
