"""Original-byte waiting reload and blocked settlement replay; no purge bypass."""
import json
import logging
from pathlib import Path
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
stem = 'rc9-focus-wait-purge-real-endpoint39'
before = json.loads((run / (stem + '.audit.json')).read_text(encoding='utf-8'))
original = run / (stem + '.sav')
alias = user / 'save games' / 'acceptance-fixtures' / 'purge-wait39.sav'
assert not alias.exists()
shutil.copyfile(original, alias)
assert h.sha256(alias) == before['save_sha256']
h.write_json(run / 'rc9-focus-wait39-original-byte-alias.json', {'source':str(original),'alias':str(alias),'sha256':h.sha256(alias),'bytes':alias.stat().st_size,'date':before['date']})
r.native_load('purge-wait39', 'rc9-focus-wait39-original-load')
restored = r.native_save('rc9-focus-wait39-original-reloaded', before['date'], (0,))
keys = ['eep_c','eep_g','eep_d','eep_made','eep_worlds']
def groups(a):
    return {k:{f:v.get(f) for f in ['planet','size','key']} for k,v in a['pop_groups'].items()}
def checks(a,b):
    c,d = a['countries']['0'], b['countries']['0']
    return {
        'same_actual_date':a['date']==b['date'],
        'same_stockpiles':c['stockpile']==d['stockpile'],
        'same_ledger':{k:c['variables'].get(k) for k in keys}=={k:d['variables'].get(k) for k in keys},
        'all_actual_population_groups':groups(a)==groups(b),
        'same_task':a['situations']==b['situations'],
        'same_targets':a['event_targets']==b['event_targets'],
        'same_source_variables':a['planets']['84']['variables']==b['planets']['84']['variables'],
        'active_pending':{'eep_active','eep_pending'}<=set(a['planets']['84']['flags']),
        'foreign1150_still_purged':sum(v['size'] for v in a['pop_groups'].values() if v.get('planet')==24 and v.get('key',{}).get('species')==39 and v['key'].get('category')=='purge')==1150,
        'scorched_hive':'civic_hive_scorched_earth' in c['government'],
    }
proof = checks(restored,before)
h.write_json(run / 'rc9-focus-wait39-reload-proof.json', {'status':'PASS_SCOPED' if all(proof.values()) else 'FAIL','checks':proof,'original_sha256':before['save_sha256'],'reloaded_sha256':restored['save_sha256'],'scope':'Authoritative waiting state only; native display/cache differences not claimed identical.'})
print(json.dumps({'phase':'reload','checks':proof}),flush=True)
assert all(proof.values())
error = user / 'logs' / 'error.log'
before_log = error.read_bytes()
shutil.copyfile(error, run / 'rc9-focus-wait39-replay-error-before.log')
h.press_scan_code(0x29,'rc9-focus-wait39-replay-console-open',1)
for n in range(5):
    h.type_text('effect root = { every_situation = { limit = { is_situation_type = situation_eep_devouring } situation_event = { id = eep.21 } } country_event = { id = eep.2 } }',True,'rc9-focus-wait39-replay-'+str(n))
r.gpu_capture('rc9-focus-wait39-replay-console-receipt')
h.press_scan_code(0x29,'rc9-focus-wait39-replay-console-close',1)
after = r.native_save('rc9-focus-wait39-five-blocked-replays',before['date'],(0,))
proof = checks(after,restored)
after_log = error.read_bytes()
shutil.copyfile(error,run / 'rc9-focus-wait39-replay-error-after.log')
proof['error_log_no_new_bytes'] = after_log == before_log
flag_changes = {k:{'before':restored['planets']['84']['flags'].get(k),'after':after['planets']['84']['flags'].get(k)} for k in set(restored['planets']['84']['flags'])|set(after['planets']['84']['flags']) if restored['planets']['84']['flags'].get(k)!=after['planets']['84']['flags'].get(k)}
h.write_json(run / 'rc9-focus-wait39-replay-proof.json', {'status':'PASS_SCOPED' if all(proof.values()) else 'FAIL','checks':proof,'before_sha256':restored['save_sha256'],'after_sha256':after['save_sha256'],'source_flag_changes':flag_changes,'settlement_checks':5,'monthly_callbacks':5,'error_delta_bytes':len(after_log)-len(before_log),'scope':'Blocked reward and same-day state only; pending flag timestamp changes explicitly listed.'})
print(json.dumps({'phase':'five_replays','checks':proof,'source_flag_changes':flag_changes}),flush=True)
assert all(proof.values())
