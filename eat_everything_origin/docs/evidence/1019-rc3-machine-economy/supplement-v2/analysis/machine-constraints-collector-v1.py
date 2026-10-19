"""Read archived native records only; no runtime/UI modules are imported."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import zipfile

sys.dont_write_bytecode = True
MOD = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MOD / 'tools'))
sys.path.insert(0, str(MOD / 'testing'))
import audit_save as a
import inspect_1019 as ins

BASE = MOD / 'docs/evidence/1019-rc3-machine-economy'
HW = MOD / 'docs/evidence/1019-rc3-hardware'
OLD = MOD / 'docs/evidence/1019-baseline'
RUN = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T092935Z')
OUT = MOD / 'docs/evidence/1019-analysis/rc3-machine-operational-constraints-report-v1.json'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def ref(p):
    p = Path(p)
    return {'path': p.relative_to(MOD).as_posix() if p.is_relative_to(MOD) else str(p),
            'sha256': sha(p)}


def native(name, folder=BASE):
    save = folder / (name + '.sav')
    audit = read(save.with_suffix('.audit.json'))
    assert sha(save) == audit['save_sha256']
    with zipfile.ZipFile(save) as z:
        data = z.read('gamestate')
        assert z.testzip() is None
    assert hashlib.sha256(data).hexdigest() == audit['gamestate_sha256']
    roots = {k: v for k, v, obj in a.fields(data.decode('utf-8-sig')) if obj}
    country = a.block(roots['country'], '0')
    fleets = {k: v for k, v, obj in a.fields(roots['fleet']) if obj}
    owned_text = a.block(a.block(country, 'fleets_manager'), 'owned_fleets')
    owned = set(re.findall(r'\bfleet\s*=\s*(\d+)', owned_text))
    fleet_records = {}
    own_ships = {}
    ships = {k: v for k, v, obj in a.fields(roots['ships']) if obj}
    for identity in sorted(owned, key=int):
        body = fleets[identity]
        fleet_records[identity] = {'native': a.scalars(body),
                                   'settings': a.scalars(a.block(body, 'settings')),
                                   'timed_modifier': ins.modifiers(body),
                                   'ships': a.ids(a.block(body, 'ships'))}
        for sid in fleet_records[identity]['ships']:
            sb = ships[str(sid)]
            own_ships[str(sid)] = {'native': a.scalars(sb),
                                    'name': a.scalars(a.block(sb, 'name')),
                                    'timed_modifier': ins.modifiers(sb)}
    jobs = {k: {'native': a.scalars(v), 'raw': v} for k, v, obj in a.fields(roots['pop_jobs'])
            if obj and k in audit['pop_jobs']}
    assert {k: v['native'] for k, v in jobs.items()} == audit['pop_jobs']
    return {'save': ref(save), 'audit': ref(save.with_suffix('.audit.json')),
            'date': audit['date'], 'country': audit['countries']['0'],
            'country_timed_modifier': ins.modifiers(country),
            'colony_records': audit['colonies'], 'pop_groups': audit['pop_groups'],
            'jobs': jobs, 'owned_fleets': fleet_records, 'owned_ships': own_ships}


def frame(name):
    p = BASE / (name + '.ocr.json')
    o = read(p)
    image = BASE / Path(o['image']).name
    assert sha(image) == o['image_sha256']
    assert o['resolution'] == [1024, 768]
    return o, {'ocr': ref(p), 'image': ref(image)}


def click_binding(stage, frame_name, label, offset=(0, 0)):
    action = read(BASE / (stage + '.action.json'))
    o, references = frame(frame_name)
    rows = [r for r in o['rows'] if r['text'] == label and r['score'] >= .8]
    assert len(rows) == 1, (stage, label)
    row = rows[0]
    center = [round(sum(p[i] for p in row['box']) / 4) + offset[i] for i in range(2)]
    assert center == action['client_point'], (stage, center, action)
    assert [action['client_point'][i] + o['client_origin'][i] for i in range(2)] == action['desktop_point']
    return {'action': ref(BASE / (stage + '.action.json')), **references,
            'native_label': label, 'row': row, 'offset': list(offset), 'matched': True}


def main():
    if OUT.exists():
        raise RuntimeError('refusing to overwrite report')
    index = read(BASE / 'archive-index-v1.json')
    assert all(sha(BASE / e['path']) == e['sha256'] for e in index['files'])
    prefixes = ['fm-clean-reload-', 'fmm00reload-', 'fm-monthly-auto-', 'fmyearui-']
    prefixes += [f'fmm{i:02}-' for i in range(1, 13)]
    paths = sorted(BASE.glob('*.action.json'))
    scoped = [p for p in paths if any(p.name.startswith(x) for x in prefixes)]
    excluded = [ref(p) for p in paths if p not in scoped]
    actions = [{'file': ref(p), 'record': read(p)} for p in scoped]
    extra_names = ['press-1792403782981.json', 'press-1792404763425.json']
    extras = [{'file': ref(RUN / n), 'record': read(RUN / n)} for n in extra_names]
    assert all(x['record']['action'] == 'press' and x['record']['keys'] == ['ctrl', 'a'] and
               x['record']['repeat'] == 1 for x in extras)
    for x, stage in zip(extras, ['fmm00reload', 'fmyearui']):
        t = datetime.fromisoformat(x['record']['at_utc'])
        typed = datetime.fromisoformat(read(BASE / (stage + '-name.action.json'))['typed_at_utc'])
        assert 0 < (typed-t).total_seconds() < 2
        x['name_edit_stage'] = stage
    typed = [x for x in actions if x['record'].get('action') == 'type_text']
    submitted = [x for x in typed if x['record']['submitted']]
    assert len(submitted) == 12 and all(x['record']['text'] == 'fast_forward 30' for x in submitted)
    assert [(x['record']['stage'], x['record']['text']) for x in typed if not x['record']['submitted']] == [
        ('fmm00reload-name', 'fmm00reload'), ('fmyearui-name', 'fmyearui')]
    scans = [x for x in actions if x['record'].get('action') == 'press_scan_code']
    assert set(x['record']['scan_code'] for x in scans) == {1, 28, 41, 88}
    assert Counter(x['record']['scan_code'] for x in scans) == {88: 54, 1: 5, 41: 2, 28: 12}
    bindings = [click_binding('fm-clean-reload-open', 'fm-clean-reload-menu-1', '\u8f7d\u5165\u6e38\u620f'),
                click_binding('fm-clean-reload-row', 'fm-clean-reload-load-window', 'fmm00.sav'),
                click_binding('fm-clean-reload-load', 'fm-clean-reload-load-window', '\u8bfb\u53d6\u5b58\u6863')]
    for s in ['fmm00reload', 'fmyearui']:
        bindings += [click_binding(s+'-open-save', s+'-menu-1', '\u4fdd\u5b58\u6e38\u620f'),
                     click_binding(s+'-name-field', s+'-save-dialog', '\u4fdd\u5b58', (-240, 0)),
                     click_binding(s+'-save-click', s+'-save-dialog', '\u4fdd\u5b58')]
    bindings.append(click_binding('fm-monthly-auto-queen-0-ack', 'fm-monthly-auto-queen-0', '\u738b\u5ea7\u4e4b\u5916\uff0c\u7686\u53ef\u541e\u566c\u3002'))
    for i in range(1, 13):
        stem = f'fmm{i:02}-auto'
        stage = stem+'-focus-console-input'
        fn = stem+'-console-ready' if (BASE/(stem+'-console-ready.ocr.json')).exists() else stem+'-console-state'
        o, refs = frame(fn)
        markers = [r for r in o['rows'] if re.fullmatch(r'Fast Forwarded \d+ Days', r['text']) or
                   any(x in r['text'] for x in ['\u4f7f\u7528\u4efb\u4f55\u8c03\u8bd5\u547d\u4ee4', 'Executing effect script.', 'Effect description:', 'You are now playing '])]
        action = read(BASE/(stage+'.action.json'))
        assert markers and action['client_point'] == [120, 322]
        assert [action['client_point'][j]+o['client_origin'][j] for j in range(2)] == action['desktop_point']
        bindings.append({'action': ref(BASE/(stage+'.action.json')), **refs,
                         'native_console_markers': markers, 'matched': True,
                         'basis': 'runtime_single_homeworld.py:167-179; console.gui tested 1024x768 edit geometry'})
    point_paths = {x['file']['path'] for x in actions if 'client_point' in x['record']}
    assert point_paths == {x['action']['path'] for x in bindings}
    states = [native(n) for n in ['fmm00reload']+[f'fmm{i:02}' for i in range(1, 13)]+['fmyearui']]
    print('native states verified', len(states), flush=True)
    original = native('bmm00', OLD)
    monthly = []
    for before, after in zip(states[:12], states[1:13]):
        cb = after['country']['budget_categories']['current_month']
        stock0, stock1 = before['country']['stockpile'], after['country']['stockpile']
        resources = sorted(set(stock0) | set(stock1) | {r for d in ['income', 'expenses'] for cats in cb[d].values() for r in cats})
        row = {'date': after['date'], 'save': after['save'], 'resources': {}}
        for resource in resources:
            inc = sum(cat.get(resource, 0) for cat in cb['income'].values())
            exp = sum(cat.get(resource, 0) for cat in cb['expenses'].values())
            delta = stock1.get(resource, 0)-stock0.get(resource, 0)
            residual = delta-(inc-exp)
            assert abs(residual) < 1e-8, (after['date'], resource, residual)
            row['resources'][resource] = {'before': stock0.get(resource, 0), 'after': stock1.get(resource, 0),
                'native_income': inc, 'native_expenses': exp, 'stock_delta': delta, 'residual': residual}
        row['native_income_categories'] = cb['income']
        row['native_expense_categories'] = cb['expenses']
        monthly.append(row)
    initial_ids = set(states[0]['owned_ships'])
    target_ids = {'1', '2', '3', '4', '5', '997'}
    assert target_ids <= initial_ids
    for s in states:
        assert set(s['owned_ships']) == initial_ids
        for sid in initial_ids:
            assert s['owned_ships'][sid]['native']['fleet'] == states[0]['owned_ships'][sid]['native']['fleet']
            assert s['owned_ships'][sid]['name'] == states[0]['owned_ships'][sid]['name']
        assert 'eep_mothership' not in [x['modifier'] for x in s['country_timed_modifier']['items']]
        assert s['country']['stockpile'].get('energy', 0) >= 200
        assert s['jobs'].keys() == states[0]['jobs'].keys()
        for identity, j in s['jobs'].items():
            v, first = j['native'], states[0]['jobs'][identity]['native']
            for field in ['type', 'planet', 'max_workforce', 'workforce_limit', 'automated_workforce_limit']:
                assert v[field] == first[field], (s['date'], identity, field)
            assert v['workforce_limit'] == v['max_workforce']
            assert v['automated_workforce_limit'] == (v['max_workforce']-1 if v['max_workforce'] >= 0 else -1)
            assert v['workforce'] > 0 if v['max_workforce'] >= 0 else v['workforce'] == -1
    core0 = next(x for x in original['colony_records'].values() if x['actual_pop_sum'] == 4800)
    core1 = states[0]['colony_records']['0']
    assert core0['actual_pop_sum'] == core1['actual_pop_sum'] == 4800
    assert sorted(original['pop_groups'][str(i)]['size'] for i in core0['pop_groups']) == [2100, 2700]
    assert sorted(states[0]['pop_groups'][str(i)]['size'] for i in core1['pop_groups']) == [2100, 2700]
    new_mod = HW/'copied_mod/common/static_modifiers/eep_modifiers.txt'
    old_manifest = read(OLD/'manifest.json')
    old_mod = Path(old_manifest['copied_mod'])/'common/static_modifiers/eep_modifiers.txt'
    old_expected = next(x['sha256'] for x in old_manifest['repository_mod_files'] if x['path'] == 'common/static_modifiers/eep_modifiers.txt')
    assert sha(old_mod) == old_expected
    new_block = a.scalars(a.block(new_mod.read_text(encoding='utf-8-sig'), 'eep_mothership'))
    old_block = a.scalars(a.block(old_mod.read_text(encoding='utf-8-sig'), 'eep_mothership'))
    upkeep = {k: v for k, v in new_block.items() if 'upkeep' in k or 'maintenance' in k}
    assert upkeep == {k: v for k, v in old_block.items() if 'upkeep' in k or 'maintenance' in k}
    assert upkeep == {'ships_upkeep_mult': -1, 'starbases_upkeep_mult': -1}
    upkeep_source_hits = []
    for p in (HW/'copied_mod').rglob('*.txt'):
        for n, line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(), 1):
            if re.search(r'\b\w*(?:upkeep|maintenance)\w*\s*=', line.split('#')[0]):
                upkeep_source_hits.append({'file': ref(p), 'line': n, 'text': line})
    assert len(upkeep_source_hits) == 2
    for s in states:
        for fid, f in s['owned_fleets'].items():
            names = [m['modifier'] for m in f['timed_modifier']['items']]
            assert ('eep_mothership' in names) == (fid == '159')
    sources = [MOD/'tools/runtime_1019.py', MOD/'tools/runtime_single_homeworld.py',
        MOD/'tools/runtime_1015.py', MOD/'tools/runtime.py', MOD.parent/'tools/stellaris_acceptance.py',
        Path('C:/SteamLibrary/steamapps/common/Stellaris/common/pop_jobs/04_gestalt_jobs.txt'), old_mod,
        new_mod, HW/'copied_mod/common/scripted_effects/eep_startup_effects.txt']
    claims = {
        'no_resource_injection': {'value': True, 'scope': 'Recorded clean-load/year-UI actions plus all-resource monthly native ledger closure; no unrecorded-input guarantee.'},
        'no_trade_subsidy': {'value': True, 'scope': 'No recorded market/trade/gift/resource-subsidy operation; normal native logistics trade production remains included.'},
        'no_job_closure': {'value': True, 'scope': 'No job-management action; all finite native jobs retain max limits and positive workforce at all 14 checkpoints.'},
        'no_ship_disband': {'value': True, 'scope': 'No recorded disband action; all initially owned ship IDs, fleet IDs and names retained at all 14 checkpoints.'},
        'population_preserved': {'value': True, 'scope': 'Same-preset old native core 4800=RC3 core 4800; excludes removed gift colony100. Not a separate pure-vanilla fixture or constant population through year.'},
        'normal_upkeep': {'value': True, 'scope': 'Nonzero native normal costs each month; only existing Mother-fleet discounts retained at equal values; no newly global free upkeep.'}}
    for row in monthly:
        assert all(sum(row['native_expense_categories'][cat].values()) > 0 for cat in ['ships', 'ship_components', 'planet_buildings', 'planet_districts'])
    result = {'schema': 'eep.1019.machine-operational-constraints.v1', 'status': 'PASS_SCOPED',
        'run_id': index['run_id'], 'production_tree_sha256': index['production_tree_sha256'],
        'claims': claims, 'archive_v1': ref(BASE/'archive-index-v1.json'),
        'action_chain': {'archived_action_file_count': len(paths), 'scoped_action_file_count': len(actions),
            'supplemental_low_level_press_count': len(extras), 'total_scoped_input_records': len(actions)+len(extras),
            'action_counts': dict(Counter(x['record'].get('action', 'native_point_click') for x in actions)),
            'scan_code_counts': dict(Counter(x['record']['scan_code'] for x in scans)),
            'actions': actions, 'low_level_presses': extras, 'excluded_preclean_actions': excluded,
            'click_bindings': bindings, 'console_history_note': 'Screens retain previous hardware text after native load. New submitted input records are exactly twelve fast_forward 30; clean SAV has no probe/tier contamination.'},
        'monthly_all_resource_ledger': monthly, 'native_states': states,
        'population_comparison': {'baseline_native_save': original['save'], 'baseline_native_audit': original['audit'],
            'baseline_core': core0, 'candidate_core': core1, 'baseline_groups': original['pop_groups'],
            'baseline_country_total': original['country']['native']['num_sapient_pops'],
            'candidate_country_total': states[0]['country']['native']['num_sapient_pops']},
        'upkeep_source_comparison': {'old_file': ref(old_mod), 'new_file': ref(new_mod),
            'unchanged_mother_discount_values': upkeep, 'all_candidate_upkeep_assignment_hits': upkeep_source_hits,
            'application_scope': 'eep_startup_mothership.create_fleet.effect adds eep_mothership to fleet159; country has native game_start only, not eep_mothership.'},
        'source_files': [ref(p) for p in sources], 'collector': ref(Path(__file__)),
        'limitations': ['Input records and screenshots cover the executed harness path, not a continuous operating-system input monitor.',
            'Monthly stock closure rules out unexplained net credit at sampled boundaries, not hypothetical equal offsetting unrecorded credit/debit.',
            'No trade subsidy does not mean no native trade income; logistics_drone has native planet_traders trade production and upkeep.',
            'Job fields prove no saved finite limit reduction; raw jobs retained without inventing an undocumented manual-suppression flag.',
            'Stable monthly ship identities and recorded actions do not claim observation of every intervening simulation tick.',
            'Same-preset old core is a provenance-verified Mod baseline, not a newly executed pure-vanilla control.',
            'Hive and later PK branch excluded; whole release and unrelated strict comparisons remain pending/FAIL as previously recorded.'],
        'created_at_utc': datetime.now(timezone.utc).isoformat()}
    with OUT.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'status': result['status'], 'claims': list(claims), 'sha256': sha(OUT), 'path': str(OUT)}))


if __name__ == '__main__':
    main()
