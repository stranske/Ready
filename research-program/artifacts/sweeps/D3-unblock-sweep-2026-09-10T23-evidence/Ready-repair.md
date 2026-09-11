# Ready CI Repair Specification
**Failure**: `black --check` failed on 29 mirrored proof scripts under `research-program/artifacts/audits/`.
**Root Cause**: `pyproject.toml` lacks exclude pattern for `research-program/artifacts/audits/`.
**Ownership**: Existing issue [#557](https://github.com/stranske/Ready/issues/557) tracks the pyproject.toml exclusion repair.
