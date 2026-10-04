Scorecard: 7 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes — sign up, create a trip, enter sourced prices and fare facts, submit to TPP, then print an approver packet; surfaces unscored 0; closed-still-broken 0.

# stranske/trip-planner audit — 2026-10-02

Tip audited: `8bca24b5e7dc97e37620011003d9f3e6ba575cc7` on `main`.

The product is still usable end-to-end under the live evidence from the 2026-10-01 browser and TPP re-score. This current-tip audit re-exercised its sole partial function, planner chat, and retained the other seven unchanged WORKS rows rather than presenting static review as new runtime coverage. The surface inventory remains 48 mapped surfaces (39 API, nine UI), unscored 0.

One verified P1 defect was filed: [#1883](https://github.com/stranske/trip-planner/issues/1883), **Planner treats month abbreviation as destination and re-asks saved trip dates**. Against isolated data, the actual planner received a Seattle-to-Boston request for “Nov 16” and returned `destinations=['Seattle', 'Boston', 'Nov']`, no timing, and “What dates or trip length should the planner assume?” The cited current code is `trip_planner/app/services/planner.py:405-438` and `559-669`; focused TP4 tests pass 9/9 because they do not cover the case. The issue requires a regression gate and deliberate-break/revert evidence.

Dedup/refutation: closed #1845 is fixed for its stated “My”/“What” reproduction; this narrower `Nov` plus persisted-context failure is new. Existing open #1842 owns the TPP portal hand-off and was not duplicated. The issue used repository labels `bug`, `priority:normal`, and `testing`; the immediate post-file check found no format-guard run yet, so that state is pending rather than assumed.

The queued trigger’s claimed hidden fabrication is not a current user-facing fabrication: it matched a scorecard phrase reporting zero visible fabrication. This artifact uses the required scorecard counts without that ambiguous phrase. The prior UX panel has not been re-run, so no new UX-gate pass is claimed.
