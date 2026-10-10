"""Exact companion for retained tutorial245 ACK failure; never mutates game state."""
import json, logging, re, shutil, sys, zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path[:0] = ['eat_everything_origin/tools']
sys.argv = ['runtime']
import runtime as r, audit_save as q

logging.disable(logging.INFO)
h = r.harness
run, user, metadata = h.load_run()
dest = run / Path(__file__).name
if dest.exists():
    assert dest.read_bytes() == Path(__file__).read_bytes()
else:
    shutil.copyfile(__file__, dest)
before = 'terravore-colony1085-build-travel360'
after = 'terravore-tutorial245-acked'
expected_shas = [
    'c0678d32ce243a8f3f037515f20103e6778ac06716d0cd90f7d39e71d48fe31d',
    'b842f83b4471807cf22014978e0da466b236045e4d50f061356584eb60656c09',
]

def load(name):
    return json.loads((run / name).read_text('utf-8'))

def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        text = z.read('gamestate').decode('utf-8-sig')
    fields = list(q.fields(text))
    return load(stage + '.audit.json'), fields, {k: v for k, v, o in fields if o}

b, bf, br = read(before)
a, af, ar = read(after)
original = load(after + '-empty-ack-proof.json')
execution = load(after + '-guard-execution.json')
failed = {'all_other_ordered_top_raw_held', 'all_ships_fleets_construction_planets_pop_species_raw_held'}
old_sha = '62d850f93d60a09265eec3b68171a595062c99e9ffdfc46dc7a7227cc5e850cb'
fleets_b, fleets_a = list(q.fields(br['fleet'])), list(q.fields(ar['fleet']))
fb = {k: v for k, v, o in fleets_b}['807']
fa = {k: v for k, v, o in fleets_a}['807']

def retained_top(fields):
    return [(k, '<exact-fleet-compared-separately>' if k == 'fleet' else v, o)
            for k, v, o in fields
            if k != 'open_player_event_selection_history'
            and not (k == 'player_event' and o and q.scalars(v).get('id') == 245)
            and not (k == 'message' and o and q.scalars(v).get('event') == 245)]

def owners(top):
    return [k for k, v, o in q.fields(top['country']) if o and '807' in
            re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(v, 'fleets_manager'), 'owned_fleets'))]

def selections(top):
    return re.findall(r'\{\s*player_event=(\d+)\s+human=(-?\d+)\s+option=(\d+)\s*\}',
                      q.block(top['open_player_event_selection_history'], 'selected'))

source = Path(original['native_source'])
events = [v for k, v, o in q.fields(source.read_text('utf-8-sig'))
          if o and q.scalars(v).get('id') == 'tutorial.2550']
assert len(events) == 1
options = [v for k, v, o in q.fields(events[0]) if k == 'option' and o]
checks = {
    'original13_exact_two_FAIL_actual1_SHA_bound': len(original['checks']) == 13
        and original['status'] == 'FAIL'
        and {k for k, v in original['checks'].items() if v is not True} == failed
        and all(original['checks'][k] is False for k in failed)
        and execution['returncode'] == 1 and execution['helper_sha256'] == old_sha
        and h.sha256(run / Path(execution['command'][1]).name) == old_sha,
    'exact_actual_same_date_SHA_pair_bound': a['date'] == b['date'] == '2266.03.17'
        and [original['before_sha256'], original['after_sha256']] == expected_shas
        and all(h.sha256(run / (st + '.sav')) == au['save_sha256'] == sha
                for st, au, sha in zip([before, after], [b, a], expected_shas)),
    'all_original11_other_checks_remain_true': all(v is True for k, v in original['checks'].items() if k not in failed),
    'all_other_ordered_top_raw_held': retained_top(bf) == retained_top(af),
    'all_other_fleets_and_order_exact_raw_held':
        [(k, '<807>' if k == '807' else v, o) for k, v, o in fleets_b]
        == [(k, '<807>' if k == '807' else v, o) for k, v, o in fleets_a],
    'fleet807_all_nonproperties_exact_raw_held':
        [(k, v, o) for k, v, o in q.fields(fb) if k != 'properties']
        == [(k, v, o) for k, v, o in q.fields(fa) if k != 'properties'],
    'fleet807_only_exact_cache_marker_appended': list(q.fields(q.block(fb, 'properties')))
        == [('civilian', 'yes', False), ('mobile', 'yes', False), ('valid_for_combat', 'yes', False)]
        and list(q.fields(q.block(fa, 'properties')))
        == list(q.fields(q.block(fb, 'properties'))) + [('dirty_cloaking_strength', 'yes', False)],
    'fleet807_country1_science_ship67110321_HP300_held': owners(br) == owners(ar) == ['1']
        and all(q.scalars(f).get('ship_class') == 'shipclass_science_ship'
                and q.scalars(f).get('hit_points') == 300
                and q.block(f, 'ships').strip() == '67110321' for f in [fb, fa]),
    'all_countries_ships_construction_planets_population_species_raw_held':
        all(br[k] == ar[k] for k in ['country', 'ships', 'construction', 'planets', 'colony', 'pop_jobs', 'pop_groups', 'species_db'])
        and a['countries'] == b['countries'],
    'exact245_tutorial2550_removed_and_single_human1_option0':
        len([v for k, v, o in bf if k == 'player_event' and o
             and q.scalars(v).get('id') == 245 and q.scalars(v).get('event') == 'tutorial.2550'
             and q.scalars(v).get('country') == 0]) == 1
        and not [v for k, v, o in af if k == 'player_event' and o and q.scalars(v).get('id') == 245]
        and selections(ar) == selections(br) + [('245', '1', '0')],
    'no_country0_pending_or_event245_messages': not [v for k, v, o in af if o
        and ((k == 'player_event' and q.scalars(v).get('country') == 0)
             or (k == 'message' and q.scalars(v).get('event') == 245))],
    'source_SHA_empty_UNDERSTOOD_bound': h.sha256(source)
        == original['native_source_sha256'] == '8c4c37f1eaaa4da170dca0085a43b98b376ce1abe4052a911b55ae119f293aa3'
        and original['native_event'] == 'tutorial.2550' and original['native_player_event_id'] == 245
        and original['native_option_index'] == 0 and q.scalars(options[0]).get('name') == 'UNDERSTOOD'
        and all(k in {'name', 'trigger', 'allow', 'custom_gui', 'default_hide_option', 'exclusive_trigger', 'custom_tooltip'}
                for k, v, o in q.fields(options[0]))
        and all(k == 'custom_tooltip' for k, v, o in q.fields(q.block(events[0], 'after'))),
    'normal_original_click_and_save_actual0':
        all(load(st + '-execution.json')['returncode'] == 0 for st in ['terravore-tutorial245-ack-click', after + '-save'])
        and load('terravore-tutorial245-ack-click.action.json')['action'] == 'left-click',
    'original_unfiltered_errors2670_exact_held':
        (run / (before + '-error-after.log')).read_bytes()
        == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and (run / (after + '-error-after.log')).stat().st_size == 2670,
}
passed = all(checks.values())
proof = {'status': 'PASS_NATIVE_TUTORIAL245_ACK_EXACT_CACHE_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'],
         'original_fail_proof': after + '-empty-ack-proof.json', 'original_fail_helper_sha256': old_sha,
         'cache_delta': {'owner': 1, 'fleet': 807, 'ship': 67110321,
                         'properties_appended': {'dirty_cloaking_strength': 'yes'}},
         'calendar_ready': passed,
         'scope': 'Exact paused tutorial245 ACK cache difference only. Original two FAIL retained. No causal C++ claim, reward, movement, upgrade, colony or route-completion claim.'}
out = run / (after + '-tutorial245-cache-ack-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks),
                  'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Original companion FAIL retained'
