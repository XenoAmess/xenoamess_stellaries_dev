"""Exact annual boundary with one native communications_spread.2 pending."""
import json, logging, shutil, sys, zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, m = h.load_run()
dest = run / Path(__file__).name
if dest.exists():
    assert dest.read_bytes() == Path(__file__).read_bytes()
else:
    shutil.copyfile(__file__, dest)
before, after = 'terravore-native-meditate-year4', 'terravore-native-meditate-year5'
def read(st):
    a = json.loads((run / (st + '.audit.json')).read_text('utf-8'))
    with zipfile.ZipFile(run / (st + '.sav')) as z:
        t = z.read('gamestate').decode('utf-8-sig')
    return a, t
b, bt = read(before)
a, at = read(after)
original = json.loads((run / (after + '-meditate-year-proof.json')).read_text('utf-8'))
execution = json.loads((run / (after + '-guard-execution.json')).read_text('utf-8'))
pending = [v for k, v, o in q.fields(at) if k == 'player_event' and o and q.scalars(v).get('country') == 0]
source = h.GAME_EXE.parent / 'events/communications_spread.txt'
ev = [v for k, v, o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id') == 'communications_spread.2']
assert len(ev) == 1
opts = [v for k, v, o in q.fields(ev[0]) if k == 'option' and o]
hidden = q.block(opts[0], 'hidden_effect') if len(opts) == 1 else ''
scope = q.block(pending[0], 'scope') if len(pending) == 1 else ''
checks = {
    'bound_original40_only_pending_FAIL_exit1': original['status'] == 'FAIL' and len(original['checks']) == 40 and {k for k, v in original['checks'].items() if not v} == {'no_country0_pending'} and execution['returncode'] == 1,
    'original_SHA_pair': h.sha256(run / (before + '.sav')) == b['save_sha256'] == original['before_sha256'] and h.sha256(run / (after + '.sav')) == a['save_sha256'] == original['after_sha256'],
    'calendar_actual_exit0': json.loads((run / (after + '-observe-execution.json')).read_text('utf-8'))['returncode'] == 0,
    'actual_year_and_progress60_stage1': b['date'] == '2249.06.02' and a['date'] == '2250.06.02' and original['days'] == 360 and b['situations']['16777221']['progress'] == 391.25 and a['situations']['16777221']['progress'] == 451.25,
    'exact_native178_pending_country_scope_and_FROM': len(pending) == 1 and q.scalars(pending[0]) == {'id': 178, 'event': 'communications_spread.2', 'date': '2252.04.01', 'country': 0} and q.scalars(scope).get('type') == 'country' and q.scalars(scope).get('id') == 0 and q.scalars(q.block(scope, 'from')).get('type') == 'country' and q.scalars(q.block(scope, 'from')).get('id') == 16777219,
    'native_event_has_no_immediate_effect': not q.block(ev[0], 'immediate'),
    'native_only_option_FROM_target_then_action1': len(opts) == 1 and [(k, o) for k, v, o in q.fields(opts[0]) if k not in ['name', 'custom_tooltip']] == [('hidden_effect', True)] and [(k, o) for k, v, o in q.fields(hidden)] == [('FROM', True), ('country_event', True)] and q.scalars(q.block(hidden, 'FROM')) == {'save_event_target_as': 'contact_empire'} and q.scalars(q.block(hidden, 'country_event')) == {'id': 'action.1'},
    'other39_original_checks_true': all(v is True for k, v in original['checks'].items() if k != 'no_country0_pending'),
}
p = {'status': 'PASS_NATIVE_YEAR5_CONTACT_PENDING_COMPONENT' if all(checks.values()) else 'FAIL', 'checks': checks, 'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'], 'calendar_ready': False, 'native_source': {'path': str(source), 'sha256': h.sha256(source)}, 'scope': 'Original annual boundary plus exact native pending178. Original40 FAIL retained, no calendar clearance.'}
out = run / (after + '-native-contact-pending-supplement.json')
assert not out.exists()
h.write_json(out, p)
print(json.dumps(p), flush=True)
assert all(checks.values()), 'Original annual contact supplement FAIL retained'
