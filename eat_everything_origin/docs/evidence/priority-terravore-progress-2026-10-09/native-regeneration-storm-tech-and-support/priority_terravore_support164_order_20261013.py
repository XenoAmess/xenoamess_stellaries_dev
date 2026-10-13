"""Exact same-date two normal mineral fleet support orders, including released berth."""
import json,logging,re,sys
from itertools import groupby
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def checked(stage):
 x=load(stage+'-execution.json');return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
before='terravore-storm550-22860402';after='terravore-support164-orders-22860402'
b,a=read_state(run,before),read_state(run,after);ba,aa=b['audit'],a['audit']
p=load(before+'-storm550-v3-proof.json');fids={'917','50332250'}
provenance={'save','save_sha256','gamestate_sha256','gamestate_bytes'}
checks={
 'prior29PASS_actual0_original_source_SAV':len(p['checks'])==29 and all(v is True for v in p['checks'].values()) and checked(before+'-storm550-v3-guard') and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')),
 'same_paused_date_original_native_save_actual0_SHA':ba['date']==aa['date']=='2286.04.02' and checked(after+'-save') and aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'all_country0_raw_held':b['country']==a['country'],
 'all_audit_business_research_cash_EEP_mother_held':{k:v for k,v in ba.items() if k not in provenance}=={k:v for k,v in aa.items() if k not in provenance},
 'all75_original_ships_complete_raw_held':len(b['ships'])==75 and b['ships']==a['ships'],
 'only_two_of35_original_fleets_changed':len(b['fleets'])==len(a['fleets'])==35 and b['fleets'].keys()==a['fleets'].keys() and {i for i,v in b['fleets'].items() if v!=a['fleets'][i]}==fids,
 'all_other_fleet_world_raw_held':omit(b['roots']['fleet'],fids)==omit(a['roots']['fleet'],fids),
 'all_other_named_world_roots_held':b['roots'].keys()==a['roots'].keys() and all(v==a['roots'][k] for k,v in b['roots'].items() if k not in ['fleet','starbase_mgr']),
 'messages_held_no_pending':b['messages']==a['messages'] and b['pending']==a['pending']==[],
 'normal_two_select_order_UI_actual0':all(checked('terravore-support-'+fid+'-'+action+'-22860402') for fid in ['917','50332250'] for action in ['select','order164']),
 'CN41_live_unfiltered_error_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
routes={}
for fid in sorted(fids):
 bf,af=b['fleets'][fid],a['fleets'][fid];bm,am=q.block(bf,'movement_manager'),q.block(af,'movement_manager');order=q.block(q.block(af,'current_order'),'orbit_planet_order');sub=q.block(q.block(order,'sub_order'),'move_to_system_point_order');path=q.block(am,'path')
 nodes=[q.scalars(q.block(v,'coordinate'))['origin'] for k,v,obj in q.fields(path) if obj and k=='node'];route=[i for i,_ in groupby(nodes)];eta=q.scalars(path)['date'];routes[fid]={'systems':route,'eta':eta,'target':q.scalars(q.block(am,'target_coordinate'))}
 checks[f'fleet{fid}_only_new_order_and_movement_exact_ID_increment']=not q.block(bf,'current_order') and q.scalars(af)['order_id']==q.scalars(bf)['order_id']+1 and omit(bf,{'current_order','order_id','movement_manager','properties'})==omit(af,{'current_order','order_id','movement_manager','properties'})
 checks[f'fleet{fid}_reachable_native_orbit1732_target164']= [(k,obj) for k,v,obj in q.fields(q.block(af,'current_order'))]==[('orbit_planet_order',True)] and q.scalars(order)['can_reach']==q.scalars(sub)['can_reach']=='yes' and q.scalars(q.block(order,'orbitable'))==q.scalars(q.block(order,'star'))=={'planet':1732} and q.scalars(q.block(sub,'coordinate'))==q.scalars(q.block(am,'target_coordinate'))=={'x':10.62,'y':12.62,'origin':164}
 checks[f'fleet{fid}_exact_native_hyperlane_path_and_future_ETA']=route==[188,139,171,70,30,71,164] and eta=={'917':'2287.06.24','50332250':'2287.06.29'}[fid] and all(re.search(r'\bto\s*=\s*'+str(target)+r'\b',q.block(q.block(a['roots']['galactic_object'],str(source)),'hyperlane')) is not None for source,target in zip(route,route[1:]))
 checks[f'fleet{fid}_original188_coordinate_only_target_path_orbit_changed']=q.block(bm,'coordinate')==q.block(am,'coordinate') and q.scalars(q.block(am,'coordinate'))['origin']==188 and omit(bm,{'target','target_coordinate','time_since_last_path_update','path','orbit'})==omit(am,{'target','target_coordinate','time_since_last_path_update','path','orbit'}) and not list(q.fields(q.block(am,'orbit')))
 checks[f'fleet{fid}_only_reviewed_native_cloaking_cache']=q.block(bf,'properties')==q.block(af,'properties') if fid=='917' else q.scalars(q.block(bf,'properties'))=={'weapon':'yes','mobile':'yes','valid_for_combat':'yes'} and q.scalars(q.block(af,'properties'))=={'weapon':'yes','mobile':'yes','valid_for_combat':'yes','dirty_cloaking_strength':'yes'}
bs,ass=q.block(b['roots']['starbase_mgr'],'starbases'),q.block(a['roots']['starbase_mgr'],'starbases');baseb,basea=q.block(bs,'160'),q.block(ass,'160')
checks['only_base160_slot1_released_slot0_stays_INVALID']=q.scalars(q.block(baseb,'orbitals'))=={'0':4294967295,'1':50332250} and q.scalars(q.block(basea,'orbitals'))=={'0':4294967295,'1':4294967295} and omit(baseb,{'orbitals'})==omit(basea,{'orbitals'}) and omit(bs,{'160'})==omit(ass,{'160'}) and omit(b['roots']['starbase_mgr'],{'starbases'})==omit(a['roots']['starbase_mgr'],{'starbases'})
fleet_owner={fid:int(cid) for cid,c,obj in q.fields(a['roots']['country']) if obj for fid in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(c,'fleets_manager'),'owned_fleets'))}
bases={k:v for k,v,obj in q.fields(ass) if obj};ships={k:v for k,v,obj in q.fields(a['roots']['ships']) if obj};owners={}
for system in [188,139,171,70,30,71,164]:
 bids=[i for i in q.ids(q.block(q.block(a['roots']['galactic_object'],str(system)),'starbases')) if i!=4294967295];values=[]
 for bid in bids:
  station=q.scalars(bases[str(bid)])['station'];fleet=q.scalars(ships[str(station)])['fleet'];values.append({'base':bid,'station':station,'fleet':fleet,'owner':fleet_owner[str(fleet)]})
 owners[str(system)]=values
checks['actual_route_owners_188own_four_foreign1_two_unowned']=owners=={'188':[{'base':160,'station':67110520,'fleet':33555300,'owner':0}],'139':[{'base':161,'station':16778697,'fleet':16777750,'owner':1}],'171':[{'base':164,'station':16779172,'fleet':16778075,'owner':1}],'70':[{'base':167,'station':16779167,'fleet':16778072,'owner':1}],'30':[],'71':[{'base':171,'station':33555437,'fleet':33555334,'owner':1}],'164':[]}
passed=all(v is True for v in checks.values());out=run/(after+'-support164-order-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_MINERAL_SUPPORT164_ORDERS' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'routes':routes,'route_owners':owners,'boundaries':['native_support_travel_hive_completion_or_border_change_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Two normal same-day support orders; actual future arrival and border stability remain untested.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'routes':routes}),flush=True);assert passed
