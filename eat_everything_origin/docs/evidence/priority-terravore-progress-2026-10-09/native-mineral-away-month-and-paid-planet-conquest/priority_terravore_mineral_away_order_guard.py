"""Read-only same-day native mineral fleet order and undocking checks."""
import json,logging,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-camera-live-pulse';after='terravore-mineral-away-valid-order'
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(st+'.audit.json'),fs,{k:v for k,v,x in fs if x}
b,bf,br=read(before);a,af,ar=read(after)
omit=lambda raw,keys:[(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
fleets=[{k:v for k,v,x in q.fields(rr['fleet']) if x} for rr in [br,ar]]
old,new=[f['50332250'] for f in fleets];bm,am=[q.block(f,'movement_manager') for f in [old,new]]
bases=[{k:v for k,v,x in q.fields(q.block(rr['starbase_mgr'],'starbases')) if x} for rr in [br,ar]]
pre=load(before+'-campaign-v11-proof.json');px=load(before+'-campaign-guard-v11-execution.json')
order=q.block(q.block(new,'current_order'),'move_to_system_point_order')
checks={
 'prior26_PASS_actual0_source_SAV':len(pre['checks'])==26 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SAV_pair':a['date']==b['date']=='2280.05.02' and all(h.sha256(run/(s+'.sav'))==u['save_sha256'] for s,u in [(before,b),(after,a)]),
 'all_other_world_ordered_raw_held':[(k,v,x) for k,v,x in bf if k not in {'fleet','starbase_mgr','random_count'}]==[(k,v,x) for k,v,x in af if k not in {'fleet','starbase_mgr','random_count'}],
 'all_other_fleets_exact_held':set(fleets[0])==set(fleets[1]) and all(fleets[0][i]==fleets[1][i] for i in fleets[0] if i!='50332250'),
 'native_random_count_exact_instance_plus2':[[v for k,v,x in f if k=='random_count'] for f in [bf,af]]==[['354334631'],['354334633']],
 'base0_only_original_berth1_vacated':bases[0].keys()==bases[1].keys() and all(bases[0][i]==bases[1][i] for i in bases[0] if i!='0') and omit(bases[0]['0'],{'orbitals'})==omit(bases[1]['0'],{'orbitals'}) and q.scalars(q.block(bases[0]['0'],'orbitals'))=={'0':33555294,'1':50332250,'2':4294967295} and q.scalars(q.block(bases[1]['0'],'orbitals'))=={'0':33555294,'1':4294967295,'2':4294967295},
 'only_native_movement_order_and_exact_dirty_property':omit(old,{'order_id','current_order','movement_manager','properties'})==omit(new,{'order_id','current_order','movement_manager','properties'}) and q.scalars(new)['order_id']==1 and q.scalars(q.block(new,'properties'))==dict(q.scalars(q.block(old,'properties')),dirty_cloaking_strength='yes'),
 'seven_original_ships_all_raw_held':len(q.ids(q.block(new,'ships')))==7 and q.block(old,'ships')==q.block(new,'ships') and br['ships']==ar['ships'],
 'same_position_system0_reachable_in_system_target':q.block(bm,'coordinate')==q.block(am,'coordinate') and q.scalars(q.block(am,'coordinate'))['origin']==0 and q.scalars(q.block(order,'coordinate'))==q.scalars(q.block(am,'target_coordinate'))==q.scalars(q.block(q.block(am,'target'),'coordinate'))=={'x':-21.034,'y':43.80752,'origin':0} and q.scalars(order)['can_reach']=='yes' and not q.block(am,'orbit').strip() and q.scalars(q.block(am,'path'))['date']=='2280.05.12',
 'all_audit_business_exact_held':all(b[k]==a[k] for k in b if k not in {'save','save_sha256','gamestate_sha256','gamestate_bytes'}),
 'native_selection_right_click_and_save_actual0':all(load(n+'-execution.json')['returncode']==0 for n in ['terravore-mineral-away-select-fleet','terravore-mineral-away-select-order','terravore-mineral-away-order-save']) and load('terravore-mineral-away-select-order.action.json')['client_point']==[680,590],
 'production41_simp_chinese_held':m['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'error_exact_3723B_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes() and h.sha256(user/'logs/error.log')=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
 'no_country0_pending':not any(k=='player_event' and x and q.scalars(v).get('country')==0 for k,v,x in af),
}
passed=all(v is True for v in checks.values());out=run/(after+'-away-order-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_MINERAL_UNDOCK_ORDER' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':29 if passed else 0,'scope':'Same-day paid original seven mineral ships ordinary order and berth removal only. Away monthly upkeep requires separate verification.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
