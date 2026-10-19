"""Existing publication vocabulary with distinct scanner and full-value redaction spans."""

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


# Existing lexical alternatives only. Matching spans intentionally differ: the
# byte scanner detects markers, while preparation removes whole text values.
VOCABULARY = {
    "home-path": ("/Users/",),
    "credential": ("sk-ant-", "sk-proj-", "ghp_", "github_pat_", "lsv2_", "crsr_", "AIza"),
    "private-key": (PRIVATE_KEY_HEADER_TEXT,),
    "scratch-path": ("clones/", "/private/tmp/", "scratchpad/"),
    "internal-host": (".local:", "localhost:"),
}


def literal_alternatives(values: tuple[str, ...]) -> str:
    return "|".join(re.escape(value) for value in values)


HOME = re.escape(VOCABULARY["home-path"][0])
CREDENTIALS = literal_alternatives(VOCABULARY["credential"])
SCRATCH = literal_alternatives(VOCABULARY["scratch-path"])
LOCAL_SUFFIX, LOCALHOST = map(re.escape, VOCABULARY["internal-host"])
SCANNER_RULES = {
    "home-path": re.compile(HOME.encode("ascii")),
    "credential": re.compile(CREDENTIALS.encode("ascii")),
    "private-key": PRIVATE_KEY_HEADER_BYTES,
    "scratch-path": re.compile(SCRATCH.encode("ascii")),
    "internal-host": re.compile(rf"{LOCAL_SUFFIX}|\b{LOCALHOST}[0-9]+".encode("ascii")),
}
# Preserve ordering: PEM before credentials, full home before its bare marker.
TEXT_REPLACEMENTS = (
    ("private-key", PRIVATE_KEY_BLOCK, "[REDACTED_PRIVATE_KEY]"),
    ("credential", re.compile(rf"(?:{CREDENTIALS})[A-Za-z0-9_-]*"), "[REDACTED_CREDENTIAL]"),
    ("home-path", re.compile(HOME + r"[^/\s\"'`<>]+/?"), "[LOCAL_HOME]/"),
    ("home-path", re.compile(HOME), "[LOCAL_HOME]/"),
    ("scratch-path", re.compile(SCRATCH), "[LOCAL_WORKSPACE]/"),
    (
        "internal-host",
        re.compile(
            rf"\b[A-Za-z0-9_.-]+{LOCAL_SUFFIX}(?:[0-9]+)?|\b{LOCALHOST}[0-9]+|{LOCAL_SUFFIX}"
        ),
        "[LOCAL_HOST]",
    ),
)
# Detection is broader than safe rewriting. These are the existing outcomes,
# not a claim that all byte findings can be removed from every artifact.
PREPARATION_DISPOSITIONS = {
    "home-path": "redact-text; preserve-binary-and-scan",
    "credential": "redact-text; preserve-binary-and-scan",
    "private-key": "redact-complete; reject-incomplete-before-writes; reviewed-exact-file-exception; preserve-binary-and-scan",
    "scratch-path": "redact-text; preserve-binary-and-scan",
    "internal-host": "redact-text; preserve-binary-and-scan",
}
