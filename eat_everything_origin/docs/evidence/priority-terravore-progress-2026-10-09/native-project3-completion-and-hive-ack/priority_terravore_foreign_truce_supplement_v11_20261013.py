"""Supplement one immutable monthly failure for an unrelated native truce expiry."""
import hashlib
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = 'terravore-post-second-society-month-22880601'
after = 'terravore-post-second-society-month-22880701'
old_stage = after + '-post-second-society-month-guard-v4'
old_file = after + '-post-second-society-month-v4-proof.json'
old = json.loads((run / old_file).read_text('utf-8'))
execution = json.loads((run / (old_stage + '-execution.json')).read_text('utf-8'))
driver = json.loads((run / 'terravore-post-hive-final-three-project3-months-driver-execution.json').read_text('utf-8'))
b, a = [read_state(run, stage) for stage in (before, after)]
target = 'no_unknown_news_pending_delayed_event_war_truce_combat'
defines_path = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/defines/00_defines.txt')
defines_raw = defines_path.read_bytes()
old_truce = b['roots']['truce']
new_truce = a['roots']['truce']
old_16777216 = q.block(old_truce, '16777216')
old_1 = q.block(old_truce, '1')
new_1 = q.block(new_truce, '1')
observe = json.loads((run / (after + '-construction-boundary-observation-v4.json')).read_text('utf-8'))

def truce_relations(state, country_id):
    raw = q.block(q.block(state['roots']['country'], str(country_id)), 'relations_manager')
    return [(v.get('owner'), v.get('country'), v.get('truce'))
            for key, value, obj in q.fields(raw) if key == 'relation' and obj
            if (v := q.scalars(value)).get('truce') == 16777216]

delays = [q.scalars(value)
          for key, value, obj in q.fields(q.block(q.block(a['country'], 'modules'), 'standard_event_module'))
          if key == 'delayed_event' and obj]
combat = [(fid, q.ids(q.block(q.block(raw, 'combat'), 'in_combat_with')))
          for fid, raw in a['fleets'].items()]
start = q.scalars(old_16777216).get('start_date')
expiry = '2288.06.25'
checks = {
    'original_one_v4_fail_17_true_actual1_driver_stop_same_native_saves':
        old['status'] == 'FAIL' and len(old['checks']) == 18
        and {key for key, value in old['checks'].items() if value is not True} == {target}
        and execution['returncode'] == driver['returncode'] == 1
        and execution['helper_sha256'] == '29bc0ae0b292f63681813bfedac9682ba138db6b46d28a9446e21de52101f79d'
        and driver['helper_sha256'] == 'fd9d41ff2aca0d152d0d17224db53ce29501c06562692204c7ef37019c42a028'
        and hashlib.sha256(Path(execution['command'][1]).read_bytes()).hexdigest() == execution['helper_sha256']
        and old['before_sha256'] == b['audit']['save_sha256'] == h.sha256(run / (before + '.sav'))
        and old['after_sha256'] == a['audit']['save_sha256'] == h.sha256(run / (after + '.sav')),
    'only_truce16777216_native_entity_to_none_truce1_held':
        {key for key, _, _ in q.fields(old_truce)} == {key for key, _, _ in q.fields(new_truce)} == {'16777216', '1'}
        and old_16777216 and q.scalars(old_16777216).get('truce_type') == 'war'
        and q.scalars(new_truce).get('16777216') == 'none'
        and not q.block(new_truce, '16777216')
        and old_1 == new_1
        and b['roots']['war'] == a['roots']['war'],
    'foreign_only_16777218_and_16777219_referenced_expired_truce':
        all(truce_relations(state, 0) == [] for state in (b, a))
        and all(truce_relations(state, 16777218) == [(16777218, 16777219, 16777216)]
                for state in (b, a))
        and all(truce_relations(state, 16777219) == [(16777219, 16777218, 16777216)]
                for state in (b, a)),
    'installed_vanilla_ten_years_truce_expired_inside_native_month':
        bool(re.search(rb'\bTRUCE_YEARS\s*=\s*10\b', defines_raw))
        and start == '2278.06.25' and expiry == f'{int(start[:4]) + 10}{start[4:]}'
        and b['audit']['date'] < expiry <= a['audit']['date'],
    'no_new_player_event_war_pending_delayed_or_combat':
        not observe['new_country0_messages_raw'] and not a['pending'] and not delays
        and all(not enemies for _, enemies in combat)
        and observe['after_sha256'] == old['after_sha256'],
}
passed = all(value is True for value in checks.values())
out = run / (after + '-post-second-society-month-v11-proof.json')
assert not out.exists()
supplement = dict(old)
supplement.update({
    'status': 'PASS_NATIVE_FOREIGN_TRUCE_EXPIRY_SUPPLEMENT' if passed else 'FAIL',
    'checks': dict(old['checks'], **{target: passed},
                   **{'foreign_truce_' + key: value for key, value in checks.items()}),
    'original_failed_proof': old_file,
    'original_failed_execution_stage': old_stage,
    'original_stopped_driver_stage': 'terravore-post-hive-final-three-project3-months-driver',
    'installed_vanilla_defines_sha256': hashlib.sha256(defines_raw).hexdigest(),
    'scope': 'One exact foreign truce expiry in Jun1-Jul1; no future truce exception.',
})
h.write_json(out, supplement)
print(json.dumps({'status': supplement['status'], 'checks': len(supplement['checks']),
                  'failed': [key for key, value in supplement['checks'].items() if value is not True],
                  'save_sha256': old['after_sha256']}), flush=True)
assert passed
