"""Independent one-month native MIA return review; no GUI or clock."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();stage='terravore-six-hives-month-22810601';load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
a=read_state(run,stage);p=load(stage+'-six-hives-serial-month-proof.json');x=load(stage+'-serial-month-guard-execution.json');f=a['fleets']['33555278'];s=a['ships']['50333369']
guard=Path(__file__).with_name('priority_terravore_six_hives_return_month_guard.py');dest=run/guard.name
if dest.exists():assert dest.read_bytes()==guard.read_bytes()
else:dest.write_bytes(guard.read_bytes())
checks={
 'prior18PASS_actual0_originalSHA':len(p['checks'])==18 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(run/'priority_terravore_six_hives_serial_month_guard.py')=='71114b36503e1952545bafa7384ff4775dcb110a5c67dfdd1dba37809c0f39be' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(stage+'.sav')),
 'original_single_colonizer_real_MIA_date_birth_design_life':q.ids(q.block(f,'ships'))==[50333369] and q.scalars(f)['return_date']=='2281.06.27' and q.scalars(q.block(f,'properties'))['mia']=='yes' and q.scalars(s)['construction_date']=='2272.09.13' and q.scalars(s)['hitpoints']==q.scalars(s)['max_hitpoints']==625 and q.scalars(s)['armor_hitpoints']==125 and q.scalars(s)['shield_hitpoints']==320 and q.scalars(q.block(s,'ship_design_implementation'))['design']==150995039 and q.scalars(q.block(s,'colonization_data'))=={'species':73},
 'only_MIA_boundary_no_engineer_project_or_storm_completion':p['boundaries']==['original_MIA_return22810627_review'] and p['engineering_zone_progress']+42<360 and p['project2_progress']+130<6000 and not a['pending'],
 'return_guard19_contract_preserved_CN_tree_error_held':h.sha256(guard)==h.sha256(dest) and 'original_colonizer_MIA_return_same_identity_and_live_system' in guard.read_text('utf-8') and m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-colonizer-return-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2281.06.01','end_date':'2281.07.01','days':30,'maximum_days':30,'allowed_boundaries':p['boundaries'],'execution_stage':stage+'-colonizer-return-review','contract_sha256':h.sha256(guard),'original_fleet':f,'original_ship':s,'scope':'Exactly one normal month across original scheduled MIA return; no free move, new ship or grants.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
