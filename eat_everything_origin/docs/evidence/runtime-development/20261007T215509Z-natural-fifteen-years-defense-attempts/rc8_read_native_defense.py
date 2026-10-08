"""Read actual movement, ownership and route records; never send game input."""
import json
from pathlib import Path
import shutil
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
copy = run / Path(__file__).name
if not copy.exists():
    shutil.copyfile(Path(__file__), copy)
assert copy.read_bytes() == Path(__file__).read_bytes()
stage = sys.argv[1]
path = run / (stage + '.sav')
audit = json.loads(path.with_suffix('.audit.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(path) as z:
    native = z.read('gamestate').decode('utf-8-sig')
roots = {k: v for k, v, obj in q.fields(native) if obj and k in ['fleet', 'country', 'galactic_object', 'player']}
fleet_ids = ['0', '1273', '83887397']
fleets = {}
for k, v, obj in q.fields(roots['fleet']):
    if obj and k in fleet_ids:
        fleets[k] = {a: b if block else q.unquote(b) for a, b, block in q.fields(v) if a not in ['name', 'ships', 'combat']}
ownership = {}
for cid, country, obj in q.fields(roots['country']):
    if not obj:
        continue
    own = q.block(q.block(country, 'fleets_manager'), 'owned_fleets')
    iterator = iter(q.tokens(own))
    for token, left, right in iterator:
        assert token == '{'
        start = right
        depth = 1
        for token, left, right in iterator:
            depth += (token == '{') - (token == '}')
            if depth == 0:
                record = q.scalars(own[start:left])
                if str(record.get('fleet')) in fleet_ids:
                    ownership.setdefault(str(record['fleet']), []).append({'country': int(cid), **record})
                break
systems = {k: v for k, v, obj in q.fields(roots['galactic_object']) if obj and k in ['5', '17']}
result = {'status': 'READ_ONLY_NATIVE_RECORDS', 'date': audit['date'], 'save_sha256': audit['save_sha256'],
          'fleets': fleets, 'ownership': ownership, 'systems': systems, 'player': roots.get('player'),
          'mother': audit['planets']['1'], 'mother_population': audit['colonies']['0']['actual_pop_sum'],
          'eep_ledger': {k: audit['countries']['0']['variables'][k] for k in ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds']}}
destination = run / (stage + '-native-defense-records.json')
assert not destination.exists()
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=True))
