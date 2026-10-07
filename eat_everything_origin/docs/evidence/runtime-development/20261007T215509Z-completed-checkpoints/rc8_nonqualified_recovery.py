import json
import logging
from pathlib import Path
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
shutil.copyfile(Path(__file__), run / Path(__file__).name)
keys = ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']
panels = json.loads((run / 'rc8-fleet-country-mother-panels-same-day.audit.json').read_text(encoding='utf-8'))
controlled = json.loads((run / 'rc8-nonqualified-player1-confirmed-native.audit.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(run / 'rc8-nonqualified-player1-confirmed-native.sav') as archive:
    native = archive.read('gamestate').decode('utf-8-sig')
assert 'country=1' in q.block(native, 'player')
country1 = q.block(q.block(native, 'country'), '1')
government = q.scalars(q.block(country1, 'government'))
assert government['origin'] == 'origin_default', government
assert not controlled['countries']['1']['flags'] and not controlled['countries']['1']['variables']
for key in keys:
    assert controlled[key] == panels[key], key
h.click_point(865, 232, 'rc8-nonqualified-own-capital-open')
frame = r.gpu_capture('rc8-nonqualified-own-capital-queen-hidden-ui')
assert any('卡尔努' in row['text'] and row['score'] >= .8 for row in frame['rows'])
assert not any('觐见女王' in row['text'] for row in frame['rows'])
after = r.native_save('rc8-nonqualified-own-capital-same-day', '2204.03.01', tuple(map(int, panels['countries'])))
for key in keys:
    assert after[key] == panels[key], key
log = user / 'logs/error.log'
shutil.copyfile(log, run / 'rc8-nonqualified-capital-stage-error.log')
content = log.read_text(encoding='utf-8-sig', errors='replace')
assert 'Wrong scope for trigger' not in content
assert 'Variable eep_old_damage is not set' not in content
proof = {'status':'PASS_SCOPED', 'country':1, 'government':government,
         'origin_path':'country.1.government.origin', 'date':'2204.03.01',
         'all_37_countries_and_9_world_collections_equal':True,
         'own_capital_queen_button_hidden':True, 'stage_error_log_scope_errors':0,
         'image':frame['image'], 'image_sha256':frame['image_sha256'],
         'limitations':['This existing ordinary hive is not the ordinary empire or assimilator creation rejection test.']}
h.write_json(run / 'rc8-nonqualified-own-capital-proof.json', proof)
print(json.dumps(proof, ensure_ascii=True), flush=True)
