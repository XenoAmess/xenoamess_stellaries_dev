import json, logging, shutil, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q

logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
assert m['role']=='Post-release organic Fanatic Purifier natural continuation'
shutil.copyfile(Path(__file__),run/Path(__file__).name)
for n in range(12):
 try:f=r.gpu_capture('organic-purifier-title-ready-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('organic-purifier-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];h.click_point(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'organic-purifier-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native Chinese main menu')
eb=(user/'logs/error.log').read_bytes();(run/'organic-purifier-load-error-before.log').write_bytes(eb)
b=q.audit(Path(m['original_seed']['path']),(0,));h.write_json(run/'organic-purifier-inherited-source.audit.json',b)
loaded=r.native_load('purifier-start','organic-purifier-original-load');assert loaded['source_sha256']==m['original_seed']['sha256']
a=r.native_save('organic-purifier-loaded','2281.01.11',(0,));c=a['countries']['0'];bc=b['countries']['0'];s=a['species'][str(c['native']['founder_species_ref'])]
checks={'original_bytes_loaded':loaded['source_sha256']==m['original_seed']['sha256'],
 'actual_date':a['date']=='2281.01.11','legal_purifier_origin':'civic_fanatic_purifiers' in c['government'] and q.scalars(c['government']).get('origin')=='origin_heart_of_devouring',
 'organic_founder':s['class']!='LITHOID' and not any(t in s['traits'] for t in ['trait_mechanical','trait_lithoid','trait_machine_unit']),
 'ledger_original':all(c['variables'].get(k)==z for k,z in {'eep_c':16,'eep_g':16,'eep_d':6,'eep_made':200,'eep_worlds':1,'eep_psi':0,'eep_fleet_stage':0}.items()),
 'all_stock_same':c['stockpile']==bc['stockpile'],'actual_population_same':sum(x['actual_pop_sum'] for x in a['colonies'].values())==20685,
 'all_pop_groups_same':a['pop_groups']==b['pop_groups'],'original_AP_only':c['ascension_perks']==['ap_one_vision','ap_consecrated_worlds'],
 'technology_same':c['completed_technologies']==bc['completed_technologies'],'research_queues_same':c['research_queues']==bc['research_queues'],
 'traditions_same':c['traditions']==bc['traditions'],'one_actual_core':sum(d.get('type')=='d_eep_core' for d in a['deposits'].values())==1}
ea=(user/'logs/error.log').read_bytes();(run/'organic-purifier-load-error-after.log').write_bytes(ea)
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'source_sha256':b['save_sha256'],'loaded_sha256':a['save_sha256'],'actual_founder':s,'actual_government':c['government'],'stockpile':c['stockpile'],'new_error_bytes':len(ea)-len(eb),'scope':'Native original-byte legal natural organic Purifier load and formal production compatibility only; no ascension/crisis or full-route claim.'}
h.write_json(run/'organic-purifier-original-load-proof.json',v);print(json.dumps(v,ensure_ascii=False),flush=True);assert all(checks.values())
