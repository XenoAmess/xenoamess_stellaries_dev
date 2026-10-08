"""Native completion acknowledgement/reload; no event or resource injection."""
import json
import logging
import shutil
import sys
from pathlib import Path

operation, start, stage = sys.argv[1:]
assert operation in ('ack', 'reload')
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--vanilla']
import runtime as r
from postrelease_vanilla_raw_source import inspect

logging.disable(logging.INFO)
h = r.harness
run, user, m = h.load_run()
assert m['enabled_mods'] == []
for name in (Path(__file__).name, 'postrelease_vanilla_raw_source.py'):
    src = Path('_runtime/heart-of-devouring') / name
    dest = run / name
    if not dest.exists():
        shutil.copyfile(src, dest)
    assert src.read_bytes() == dest.read_bytes()
b = json.loads((run / (start + '.audit.json')).read_text(encoding='utf-8'))
eb = (user / 'logs/error.log').read_bytes()
(run / (stage + '-error-before.log')).write_bytes(eb)
alias_path = None
if operation == 'ack':
    f = r.gpu_capture(stage + '-actual-completion-window')
    rows = [row for row in f['rows'] if h.normalized(row['text']) ==
            h.normalized('\u6211\u4eec\u8fd8\u662f\u5f88\u997f\u3002')
            and row['score'] >= .8]
    assert len(rows) == 1, 'Native completion option not uniquely visible'
    row = rows[0]
    import time
    x = round(sum(p[0] for p in row['box']) / 4)
    y = round(sum(p[1] for p in row['box']) / 4)
    hwnd = h.focus_pid(int(h.process_record(run)['pid']))
    assert h.win32gui.GetForegroundWindow() == hwnd
    desktop = h.win32gui.ClientToScreen(hwnd, (x, y))
    old_pause = h.pyautogui.PAUSE
    started = time.monotonic_ns()
    try:
        h.pyautogui.PAUSE = 0
        h.pyautogui.click(*desktop)
        h.win32api.keybd_event(0, 0x01, 0x0008, 0)
        h.win32api.keybd_event(0, 0x01, 0x0008 | h.win32con.KEYEVENTF_KEYUP, 0)
    finally:
        h.pyautogui.PAUSE = old_pause
    h.write_json(run / (stage + '-click-and-native-menu.action.json'),
                 {'action': 'physical_click_then_physical_escape', 'client_point': [x, y],
                  'desktop_point': list(desktop), 'foreground_hwnd': hwnd,
                  'source_image_sha256': f['image_sha256'],
                  'elapsed_ns': time.monotonic_ns() - started})
    r.gpu_capture(stage + '-native-acknowledged-menu')
else:
    alias = 'vanilla-stable' if 'stable' in stage else 'vanilla-end'
    alias_path = user / 'save games/acceptance-fixtures' / (alias + '.sav')
    if not alias_path.exists():
        alias_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(run / (start + '.sav'), alias_path)
    assert h.sha256(alias_path) == b['save_sha256']
    r.native_load(alias, stage + '-load')
a = r.native_save(stage, b['date'], (0,))
cb, ca = b['countries']['0'], a['countries']['0']
checks = {'same_date': b['date'] == a['date'],
          'all_stock_same': cb['stockpile'] == ca['stockpile'],
          'all_pop_groups_same': b['pop_groups'] == a['pop_groups'],
          'all_pop_jobs_same': b['pop_jobs'] == a['pop_jobs'],
          'technology_same': cb['completed_technologies'] == ca['completed_technologies'],
          'research_queues_same': cb['research_queues'] == ca['research_queues'],
          'traditions_same': cb['traditions'] == ca['traditions'],
          'AP_empty': cb['ascension_perks'] == ca['ascension_perks'] == [],
          'no_EEP_variables': cb['variables'] == ca['variables'] == {},
          'no_EEP_flags': cb['flags'] == ca['flags'] == {}}
for key in ('colonies', 'planets', 'districts', 'deposits', 'situations',
            'event_targets', 'species'):
    checks[key + '_same'] = b[key] == a[key]
if operation == 'ack':
    checks.pop('situations_same')
    old = b['situations'].get('11', {})
    new = a['situations'].get('11', {})
    checks['expected_native_terminal_transition'] = old.get('progress') == 1000 and old.get('type') == 'situation_terravore_consume_planet' and (not new or new.get('killed') == 'yes')
    checks['other_situations_same'] = {k: v for k, v in b['situations'].items() if k != '11'} == {k: v for k, v in a['situations'].items() if k != '11'}
raw_before, raw_after = inspect(run / (start + '.sav')), inspect(run / (stage + '.sav'))
checks.update({'raw_source_same': raw_before['source'] == raw_after['source'],
               'native_shattered': raw_after['source']['planet_class'] == 'pc_shattered',
               'source_unowned': raw_after['source'].get('owner', 4294967295) in (None, 4294967295),
               'no_EEP_origin_or_probe': not raw_after['EEP_probe_reference'] and not raw_after['EEP_origin_reference']})
ea = (user / 'logs/error.log').read_bytes()
(run / (stage + '-error-after.log')).write_bytes(ea)
checks['no_new_errors'] = eb == ea
changes = {key: {'before': b[key], 'after': a[key]} for key in
           ('colonies', 'planets', 'districts', 'deposits', 'situations',
            'pop_groups', 'pop_jobs', 'event_targets', 'species') if b[key] != a[key]}
proof = {'status': 'PASS_SCOPED' if all(checks.values()) else 'FAIL',
         'operation': operation, 'checks': checks,
         'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'],
         'alias_sha256': h.sha256(alias_path) if alias_path else None,
         'raw_before': raw_before, 'raw_after': raw_after, 'collection_changes': changes,
         'scope': 'Actual no-mod native completion confirmation or original-byte reload only; no full Mod route acceptance.'}
h.write_json(run / (stage + '-proof.json'), proof)
print(json.dumps({k: v for k, v in proof.items() if k not in ('raw_before', 'raw_after', 'collection_changes')}), flush=True)
assert all(checks.values()), 'Original FAIL and all native collections retained'
