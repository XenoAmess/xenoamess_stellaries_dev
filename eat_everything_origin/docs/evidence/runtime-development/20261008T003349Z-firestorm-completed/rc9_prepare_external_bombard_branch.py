"""Independent native-source restoration and formal devouring entry."""
import json
import logging
from pathlib import Path
import shutil
import sys
branch=sys.argv[1]
assert branch == 'bombard'
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,m=h.load_run()
cp=run/Path(__file__).name
if not cp.exists():shutil.copyfile(Path(__file__),cp)
assert cp.read_bytes()==Path(__file__).read_bytes()
base='rc9-focus-developed-source69-before-begin'
b=json.loads((run/(base+'.audit.json')).read_text(encoding='utf-8'))
assert b['save_sha256']=='da3c94846bb666daa5bd7dfd13a683ce0decf6ab3617c2e5cbbc704bf0838547'
assert b['colonies']['24']['actual_pop_sum']==69
alias=user/'save games/acceptance-fixtures/focus-finished69.sav'
if not alias.exists():shutil.copyfile(run/(base+'.sav'),alias)
assert h.sha256(alias)==b['save_sha256']
receipt_path=run/'rc9-focus-finished69-original-byte-alias.json'
if not receipt_path.exists():h.write_json(receipt_path,{'source':str(run/(base+'.sav')),'alias':str(alias),'sha256':h.sha256(alias),'bytes':alias.stat().st_size,'date':b['date']})
prefix='rc9-external-'+branch
receipt=r.native_load('focus-finished69',prefix+'-original-load')
assert receipt['source_sha256']==b['save_sha256']
h.press_scan_code(0x29,prefix+'-formal-begin-console-open',1)
h.type_text('effect root = { event_target:eep_native_purge_source = { set_name = "EEP-'+branch.upper()+'-16" eep_begin = yes } }',True,prefix+'-formal-begin-entry')
r.gpu_capture(prefix+'-formal-begin-native-receipt')
h.press_scan_code(0x29,prefix+'-formal-begin-console-close',1)
a=r.native_save(prefix+'-task-ready',b['date'],(0,))
c=a['countries']['0'];s=a['planets']['84'];tasks=[v for v in a['situations'].values() if v.get('type')=='situation_eep_devouring']
checks={
 'actual_focus_origin_and_civic':'origin_heart_of_devouring' in c['government'] and 'civic_hive_scorched_earth' in c['government'],
 'same_original_stockpiles':c['stockpile']==b['countries']['0']['stockpile'],
 'no_reward':all(c['variables'].get(k)==b['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']),
 'mother_paid31_seed':a['colonies']['0']['actual_pop_sum']==7721,
 'source_actual100':a['colonies']['24']['actual_pop_sum']==100,
 'all_owned_population_conserved':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in c['owned_colonies'])==7821,
 'exact_q16_t39':s['variables'].get('eep_q')==16 and s['variables'].get('eep_months')==39,
 'actual_source_active':'eep_active' in s['flags'],
 'task0_for_source84':len(tasks)==1 and tasks[0].get('progress')==0 and tasks[0].get('target',{}).get('id')==84 and tasks[0].get('country')==0,
 'original_core_binding':next(v for v in a['event_targets'] if v['name']=='eep_core0')['id']==1,
 'no_first_notice':'eep_first_notice' not in c['flags'],
}
h.write_json(run/(prefix+'-task-preconditions.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'save_sha256':a['save_sha256'],'source_original_sha256':b['save_sha256'],'date':a['date'],'scope':'Independent original-byte reload and real formal100 seed transfer; controlled external destruction not yet executed.'})
print(json.dumps({'branch':branch,'checks':checks,'save_sha256':a['save_sha256']}),flush=True)
assert all(checks.values())
