# Travel-Plan-Permission — breadth audit (dimensions 2, 5, 6, 7, 8)

**Repo:** stranske/Travel-Plan-Permission  
**HEAD:** `3ba14a8541b97338586ab6c253ea30e2aed7b86e` (branch `main`)  
**Collected tests:** 857/858 (1 deselected `perf`)  
**Scope:** `src/`, `config/`, `docs/`, `pyproject.toml`, `.github/workflows/ci.yml`, artifact inventories  
**Mode:** read-only; no issues filed from this unit

---

## Executive summary

Four verified, non-duplicate candidates emerged. Exact AST-level function duplication is absent, but **structural duplication** (mirrored YAML trees and repeated config-path walkers) is real and unguarded. Public-field comparison confirms TPP’s deterministic YAML policy engine is directionally aligned with peer open-source patterns, while the **accounting export schema is intentionally minimal** and misaligned with common ERP import shapes (NetSuite dual-file CSV). CI covers planner cross-repo smoke and high pytest coverage, but **Black/format enforcement and local `.venv` freshness are deliberately excluded** from the gate path documented in `docs/local-testing-plan.md`.

Open issues **#1507**, **#1508**, and **#1513** already cover unknown policy keys, validation override wiring, and local-first delivery docs — not repeated here.

---

## Dimension dispositions

| Dim | Topic | Disposition |
| --- | --- | --- |
| **2** | AST duplication + consolidation | **Finding.** No identical function/class AST hashes ≥3 statements, but mirrored config files and five near-copy config-path helpers are consolidation targets. |
| **5** | Public-field comparison (policy + exports) | **Finding.** Policy engine matches YAML/JSON deterministic peers; export layer is a flat 6-column handoff that lacks ERP linkage fields required by major import guides. |
| **6** | Adjacent bounded opportunities | **Finding.** NetSuite-oriented export profile is the highest-yield bounded extension without ERP write-back. |
| **7** | Tools (benefit/cost) | **Finding (narrow).** Borrow duplicate-claim detection pattern from auxilab; skip OPA/full T&E middleware. |
| **8** | CI + local automation gaps | **Finding.** `format_check: false` and missing gate-time env-freshness check create documented local/CI skew. |

---

## Candidate 1 — Guard dual YAML config trees in CI

**Dimensions:** 2, 8  
**Severity:** P1  
**Confidence:** high (files opened and diffed at HEAD)

### Evidence

Five policy/mapping YAML files exist in two locations with identical content today:

- Repo root: `config/policy.yaml`, `config/approval_rules.yaml`, `config/excel_mappings.yaml`, `config/providers.yaml`, `config/validation.yaml`
- Packaged copy: `src/travel_plan_permission/config/*.yaml` (shipped via `pyproject.toml:81-86`)

Runtime loaders walk parents for `config/<file>` (e.g. `src/travel_plan_permission/policy.py:439-444`) and fall back to packaged resources (`policy.py:447-459`). Tests and docs often read the **root** tree directly (`tests/python/test_template_assets.py:61`, `tests/python/test_mapping_integrity.py:36`; `docs/validation-rules.md:93`, `docs/approval-workflow.md:7`).

There is **no test or CI step** asserting the two trees stay identical. A root-only edit would pass pytest while breaking wheel installs.

### Recommendation

Add a small pytest (or CI step) that byte-compares each paired file under `config/` and `src/travel_plan_permission/config/`. Fail with a message naming both paths.

### Non-goals

- Do not delete either tree in the same change; wheels need packaged data, baseline/docs need root paths.
- Do not refactor loaders in the guard PR.

### Dedup

No open issue covers config-tree parity (checked open inventory: #1513, #1508, #1507, #1494, #1238, #1203, #977).

### Test gate

`tests/python/test_config_tree_parity.py::test_packaged_yaml_matches_repo_root` — deliberate break: edit only `config/policy.yaml`, expect failure.

---

## Candidate 2 — Consolidate config path/resource helpers into `config_loader.py`

**Dimensions:** 2  
**Severity:** P2  
**Confidence:** high

### Evidence

Near-identical “walk parents for `config/<name>` + `importlib.resources` fallback” blocks appear in:

| Module | Walker | Package resource helper |
| --- | --- | --- |
| `policy.py` | `_default_policy_path()` :439-444 | `_package_policy_resource()` :447-459 |
| `approval.py` | `_default_rules_path()` :20-27 | `_package_rules_resource()` :30-37 |
| `validation.py` | `_default_policy_path()` :277-282 (misleading name; resolves `validation.yaml`) | `_package_validation_resource()` :23-30 |
| `mapping.py` | `_default_mapping_path()` :34-41 | `_package_mapping_resource()` :16-23 |
| `providers.py` | inline in `_default_config_path()` :130-135 | `_package_providers_resource()` :15-22 |

`config_loader.py` already defines `YamlConfigLoaderMixin.from_file()` (:31-42) but each consumer reimplements path discovery.

### Recommendation

Add shared helpers, e.g. `resolve_repo_config(name: str) -> Path | None` and `read_packaged_config(name: str) -> str | None`, and migrate the five modules to call them. Keep public APIs unchanged.

### Benefit / cost

- **Benefit:** one place to fix checkout-vs-wheel behavior; removes misleading duplicate function names (`validation._default_policy_path`).
- **Cost:** ~5 call-site edits + focused tests; low regression risk if parity tests from Candidate 1 land first.

### Dedup

Not covered by open issues.

### Test gate

Existing loader tests plus `tests/python/test_config_loader.py::test_repo_and_package_fallbacks` with temp layouts.

---

## Candidate 3 — Add optional NetSuite-style dual-file export profile

**Dimensions:** 5, 6  
**Severity:** P2  
**Confidence:** medium-high (export code verified; ERP shape from Oracle primary doc)

### Evidence — current export

`ExportService.schema` at `src/travel_plan_permission/export.py:20` emits six columns: `date`, `vendor`, `amount`, `category`, `cost_center`, `receipt_link`. Documented in `docs/accounting-integration.md:9-16` as the canonical handoff. Portal reuses this layer (`docs/expense-workflow.md:30-31`, `http_service.py` via `ExportService.to_csv`).

### Evidence — public field gap

Oracle NetSuite’s expense import guide requires **separate header and line files** with linkage fields (`External ID`, `Employee`, line `Category`/`Amount`, map line External ID → Line ID): [NetSuite Expense Report CSV Examples](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_3746675443.html).

Industry T&E→ERP playbooks describe JSON/API or pipe-delimited financial documents with GL account, cost center, and idempotency keys — not TPP’s flat six columns: [T&E System-to-ERP Integration Playbook (Concur)](https://knowledgelib.io/business/erp-integration/time-expense-integration/2026).

TPP correctly documents export-only scope (`docs/accounting-integration.md:39`); the gap is **shape**, not missing ERP writes.

### Recommendation

Add an optional export profile (e.g. `ExportService.to_netsuite_csv_pair(...)`) producing:

1. Header CSV: `external_id`, `employee`, `use_multiple_currencies` (from report metadata)
2. Line CSV: `external_id`, `line_reference_number`, `category`, `amount`, `currency`, `date`

Keep the existing flat schema as default; document the profile in `docs/accounting-integration.md`.

### Non-goals

- No live NetSuite API integration.
- No change to approval/policy engines.

### Dedup

Not in open issues.

### Test gate

`tests/python/test_export_service.py::test_netsuite_profile_emits_linked_header_and_line_files` with deliberate break removing `external_id` from line file.

---

## Candidate 4 — Close CI/local automation gaps (format + env freshness)

**Dimensions:** 8  
**Severity:** P2  
**Confidence:** high

### Evidence

1. **Black/format not gated.** `.github/workflows/ci.yml:30` and `pr-00-gate.yml:81` set `format_check: false` with comment “Existing repo-wide Black drift is tracked outside this CI smoke issue.” Ruff is selected for lint (`pyproject.toml:122-138`) but Black remains a dev pin (`pyproject.toml:37`). Keepalive prompts still instruct `black --check` (`.github/codex/prompts/fix_ci_failures.md:25`), creating **agent/human vs CI divergence**.

2. **Local env freshness documented but not gate-enforced.** `docs/local-testing-plan.md:44-60` and `scripts/check_local_env_freshness.py` describe stale `.venv` as a primary false-failure source. The helper is verified to exist only in `maint-51-dependency-refresh.yml:61,131-154` (PR-body checklist), **not** in Gate `python-ci` or main `ci.yml` reusable job.

3. **Cross-repo smoke covers planner only** (`.github/workflows/ci.yml:89-236`); expense portal Stage 6 checks from `docs/local-testing-plan.md:180-192` rely on pytest in the default suite (`tests/python/test_http_service.py:899+`) but are not singled out in a named CI job — acceptable, but env-freshness and format gaps remain the actionable automation holes.

### Recommendation

Two bounded PRs (either order):

1. Re-enable `format_check: true` on Gate after a one-time Black pass **or** migrate keepalive/CI docs to Ruff format exclusively and drop conflicting Black instructions.
2. Add `python scripts/check_local_env_freshness.py --check` as a fast step in Gate `python-ci` (or post-install hook in reusable workflow inputs) so lock/pyproject drift fails in CI the same way docs promise locally.

### Dedup

Distinct from #1495 (dev tool version sync PR) and workflow-sync PR #1516.

### Test gate

- Format: CI job green on main; deliberate misformat fails check.
- Freshness: `tests/python/test_dependency_version_patterns.py` + freshness script exit 1 when `.venv` pins lag lock (may need CI-only install path without `.venv` — script should no-op or compare against pip freeze in CI).

---

## Dimension 7 — tool integration note (no standalone candidate issue)

**Disposition:** evaluated; **no fourth tool import recommended** beyond patterns already native to TPP.

| Tool / pattern | Source | Benefit | Cost | Verdict |
| --- | --- | --- | --- | --- |
| **auxilab duplicate detector** | [auxilab-mcp-expense-mgmt](https://github.com/AuxiLabs-Auxiliobits/auxilab-mcp-expense-mgmt) | Deterministic duplicate screening before reimbursement | Small pure-Python module; no MCP runtime required for TPP | **Consider** as follow-on to Candidate 3, not standalone |
| **Agent-Rail stipend policy YAML** | [agent-rail/stipend](https://github.com/agent-rail/stipend) | YAML caps + audit JSONL | TPP already has YAML policy (`policy.py`) + SQLite audit (`audit.py:6-25`) | **Skip** — redundant |
| **Open Policy Agent / Concur API middleware** | [knowledgelib T&E playbook](https://knowledgelib.io/business/erp-integration/time-expense-integration/2026) | Enterprise ERP parity | Heavy ops; conflicts with export-only boundary | **Decline** for 2-week scope |

Fold duplicate detection into a future expense-hardening issue only if finance requests it; not promoted to top-4 because TPP lacks duplicate semantics in `ExpenseReport` today and scope would exceed “bounded.”

---

## Dimension 5 — policy engine public comparison (context for fleet)

TPP’s deterministic YAML rule engine (`PolicyEngine` in `policy.py:462-574`, rules in `config/policy.yaml`) aligns with peers that keep policy **out of LLM context**:

- **stipend:** YAML-defined caps/thresholds with schema validation ([agent-rail/stipend](https://github.com/agent-rail/stipend))
- **auxilab:** JSON policy files, deterministic checker, Decimal money ([auxilab-mcp-expense-mgmt](https://github.com/AuxiLabs-Auxiliobits/auxilab-mcp-expense-mgmt))

Differentiator: TPP combines **pre-trip policy**, **Excel population**, and **post-trip approval** (`approval.py:41-120`) in one repo — uncommon in single OSS samples surveyed.

Known weakness already filed: silent acceptance of unknown YAML rule keys (`policy.py:431-436` merges unknown keys via defaults) — **#1507**.

---

## Inventories consulted

- Open issues: 7 open / 150 total (`issues.json`) — deduped against candidates above
- Open PRs: #1516 workflow sync (staging), #1495 dev tool versions
- CI: HEAD runs mostly green; Gate failure on sync branch SHA `4b044ede` (not audited HEAD)

---

## Adversarial notes (evaluator stance)

- **Dual config trees may be intentional** for editable root configs vs packaged defaults; the finding is the **missing guard**, not the duplication itself. Consolidating to a single tree would be a larger breaking change — not recommended here.
- **NetSuite profile** assumes finance uses CSV import; Concur/Ramp JSON APIs are the live path for many firms. Profile should stay optional and documented as one adapter.
- **`format_check: false` may be deliberate debt** until Black drift burn-down completes; re-enabling without a formatting PR will fail Gate — sequence matters.
- **Confidence on duplicate-detection tool:** medium — auxilab is illustrative, not a drop-in dependency audit.

---

## Top 3 (for primary lead synthesis)

1. **CI guard for dual YAML config parity** (Candidate 1) — prevents silent wheel/checkout drift.  
2. **NetSuite-style optional export profile** (Candidate 3) — closes documented export-only vs ERP-shape gap with primary-source backing.  
3. **Gate format + env-freshness automation** (Candidate 4) — closes local-testing-plan promises vs CI reality.

**Candidate count:** 4 actionable (+ explicit tool skip table for D7)
