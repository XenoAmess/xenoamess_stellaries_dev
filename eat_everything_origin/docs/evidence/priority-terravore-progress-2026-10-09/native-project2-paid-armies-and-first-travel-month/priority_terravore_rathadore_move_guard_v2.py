"""Native main18 move to target147, exact same-day world diff."""
import itertools,json,logging,re,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'));sha=h.sha256
before='terravore-three-assault-armies-paid';after='terravore-main-rathadore-move-ordered'
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return load(st+'.audit.json'),fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after);omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
old,new=[q.block(u['fleet'],'83886903') for u in [br,ar]];bm,am=[q.block(f,'movement_manager') for f in [old,new]];nodes=[v for k,v,o in q.fields(q.block(am,'path')) if k=='node'];route=[k for k,g in itertools.groupby(q.scalars(q.block(n,'coordinate'))['origin'] for n in nodes)];order=q.block(q.block(new,'current_order'),'orbit_planet_order');move=q.block(q.block(order,'sub_order'),'move_to_system_point_order');pre=load(before+'-paid-armies-proof.json');px=load(before+'-guard-execution.json')
checks={
 'prior21_PASS_actual0_original_source_SAV':len(pre['checks'])==21 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==sha(Path(px['command'][1]))=='49f3f7296b6ed96b7b98581c13bd8affd5633a35409277dc0d62d97779a17c74' and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SAV_pair':a['date']==b['date']=='2279.03.01' and all(sha(run/(s+'.sav'))==u['save_sha256'] for s,u in [(before,b),(after,a)]),
 'all_other_world_raw_held_camera37_removed':[(k,v,o) for k,v,o in bf if k not in {'fleet','camera_focus'}]==[(k,v,o) for k,v,o in af if k not in {'fleet','camera_focus'}] and [v for k,v,o in bf if k=='camera_focus']==['37'] and not any(k=='camera_focus' for k,v,o in af),
 'only_main_fleet_order_movement_changed':omit(br['fleet'],{'83886903'})==omit(ar['fleet'],{'83886903'}) and omit(old,{'order_id','current_order','movement_manager'})==omit(new,{'order_id','current_order','movement_manager'}),
 'native_orderid1_to2_new_reachable_star1573_order1':q.scalars(old)['order_id']==1 and q.scalars(new)['order_id']==2 and not q.block(old,'current_order').strip() and q.scalars(order)=={'merge_fleet':'none','can_reach':'yes','order_id':1,'commissioner':4294967295} and q.scalars(q.block(order,'orbitable'))==q.scalars(q.block(order,'star'))=={'planet':1573},
 'original18_and_HP4860_designs_held':len(q.ids(q.block(new,'ships')))==18 and q.block(old,'ships')==q.block(new,'ships') and q.scalars(new)['hit_points']==4860 and br['ships']==ar['ships'],
 'only_native_movement_path_target_change_current188_held':omit(bm,{'target','target_coordinate','path','time_since_last_path_update'})==omit(am,{'target','target_coordinate','path','time_since_last_path_update'}) and q.block(bm,'coordinate')==q.block(am,'coordinate') and q.scalars(q.block(am,'coordinate'))['origin']==188,
 'exact_reachable_target147_center':q.scalars(q.block(move,'coordinate'))==q.scalars(q.block(am,'target_coordinate'))==q.scalars(q.block(q.block(am,'target'),'coordinate'))=={'x':9.63,'y':9.63,'origin':147} and q.scalars(move)=={'can_reach':'yes','commissioner':4294967295},
 'exact_native_hyperlane_path_estimate':route==[188,146,96,53,147] and len(nodes)==9 and q.scalars(q.block(am,'path'))=={'date':'2279.12.18'} and all(q.scalars(n)=={'ftl':'jump_hyperlane'} for n in nodes),
 'all_four_real_hyperlane_edges_exist':all(y in map(int,re.findall(r'\bto\s*=\s*(\d+)',q.block(q.block(ar['galactic_object'],str(x)),'hyperlane'))) for x,y in zip(route,route[1:])),
 'all_audit_business_exact_held':all(b[k]==a[k] for k in b if k not in {'save','save_sha256','gamestate_sha256','gamestate_bytes'}),
 'normal_right_click510385_actual0':load('terravore-main-rathadore-normal-move-execution.json')['returncode']==0 and load('terravore-main-rathadore-normal-move.action.json')['client_point']==[510,385],
 'native_save_actual0_original_error_held':load(after+'-native-save-execution.json')['returncode']==0 and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
 'no_country0_pending':not any(k=='player_event' and o and q.scalars(v).get('country')==0 for k,v,o in af),
}
original=load(after+'-move-proof.json');ox=load(after+'-guard-execution.json');iv=load(after+'-audit-metadata-diff.json')
checks['original14_one_metadata_FAIL_actual1_preserved']=len(original['checks'])==14 and {k for k,v in original['checks'].items() if v is not True}=={'all_audit_business_exact_held'} and ox['returncode']==1 and ox['helper_sha256']==sha(Path(ox['command'][1])) and set(iv['only_changed_audit_keys'])=={'save','save_sha256','gamestate_sha256','gamestate_bytes'} and all(iv['only_changed_audit_keys'][k]==[b[k],a[k]] for k in iv['only_changed_audit_keys'])
passed=all(v is True for v in checks.values());out=run/(after+'-move-v2-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_TERRAVORE_NATIVE_MAIN18_RATHADORE_MOVE_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'route':route,'estimated_arrival':'2279.12.18','boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':30 if passed else 0,'scope':'Normal movement order, first30-day recruitment observation authorized. No arrival or battle claim.'});print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
