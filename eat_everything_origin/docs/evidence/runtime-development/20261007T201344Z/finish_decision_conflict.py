import json
import logging
from pathlib import Path
import shutil
import sys
import time

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
order = manifest['conflict_order']
prefix = 'conflict-' + order
shutil.copyfile(Path(__file__), run / 'finish_decision_conflict.py')
before = json.loads((run / (prefix + '-restored.audit.json')).read_text(encoding='utf-8'))
start = r.native_save(prefix + '-native-ui-start', '2200.01.01', (0,))
tasks = [value for value in start['situations'].values() if value['type'] in ('situation_eep_devouring', 'situation_terravore_consume_planet')]
assert len(tasks) == 1, tasks
task = tasks[0]
source = str(task['target']['id'])
assert task['country'] == 0 and task['progress'] == 0
assert start['planets'][source]['planet_size'] == 20
assert start['colonies'][str(start['planets'][source]['colony'])]['actual_pop_sum'] == 100
expected = 'situation_terravore_consume_planet' if order == 'eep-first' else 'situation_eep_devouring'
assert task['type'] == expected, (task, manifest['enabled_mods'])
print(json.dumps({'order': order, 'actual_type': task['type'], 'source': source, 'start_sha256': start['save_sha256']}), flush=True)
h.press_scan_code(0x29, prefix + '-month-console-open', 1)
h.type_text('fast_forward 30', True, prefix + '-actual-first-month')
for attempt in range(15):
    frame = r.gpu_capture(prefix + '-month-completion-' + str(attempt))
    texts = [row['text'] for row in frame['rows']]
    if '2200.02.01' in texts and any('fastforwarded30days' in h.normalized(label) for label in texts):
        break
    time.sleep(5)
else:
    raise RuntimeError('actual first month did not complete')
h.press_scan_code(0x29, prefix + '-month-console-close', 1)
end = r.native_save(prefix + '-native-first-month', '2200.02.01', (0,))
checks = []
def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})
check('actual enabled_mods matches manifest bytes', json.loads((user / 'dlc_load.json').read_text(encoding='utf-8-sig'))['enabled_mods'] == manifest['enabled_mods'] and h.sha256(user / 'dlc_load.json') == manifest['dlc_load_sha256'])
check('primary fixture immutable', h.tree_manifest(Path(manifest['copied_mod']))[1] == manifest['copied_mod_tree_sha256'])
check('second control immutable', h.tree_manifest(Path(manifest['conflict_mod']['copied']))[1] == manifest['conflict_mod']['tree_sha256'])
check('same zero source bytes loaded', json.loads((run / (prefix + '-restore-exact-zero.load.json')).read_text(encoding='utf-8'))['source_sha256'] == '796f0fe3083641b413cae3e2f62674548da96e146e11760dd5211a10cfd11be5')
check('actual native decision clicked', (run / (prefix + '-native-original-decision-click.action.json')).is_file())
check('same actual source selected', source == '1115')
check('start date and free decision stocks', start['date'] == '2200.01.01' and start['countries']['0']['stockpile'] == before['countries']['0']['stockpile'])
for state in (start, end):
    label = state['date']
    tasks = [value for value in state['situations'].values() if value['type'] == expected]
    check(label + ' actual routed type/owner/target', len(tasks) == 1 and tasks[0]['country'] == 0 and str(tasks[0]['target']['id']) == source)
    check(label + ' no premature credit/manufacture', all(state['countries']['0']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_made', 0), ('eep_d', 2)]))
    check(label + ' core binding same', [value for value in state['event_targets'] if value['name'].startswith('eep_core')] == [value for value in before['event_targets'] if value['name'].startswith('eep_core')])
    flags = state['planets'][source]['flags']
    check(label + ' source flags match route', ('eep_active' in flags) == (expected == 'situation_eep_devouring'))
    if expected == 'situation_eep_devouring':
        check(label + ' actual fixedQ20T48', state['planets'][source]['variables']['eep_q'] == 20 and state['planets'][source]['variables']['eep_months'] == 48)
end_task = next(value for value in end['situations'].values() if value['type'] == expected)
check('actual first month progress', end_task['progress'] == (8.5 if expected == 'situation_terravore_consume_planet' else 1))
report = {'status': 'PASS' if all(value['passed'] for value in checks) else 'FAIL',
          'scope': 'Controlled two-Mod same-file override; native decision UI and actual first month only. Does not claim native118 completion or full Terravore acceptance.',
          'order': order, 'enabled_mods': manifest['enabled_mods'], 'source_id': source,
          'actual_situation_type': expected, 'actual_first_month_progress': end_task['progress'],
          'start_save_sha256': start['save_sha256'], 'end_save_sha256': end['save_sha256'],
          'checks_passed': sum(value['passed'] for value in checks), 'checks_total': len(checks), 'checks': checks}
h.write_json(run / (prefix + '-route-proof.json'), report)
print(json.dumps({key: value for key, value in report.items() if key != 'checks'}), flush=True)
assert report['status'] == 'PASS', [value for value in checks if not value['passed']]
print(json.dumps(h.stop(30)), flush=True)
