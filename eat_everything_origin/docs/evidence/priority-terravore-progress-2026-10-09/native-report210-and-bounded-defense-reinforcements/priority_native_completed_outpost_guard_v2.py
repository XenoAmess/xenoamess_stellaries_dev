"""Bind real paid outpost order to completed station ownership chain."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after,system,planet,sbid,shipid,fleetid=sys.argv[1:];system,planet,sbid,shipid,fleetid=map(int,(system,planet,sbid,shipid,fleetid))
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 roots={k:v for k,v,o in q.fields(t) if o};sb={k:v for k,v,o in q.fields(q.block(roots['starbase_mgr'],'starbases')) if o};ships={k:v for k,v,o in q.fields(roots['ships']) if o}
 owned=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(roots['country'],'0'),'fleets_manager'))))
 local={k:v for k,v in sb.items() if q.scalars(ships[str(q.scalars(v)['station'])])['fleet'] in owned}
 return a,roots,sb,ships,owned,local
b,br,bs,bships,bowned,bl=read(before);a,ar,ass,aships,aowned,al=read(after)
wait=json.loads((run/(after+'-paid-wait-v3-proof.json')).read_text('utf-8'));paid=json.loads((run/(before+'-paid-outpost-v2-proof.json')).read_text('utf-8'))
new=ass[str(sbid)];ss=q.scalars(aships[str(shipid)]);f=q.block(ar['fleet'],str(fleetid));oldconstructor=q.block(br['fleet'],'2');constructor=q.block(ar['fleet'],'2');p=q.block(q.block(ar['planets'],'planet'),str(planet));sysraw=q.block(ar['galactic_object'],str(system))
checks={
 'bound_original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'bound_all21_wait_checks_PASS':len(wait['checks'])==21 and all(wait['checks'].values()) and wait['before_sha256']==b['save_sha256'] and wait['after_sha256']==a['save_sha256'],
 'bound_all39_paid_order_checks_PASS':len(paid['checks'])==39 and all(paid['checks'].values()) and paid['after_sha256']==b['save_sha256'],
 'exact_existing_local_starbase_ids_plus_one':set(al)==set(bl)|{str(sbid)} and str(sbid) not in bl,
 'exact_original_all_owned_fleets_plus_new_station':aowned==bowned+[fleetid],
 'system_original_unowned_now_exact_starbase':q.ids(q.block(q.block(br['galactic_object'],str(system)),'starbases'))==[4294967295] and q.ids(q.block(sysraw,'starbases'))==[sbid],
 'new_starbase_outpost_real_station_ship':str(sbid) not in bs and str(shipid) not in bships and q.scalars(new)['level']=='starbase_level_outpost' and q.scalars(new)['station']==shipid,
 'real_station_ship_correct_fleet_date':ss['fleet']==fleetid and b['date']<ss['construction_date']<=a['date'],
 'new_owned_station_fleet_class_exact_ship':fleetid in aowned and q.scalars(f)['ship_class']=='shipclass_starbase' and q.ids(q.block(f,'ships'))==[shipid],
 'station_fleet_real_system_and_star_orbit':q.scalars(q.block(q.block(f,'movement_manager'),'coordinate'))['origin']==system and q.scalars(q.block(q.block(q.block(f,'movement_manager'),'orbit'),'orbitable'))=={'planet':planet},
 'star_controller_and_orbital_defence_chain':q.scalars(p)['controller']==0 and q.scalars(p)['orbital_defence']==fleetid,
 'original_paid_constructor_order_consumed_original_ship_held':bool(q.block(oldconstructor,'current_order')) and not q.block(constructor,'current_order') and q.ids(q.block(oldconstructor,'ships'))==q.ids(q.block(constructor,'ships'))==[2],
 'original_constructor_arrived_correct_system':q.scalars(q.block(q.block(constructor,'movement_manager'),'coordinate'))['origin']==system,
 'target_continental124_still_uncolonized':q.scalars(q.block(q.block(ar['planets'],'planet'),'124')).get('colony') is None and q.scalars(q.block(q.block(ar['planets'],'planet'),'124')).get('planet_class')=='pc_continental',
}
p={'status':'PASS_NATIVE_PAID_OUTPOST_COMPLETION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'local_starbase_ids_before_after':[list(bl),list(al)],'station_native_construction_date':ss['construction_date'],'ownership_chain':{'country':0,'owned_fleet':fleetid,'ship':shipid,'starbase':sbid,'system':system,'star':planet},'scope':'Real original paid outpost completed and owned; no colony, second swallow or full-route claim.'}
out=run/(after+'-completed-outpost-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original completion FAIL retained; no next outpost'
