import json,logging,shutil,subprocess,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(Path(__file__),run/Path(__file__).name)
points=[97,108,109,116,117,118,119];previous=96;start='postvanilla-q20-m096';records=[]
for month in points:
 absolute=2200*12+month;year,offset=divmod(absolute,12);end=f'{year:04}.{offset+1:02}.02';stage=f'postvanilla-q20-m{month:03}'
 print(json.dumps({'phase':'NATIVE_CALENDAR_START','effective_month':month,'date':end}),flush=True)
 result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/postrelease_vanilla_native_calendar_v2.py',start,end,stage,str((month-previous)*30)])
 if result.returncode:
  h.write_json(run/'postvanilla-boundary-driver-v2-result.json',{'status':'FAILED_STAGE','month':month,'completed':records,'exit_code':result.returncode});raise RuntimeError('Native calendar stage failed')
 a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'));observed=json.loads((run/(stage+'-state.json')).read_text(encoding='utf-8'));c=a['countries']['0'];from postrelease_vanilla_raw_source import inspect;p=inspect(run/(stage+'.sav'))['source'];tasks=[s for s in a['situations'].values() if s.get('country')==0 and s.get('type')=='situation_terravore_consume_planet' and s.get('killed')!='yes']
 checks={'actual_date':a['date']==end,'no_EEP_variables':not any(k.startswith('eep_') for k in c['variables']),'no_EEP_flags':not any(k.startswith('eep_') for k in c['flags']),'no_EEP_core_deposit':not any(d.get('type')=='d_eep_core' for d in a['deposits'].values()),'AP_empty':c['ascension_perks']==[],'new_error_zero':observed['new_error_bytes']==0}
 if month<118:checks.update({'original_source_owned':p.get('owner')==0,'source_not_destroyed':p['planet_class']=='pc_continental','one_native_task':len(tasks)==1,'fixed_Q20':p['variables'].get('num_districts_terravore')==20,'actual_progress_observed':len(tasks)==1 and tasks[0]['progress']==month*8.5})
 else:checks.update({'native_end_shattered':p['planet_class']=='pc_shattered','source_actual_population_zero':observed['source_population']==0,'no_live_terravore_task':len(tasks)==0})
 receipt={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','effective_month':month,'date':end,'checks':checks,'save_sha256':a['save_sha256'],'actual_state_file':stage+'-state.json','scope':'Native no-mod calendar and genuine endpoint only; natural random awards are observed, never manufactured.'};h.write_json(run/(stage+'-calendar-scope-proof.json'),receipt);records.append(receipt)
 h.write_json(run/'postvanilla-boundary-driver-v2-result.json',{'status':'IN_PROGRESS' if all(checks.values()) else 'FAIL','completed':records});print(json.dumps(receipt),flush=True);assert all(checks.values()),'Native checkpoint unexpected; original state retained'
 previous=month;start=stage
h.write_json(run/'postvanilla-boundary-driver-v2-result.json',{'status':'CALENDAR_SCOPED_PASS','completed':records,'scope':'No-mod native calendar checkpoints only; final message/reload/random-yield analysis still required.'});print('NATIVE_CALENDAR_CHECKPOINTS_FINISHED',flush=True)
