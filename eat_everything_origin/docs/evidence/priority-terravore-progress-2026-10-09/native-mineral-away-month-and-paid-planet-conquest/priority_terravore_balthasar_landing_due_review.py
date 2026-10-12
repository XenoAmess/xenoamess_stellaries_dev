"""One native day at the paid three-army landing boundary, no conquest claim."""
import json,logging,sys,zipfile,shutil
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-balthasar-transit-22801101';stage='terravore-balthasar-landing-due-review'
pre=load(before+'-campaign-v16-proof.json');px=load(before+'-campaign-guard-v16-execution.json');a=load(before+'-construction-boundary-observation-v4.json')['after_state'];failed=load(before+'-campaign-v15-proof.json');fx=load(before+'-campaign-guard-v15-execution.json')
with zipfile.ZipFile(run/(before+'.sav')) as z:rr={k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
source=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/defines/00_defines.txt');preserved=run/(stage+'-00_defines.txt');assert not preserved.exists();shutil.copyfile(source,preserved)
fleet=a['owned_fleets_raw']['16778104'];tm=q.block(fleet,'movement_manager');planet=q.block(q.block(rr['planets'],'planet'),'1578')
army_raw={str(i):q.block(rr['army'],str(i)) for i in [50331728,33554574,33554634]}
checks={
 'prior28_PASS_actual0_source_SAV':len(pre['checks'])==28 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'original_arrival_mirror_single_FAIL1_retained':len(failed['checks'])==28 and {k for k,v in failed['checks'].items() if v is not True}=={'paid_original_three_transports_native_colony30_landing_order_held'} and fx['returncode']==1 and fx['helper_sha256']==h.sha256(Path(fx['command'][1])),
 'only_ground_boundary_exact_date':pre['boundaries']==['native_ground_invasion_due_review'] and a['audit']['date']=='2280.11.01',
 'original_three_transports_orbit_actual1578_reachable_landing':set(q.ids(q.block(fleet,'ships')))=={100664961,50333234,16777713} and q.scalars(q.block(tm,'coordinate'))['origin']==147 and q.scalars(q.block(q.block(tm,'orbit'),'orbitable'))=={'planet':1578} and q.scalars(q.block(q.block(fleet,'current_order'),'land_armies_order'))['colony']==30 and q.scalars(q.block(tm,'path'))['date']=='2280.10.21',
 'paid_three_original_armies_full330_association':all(q.scalars(army_raw[str(i)])['ship']==ship and q.scalars(army_raw[str(i)])['owner']==0 and q.scalars(army_raw[str(i)])['health']==330 for i,ship in [(50331728,100664961),(33554574,50333234),(33554634,16777713)]),
 'target_still_enemy14_and_active_war1':q.scalars(planet)['owner']==q.scalars(planet)['controller']==1 and q.scalars(planet)['planet_size']==14 and q.scalars(q.block(rr['war'],'1'))['start_date']=='2265.12.30',
 'native_landing10_days_original_source_SHA':h.sha256(source)==h.sha256(preserved) and any('LANDING_TIME_DAYS' in line and '= 10' in line for line in source.read_text('utf-8-sig').splitlines()),
 'CN_no_pending_error_held':m['language']=='l_simp_chinese' and not a['pending_country0_raw'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':pre['after_sha256'],'after_sha256':pre['after_sha256'],'start_date':'2280.11.01','end_date':'2280.11.02','days':1,'maximum_days':1,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'source':str(source),'source_sha256':h.sha256(source),'preserved_source':preserved.name,'fleet_original':fleet,'army_original':army_raw,'target_original':planet,'scope':'Observe one original native day. No landing, casualties, conquest, resources or Menace pre-approved.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
