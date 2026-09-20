title:	Capability probe: settle whether WebAssembly and Pyodide actually load in the target environment
state:	CLOSED
author:	stranske
labels:	enhancement, priority:high
comments:	11
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	4
--
## Why

The fleet has invested in WebAssembly-based offline applications (Pyodide and stlite bundles) as the delivery channel for locked-down environments. The work environment's answer to whether that runs there is **unknown**: ordinary JavaScript is confirmed working and in production use, but nothing has ever shipped a WebAssembly payload there to test it. Several tools' delivery strategy therefore rests on an untested assumption, and the cost of finding out is one small file an operator opens once.

Evidence: response section A1, the WebAssembly row, which reads "Unknown, ordinary JavaScript is confirmed working; no tool here has shipped a `.wasm` payload to test the specific case" (https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).

## Scope

A single self-contained probe page an operator opens in a locked-down environment, which reports what that environment actually supports and produces a result the operator can send back without exposing anything about their data.

## Non-Goals

- No telemetry, no network calls, no automatic reporting. The operator reads the result and copies it out deliberately.
- No attempt to run a real application in the probe. It answers capability questions only.
- No environment fingerprinting beyond what the capability answers require. The probe must not collect the machine name, user name, file paths or anything identifying.

## Tasks

- [ ] Add `src/deliverable_render/probe/build_probe.py` emitting one self-contained HTML file.
- [ ] Probe, and report pass or fail for each: WebAssembly instantiation from an inlined module; a Web Worker; `SharedArrayBuffer`; `IndexedDB` write and read; `localStorage`; a `fetch` of a same-directory local file; opening a local-file link in a new tab; and the JavaScript baseline the renderer targets.
- [ ] Include an optional second stage the operator can choose to run, loading a real Pyodide runtime from a local subdirectory, so the probe distinguishes "WebAssembly works" from "a large runtime loads and initializes here".
- [ ] Render results as a table plus a copyable one-line summary string containing only the capability results and the browser's own user-agent-reported engine version.
- [ ] State on the page, in plain language, exactly what the summary string contains and that nothing is transmitted.
- [ ] Add a test that the built probe contains no external resource reference and no network call other than the operator-initiated local runtime load.

## Acceptance Criteria

- [ ] The built probe is one file, opens from a local path, and reports every capability above as pass, fail or blocked.
- [ ] The page makes no request on load, asserted by a test that scans for external references and network calls.
- [ ] The copyable summary contains no path, host name, user name or file listing, asserted by a test over a rendered sample.
- [ ] Disabling WebAssembly in the test harness produces a clear fail rather than a hang or a blank page.

## Test Gate

`tests/test_probe_offline_and_minimal.py`, run by this repo's CI gate. Demonstrate it by deliberately adding a remote script tag to the probe template, confirming the no-external-resource test fails, then reverting and confirming it passes. Record both in the pull request.

## Implementation Notes

This probe answers a question that gates other decisions, so keep it first-class rather than a scratch file: the fleet's Tier-A delivery strategy and this repository's own renderer constraints both depend on the answer. Ship a short operator instruction alongside it, written for someone who will open one file and paste one line back.

