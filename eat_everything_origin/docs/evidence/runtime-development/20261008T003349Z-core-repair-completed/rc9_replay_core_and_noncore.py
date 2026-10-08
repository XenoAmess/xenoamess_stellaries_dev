import hashlib
import json
import logging
from pathlib import Path
import re
import shutil
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
copy = run / Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__), copy)
start_name = 'rc9-hiveworld-paid-natural-complete'
start = json.loads((run / (start_name + '.audit.json')).read_text(encoding='utf-8'))
assert start['date'] == '2319.03.12'
error_path = user / 'logs/error.log'
error_before = error_path.read_bytes()
(run / 'rc9-replay-error-before.log').write_bytes(error_before)
h.press_scan_code(0x29, 'rc9-replay-console-open', 1)
event = 'carrier_event = { id = eep.4 } '
monthly = 'country_event = { id = eep.2 } '
h.type_text('effect event_target:eep_core@this = { ' + event * 5 + '} ' + monthly * 5,
            True, 'rc9-five-completion-and-monthly-replays')
h.type_text('effect every_country = { limit = { NOT = { has_origin = origin_heart_of_devouring } exists = capital_scope } capital_scope = { planet = { eep_repair_core_deposit = yes carrier_event = { id = eep.4 } } } }',
            True, 'rc9-noncore-foreign-native-capital-requests')
r.gpu_capture('rc9-replay-and-noncore-console-receipts')
h.press_scan_code(0x29, 'rc9-replay-console-close', 1)
after = r.native_save('rc9-core-five-replays-noncore-negative', '2319.03.12', (0,))
error_after = error_path.read_bytes()
(run / 'rc9-replay-error-after.log').write_bytes(error_after)
assert error_after.startswith(error_before), 'Native log was reset; cannot claim an append-only delta.'
delta = error_after[len(error_before):]
(run / 'rc9-replay-error-delta.log').write_bytes(delta)

def raw_snapshot(path):
    with zipfile.ZipFile(path) as z:
        text = z.read('gamestate').decode('utf-8-sig')
    roots = {k:v for k,v,b in q.fields(text) if b and k in ('country','pop_groups','planets')}
    stocks = {}
    for identity, value, obj in q.fields(roots['country']):
        if obj:
            stocks[identity] = q.scalars(q.block(q.block(q.block(value, 'modules'), 'standard_economy_module'), 'resources'))
    groups = {}
    for identity, value, obj in q.fields(roots['pop_groups']):
        if obj:
            scalar = q.scalars(value)
            groups[identity] = {'size':scalar.get('size'), 'planet':scalar.get('planet'), 'key':q.scalars(q.block(value, 'key'))}
    deposits = {}
    for identity, value, obj in q.fields(q.block(roots['planets'], 'planet')):
        if obj:
            deposits[identity] = q.ids(q.block(value, 'deposits'))
    return stocks, groups, deposits

before_raw = raw_snapshot(run / (start_name + '.sav'))
after_raw = raw_snapshot(run / 'rc9-core-five-replays-noncore-negative.sav')
before_c, after_c = start['countries']['0'], after['countries']['0']
planet = after['planets']['1']
modifiers = [q.scalars(m.group(1)) for m in re.finditer(r'\{([^{}]*)\}', q.block(planet['modifiers'], 'items'))]
checks = {
    'all_country_stockpiles_equal': before_raw[0] == after_raw[0],
    'all_population_group_sizes_keys_equal': before_raw[1] == after_raw[1],
    'all_physical_deposit_ids_equal': before_raw[2] == after_raw[2],
    'all_eep_targets_equal': start['event_targets'] == after['event_targets'],
    'all_eep_country_variables_equal': before_c['variables'] == after_c['variables'],
    'all_eep_country_flags_equal': before_c['flags'] == after_c['flags'],
    'original_physical_core_colony_owner': planet.get('colony') == 0 and planet.get('owner') == 0,
    'one_core_deposit': sum(after['deposits'][str(i)]['type'] == 'd_eep_core' for i in planet['deposits']) == 1,
    'one_court': sum(m.get('modifier') == 'eep_court' for m in modifiers) == 1,
    'one_capacity16': sum(m.get('modifier') == 'eep_capacity' and m.get('multiplier') == 16 for m in modifiers) == 1,
    'no_new_native_error': not delta,
}
result = {
    'status': 'PASS_SCOPED' if all(checks.values()) else 'FAIL',
    'scope':'Five direct native completion and monthly replays plus foreign noncore capital requests. No time advancement. No claim of whole-object cache identity.',
    'date': after['date'], 'save_sha256': after['save_sha256'],
    'before_save_sha256': start['save_sha256'], 'checks': checks,
    'countries_checked':len(before_raw[0]),'population_groups_checked':len(before_raw[1]),
    'physical_planets_checked':len(before_raw[2]),'error_before_sha256':hashlib.sha256(error_before).hexdigest(),
    'error_after_sha256':hashlib.sha256(error_after).hexdigest(), 'error_delta_bytes':len(delta),
    'modifiers':modifiers,
}
h.write_json(run / 'rc9-core-replay-and-noncore-proof.json', result)
print(json.dumps(result, ensure_ascii=True), flush=True)
assert all(checks.values()), 'At least one replay/negative acceptance check failed.'
