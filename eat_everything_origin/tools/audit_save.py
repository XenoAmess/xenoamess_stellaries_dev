"""Read native Stellaris saves without editing them or assigning acceptance status."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

TOKEN = re.compile(r'\s+|#[^\n]*|"(?:\\.|[^"\\])*"|[{}=]|[^\s{}=\"]+')


def tokens(text):
    for match in TOKEN.finditer(text):
        value = match.group()
        if value.isspace() or value.startswith('#'):
            continue
        yield value, match.start(), match.end()


def fields(text):
    """Yield only direct named fields; keep duplicate keys and skip nested values."""
    iterator = iter(tokens(text))
    for key, _, _ in iterator:
        if key in ('{', '}', '='):
            raise ValueError('unexpected delimiter at field boundary')
        operator = next(iterator, None)
        if operator is None or operator[0] != '=':
            raise ValueError('expected equals after field: ' + key)
        value = next(iterator, None)
        if value is None:
            raise ValueError('missing value: ' + key)
        if value[0] == '{':
            depth = 1
            start = value[2]
            end = None
            for token, before, _ in iterator:
                if token == '{':
                    depth += 1
                elif token == '}':
                    depth -= 1
                    if depth == 0:
                        end = before
                        break
            if end is None:
                raise ValueError('unclosed object: ' + key)
            yield key, text[start:end], True
        elif value[0] in ('}', '='):
            raise ValueError('invalid scalar: ' + key)
        else:
            yield key, value[0], False


def unquote(value):
    if value.startswith('"'):
        return value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
    if re.fullmatch(r'-?\d+', value):
        return int(value)
    if re.fullmatch(r'-?\d+\.\d+', value):
        return float(value)
    return value


def scalars(text):
    return {key: unquote(value) for key, value, block in fields(text) if not block}


def block(text, key):
    return next((value for name, value, obj in fields(text) if name == key and obj), '')


def ids(text):
    return [int(t) for t, _, _ in tokens(text) if re.fullmatch(r'\d+', t)]


def audit(path):
    raw = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        native = archive.read('gamestate')
    text = native.decode('utf-8-sig')
    roots = list(fields(text))
    containers = {key: value for key, value, obj in roots if obj and key in
                  ('country', 'colony', 'planets', 'pop_groups', 'pop_jobs', 'situations', 'districts', 'zones')}
    result = {'save': str(path.resolve()), 'save_sha256': hashlib.sha256(raw).hexdigest(),
              'gamestate_sha256': hashlib.sha256(native).hexdigest(), 'gamestate_bytes': len(native),
              'date': next(unquote(v) for k, v, obj in roots if k == 'date'),
              'required_dlcs': [unquote(t) for t, _, _ in tokens(block(text, 'required_dlcs'))],
              'event_targets': [], 'countries': {}, 'planets': {}, 'colonies': {},
              'pop_groups': {}, 'pop_jobs': {}, 'situations': {}}
    for key, value, obj in roots:
        if key == 'saved_event_target' and obj:
            target = scalars(value)
            if str(target.get('name', '')).startswith('eep'):
                result['event_targets'].append(target)
    for identity, value, obj in fields(containers.get('country', '')):
        if not obj:
            continue
        variables = scalars(block(value, 'variables'))
        flags = scalars(block(value, 'flags'))
        if not any(k.startswith('eep') for k in variables) and not any(k.startswith('eep') for k in flags):
            continue
        native_country = scalars(value)
        budget = block(value, 'budget')
        budget_categories = {}
        for period in ('current_month', 'last_month'):
            budget_categories[period] = {}
            for direction in ('income', 'expenses', 'balance'):
                categories = block(block(budget, period), direction)
                budget_categories[period][direction] = {
                    name: scalars(resources) for name, resources, obj in fields(categories) if obj}
        result['countries'][identity] = {
            'name': scalars(block(value, 'name')).get('key'),
            'native': {k: v for k, v in native_country.items() if k in ('capital', 'founder_species_ref', 'type', 'personality', 'military_power', 'economy_power', 'tech_power', 'empire_size', 'num_sapient_pops', 'employable_pops', 'fleet_size', 'used_naval_capacity', 'ruler')},
            'variables': {k: v for k, v in variables.items() if k.startswith('eep')},
            'flags': {k: v for k, v in flags.items() if k.startswith('eep')},
            'government': block(value, 'government'),
            'budget': budget,
            'budget_categories': budget_categories,
            'stockpile': scalars(block(block(block(value, 'modules'), 'standard_economy_module'), 'resources')),
            'modules': block(value, 'modules'),
            'owned_colonies': ids(block(value, 'owned_planets')),
            'crisis': block(value, 'crisis')}
    planet_data = block(containers.get('planets', ''), 'planet')
    for identity, value, obj in fields(planet_data):
        if not obj:
            continue
        variables = scalars(block(value, 'variables'))
        flags = {k: (scalars(v) if b else unquote(v)) for k, v, b in fields(block(value, 'flags'))}
        if not any(k.startswith('eep') for k in variables) and 'eep_core' not in flags:
            continue
        record = scalars(value)
        record['name'] = scalars(block(value, 'name')).get('key')
        record['variables'] = variables
        record['flags'] = flags
        record['modifiers'] = block(value, 'timed_modifier')
        result['planets'][identity] = record
    colony_ids = {str(p['colony']) for p in result['planets'].values() if 'colony' in p}
    group_ids = set()
    job_ids = set()
    for identity, value, obj in fields(containers.get('colony', '')):
        if obj and identity in colony_ids:
            record = scalars(value)
            record['pop_groups'] = ids(block(value, 'pop_groups'))
            record['pop_jobs'] = ids(block(value, 'pop_jobs'))
            record['districts'] = ids(block(value, 'districts'))
            record['buildings'] = ids(block(value, 'buildings'))
            result['colonies'][identity] = record
            group_ids.update(str(i) for i in record['pop_groups'])
            job_ids.update(str(i) for i in record['pop_jobs'])
    for identity, value, obj in fields(containers.get('pop_jobs', '')):
        if obj and identity in job_ids:
            result['pop_jobs'][identity] = scalars(value)
    for identity, value, obj in fields(containers.get('pop_groups', '')):
        if obj and identity in group_ids:
            record = scalars(value)
            record['key'] = scalars(block(value, 'key'))
            record['current_month_growth_details'] = block(value, 'current_month_growth_details')
            result['pop_groups'][identity] = record
    for identity, value, obj in fields(block(containers.get('situations', ''), 'situations')):
        if obj and 'situation_eep_devouring' in value:
            record = scalars(value)
            record['target'] = scalars(block(value, 'target'))
            record['variables'] = scalars(block(value, 'variables'))
            result['situations'][identity] = record
    for identity, colony in result['colonies'].items():
        colony['actual_pop_sum'] = sum(result['pop_groups'][str(i)]['size'] for i in colony['pop_groups'])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('save', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.save)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'date': result['date'], 'countries': len(result['countries']),
                      'planets': len(result['planets']), 'situations': len(result['situations']),
                      'actual_pop_sums': {i: c['actual_pop_sum'] for i, c in result['colonies'].items()}}))


if __name__ == '__main__':
    main()
