"""Independently re-read the sealed configuration source and WS03 proposal."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import zipfile
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def read(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ok(r):
    p=ROOT/r['path']
    return p.stat().st_size==r['bytes'] and digest(p)==r['sha256']


def main():
    selection=read(HERE/'selection.json')
    package=ROOT/'docs/evidence/1020-rc7-relic-configuration-v1'
    archive=read(package/'archive-index.json')
    sourceverify=read(package/'verification-v1.json')
    checks={}
    checks['164_sealed_payload_sizes_and_SHA_unchanged']=len(archive['files'])==164 and all((package/r['path']).stat().st_size==r['bytes'] and digest(package/r['path'])==r['sha256'] for r in archive['files'])
    checks['source_index_pinned_by_sealed_verification']=digest(package/'archive-index.json')==sourceverify['archive_index_sha256']=='aaa439d71053b207d3b92801d27f462b5187e1a6207e80f3d25016300ec42523' and sourceverify['status']=='PASS_SCOPED_BYTES'
    names=('source','destination','ocr','native_save','native_save_audit','native_save_receipt','source_archive','source_archive_verification','source_configuration_report','same_day_native_reference_image','original_failed_obscured_v1','proposed_manifest')
    checks['12_selection_reference_bytes_sizes_SHA_exact']=all(ok(selection[k]) for k in names)
    source=ROOT/selection['source']['path'];destination=ROOT/selection['destination']['path']
    checks['new_WS03_unchanged_clean_v2_bytes']=source.name=='r7cfgui-mother-details-clean-v2.jpg' and source.read_bytes()==destination.read_bytes()
    with Image.open(destination) as image:
        checks['native_JPEG_1024x768_under_1MB']=image.size==(1024,768) and image.format=='JPEG' and destination.stat().st_size<1_000_000
        image.verify()
    ocr=read(ROOT/selection['ocr']['path']);labels=[r['text'] for r in ocr['rows']]
    checks['native_GPU_OCR_PID_date_binding']=ocr['pid']==37300 and ocr['capture']=='fresh Steam F12 GPU backbuffer' and ocr['image_sha256']==digest(destination) and '2201.01.07' in labels
    audit=read(ROOT/selection['native_save_audit']['path']);receipt=read(ROOT/selection['native_save_receipt']['path'])
    with zipfile.ZipFile(ROOT/selection['native_save']['path']) as z:
        checks['native_save_ZIP_audit_receipt_SHA_date']=z.testzip() is None and hashlib.sha256(z.read('gamestate')).hexdigest()==audit['gamestate_sha256'] and audit['save_sha256']==receipt['sha256']==selection['native_save']['sha256'] and audit['date']==receipt['date']=='2201.01.07'
    v=audit['countries']['0']['variables']
    checks['actual_C0_L0_six_ranks_zero']=v['eep_c']==v['eep_mothership_level']==0 and all(v['eep_component_'+k+'_level']==0 for k in ('shield','armor','hull','damage','tracking','regen'))
    bounded=read(ROOT/selection['source_configuration_report']['path'])
    checks['actual_native_same_country_same_date_reference']=bounded['actual_identity']=={'mother_fleet':151,'mother_ship':1044,'mother_design':1844,'reference_fleet':175,'reference_ship':1068,'reference_design':16779116,'country':0,'core_world':2} and bounded['date']=='2201.01.07' and bounded['checks']['same_actual_country_reference_identity'] is True
    checks['actual_displayed_stats_and_nonzero_upkeep_preserved']=bounded['actual_panels']['mother']==selection['actual_displayed_stats'] and bounded['maintenance']['energy_per_month_displayed']==10.07 and bounded['maintenance']['alloys_per_month_displayed']==2.88
    proposal=read(ROOT/selection['proposed_manifest']['path']);old=read(ROOT/proposal['previous_proposal']['path'])
    checks['seven_IDs_six_gallery_slots_exact']=[i['id'] for i in proposal['images']]==[f'WS-{i:02}' for i in range(7)] and sum(i['role']=='gallery' for i in proposal['images'])==6
    checks['other_six_slots_and_four_inline_exact']=all(proposal['images'][i]==old['images'][i] for i in (0,1,2,4,5,6)) and proposal['inline_images_unchanged']==old['inline_images_unchanged'] and len(proposal['inline_images_unchanged'])==4
    checks['12_protected_inputs_old_candidates_and_history_exact']=len(selection['untouched_inputs'])==12 and all(ok(r) for r in selection['untouched_inputs'])
    ws03=proposal['images'][3]
    checks['WS03_zero_growth_Jan7_caption_scope']=all(w in ws03['caption'] for w in ('C0','L0','2201.01.07','同国同日')) and '2200.01.01' not in ws03['caption'] and '免维护' not in ws03['caption']
    checks['distinct_active_images_and_raw_source_equal']=len({i['sha256'] for i in proposal['images']})==7 and all((ROOT/'workshop'/i['file']).read_bytes()==(ROOT/'workshop'/i['source']).read_bytes() for i in proposal['images'])
    checks['proposal_and_all_cases_still_pending']=proposal['status']=='PROPOSED' and proposal['final_release_selection'] is False and all(proposal['images'][i]['status']=='LOCAL_READY_PENDING_CASE_REVIEW' for i in (3,4,5,6)) and selection['no_case_promoted'] is True
    result={'schema':'eep.1020.rc7-ws03-gallery-independent-verification.v1',
        'status':'PASS_BYTES_AND_MEDIA_SCOPE_ONLY' if all(checks.values()) else 'FAIL',
        'verified_at_utc':datetime.now(timezone.utc).isoformat(),
        'method':'Independent fresh process re-read all164 sealed payloads, selection references, raw ZIP/audit/receipt, native original GPU/OCR, unchanged formal inputs and history, exact other slots/inline and local copies. No desktop, logs or Mod/tool changes.',
        'checks':checks,'selection_sha256':digest(HERE/'selection.json'),
        'proposed_manifest_sha256':selection['proposed_manifest']['sha256'],
        'whole_case_or_release_accepted':False}
    with (HERE/'verification.json').open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps(result,ensure_ascii=True,indent=2))
    assert all(checks.values())


if __name__=='__main__':main()
