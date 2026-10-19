"""Capture local primary-source excerpts without modifying any input."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
NATIVE = Path('C:/SteamLibrary/steamapps/common/Stellaris')
FROZEN = REPO / 'eat_everything_origin/docs/evidence/1019-rc3-final-logs'


def digest(data):
    return sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


manifest_raw = (FROZEN / 'manifest.json').read_bytes()
manifest = json.loads(manifest_raw)
MOD = Path(manifest['repository_mod'])
expected = {item['path']: item['sha256'] for item in manifest['repository_mod_files']}
sources = []
numbered = []


def capture(kind, relative, ranges):
    base = {'native': NATIVE, 'engine': FROZEN / 'logs/script_documentation',
            'observed': FROZEN, 'rc3_mod': MOD}[kind]
    path = base / relative
    raw = path.read_bytes()
    if kind == 'rc3_mod':
        assert digest(raw) == expected[relative], relative
    lines = raw.splitlines(keepends=True)
    item = {'kind': kind, 'relative_path': relative, 'source_path': str(path),
            'source_bytes': len(raw), 'source_sha256': digest(raw),
            'source_line_count': len(lines), 'excerpts': []}
    for start, end in ranges:
        assert 1 <= start <= end <= len(lines), (relative, start, end)
        content = b''.join(lines[start - 1:end])
        relout = f'excerpts/{kind}/{relative.replace(chr(47), chr(95))}.L{start}-L{end}.txt'
        dest = OUT / relout
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
        item['excerpts'].append({'start_line': start, 'end_line': end,
                                 'path': relout, 'bytes': len(content), 'sha256': digest(content)})
        numbered.append(f'FILE {path}\nSHA256 {digest(raw)}\nLINES {start}-{end}\n')
        numbered.extend(f'{n}: {lines[n - 1].decode("utf-8-sig").rstrip(chr(13) + chr(10))}\n'
                        for n in range(start, end + 1))
        numbered.append('\n')
    assert digest(path.read_bytes()) == item['source_sha256'], str(path)
    sources.append(item)


capture('native', 'events/nomads_events_1.txt', [(711,835), (2256,2325)])
capture('native', 'common/on_actions/00_on_actions.txt', [(1337,1358), (2627,2647), (4496,4515)])
capture('native', 'common/on_actions/01_planet_destruction.txt', [(1,34), (56,61)])
capture('native', 'events/planet_destruction_events.txt', [(1,47), (264,339), (784,795), (957,983), (2267,2273), (2484,2512)])
capture('native', 'common/special_projects/06_projects_nomads.txt', [(81,90)])
capture('native', 'common/ship_sizes/00_waystations.txt', [(64,70), (175,181), (289,295)])
capture('engine', 'effects.log', [(409,434), (1638,1640), (2317,2319)])
capture('engine', 'scopes.log', [(58,80), (98,104)])
capture('engine', 'triggers.log', [(703,705)])
capture('observed', 'logs/error.log', [(28,42)])
capture('observed', 'logs/game.log', [(1,1)])
capture('rc3_mod', 'common/on_actions/eep_on_actions.txt', [(1,8)])
capture('rc3_mod', 'events/eep_planet_killer_events.txt', [(1,10)])
capture('rc3_mod', 'common/scripted_effects/eep_planet_killer_effects.txt', [(1,35)])
capture('rc3_mod', 'common/scripted_effects/eep_settlement_effects.txt', [(1,27), (102,136)])


def search(label, pattern, locations, globs=None):
    command = ['rg', '--json', '--hidden', '--no-ignore', '-e', pattern]
    for glob in globs or []:
        command += ['-g', glob]
    command += [str(p) for p in locations]
    result = subprocess.run(command, capture_output=True, check=False)
    assert result.returncode in (0, 1), result.stderr.decode('utf-8', errors='replace')
    matches = []
    for line in result.stdout.decode('utf-8').splitlines():
        record = json.loads(line)
        if record['type'] == 'match':
            data = record['data']
            matches.append({'path': data['path']['text'], 'line': data['line_number'],
                            'text': data['lines']['text'].rstrip('\r\n')})
    return {'label': label, 'argv': command, 'exit_code': result.returncode,
            'stderr': result.stderr.decode('utf-8'), 'match_count': len(matches), 'matches': matches}


globs = ['*.txt', '*.log', '*.gui', '*.gfx']
searches = [
    search('all_literal_native_nomads94', r'\bnomads\.94\b', [NATIVE], globs),
    search('native_destroy_planet_assignment', r'\bdestroy_planet\s*=', [NATIVE], globs),
    search('engine_destroy_planet_effect_entry', r'^destroy_planet\s*[-=]', [FROZEN / 'logs/script_documentation']),
    search('rc3_mod_nomads94_or_global_hooks', r'\bnomads\.94\b|\bon_war_ended\b|\bon_colony_destroyed\b|\bon_becoming_subject\b', [MOD], ['*.txt']),
]
assert searches[0]['match_count'] == 7
assert all(item['match_count'] == 0 for item in searches[1:])
inventory_command = ['rg', '--files', '--hidden', '--no-ignore']
for glob in globs:
    inventory_command += ['-g', glob]
inventory_command += [str(NATIVE)]
inventory = subprocess.run(inventory_command, capture_output=True, check=True).stdout
(OUT / 'search-inventory.txt').write_bytes(inventory)
write_json(OUT / 'search-results.json', {'search_scope': 'Loose files only; binary/internal engine dispatch not searched.',
           'inventory_argv': inventory_command, 'inventory_file_count': len(inventory.splitlines()),
           'inventory_sha256': digest(inventory), 'searches': searches})
(OUT / 'excerpts-numbered.txt').write_text(''.join(numbered), encoding='utf-8')
write_json(OUT / 'sources.json', {'schema': 'xenoamess.stellaris.native-semantics.v1',
    'captured_at_utc': datetime.now(timezone.utc).isoformat(),
    'run_id': manifest['run_id'], 'game_exe_sha256_from_run_manifest': manifest['game_exe_sha256'],
    'run_manifest_sha256': digest(manifest_raw), 'rc3_mod_tree_sha256': manifest['repository_mod_tree_sha256'],
    'mode': 'Static local primary-source inspection only. No UI, game mutation, or final acceptance.',
    'sources': sources})
print(json.dumps({'sources': len(sources), 'excerpts': sum(len(item['excerpts']) for item in sources),
                  'native_literal_references': searches[0]['match_count'],
                  'destroy_planet_assignments': searches[1]['match_count'],
                  'inventory_file_count': len(inventory.splitlines())}))
