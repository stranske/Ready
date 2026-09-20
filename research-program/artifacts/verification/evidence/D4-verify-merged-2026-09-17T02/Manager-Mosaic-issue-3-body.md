## Why

The mosaic is the capability the owner's work environment does not have and cannot easily build there: one place where a fact drawn from any manager communication source carries its evidence, contradictions between sources surface on their own, and a written investment thesis is monitored against what the documents actually say. The response describes the nearest existing tool as phase one only, a hand-edited structured data file rendered to a single page, and names two failure modes that this repo has to design against rather than rediscover.

The two failures are specific and both are silent. A single mistyped internal identifier made an entire record vanish from the rendered view with no error at all. And a shell text substitution over the data file turned a dollar figure into a fragment while leaving the file syntactically valid, because the amount was read as a capture-group reference. Valid is not the same as undamaged. Separately, the response states the rule that must be an invariant here: **silence in a document is weak evidence, never proof that a position was exited** — inferring a removal from an absence has already produced a wrong finding.

Evidence: response section D, the communication synthesis tool, and section D's field list (https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).

## Scope

The core data model plus its validator: facts with evidence, entities, periods, themes, thesis claims, and gaps. No rendering and no extraction.

## Non-Goals

- No renderer. Rendering belongs to `stranske/Deliverable-Render`.
- No extraction. Document identity and text extraction belong to `stranske/Doc-Lineage`.
- No new names where the existing tool has one. Adopt its field names.
- No proprietary content. Fixtures are synthetic.

## Tasks

- [ ] Add `src/manager_mosaic/model.py` with the existing tool's shapes: `fund(name, manager, strategy, archetype, note)`; `period(id, sort, label, kind, title, author, attendees, verdict, note)`; `entry(id, name, ticker, counterparty, first, last, status, peak, flag, thesis)` carrying `pub(state, as_of, detail, src)` and `mentions[(period, text, bps, size, src, inferred)]`; `theme(id, name, desc, periods)`; `document(name, date, verdict, note)`; `gap(sev, title, desc)`.
- [ ] Keep `pub.state` a closed set of `PENDING, COMPLETED, TERMINATED`, and make the entry status vocabulary configurable per position kind rather than hard-coded, since the response records two different vocabularies in use.
- [ ] Require every `mention` to carry `src`, and make `inferred` explicit rather than defaulted, so an inference can never be read as an observation.
- [ ] Add `validate(store)` that fails on: an identifier referenced but not defined; an identifier defined twice; a mention whose `src` names an unknown document; a numeric field that is not finite; and a value that looks like a truncated currency amount, meaning a bare currency suffix with no digits.
- [ ] Make the validator report every violation in one pass with the record identifier, never the first one only.
- [ ] Add `derive_gaps(store)` computing an absence of coverage as a `gap` record, and assert in tests that no code path converts a gap into a status change.
- [ ] Publish JSON Schema for the store under `schemas/` and validate all fixtures against it.

## Acceptance Criteria

- [ ] A store with one mistyped entry identifier fails validation naming that identifier; the record does not silently disappear.
- [ ] A store containing a currency value damaged to a bare suffix fails validation.
- [ ] A mention without `src` fails validation.
- [ ] A period in which an entry is not mentioned produces a `gap` and leaves the entry's `status` unchanged, asserted directly.
- [ ] The validator returns all violations for a fixture seeded with four distinct defects.

## Test Gate

`tests/test_model_validation.py`, run by this repo's CI gate. Demonstrate it by deliberately making `derive_gaps` set an entry status to exited on an absence, confirming the silence invariant test fails, then reverting and confirming it passes. Record both outcomes in the pull request.

## Implementation Notes

The store is meant to be edited by a person, so the validator is the safety net that makes hand editing viable. Prefer a format that survives hand editing and refuses ambiguity, and state in the module docstring that editing a rendered output instead of the store is a discarded edit.

