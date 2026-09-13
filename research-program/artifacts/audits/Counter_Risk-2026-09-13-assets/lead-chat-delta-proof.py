"""Run from clone cwd with PYTHONPATH=src; no network or credentials used."""
from pathlib import Path
from types import SimpleNamespace
import json, os, tempfile
import pytest
import counter_risk.chat.session as s
import counter_risk.chat.providers.base as b
from counter_risk.chat.context import RunContext

out=Path(__file__).parent
with tempfile.TemporaryDirectory(prefix='cr-chat-proof-') as tmp, pytest.MonkeyPatch.context() as m:
    m.setenv('COUNTER_RISK_CHAT_OFFLINE_MODE','1')
    captured=[]
    class Transport:
        def invoke(self,messages,config):
            captured.append(messages)
            return SimpleNamespace(content='Captured transport only; no model call.')
    m.setattr(b,'build_chat_client',lambda **kw: SimpleNamespace(client=Transport(),provider='probe',model='probe'))
    m.setattr(b,'get_provider_model_catalog',lambda: {})
    m.setattr(b,'missing_provider_dependencies',lambda p: ())
    m.setattr(s,'provider_dependency_error',lambda p: None)
    m.setitem(s._PROVIDER_CLIENTS,'local',b.LangChainProviderClient(provider_chain=('probe',),required_env_keys=()))
    context=RunContext(run_dir=Path(tmp),manifest={'as_of_date':'2025-12-31'},tables={},warnings=[],deltas={'all_programs':[{'counterparty':'DeltaOnlyBank','delta_notional':876543.21}]},chat_logs=[])
    session=s.ChatSession(context=context,provider='local',model=s._PLACEHOLDER_MODEL,log_mode='off')
    computed=session._answer_from_context('show deltas')
    session.ask('show deltas')
    transmitted=json.dumps(captured)
    assert 'DeltaOnlyBank' in computed, computed
    assert 'DeltaOnlyBank' not in transmitted and '876543' not in transmitted,transmitted
    result={'computed_context_answer':computed,'actual_transport_messages':captured,'result':'CONFIRMED: delta values exist locally but are omitted from actual LangChain invoke messages; fake final transport only.'}
    (out/'lead-chat-delta-proof.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
