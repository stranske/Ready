# Issue 622: publication vocabulary and preparation dispositions

At base `b661e20700352d79c8bfd86a09b4fa6aac723502`, scanner marker spans and preparation full-value spans were duplicated outside the already shared PEM grammar. This change centralizes only the existing vocabulary. Scanner rule order and preparation replacement order remain unchanged. It adds no token families or exception policy.

## Executed local evidence

`python -m pytest tests/test_publication_safety.py tests/test_prepare_publication.py -q -o addopts=''`: **360 passed**, then **360 passed** after byte-identical restoration of both deliberate mutations. This is local Python validation, not hosted CI or publication/confidentiality approval.

The independent witnesses cover all seven credential prefixes, home-prefix/full username removal, all three scratch markers, qualified and bare local-host suffixes, and localhost ports. Entire prepared strings are asserted, including sensitive synthetic suffix, username and hostname removal. The real copy/preparation/scan path preserves source bytes. The inventory check requires every vocabulary alternative to have a witness, every scanner rule to have a documented preparation disposition, and every non-PEM lexical alternative to appear in the corresponding full-value redactor expression (without requiring scanner/redactor regex equality).

Existing controls retain complete PEM removal across qualified labels, incomplete-block refusal before writes, reviewed exact-file incomplete fixtures, structured data validity, and binary preservation with subsequent scan refusal. The binary matrix covers every non-PEM lexical alternative plus complete PEM blocks.

## Deliberate disconnections

1. Temporarily removed only `AIza` from the actual full-value credential replacement in `scripts/publication_patterns.py`, retaining scanner detection and VOCABULARY. Command: `python -m pytest tests/test_prepare_publication.py::test_scanner_vocabulary_has_explicit_preparation_dispositions tests/test_prepare_publication.py::test_shared_vocabulary_through_real_preparation_and_scan -k "AIza or preparation_dispositions" -q -o addopts=''`. Result: **2 failed, 14 deselected** (inventory: `credential alternative 'AIza' missing from redactor`; behavioral: prepared text retained `AIzaSYNTHETIC_SUFFIX-123_abc`). Restored exact bytes: **2 passed**.
2. Temporarily disconnected the credential rule at the actual `RULES = SCANNER_RULES` consumer in `scripts/check_publication_safety.py`. Command: `python -m pytest tests/test_prepare_publication.py -k "shared_vocabulary_through_real_preparation_and_scan or preparation_dispositions" -q -o addopts=''`. Result: **8 failed, 8 passed, 116 deselected** (`RULES is SCANNER_RULES` and credential KeyError regressions). Restored exact bytes: **16 passed, 116 deselected**, then the named complete suite passed **360/360**.

Neither mutation is committed. Black check passed (`89 files would be left unchanged`). Default research-tree scan result is recorded below separately; synthetic tests do not authorize publishing the research tree.

Default publication scan (`python scripts/check_publication_safety.py`): exit **0**, `files_scanned=3301`, all five rule totals **0**, `allowed_hits=11`, `errors=0`. Existing allowlist and research bytes were unchanged. This is scanner evidence only.

## Follow-up: exhaustive structured-text witnesses

The vocabulary matrix now runs each alternative through plain text, JSON and JSONL, including fully Unicode-escaped JSON strings. Structured cases exercise object keys and nested values, check complete decoded output, and retain public values and JSONL blank lines. All cases still verify source-byte preservation and the subsequent scanner result. This adds 60 cases without changing publication policy.

Temporarily removing only `AIza` from the preparation replacement in memory made all five matching format cases fail (**5 failed, 187 deselected**); the process restored the original replacement tuple afterward. No source mutation was written. The restored full suite passed **420 tests** using `-m 'not slow'`.

Targeted coverage command: `python -m pytest tests/test_publication_safety.py tests/test_prepare_publication.py -q -o addopts='' -m 'not slow' --cov=scripts.prepare_publication --cov=scripts.check_publication_safety --cov=scripts.publication_patterns --cov-report=term-missing`. Result: **420 passed**; preparation **91%**, scanner **88%**, shared patterns **100%** (combined **89.58%**, exceeding the configured 80% gate).

The default publication scan again passed: **3301 files**, zero unallowed findings, **11 allowed hits**, zero errors. Ruff and `git diff --check` passed. Black checked all **89** tracked Python files individually with a writable temporary cache, then the required repository-wide Black command passed using that cache and one worker; this avoids a sandbox hang in Black's worker completion handling. The allowlist, publication implementation and research source files were unchanged.

## Follow-up: overlapping markers and replacement order

Reconciled the implementation and follow-up commits through `4b68994a` against PR #637. The live PR already had all four tasks and five acceptance criteria checked, and was open with `draft=false`. The baseline suite passed **420 tests**. Updating the PR validation paragraph was rejected by the connector because approval policy is `never`; no checkbox changes were necessary.

Added six cases in `test_overlapping_vocabulary_preserves_replacement_order`, spanning plain text, JSON and JSONL. A complete PEM block contains credential, home, scratch and host markers; the expected output and counts require PEM removal before replacements inside its body. A home path containing a scratch marker requires full username removal before the bare home-prefix fallback. Each case also verifies public surrounding text, source-byte preservation, a clean subsequent scan, and byte-preserving repeated preparation.

Deliberate mutations used the real preparation replacement tuple in memory and restored it in `finally`, without writing implementation files:

- Swapping replacement entries 0 and 1 (PEM and credential), then running the new test with `-k 'overlapping_vocabulary and pem'`, produced **3 failed, 195 deselected**. Counts included an unexpected credential replacement inside the PEM block.
- Swapping entries 2 and 3 (full home and bare marker), then running with `-k 'overlapping_vocabulary and full-home'`, produced **3 failed, 195 deselected**. Prepared values retained the synthetic username.
- The restored implementation passed all **6** new cases. The targeted coverage command from the preceding section then passed **426 tests** with preparation **91%**, scanner **88%**, shared patterns **100%**, and combined coverage **89.58%**, above the configured 80% gate. All runs used `-m 'not slow'`.

The default publication scan passed again: **3301 files**, zero unallowed findings, **11 allowed hits**, zero errors. Ruff and `git diff --check` passed. The required repository-wide Black check passed for **89 files** after populating its temporary cache with individual file checks; the initial uncached worker run timed out during completion. Publication code, policy and research source files remain unchanged.

Handoff limitation: staging and committing these two files failed because this run mounts `.git` read-only (`Unable to create .git/index.lock: Read-only file system`). The validated changes remain uncommitted in the working tree.
