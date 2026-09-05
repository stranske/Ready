# Verification and reconciliation — D-audit-Travel-Plan-Permission--2026-09-05T16-11-36Z

Time 2026-09-05T16:38:56.584615+00:00; baseline and final remote tip 3ba14a8541b97338586ab6c253ea30e2aed7b86e. All eight draft bodies passed `.github/scripts/issue_format.py` without advisories after the lead corrected line references and slash-delimited prose that looked like paths. Citation text is preserved in /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/citation-verification.json. The generic body-generation script is a provenance artifact; final validated issue bodies are authoritative.

## Candidate dispositions

| Candidate | Disposition | Basis |
| --- | --- | --- |
| Correctness 1: expense export auth | Staged 01, expanded to expense intake and detail permissions | Independent HTTP plus browser CSV download without auth. Known-ID precondition stated; linkage failure control 400. |
| Correctness 2: anonymous exception write | Staged 02 | Independent 303, persisted traveler-attributed exception. Corrected delegate suggestion: view-only handoff cookies must remain unable to mutate. |
| Correctness 3: board exception by generic approver | Staged 08 as P2 design extension | Runtime reproduced, but docs/exception-policy.md:53 permits generic approve-capable roles today. No claim of violating a pre-existing tier-entitlement policy. Real principal mapping is a deployment decision, not invented by this audit. |
| Correctness 4: forged decision actor | Staged 03 | Token subject differs from persisted approval-history actor in runtime proof. Distinct from closed 1506's admin actor_role read. |
| Correctness 5: unsigned placeholder receipt link | Staged 05 | Actual portal constructs default service; placeholder origin plus expiry only. A remote verifier bypass is NOT demonstrated. Corrected design to preserve local receipt-reference option per owner notes. |
| Correctness 6: expense export audit loss on restart | Follow-up to closed 1436, not new issue | Independent restart proof reproduced. A closed issue is not evidence of delivery; follow-up note below retains the outstanding result. |
| Lead: XLSX formula text | Staged 04 | Actual XLSX B2/E2 data_type=f for benign =1+1 and =2+2, CSV preserves prefixes. No external formula payload or native Excel execution. |
| Lead/panel: direct browser draft auth dead end | Staged 06 | Completed form leads to raw 401, same draft with token renders; use existing scoped view-cookie contract. |
| Breadth 1: dual YAML parity | Staged 07, downgraded P1 to P2 latent fragility | Five pairs byte-identical; existing tests cover resource presence and construction, not a content-equivalence gate. Intentional operator overrides remain distinct. |
| Breadth 2: config path helper consolidation | Deferred, optional maintenance | Shared loader already delivered by closed 1151. Remaining small path helpers do not establish an observable failure. No duplicate issue. |
| Breadth 3: NetSuite dual-file profile | Deferred pending actual ERP requirement | Oracle permits both single- and multiple-file imports; delegate claim of required two files corrected. No evidence owner uses NetSuite. |
| Breadth 4: format/env-freshness CI | Declined as new issue | Format disabled by explicit repo debt comment; generic synced prompt fixes belong to Workflows. Existing version tests already detect the local Ruff mismatch. CI's fresh runner does not reproduce a stale local venv problem. |
| Flagged expense can still export | Intentionally retained accounting-review handoff | Existing tests and docs encode export for accounting review; no downstream reimbursement release observed. |
| OCR mismatch warnings | Intentional | Manual corrections and advisory OCR documented. |
| Existing policy configuration issues | Deduplicated to open 1507 and 1508 | Current unknown-key/validation override scope already owned. |
| Local-first delivery | Deduplicated to open 1513 | Owner notes and work-environment response read; no hosted-only recommendation. |

## Breadth and sources

Primary URLs were independently opened by the lead on 2026-09-05. Advice remains bounded to what these sources support.

- [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): validate permission on every request and protect identifier-addressed resources. This supports fixing local endpoint omissions; it does not establish an actual production attack.
- [OWASP CSV injection](https://owasp.org/www-community/attacks/CSV_Injection): untrusted cell prefixes may be formulas; quoting alone is not a universal fix and CSV mitigations depend on consumers. Use explicit XLSX text cells and test the declared CSV import behavior.
- [Amazon S3 presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html): signed, limited-duration access is tied to signing credentials and authorization. A timestamp by itself is not equivalent. This is a reference design, not an AWS integration recommendation.
- [Oracle expense CSV examples](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_3746675443.html): both single-file and multiple-file import forms exist; linked rows are one supported option. An ERP-specific adapter remains an owner-requirement question.
- [Agent-Rail Stipend](https://github.com/agent-rail/stipend) documents itself as development-time mock financial infrastructure. Its YAML policy pattern supports comparison only; it is not production assurance or a TPP replacement.
- [Auxilab expense server](https://github.com/AuxiLabs-Auxiliobits/auxilab-mcp-expense-mgmt) documents receipt and duplicate-claim functionality. Candidate pattern only: no dependency imported, maturity or security audit claimed, or unverified package selected.
- The delegate's secondary knowledgelib URL is not used as technical evidence in the final recommendations.

## Test, offload, and ownership evidence

- Tests: collection.txt, python-tests.txt, independent-repros.json, expense-proof.json and formula-proof.json. Broad run 810 pass / 1 skip / 3 xfail / 1 environment pin failure. Do not present this as an all-green suite.
- Cursor breadth offload: completed with a nonempty disk artifact. Codex correctness offload: dispatcher returned exit 1 with OFFLOAD_INCOMPLETE even though a completed transcript, 12KB report and six runnable proofs were written. We do not relabel the dispatch a success: each retained claim was separately inspected and runtime-verified by the lead. No retry was needed to recover source evidence.
- Two bounded reading offloads plus the required UX panel; no Claude dispatch during conserve-until. Capacity sampled, stale-claim reaper found no claims to reap; elevated machine load did not justify killing unrelated processes.
- Source checkout final status contains only pre-existing untracked dossier-out; tracked source/config unchanged. No commits, PRs, remote issue writes or routing labels were applied.
- Research-only executor rule overrides generic filing step. Measurement intake log was not appended because no issue URLs exist. Publishing lane must recheck live head and dedup before filing and then inspect remote format guard.
- Capability usefulness: frontend verifier changed a code-only UX hypothesis into observed auth-recovery evidence; independent offload supplied actor-integrity and anonymous-exception probes; panel corroborated recovery and added no automatic permission changes. No claimed causal fleet throughput improvement.

## Follow-up on closed issue 1436

The expense-download success event exists before restart but disappears after reloading the persisted portal store. repro_expense_export_audit_lost_on_restart.py reproduced this on the audited current head. Route a concrete reopen/comment review to https://github.com/stranske/Travel-Plan-Permission/issues/1436 under the publishing lane, with the script and independent result; do not create a duplicate or mark it fixed from its closed label. No remote comment was posted here.
