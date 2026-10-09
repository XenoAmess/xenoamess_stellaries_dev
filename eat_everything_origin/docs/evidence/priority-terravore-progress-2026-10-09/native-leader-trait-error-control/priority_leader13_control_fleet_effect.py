"""One native fleet-scoped event; isolated no-mod diagnostic, no date advance."""
import json,logging,shutil,sys,zipfile,re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
old=json.loads((run/'leader13-control-error-reproduction-proof.json').read_text('utf-8'));assert old['status']=='FAIL' and len(old['checks'])==14 and [k for k,v in old['checks'].items() if not v]==['exact144_error_increment_each','entire_error_body_same_after_timestamp_normalization','exact_one_native_trait_error_no_extra'] and json.loads((run/'leader13-control-error-guard-execution.json').read_text('utf-8'))['returncode']==1
before='leader13-control-event';stage='leader13-control-fleet-effect';b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));assert h.sha256(run/(before+'.sav'))==b['save_sha256']==old['after_sha256']
with zipfile.ZipFile(run/(before+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
rt={k:v for k,v,o in q.fields(t) if o};ls={k:v for k,v,o in q.fields(rt['leaders']) if o};ships={k:v for k,v,o in q.fields(rt['ships']) if o};fleets={k:v for k,v,o in q.fields(rt['fleet']) if o};matches=[]
for cid,c,o in q.fields(rt['country']):
 if not o:continue
 for fid in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(c,'fleets_manager'),'owned_fleets')):
  for sid in q.ids(q.block(fleets[fid],'ships')):
   lid=str(q.scalars(ships[str(sid)]).get('leader'));l=ls.get(lid,'');traits=[v.strip('"') for k,v,o in q.fields(l) if k=='traits']
   if {'leader_trait_cautious','leader_trait_adaptable'}<=set(traits):matches.append([int(cid),int(fid),sid,int(lid)])
assert matches==[[16777218,565,1527,50331733]],matches
assert all(h.sha256(Path(s['path']))==s['sha256'] for s in old['native_sources'])
command='effect every_country = { every_owned_fleet = { limit = { exists = leader leader = { has_trait = leader_trait_cautious has_trait = leader_trait_adaptable } } fleet_event = { id = leader.13 } } }'
eb=(user/'logs/error.log').read_bytes();assert eb==(run/(before+'-error-after.log')).read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
h.write_json(run/(stage+'-preflight.json'),{'status':'PASS_ONE_UNIQUE_NATIVE_FLEET_TARGET_ONLY','matches':matches,'before_sha256':b['save_sha256'],'original_invalid_scope_proof':old['status'],'command':command})
h.press_scan_code(0x29,stage+'-console-open',1);h.type_text(command,True,stage+'-one-native-effect');f=r.gpu_capture(stage+'-command-receipt');h.press_scan_code(0x29,stage+'-console-close',1)
a=r.native_save(stage,b['date'],(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
p={'status':'OBSERVED_CONTROLLED_NATIVE_FLEET_SCOPED_EFFECT_ONLY','command':command,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_date':a['date'],'receipt_image_sha256':f['image_sha256'],'new_error_bytes':len(ea)-len(eb),'scope':'Exactly one native fleet event via unique actual commander trait selection in empty-mod control. No date advance, production mutation or acceptance claim.'};h.write_json(run/(stage+'-observation.json'),p);print(json.dumps(p),flush=True)
