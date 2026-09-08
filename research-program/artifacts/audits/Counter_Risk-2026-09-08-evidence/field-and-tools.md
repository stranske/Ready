# Dimensions 2, 5, 6, 7 and 8 — bounded assessment

Baseline: e2a1bacf37503217e00e467aa72198988777afa4. Sources checked 2026-09-08. These are evidence-based engineering options, not portfolio-policy recommendations.

## Public-field comparison (D5)

The app implements historical notional concentration, configured limit checks, and optional linear notional-times-volatility proxies (README.md:14–19; docs/risk_proxy_outputs.md:17–24). BIS counterparty guidance advocates complementary exposure measures and stress analysis. Inference: this reporting toolkit could gain scenario-based concentration comparisons, but its existing inputs cannot establish netting/collateral-adjusted credit exposure or potential future exposure. Those require netting-set and collateral terms plus a model mandate. Do not label the current toolkit noncompliant or represent bank supervisory guidance as a requirement for this owner.
Source: https://www.bis.org/committees/bcbs/basel-consolidated-guidelines/module/cri/40

The operator HHI guide mixes threshold vintages. A small documentation body is staged, explicitly preserving policy neutrality. Source: https://www.justice.gov/atr/herfindahl-hirschman-index

## Reuse and adjacent opportunities (D2/D6)

AST equality found four duplicate function-body groups (duplicates.json): three demo helpers are duplicated between demo_artifact and web_demo; table-row adapters match in compute/limits and compute/rollups. Duplication alone is not a defect. The demo divergence is already tracked in the August 24 D-1 audit; retain as a known consolidation follow-up, do not open a duplicate. Keep these observations separate from correctness findings.

Short increment: add a scenario delta report over the existing normalized exposures, explicitly marking assumptions and preserving current outputs; first prove split-row/order invariance and conservation before proposing new stress knobs. Roadmap: legally meaningful netting sets, collateral and settlement exposures need input contracts and owner-defined interpretation. No new question is needed for this audit; no financial model or policy choice is made.

## Tool choices (D7)

1. Hypothesis is a candidate for a small dev-only property-test pilot over numeric aggregation: permutation invariance, split/merge conservation, rejected NaN/infinity, and monotonic limit response. Official strategies support targeted finite/non-finite floats. Benefit: catches sibling variations of yesterday's bugs. Cost: generator design and shrinker runtime; deterministic bounded profiles should run in PRs. First compare yield against targeted parametrized tests; do not introduce it solely to raise coverage.
Source: https://hypothesis.readthedocs.io/en/latest/reference/strategies.html
2. Keep openpyxl for workbook manipulation but do not treat a successful save as formula recalculation: its documentation says formulas are not evaluated. Test a representative saved workbook through the existing Excel COM route when calculation matters; do not add a second spreadsheet engine without a demonstrated gap. No new formula-corruption defect was established in this audit.
Source: https://openpyxl.readthedocs.io/en/stable/simple_formulae.html
3. Keep PyInstaller; fix the assembly boundary and execute the actual assembled bundle. Its documented executable/runtime and platform distinctions explain why a shell-script test double cannot establish Windows portability.
Sources: https://pyinstaller.org/en/stable/operating-mode.html and https://pyinstaller.org/en/stable/runtime-information.html

## Local tooling and automation (D8)

Exact-head main CI 34244935833 passed Ruff, Black, mypy and Python 3.12/3.13. PR Gate excludes release/slow suites and disables format_check; this known August 24 concern is retained, not reported as a new incident. Release E2E runs Linux; the Windows release workflow checks file existence without executing the assembled binary. Packaging/launcher staged bodies include concrete runtime gates.

The shared research queue includes Counter_Risk. Live issue snapshot has one implementation item (#996) plus dependency/metrics trackers; its body narrows work to historical_update workflow test coverage. The open PR snapshot contains one dependency-sync PR (#1013), so these audit drafts do not overlap an active feature branch. No independent Counter_Risk-specific Codex automation TOML was found in the bounded name/content search. This is not an assertion about all external scheduler installations.
