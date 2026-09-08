## src/lms/__main__.py:526-526
526:         except CsvGraphImportError as exc:
## src/lms/__main__.py:526-527
526:         except CsvGraphImportError as exc:
527:             raise SystemExit(f"CSV graph import failed: {exc}") from exc
## src/lms/auth/dependencies.py:100-100
## src/lms/capability/repository.py:221-240
221:     score_components = [_as_float(row["current_estimate"]) for row in node_rows]
222:     score_components.extend(_as_float(row["weighted_score"]) for row in competency_rows)
223:     current_score = (
224:         round(sum(score_components) / len(score_components), 4) if score_components else 0.0
225:     )
226: 
227:     confidence_components = [_as_float(row["confidence"]) for row in node_rows]
228:     confidence_components.extend(_as_float(row["confidence"]) for row in competency_rows)
229:     coverage = _coverage_factor(node_rows=node_rows, competency_rows=competency_rows)
230:     confidence = (
231:         round((sum(confidence_components) / len(confidence_components)) * coverage, 4)
232:         if confidence_components
233:         else 0.0
234:     )
235:     weak_node_ids = [
236:         str(row["knowledge_node_id"])
237:         for row in node_rows
238:         if _as_float(row["current_estimate"]) < target.confidence_threshold
239:         or _as_float(row["confidence"]) < target.confidence_threshold
240:     ]
## src/lms/capability/repository.py:225-225
225:     )
## src/lms/capability/repository.py:230-245
230:     confidence = (
231:         round((sum(confidence_components) / len(confidence_components)) * coverage, 4)
232:         if confidence_components
233:         else 0.0
234:     )
235:     weak_node_ids = [
236:         str(row["knowledge_node_id"])
237:         for row in node_rows
238:         if _as_float(row["current_estimate"]) < target.confidence_threshold
239:         or _as_float(row["confidence"]) < target.confidence_threshold
240:     ]
241:     evidence_breakdown = _json_safe(
242:         {
243:             "target_node_estimates": node_rows,
244:             "competency_evidence": competency_rows,
245:             "required_evidence_types": target.required_evidence_types,
## src/lms/export_import.py:62-130
62: MODEL_BY_TYPE = {
63:     "User": User,
64:     "Learner": Learner,
65:     "SourceReference": SourceReference,
66:     "KnowledgeNode": KnowledgeNode,
67:     "KnowledgeEdge": KnowledgeEdge,
68:     "LearningGoal": LearningGoal,
69:     "Prompt": Prompt,
70:     "PromptVersion": PromptVersion,
71:     "LLMSession": LLMSession,
72:     "Attempt": Attempt,
73:     "EvidenceRecord": EvidenceRecord,
74:     "Competency": Competency,
75:     "CompetencyEvidence": CompetencyEvidence,
76:     "FeedbackRecord": FeedbackRecord,
77:     "FeedbackAction": FeedbackAction,
78:     "MisconceptionPattern": MisconceptionPattern,
79:     "Rubric": Rubric,
80:     "RubricCriterion": RubricCriterion,
81:     "RubricScore": RubricScore,
82:     "Case": Case,
83:     "CaseStep": CaseStep,
84:     "EvidencePacket": EvidencePacket,
85:     "DecisionPoint": DecisionPoint,
86:     "ReviewQueueItem": ReviewQueueItem,
87:     "ReviewPolicy": ReviewPolicy,
88:     "ReviewSchedule": ReviewSchedule,
89:     "RemediationTrigger": RemediationTrigger,
90:     "SchedulerDecision": SchedulerDecision,
91:     "CapabilityTarget": CapabilityTarget,
92:     "CapabilityEstimate": CapabilityEstimate,
93:     "GapAnalysis": GapAnalysis,
94:     "MaintenancePlan": MaintenancePlan,
95: }
96: 
97: EXPORT_ORDER = (
98:     User,
99:     Learner,
100:     SourceReference,
101:     KnowledgeNode,
102:     KnowledgeEdge,
103:     LearningGoal,
104:     Prompt,
105:     PromptVersion,
106:     LLMSession,
107:     Attempt,
108:     EvidenceRecord,
109:     Competency,
110:     CompetencyEvidence,
111:     FeedbackRecord,
112:     FeedbackAction,
113:     MisconceptionPattern,
114:     Rubric,
115:     RubricCriterion,
116:     RubricScore,
117:     Case,
118:     CaseStep,
119:     EvidencePacket,
120:     DecisionPoint,
121:     ReviewQueueItem,
122:     ReviewPolicy,
123:     ReviewSchedule,
124:     RemediationTrigger,
125:     SchedulerDecision,
126:     CapabilityTarget,
127:     CapabilityEstimate,
128:     GapAnalysis,
129:     MaintenancePlan,
130: )
## src/lms/feedback/scoring.py:233-237
233:         points = float(item.get("points", 0))
234:         if points < 0 or points > criterion.max_points:
235:             raise InvalidRubricScoringError(
236:                 "criterion score points must be within criterion max_points"
237:             )
## src/lms/importers/csv_graph.py:113-126
113:     for row in rows:
114:         source_node_id = nodes_by_key[_node_key(row.ownership_scope, row.title)]
115:         for prerequisite_title in row.prerequisites:
116:             target_node_id = nodes_by_key[_node_key(row.ownership_scope, prerequisite_title)]
117:             create_knowledge_edge(
118:                 session,
119:                 source_node_id=source_node_id,
120:                 target_node_id=target_node_id,
121:                 edge_type="prerequisite",
122:                 scope=row.ownership_scope,
123:                 actor_id=actor_id,
124:                 status="draft",
125:                 source_subsystem="csv-graph-importer",
126:             )
## src/lms/importers/csv_graph.py:120-120
120:                 target_node_id=target_node_id,
## src/lms/llm/api.py:657-686
657: @router.post("/sessions/{session_id}/trace-control", response_model=LLMTraceControlRead)
658: def control_llm_trace_route(
659:     session_id: str,
660:     payload: LLMTraceControlRequest,
661:     session: SessionDep,
662: ) -> LLMTraceControlRead:
663:     """Apply a learner keep/forget override to one persisted LLM session."""
664:     llm_session = session.get(LLMSession, session_id)
665:     if llm_session is None:
666:         raise HTTPException(status_code=404, detail="LLM session not found")
667:     if llm_session.learner_id != payload.actor_id:
668:         raise HTTPException(status_code=404, detail="LLM session not found")
669:     try:
670:         apply_trace_control(
671:             session,
672:             llm_session,
673:             action=payload.action,
674:             actor_id=payload.actor_id,
675:         )
676:     except ValueError as exc:
677:         raise HTTPException(status_code=422, detail=str(exc)) from exc
678:     session.commit()
679:     session.refresh(llm_session)
680:     return LLMTraceControlRead(
681:         session_id=llm_session.id,
682:         trace_class=llm_session.trace_class,
683:         trace_control_state=llm_session.trace_control_state,
684:         response_summary_retained=llm_session.response_summary is not None,
685:         external_export_allowed=llm_session.external_export_allowed,
686:     )
## src/lms/llm/api.py:666-666
666:         raise HTTPException(status_code=404, detail="LLM session not found")
## src/lms/ui/capability_gap.py:92-221
92: @router.get(f"{CAPABILITY_PATH}/targets/{{target_id}}", response_class=HTMLResponse)
93: def capability_target_detail_route(target_id: str, session: SessionDep) -> str:
94:     """Return the detail surface for one personal capability target."""
95:     target = _target_payload(session, target_id)
96:     if target is None:
97:         return _not_found_page()
98:     return _detail_surface(session=session, target=target, notice=None)
99: 
100: 
101: @router.post(TARGETS_PATH, response_class=HTMLResponse)
102: async def create_capability_target_action(
103:     request: Request,
104:     session: SessionDep,
105:     settings: SettingsDep,
106:     current_user: CurrentUserDep,
107: ) -> str:
108:     """Create a personal capability target from the overview form."""
109:     form = _parse_form((await request.body()).decode())
110:     learner_id = resolve_learner_id(
111:         session,
112:         user=current_user,
113:         settings=settings,
114:         requested=_one(form, "learner_id", "") or None,
115:     )
116:     try:
117:         payload = CapabilityTargetCreate(
118:             learner_id=learner_id,
119:             title=_one(form, "title"),
120:             description=_one(form, "description") or None,
121:             target_node_ids=_many(form, "target_node_ids"),
122:             target_competency_ids=_many(form, "target_competency_ids"),
123:             required_evidence_types=_split_tokens(_one(form, "required_evidence_types")),
124:             confidence_threshold=_float_or_default(
125:                 _optional_float(_one(form, "confidence_threshold")), 0.8
126:             ),
127:         )
128:     except (ValidationError, ValueError):
129:         return _overview_surface(
130:             session=session,
131:             learner_id=learner_id,
132:             error=(
133:                 "Enter a title and select at least one knowledge node or competency "
134:                 "for this personal capability target."
135:             ),
136:         )
137:     try:
138:         target_model = create_capability_target(
139:             session,
140:             learner_id=payload.learner_id,
141:             title=payload.title,
142:             description=payload.description,
143:             ownership_scope=payload.ownership_scope,
144:             learning_goal_id=payload.learning_goal_id,
145:             target_node_ids=payload.target_node_ids,
146:             target_competency_ids=payload.target_competency_ids,
147:             required_evidence_types=payload.required_evidence_types,
148:             confidence_threshold=payload.confidence_threshold,
149:             status=payload.status,
150:         )
151:         session.commit()
152:         session.refresh(target_model)
153:         target = serialize_capability_target(target_model)
154:     except ValueError as exc:
155:         session.rollback()
156:         return _overview_surface(session=session, learner_id=learner_id, error=str(exc))
157:     return _detail_surface(
158:         session=session, target=target, notice="Saved your personal capability target."
159:     )
160: 
161: 
162: @router.post(ESTIMATES_PATH, response_class=HTMLResponse)
163: async def recompute_estimate_action(request: Request, session: SessionDep) -> str:
164:     """Recompute a current capability estimate for one target."""
165:     form = _parse_form((await request.body()).decode())
166:     target_id = _one(form, "target_id")
167:     try:
168:         payload = CapabilityEstimateRecompute(target_id=target_id)
169:         estimate = recompute_capability_estimate(session, target_id=payload.target_id)
170:         session.commit()
171:         session.refresh(estimate)
172:     except (ValidationError, ValueError) as exc:
173:         session.rollback()
174:         return _action_error(session=session, target_id=target_id, exc=exc)
175:     return _detail_after_action(
176:         session=session,
177:         target_id=target_id,
178:         notice="Recomputed your current capability estimate from the latest evidence.",
179:     )
180: 
181: 
182: @router.post(GAP_PATH, response_class=HTMLResponse)
183: async def create_gap_analysis_action(request: Request, session: SessionDep) -> str:
184:     """Generate a gap analysis from the most recent estimate."""
185:     form = _parse_form((await request.body()).decode())
186:     target_id = _one(form, "target_id")
187:     try:
188:         payload = GapAnalysisCreate(estimate_id=_one(form, "estimate_id"))
189:         analysis = create_gap_analysis(session, estimate_id=payload.estimate_id)
190:         session.commit()
191:         session.refresh(analysis)
192:         target_id = analysis.target_id
193:     except (ValidationError, ValueError) as exc:
194:         session.rollback()
195:         return _action_error(session=session, target_id=target_id, exc=exc)
196:     return _detail_after_action(
197:         session=session,
198:         target_id=target_id,
199:         notice="Generated a gap analysis from your current evidence.",
200:     )
201: 
202: 
203: @router.post(PLAN_PATH, response_class=HTMLResponse)
204: async def create_maintenance_plan_action(request: Request, session: SessionDep) -> str:
205:     """Create a maintenance plan with scheduled next steps from a gap analysis."""
206:     form = _parse_form((await request.body()).decode())
207:     target_id = _one(form, "target_id")
208:     try:
209:         payload = MaintenancePlanCreate(gap_analysis_id=_one(form, "gap_analysis_id"))
210:         plan = create_maintenance_plan(session, gap_analysis_id=payload.gap_analysis_id)
211:         session.commit()
212:         session.refresh(plan)
213:         target_id = plan.target_id
214:     except (ValidationError, ValueError) as exc:
215:         session.rollback()
216:         return _action_error(session=session, target_id=target_id, exc=exc)
217:     return _detail_after_action(
218:         session=session,
219:         target_id=target_id,
220:         notice="Created a maintenance plan with scheduled next steps.",
221:     )
## src/lms/ui/capability_gap.py:98-98
98:     return _detail_surface(session=session, target=target, notice=None)
## src/lms/ui/feedback.py:80-184
80: @router.get("/app/learner/feedback/{feedback_record_id}", response_class=HTMLResponse)
81: def learner_feedback_detail_route(feedback_record_id: str, session: SessionDep) -> str:
82:     """Return one learner feedback detail page."""
83:     record = get_feedback_record(session, feedback_record_id)
84:     if record is None:
85:         return _missing_feedback_page()
86:     return _feedback_detail_page(session, record)
87: 
88: 
89: @router.post("/app/learner/feedback/{feedback_record_id}/hints/{hint_id}/reveal")
90: def learner_hint_reveal_route(
91:     feedback_record_id: str,
92:     hint_id: str,
93:     session: SessionDep,
94: ) -> HTMLResponse:
95:     """Reveal a hint from the feedback detail page."""
96:     record = get_feedback_record(session, feedback_record_id)
97:     hint = get_hint(session, hint_id)
98:     if record is None or hint is None:
99:         return HTMLResponse(_missing_feedback_page(), status_code=404)
100:     try:
101:         reveal_hint(
102:             session,
103:             hint,
104:             learner_id=record.learner_id,
105:             attempt_id=record.attempt_id,
106:         )
107:         session.commit()
108:     except ValueError as exc:
109:         session.rollback()
110:         return HTMLResponse(_feedback_detail_page(session, record, error=str(exc)), status_code=422)
111:     return HTMLResponse(
112:         _feedback_detail_page(session, record, message=f"Hint revealed: {hint.hint_text}")
113:     )
114: 
115: 
116: @router.post("/app/learner/feedback/{feedback_record_id}/model-answers/{model_answer_id}/reveal")
117: def learner_model_answer_reveal_route(
118:     feedback_record_id: str,
119:     model_answer_id: str,
120:     session: SessionDep,
121: ) -> HTMLResponse:
122:     """Reveal a model answer after backend policy allows it."""
123:     record = get_feedback_record(session, feedback_record_id)
124:     answer = get_model_answer(session, model_answer_id)
125:     if record is None or answer is None:
126:         return HTMLResponse(_missing_feedback_page(), status_code=404)
127:     try:
128:         reveal_model_answer(
129:             session,
130:             answer,
131:             learner_id=record.learner_id,
132:             attempt_id=record.attempt_id,
133:         )
134:         session.commit()
135:     except ValueError as exc:
136:         session.rollback()
137:         return HTMLResponse(_feedback_detail_page(session, record, error=str(exc)), status_code=422)
138:     return HTMLResponse(
139:         _feedback_detail_page(
140:             session,
141:             record,
142:             message=f"Model answer revealed: {reveal_model_answer_text(answer.answer_body)}",
143:         )
144:     )
145: 
146: 
147: @router.post("/app/learner/feedback/{feedback_record_id}/revision")
148: async def learner_revision_submit_route(
149:     feedback_record_id: str,
150:     request: Request,
151:     session: SessionDep,
152: ) -> HTMLResponse:
153:     """Open or reuse a revision request and submit the learner revision."""
154:     record = get_feedback_record(session, feedback_record_id)
155:     if record is None:
156:         return HTMLResponse(_missing_feedback_page(), status_code=404)
157:     form = await _read_form(request)
158:     response_text = form.get("response_text", "").strip()
159:     if not response_text:
160:         return HTMLResponse(
161:             _feedback_detail_page(session, record, error="Revision response is required."),
162:             status_code=422,
163:         )
164:     try:
165:         revision = _open_revision_request(session, record)
166:         submit_revision_request(
167:             session,
168:             revision,
169:             response_text=response_text,
170:             confidence_rating=_optional_int(form.get("confidence_rating")),
171:         )
172:         session.commit()
173:         session.refresh(revision)
174:     except ValueError as exc:
175:         session.rollback()
176:         return HTMLResponse(_feedback_detail_page(session, record, error=str(exc)), status_code=422)
177:     return HTMLResponse(
178:         _feedback_detail_page(
179:             session,
180:             record,
181:             message=f"Revision submitted. Status: {revision.status}.",
182:         )
183:     )
184: 
## src/lms/ui/feedback.py:85-85
85:         return _missing_feedback_page()
## src/lms/ui/graph_design.py:96-150
96: @router.post("/app/author/graph/proposals/{proposal_id}/approve", response_class=HTMLResponse)
97: async def approve_graph_proposal_route(
98:     proposal_id: str,
99:     request: Request,
100:     session: SessionDep,
101: ) -> str:
102:     """Publish draft graph artifacts linked to an LLM proposal."""
103:     form = await _form_data(request)
104:     scope = _scope(form.get("ownership_scope"))
105:     message = _set_proposal_status(
106:         session=session,
107:         proposal_id=proposal_id,
108:         node_status="published",
109:         edge_status="published",
110:         actor_id="graph-ui",
111:     )
112:     session.commit()
113:     return _graph_surface(session=session, scope=scope, message=message)
114: 
115: 
116: @router.post("/app/author/graph/proposals/{proposal_id}/reject", response_class=HTMLResponse)
117: async def reject_graph_proposal_route(
118:     proposal_id: str,
119:     request: Request,
120:     session: SessionDep,
121: ) -> str:
122:     """Deprecate draft graph artifacts linked to an LLM proposal."""
123:     form = await _form_data(request)
124:     scope = _scope(form.get("ownership_scope"))
125:     message = _set_proposal_status(
126:         session=session,
127:         proposal_id=proposal_id,
128:         node_status="deprecated",
129:         edge_status="deprecated",
130:         actor_id="graph-ui",
131:     )
132:     session.commit()
133:     return _graph_surface(session=session, scope=scope, message=message)
134: 
135: 
136: def _graph_surface(
137:     *,
138:     session: Session,
139:     scope: str,
140:     learner_id: str | None = None,
141:     message: str | None = None,
142: ) -> str:
143:     nodes = list_knowledge_nodes(session, scope=scope, limit=200)
144:     edges = list_knowledge_edges(session, scope=scope, limit=200)
145:     proposals = _list_graph_proposals(session, scope=scope)
146:     evidence_counts = _evidence_counts(session)
147:     mastery_by_node = _mastery_by_node(session, learner_id=learner_id)
148:     node_options = "".join(
149:         f'<option value="{escape(node.id)}">{escape(node.title)}</option>' for node in nodes
150:     )
## src/lms/ui/graph_design.py:105-105
105:     message = _set_proposal_status(
## tests/api/test_deployed_learner_ownership.py:50-120
50:     session.add_all([owner, other_user])
51:     session.flush()
52:     owner_learner = Learner(user_id=owner.id, display_name="Owner learner")
53:     other_learner = Learner(user_id=other_user.id, display_name="Other learner")
54:     session.add_all([owner_learner, other_learner])
55:     session.flush()
56:     foreign_attempt = Attempt(
57:         learner_id=other_learner.id,
58:         prompt_id="foreign-prompt",
59:         response_text="private response text",
60:         feedback={
61:             "goal": "Foreign private goal",
62:             "observed_evidence": "Foreign private evidence",
63:             "next_action": "Keep private",
64:         },
65:     )
66:     owner_attempt = Attempt(
67:         learner_id=owner_learner.id,
68:         prompt_id="owner-prompt",
69:         response_text="owner response text",
70:         feedback={
71:             "goal": "Owner goal",
72:             "observed_evidence": "Owner evidence",
73:             "next_action": "Keep learning",
74:         },
75:     )
76:     owner_feedback = FeedbackRecord(
77:         learner_id=owner_learner.id,
78:         feedback_level="coaching",
79:         goal="Owner goal",
80:         observed_evidence="Owner evidence",
81:         source_feedback={},
82:     )
83:     foreign_feedback = FeedbackRecord(
84:         learner_id=other_learner.id,
85:         feedback_level="coaching",
86:         goal="Foreign goal",
87:         observed_evidence="Foreign evidence",
88:         source_feedback={},
89:     )
90:     foreign_evidence = EvidenceRecord(
91:         learner_id=other_learner.id,
92:         knowledge_node_id="private-node",
93:         validity_scope="private evidence scope",
94:     )
95:     session.add_all(
96:         [
97:             foreign_attempt,
98:             owner_attempt,
99:             owner_feedback,
100:             foreign_feedback,
101:             foreign_evidence,
102:         ]
103:     )
104:     session.commit()
105: 
106:     def override_session() -> Generator[Session, None, None]:
107:         yield session
108: 
109:     app = create_app(enable_local_identity_routes=False)
110:     app.dependency_overrides[get_session] = override_session
111:     app.dependency_overrides[get_settings] = lambda: Settings(auth_required=auth_required)
112:     app.dependency_overrides[require_authenticated_user] = lambda: owner
113:     try:
114:         with TestClient(app) as client:
115:             client.owner_learner_id = owner_learner.id  # type: ignore[attr-defined]
116:             client.other_learner_id = other_learner.id  # type: ignore[attr-defined]
117:             client.foreign_attempt_id = foreign_attempt.id  # type: ignore[attr-defined]
118:             client.owner_attempt_id = owner_attempt.id  # type: ignore[attr-defined]
119:             client.foreign_evidence_id = foreign_evidence.id  # type: ignore[attr-defined]
120:             yield client, session
