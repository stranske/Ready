fix(scheduling): recover losing card-state seed writer with a savepoint (#697)

* fix(scheduling): recover losing card-state seed writer with a savepoint

`get_or_seed_card_state` did a check-then-insert against the unique index
`ux_review_card_states_learner_subject` with no recovery for the losing
writer, so two concurrent first attempts on the same learner/node made one
request fail with an IntegrityError and an HTTP 500 without recording the
attempt.

Port the savepoint-and-requery pattern that `get_or_create_review_policy`
already documents and uses: wrap the add/flush in `session.begin_nested()`,
catch `IntegrityError`, re-query the winning row, reconcile the caller's
requested `retention_tier` onto it, and re-raise when the re-query finds
nothing so a genuine constraint violation is not masked as a missing row.

Closes #689

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

* fix(scheduling): only recover card identity constraint conflicts

---------

Co-authored-by: stranske <tim@stranskemo.com>
Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
