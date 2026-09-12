# Belt promotion queue scan fails: proxy TypeError on `__getTokenSource`

## Context
`Execute / Scan belt promotion queue` has been failing continuously on `main` (head `afb7507`). Latest occurrence: job 103524896686, run 34682931898, 2026-09-12T08:19:37Z. Previous runs (103520070435, 103517519711, 103456672767) failed identically, confirming deterministic failure.

## Evidence
The job aborts with an unhandled runtime error:
```
TypeError: 'get' on proxy: property '__getTokenSource' is a read-only and non-configurable data property on the proxy target but the proxy did not return its actual value (expected '() => currentTokenSource' but got 'function () { [native code] }')
```
Immediately above it in the log:
```js
const detail = status.error
  ? `probe failed for pool ${status.credentialPoolId || "unknown"}: ${status.error}`
  : ...
core.setFailed(`Belt scan deferred — ${detail}`);
```
The intended failure mode is a handled deferral report; the proxy TypeError escapes before `core.setFailed` completes.

## Root cause
A `Proxy` wrapping the credential/token-source object defines a `get` trap returning a bound/wrapped forwarder function instead of the underlying target's exact `currentTokenSource` identity. The ES specification requires a proxy `get` trap to return the identical value of a non-configurable, non-writable data property.

## Tasks
- [ ] Locate the `Proxy` handler intercepting `__getTokenSource` in the belt promotion queue scan path.
- [ ] Return the target's own property value unchanged for `__getTokenSource` (e.g. `Reflect.get(target, prop, receiver)`).
- [ ] Ensure probe failure cleanly reaches `core.setFailed("Belt scan deferred — …")`.

## Acceptance criteria
- [ ] `Execute / Scan belt promotion queue` completes on `main` without an unhandled `TypeError`.
- [ ] Regression test verifies that the proxy returns the exact function reference (`assert.strictEqual`).
