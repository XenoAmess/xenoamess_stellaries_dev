import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path(__file__).parent
manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
user = Path(manifest['userdir'])
checks = []

def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})

def load(name):
    path = run / (name + '.sav')
    audit = json.loads((run / (name + '.audit.json')).read_text(encoding='utf-8'))
    with zipfile.ZipFile(path) as archive:
        meta = archive.read('meta').decode('utf-8-sig')
        raw = archive.read('gamestate').decode('utf-8-sig')
    identities = [int(key) for key, value, obj in q.fields(q.block(raw, 'country')) if obj]
    full = q.audit(path, identities)
    (run / (name + '.all-countries.audit.json')).write_text(json.dumps(full, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    check(name + ' native-save hash', hashlib.sha256(path.read_bytes()).hexdigest() == audit['save_sha256'])
    check(name + ' no loaded mods in native meta', q.block(meta, 'mods').strip() == '')
    check(name + ' no EEP script state anywhere', 'origin_heart_of_devouring' not in raw and '\neep_' not in raw and 'eep_core' not in raw and 'situation_eep_devouring' not in raw)
    check(name + ' every country has no EEP variables or flags', all(not value['variables'] and not value['flags'] for value in full['countries'].values()))
    check(name + ' no EEP event target', full['event_targets'] == [])
    return audit, full

initial, initial_full = load('vanilla-shared-world-native-initial')
frozen, frozen_full = load('vanilla-shared-world-frozen50-unstarted')
restored, restored_full = load('vanilla-shared-world-frozen-restored-retry')
end, end_full = load('vanilla-shared-world-native-year-retry-complete')
check('actual enabled_mods empty', json.loads((user / 'dlc_load.json').read_text(encoding='utf-8-sig'))['enabled_mods'] == [])
check('manifest role true vanilla', manifest['role'] == 'vanilla Chinese environment control')
check('normal stop', json.loads((run / 'stop.json').read_text(encoding='utf-8'))['forced'] is False)
check('initial ordinary origin and Lithoid Hive', 'origin="origin_default"' in initial['countries']['0']['government'] and 'trait_lithoid' in initial['species'][str(initial['countries']['0']['native']['founder_species_ref'])]['traits'])
check('same 38-or-actual countries preserved', initial_full['countries'].keys() == frozen_full['countries'].keys() == restored_full['countries'].keys())
check('initial mother size20', initial['planets']['3']['planet_size'] == 20)
check('initial mother5700', initial['countries']['0']['native']['num_sapient_pops'] == 5700)
sources = {key: value for key, value in frozen['planets'].items() if 'perf_constructed' in value['flags']}
check('frozen exactly50 sources', len(sources) == 50)
for key, value in sources.items():
    groups = [frozen['pop_groups'][str(identity)] for identity in frozen['colonies'][str(value['colony'])]['pop_groups']]
    check('source' + key + ' valid Q20 and actual100 founder', value['planet_class'] == 'pc_continental' and value['planet_size'] == 20 and value['owner'] == 0 and sum(group['size'] for group in groups) == 100 and all(group['key']['species'] == frozen['countries']['0']['native']['founder_species_ref'] for group in groups))
mother_groups = [frozen['pop_groups'][str(identity)] for identity in frozen['colonies']['0']['pop_groups']]
check('actual mother700 and total5700', sum(group['size'] for group in mother_groups) == 700 and sum(group['size'] for group in frozen['pop_groups'].values()) == 5700)
check('prepare no stockpile creation', initial['countries']['0']['stockpile'] == frozen['countries']['0']['stockpile'])
check('frozen has no situation', frozen['situations'] == {})
load_receipt = json.loads((run / 'vanilla-native-retry-restore.load.json').read_text(encoding='utf-8'))
check('retry restored exact frozen bytes', load_receipt['source_sha256'] == frozen['save_sha256'])
check('restored date and all actual population preserved', restored['date'] == '2200.01.01' and sum(group['size'] for group in restored['pop_groups'].values()) == 5700)
check('restored source assets preserved', {key: (value['planet_size'], value['planet_class'], value['owner'], value['colony']) for key, value in restored['planets'].items()} == {key: (value['planet_size'], value['planet_class'], value['owner'], value['colony']) for key, value in frozen['planets'].items()})
check('restored stockpile preserved', restored['countries']['0']['stockpile'] == frozen['countries']['0']['stockpile'])
measurement = json.loads((run / 'vanilla-shared-world-native-year-retry-measurement.json').read_text(encoding='utf-8'))
check('measurement starts at restored actual state', measurement['baseline_save_sha256'] == restored['save_sha256'])
check('measured360days actual endpoint', measurement['status'] == 'MEASURED_NATIVE_DATE_VERIFIED' and measurement['start_date'] == '2200.01.01' and end['date'] == measurement['end_date'] == '2201.01.01' and measurement['end_save_sha256'] == end['save_sha256'])
check('positive measured wall and cpu', measurement['samples'][-1]['elapsed_wall_seconds'] > 0 and measurement['samples'][-1]['cpu_user_seconds'] > 0 and measurement['samples'][-1]['completed'] is True)
check('only native deficit situations at endpoint', all(value['type'] in ('situation_energy_deficit', 'situation_mineral_deficit') for value in end['situations'].values()))
check('first invalid attempt retained', (run / 'measure_native_year_first_attempt.py').exists() and (run / 'vanilla-shared-world-native-year-first-attempt-invalid.json').exists())
report = {'status': 'PASS' if all(value['passed'] for value in checks) else 'FAIL',
          'scope': 'True no-Mod shared-world preparation and one360-day measurement only; not full performance or Mod acceptance.',
          'checks': checks, 'checks_passed': sum(value['passed'] for value in checks), 'checks_total': len(checks),
          'countries': len(frozen_full['countries']), 'baseline_original_save_sha256': frozen['save_sha256'],
          'restored_save_sha256': restored['save_sha256'], 'endpoint_save_sha256': end['save_sha256'],
          'measurement': measurement['samples'][-1], 'mod_comparison': 'PENDING', 'scorched_hive_acceptance': 'NOT_COMPLETE',
          'limitations': ['One sample; includes physical Enter and fresh GPU/OCR polling overhead, excludes native saving.',
                          'Controlled50 colony construction/population transfer, not a natural economy result.',
                          'Native loading recalculated empire_size55 to1081 while actual population, source assets and stockpile stayed fixed.',
                          'Native energy/mineral deficit and subsequent growth are retained, without resource grants.',
                          'First completion-text case-matching error retained and excluded from comparison.']}
(run / 'true-vanilla-shared-world-baseline-proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in report.items() if key not in ('checks', 'limitations')}, ensure_ascii=False))
assert report['status'] == 'PASS', [value for value in checks if not value['passed']]
