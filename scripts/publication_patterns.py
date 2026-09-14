"""Shared PEM private-key patterns for publication scanning and redaction."""

import re

# Include unqualified PKCS#8 and any algorithm/encryption-qualified PEM label.
PRIVATE_KEY_LABEL = r"(?:[A-Z0-9]+[ -])*PRIVATE KEY"
PRIVATE_KEY_HEADER_TEXT = rf"BEGIN {PRIVATE_KEY_LABEL}"
PRIVATE_KEY_HEADER = re.compile(PRIVATE_KEY_HEADER_TEXT)
PRIVATE_KEY_HEADER_BYTES = re.compile(PRIVATE_KEY_HEADER_TEXT.encode("ascii"))
# A nested header must not hide an incomplete block during redaction.
PRIVATE_KEY_BLOCK = re.compile(
    rf"-----BEGIN (?P<label>{PRIVATE_KEY_LABEL})-----"
    rf"(?:(?!BEGIN {PRIVATE_KEY_LABEL}).)*?-----END (?P=label)-----",
    re.S,
)
