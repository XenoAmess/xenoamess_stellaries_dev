"""Read-only exact-instance same-day native main fleet reinforcement guard."""
import itertools,json,logging,re,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-autosave2-campaign-22791201';after='terravore-rear-defense-main-ordered'
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(st+'.audit.json'),fs,{k:v for k,v,x in fs if x}
b,bf,br=read(before);a,af,ar=read(after)
omit=lambda raw,keys:[(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
fleets=[{k:v for k,v,x in q.fields(rr['fleet']) if x} for rr in [br,ar]]
old,new=[f['83886903'] for f in fleets];bm,am=[q.block(f,'movement_manager') for f in [old,new]]
nodes=[v for k,v,x in q.fields(q.block(am,'path')) if k=='node'];route=[k for k,g in itertools.groupby(q.scalars(q.block(n,'coordinate'))['origin'] for n in nodes)]
order=q.block(q.block(new,'current_order'),'orbit_planet_order');move=q.block(q.block(order,'sub_order'),'move_to_system_point_order')
ps=[{k:v for k,v,x in q.fields(q.block(rr['planets'],'planet')) if x} for rr in [br,ar]]
pre=load(before+'-campaign-v4-proof.json');px=load(before+'-campaign-guard-v4-execution.json')
iv=load('terravore-rear-defense-native-cache-diff-investigation.json')
checks={
 'prior17_PASS_actual0_source_SAV':len(pre['checks'])==17 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SAV_pair':a['date']==b['date']=='2279.12.01' and all(h.sha256(run/(s+'.sav'))==u['save_sha256'] for s,u in [(before,b),(after,a)]),
 'all_other_world_raw_held':[(k,v,x) for k,v,x in bf if k not in {'fleet','planets','random_count'}]==[(k,v,x) for k,v,x in af if k not in {'fleet','planets','random_count'}],
 'other_fleets_only_exact_caravaneer_dirty_flag':set(fleets[0])==set(fleets[1]) and all(fleets[0][i]==fleets[1][i] for i in fleets[0] if i not in {'83886903','64'}) and fleets[0]['64']==iv['fleet64_raw'][0] and fleets[1]['64']==iv['fleet64_raw'][1] and omit(fleets[0]['64'],{'properties'})==omit(fleets[1]['64'],{'properties'}) and q.scalars(q.block(fleets[1]['64'],'properties'))==dict(q.scalars(q.block(fleets[0]['64'],'properties')),dirty_cloaking_strength='yes'),
 'native_random_count_exact_instance_plus2':[[v for k,v,x in f if k=='random_count'] for f in [bf,af]]==iv['random_count']==[['348048821'],['348048823']],
 'planets_only_main_leaving_old_star_orbit':set(ps[0])==set(ps[1]) and all(ps[0][i]==ps[1][i] for i in ps[0] if i!='1573') and omit(ps[0]['1573'],{'planet_orbitals'})==omit(ps[1]['1573'],{'planet_orbitals'}) and q.scalars(q.block(ps[0]['1573'],'planet_orbitals'))=={'0':83886903} and not q.block(ps[1]['1573'],'planet_orbitals').strip(),
 'only_main_order_movement_auto_order_changed':omit(old,{'order_id','current_order','movement_manager','auto_movement'})==omit(new,{'order_id','current_order','movement_manager','auto_movement'}) and q.scalars(old)['order_id']==2 and q.scalars(new)['order_id']==3 and not q.block(new,'auto_movement'),
 'main18_full_hull_all_ship_raw_held':len(q.ids(q.block(new,'ships')))==18 and q.block(old,'ships')==q.block(new,'ships') and q.scalars(new)['hit_points']==4860 and br['ships']==ar['ships'],
 'same_position147_and_native_target188':q.block(bm,'coordinate')==q.block(am,'coordinate') and q.scalars(q.block(am,'coordinate'))['origin']==147 and q.scalars(q.block(move,'coordinate'))==q.scalars(q.block(am,'target_coordinate'))==q.scalars(q.block(q.block(am,'target'),'coordinate'))=={'x':19.61,'y':-21.61,'origin':188} and q.scalars(order)['can_reach']=='yes' and q.scalars(q.block(order,'orbitable'))=={'starbase':160} and q.scalars(q.block(order,'star'))=={'planet':1950},
 'actual_native_route_edges_and_estimate':route==[147,53,96,146,188] and len(nodes)==9 and q.scalars(q.block(am,'path'))['date']=='2280.09.18' and all(y in map(int,re.findall(r'\bto\s*=\s*(\d+)',q.block(q.block(ar['galactic_object'],str(x)),'hyperlane'))) for x,y in zip(route,route[1:])),
 'all_audit_business_exact_held':all(b[k]==a[k] for k in b if k not in {'save','save_sha256','gamestate_sha256','gamestate_bytes'}),
 'normal_right_click_actual0_native_save_actual0':load('terravore-rear-defense-main-right-ordered-execution.json')['returncode']==load(after+'-save-execution.json')['returncode']==0 and load('terravore-rear-defense-main-right-ordered.action.json')['client_point']==[511,385],
 'error_exact_3723B_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes() and h.sha256(user/'logs/error.log')=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
 'no_country0_pending':not any(k=='player_event' and x and q.scalars(v).get('country')==0 for k,v,x in af),
}
passed=all(v is True for v in checks.values());out=run/(after+'-move-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_REAR188_REINFORCEMENT_ORDER' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'route':route,'boundaries':['native_active_combat_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Same-day normal order only; no arrival, battle or full route acceptance claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
