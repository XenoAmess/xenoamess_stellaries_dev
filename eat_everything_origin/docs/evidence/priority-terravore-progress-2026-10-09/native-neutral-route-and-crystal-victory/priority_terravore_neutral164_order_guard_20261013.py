"""Read-only proof of a same-date normal UI order to a neutral waypoint."""
import json, logging, sys
from itertools import groupby
from pathlib import Path
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state, omit
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = 'terravore-postmarket-operating-22851101'
after = 'terravore-main-neutral164-order-22851101'
load = lambda name: json.loads((run / name).read_text('utf-8-sig'))
def checked(stage):
    x = load(stage + '-execution.json')
    return x['returncode'] == 0 and x['helper_sha256'] == h.sha256(Path(x['command'][1]))
b, a = read_state(run, before), read_state(run, after)
ba, aa = b['audit'], a['audit']
p = load(before + '-postmarket-29day-v2-proof.json')
fid = '83886903'
bf, af = b['fleets'][fid], a['fleets'][fid]
bm, am = q.block(bf, 'movement_manager'), q.block(af, 'movement_manager')
order = q.block(q.block(af, 'current_order'), 'orbit_planet_order')
path = q.block(am, 'path')
nodes = [q.scalars(q.block(v, 'coordinate'))['origin'] for k, v, obj in q.fields(path) if obj and k == 'node']
bp, ap = q.block(b['roots']['planets'], 'planet'), q.block(a['roots']['planets'], 'planet')
provenance = {'save', 'save_sha256', 'gamestate_sha256', 'gamestate_bytes'}
checks = {
 'prior24PASS_actual0_source_originalSAV': len(p['checks']) == 24 and p['status'].startswith('PASS') and all(v is True for v in p['checks'].values()) and checked(before + '-postmarket-29day-v2-guard') and p['after_sha256'] == ba['save_sha256'] == h.sha256(run / (before + '.sav')),
 'same_paused_November1_save_actual0': ba['date'] == aa['date'] == '2285.11.01' and checked(after + '-native-save') and aa['save_sha256'] == h.sha256(run / (after + '.sav')),
 'all_country0_raw_held': b['country'] == a['country'],
 'all_audit_business_held': {k:v for k,v in ba.items() if k not in provenance} == {k:v for k,v in aa.items() if k not in provenance},
 'all77_original_ships_full_raw_held': len(b['ships']) == 77 and b['ships'] == a['ships'],
 'only_main_of35_fleets_order_fields_change': len(b['fleets']) == len(a['fleets']) == 35 and set(b['fleets']) == set(a['fleets']) and {k for k in b['fleets'] if b['fleets'][k] != a['fleets'][k]} == {fid} and omit(bf, {'auto_movement','current_order','order_id','movement_manager'}) == omit(af, {'auto_movement','current_order','order_id','movement_manager'}),
 'single_reachable_native_order_target_star1732': [(k,obj) for k,v,obj in q.fields(q.block(af,'current_order'))] == [('orbit_planet_order',True)] and q.scalars(order)['can_reach'] == 'yes' and q.scalars(q.block(order,'orbitable')) == {'planet':1732} and q.scalars(q.block(order,'star')) == {'planet':1732} and q.scalars(q.block(q.block(order,'sub_order'),'move_to_system_point_order'))['can_reach'] == 'yes',
 'main_order_id4_to5_completed_auto_removed': q.scalars(bf)['order_id'] == 4 and q.scalars(af)['order_id'] == 5 and not q.block(af,'auto_movement'),
 'neutral_hyperlane_path30_71_164_no_foreign_border': [i for i,_ in groupby(nodes)] == [30,71,164] and all(not q.ids(q.block(q.block(a['roots']['galactic_object'],str(i)),'starbases')) for i in [30,71,164]) and all(target in q.block(q.block(a['roots']['galactic_object'],str(source)),'hyperlane') for source,target in [(30,'to=71'),(71,'to=164')]),
 'ETA_and_current_position_exact_no_day_advance': q.scalars(path)['date'] == '2286.04.25' and q.block(bm,'coordinate') == q.block(am,'coordinate') and q.scalars(q.block(am,'coordinate'))['origin'] == 30 and q.scalars(q.block(am,'target_coordinate')) == {'x':10.62,'y':10.62,'origin':164},
 'only_native_movement_order_fields_changed': omit(bm, {'target','target_coordinate','time_since_last_path_update','path','orbit'}) == omit(am, {'target','target_coordinate','time_since_last_path_update','path','orbit'}) and not q.block(am,'orbit'),
 'only_original_planet462_orbital_released': q.scalars(q.block(q.block(bp,'462'),'planet_orbitals')) == {'0':83886903} and not q.block(q.block(ap,'462'),'planet_orbitals') and omit(q.block(bp,'462'),{'planet_orbitals'}) == omit(q.block(ap,'462'),{'planet_orbitals'}) and omit(bp,{'462'}) == omit(ap,{'462'}) and omit(b['roots']['planets'],{'planet'}) == omit(a['roots']['planets'],{'planet'}),
 'all_other_roots_fleets_held': set(a['roots']) == set(b['roots']) and all(a['roots'][k] == v for k,v in b['roots'].items() if k not in ['planets','fleet']) and omit(a['roots']['fleet'],{fid}) == omit(b['roots']['fleet'],{fid}),
 'normal_UI_inputs_and_two_original_F12_actual0': all(checked(s) for s in ['terravore-vayer-neutral-hover-22851101','terravore-main-select-before164','terravore-main-order-neutral164','terravore-main-order164-eta']) and load('terravore-main-order-neutral164.action.json')['client_point'] == [554,358],
 'messages_held_no_pending': a['messages'] == b['messages'] and not a['pending'] and not b['pending'],
 'CN41_unfiltered_error_held': meta['language'] == 'l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes() == (run/(before+'-error-after.log')).read_bytes() == (run/(after+'-error-after.log')).read_bytes(),
}
passed = all(v is True for v in checks.values())
out = run / (after + '-neutral164-order-proof.json')
assert not out.exists()
h.write_json(out, {'status':'PASS_NATIVE_NEUTRAL164_ORDER' if passed else 'FAIL', 'checks':checks, 'before_sha256':ba['save_sha256'], 'after_sha256':aa['save_sha256'], 'date':aa['date'], 'boundaries':['native_neutral164_travel_operating_review'], 'native_devour_calendar_ready':False, 'maximum_days_to_native_bite_boundary':0, 'scope':'Same-date normal native waypoint order only; no battle, war or full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL', 'checks':len(checks), 'failed':[k for k,v in checks.items() if v is not True]}), flush=True)
assert passed
