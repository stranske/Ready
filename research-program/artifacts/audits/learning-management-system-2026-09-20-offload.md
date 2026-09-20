# Learning-management-system focused audit

Static review is against `ecfe8de`. Confidence is high for F1 and F5, and medium-high for F2–F4/F6–F7. I excluded ownership authorization and finite-number validation, as instructed. Targeted tests were executed: 151 cases passed; the command's final nonzero result was only the repository-wide 80% coverage floor applied to that partial selection.

### F1 — The “daily” LLM budget never starts a new day
- Dimension: D8
- Severity: P1
- Evidence: `src/lms/llm/budgets.py:76-114`; `src/lms/llm/api.py:171-200`
- Snippet:
      def _add_spend_locked(self, mode: str, delta_micro_usd: int) -> None:
          """Apply a (possibly negative) spend delta. Caller MUST hold ``_lock``."""
          self._global_spend += delta_micro_usd
          self._mode_spend[mode] = self._mode_spend.get(mode, 0) + delta_micro_usd
- Failure: After a long-lived web worker cumulatively spends `LLM_DAILY_BUDGET_USD`, a request on the next calendar day still gets `BudgetExceeded`; `_default_client()` is cached and neither it nor `DailyBudgetTracker` records a day/window or resets spend. Gate audit: only `release()` decrements and it can refund an in-flight failed reservation, not already committed spend; once closed, a new reservation cannot run; the named measuring window is a day but the draining window is process lifetime; the only exhausted-state text is “already spent X,” and no input yields a fully-drained/new-day state without process restart.
- Test coverage: No. Checked `tests/llm/test_client_budget.py`; it covers release and concurrent reservations but has no clock rollover or cached-client reset test.
- Fix sketch: Store a UTC budget period with the counters and atomically reset both when the current UTC date changes, before cap comparison. Add a clock-injected test that exhausts the cap, advances a day without recreating the tracker, and proves the next reservation succeeds.

### F2 — Per-mode cap and timeout configuration are constructor-only dead knobs
- Dimension: D3
- Severity: P2
- Evidence: `src/lms/llm/config.py:24-32`; `src/lms/llm/config.py:73-94`; `src/lms/llm/api.py:193-200`
- Snippet:
      mode_models: Mapping[str, str]
      global_daily_cap_micro_usd: int = 200_000  # 0.20 USD/day default kill-switch
      per_mode_daily_cap_micro_usd: Mapping[str, int] = field(default_factory=dict)
      default_provider: str = "fake"
      default_timeout_seconds: float = 30.0
- Failure: Setting any plausible deployment key for a per-mode cap or provider timeout has no effect: the only loader inputs are model overrides, global cap, and provider, so the runtime always receives `{}` for per-mode caps and `30.0` seconds. A supposed `study-coach` cap therefore never blocks a mode independently, despite the client accepting and enforcing such a map when manually constructed.
- Test coverage: No runtime coverage. Checked `tests/llm/test_client_routing.py` and `tests/llm/test_client_budget.py`; they instantiate `LLMConfig(per_mode_daily_cap_micro_usd=...)` directly rather than loading it from deployment configuration.
- Fix sketch: Define documented environment variables (for example, `LLM_MODE_DAILY_CAPS_MICRO_USD` JSON and `LLM_DEFAULT_TIMEOUT_SECONDS`), parse and validate them in `load_llm_config_from_env`, and expose them in `render.yaml`/`.env.example`. Add an API-client construction test proving each is passed to `DailyBudgetTracker` and the provider call.

### F3 — `LLM_DEFAULT_PROVIDER` is read, then discarded by every runtime client
- Dimension: D3
- Severity: P2
- Evidence: `src/lms/llm/config.py:89-94`; `src/lms/llm/config.py:97-110`
- Snippet:
      return replace(
          load_llm_config_from_env(defaults=defaults),
          default_provider=default_provider,
      )
- Failure: With `LLM_DEFAULT_PROVIDER=anthropic` (or `fake`) configured, the HTTP and CLI runtime clients replace it with the credential-derived provider. The advertised environment setting changes the standalone loader result but cannot change live routing, so an operator receives the opposite provider from the configured value.
- Test coverage: No; `tests/llm/test_client_routing.py` has a loader-only test for the variable, while `test_default_api_client_applies_runtime_policy` explicitly asserts that a contradictory environment value loses.
- Fix sketch: Choose one authority and make it explicit. Either remove/document-deprecate `LLM_DEFAULT_PROVIDER`, or validate that the requested provider is registered and honor it; retain a safe fallback only when the configured provider is unavailable. Cover the live `_default_client()` behavior rather than only the loader.

### F4 — The repository’s three model-policy JSON files do not configure the LMS runtime
- Dimension: D3
- Severity: P2
- Evidence: `config/model_registry.json:1-6`; `src/lms/llm/config.py:73-94`; `tools/llm_registry.py:25-28`
- Snippet:
      env = dict(environ) if environ is not None else dict(os.environ)
      mode_models = {mode: env.get(_env_var_for(mode), defaults[mode]) for mode in LLM_MODES}
      cap_str = env.get("LLM_DAILY_CAP_MICRO_USD")
      if cap_str:
          cap = int(cap_str)
- Failure: Editing `config/model_registry.json`, its declared `config/model_selection_policy.json`, or `config/llm_slots.json` does not change an LMS LLM call: no `src/lms` path loads any of them, while the only registry path is under `tools/`. The app continues with environment/default models, making repository policy changes appear deployed when they are not.
- Test coverage: No. Checked `tests/llm/test_client_routing.py`; it exercises environment routing only and contains no JSON-policy integration test.
- Fix sketch: If these are intended application configuration, load and validate one canonical registry at startup and derive runtime models/providers from it. If they are only CI/agent-fleet metadata, relocate or rename them and document that boundary so LMS operators cannot mistake them for live app policy.

### F5 — First concurrent scheduling writes can crash on the unique review-card row
- Dimension: D1
- Severity: P1
- Evidence: `src/lms/scheduling/card_state.py:49-76`; `src/lms/scheduling/models.py:396-403`; `src/lms/scheduling/service.py:741-748`
- Snippet:
      existing = get_card_state(
          session, learner_id=learner_id, subject_id=subject_id, subject_type=subject_type
      )
      if existing is not None:
          if retention_tier is not None and existing.retention_tier != retention_tier:
              existing.retention_tier = retention_tier
- Failure: Two first attempts for the same learner/node can both observe no card state and both insert one. The `(learner_id, subject_type, subject_id)` unique index rejects one flush with `IntegrityError`, turning a normal concurrent evidence/scheduling request into a 500; unlike `get_or_create_review_policy`, this path has no savepoint/requery recovery.
- Test coverage: No. Checked `tests/scheduling/test_review_policies.py`, which tests concurrent recovery only for policies, and `tests/scheduling/test_review_queue.py`; neither races `get_or_seed_card_state` across two sessions.
- Fix sketch: Mirror the policy helper’s nested-transaction pattern: attempt the insert in a savepoint, catch the unique violation, then select and return the winning row. Add a two-session PostgreSQL test because SQLite’s test connection topology does not faithfully model this race.

### F6 — The pending-draft ceiling is bypassable by concurrent seed commands
- Dimension: D1
- Severity: P2
- Evidence: `src/lms/maintenance/drafts.py:146-169`; `src/lms/__main__.py:641-657`
- Snippet:
      def can_accept_drafts(
          session: Session, *, learner_id: str, wanted: int = 1, now: datetime | None = None
      ) -> bool:
          """Whether ``wanted`` more drafts fit under the cap."""
          return remaining_draft_capacity(session, learner_id=learner_id, now=now) >= wanted
- Failure: Two `lms maintenance load` processes can each count 39 pending drafts, both accept one item, and commit 41 drafts even though `PENDING_DRAFT_CAP` is 40. There is no database constraint or lock tying the count check to the subsequent `session.add()` loop, so the stated structural backlog limit is not structural.
- Test coverage: No. Checked `tests/maintenance/test_draft_approval.py`; it checks a single session at the boundary, not two transactions interleaving check and insert.
- Fix sketch: Serialize draft admission per learner with a row lock/admission counter, or atomically reserve capacity before inserting the batch. Add a Postgres two-session test that coordinates both reads before either writes and asserts one command is refused.

### F7 — “Latest” learner feedback is nondeterministic for same-timestamp attempts
- Dimension: D1
- Severity: P2
- Evidence: `src/lms/ui/api.py:1383-1391`; `src/lms/ui/attempts.py:384-390`; `src/lms/api/inspect.py:126-142`
- Snippet:
      attempt = session.scalars(
          select(Attempt)
          .where(Attempt.learner_id == learner_id, Attempt.prompt_id == prompt_id)
          .order_by(Attempt.created_at.desc())
          .limit(1)
- Failure: If two attempts for a prompt share `created_at` (common for fixture/imported rows or database timestamp resolution), the dashboard may display either attempt’s evidence and feedback as “latest.” Similar one-row latest queries for rubric score and inspect prompts omit an ID tie-breaker, while other list queries consistently add it.
- Test coverage: No. Checked `tests/ui/test_learner_dashboard.py`, `tests/ui/test_activity_attempt_flow.py`, and `tests/evidence/test_attempts.py`; none creates tied timestamps and asserts a stable chosen record.
- Fix sketch: Add a stable secondary key (`Attempt.id.desc()`, `RubricScore.id.desc()`, `Prompt.id.desc()`) to every one-row latest query. Add tied-timestamp tests that assert the same record is rendered across repeated reads and PostgreSQL/SQLite.

