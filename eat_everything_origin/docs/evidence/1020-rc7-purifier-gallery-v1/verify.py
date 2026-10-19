"""Separate-process, read-only verification of the scoped archive and proposals."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib
import json
import zipfile
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def refok(ref):
    p=ROOT/ref['path']
    return p.stat().st_size==ref['bytes'] and sha(p)==ref['sha256']


def main():
    index=read(HERE/'index.json')
    checks={}
    rows=index['files']
    checks['58_raw_files_destination_and_original_SHA_sizes_exact']=len(rows)==58 and all(
        sha(HERE/r['path'])==sha(Path(r['source']))==r['sha256'] and
        (HERE/r['path']).stat().st_size==Path(r['source']).stat().st_size==r['bytes'] for r in rows)
    checks['raw_file_set_exact']=set(p.name for p in (HERE/'raw').iterdir())=={Path(r['path']).name for r in rows}
    checks['two_authored_payload_refs_exact']=len(index['authored'])==2 and all(refok(r) for r in index['authored'])
    checks['11_canonical_references_exact']=len(index['canonical_references'])==11 and all(refok(r) for r in index['canonical_references'])
    manifest=read(ROOT/'docs/evidence/1019-rc7-growth-v1/run/manifest.json')
    checks['canonical_manifest_exact_RC7_tree_and_Chinese']=manifest['copied_mod_tree_sha256']==index['production_tree_sha256'] and manifest['language']=='l_simp_chinese'
    count=0
    for image in (HERE/'raw').glob('*.jpg'):
        ocr=read(image.with_suffix('.ocr.json'))
        assert ocr['image_sha256']==sha(image)
        assert ocr['pid']==37300 and ocr['capture']=='fresh Steam F12 GPU backbuffer'
        with Image.open(image) as img:img.verify()
        count+=1
    checks['all_native_GPU_OCR_frame_bindings']=count>0
    rawsave=HERE/'raw/r7pucmedia.sav'
    audit=read(rawsave.with_suffix('.audit.json'))
    receipt=read(rawsave.with_suffix('.native-save.json'))
    with zipfile.ZipFile(rawsave) as z:
        native=z.read('gamestate')
        checks['native_ZIP_CRC_receipt_audit_gamestate_exact']=z.testzip() is None and sha(rawsave)==audit['save_sha256']==receipt['sha256']=='d170383d77f516a21da859e606a4061e6b0ffcc245b69c61ed267ee346263574' and hashlib.sha256(native).hexdigest()==audit['gamestate_sha256']
    report=read(HERE/'media-observation.json')
    before=read(ROOT/'docs/evidence/1019-rc7-economy/purifier/r7pucyearui.audit.json')
    expected={'minerals':Decimal('2'),'physics_research':Decimal('3.0899'),'society_research':Decimal('3.0899'),'engineering_research':Decimal('3.8099')}
    checks['actual_post_boundary_stock_changes_not_hidden']=all(Decimal(str(audit['countries']['0']['stockpile'][k]))-Decimal(str(before['countries']['0']['stockpile'][k]))==v for k,v in expected.items()) and report['full_strict_equality'] is False
    changes=read(HERE/'native-differences.json')
    paths={c['path'] for c in changes['native_differences']}
    checks['crisis_project_tutorial_world_and_rng_differences_retained']=all(p in paths for p in (
        '/country#1/0#1/events#1/special_project#1','/country#1/0#1/flags#1/tutorial_level_picked#1',
        '/planets#1/planet#1/9#1/binary_flags#1','/random_count#1')) and changes['native_difference_count']==23 and changes['full_gamestate_equal'] is False
    checks['native_ledger_budget_and_population_unchanged']=all(before['countries']['0'][k]==audit['countries']['0'][k] for k in ('variables','budget_categories','owned_colonies','native')) and all(before[k]==audit[k] for k in ('colonies','pop_groups','pop_jobs','districts','species'))
    branch=read(ROOT/'docs/evidence/1019-rc7-economy/purifier/native-branch-report.json')
    checks['annual_positive_claim_from_separate_12_native_samples']=len(branch['candidate_months'])==12 and all(row['net_energy']>0 for row in branch['candidate_months']) and all(branch['economy_checks'][k] is None for k in ('no_resource_injection','no_trade_subsidy','no_job_closure','no_ship_disband'))
    selection=read(HERE/'local-media-selection.json')
    checks['three_local_copies_byte_identical_to_distinct_sources']=len(selection['copies'])==3 and len({r['source']['sha256'] for r in selection['copies']})==3 and all(refok(r['source']) and refok(r['destination']) and refok(r['native_save']) and (ROOT/r['source']['path']).read_bytes()==(ROOT/r['destination']['path']).read_bytes() for r in selection['copies'])
    checks['official_inputs_and_old_RC6_photo_and_v1_untouched']=all(refok(r) for r in selection['untouched_inputs'])
    proposal=read(ROOT/selection['proposed_manifest']['path'])
    checks['v2_remains_draft_WS03_pending_no_final_acceptance']=refok(selection['proposed_manifest']) and proposal['status']=='PROPOSED' and proposal['final_release_selection'] is False and proposal['images'][3]['status']=='PENDING_NATIVE_SOURCE' and report['status']=='PASS_SCOPED_MEDIA_BINDING_ONLY' and index['case_status']=='PENDING'
    checks['WS04_WS05_caption_pressure_test_WS06_preset']=all('成长压力测试' in proposal['images'][i]['caption'] for i in (4,5)) and '实机验收预设' in proposal['images'][6]['caption'] and '殖民地1' in proposal['images'][6]['caption']
    checks['parent_exit_zero_not_claimed']=index['parent_script_exit_zero_claimed'] is False
    result={'schema':'eep.1020.rc7-purifier-gallery-independent-verify.v1',
        'status':'PASS_BYTES_AND_MEDIA_SCOPED_ONLY' if all(checks.values()) else 'FAIL',
        'verified_at_utc':datetime.now(timezone.utc).isoformat(),
        'method':'Independent fresh process re-read all raw source/destination bytes, canonical and authored references, native ZIP/audit/receipt, original GPU/OCR, separate annual report, local copies, untouched formal inputs and v2 scope. No archive computed Python state reused.',
        'checks':checks,'index_sha256':sha(HERE/'index.json'),
        'raw_payload_files':len(rows),'raw_payload_bytes':sum(r['bytes'] for r in rows),
        'GPU_OCR_pairs':count,'canonical_references':len(index['canonical_references']),
        'native_difference_count':changes['native_difference_count'],
        'parent_script_exit_zero_claimed':False,'case_status':'PENDING',
        'read_active_Hive_or_logs':False,'UI_Steam_Git_Mod_tools_operations':False}
    with (HERE/'verify.json').open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps(result,ensure_ascii=True,indent=2))
    assert all(checks.values())


if __name__=='__main__':
    main()
