"""One native day of the original three-army zero-defender ground combat."""
import json,logging,sys,zipfile,shutil
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-balthasar-landing-day-22801102';stage='terravore-balthasar-ground-endpoint-review'
pre=load(before+'-campaign-v17-proof.json');px=load(before+'-campaign-guard-v17-execution.json');a=load(before+'-construction-boundary-observation-v4.json')['after_state']
with zipfile.ZipFile(run/(before+'.sav')) as z:rr={k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
source=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/crisis_objectives/00_crisis_objectives.txt');dest=run/(stage+'-00_crisis_objectives.txt');assert not dest.exists();shutil.copyfile(source,dest)
ground=q.block(rr['ground_combat'],'150994944');armies={i:v for i,v,x in q.fields(rr['army']) if x and q.scalars(v).get('colony')==30};planet=q.block(q.block(rr['planets'],'planet'),'1578')
checks={
 'prior29_PASS_actual0_source_SAV':len(pre['checks'])==29 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_ground_boundary_date':pre['boundaries']==['native_active_ground_combat_review'] and a['audit']['date']=='2280.11.02',
 'original_ground_colony30_three_full_attackers_no_defenders':q.scalars(ground)['colony']==30 and set(q.ids(q.block(ground,'attackers')))=={50331728,33554574,33554634} and not q.ids(q.block(ground,'defenders')) and set(map(int,armies))=={50331728,33554574,33554634} and all(q.scalars(v)['owner']==0 and q.scalars(v)['health']==330 and q.scalars(v)['morale']==200 for v in armies.values()),
 'target14_still_enemy1_active_original_war':q.scalars(planet)['owner']==q.scalars(planet)['controller']==1 and q.scalars(planet)['planet_size']==14 and q.scalars(q.block(rr['war'],'1'))['start_date']=='2265.12.30',
 'native_conquer_objective_original_SHA':h.sha256(source)==h.sha256(dest) and 'crisobj_conquer_worlds = {' in source.read_text('utf-8-sig'),
 'CN_no_pending_error_held':m['language']=='l_simp_chinese' and not a['pending_country0_raw'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':pre['after_sha256'],'after_sha256':pre['after_sha256'],'start_date':'2280.11.02','end_date':'2280.11.03','days':1,'maximum_days':1,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'source':str(source),'source_sha256':h.sha256(source),'preserved_source':dest.name,'ground_original':ground,'armies_original':armies,'target_original':planet,'scope':'Observe one day only. No victory, conquest ownership, Menace or other rewards pre-approved.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
