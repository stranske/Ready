Scorecard: 5 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Audit: stranske/Inv-Man-Intake

Audited exact tip `6d3d7063a928b5ddf9216f449968b683e63a5e76`. The prior 2026-09-24 scorecard had one unscored static operator-app surface. This round drove it locally through seven passing browser scenarios: offline upload with no egress, packet profiling, deterministic conflict escalation, graphic preview, alternate vector-PDF rendering, export selection, local PNG/XLSX/one-pager artifacts, deliberate handler breaks, and print layout. The alternate vector input produced a genuine non-uniform PNG rather than a constant placeholder.

Focused core checks passed 46 tests. The focused command exited nonzero only because this repository applies an 80% whole-repository coverage threshold to subset runs; exact-head GitHub CI `36979027428` is successful. The browser suite's single failure is limited to Playwright's own bundled-Chromium availability check; its functional scenarios ran through installed Chrome and passed. Current CI installs the bundled browser.

The scorecard remains five working and two intentionally partial contract rows: production scoring refuses to manufacture a score without evidence-backed components, and validation-queue persistence remains explicitly out of the CLI seam. #948 is the only substantive open issue; its consultant ontology needs the owner's authoritative vocabulary, so no guessed duplicate was filed. Closed report-spec and UI-evidence work was revalidated on the live tip. No fresh reproducible, non-duplicate finding survived verification.

Issues filed: 0.
