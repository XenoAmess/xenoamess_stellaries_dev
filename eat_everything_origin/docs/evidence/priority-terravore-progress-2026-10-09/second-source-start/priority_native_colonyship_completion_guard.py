"""Bind paid native colony ship item to its real new owned ship and order."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 roots={k:v for k,v,o in q.fields(t) if o};c=q.block(roots['country'],'0');owned=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(c,'fleets_manager'))))
 return a,roots,c,owned
b,br,bc,bo=read(before);a,ar,ac,ao=read(after)
paid=json.loads((run/(before+'-paid-colonyship-proof.json')).read_text('utf-8'));wait=json.loads((run/(after+'-paid-wait-v4-proof.json')).read_text('utf-8'))
f=q.block(ar['fleet'],'507');ship=q.block(ar['ships'],'16778453');ss=q.scalars(ship);order=q.block(q.block(f,'current_order'),'colonize_planet_order')
checks={
 'original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'original_all44_paid_checks_bound':len(paid['checks'])==44 and all(paid['checks'].values()) and paid['after_sha256']==b['save_sha256'],
 'original_all21_wait_checks_bound':len(wait['checks'])==21 and all(wait['checks'].values()) and wait['before_sha256']==b['save_sha256'] and wait['after_sha256']==a['save_sha256'],
 'original_owned_fleets_only_append507':ao==bo+[507] and not q.block(br['fleet'],'507'),
 'new_real_colonizer_ship_owned_exact':not q.block(br['ships'],'16778453') and q.ids(q.block(f,'ships'))==[16778453] and ss['fleet']==507 and q.scalars(f)['ship_class']=='shipclass_colonizer',
 'new_ship_actual_date_original_design_species':b['date']<ss['construction_date']<=a['date'] and q.scalars(q.block(ship,'ship_design_implementation'))=={'design':33554522,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(ship,'colonization_data'))=={'species':3321888769},
 'original_paid_queue3_and_expansion_consumed':q.ids(q.block(q.block(q.block(q.block(br['construction'],'queue_mgr'),'queues'),'3'),'items'))==[553648131] and not q.block(q.block(q.block(q.block(ar['construction'],'queue_mgr'),'queues'),'3'),'items') and not q.block(q.block(ac,'modules'),'standard_expansion_module').strip(),
 'original_paid_colonization_target124_reachable':q.scalars(order)['planet']==124 and q.scalars(order)['can_reach']=='yes' and q.scalars(q.block(q.block(q.block(f,'movement_manager'),'target'),'coordinate'))['origin']==75,
}
p={'status':'PASS_NATIVE_COLONYSHIP_COMPLETION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_fleet':507,'actual_ship':16778453,'actual_construction_date':ss['construction_date'],'actual_system':q.scalars(q.block(q.block(f,'movement_manager'),'coordinate'))['origin'],'native_path_ETA':q.scalars(q.block(q.block(f,'movement_manager'),'path')).get('date'),'scope':'Paid real ship completed and owns order to124; no arrival or established colony claim.'}
out=run/(after+'-colonyship-completion-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original completion FAIL retained'
