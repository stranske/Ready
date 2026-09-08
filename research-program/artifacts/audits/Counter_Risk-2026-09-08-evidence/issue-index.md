#1006 CLOSED [P2] Reject non-finite values in repo cash structured and override parsers
#1005 CLOSED [P2] Bind dynamic GitHub issue reference to FleetRunContext in langsmith telemetry
#1004 CLOSED [P2] Validate non-negative and finite bounds for cash_total_min and cash_total_max
#1003 CLOSED [P2] Accumulate multi-row counterparties in change attribution prior mapping
#1002 CLOSED [P2] Guard change attribution float parsers against non-finite values
#1001 CLOSED [P1] Deduplicate and group current-month normalized descriptions in compute_futures_delta
#1000 CLOSED [P1] Reject non-finite notional values in futures delta computation
#996 OPEN Raise test coverage toward 90% (autopilot round 3, low blast radius only)
#991 CLOSED Raise test coverage toward 90% (autopilot round 2, low blast radius only)
#986 CLOSED Raise test coverage toward 90% (manual round -- fleet auto-pilot appears stalled)
#984 CLOSED Coverage: prove reconciliation skips unmanaged sheets
#978 CLOSED Raise test coverage toward 90% (most-productive-gap-first)
#965 CLOSED Call configure_logging from the CLI entry point so diagnostics reach the operator
#964 CLOSED Fix the symlink-blind PyInstaller skip-guard so an absent prerequisite skips instead of failing
#963 CLOSED Guard the WAL denominator against signed near-cancellation
#962 CLOSED Reject non-finite values in _find_numeric so the risk ranking is deterministic
#881 CLOSED Re-pin stranske-pdf-extract to the pdf-extract-v0.1.0 tag (currently main SHA a0ee3aa2)
#791 CLOSED [design-system] Adopt the shared light theme (inject_theme + config.toml)
#777 CLOSED [MINOR] GUI: extend inline help to As-of Date/Input Root/Output Root, surface missing-root hint at launch, add run-status line
#772 CLOSED [MAJOR] GUI runner has no in-app help/tooltips and uses unexplained developer labels for non-technical operators
#771 CLOSED [MAJOR] GUI runner opens into an invalid state ('Input Root not found') with no operator guidance
#745 CLOSED Emit DATE_RESOLUTION_FALLBACK DQ warning when as_of_date is inferred from CPRS workbook headers
#728 CLOSED Align Runner and GUI output folders with the pipeline repeat-run contract
#724 OPEN Dependency Dashboard
#712 CLOSED [orchestrator seat test] Add a module docstring to one undocumented module
#711 CLOSED [orchestrator demo] Add a module docstring to one undocumented module
#705 CLOSED Add directional baseline checks for treasury and equity concentration metric segments
#703 CLOSED Align Runner and GUI output folders with the pipeline repeat-run contract
#651 CLOSED Attach Evidence provenance (source file + sheet + row) to extracted `top_exposures` facts
#650 CLOSED Preserve structured warning fields (code / row_idx / source extras) into the manifest, not only flattened strings
#649 CLOSED Add tool/version/git provenance and a top-level `manifest_schema_version` to the manifest
#648 CLOSED Enforce the full run manifest against `manifest_schema()` end-to-end and gate it on PRs
#647 CLOSED Fix the `--formatting-profile` CLI help string to match its real (working) behavior
#646 CLOSED Replace template placeholder package metadata and remove the stray `src/my_project` package
#645 CLOSED Provide a no-egress, browser-runnable demo of the pipeline for a no-install/no-terminal evaluator, honoring the data-confidentiality boundary
#644 CLOSED Declare `pandas` (and reconcile the runtime dependency set) in `pyproject.toml` so a `pip install`ed environment can actually run the pipeline
#643 CLOSED Register a `counter-risk` console-script entry point so the documented operator/maintainer commands work after `pip install`
#610 CLOSED Use repo-specific LangSmith project and trace risk workflows
#597 CLOSED Update operator_ux_decision.md output folder naming convention to match implementation
#594 CLOSED Update runner_xlsm_macro_manual_verification.md to include all 7 macros from macro_spec.md
#593 CLOSED Update operator_ux_decision.md output folder naming convention to match implementation
#591 CLOSED Update runner_xlsm_macro_manual_verification.md to include all 7 macros from macro_spec.md
#552 CLOSED Align Runner Open PPT Folder with manifest-registered PPT deliverables
#499 OPEN Agent metrics weekly summary
#479 CLOSED [Agent] [M1] Add a counterparty mapping registry + maintainers workflow for updating series headers safely
#478 CLOSED [Agent] [M3] Add a “Data Quality Report” section to manifest + operator-friendly warnings in Runner UI
#477 CLOSED [Agent] [M3] Add limit monitoring framework (config-driven limits, breach flags, and operator warnings)
#476 CLOSED [Agent] [M3] Add risk-weighted exposure proxies and rankings (Notional×Vol, Position×Vol where available)
#475 CLOSED [Agent] [M3] Add concentration metrics exhibit (Top N share + HHI) by variant and by segment
#474 CLOSED [Agent] [M2] Cash ingestion hardening: structured source preference, overrides, and reconciliation checks
#473 CLOSED [Agent] [M2] Replace VBA layout/plug-value steps with Python transformations guided by the macro spec
#472 CLOSED [Agent] [M2] Convert VBA macros into a machine-readable “spec” (macro parity harness)
#471 CLOSED [Agent] [M1] Maintain dual deliverables: “Maintainer Master” (linked/editable) vs “Distribution” (static)
#470 CLOSED [Agent] [M1] Produce a “Distribution” PPT deliverable with static charts (render-to-images) and optional PDF
#469 CLOSED [Agent] [M1] Sanitize header and series names everywhere (trim, normalize whitespace, canonicalize aliases)
#468 CLOSED [Agent] [M1] Add “you’re about to lose data” reconciliation checks (unmapped series, missing mappings, dropped rows)
#467 CLOSED [Agent] [M1] Standardize date semantics (as_of_date vs run_date) and enforce across the pipeline
#304 CLOSED [Agent] [Chat] Formalize configurable chat logging modes for policy alignment
#303 CLOSED [Agent] [Ops] Implement operator formatting settings contract in output writers
#302 CLOSED [Agent] [Chat] Productionize LangChain runtime dependencies and fail-fast diagnostics
#301 CLOSED [Agent] [Ops] Port Tkinter GUI runner deliverable onto main (#280 follow-up)
#283 CLOSED [Agent] [Chat] Persist chat prompts/responses with LangSmith trace metadata
#282 CLOSED [Agent] [Chat] Replace stub providers with real LangChain clients
#281 CLOSED [Agent] [Ops] Make MOSERS CPRS-CH writes marker-driven with fail-fast warnings
#280 CLOSED [Agent] [Ops] Ship a Tkinter GUI runner for macro-restricted operators
#279 CLOSED [Agent] [Ops] Expand Runner.xlsm with operator settings + manifest status links
#278 CLOSED [Agent] [Ops] Productionize `counter-risk run` for real monthly executions
#277 CLOSED [Agent] [M2] Cash ingestion hardening: structured source preference, overrides, and reconciliation checks
#241 CLOSED [Follow-up] Modify the build_run_folder_readme_content functio (PR #237)
#240 CLOSED [Follow-up] Update the field validation logic so that missing/ (PR #235)
#239 CLOSED [Follow-up] Complete registry-first resolution, add missing config, fix public API source attribution (PR #228 gaps)
#236 CLOSED [Follow-up] Close remaining PPT output gaps from issue #222 (PR #225)
#233 CLOSED [Follow-up] Implement workbook write-back functionality that c (PR #232)
#230 CLOSED [Follow-up] Move and update the pipeline sheet keying logic to (PR #224)
#227 CLOSED [Follow-up] Implement a new CLI command (or add a console_scri (PR #208)
#222 CLOSED [Follow-up] Modify the PPT generation code to conditionally cr (PR #185)
#221 CLOSED [Follow-up] Modify the strict/fail mode counterparty reconcili (PR #191)
#219 CLOSED [Follow-up] Enhance the PPTX post-processing to iterate over a (PR #170)
#217 CLOSED [Agent] [M1] Sanitize header and series names everywhere (trim, normalize whitespace, canonicalize aliases)
#216 CLOSED [Agent] [M1] Sanitize header and series names everywhere (trim, normalize whitespace, canonicalize aliases)
#190 CLOSED [Follow-up] Implement normalization mapping checks for counter (PR #163)
#129 CLOSED [Follow-up] Implement the VBA code changes in assets/vba/Runne (PR #104)
#127 CLOSED [Follow-up] Integrate calculate_wal and append_wal_row into th (PR #116)
#118 CLOSED [Follow-up] Make missing-directory message readable
#114 CLOSED [Follow-up] Update the chat interface to connect the UI input  (PR #109)
#112 CLOSED [Follow-up] Refactor generate_mosers_workbook to parse the raw (PR #107)
#110 CLOSED [Follow-up] Create and commit a complete .github/workflows/rel (PR #100)
#108 CLOSED [Agent] [M1] Add LangChain-based “Run Review” chat UI (model selection + guardrails) for maintainers/operators
#106 CLOSED [Follow-up] Add an approved reference MOSERS-format workbook a (PR #105)
#103 CLOSED [Follow-up] Update the embedded VBA project in Runner.xlsm so  (PR #98)
#101 CLOSED [Follow-up] Update assets/vba/vbaProject.bin to include the fu (PR #90)
#99 CLOSED [Follow-up] Add a step in the CI/CD process (or update the PR  (PR #94)
#97 CLOSED [Follow-up] Enforce Drop-In Template tests in CI (openpyxl + broader assertions)
#95 CLOSED [Follow-up] Finish PR #91 acceptance criteria (coverage + run-dir isolation tests)
#93 CLOSED [Follow-up] Add release CI workflow (.github/workflows/release.yml)
#89 CLOSED [Follow-up] Update the pipeline’s run entrypoint (in src/count (PR #82)
#88 CLOSED [Follow-up] Update Runner.xlsm to embed and correctly link VBA (PR #73)
#86 CLOSED [Follow-up] Implement the .github/workflows/release.yml file w (PR #79)
#83 CLOSED [Follow-up] Implement the render_cprs_fcm_png(...) function in (PR #63)
#81 CLOSED [Follow-up] Update the output directory creation logic to enfo (PR #69)
#78 CLOSED [Follow-up] Create and commit a PyInstaller specification file (PR #76)
#70 CLOSED [Follow-up] Modify the logic that writes the appended row so t (PR #64)
#58 CLOSED [Follow-up] Add tests/helpers/pptx_asserts.py with functions a (PR #57)
#51 CLOSED Smoke test: keepalive bootstrap
#48 CLOSED [Agent] [M1] Add a counterparty mapping registry + maintainers workflow for updating series headers safely
#47 CLOSED [Agent] [M3] Add a “Data Quality Report” section to manifest + operator-friendly warnings in Runner UI
#46 CLOSED [Agent] [M3] Add change attribution exhibit with confidence flags (new positions vs proxy drivers)
#45 CLOSED [Agent] [M3] Add limit monitoring framework (config-driven limits, breach flags, and operator warnings)
#44 CLOSED [Agent] [M3] Add risk-weighted exposure proxies and rankings (Notional×Vol, Position×Vol where available)
#43 CLOSED [Agent] [M3] Add concentration metrics exhibit (Top N share + HHI) by variant and by segment
#42 CLOSED [Agent] [M2] Replace VBA layout/plug-value steps with Python transformations guided by the macro spec
#41 CLOSED [Agent] [M2] Convert VBA macros into a machine-readable “spec” (macro parity harness)
#40 CLOSED [Agent] [M1] Maintain dual deliverables: “Maintainer Master” (linked/editable) vs “Distribution” (static)
#39 CLOSED [Agent] [M1] Produce a “Distribution” PPT deliverable with static charts (render-to-images) and optional PDF
#38 CLOSED [Agent] [M1] Sanitize header and series names everywhere (trim, normalize whitespace, canonicalize aliases)
#37 CLOSED [Agent] [M1] Add “you’re about to lose data” reconciliation checks (unmapped series, missing mappings, dropped rows)
#36 CLOSED [Agent] [M1] Standardize date semantics (as_of_date vs run_date) and enforce across the pipeline
#35 CLOSED Smoke test: keepalive bootstrap
#34 CLOSED [Agent] [M2] Extract CASH amounts from Daily Holdings PDFs and integrate into Repo “Cash” column (All Programs)
#33 CLOSED [Agent] [M2] Governance, audit, and safety hardening (operator-friendly errors, logs, and LLM safeguards)