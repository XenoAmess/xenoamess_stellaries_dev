"""Permit three native days around the original ordinary corvette MIA return."""
import json,logging,re,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-rear188-campaign-22800101';stage='terravore-first-original-corvette-mia-review'
pre=load(before+'-campaign-v5-proof.json');px=load(before+'-campaign-guard-v5-execution.json');o=load(before+'-construction-boundary-observation-v4.json');a=o['after_state'];f=a['owned_fleets_raw']['33555013'];ship=a['owned_ships_raw']['33555519']
checks={
 'prior18_PASS_actual0_source_SAV':len(pre['checks'])==18 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_original_MIA_boundary_no_active_combat':pre['boundaries']==['original_native_MIA_return_review'] and not any(re.search(r'\bfleet\s*=',q.block(q.block(v,'combat'),'in_combat_with')) for v in a['owned_fleets_raw'].values()),
 'original_corvette_MIA_identity_date_full_health':q.ids(q.block(f,'ships'))==[33555519] and q.scalars(q.block(f,'properties')).get('mia')=='yes' and q.scalars(f)['return_date']=='2280.01.03' and q.scalars(q.block(q.block(f,'movement_manager'),'coordinate'))['origin']==4294967295 and q.scalars(ship)['fleet']==33555013 and q.scalars(ship)['construction_date']=='2261.11.08' and q.scalars(ship)['hitpoints']==q.scalars(ship)['max_hitpoints']==270,
 'other_original_MIA_dates_held':all(q.scalars(q.block(a['owned_fleets_raw'][fid],'properties')).get('mia')=='yes' and q.scalars(a['owned_fleets_raw'][fid])['return_date']==date for fid,date in [('2','2280.03.16'),('33555278','2281.06.27')]),
 'CN_date_no_pending_error_held':m['language']=='l_simp_chinese' and a['audit']['date']=='2280.01.01' and not a['pending_country0_raw'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'start_date':'2280.01.01','end_date':'2280.01.04','days':3,'maximum_days':3,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'original_mia_fleet_raw':f,'original_mia_ship_raw':ship,'scope':'Three native days only. A return must retain the original fleet/ship identity; no teleport/grant and no future return claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
