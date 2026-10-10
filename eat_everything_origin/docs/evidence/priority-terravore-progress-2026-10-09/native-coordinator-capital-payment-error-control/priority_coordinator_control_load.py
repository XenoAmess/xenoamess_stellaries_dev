"""Load original-byte world in empty-mod CN diagnosis; preserve load baseline."""
import json,logging,shutil,sys,time,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
for n in range(15):
 try:f=r.gpu_capture('coordinator-title-ready-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('coordinator-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'coordinator-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN main menu')
(run/'coordinator-load-error-before.log').write_bytes((user/'logs/error.log').read_bytes())
loaded=r.native_load('coordinator-source','coordinator-control-original-load');a=r.native_save('coordinator-control-loaded','2238.10.02',(0,));(run/'coordinator-load-error-after.log').write_bytes((user/'logs/error.log').read_bytes())
with zipfile.ZipFile(run/'coordinator-control-loaded.sav') as z:t=z.read('gamestate').decode('utf-8-sig')
rt={k:v for k,v,o in q.fields(t) if o};src=Path(m['original_seed']['path']);b=json.loads(src.with_suffix('.audit.json').read_text('utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
checks={'actual_enabled_mods_empty':json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':[],'disabled_dlcs':[]},'original_alias_SHA':loaded['source_sha256']==m['original_seed']['sha256']=='4371182e222afb2b0ad278c0b1e06f8b767ac28049ad39d1edccf6f6e10b6214','same_actual_date':a['date']==b['date']=='2238.10.02','actual_country0_stockpile_held':bc['effective_stockpile']==ac['effective_stockpile'],'actual_all_population_identity_and_size_held':{i:(p['planet'],p['size'],p['key']) for i,p in b['pop_groups'].items()}=={i:(p['planet'],p['size'],p['key']) for i,p in a['pop_groups'].items()},'actual_paid_districts_held':a['districts']==b['districts'],'original_native_capital_and_zone_relation':q.scalars(q.block(rt['buildings'],'0'))=={'type':'building_hive_capital','position':0} and 0 in q.ids(q.block(q.block(rt['zones'],'0'),'buildings')),'capital_upgrade_tech_present':all(v in ac['completed_technologies'] for v in ['tech_colonial_centralization','tech_hive_node'])}
p={'status':'PASS_COORDINATOR_CONTROL_LOAD_ONLY' if all(checks.values()) else 'FAIL','checks':checks,'after_sha256':a['save_sha256'],'load_error_bytes':len((user/'logs/error.log').read_bytes()),'scope':m['scope']};h.write_json(run/'coordinator-control-loaded-proof.json',p);print(json.dumps(p),flush=True);assert all(checks.values()),'Control load FAIL retained'
