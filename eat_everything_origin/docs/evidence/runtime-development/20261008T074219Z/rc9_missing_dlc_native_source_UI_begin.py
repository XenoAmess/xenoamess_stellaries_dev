import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();variant=m['dlc_variant'];assert variant in ['nemesis','shroud']
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest);stem='rc9-missing-'+variant+'-native-Q8'
b=json.loads((run/('rc9-missing-'+variant+'-source-native-nextday.audit.json')).read_text(encoding='utf-8'));c=lambda a:a['countries']['0']
def center(row):return [round(sum(p[i] for p in row['box'])/4) for i in [0,1]]
f=r.gpu_capture(stem+'-native-source-row-guard');rows=[x for x in f['rows'] if x['text']=='EEP-DLC-Q8' and min(p[0] for p in x['box'])>800];assert len(rows)==1,rows
r.gpu_click(*center(rows[0]),stem+'-select-source');f=r.gpu_capture(stem+'-selected-source-guard');assert any(x['text']=='EEP-DLC-Q8' and max(p[0] for p in x['box'])<300 for x in f['rows'])
r.gpu_click_text('\u51b3\u8bae',stem+'-decisions-open');h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(.6);f=r.gpu_capture(stem+'-decision-guard')
rows=[x for x in f['rows'] if '\u541e\u566c' in x['text'] and min(p[0] for p in x['box'])>700 and max(p[1] for p in x['box'])<160];assert len(rows)==1,rows
r.gpu_click(*center(rows[0]),stem+'-actual-begin');a=r.native_save(stem+'-begun',b['date'],(0,))
targets=[x for x in a['event_targets'] if x['name']=='eep_missing_dlc_source'];assert len(targets)==1;pid=targets[0]['id'];p=a['planets'][str(pid)];tasks=[s for s in a['situations'].values() if s.get('country')==0 and s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes']
research={'physics_research','society_research','engineering_research'};stockchanges={k:[c(b)['stockpile'].get(k),c(a)['stockpile'].get(k)] for k in set(c(b)['stockpile'])|set(c(a)['stockpile']) if c(b)['stockpile'].get(k)!=c(a)['stockpile'].get(k)}
checks={'one_actual_task':len(tasks)==1,'task_progress_zero':len(tasks)==1 and tasks[0]['progress']==0,'actual_source_target':len(tasks)==1 and tasks[0]['target']['id']==pid,'Q8_T20':p['variables']['eep_q']==8 and p['variables']['eep_months']==20,'source_active':'eep_active' in p['flags'],
 'all_real_population_same':a['pop_groups']==b['pop_groups'],'ledger_same':c(a)['variables']==c(b)['variables'],'AP_empty':c(a)['ascension_perks']==[],'technology_same':c(a)['completed_technologies']==c(b)['completed_technologies'],'queues_same':c(a)['research_queues']==c(b)['research_queues'],'all_nonresearch_stock_same':not(set(stockchanges)-research)}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'full_stock_check':'FAIL' if stockchanges else 'PASS','all_stock_differences':stockchanges,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Actual CN no-fee source decision with native missing DLC; research pool differences preserved without compensation.'};h.write_json(run/(stem+'-begin-proof.json'),v);print(json.dumps(v),flush=True);assert all(checks.values())
