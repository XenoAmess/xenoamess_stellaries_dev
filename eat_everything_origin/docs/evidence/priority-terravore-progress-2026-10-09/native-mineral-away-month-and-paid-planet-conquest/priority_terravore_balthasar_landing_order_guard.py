"""Read-only original same-day native paid three-army landing order checks."""
import itertools,json,logging,re,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-away-full-month-22800701';after='terravore-balthasar-landing-ordered'
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(st+'.audit.json'),fs,{k:v for k,v,x in fs if x}
b,bf,br=read(before);a,af,ar=read(after)
omit=lambda raw,keys:[(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
fleets=[{k:v for k,v,x in q.fields(rr['fleet']) if x} for rr in [br,ar]]
old,new=[f['16778104'] for f in fleets];bm,am=[q.block(f,'movement_manager') for f in [old,new]]
ps=[{k:v for k,v,x in q.fields(q.block(rr['planets'],'planet')) if x} for rr in [br,ar]]
pre=load(before+'-campaign-v13-proof.json');px=load(before+'-campaign-guard-v13-execution.json')
order=q.block(q.block(new,'current_order'),'land_armies_order');orbit=q.block(q.block(order,'sub_order'),'orbit_planet_order');move=q.block(q.block(orbit,'sub_order'),'move_to_system_point_order')
nodes=[v for k,v,x in q.fields(q.block(am,'path')) if k=='node'];route=[k for k,g in itertools.groupby(q.scalars(q.block(n,'coordinate'))['origin'] for n in nodes)]
checks={
 'prior26_PASS_actual0_source_SAV':len(pre['checks'])==26 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SAV_pair':a['date']==b['date']=='2280.07.01' and all(h.sha256(run/(s+'.sav'))==u['save_sha256'] for s,u in [(before,b),(after,a)]),
 'all_other_world_ordered_raw_held':[(k,v,x) for k,v,x in bf if k not in {'fleet','planets','camera_focus','random_count'}]==[(k,v,x) for k,v,x in af if k not in {'fleet','planets','camera_focus','random_count'}],
 'all_other_fleets_exact_held':set(fleets[0])==set(fleets[1]) and all(fleets[0][i]==fleets[1][i] for i in fleets[0] if i!='16778104'),
 'native_random_count_and_camera_exact_instance':[[v for k,v,x in f if k=='random_count'] for f in [bf,af]]==[['356776840'],['356776842']] and [[v for k,v,x in f if k=='camera_focus'] for f in [bf,af]]==[['0'],['147']],
 'mother_only_original_transport_orbit_vacated':ps[0].keys()==ps[1].keys() and all(ps[0][i]==ps[1][i] for i in ps[0] if i!='7') and omit(ps[0]['7'],{'planet_orbitals'})==omit(ps[1]['7'],{'planet_orbitals'}) and q.scalars(q.block(ps[0]['7'],'planet_orbitals'))=={'0':16778104,'1':33555013,'2':2} and q.scalars(q.block(ps[1]['7'],'planet_orbitals'))=={'0':4294967295,'1':33555013,'2':2},
 'only_native_order_movement_arrived_auto_order_cleared':omit(old,{'order_id','current_order','movement_manager','auto_movement'})==omit(new,{'order_id','current_order','movement_manager','auto_movement'}) and q.scalars(new)['order_id']==1 and not q.block(new,'auto_movement').strip(),
 'three_paid_original_transports_and_armies_all_raw_held':set(q.ids(q.block(new,'ships')))=={100664961,50333234,16777713} and q.block(old,'ships')==q.block(new,'ships') and br['ships']==ar['ships'] and br['army']==ar['army'],
 'same_position_system0_no_instant_arrival':q.block(bm,'coordinate')==q.block(am,'coordinate') and q.scalars(q.block(am,'coordinate'))['origin']==0 and not q.block(am,'orbit').strip(),
 'actual_reachable_landing_target_colony30_planet1578':q.scalars(order)['colony']==30 and q.scalars(q.block(orbit,'orbitable'))=={'planet':1578} and q.scalars(q.block(orbit,'star'))=={'planet':1573} and q.scalars(q.block(move,'coordinate'))==q.scalars(q.block(am,'target_coordinate'))=={'x':98.8884,'y':58.75845,'origin':147} and all(q.scalars(v)['can_reach']=='yes' for v in [order,orbit,move]) and q.scalars(ps[1]['1578'])['owner']==q.scalars(ps[1]['1578'])['controller']==1 and q.scalars(ps[1]['1578'])['planet_size']==14 and not q.ids(q.block(q.block(ar['colony'],'30'),'armies')),
 'actual_native_hyperlane_edges_and_arrival_estimate':route==[0,48,53,147] and len(nodes)==7 and q.scalars(q.block(am,'path'))['date']=='2281.02.12' and all(y in map(int,re.findall(r'\bto\s*=\s*(\d+)',q.block(q.block(ar['galactic_object'],str(x)),'hyperlane'))) for x,y in zip(route,route[1:])),
 'all_audit_business_exact_held':all(b[k]==a[k] for k in b if k not in {'save','save_sha256','gamestate_sha256','gamestate_bytes'}),
 'normal_native_landing_menu_and_save_actual0':all(load(n+'-execution.json')['returncode']==0 for n in ['terravore-balthasar-land-armies-confirm','terravore-balthasar-landing-order-save']) and load('terravore-balthasar-land-armies-confirm.action.json')['client_point']==[487,488],
 'production41_CN_error_exact_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
 'no_country0_pending':not any(k=='player_event' and x and q.scalars(v).get('country')==0 for k,v,x in af),
}
passed=all(v is True for v in checks.values());out=run/(after+'-landing-order-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_PAID_THREE_ARMY_LANDING_ORDER' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'route':route,'arrival_estimate':'2281.02.12','boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':30 if passed else 0,'scope':'Original native landing order only; not arrival, conquest or devour completion.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
