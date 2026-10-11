"""Read-only exact native rear capture and single same-day science retreat."""
import json
import logging
import re
import sys
import zipfile

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run / n).read_text('utf-8-sig'))
def read(label):
    with zipfile.ZipFile(run / (label + '.sav')) as archive:
        fs = list(q.fields(archive.read('gamestate').decode('utf-8-sig')))
    roots = {k: v for k, v, obj in fs if obj}
    countries = {i: q.block(roots['country'], i) for i in ['0', '1']}
    fleets = {k: v for k, v, obj in q.fields(roots['fleet']) if obj}
    ships = {k: v for k, v, obj in q.fields(roots['ships']) if obj}
    owned = {i: list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)',
        q.block(q.block(c, 'fleets_manager'), 'owned_fleets')))) for i, c in countries.items()}
    ids = sorted({sid for fid in owned['0'] for sid in q.ids(q.block(fleets[str(fid)], 'ships'))})
    messages = [v for k, v, obj in fs if k == 'message' and obj and q.scalars(v).get('receiver') == 0]
    return {'audit': load(label + '.audit.json'), 'countries_raw': countries, 'owned_fleets': owned,
        'owned_ship_ids': ids, 'owned_fleets_raw': {str(i): fleets[str(i)] for i in owned['0']},
        'owned_ships_raw': {str(i): ships[str(i)] for i in ids},
        'watched_fleets_raw': {i: fleets[i] for i in ['166', '804', '825']},
        'watched_ships_raw': {i: ships[i] for i in ['1049', '67109591']},
        'leader74_raw': q.block(roots['leaders'], '74'),
        'starbases_raw': {i: q.block(q.block(roots['starbase_mgr'], 'starbases'), i) for i in ['153', '158']},
        'wars_raw': roots['war'], 'messages_country0_raw': messages,
        'pending_country0_raw': [v for k, v, obj in fs if k == 'player_event' and obj and q.scalars(v).get('country') == 0]}

before = 'terravore-rear97-science-native-emergency-retreated'
after = 'terravore-source37-native-mainfleet-reinforcement-ordered'
pre = load(before + '-native-capture-retreat-v2-proof.json')
pe = load(before + '-independent-guard-v2-execution.json')
se = load(after + '-save-execution.json')
b, a = read(before), read(after)
ba, aa = b['audit'], a['audit']
with zipfile.ZipFile(run / (after + '.sav')) as z:
    main = q.block(q.block(z.read('gamestate').decode('utf-8-sig'), 'fleet'), '83886903')
move = q.block(main, 'movement_manager')
checks = {
    'prior13_PASS_actual0_exact_source_SAV': len(pre['checks']) == 13 and all(v is True for v in pre['checks'].values())
        and pe['returncode'] == 0 and pe['helper_sha256'] == h.sha256(run / 'priority_terravore_native_capture_retreat_guard_v2.py')
        == 'a4f1c1002256671f34923a7b4198b98cf25cc47526f9a16cc90c1413bf95f297'
        and pre['after_sha256'] == ba['save_sha256'],
    'same_day_normal_save_actual0_source_SAVs': ba['date'] == aa['date'] == '2277.11.01'
        and se['returncode'] == 0 and se['helper_sha256'] == h.sha256(run / 'priority_native_save.py')
        == '19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e'
        and all(au['save_sha256'] == h.sha256(run / (st + '.sav')) for st, au in [(before, ba), (after, aa)]),
    'same_country_resources_banks_EEP_gov': ba['countries']['0'] == aa['countries']['0'],
    'same_source_mother_pops_situation_and_structures': all(ba[k] == aa[k]
        for k in ['planets', 'colonies', 'situations', 'districts', 'deposits', 'pop_groups', 'pop_jobs', 'species']),
    'all_owned_ship_ids_actual_design_HP_and_leader_held': b['owned_ship_ids'] == a['owned_ship_ids']
        and b['owned_ships_raw'] == a['owned_ships_raw'] and b['leader74_raw'] == a['leader74_raw'],
    'original18_main_fleet_normal_target37_current_location0': len(q.ids(q.block(main, 'ships'))) == 18
        and q.ids(q.block(main, 'ships')) == q.ids(q.block(b['owned_fleets_raw']['83886903'], 'ships'))
        and q.scalars(q.block(move, 'target_coordinate')).get('origin') == 37
        and q.scalars(q.block(move, 'coordinate')).get('origin') == 0,
    'original_science_native_MIA_and_capture_remain_unchanged': b['watched_fleets_raw'] == a['watched_fleets_raw']
        and b['starbases_raw'] == a['starbases_raw'] and b['wars_raw'] == a['wars_raw'],
    'one_native_rightclick_source_actual0_no_extra_orders': load('terravore-source37-mainfleet7-native-move-order-execution.json')['returncode'] == 0
        and load('terravore-source37-mainfleet7-native-move-order.action.json')['client_point'] == [601, 423],
    'no_new_messages_pending_or_error': b['messages_country0_raw'] == a['messages_country0_raw']
        and b['pending_country0_raw'] == a['pending_country0_raw'] == []
        and (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes(),
    'production41_version020_simp_chinese_held': meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese'
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41 and h.tree_manifest(h.MOD_ROOT)[1]
        == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_MAINFLEET_REINFORCEMENT_ORDER_COMPONENT' if passed else 'FAIL', 'checks': checks,
    'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'], 'date': aa['date'],
    'before_state': b, 'after_state': a, 'main_fleet_order_raw': main, 'paid_births': pre['paid_births'],
    'scope': 'Normal movement order only, not arrival or full route acceptance.'}
out = run / (after + '-native-reinforcement-order-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k,v in checks.items() if v is not True]}), flush=True)
assert passed, 'Original order component failure retained'
