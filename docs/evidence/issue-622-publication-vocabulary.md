# Issue 622: publication vocabulary and preparation dispositions

At base `b661e20700352d79c8bfd86a09b4fa6aac723502`, scanner marker spans and preparation full-value spans were duplicated outside the already shared PEM grammar. This change centralizes only the existing vocabulary. Scanner rule order and preparation replacement order remain unchanged. It adds no token families or exception policy.

## Executed local evidence

`/opt/anaconda3/bin/python3 -m pytest tests/test_publication_safety.py tests/test_prepare_publication.py -q -o addopts=''`: **358 passed**, then **358 passed** after byte-identical restoration of both deliberate mutations. This is local Python validation, not hosted CI or publication/confidentiality approval.

The new independent witnesses cover all seven credential prefixes, home-prefix/full username removal, all three scratch markers, qualified and bare local-host suffixes, and localhost ports. Entire prepared strings are asserted, including sensitive synthetic suffix removal. The real copy/preparation/scan path preserves source bytes. The inventory check requires every vocabulary alternative to have a witness and every scanner rule to have a documented preparation disposition.

Existing controls retain complete PEM removal across qualified labels, incomplete-block refusal before writes, reviewed exact-file incomplete fixtures, structured data validity, and binary preservation with subsequent scan refusal. The new binary matrix covers every non-PEM lexical alternative.

## Deliberate disconnections

1. Temporarily removed only `AIza` from the actual full-value credential replacement in `scripts/publication_patterns.py`, retaining scanner detection. Command: `python -m pytest tests/test_prepare_publication.py -k shared_vocabulary_through_real_preparation_and_scan -q -o addopts=''`. Result: **1 failed, 14 passed**; the full prepared-value assertion found the synthetic credential unchanged. Restored exact bytes.
2. Temporarily disconnected the credential rule at the actual `RULES = SCANNER_RULES` consumer in `scripts/check_publication_safety.py`. Same command: **7 failed, 8 passed**. Restored exact bytes, then the named complete suite passed **358/358**.

Neither mutation is committed. Run-owned transcripts retain the assertion failures and restoration receipt. Black, Ruff, mypy for the shared vocabulary module, and diff checks passed. Default research-tree scan result is recorded below separately; synthetic tests do not authorize publishing the research tree.

Default publication scan (`python scripts/check_publication_safety.py`): exit **0**, `files_scanned=3301`, all five rule totals **0**, `allowed_hits=11`, `errors=0`. Existing allowlist and research bytes were unchanged. This is scanner evidence only.
