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
