import copy,json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';shutil.copyfile(Path(__file__),run/Path(__file__).name)
b=json.loads((run/'formal-prod-report-before.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/'formal-prod-report-error-before.log').write_bytes(eb)
f=r.gpu_capture('formal-prod-mother-button-confirm');label='\u89d0\u89c1\u5973\u738b\u00b7\u767d\u7eee'
rows=[x for x in f['rows'] if x['text']==label];assert len(rows)==1;box=rows[0]['box'];r.gpu_click(round((box[0][0]+box[2][0])/2),round((box[0][1]+box[2][1])/2),'formal-prod-native-audience-button')
h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);f=r.gpu_capture('formal-prod-native-report-visible');print(json.dumps({'image':f['image'],'labels':[x['text'] for x in f['rows']]},ensure_ascii=True),flush=True)
a=r.native_save('formal-prod-report-pending',b['date'],(0,));c=lambda x:x['countries']['0']
display={'eep_c_remainder','eep_g_remainder','eep_chunks','eep_tasks','eep_waiting','eep_core_state','eep_psi','eep_crisis'}
cv=lambda x:{k:v for k,v in c(x)['variables'].items() if k not in display}
def planets(x):
 y=copy.deepcopy(x['planets'])
 for p in y.values():
  for k in ['eep_actual_pop','eep_free_districts']:p.get('variables',{}).pop(k,None)
 return y
checks={'same_date':a['date']==b['date'],'all_root_stock_same':c(a)['stockpile']==c(b)['stockpile'],'all_pop_groups_same':a['pop_groups']==b['pop_groups'],'all_pop_jobs_same':a['pop_jobs']==b['pop_jobs'],
 'economic_EEP_variables_same':cv(a)==cv(b),'all_EEP_flags_same':c(a)['flags']==c(b)['flags'],'AP_empty_same':c(a)['ascension_perks']==c(b)['ascension_perks']==[],
 'traditions_same':c(a).get('traditions')==c(b).get('traditions'),'technology_same':c(a)['completed_technologies']==c(b)['completed_technologies'],'queues_same':c(a)['research_queues']==c(b)['research_queues'],
 'colonies_same':a['colonies']==b['colonies'],'physical_planets_except_documented_display_snapshot_same':planets(a)==planets(b),'districts_same':a['districts']==b['districts'],'deposits_same':a['deposits']==b['deposits'],'situations_same':a['situations']==b['situations'],
 'report_actual_pop_matches_native':a['planets']['1']['variables']['eep_actual_pop']==a['colonies']['0']['actual_pop_sum']==5300,
 'zero_ledger_and_tasks_display':all(c(a)['variables'].get(k)==0 for k in ['eep_c','eep_g','eep_made','eep_worlds','eep_tasks','eep_waiting','eep_core_state','eep_psi','eep_crisis']),
 'capacity_2_preserved':c(a)['variables']['eep_d']==2,'no_new_errors':(user/'logs/error.log').read_bytes()==eb}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'allowed_display_variables':sorted(display),'planet_display_variables':['eep_actual_pop','eep_free_districts'],'actual_display':c(a)['variables'],'mother_display':a['planets']['1']['variables'],'scope':'Final production actual mother GUI button; first report snapshots are display-only, exact economic state unchanged.'};h.write_json(run/'formal-prod-native-report-readonly-proof.json',v);print(json.dumps(v),flush=True);assert all(checks.values())
