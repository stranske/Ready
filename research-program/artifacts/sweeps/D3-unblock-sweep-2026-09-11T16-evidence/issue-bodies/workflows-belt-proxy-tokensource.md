# Belt promotion queue scan fails: proxy TypeError on `__getTokenSource`

## Context
`Execute / Scan belt promotion queue` has been failing on `main` (head `afb7507`). Latest
occurrence: job 103342172996, 2026-09-11T16:39:59Z. Two earlier runs at the same head failed
identically (103335245099, 103322320923), so this is deterministic, not a flake.

## Evidence
The job aborts with an unhandled error rather than a handled "scan deferred" path:

```
TypeError: 'get' on proxy: property '__getTokenSource' is a read-only and non-configurable
data property on the proxy target but the proxy did not return its actual value
(expected '() => currentTokenSource' but got 'function () { [native code] }')
```

Immediately above it in the same log, the script's own deferral branch is present:

```js
const detail = status.error
  ? `probe failed for pool ${status.credentialPoolId || 'unknown'}: ${status.error}`
  : ...
core.setFailed(`Belt scan deferred — ${detail}`);
```

so the intended failure mode is a reported deferral; the proxy TypeError escapes before that
can run.

## Root cause (to confirm)
A `Proxy` wrapping the credential/token-source object defines a `get` trap that returns a
different function identity than the underlying target's non-configurable, non-writable
`__getTokenSource` data property. The ES spec invariant requires a `get` trap to return the
exact value of a non-configurable non-writable data property, so V8 throws. The trap is
almost certainly returning a bound/wrapped forwarder (`function () { [native code] }`,
i.e. the result of `.bind()`) instead of `currentTokenSource` itself.

## Tasks
- [ ] Locate the `Proxy` whose handler intercepts `__getTokenSource` in the belt promotion
      queue scan path and identify where the returned function is wrapped or bound.
- [ ] Either return the target's own property value unchanged for `__getTokenSource`
      (e.g. `Reflect.get(target, prop, receiver)` when the property is non-configurable and
      non-writable), or make the underlying property configurable/writable so a wrapper is
      legal.
- [ ] Ensure a probe failure reaches the existing `core.setFailed("Belt scan deferred — …")`
      branch instead of throwing, so the job reports a cause rather than an engine error.

## Acceptance criteria
- [ ] `Execute / Scan belt promotion queue` completes on `main` without an unhandled
      `TypeError`.
- [ ] A regression test constructs the proxy over a target carrying a non-configurable,
      non-writable `__getTokenSource` and asserts the trap returns the identical function
      reference (`assert.strictEqual`), not merely a callable.
- [ ] A simulated probe failure produces the `Belt scan deferred — …` message.

## Test gate
Named gate: the new regression test above. Demonstrate it is load-bearing by temporarily
restoring the wrapping/binding behaviour in the trap, confirming the test fails with the
proxy invariant `TypeError`, then reverting.

## Non-goals
- Do not disable, skip, or `continue-on-error` the belt scan step.
- Do not remove the proxy layer wholesale as a shortcut.
- No scaffolding, stubs, or placeholder implementations.

## Evidence paths
Run logs: `https://github.com/stranske/Workflows/actions/runs/34620...` job `103342172996`.
Sweep evidence: `research-program/artifacts/sweeps/D3-unblock-sweep-2026-09-11T16-evidence/Workflows.checks.tsv`.
