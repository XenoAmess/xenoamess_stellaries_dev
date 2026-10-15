"""One-shot read-only native comparison; never starts the game."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[5]
SPEC = importlib.util.spec_from_file_location('high_r_native_reader', ROOT / 'shishan_code_origin/tools/audit_feedback_runtime_save.py')
a = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = a
SPEC.loader.exec_module(a)
RUN = Path(__file__).resolve().parent
BEFORE = RUN.parent / '20261015T090720Z/fb456_legacy25_reload.sav'
AFTER = RUN / 'formal021_legacy25_reload.sav'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return sha(json.dumps(value, ensure_ascii=True, separators=(',', ':')).encode('ascii'))


def fields(doc, source, keys):
    return {key: [doc.native(v) for v in doc.values(source, key)] for key in keys}


def snapshot(path):
    raw = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        game = archive.read('gamestate')
        meta = a.Document(archive.read('meta').decode('utf-8-sig'))
        doc = a.Document(game.decode('utf-8-sig'))
    actor_id, actor, _ = a.locate_player(doc)
    main, _ = a.locate_main_species(doc, actor)
    species = a.species_records(doc)
    population = a.inspect_populations(doc, actor, actor_id, species, main)
    variables = a.mod_fields(doc, doc.section(actor, 'variables', False))
    flags = a.mod_fields(doc, doc.section(actor, 'flags', False))
    modifiers = a.native_modifiers(doc, actor)
    expected, diagnostics = a.expected_and_observed(population, variables, flags, modifiers)
    databases = {}
    for key in ('species_db', 'leaders', 'pop_groups', 'pop_jobs'):
        database = a.numeric_database(doc, doc.section(doc.root, key), key)
        databases[key] = {str(index): doc.native(block) for index, block in database.items()}
    groups = a.numeric_database(doc, doc.section(doc.root, 'pop_groups'), 'population')
    own_colonies = set(population['owned_colony_ids'])
    foreign_species, domestic_species = set(), set()
    domestic_groups, foreign_groups = [], []
    for index, block in groups.items():
        size = a.integer(doc.scalar(block, 'size'), 'population size')
        if size <= 0:
            continue
        colony = a.integer(doc.scalar(block, 'planet'), 'population colony')
        sid = a.integer(doc.scalar(doc.section(block, 'key'), 'species'), 'population species')
        row = {'id': index, 'colony': colony, 'species': sid, 'size': size}
        if colony in own_colonies:
            domestic_species.add(sid)
            domestic_groups.append(row)
        else:
            foreign_species.add(sid)
            foreign_groups.append(row)
    foreign_definitions = set(foreign_species)
    for index in list(foreign_species):
        foreign_definitions.update(species[index]['base_ref_chain'])
    owned = a.integer_list(doc, doc.section(actor, 'owned_leaders'), 'owned leaders')
    leader_db = a.numeric_database(doc, doc.section(doc.root, 'leaders'), 'leaders')
    white = []
    leader_core = {}
    for index, block in leader_db.items():
        leader_flags = doc.section(block, 'flags', False)
        flag_keys = [e.key for e in doc.entries(leader_flags)] if leader_flags else []
        core = fields(doc, block, ('name', 'species', 'portrait', 'country', 'class', 'tier', 'level', 'bonus_skill_level', 'experience', 'traits', 'available_trait', 'available_trait_selections', 'flags', 'leader_flags', 'variables', 'job', 'location', 'council_location', 'design'))
        leader_core[str(index)] = core
        if 'shishan_code_vivhite' in flag_keys:
            white.append({'id': index, 'owned': index in owned, 'native': databases['leaders'][str(index)], 'core': core})
    root_raw = {}
    for entry in doc.entries():
        key = entry.key
        if key in root_raw:
            key = f'{key}#{sum(str(k).split("#")[0] == str(entry.key) for k in root_raw)}'
        value = doc.text[entry.value.start:entry.value.end] if isinstance(entry.value, a.Block) else entry.value
        root_raw[key] = sha(value.encode('utf-8'))
    return {'identity': {'save': str(path.resolve()), 'sha256': sha(raw), 'bytes': len(raw), 'gamestate_sha256': sha(game),
                          'date': doc.scalar(doc.root, 'date'), 'meta_date': meta.scalar(meta.root, 'date'),
                          'version': doc.scalar(doc.root, 'version'), 'mods': meta.native(meta.field(meta.root, 'mods'))},
            'actor_id': actor_id, 'main_evidence': a.main_species_evidence(doc, actor),
            'population': population, 'variables': variables, 'flags': flags, 'modifiers': modifiers,
            'expected': expected, 'diagnostics': diagnostics, 'projects': a.native_projects(doc, actor),
            'owned_leader_ids': owned, 'white': white, 'leader_core': leader_core,
            'domestic_species_ids': sorted(domestic_species), 'foreign_actual_species_ids': sorted(foreign_species),
            'foreign_referenced_definition_ids': sorted(foreign_definitions), 'domestic_groups': domestic_groups, 'foreign_groups': foreign_groups,
            'rights': doc.native(doc.section(doc.section(actor, 'modules'), 'standard_species_rights_module')),
            'country_budget': doc.native(doc.section(actor, 'budget')),
            'cached_species_refs': fields(doc, actor, ('owned_species_refs', 'default_species', 'founder_species_ref')),
            'root_scalar_values': {key: doc.native(doc.field(doc.root, key)) for key in ('last_created_design', 'last_event_id', 'random_count', 'random_seed')},
            'root_raw_hashes': root_raw, 'databases': databases}


def diff(before, after, path=''):
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(set(before) | set(after), key=str):
            if key not in before or key not in after:
                result.append({'path': path + '/' + str(key), 'before': before.get(key), 'after': after.get(key),
                               'before_present': key in before, 'after_present': key in after})
            else:
                result.extend(diff(before[key], after[key], path + '/' + str(key)))
        return result
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        result = []
        for index, (left, right) in enumerate(zip(before, after)):
            result.extend(diff(left, right, path + '/' + str(index)))
        return result
    return [{'path': path, 'before': before, 'after': after}]


def record_changes(left, right):
    result = []
    for index in sorted(set(left) | set(right), key=int):
        if left.get(index) != right.get(index):
            result.append({'id': int(index), 'before_present': index in left, 'after_present': index in right,
                           'before_sha256': canonical(left[index]) if index in left else None,
                           'after_sha256': canonical(right[index]) if index in right else None,
                           'diff': diff(left.get(index), right.get(index))})
    return result


def check(name, condition, **observed):
    return {'name': name, 'status': 'PASS' if condition else 'FAIL', **observed}


def main():
    before = snapshot(BEFORE)
    print('before extracted', flush=True)
    after = snapshot(AFTER)
    print('after extracted', flush=True)
    p0, p1 = before['population'], after['population']
    v0, v1 = before['variables'], after['variables']
    f0, f1 = before['flags'], after['flags']
    core_checks = []
    core_checks.append(check('native_same_date_version_actor',
        before['identity']['date'] == after['identity']['date'] == before['identity']['meta_date'] == after['identity']['meta_date'] and
        before['identity']['version'] == after['identity']['version'] and before['actor_id'] == after['actor_id']))
    for label, source in [('before', before), ('after', after)]:
        pop, var = source['population'], source['variables']
        complete = all(row['status'] == 'MATCH' for row in source['expected']['comparisons'].values())
        errors = [d for d in source['diagnostics'] if d['severity'] == 'error']
        core_checks.append(check(label + '_independent_architecture', complete and not errors and
            pop['population'] == 5567 and pop['trait_weight'] == 239381 and
            a.decimal(pop['trait_average_decimal'], 'U') == 43 and
            a.decimal(var.get('shishan_code_architecture_repeat_count'), 'R') == 25 and
            a.decimal(source['expected']['total'], 'T') == 68 and
            a.decimal(source['expected']['bonus'], 'B') == a.Decimal('3.4'),
            P=pop['population'], W=pop['trait_weight'], U=pop['trait_average_decimal'],
            R=var.get('shishan_code_architecture_repeat_count'), T=source['expected']['total'], B=source['expected']['bonus'],
            comparisons=source['expected']['comparisons'], diagnostics=source['diagnostics']))
        instances = [m for m in source['modifiers'] if m['modifier'] == 'shishan_code_architecture_jobs']
        core_checks.append(check(label + '_single_architecture_instance_68', len(instances) == 1 and a.decimal(instances[0]['effective_multiplier'], 'scale') == 68, instances=instances))
        counters = {suffix: var.get('shishan_code_iteration_' + suffix) for suffix in ('output', 'energy', 'assembly', 'experience')}
        core_checks.append(check(label + '_legacy_k_and_migration', list(counters.values()) == ['7', '5', '11', '4'] and 'shishan_code_architecture_migrated' in source['flags'], counters=counters, migrated=source['flags'].get('shishan_code_architecture_migrated')))
    core_checks += [check('all_Mod_variables_and_flags_unchanged', v0 == v1 and f0 == f1,
                         variable_diff=diff(v0, v1), flag_diff=diff(f0, f1)),
                    check('n2_CD2_unchanged', all(v.get('shishan_code_maintenance_count') == '2' and v.get('shishan_code_reroll_cooldown') == '2' for v in (v0, v1)))]
    slots = {label: {str(n): {'present': 'shishan_code_reward_slot_' + str(n) in var, 'value': var.get('shishan_code_reward_slot_' + str(n))}
                       for n in range(1, 4)} for label, var in [('before', v0), ('after', v1)]}
    tickets = ('shishan_code_reward_pending', 'shishan_code_reward_ticket_ready', 'shishan_code_reward_window_open',
               'shishan_code_maintain_success_pending', 'shishan_code_optimize_success_pending', 'shishan_code_clean_success_pending', 'shishan_code_relapse_pending')
    ticket_state = {label: {k: flags.get(k) for k in tickets} for label, flags in [('before', f0), ('after', f1)]}
    core_checks.append(check('no_entity_slots_or_unconsumed_ticket', slots['before'] == slots['after'] and
        all(not row['present'] for side in slots.values() for row in side.values()) and
        all(value is None for side in ticket_state.values() for value in side.values()), slots=slots, tickets=ticket_state))
    databases = {key: record_changes(before['databases'][key], after['databases'][key]) for key in before['databases']}
    owned_ids = sorted(set(before['owned_leader_ids']) | set(after['owned_leader_ids']))
    owned_leaders = [{'id': index, 'before': before['databases']['leaders'].get(str(index)),
                     'after': after['databases']['leaders'].get(str(index)),
                     'exact_native_equal': before['databases']['leaders'].get(str(index)) == after['databases']['leaders'].get(str(index))}
                    for index in owned_ids]
    owned_core_diff = {str(index): diff(before['leader_core'].get(str(index)), after['leader_core'].get(str(index))) for index in owned_ids}
    core_checks.append(check('owned_leader_identity_XP_level_traits_choices_portrait_flags_state',
        before['owned_leader_ids'] == after['owned_leader_ids'] and not any(owned_core_diff.values()), differences=owned_core_diff))
    white_before = {str(r['id']): r for r in before['white']}
    white_after = {str(r['id']): r for r in after['white']}
    core_checks.append(check('complete_vivhite_records_unchanged', white_before == white_after,
                             flagged_before=list(white_before), flagged_after=list(white_after), differences=diff(white_before, white_after)))
    domestic = sorted(set(before['domestic_species_ids']) | set(after['domestic_species_ids']))
    foreign = sorted(set(before['foreign_referenced_definition_ids']) | set(after['foreign_referenced_definition_ids']))
    template_states = {str(index): {'before': before['databases']['species_db'].get(str(index)),
                                   'after': after['databases']['species_db'].get(str(index)),
                                   'equal': before['databases']['species_db'].get(str(index)) == after['databases']['species_db'].get(str(index))} for index in domestic}
    core_checks.append(check('domestic_actual_templates_and_population_groups_unchanged', all(r['equal'] for r in template_states.values()) and before['domestic_groups'] == after['domestic_groups'] and before['main_evidence']['founder_species_ref'] == after['main_evidence']['founder_species_ref'],
                             actual_species_before=before['domestic_species_ids'], actual_species_after=after['domestic_species_ids']))
    foreign_definition_changes = [r for r in databases['species_db'] if r['id'] in foreign]
    core_checks.append(check('foreign_actual_species_and_ancestor_definitions_unchanged', not foreign_definition_changes,
                             referenced_ids_before=before['foreign_referenced_definition_ids'], referenced_ids_after=after['foreign_referenced_definition_ids'], differences=foreign_definition_changes))
    raw_differences = {'root_section_raw_hash_changes': diff(before['root_raw_hashes'], after['root_raw_hashes']),
                       'database_record_changes': databases,
                       'cached_species_reference_diff': diff(before['cached_species_refs'], after['cached_species_refs']),
                       'species_rights_diff': diff(before['rights'], after['rights']),
                       'country_budget_diff': diff(before['country_budget'], after['country_budget']),
                       'foreign_actual_group_state_diff': diff(before['foreign_groups'], after['foreign_groups'])}
    core_status = 'PASS' if all(c['status'] == 'PASS' for c in core_checks) else 'FAIL'
    observed_raw = any(raw_differences.values())
    raw_differences['country_budget_native_before'] = before['country_budget']
    raw_differences['country_budget_native_after'] = after['country_budget']
    raw_differences['root_scalar_values'] = {'before': before['root_scalar_values'], 'after': after['root_scalar_values']}
    observed_lengths = {}
    for label, source in [('before', before), ('after', after)]:
        high_water = next(row['value'] for row in source['country_budget'] if row['key'] == 'income_high_water_mark')
        observed_lengths[label] = next(row['value'] for row in high_water if row['key'] == 'length')
    raw_differences['country_budget_named_differences'] = [
        {'path': f'country[{after["actor_id"]}].budget.income_high_water_mark.length', **observed_lengths,
         'evidence': 'the sole recursive raw budget difference is /4/value/1/value; complete native budget arrays are preserved above'}]
    report = {'status': 'FAIL' if core_status == 'FAIL' else ('OBSERVED_WITH_RAW_DIFFERENCES' if observed_raw else 'PASS'),
              'core_state_status': core_status,
              'scope': 'independent native saved-data comparison after root performed genuine formal 0.2.1 reload; no GUI or engine execution by this auditor',
              'before': before['identity'], 'after': after['identity'], 'checks': core_checks,
              'architecture_before': {'population': p0, 'expected': before['expected'], 'variables': v0, 'flags': f0, 'modifiers': before['modifiers']},
              'architecture_after': {'population': p1, 'expected': after['expected'], 'variables': v1, 'flags': f1, 'modifiers': after['modifiers']},
              'main_pointer_before': before['main_evidence'], 'main_pointer_after': after['main_evidence'],
              'owned_leaders_complete': owned_leaders, 'vivhite_complete_before': before['white'], 'vivhite_complete_after': after['white'],
              'all_global_leader_count_before': len(before['databases']['leaders']), 'all_global_leader_count_after': len(after['databases']['leaders']),
              'domestic_actual_template_definitions': template_states,
              'foreign_definition_sha256_before': {str(i): canonical(before['databases']['species_db'].get(str(i))) for i in foreign},
              'foreign_definition_sha256_after': {str(i): canonical(after['databases']['species_db'].get(str(i))) for i in foreign},
              'native_raw_differences': raw_differences,
              'interpretation_boundaries': ['Do not infer all-world byte identity from core-state PASS.',
                  'Foreign species-definition identity is separate from foreign employment/budget/cache identity.',
                  'Saved history R is compared, not inferred from traits; old k values remain 7/5/11/4.',
                  'Absent slot values remain absent, not observed zero.',
                  'This comparison cannot prove intermediate callback counts, GUI rendering, or a new natural progression to R25.']}
    output = RUN / 'independent-formal021-high-r-reload-audit.json'
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'core': core_status, 'failed_checks': [c['name'] for c in core_checks if c['status'] != 'PASS'],
                      'report': str(output), 'sha256': sha(output.read_bytes()),
                      'database_changes': {k: len(v) for k, v in databases.items()},
                      'owned_leaders': len(owned_ids), 'white': list(white_before),
                      'other_diff_counts': {k: len(v) for k, v in raw_differences.items() if k != 'database_record_changes'}}, ensure_ascii=True), flush=True)


if __name__ == '__main__':
    main()
