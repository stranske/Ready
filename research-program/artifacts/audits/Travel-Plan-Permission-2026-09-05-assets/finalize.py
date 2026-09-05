from pathlib import Path
from datetime import datetime,timezone
import json,shutil,subprocess
root=Path(__file__).resolve().parents[3];assets=Path(__file__).resolve().parent
unit='D-audit-Travel-Plan-Permission--2026-09-05T16-11-36Z';sha='3ba14a8541b97338586ab6c253ea30e2aed7b86e';now=datetime.now(timezone.utc).isoformat()
audit=Path('/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Travel-Plan-Permission')
manifest=json.loads((assets/'issue-manifest.json').read_text());panel=json.loads((assets/'report.json').read_text());gate=json.loads((assets/'gate.json').read_text())
for name in ['correctness.md','breadth.md','issue-manifest.json','format-validation.json','independent-repros.json','citation-verification.json']:
 assert (assets/name).stat().st_size>0,name
rows='\n'.join('| '+x['priority']+' | ['+x['title']+']('+x['body_file']+') | '+('Design extension' if x['id'].startswith('08') else 'Latent guard gap' if x['id'].startswith('07') else 'Runtime reproduced')+' |' for x in manifest)
report=f'''# Travel-Plan-Permission research audit — 2026-09-05

Unit: `{unit}`. Audited and rechecked remote main `{sha}`. Completed {now}.

Eight issue bodies are ready on disk: five P1 and three P2. Six describe reproduced behavior, one adds a configuration parity guard, and one proposes explicit exception-tier authority. **No issues were filed:** the executor's research-only instruction supersedes the generic brief's filing step. No issue URLs or intake-measurement rows were invented, and no implementation code changed.

| Priority | Staged work order | Evidence class |
| --- | --- | --- |
{rows}

Start with expense and exception authorization, immutable approval actors, and literal spreadsheet text. The strongest probes show anonymous expense creation/read/export returning 303/200/200, an anonymous traveler-attributed exception, a forged actor in approval history, and benign vendor/cost-center formulas saved as XLSX formula cells. Placeholder receipt links are also emitted through the actual portal path.

Validation: all eight bodies pass the repository's actual format validator **without advisories**; every cited path and line was opened and verified. Dedup used 150 issue bodies, two open PRs, and a final recent-issue refresh. Remote main stayed unchanged. Local collection found 858 tests (857 with default perf exclusion). The broad Python run produced **810 passed, 1 skipped, 3 xfailed, 1 failed**; that failure identifies installed Ruff 0.16.5 versus required 0.16.4. It is an environment mismatch, not a new code defect. The delegated focused run passed ten tests, and the lead independently reran all six supplied runtime proofs successfully.

Browser evidence covers public intake, empty-form validation, anonymous and authenticated travel review, mobile expense intake, anonymous expense review and CSV download, and permitted/denied admin and manager views. The direct draft flow ends at a raw missing-token error; the same draft renders with credentials. The four-evaluator UX panel (Codex, Cursor, Gemini, Vibe; Cursor critic) returned overall median **3.0/10** for the sampled bundle, with dimension medians 4/4/4/5. This is **not a whole-product score or passing UX gate**. OIDC sign-in, production hosting, real receipt storage and native Excel execution remain unverified.

Eight dimensions were assessed: correctness and wiring generated the core defects; duplication produced a default-config guard; UX produced scoped draft recovery; field research favored local contract repairs; adjacent opportunity work retained tier authority and deferred ERP selection; tool review recommended no new dependency; local automation review rejected a redundant CI environment check. See the [verification and disposition log]({audit}/2026-09-05-verification-log.md) and [UX coverage report]({audit}/2026-09-05-UX_REVIEW.md).

The generic-approver/board result was downgraded from the delegate's BLOCKER to P2 design hardening because the current docs expressly permit generic approve-capable roles. A retained export-audit-loss repro overlaps closed issue 1436; route a follow-up there instead of filing a duplicate. NetSuite-specific exports and further loader consolidation were deferred. All candidates have a recorded disposition.

Evidence packet: [assets]({assets}); [issue manifest]({assets}/issue-manifest.json); [format results]({assets}/format-validation.json). Next owner: the publishing/intake lane can review the staged bodies and follow-up note under its own filing authority.
'''
(root/'artifacts/audits/Travel-Plan-Permission-2026-09-05.md').write_text(report)
(audit/'2026-09-05-AUDIT_REPORT.md').write_text(report)
verification=f'''# Verification and reconciliation — {unit}

Time {now}; baseline and final remote tip {sha}. All eight draft bodies passed `.github/scripts/issue_format.py` without advisories after the lead corrected line references and slash-delimited prose that looked like paths. Citation text is preserved in {assets}/citation-verification.json. The generic body-generation script is a provenance artifact; final validated issue bodies are authoritative.

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
'''
(audit/'2026-09-05-verification-log.md').write_text(verification)
(assets/'verification-log.md').write_text(verification)
ux=f'''# Observed UX audit — Travel-Plan-Permission

Review {panel['review_id']}; commit {sha}; completed {now}.

The four declared evaluators produced nonempty rubric outputs (Codex, Cursor, Gemini, Vibe), followed by the Cursor critic. Raw reports remain in /Users/teacher/.codex/orchestrator-mirror/ux_reviews/{panel['review_id']}/. Overall median {panel['overall_median']}; dimension medians {json.dumps(panel['dimension_medians'])}; consensus flags {json.dumps(panel['consensus_flags'])}. Gate {json.dumps(gate)}. This scores a local captured subset, not the whole product. Additional seeded captures were taken after the panel and were not silently folded into its scores.

| Surface or scenario | Driven | Observed outcome | Evidence |
| --- | --- | --- | --- |
| Portal home and navigation | Yes | Home and intake links render | portal-home.json and PNG |
| Direct draft empty form | Yes | Server-side missing-field feedback | draft-empty-submit.png, ux-capture.json |
| Direct draft valid form | Yes | Save then raw missing-bearer response; credential control renders same draft | drive-request.txt, anonymous-draft-result.png, authenticated-draft-result.png |
| Expense mobile form | Yes | 375px viewport and scrollWidth 375, 3105px document; no horizontal overflow | expense-mobile.png, capture.txt |
| Expense linked review and CSV | Yes | Anonymous review and actual CSV download succeed | ux-seeded.json, anonymous-expense-review.png, anonymous-expense-download.csv |
| Admin and manager without access | Yes | Missing token or configure denial as raw JSON | admin.json, queue.json, admin-auth capture |
| Admin with configure and manager with approve | Yes | Populated admin, queue and manager detail render | ux-seeded.json, admin-configure.png, queue-approve.png, manager-detail.png |
| Approval/exception mutations | HTTP runtime only | Forged actor, anonymous exception and generic-tier behavior reproduced; not full browser button coverage | independent-repros.json |
| Handoff entry | Existing test coverage; not browser driven | Existing capability contract read and tested in suite; direct-draft reuse proposed | python-tests.txt and test_portal_handoff.py |
| Real OIDC sign-in | No | Production identity provider not configured in synthetic test server | handoff brief below |
| Hosted Render, native Excel, real receipt storage | No | Deployment/platform validation outside this local run | handoff brief below |

Accepted panel improvements: usable draft auth recovery (staged 06); keep permission restrictions; human-readable denied-access navigation is an adjacent polish follow-up, not a separate duplicate blocker. Rejected or deferred: changing advisory waiver semantics solely because the screen says pass; full form redesign without broader usability study; removing auth to make a browser test pass. Initial empty-submit scenario marked goal_achieved was checked against captured validation feedback; do not infer success from the boolean alone.

The tool's synthesize_improvements output is retained at {assets}/improvements.json. Cross-repo patterns are retained at {assets}/cross-repo-patterns.json and are advisory; they do not add findings against this repo without local evidence.

## Platform/identity handoff brief

Use a disposable configured deployment, synthetic users and receipts. Start `tpp-planner-service --host 127.0.0.1 --port 8000` after installing the repo's pinned runtime. Configure an authorized test identity provider privately; never put tokens in URLs or evidence logs. Drive new draft → review → approved manager request → expense review → CSV/XLSX download. Confirm denied roles cannot invoke mutations/downloads directly; test expired and wrong-draft capability recovery. Open the workbook in target Excel and confirm benign =1+1 vendor text stays literal. Resolve an actual synthetic receipt under the selected local or signed-link mode; hosted mode must reject expired/tampered credentials. Capture sanitized browser snapshots, request status, workbook cell types, and receipt-resolution outcomes under {audit}/2026-09-05-platform-verification/. A successful saved draft ending at JSON auth failure, unauthorized mutation, formula cell, or placeholder receipt link is FAIL. Preserve every unresolved surface until those observations exist.
'''
(audit/'2026-09-05-UX_REVIEW.md').write_text(ux)
(assets/'UX_REVIEW.md').write_text(ux)
canonical_bodies=audit/'2026-09-05-issue-bodies';canonical_bodies.mkdir(exist_ok=True)
for p in (assets/'issue-bodies').glob('*.md'):shutil.copy2(p,canonical_bodies/p.name)
with (audit/'README.md').open('a') as f:f.write(f'\n## {now} — Research Program audit refill\n\nRemote main {sha}. Eight staged issue bodies (5 P1, 3 P2), zero filed under research-only executor restriction. See 2026-09-05-AUDIT_REPORT.md, 2026-09-05-verification-log.md, 2026-09-05-UX_REVIEW.md and 2026-09-05-issue-bodies/. Runtime auth/actor/formula/receipt defects and observed draft recovery; config parity latent; tier authority proposed extension. Existing 1436 audit-loss follow-up retained. Next: publishing-lane review and live dedup.\n')
with (audit.parent/'AUDIT_LEDGER.md').open('a') as f:f.write(f'\n## {now} — Travel-Plan-Permission research refill completed\n\nSource {unit}, head {sha}. Eight dimensions assessed; 8 staged issue bodies (5 P1, 3 P2), 0 issues/PRs filed, 0 intake log rows. Primary: expense/exception auth, approval identity, literal export text, receipt delivery and browser recovery. Config parity latent; exception tier hardening downgraded to P2. All 8 bodies pass repo validator with no advisories. Existing 1436 restart audit-loss repro retained for follow-up. Scope limits: local browser subset, OIDC/production/native Excel unverified; one full-suite environment pin failure. Artifacts Travel-Plan-Permission/2026-09-05-AUDIT_REPORT.md, verification-log, UX_REVIEW and issue-bodies. Next owner publishing/intake lane: review drafts, recheck remote head/dedup, then file under its own authority.\n')
for phase,desc in [('Phase 2','Completed two bounded reading offloads plus local synthetic browser captures and four-evaluator UX panel without Claude; all eight dimensions assessed.'),('Phase 3','Independently reran six supplied proofs; verified anonymous expense routes, literal XLSX formula cells and draft auth failure. Corrected tier severity, ERP claim and proposed handoff permissions. Remote main unchanged.'),('Phase 4','Wrote eight issue bodies, all repo validator PASS without advisories. Citations opened at exact lines. Zero filed per research-only executor rule.'),('Phase 5','Wrote OUT and canonical audit/UX/verification reports, copied issue bodies, reconciled every candidate and updated ledger/index. Existing 1436 follow-up retained; platform gaps explicit.')]:
 for p in [root/'artifacts/audits/CHECKPOINT.md',root/f'artifacts/audits/{unit}.CHECKPOINT.md']:
  with p.open('a') as f:f.write(f'\n## {now} — {unit} {phase}\n{desc}\n')
print('Final OUT, canonical report, UX report, verification log, eight issue bodies, ledger, index and phase checkpoints written.')
