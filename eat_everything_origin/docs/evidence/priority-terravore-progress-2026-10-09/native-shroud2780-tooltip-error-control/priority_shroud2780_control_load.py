"""Load original-byte world in empty-mod CN diagnosis; preserve load baseline."""
import json,logging,shutil,sys,time,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
for n in range(15):
 try:f=r.gpu_capture('shroud2780-title-ready-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('shroud2780-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'shroud2780-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN main menu')
(run/'shroud2780-load-error-before.log').write_bytes((user/'logs/error.log').read_bytes())
loaded=r.native_load('shroud2780-source','shroud2780-control-original-load');a=r.native_save('shroud2780-control-loaded','2254.11.02',(0,));(run/'shroud2780-load-error-after.log').write_bytes((user/'logs/error.log').read_bytes())
with zipfile.ZipFile(run/'shroud2780-control-loaded.sav') as z:t=z.read('gamestate').decode('utf-8-sig')
rt={k:v for k,v,o in q.fields(t) if o};src=Path(m['original_seed']['path']);b=json.loads(src.with_suffix('.audit.json').read_text('utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
with zipfile.ZipFile(src) as z:bt=z.read('gamestate').decode('utf-8-sig')
br={k:v for k,v,o in q.fields(bt) if o}
pending=lambda text:[v for k,v,o in q.fields(text) if k=='player_event' and o and q.scalars(v).get('country')==0]
checks={'actual_enabled_mods_empty':json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':[],'disabled_dlcs':[]},'original_alias_SHA':loaded['source_sha256']==m['original_seed']['sha256']=='544e3f225293364c1335d633877f4fbe2622841974d6e2db566a8dd48121b873','same_actual_date':a['date']==b['date']=='2254.11.02','actual_country0_stockpile_held':bc['effective_stockpile']==ac['effective_stockpile'],'all_actual_population_identity_size_held':{i:(p['planet'],p['size'],p['key']) for i,p in b['pop_groups'].items()}=={i:(p['planet'],p['size'],p['key']) for i,p in a['pop_groups'].items()},'unique189_pending_raw_held':pending(bt)==pending(t) and len(pending(t))==1 and q.scalars(pending(t)[0])['id']==189,'native_breach_raw_held':q.block(q.block(br['situations'],'situations'),'16777221')==q.block(q.block(rt['situations'],'situations'),'16777221'),'native_full_psionic_species_held':b['species']==a['species'],'native_government_ruler_founder_held':bc['government']==ac['government'] and all(bc['native'][k]==ac['native'][k] for k in ['ruler','founder_species_ref']),'true_research_held':bc['tech_status']==ac['tech_status'] and bc['research_stockpile']==ac['research_stockpile']}
p={'status':'PASS_NATIVE2780_CONTROL_LOAD_ONLY' if all(checks.values()) else 'FAIL','checks':checks,'after_sha256':a['save_sha256'],'original_seed_sha256':m['original_seed']['sha256'],'load_error_bytes':len((user/'logs/error.log').read_bytes()),'scope':m['scope']};h.write_json(run/'shroud2780-control-loaded-proof.json',p);print(json.dumps(p),flush=True);assert all(checks.values()),'Control load original FAIL retained'
