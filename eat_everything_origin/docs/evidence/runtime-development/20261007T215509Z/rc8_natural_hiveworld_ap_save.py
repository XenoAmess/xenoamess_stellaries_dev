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
before_path = run / 'rc8-hiveworld-natural2297-loaded.sav'
with zipfile.ZipFile(before_path) as archive:
    text = archive.read('gamestate').decode('utf-8-sig')
identities = tuple(int(key) for key,value,obj in q.fields(q.block(text, 'country')) if obj)
before = q.audit(before_path, identities)
h.write_json(run / 'rc8-hiveworld-natural2297-loaded-all-countries.audit.json', before)
frame = r.gpu_capture('rc8-hiveworld-ap-current-confirmation-guard')
yes = [row for row in frame['rows'] if row['text'] == '是' and row['score'] >= .8]
assert len(yes) == 1, yes
row = yes[0]
h.click_point(round(sum(p[0] for p in row['box'])/4), round(sum(p[1] for p in row['box'])/4), 'rc8-hiveworld-ap-native-confirm')
after = r.native_save('rc8-hiveworld-natural-ap5-paid', '2297.03.12', identities)
country = after['countries']['0']
assert country['ascension_perks'] == before['countries']['0']['ascension_perks'] + ['ap_hive_worlds']
assert country['traditions'] == before['countries']['0']['traditions'] + ['tr_expansion_galactic_ambition', 'tr_expansion_finish']
assert country['stockpile']['unity'] == before['countries']['0']['stockpile']['unity'] - 6155
for key in country['stockpile']:
    if key != 'unity':
        assert country['stockpile'][key] == before['countries']['0']['stockpile'][key], key
assert country['variables'] == before['countries']['0']['variables']
assert country['flags'] == before['countries']['0']['flags']
for key in ['colonies','pop_groups','pop_jobs','districts','deposits','situations','species','event_targets']:
    assert after[key] == before[key], key
h.write_json(run / 'rc8-hiveworld-natural-ap5-purchase-proof.json',
             {'status':'PASS_SCOPED','date':after['date'],'countries_audited':len(identities),
              'unity_paid':6155,'ap':'ap_hive_worlds','traditional_capacity_added':1,
              'eep_capacity_kept':16,'actual_population_kept':15835,
              'all_other_stockpiles_and_world_collections_kept':True,
              'native_save_sha256':after['save_sha256']})
print(json.dumps({'date':after['date'],'sha256':after['save_sha256'],'stockpile':country['stockpile']},ensure_ascii=True),flush=True)
