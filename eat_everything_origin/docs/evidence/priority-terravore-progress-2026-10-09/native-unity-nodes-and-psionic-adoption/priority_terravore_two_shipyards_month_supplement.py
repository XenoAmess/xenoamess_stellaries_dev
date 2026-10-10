"""Exact read-only explanation of two original monthly assumptions; retain FAIL."""
import json,logging,math,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,{k:v for k,v,o in q.fields(t) if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,br=read(before);a,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];old=json.loads((run/(after+'-two-shipyards-month-proof.json')).read_text('utf-8'));execution=json.loads((run/'terravore-defense-two-shipyards-first-month-guard-execution.json').read_text('utf-8'))
bs,ass=[q.block(rt['ships'],'1564') for rt in [br,ar]];motion={'forward_x','forward_y','rotation','speed','coordinate','target_coordinate'}
checks={
 'original_unique_two_FAIL_retained':old['status']=='FAIL' and len(old['checks'])==32 and [k for k,v in old['checks'].items() if not v]==['original_four_real_design_hull_held','Theory_selected_and_growing'] and execution['returncode']==1,
 'exact_original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256']==old['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==old['after_sha256'],
 'original_other30_checks_bound':sum(v is True for v in old['checks'].values())==30,
 'first_three_whole_ships_raw_held':all(q.block(br['ships'],str(i))==q.block(ar['ships'],str(i)) for i in [16777221,16778303,16778412]),
 'fourth_only_exact_movement_fields':omit(bs,motion)==omit(ass,motion) and {k for k in set(q.scalars(bs))|set(q.scalars(ass)) if q.scalars(bs).get(k)!=q.scalars(ass).get(k)}=={'forward_x','forward_y','rotation','speed'},
 'fourth_same_real_design_full_hull_date_fleet':q.block(bs,'ship_design_implementation')==q.block(ass,'ship_design_implementation') and q.scalars(q.block(ass,'ship_design_implementation'))['design']==67110548 and q.scalars(ass)['hitpoints']==q.scalars(ass)['max_hitpoints']==250 and q.scalars(ass)['construction_date']=='2236.10.13' and q.scalars(ass)['fleet']==16777797,
 'fourth_motion_finite_same_native_system':all(q.scalars(co:=q.block(s,k))['origin']==0 and all(math.isfinite(q.scalars(co)[axis]) for axis in ['x','y']) for s in [bs,ass] for k in ['coordinate','target_coordinate']),
 'Theory_queue_raw_held462_58704':q.block(bc['tech_status'],'society_queue')==q.block(ac['tech_status'],'society_queue') and q.scalars(q.block(ac['tech_status'],'society_queue').strip()[1:-1])['progress']==462.58704 and q.scalars(q.block(ac['tech_status'],'society_queue').strip()[1:-1])['technology']=='tech_psionic_theory' and 'tech_psionic_theory' not in ac['completed_technologies'],
 'true_banks_and_special_points_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints') and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'unfiltered_errors_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_NATIVE_TWO_SHIPYARDS_MONTH_EXACT_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'bound_original_proof_sha256':h.sha256(run/(after+'-two-shipyards-month-proof.json')),'scope':'Only original 30 PASS plus exact motion/unchanged Theory explanation. Original 32-check FAIL retained. No observed Theory increment, defense victory or full-route claim.'}
out=run/(after+'-two-shipyards-month-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Exact supplement FAIL retained; no next calendar'
