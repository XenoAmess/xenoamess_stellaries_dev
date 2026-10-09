"""Native load of original-byte Mod-derived world with zero enabled mods; baseline only."""
import json,logging,shutil,sys,time,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(Path(__file__),run/Path(__file__).name)
for n in range(12):
 try:f=r.gpu_capture('preftl-title-ready-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('preftl-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'preftl-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN main menu')
(run/'preftl-control-load-error-before.log').write_bytes((user/'logs/error.log').read_bytes())
loaded=r.native_load('preftl-source','preftl-control-original-load');a=r.native_save('preftl-control-loaded','2233.09.01',(0,));(run/'preftl-control-load-error-after.log').write_bytes((user/'logs/error.log').read_bytes())
with zipfile.ZipFile(run/'preftl-control-loaded.sav') as z:t=z.read('gamestate').decode('utf-8-sig')
c=q.block(q.block(t,'country'),'29');cs=q.scalars(c);g=q.block(c,'government');gs=q.scalars(g)
with zipfile.ZipFile(Path(m['original_seed']['path'])) as z:orig=z.read('gamestate').decode('utf-8-sig')
oc=q.block(q.block(orig,'country'),'29')
checks={'actual_enabled_mods_empty':json.loads((user/'dlc_load.json').read_text('utf-8'))['enabled_mods']==[], 'original_world_alias_SHA':loaded['source_sha256']==m['original_seed']['sha256']=='58a0eb48e92ec37286fa4084d8b33a4f98de1de4bcfbf4f5e0bc4eaa4d9e682e','same_actual_date':a['date']=='2233.09.01','country29_primitive_stone_age':cs['type']=='primitive' and cs['preftl_age']=='stone_age' and 'stone_age' in q.scalars(q.block(c,'flags')),'country29_hive_post_apocalyptic':gs['authority']=='auth_hive_mind' and gs['origin']=='origin_post_apocalyptic','country29_government_original_raw_held':g==q.block(oc,'government')}
p={'status':'PASS_PRE_FTL_CONTROL_LOAD_ONLY' if all(checks.values()) else 'FAIL','checks':checks,'after_sha256':a['save_sha256'],'country29_scalars':cs,'country29_government':g,'load_error_bytes':len((user/'logs/error.log').read_bytes()),'scope':'Original-byte Mod-derived world loaded with no enabled mods. Missing EEP definitions are baseline; not clean vanilla-origin world or Mod acceptance.'}
h.write_json(run/'preftl-control-loaded-proof.json',p);print(json.dumps(p),flush=True);assert all(checks.values()),'Control load FAIL retained; no event'
