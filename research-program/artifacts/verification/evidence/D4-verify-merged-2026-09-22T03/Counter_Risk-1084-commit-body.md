fix(pipeline): fleet data_quality_status reflects fail limit breaches (#1084) (#1096)

* fix(pipeline): emit fail fleet data_quality_status for limit breaches

Derive LangSmith fleet status from build_data_quality overall_status and
limit_breach_summary max_severity so fail-severity breaches are not reported
as success when warnings are empty.

Co-authored-by: Cursor <cursoragent@cursor.com>

* fix(pipeline): resolve fleet test collision and mapper review findings

Rename pipeline LangSmith fleet tests to avoid pytest import collision with
observability/test_langsmith_fleet.py, derive warning status from computed
overall_status instead of raw warnings truthiness, and add mapper coverage
for fail/warning/success paths including info-only warnings.

Co-authored-by: Cursor <cursoragent@cursor.com>

---------

Co-authored-by: Cursor <cursoragent@cursor.com>
