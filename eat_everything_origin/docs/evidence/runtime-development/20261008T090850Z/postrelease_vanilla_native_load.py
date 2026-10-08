import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(Path(__file__),run/Path(__file__).name)
for n in range(12):
 try:f=r.gpu_capture('postvanilla-title-ready-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('postvanilla-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'postvanilla-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN main menu')
loaded=r.native_load('vanilla-start','postvanilla-original-initial-load');assert loaded['source_sha256']==m['original_seed']['sha256'];a=r.native_save('postvanilla-initial','2200.01.01',(0,));c=a['countries']['0'];s=a['species'][str(c['native']['founder_species_ref'])]
checks={'native_default_origin':q.scalars(c['government']).get('origin')=='origin_default','native_hive_and_swarm':q.scalars(c['government']).get('authority')=='auth_hive_mind' and 'civic_hive_devouring_swarm' in c['government'],'lithoid_class_and_trait':s['class']=='LITHOID' and 'trait_lithoid' in s['traits'],
 'initial_population5700':a['colonies']['0']['actual_pop_sum']==5700,'single_initial_mother':c['owned_colonies']==[0],'no_EEP_variables':not any(k.startswith('eep_') for k in c['variables']),'no_EEP_flags':not any(k.startswith('eep_') for k in c['flags']),'no_EEP_deposit':not any(x.get('type')=='d_eep_core' for x in a['deposits'].values()),'no_EEP_situation':not a['situations'],'actual_enabled_mods_empty':json.loads((user/'dlc_load.json').read_text(encoding='utf-8'))['enabled_mods']==[]}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'source_sha256':loaded['source_sha256'],'native_initial_sha256':a['save_sha256'],'government':c['government'],'founder':s,'scope':'Actual native no-mod original-byte initial load and native save; not new random world or a Mod acceptance claim.'};h.write_json(run/'postvanilla-original-initial-proof.json',v);print(json.dumps(v),flush=True);assert all(checks.values())
