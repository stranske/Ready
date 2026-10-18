# Keepalive reconciliation — 2026-10-18

Reviewed the recent commits through `3ee1596441813156725aff225c9b0fa844252754`.
The six implementation tasks are supported by the decoder, CLI/preparation
regressions, README and regeneration receipts. The latest earlier commits added
private-key split-run cases, routed DOCX findings through `line_hits`, and tested
malformed Word parts and resource-limit boundaries.

One acceptance checkbox needs reopening:

- [ ] `pytest tests/test_publication_safety.py tests/test_prepare_publication.py` passes.

Running that command with `-m "not slow"` produced 274 passing tests but exited 1:
the existing `--cov=src` configuration measured the unrelated scaffold at 0%,
below its unchanged 80% threshold. This agrees with the earlier evidence; the
checked PR checkbox overstates the result. Broader coverage configuration remains
tracked separately in #623. No coverage configuration or threshold was changed.

Added three CLI regressions for a missing main Word document, an encrypted ZIP
member and an unsupported ZIP compression method. Each requires a nonzero exit,
exact outer-file-only error output without a traceback or package text, continued
scanning of another file, and unchanged DOCX bytes. All three pass.

`pytest -m "not slow" -q` passes: 328 tests, 100% existing scaffold coverage,
unchanged 80% threshold. Ruff passes for the changed test file.

The required whole-repository Black check passes: 89 files unchanged, line length
100 and the requested excludes. The sandbox denies multiprocessing sockets and
the thread-based fallback hangs, so a temporary runner outside the repository
scheduled Black's normal `reformat_one` function serially for every source selected
by its normal CLI. It used Black 26.10.1 with caching disabled; no formatter rules,
source selection or repository files were changed for this workaround.

`python scripts/check_publication_safety.py` exits 0:

```text
files_scanned=3294 home-path=0 credential=0 private-key=0 scratch-path=0 internal-host=0 allowed_hits=11 errors=0
```

`.publication-allow` is unchanged; SHA-256 remains
`fb097006f598e678d946107f0a2a9a2a81dfa32562114fd971caefc28efed5bc`.

GitHub reported [Gate](https://github.com/stranske/Ready/actions/runs/39121185431)
and [Publication guard](https://github.com/stranske/Ready/actions/runs/39121185215)
successful at the reviewed head above. This does not verify the new local commit.
PR #634 was open and ready for review.

The attempted PR-body reconciliation was rejected by the connector with
"MCP tool call requires approval, but approval policy is never". Shell GitHub
access also failed to connect. The PR body could not be updated in this run;
the unchecked acceptance item above records the required handoff.

The commit attempt also failed: `.git` is mounted read-only, so Git could not
create `.git/index.lock`. The test and evidence changes remain uncommitted in
the workspace for the automation runner to collect.
