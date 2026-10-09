"""Chinese native load and native fleet/leader eligibility in empty-mod branch."""
import json,logging,shutil,sys,time,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
for n in range(15):
 try:f=r.gpu_capture('leader13-title-ready-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('leader13-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'leader13-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN main menu')
(run/'leader13-load-error-before.log').write_bytes((user/'logs/error.log').read_bytes())
loaded=r.native_load('leader13-source','leader13-control-original-load');a=r.native_save('leader13-control-loaded','2237.08.02',(0,));(run/'leader13-load-error-after.log').write_bytes((user/'logs/error.log').read_bytes())
def read(p):
 with zipfile.ZipFile(p) as z:t=z.read('gamestate').decode('utf-8-sig')
 return {k:v for k,v,o in q.fields(t) if o}
rt=read(run/'leader13-control-loaded.sav');orig=read(Path(m['original_seed']['path']));leader=q.block(rt['leaders'],'50331733');ship=q.block(rt['ships'],'1527');fleet=q.block(rt['fleet'],'565');country=q.block(rt['country'],'16777218');ls=q.scalars(leader);fs=q.scalars(fleet);traits=[v.strip('"') for k,v,o in q.fields(leader) if k=='traits'];loc=q.scalars(q.block(leader,'location'));coord=q.scalars(q.block(q.block(fleet,'movement_manager'),'coordinate'))
checks={'actual_enabled_mods_empty':json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':[],'disabled_dlcs':[]},'original_alias_SHA':loaded['source_sha256']==m['original_seed']['sha256']=='d2daf0d4bc7cfd690abb5c573f657a7bd97121d4babaf7b703d3beeef7d69c6f','same_actual_date':a['date']=='2237.08.02','target_commander_default_owner':ls['class']=='commander' and ls['country']==16777218 and q.scalars(country)['type']=='default','exact_two_eligible_native_traits':traits==['leader_trait_cautious','leader_trait_adaptable'],'native_ship_leader_fleet_relations':loc['type']=='ship' and loc['id']==1527 and q.scalars(ship)['leader']==50331733 and q.scalars(ship)['fleet']==565 and 1527 in q.ids(q.block(fleet,'ships')),'not_missing_in_action_valid_system45':not fs.get('return_date') and coord['origin']==45,'native_target_traits_and_government_held':traits==[v.strip('"') for k,v,o in q.fields(q.block(orig['leaders'],'50331733')) if k=='traits'] and q.block(country,'government')==q.block(q.block(orig['country'],'16777218'),'government')}
p={'status':'PASS_LEADER13_CONTROL_LOAD_ONLY' if all(checks.values()) else 'FAIL','checks':checks,'after_sha256':a['save_sha256'],'leader_raw':leader,'fleet_raw':fleet,'load_error_bytes':len((user/'logs/error.log').read_bytes()),'scope':m['scope']};h.write_json(run/'leader13-control-loaded-proof.json',p);print(json.dumps(p),flush=True);assert all(checks.values()),'Control load FAIL retained'
