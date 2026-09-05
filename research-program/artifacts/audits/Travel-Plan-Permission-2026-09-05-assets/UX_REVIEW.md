# Observed UX audit — Travel-Plan-Permission

Review TPP-research-20260905-1611; commit 3ba14a8541b97338586ab6c253ea30e2aed7b86e; completed 2026-09-05T16:38:56.584615+00:00.

The four declared evaluators produced nonempty rubric outputs (Codex, Cursor, Gemini, Vibe), followed by the Cursor critic. Raw reports remain in /Users/teacher/.codex/orchestrator-mirror/ux_reviews/TPP-research-20260905-1611/. Overall median 3.0; dimension medians {"wired": 4.0, "usability": 4.0, "help_clarity": 4.0, "workflow_productivity": 5.0}; consensus flags {"wired": false, "usability": false, "help_clarity": false, "workflow_productivity": true}. Gate {"done": false, "reasons": ["gate1_not_ok", "overall_median_below_7.0", "blockers_present"]}. This scores a local captured subset, not the whole product. Additional seeded captures were taken after the panel and were not silently folded into its scores.

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

The tool's synthesize_improvements output is retained at /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/improvements.json. Cross-repo patterns are retained at /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/cross-repo-patterns.json and are advisory; they do not add findings against this repo without local evidence.

## Platform/identity handoff brief

Use a disposable configured deployment, synthetic users and receipts. Start `tpp-planner-service --host 127.0.0.1 --port 8000` after installing the repo's pinned runtime. Configure an authorized test identity provider privately; never put tokens in URLs or evidence logs. Drive new draft → review → approved manager request → expense review → CSV/XLSX download. Confirm denied roles cannot invoke mutations/downloads directly; test expired and wrong-draft capability recovery. Open the workbook in target Excel and confirm benign =1+1 vendor text stays literal. Resolve an actual synthetic receipt under the selected local or signed-link mode; hosted mode must reject expired/tampered credentials. Capture sanitized browser snapshots, request status, workbook cell types, and receipt-resolution outcomes under /Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Travel-Plan-Permission/2026-09-05-platform-verification/. A successful saved draft ending at JSON auth failure, unauthorized mutation, formula cell, or placeholder receipt link is FAIL. Preserve every unresolved surface until those observations exist.
