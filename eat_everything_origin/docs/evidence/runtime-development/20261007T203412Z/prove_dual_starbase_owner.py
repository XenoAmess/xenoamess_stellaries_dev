import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q
run = Path('_runtime/heart-of-devouring/runs/20261007T203412Z')
stages = [('rc7-dual-separate-system-source-starbase-prepared', 0), ('rc7-dual-separate-starbase-source-owner33-native', 33), ('rc7-dual-separate-first-month-stable-owner33-native', 33), ('rc7-dual-separate-new33-settled-old0-isolated-native', 33)]
checks = []
records = []
for name, expected in stages:
    raw = (run / (name + '.sav')).read_bytes()
    with zipfile.ZipFile(run / (name + '.sav')) as archive:
        roots = {key: value for key, value, obj in q.fields(archive.read('gamestate').decode('utf-8-sig')) if obj}
    base = q.scalars(q.block(q.block(roots['starbase_mgr'], 'starbases'), '22'))
    station = str(base['station'])
    ship = q.scalars(q.block(roots['ships'], station))
    fleet = ship['fleet']
    owners = []
    for country, value, obj in q.fields(roots['country']):
        if obj:
            fleets = {int(identity) for identity in re.findall(r'fleet=(\d+)', q.block(q.block(value, 'fleets_manager'), 'owned_fleets'))}
            if fleet in fleets:
                owners.append(int(country))
    actual = {'base22_level': base['level'], 'station': int(station), 'fleet': fleet, 'actual_owned_fleet_countries': owners}
    checks.append({'check': name + ':actual_starbase_fleet_owner', 'status': 'PASS' if owners == [expected] and base['level'] == 'starbase_level_outpost' else 'FAIL', 'actual': actual, 'expected_owner': expected})
    records.append({'save': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'native': actual})
result = {'status': 'PASS' if all(value['status'] == 'PASS' for value in checks) else 'FAIL', 'scope': 'Read-only native outpost22 ownership via actual station ship, fleet, and country owned_fleets references. Separate system154 controlled fixture; not natural colonization.', 'version': '0.2.0-rc.7', 'checks': checks, 'records': records}
out = run / 'rc7-dual-separate-outpost-native-owner-proof.json'
assert not out.exists()
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result))
