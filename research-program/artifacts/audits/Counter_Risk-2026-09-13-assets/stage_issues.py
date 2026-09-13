from pathlib import Path
from datetime import datetime,timezone
import json,subprocess
b=Path('[LOCAL_HOME]/.codex/automations/research-program'); repo=b/'[LOCAL_WORKSPACE]/Counter_Risk'; art=b/'artifacts/audits/Counter_Risk-2026-09-13-assets'; bodies=art/'issue-bodies';bodies.mkdir(exist_ok=True)
# Each entry is a verified work order, never posted by this executor.
entries=[
('01','P1','Resolve registry aliases when matching counterparty limits','src/counter_risk/compute/limits.py',263,'tests/compute/test_limits.py','test_registered_alias_triggers_canonical_limit',
'The limit contract accepts canonical entity keys (`config/limits.yml:15`). A registered Bank of America, NA exposure of 200 against a bank_of_america cap of 100 produces no breach and reports the target missing. The canonical-spelling control produces a fail breach of 100. Current break: `_normalize_entity_key` performs only whitespace/case normalization; it never resolves the registry alias. The default missing-entity policy warns and continues, so a genuine cap breach loses its fail severity.',
'Use the existing counterparty registry resolver consistently for breach matching and missing-entity detection; keep documented fallback semantics for other entity types.',
'Route both matching loops through the same canonical counterparty identity while preserving unknown-name and non-counterparty behavior.',
'Feed the registered alias through `_build_limit_exposure_rows` and then `check_limits`; assert the cap breaches and find_missing_limit_entities is empty, while an unknown name still follows strictness.',
'For the alias input, actual_value is 200 and breach_amount is 100 with severity fail; canonical and alias spellings give identical records.',
'lead-numerical-seams.py; standalone proof plus actual pipeline reshaper and spelling control. Related historical #479/#468 introduced registry/reconciliation; #1047 concerns numeric aliases, not entity aliases.'),
('02','P1','Consolidate counterparties before concentration calculations','src/counter_risk/compute/rollups.py',575,'tests/compute/test_concentration_metrics.py','test_split_counterparty_preserves_concentration',
'Current break: concentration uses input rows as independent counterparties, although `docs/concentration_metrics.md:28` defines Top-N by counterparty. Alpha split into 60+60 and ten other names at 10 yields HHI 0.16942149 and Top5 0.68181818. A pre-aggregated Alpha=120 control yields HHI 0.31818182 and Top5 0.72727273. The actual pipeline reshaper preserves split rows, so representation alone changes reported concentration.',
'Aggregate gross exposure for each counterparty within variant and segment before ranking; preserve the existing sign convention and supported group_by API.',
'Consolidate repeated counterparty identities before Top5, Top10, and HHI while preserving zero-total behavior and existing gross-sign semantics.',
'Compare split and pre-aggregated inputs through `_build_concentration_exposure_rows` in `src/counter_risk/pipeline/run.py`; assert equal Top5, Top10, and HHI for both representations.',
'The synthetic split fixture gives Top5 160/220, Top10 210/220, and HHI 15400/48400 within numeric tolerance; zero and mixed-sign controls retain documented behavior.',
'lead-numerical-seams.py. Historical #475 introduced the feature; #1032 concerns non-finite inputs. Reviewer Top5=1.0 was rejected and corrected to160/220 before staging.'),
('03','P2','Reject malformed nonblank maturity amounts','src/counter_risk/parsers/exposure_maturity_schedule.py',247,'tests/parsers/test_exposure_maturity_schedule.py','test_invalid_nonblank_total_raises',
'Current break: a real synthetic workbook with a maturity date and Total=not-a-number parses as total=0.0. The parser catches every numeric-coercion error and replaces it with zero. Its documented zero-fill contract covers blank cells only (`src/counter_risk/parsers/exposure_maturity_schedule.py:226`); silently discarding a malformed leg can bias the downstream WAL.',
'Keep blank cells as zero, but reject nonblank invalid amounts with source row/column context before WAL calculation.',
'Raise the existing maturity schedule error for nonblank unparseable amounts instead of replacing numeric conversion failures with zero.',
'Add real workbook cases for blank, malformed text, boolean, NaN/Infinity text, and valid accounting amounts; assert malformed rows fail before `src/counter_risk/calculations/wal.py` returns a result.',
'Blank totals still parse as zero; malformed nonblank totals raise with row and Total-column context; valid accounting values retain their amounts.',
'lead-numerical-seams.py creates and parses an actual XLSX. #963 validates signed WAL denominators and #1022 validates WAL output; neither preserves rejected parser inputs.'),
('04','P2','Include change facts in live chat messages','src/counter_risk/chat/session.py',292,'tests/test_chat_provider_clients.py','test_delta_facts_reach_langchain_invoke',
'Current break at the transport boundary: asking show deltas computes DeltaOnlyBank delta_notional=876543.21 locally, but that name and value never reach LangChain invoke. `build_guarded_prompt` includes summary/warnings/top exposures only (`src/counter_risk/chat/session.py:404`), and `src/counter_risk/chat/providers/base.py:133` invokes the provider with messages while ignoring context_answer. Offline providers and test doubles consume context_answer, masking the missing facts. No live model response or external API call was used to establish this payload omission.',
'Carry relevant loaded deltas into the actual guarded provider messages, preserving untrusted-data handling and bounded prompt size.',
'Serialize the requested delta facts into guarded message content before provider invocation, using existing sanitization and data boundaries.',
'Exercise ChatSession through the actual LangChainProviderClient with only the final client.invoke transport intercepted; assert the name/value are in messages and malicious source strings remain untrusted.',
'The named transport test finds DeltaOnlyBank and876543.21 in the actual messages for show deltas; ordinary top-exposure queries remain supported without network access.',
'lead-chat-delta-proof.py uses the actual adapter with an intercepted final transport. Historical #108/#25 introduced run review; #1036 fixes exposure sorting, not delta context transfer.'),
('05','P2','Report skipped link refresh without denying generated slides','src/counter_risk/pipeline/data_quality.py',217,'tests/pipeline/test_monthly_pipeline_ppt_outputs.py','test_skipped_refresh_reports_existing_distribution',
'Current operator-message defect: when link refresh is skipped, the distribution PPT is still successfully generated, yet the summary emits PPT_GENERATION_SKIPPED and says generation was skipped. Per-output distribution status is success. A warning about an unrefreshed master is justified; the claim that no PPT generation occurred is inaccurate. `src/counter_risk/pipeline/run.py:2867` returns the refresh result as aggregate ppt_status.',
'Distinguish master link-refresh state from distribution generation in the existing status/summary contract. Preserve warnings for stale/unrefreshed links.',
'Derive operator findings from the relevant per-output and refresh results so a successful distribution is described as generated even when refresh skipped.',
'Use a real generated distribution deck with skipped refresh and assert the summary identifies link refresh as skipped while preserving any warranted yellow status.',
'The named test confirms an existing successful distribution is never described as generation skipped; a genuinely absent distribution remains explicitly reported.',
'wiring-proof-ppt-status-skew.py independently rerun successfully. This is P2 message precision, not a demand to turn yellow into green.'),
('06','P2','Reject incompatible PDF and distribution settings','src/counter_risk/pipeline/run.py',2757,'tests/pipeline/test_monthly_pipeline_ppt_outputs.py','test_pdf_request_with_distribution_disabled_is_explicit',
'Current break: export_pdf=True combined with enable_distribution_output=False produces no PDF and no operator warning. The post-distribution PDF generator is only invoked in the enabled-distribution branch (`src/counter_risk/pipeline/run.py:2835`), so its own skip reporting cannot run. The settings are independently accepted by the configuration model, and GUI/CLI can request PDF output.',
'Validate or explicitly report the incompatible PDF/distribution combination before claiming the requested output set is complete.',
'Add a configuration validation error or an explicit PDF-skipped result when PDF export is requested while distribution output is disabled.',
'Cover the incompatible flags and the enabled-distribution control using an intercepted PDF exporter; assert visible error/skipped reason for the former and exporter invocation for the latter.',
'An explicit PDF request never disappears silently; export_pdf=False continues to omit PDF without a failure.',
'wiring-proof-export-pdf-silent-skip.py independently rerun; actual output orchestration with mocked COM refresh only. No source edits required for reproduction.'),
('07','P2','Hash optional inputs that alter report artifacts','src/counter_risk/pipeline/run.py',917,'tests/pipeline/test_run_pipeline.py','test_optional_input_provenance_hashes',
'Current provenance gap: `_resolve_input_paths` omits exposure_summary_xlsx and screenshot_inputs, although the WAL generator consumes the former (`src/counter_risk/pipeline/run.py:3843`) and screenshot replacement validates and uses the latter (`src/counter_risk/pipeline/run.py:3157`). A valid generated PNG passes screenshot mapping validation but is absent from the input-hash mapping. The optional maturity workbook is also absent. Material inputs can therefore change without an identifying hash in the manifest.',
'Include active externally supplied WAL and screenshot sources in the manifest provenance; distinguish generated intermediate images and avoid requiring unused optional files.',
'Extend the provenance input enumeration for active optional sources using stable logical names, retaining explicit separation for generated intermediates.',
'Add valid PNG/maturity workbook fixtures; mutate bytes at the same path and assert the corresponding manifest hash changes when the source is active, with disabled-source controls.',
'The named test verifies active optional sources have correct SHA-256 values and altered bytes change them; generated internal images are not mislabeled as original external sources.',
'lead-numerical-seams.py verifies a valid PNG passes runtime mapping while missing from hash enumeration. Closed #649 introduced general provenance and #651 exposure evidence; this is optional-source coverage.'),
]
for num,priority,title,src,line,test,name,why,scope,task,testtask,expected,notes in entries:
 body=f'''# [{priority}] {title}\n\n## Why\n\n`{src}:{line}` is current evidence at commit 6e2a87b27be9a23d388155e37ed01675b1e27dc7. {why}\n\n## Scope\n\n{scope}\n\n## Non-Goals\n\nNo upstream workflow changes, model redesign, or unrelated refactors. Scaffold-only completion does NOT count: adding a helper or a test double that leaves {title.lower()} unimplemented is a failure of this issue.\n\n## Tasks\n\n- [ ] In `{src}`, {task[0].lower()+task[1:]}\n- [ ] In `{test}`, add `{name}`. {testtask}\n\n## Acceptance Criteria\n\n- [ ] `python -m pytest {test} -q` passes and collects `{name}`. {expected}\n- [ ] Deliberate-break gate: temporarily restore the faulty behavior in `{src}`; `{test}::{name}` must fail; revert the deliberate break and rerun the named test to pass. Capture both outcomes in the implementation PR.\n- [ ] The test exercises the actual production boundary and retains a valid-input control.\n\n## Implementation Notes\n\nResearch-only draft; not filed. Current-code proof: {notes}\n'''
 (bodies/f'{num}.md').write_text(body)
 metadata=[{'id':e[0],'priority':e[1],'title':e[2],'body':str(bodies/f'{e[0]}.md')} for e in entries]
 (art/'staged-issues.json').write_text(json.dumps(metadata,indent=2))
now=datetime.now(timezone.utc).isoformat(); unit='D-audit-Counter_Risk--2026-09-13T18-41-41Z'
for p in [b/'artifacts/audits/CHECKPOINT.md',b/f'artifacts/audits/{unit}.CHECKPOINT.md']:
 with p.open('a') as f:f.write(f'\n## {now} {unit} Phase 2 complete\nEight dimensions considered. Two scoped offloads yielded8 candidates plus lead chat transport defect; operator fixture/GUI/chat tests145 passed. Function-only UX panel4 evaluators plus Cursor critic; browser/Windows coverage blocked. Corrected numerical Top5 arithmetic.\n')
print('staged',len(entries))
