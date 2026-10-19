"""Freeze the completed r7pucmedia prefix and prepare three unedited proposals.

This offline evidence author has no desktop/Steam/acceptance or Git operations.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z')
TREE = '61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0'
SAVE_SHA = 'd170383d77f516a21da859e606a4061e6b0ffcc245b69c61ed267ee346263574'
sys.path.insert(0, str(ROOT / 'tools'))
import audit_save as a
from PIL import Image


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def reference(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size,
            'sha256': digest(path)}


def differences(before, after, path=''):
    if type(before) is not type(after):
        return [{'path': path, 'before': before, 'after': after}]
    if isinstance(before, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            if key not in before or key not in after:
                result.append({'path': path+'/'+key, 'before': before.get(key), 'after': after.get(key)})
            else:
                result.extend(differences(before[key], after[key], path+'/'+key))
        return result
    return [] if before == after else [{'path': path, 'before': before, 'after': after}]


def named(text):
    counts, result = Counter(), {}
    for key, body, block in a.fields(text):
        counts[key] += 1
        result[f'{key}#{counts[key]}'] = (body, block)
    return result


def native_differences(before, after, path=''):
    if before == after:
        return []
    try:
        left, right = named(before), named(after)
    except ValueError:
        return [{'path': path, 'kind': 'unnamed_list_or_raw_leaf', 'before': before, 'after': after}]
    if not left and not right:
        return [{'path': path, 'kind': 'raw_whitespace_or_empty', 'before': before, 'after': after}]
    result = []
    if list(left) != list(right):
        result.append({'path': path, 'kind': 'field_order_or_presence',
                       'before_keys': list(left), 'after_keys': list(right)})
    for key in sorted(left.keys() | right.keys()):
        if key not in left or key not in right:
            result.append({'path': path+'/'+key, 'kind': 'added_or_removed',
                           'before': left.get(key), 'after': right.get(key)})
        elif left[key] != right[key]:
            lb, lo = left[key]
            rb, ro = right[key]
            if lo and ro:
                result.extend(native_differences(lb, rb, path+'/'+key))
            else:
                result.append({'path': path+'/'+key, 'kind': 'scalar_or_type',
                               'before': lb, 'after': rb})
    # Whitespace differences are explicitly represented, never silently equal.
    if not result:
        result.append({'path': path, 'kind': 'serialization_whitespace_only',
                       'before_sha256': hashlib.sha256(before.encode()).hexdigest(),
                       'after_sha256': hashlib.sha256(after.encode()).hexdigest()})
    return result


def main():
    raw = HERE / 'raw'
    raw.mkdir()
    sources = sorted(p for p in SOURCE.glob('r7pucmedia*') if p.is_file())
    assert len(sources) == 58
    files = []
    for source in sources:
        before, length = digest(source), source.stat().st_size
        destination = raw / source.name
        assert not destination.exists()
        shutil.copyfile(source, destination)
        assert digest(destination) == before == digest(source)
        assert destination.stat().st_size == length == source.stat().st_size
        files.append({'source': str(source), 'path': destination.relative_to(HERE).as_posix(),
                      'bytes': length, 'sha256': before, 'source_class': 'fixed_r7pucmedia_raw'})
    assert digest(raw/'r7pucmedia.sav') == SAVE_SHA
    receipt, audit = read(raw/'r7pucmedia.native-save.json'), read(raw/'r7pucmedia.audit.json')
    assert receipt['sha256'] == audit['save_sha256'] == SAVE_SHA
    assert receipt['date'] == audit['date'] == '2201.01.01'
    year = ROOT/'docs/evidence/1019-rc7-economy/purifier'
    before_audit = read(year/'r7pucyearui.audit.json')
    native_texts = []
    for save in (year/'r7pucyearui.sav', raw/'r7pucmedia.sav'):
        with zipfile.ZipFile(save) as archive:
            assert archive.testzip() is None
            native_texts.append(archive.read('gamestate').decode('utf-8-sig'))
    native_changes = native_differences(*native_texts)
    audit_changes = differences(before_audit, audit)
    change_report = {'schema': 'eep.1020.purifier-media-native-differences.v1',
        'method': 'Recursive exact named native fields, duplicate keys retained by occurrence; raw/list/whitespace differences retained without numerical tolerance or ignored paths.',
        'full_zip_equal': digest(year/'r7pucyearui.sav') == SAVE_SHA,
        'full_gamestate_equal': native_texts[0] == native_texts[1],
        'audit_differences': audit_changes, 'audit_difference_count': len(audit_changes),
        'native_differences': native_changes, 'native_difference_count': len(native_changes)}
    change_path = HERE/'native-differences.json'
    write(change_path, change_report)
    picture = raw/'r7pucmedia-single-colony-clean.jpg'
    ocr = read(picture.with_suffix('.ocr.json'))
    labels = [row['text'] for row in ocr['rows']]
    country = audit['countries']['0']
    colony_id = str(country['owned_colonies'][0])
    root_before, root_after = [dict((k,(v,o)) for k,v,o in a.fields(t)) for t in native_texts]
    current = country['budget_categories']['current_month']
    income = sum(Decimal(str(v.get('energy',0))) for v in current['income'].values())
    expenses = sum(Decimal(str(v.get('energy',0))) for v in current['expenses'].values())
    branch_report = read(year/'native-branch-report.json')
    months = branch_report['candidate_months']
    stocks = []
    for key in ('minerals','physics_research','society_research','engineering_research'):
        old, new = before_audit['countries']['0']['stockpile'][key], country['stockpile'][key]
        stocks.append({'resource': key, 'before': old, 'after': new,
                       'delta_exact': str(Decimal(str(new))-Decimal(str(old)))})
    excluded_metadata = {'save','save_sha256','gamestate_sha256','gamestate_bytes'}
    report = {'schema':'eep.1020.rc7-purifier-gallery-observation.v1',
        'status':'PASS_SCOPED_MEDIA_BINDING_ONLY',
        'scope':'Post-economy native preset screenshot and independent media save; not a whole case, not yearUI byte equality, not a new annual-economy sample.',
        'run_id':'20261019T164112Z','version':'0.4.0-rc.7','production_tree_sha256':TREE,
        'media_save':reference(raw/'r7pucmedia.sav'),
        'economic_year_ui':reference(year/'r7pucyearui.sav'),
        'economic_report':reference(year/'native-branch-report.json'),
        'selected_image':reference(picture), 'selected_ocr':reference(picture.with_suffix('.ocr.json')),
        'selected_ocr_metadata':{k:v for k,v in ocr.items() if k!='rows'},
        'checks':{
            'native_save_receipt_audit_SHA_date':receipt['date']==audit['date']=='2201.01.01',
            'image_SHA_matches_GPU_OCR':digest(picture)==ocr['image_sha256'],
            'actual_GPU_PID_37300':ocr['pid']==37300 and ocr['capture']=='fresh Steam F12 GPU backbuffer',
            'Chinese_date_and_relic_homeworld_visible':'2201.01.01' in labels and '遗落星球' in labels,
            'energy_rounded_plus_46_visible':'757+46' in labels,
            'native_single_owned_colony':len(country['owned_colonies'])==1,
            'native_core_relic':audit['planets']['3']['planet_class']=='pc_relic',
            'country_population_4859':country['native']['num_sapient_pops']==4859,
            'native_energy_stock_unchanged':before_audit['countries']['0']['stockpile']['energy']==country['stockpile']['energy']==757.88612,
            'native_budget_unchanged':before_audit['countries']['0']['budget_categories']==country['budget_categories'],
            'economic_ledger_growth_and_core_tiers_unchanged':before_audit['countries']['0']['variables']==country['variables'],
            'native_queues_construction_ships_fleets_designs_unchanged':all(root_before[k]==root_after[k] for k in ('construction','ships','fleet','ship_design','starbase_mgr')),
            'native_population_entities_jobs_and_colony_layout_unchanged':all(before_audit[k]==audit[k] for k in ('colonies','pop_groups','pop_jobs','districts','species')),
            'original_months_12_all_nonnegative':len(months)==12 and all(m['net_energy']>=0 for m in months),
            'screenshot_visual_review_empty_build_queue_single_colony_relic_date':True,
            'parent_script_exit_zero_not_claimed':True},
        'visual_review':'Independently viewed three original full frames. Selected WS06 shows EEP-Core relic planet, one colony entry, empty construction panel, 2201.01.01 paused and top-bar +46. No crop, repaint or generated content.',
        'media_current_month_energy':{'income_exact':str(income),'expenses_exact':str(expenses),'net_exact':str(income-expenses)},
        'year_ui_to_media_stock_changes':stocks,
        'audit_semantic_difference_count_excluding_four_file_metadata_fields':sum(c['path'].split('/')[1] not in excluded_metadata for c in audit_changes),
        'full_strict_equality':False,'native_differences':reference(change_path),
        'full_native_differences_count':len(native_changes),
        'changed_root_fields':[k for k in sorted(root_before.keys()|root_after.keys()) if root_before.get(k)!=root_after.get(k)],
        'original_economy_monthly_net_energy':[m['net_energy'] for m in months],
        'economic_operation_constraints':branch_report['economy_checks'],
        'parent_execution':'The native media save completed. The following parent-script uppercase startswith assertion failed after this save and before Hive new_game; no parent exit0 claim.',
        'limitations':['Popup acknowledgements have real mineral/research stock effects after the economic boundary. No new pure-economy sample or strict yearUI equality is claimed.','The frame does not independently prove twelve monthly budgets; those values are cited from the already sealed separate economic report, whose operation-constraint checks remain null.','Final 18-case acceptance and public release remain PENDING.']}
    assert all(report['checks'].values()), report['checks']
    write(HERE/'media-observation.json',report)
    refs = [ROOT/p for p in (
        'docs/evidence/1019-rc7-growth-v1/run/manifest.json',
        'docs/evidence/1019-rc7-static/source-index.json',
        'docs/evidence/1019-rc7-static/candidate-rc7-open-kaishek.json',
        'docs/evidence/1020-rc7-high-level-ui-v1/index.json',
        'docs/evidence/1019-analysis/rc7-high-level-growth-ui-binding-report-v2.json',
        'docs/evidence/1019-rc7-economy/purifier/manifest.json',
        'docs/evidence/1019-rc7-economy/purifier/archive-index.json',
        'docs/evidence/1019-rc7-economy/purifier/native-branch-report.json',
        'docs/evidence/1019-rc7-economy/purifier/r7pucyearui.sav',
        'docs/evidence/1019-rc7-economy/purifier/r7pucyearui.audit.json',
        'tools/audit_save.py')]
    write(HERE/'index.json',{'schema':'eep.1020.rc7-purifier-gallery-archive.v1',
        'status':'SEALED_SCOPED_POST_ECONOMY_MEDIA_ONLY','created_at_utc':datetime.now(timezone.utc).isoformat(),
        'run_id':'20261019T164112Z','version':'0.4.0-rc.7','production_tree_sha256':TREE,
        'raw_whitelist':'Exactly the completed 58 regular r7pucmedia* files; no logs, Hive or live prefix.',
        'files':files,
        'authored':[reference(HERE/'media-observation.json'),reference(change_path)],
        'canonical_references':[reference(p) for p in refs],
        'native_roles':{'media':reference(raw/'r7pucmedia.sav'),'economic_year_ui':reference(year/'r7pucyearui.sav')},
        'raw_payload_files':len(files),'raw_payload_bytes':sum(x['bytes'] for x in files),
        'case_status':'PENDING','full_year_ui_media_strict_equal':False,
        'copied_59_mod_files':False,'parent_script_exit_zero_claimed':False,
        'final_result_written':False,'formal_inputs_modified':False})
    print(json.dumps({'raw_files':len(files),'raw_bytes':sum(x['bytes'] for x in files),
                      'native_difference_count':len(native_changes),'checks':report['checks']}))


if __name__=='__main__':
    main()
