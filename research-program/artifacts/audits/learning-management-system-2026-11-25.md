Scorecard: 5 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0

Issues filed: 2 — [#859](https://github.com/stranske/learning-management-system/issues/859), [#860](https://github.com/stranske/learning-management-system/issues/860)

## Run report (Track D refill 2026-11-25)

**Repo:** stranske/learning-management-system @ `c13f039` (one workflow-template commit since 2026-10-25 `e08460a`). **Trigger:** agent-ready supply 0/3; scorecard age >30d.

**Phase 1.5 — product scorecard:** Re-probed CF1–CF7 with fast pytest subsets and OpenAPI inventory. Prior round findings #789–#791 verified fixed on tip (mastery confidence, calibration page, Learn feedback surface). CF3/4/5/6/7 upgraded to WORKS where probes pass; CF1 remains PARTIAL (author journey not end-to-end); CF2 PARTIAL because legacy `/learn/attempts` still lacks attempt-context fields wired on the canonical activity surface (#835 follow-up gap → #859).

**Dimensions (abbreviated):** D1/D3 adversarial pass on learn vs attempts wiring; D4 static UX review on server HTML; other dimensions deferred to prior rounds / green CI (3048 tests). No closed-still-broken candidates on core functions.

**Filing:** Two P2 `priority:normal` issues with AGENT_ISSUE_FORMAT bodies in `Code/Audits/learning-management-system/2026-11-25-issue-bodies/`. Intake log appended. Ledger entry pending owner sync for Dropbox `AUDIT_LEDGER.md`.

**Artifacts:** Canonical scorecard `Code/Audits/learning-management-system/2026-11-25-SCORECARD.md`; checkpoint `artifacts/audits/D-audit-learning-management-system--2026-11-25T04-28-18Z.CHECKPOINT.md`.

**Format guard:** #859 run 45570333881 success; #860 run 45570334693 still queued at report time (re-check `gh issue view 860 --json labels` for `agents:formatted`).