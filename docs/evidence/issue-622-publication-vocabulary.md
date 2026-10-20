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

## Follow-up: complete and incomplete PEM binary dispositions

Reconciled the recent commits through `e7733d47` with PR #637 before making changes. All four tasks and five acceptance criteria were already checked; the PR was open and ready for review. The baseline named suite passed **426 tests**.

Expanded the binary lexical matrix to include every witness, including bare home and host markers. A separate 21-case matrix covers the seven PEM labels already used by the text tests, each with matching, absent and mismatched footers. It verifies byte-preserving binary preparation, subsequent scanner refusal without printing synthetic material, successful preparation of neighboring supported text, and preservation of the entire source tree.

Temporarily disconnecting `private-key` from the scanner's actual `RULES` consumer in memory made all **21** new PEM cases fail because scanning returned success. The original rules were restored in `finally`; no implementation file was written. The restored binary matrix passed **36 tests**, and the full targeted coverage command from the structured-text section passed **447 tests**. Preparation coverage remains **91%**, scanner **88%**, shared patterns **100%**, and combined coverage **89.58%**, above the configured 80% gate. All pytest runs used `-m 'not slow'`.

Ruff and `git diff --check` passed. Black individually verified all **89** tracked Python files, then the required repository-wide command passed using the populated temporary cache and one worker. The initial uncached command reported unchanged formatting but timed out while exiting.

The default publication scan passed: **3301 files**, zero unallowed findings, **11 allowed hits**, zero errors. SHA-256 manifests verified identical bytes for all **3302** policy and research files before and after validation. PR #637 remained open with `draft=false` and all nine checkboxes checked.

The commit attempt was blocked at `git add` because `.git` is mounted read-only (`Unable to create .git/index.lock: Read-only file system`). The test and evidence changes remain in the working tree for the automation runner to commit.

Attempts to post the required blocker comment and add `needs-human` to PR #637 were both rejected by the GitHub connector: `MCP tool call requires approval, but approval policy is never`. No PR metadata was changed by this run.

## Follow-up: exact-file and rule boundaries for reviewed incomplete PEM

Reconciled the recent commits through `0ef8dacc` against the live PR before editing. All nine task and acceptance checkboxes were already checked; PR #637 was open with `draft=false`. The baseline named suite passed **447 tests**, so no checkbox changes were needed.

Added nine preparation cases across text, JSON and JSONL. Three show that a reviewed incomplete PEM fixture survives while complete PEM blocks, credentials and home usernames in that same file are fully redacted. They also verify source/policy preservation, idempotence and the subsequent clean scan. Six enforce exact-path and rule boundaries: an incomplete PEM in a subdirectory with the same basename receives no exception, and an exception for a different rule cannot approve an incomplete PEM. Rejection must leave every staged file unchanged, including an earlier queued rewrite.

A deliberate in-memory mutation broadened the preparation allowlist to approve private-key findings in every staged file. Running `python -m pytest tests/test_prepare_publication.py -q -o addopts='' -m 'not slow' -k incomplete_pem_exception --tb=short` through `pytest.main` with that mutation produced **6 failed, 222 deselected**, each because preparation incorrectly stopped raising. The original loader was restored in `finally`; implementation files were never modified.

The restored targeted coverage command documented above passed **456 tests** with preparation **91%**, scanner **88%**, shared patterns **100%**, and combined coverage **89.58%**, above the configured 80% gate. All runs used `-m 'not slow'`. Black formatted the changed test file and the required repository-wide check passed for **89 files**, using a temporary populated cache and one worker. An initial auxiliary check included archived Python files with their own configuration and reported an excluded artifact; rerunning within the root formatting policy and the required repository-wide command passed. Ruff and `git diff --check` passed.

The default publication scan passed: **3301 files**, all five unallowed rule totals zero, **11 allowed hits**, and zero errors. SHA-256 manifests confirmed all **3302** policy and research files remained unchanged.

`git add tests/test_prepare_publication.py` failed because `.git` is mounted read-only and cannot create `index.lock`. The test/evidence changes therefore require the automation runner to commit them. The connector rejected the PR validation-body update, blocker comment and `needs-human` label with `MCP tool call requires approval, but approval policy is never`; no PR metadata was changed.

## Follow-up: packaged vocabulary and split Word text runs

Reconciled the recent commits through `f0ded502` against live PR #637: all nine task and acceptance checkboxes were already checked, and the PR was open with `draft=false`. The baseline named suite passed **456 tests**, so no checkbox changes were needed.

Added 17 cases in `test_packaged_vocabulary_is_preserved_then_scan_rejected`: every existing non-PEM witness and complete/incomplete PEM examples inside compressed DOCX packages. Every character occupies a separate Word text run, so neither package bytes nor raw XML contains the lexical marker. Preparation must preserve the package bytes, prepare neighboring supported text, and leave the finding for the subsequent scanner to reject without exposing contents. Each case verifies source preservation.

Temporarily replacing only the scanner consumer's credential expression with a never-matching expression in memory produced **7 failed, 10 passed, 228 deselected**: scanning incorrectly returned success for each credential prefix. The original `RULES` mapping was restored in `finally`; no implementation file was written. The original scanner passed all **17** new cases, and the full targeted coverage command documented above passed **473 tests**, with preparation **91%**, scanner **88%**, shared patterns **100%**, and combined coverage **89.58%**, above the configured 80% gate. All pytest runs used `-m 'not slow'`.

Black formatted the changed Python file. Individual checks of the 89 tracked Python files within the root formatting policy populated a temporary cache, and the required repository-wide Black check passed using that cache and one worker. Ruff and `git diff --check` passed. The default publication scan passed: **3301 files**, zero unallowed findings, **11 allowed hits**, zero errors. SHA-256 manifests confirmed unchanged bytes and paths for all **3302** policy/research files. Publication implementation and policy remain unchanged.

The commit is blocked: `git add` cannot create `.git/index.lock` because `.git` is mounted read-only. The validated test/evidence changes remain in the working tree for the automation runner to commit. The GitHub connector rejected the PR validation-body update, blocker comment and `needs-human` label with `MCP tool call requires approval, but approval policy is never`. No PR metadata was changed; all nine checkboxes remain checked and the PR is open and ready for review.
