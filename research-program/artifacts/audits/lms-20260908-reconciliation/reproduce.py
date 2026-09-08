"""Bounded audit reproductions; synthetic in-memory data, no source changes."""
import importlib.util
import json
import math
import tempfile
from pathlib import Path
from types import SimpleNamespace

from lms.feedback.models import FeedbackRecord
from lms.feedback.scoring import _normalize_criterion_scores
from lms.capability.repository import _as_float, create_capability_target
from lms.graphs.repository import create_knowledge_node
from lms.importers.csv_graph import import_csv_graph
from lms.llm.models import LLMSession
from lms.llm.proposals import LLMProposal
from lms.export_import import MODEL_BY_TYPE

root = Path(__file__).resolve().parents[3] / 'clones/learning-management-system'
spec = importlib.util.spec_from_file_location('ownership_fixture', root / 'tests/api/test_deployed_learner_ownership.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fixture = module._deployed_client()
client, session = next(fixture)
results = {}
try:
    record = session.query(FeedbackRecord).filter_by(learner_id=client.other_learner_id).one()
    response = client.get(f'/app/learner/feedback/{record.id}')
    results['620'] = {'foreign_detail_http': response.status_code, 'private_goal_visible': 'Foreign goal' in response.text}
    assert response.status_code == 200 and 'Foreign goal' in response.text

    node = create_knowledge_node(session, title='Synthetic private target node', knowledge_type='conceptual', scope='personal', actor_id='audit', status='draft')
    target = create_capability_target(session, learner_id=client.other_learner_id, title='Synthetic foreign target', target_node_ids=[node.id])
    session.commit()
    response = client.get(f'/app/learner/capability/targets/{target.id}')
    estimate = client.post('/app/learner/capability/estimates', data={'target_id': target.id})
    results['621'] = {'foreign_detail_http': response.status_code, 'private_title_visible': 'Synthetic foreign target' in response.text, 'foreign_recompute_http': estimate.status_code}
    assert response.status_code == estimate.status_code == 200

    trace = LLMSession(mode='authoring-assist', trace_class='evidence-grade', provider='fake', model='audit', learner_id=client.other_learner_id, response_summary='Synthetic private summary')
    session.add(trace)
    session.commit()
    response = client.post(f'/llm/sessions/{trace.id}/trace-control', json={'actor_id': client.other_learner_id, 'action': 'forget'})
    session.refresh(trace)
    results['622'] = {'authenticated_foreign_forget_http': response.status_code, 'summary_cleared': trace.response_summary is None}
    assert response.status_code == 200 and trace.response_summary is None

    criterion = SimpleNamespace(id='audit-criterion', status='active', max_points=10, criterion_order=1, description='Synthetic criterion')
    normalized = _normalize_criterion_scores(SimpleNamespace(criteria=[criterion]), [{'criterion_id': criterion.id, 'points': float('nan')}])
    results['623'] = {'normalizer_accepts_nan': math.isnan(normalized[0]['points'])}
    assert results['623']['normalizer_accepts_nan']

    missing = [name for name in ['Hint', 'HintReveal', 'ModelAnswer', 'ModelAnswerReveal', 'RevisionRequest', 'FeedbackTemplate', 'WorkProduct', 'LearnerReflection'] if name not in MODEL_BY_TYPE]
    results['624'] = {'missing_registry_entries': missing}
    assert len(missing) == 8

    proposal = LLMProposal(llm_session_id=trace.id, llm_model='audit', proposed_by='audit', knowledge_node_id=node.id)
    session.add(proposal)
    session.commit()
    statuses = [client.post(f'/app/author/graph/proposals/{proposal.id}/{action}', data={'ownership_scope': 'personal'}).status_code for action in ['approve', 'approve', 'reject', 'reject']]
    missing_response = client.post('/app/author/graph/proposals/missing/approve', data={'ownership_scope': 'personal'})
    results['627'] = {'approve_approve_reject_reject_http': statuses, 'missing_proposal_http': missing_response.status_code, 'missing_notice_present': 'Proposal not found.' in missing_response.text, 'disposition': 'REFUTED'}
    assert statuses == [200] * 4 and missing_response.status_code == 200

    results['626'] = {'nan_accepted': math.isnan(_as_float('nan')), 'inf_accepted': math.isinf(_as_float('inf'))}
    try:
        _as_float('invalid')
    except ValueError:
        results['626']['malformed_raises_value_error'] = True
    assert all(results['626'].values())

    with tempfile.TemporaryDirectory(prefix='lms-audit-csv-') as temp:
        csv = Path(temp) / 'cycle.csv'
        csv.write_text('title,knowledge_type,prerequisites,ownership_scope,status,source_locator\nA,conceptual,B,personal,draft,audit\nB,conceptual,A,personal,draft,audit\n')
        dry = import_csv_graph(session, csv, dry_run=True)
        results['625'] = {'dry_run_accepts_cycle': dry.nodes == 2 and dry.edges == 2}
        try:
            import_csv_graph(session, csv)
        except ValueError as exc:
            results['625']['live_exception_type'] = type(exc).__name__
            results['625']['live_exception'] = str(exc)
        assert results['625']['live_exception_type'] == 'ValueError'
        session.rollback()
finally:
    fixture.close()
print(json.dumps(results, indent=2))
