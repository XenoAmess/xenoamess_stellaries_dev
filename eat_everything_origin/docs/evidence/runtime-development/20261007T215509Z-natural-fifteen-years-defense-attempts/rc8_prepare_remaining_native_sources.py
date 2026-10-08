import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
user = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261007T215509Z')
assert not (run / Path(__file__).name).exists()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
sources = {
    'focus-base23': Path('_runtime/heart-of-devouring/runs/20261006T232907Z/hive-scorched-natural23-source-ready.sav'),
    'fleet2-war80': Path('_runtime/heart-of-devouring/runs/20261007T031421Z/native-psi80-natural.sav'),
}
receipts = []
for alias, source in sources.items():
    audit = json.loads(source.with_suffix('.audit.json').read_text(encoding='utf-8'))
    c = audit['countries']['0']
    assert 'civic_hive_scorched_earth' in c['government']
    assert 'origin_heart_of_devouring' in c['government']
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == audit['save_sha256']
    with zipfile.ZipFile(source) as archive:
        native = archive.read('gamestate').decode('utf-8-sig')
    details = {}
    if alias == 'focus-base23':
        assert digest == 'ce4dc4f2c848ebbabeaa365f8531ba480774d52a25ee7337d04fb52a04da2c6f'
        assert audit['colonies']['24']['actual_pop_sum'] == 69
        coordinates = {}
        systems = {}
        for identity in ['1', '84']:
            p = q.block(q.block(q.block(native, 'planets'), 'planet'), identity)
            coordinates[identity] = q.scalars(q.block(p, 'coordinate'))
            gid = str(coordinates[identity]['origin'])
            system = q.block(q.block(native, 'galactic_object'), gid)
            planets = [q.unquote(v) for k, v, obj in q.fields(system) if k == 'planet' and not obj]
            assert int(identity) in planets
            systems[gid] = {'native': q.scalars(system), 'name': q.scalars(q.block(system, 'name')),
                            'planet_ids': planets}
        assert coordinates['1']['origin'] != coordinates['84']['origin']
        aliens = []
        countries = q.block(native, 'country')
        species = q.block(native, 'species_db')
        for identity, value, obj in q.fields(countries):
            if not obj or identity == '0':
                continue
            data = q.scalars(value)
            government = q.scalars(q.block(value, 'government'))
            if data.get('type') != 'default' or government.get('authority') in ['auth_hive_mind', 'auth_machine_intelligence']:
                continue
            sid = str(data.get('founder_species_ref'))
            s = q.block(species, sid)
            klass = q.scalars(s).get('class')
            traits = [q.unquote(v) for k, v, b in q.fields(q.block(s, 'traits')) if k == 'trait' and not b]
            if klass in ['MAM', 'HUM', 'REP', 'AVI', 'MOL', 'ART', 'PLANT', 'FUN'] and 'trait_hive_mind' not in traits:
                aliens.append({'country_id': int(identity), 'species_id': int(sid), 'class': klass, 'traits': traits})
        assert aliens
        details = {'coordinates': coordinates, 'systems': systems,
                   'actual_source_population': 69, 'required_formal_seed_topup': 31,
                   'ordinary_organic_alien_candidates': aliens}
    else:
        country = q.block(q.block(native, 'country'), '0')
        crisis = q.scalars(q.block(country, 'crisis_progression'))
        flags = q.scalars(q.block(country, 'flags'))
        assert crisis['level'] == 'crisis_level_1'
        assert c['stockpile']['menace'] == 135
        assert 'crisis_special_project_1_complete' in flags and 'eep_fleet_notice' not in flags
        details = {'crisis_progression': q.block(country, 'crisis_progression'),
                   'native_project1_complete': flags['crisis_special_project_1_complete'],
                   'first_fleet_notice_present': False, 'actual_menace': 135}
    destination = user / 'save games' / 'acceptance-fixtures' / (alias + '.sav')
    assert not destination.exists()
    shutil.copyfile(source, destination)
    assert hashlib.sha256(destination.read_bytes()).hexdigest() == digest
    receipts.append({'alias': alias, 'original_source': str(source.resolve()), 'copied': str(destination),
                     'source_sha256': digest, 'source_bytes': source.stat().st_size,
                     'actual_date': audit['date'], 'country0_eep_ledger': c['variables'], 'preflight': details})
out = run / 'rc8-remaining-natural-source-original-byte-preflight.json'
assert not out.exists()
out.write_text(json.dumps({'status': 'SOURCE_PREFLIGHT_ONLY',
                           'scope': 'Short-name file copies and native source identity; no GUI input, no runtime acceptance.',
                           'sources': receipts}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'SOURCE_PREFLIGHT_ONLY', 'sources': [
    {k: row[k] for k in ['alias', 'source_sha256', 'actual_date', 'preflight']} for row in receipts]}, ensure_ascii=True))
