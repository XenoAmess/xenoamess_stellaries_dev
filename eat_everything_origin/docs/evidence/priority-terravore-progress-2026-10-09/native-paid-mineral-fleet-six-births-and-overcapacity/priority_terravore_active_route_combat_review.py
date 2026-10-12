"""Permit one bounded native battle continuation; does not claim victory."""
import json,logging,re,sys,zipfile
from pathlib import Path
before,end,proof_name,execution,stage=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from formal_production_native_calendar_checked_v3 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8'))
pre=load(proof_name);px=load(execution+'-execution.json');au=load(before+'.audit.json');validate_native_interval(au['date'],end,30)
with zipfile.ZipFile(run/(before+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
roots={k:v for k,v,x in fs if x};country=q.block(roots['country'],'0');main=q.block(roots['fleet'],'83886903');combat=q.block(main,'combat');enemyids=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(combat,'in_combat_with'))));assert len(enemyids)==1
enemy=q.block(roots['fleet'],str(enemyids[0]));enemyships=q.ids(q.block(enemy,'ships'));es=q.block(roots['ships'],str(enemyships[0])) if len(enemyships)==1 else '';origin=q.scalars(q.block(combat,'coordinate')).get('origin')
owned=q.block(q.block(q.block(roots['country'],'1'),'fleets_manager'),'owned_fleets');ourids=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(country,'fleets_manager'),'owned_fleets'))));active=[i for i in ourids if re.search(r'\bfleet\s*=',q.block(q.block(q.block(roots['fleet'],str(i)),'combat'),'in_combat_with'))]
checks={
 'actual_prior_PASS_source_SAV':pre['status'].startswith('PASS') and all(pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==au['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_known_active_combat_boundary':pre['boundaries']==['native_active_combat_review'] and active==[83886903],
 'original_main18_all_alive_target147':len(q.ids(q.block(main,'ships')))==18 and all(q.scalars(q.block(roots['ships'],str(i))).get('hitpoints',0)>0 for i in q.ids(q.block(main,'ships'))) and q.scalars(q.block(q.block(main,'movement_manager'),'target_coordinate')).get('origin')==147,
 'preexisting_enemy_country1_single_outpost_known_route':enemyids[0] in list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',owned))) and q.scalars(enemy).get('ship_class')=='shipclass_starbase' and len(enemyships)==1 and q.scalars(es).get('construction_date','')<au['date'] and origin in [146,96,53,147],
 'war1_and_no_pending':bool(q.block(roots['war'],'1')) and not any(k=='player_event' and x and q.scalars(v).get('country')==0 for k,v,x in fs),
 'unchanged_reviewed_error':h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':au['save_sha256'],'after_sha256':au['save_sha256'],'start_date':au['date'],'end_date':end,'days':30,'maximum_days':30,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'main_fleet_raw':main,'enemy_fleet_raw':enemy,'enemy_ship_raw':es,'scope':'One bounded actual known route battle continuation; losses or unexpected messages still require separate investigation.'});print(json.dumps({'status':'PASS' if passed else 'FAIL','failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
