"""Independent same-date, paid-asset-preserving native military rally orders."""
import json,logging,re,sys
from itertools import groupby
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
before='terravore-full-paid-fleet-budget-22850601';after='terravore-rally-orders-22850601'
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def checked(stage):
 x=load(stage+'-execution.json');return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
b=read_state(run,before);a=read_state(run,after);ba=b['audit'];aa=a['audit'];p=load(before+'-final-paid-budget-proof.json')
spec={'83886903':(30,[188,139,171,70,30],'2286.03.14',4),'50332250':(188,[0,103,151,188],'2285.12.13',4),'917':(188,[0,103,151,188],'2285.12.10',2)}
routes={};movement=True
for fid,(target,route,eta,oid) in spec.items():
 bm=q.block(b['fleets'][fid],'movement_manager');am=q.block(a['fleets'][fid],'movement_manager');path=q.block(am,'path')
 nodes=[q.scalars(q.block(v,'coordinate'))['origin'] for k,v,obj in q.fields(path) if obj and k=='node'];actual=[i for i,_ in groupby(nodes)];routes[fid]={'nodes':nodes,'route':actual,'eta':q.scalars(path)['date'],'target':q.scalars(q.block(am,'target_coordinate')),'movement_raw':am}
 movement=movement and actual==route and q.scalars(path)['date']==eta and eta<'2286.03.30' and q.scalars(q.block(am,'target_coordinate'))['origin']==target and q.scalars(q.block(q.block(am,'target'),'coordinate'))==q.scalars(q.block(am,'target_coordinate')) and q.scalars(a['fleets'][fid])['order_id']==oid and q.scalars(am)['state']=='move_idle' and not q.block(am,'orbit').strip() and omit(bm,{'target','target_coordinate','path','orbit','state','time_since_last_path_update'})==omit(am,{'target','target_coordinate','path','orbit','state','time_since_last_path_update'})
adjacent=all(v in list(map(int,re.findall(r'\bto\s*=\s*(\d+)',q.block(q.block(a['roots']['galactic_object'],str(u)),'hyperlane')))) for info in routes.values() for u,v in zip(info['route'],info['route'][1:]))
bases={k:v for k,v,obj in q.fields(q.block(a['roots']['starbase_mgr'],'starbases')) if obj};allships={k:v for k,v,obj in q.fields(a['roots']['ships']) if obj};owners={}
for cid,raw,obj in q.fields(a['roots']['country']):
 if obj:
  for fleet in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(raw,'fleets_manager'),'owned_fleets')):owners[int(fleet)]=int(cid)
system_owners={}
for sid in {i for info in routes.values() for i in info['route']}:
 raw=q.block(a['roots']['galactic_object'],str(sid));bs=[i for i in q.ids(q.block(raw,'starbases')) if i!=4294967295];system_owners[str(sid)]=[]
 for bid in bs:
  station=q.scalars(bases[str(bid)])['station'];fid=q.scalars(allships[str(station)])['fleet'];system_owners[str(sid)].append(owners[fid])
expected_owners={'0':[0],'103':[1],'151':[],'188':[0],'139':[1],'171':[1],'70':[1],'30':[]}
base_before=q.block(b['roots']['starbase_mgr'],'starbases');base_after=q.block(a['roots']['starbase_mgr'],'starbases');dock_ok=omit(base_before,{'0','160'})==omit(base_after,{'0','160'})
for sid,old,new in [('0',{'0':33555294,'1':50332250,'2':917},{'0':33555294,'1':4294967295,'2':4294967295}),('160',{'0':83886903},{'0':4294967295})]:
 br,ar=q.block(base_before,sid),q.block(base_after,sid);dock_ok=dock_ok and omit(br,{'orbitals'})==omit(ar,{'orbitals'}) and q.scalars(q.block(br,'orbitals'))==old and q.scalars(q.block(ar,'orbitals'))==new
actions=['terravore-rally-main-order-nishpan','terravore-rally-new-mineral-order-nishpan','terravore-rally-old-mineral-order-nishpan','terravore-rally-old-mineral-order-owned188','terravore-rally-new-mineral-order-owned188','terravore-rally-new-mineral-cancel-late','terravore-rally-old-mineral-cancel-late']
images={'terravore-rally-main-order-ui':'99ced51dafacb1f94dae423284fdec210752753a79972b954e0ac8420a896f74','terravore-rally-old-mineral-owned188-ui':'4ef918a05e102c85e36f2ca7adb9af716ec65da320bedf656f25cf3204ea282e','terravore-rally-new-mineral-owned188-ui':'afa0628c1b8a96edce84e3473bbf4cbbbb972b879655941d018a1943ce9db149'}
checks={
 'prior25_PASS_actual0_source_exact_originalSAV':len(p['checks'])==25 and p['status'].startswith('PASS') and all(v is True for v in p['checks'].values()) and checked(before+'-final-paid-budget-guard') and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')),
 'same_paused_June1_normal_unique_save_actual0':ba['date']==aa['date']=='2285.06.01' and checked(after+'-native-save') and aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'all_country0_raw_cash_research_EEP_crisis_flags_held':b['country']==a['country'],
 'all_audit_business_population_buildings_jobs_assets_held':{k:v for k,v in ba.items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']}=={k:v for k,v in aa.items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']},
 'all77_owned_ships_full_raw_held':len(b['ships'])==77 and b['ships']==a['ships'],
 'only_three_owned_military_fleets_change_exact_order_movement':len(b['fleets'])==len(a['fleets'])==35 and set(b['fleets'])==set(a['fleets']) and {k for k in b['fleets'] if b['fleets'][k]!=a['fleets'][k]}==set(spec) and all(omit(b['fleets'][k],{'movement_manager','order_id'})==omit(a['fleets'][k],{'movement_manager','order_id'}) and q.scalars(a['fleets'][k])['ship_class']=='shipclass_military' for k in spec),
 'actual_normal_target_paths_ETAs_local_coordinates_held':movement,
 'actual_all_route_hops_are_native_hyperlanes':adjacent,
 'route_current_ownership_only_self_open1_unowned':system_owners==expected_owners,
 'only_three_exact_station_orbital_references_cleared':dock_ok,
 'all_other_roots_raw_held_no_civilian_diplomacy_war_construction':set(a['roots'])==set(b['roots']) and all(a['roots'][k]==v for k,v in b['roots'].items() if k not in ['fleet','starbase_mgr']) and omit(a['roots']['fleet'],set(spec))==omit(b['roots']['fleet'],set(spec)),
 'original_move_and_late_route_cancel_UI_actual0_bound':all(checked(s) for s in actions) and all(load(s+'.action.json')['scan_code']==35 for s in actions[-2:]),
 'three_native_ETAs_original_F12_images_source_actual0':all(checked(s) and h.sha256(run/(s+'.jpg'))==sha for s,sha in images.items()),
 'no_new_pending_or_messages':not a['pending'] and a['messages']==b['messages'],
 'CN41_production_unfiltered_error_original_bytes_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-rally-orders-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_RALLY_ORDERS' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'routes':routes,'system_owners':system_owners,'actual_UI_ETAs':images,'boundaries':['native_rally_first_month_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Same-date normal native rally orders only; no calendar, battle, survey, gifts or full-route claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
