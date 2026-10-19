"""Prepare WS03 only from a sealed, zero-growth native configuration stage."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import shutil
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PACKAGE=ROOT/'docs/evidence/1020-rc7-relic-configuration-v1'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def ref(p):
    raw=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(raw),
            'sha256':hashlib.sha256(raw).hexdigest()}


def write(p,d):
    with p.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')


def main():
    previous=ROOT/'docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v2.json'
    old=read(previous)
    protected=[ROOT/p for p in ('VERSION','mod/descriptor.mod','CHANGELOG.md',
        'workshop/description.bbcode','workshop/images-manifest.json','workshop/item-id.txt',
        'docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v1.json',
        'docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v2.json',
        'workshop/images/06-purifier-single-homeworld-0.4.0-2201.jpg')]
    protected += [ROOT/'workshop'/old['images'][i]['file'] for i in (4,5,6)]
    before=[ref(p) for p in protected]
    source=PACKAGE/'raw/r7cfgui-mother-details-clean-v2.jpg'
    save=PACKAGE/'raw/r7cfgui.sav'
    ocr=read(source.with_suffix('.ocr.json'))
    audit=read(save.with_suffix('.audit.json'))
    bounded=read(PACKAGE/'bounded-configuration-ui-report-v1.json')
    assert ref(source)['sha256']==ocr['image_sha256']=='05943ebe60152e07978eedaa8597c97a49fcebaf3152c81af251370de5da2f7f'
    assert audit['date']==bounded['date']=='2201.01.07'
    variables=audit['countries']['0']['variables']
    assert variables['eep_c']==variables['eep_mothership_level']==0
    assert all(variables['eep_component_'+kind+'_level']==0 for kind in ('shield','armor','hull','damage','tracking','regen'))
    destination=ROOT/'workshop/images/03-mothership-zero-growth-0.4.0-rc7-2201.jpg'
    assert not destination.exists()
    shutil.copyfile(source,destination)
    assert destination.read_bytes()==source.read_bytes()
    with Image.open(destination) as image:
        size,format_name=image.size,image.format;image.verify()
    assert size==(1024,768) and format_name=='JPEG' and destination.stat().st_size<1_000_000
    proposal=deepcopy(old)
    proposal['purpose']='All four RC7 replacement candidates now have actual local sources. Independent proposal only; final 18-case review and formal release freezing remain PENDING.'
    proposal['previous_proposal']=ref(previous)
    proposal['ws03_source_archive']=ref(PACKAGE/'archive-index.json')
    proposal['ws03_source_verification']=ref(PACKAGE/'verification-v1.json')
    proposal['images'][3]={
        'id':'WS-03','role':'gallery','file':'images/'+destination.name,
        'caption':'零成长母舰配置：C0／L0，2201.01.07；原生遗迹舰同国同日对照夹具。',
        'source':'../'+source.relative_to(ROOT).as_posix(),
        'status':'LOCAL_READY_PENDING_CASE_REVIEW','evidence_kind':'native_screenshot',
        'game_date':'2201.01.07','native_save':'../'+save.relative_to(ROOT).as_posix(),
        'native_save_date':'2201.01.07','run_id':'20261019T164112Z',
        'notes':'Actual country0 Mother fleet151/ship1044 at C0/L0 and six core ranks0. Clean-v2 actual native panel, not obscured-v1. Same-country/date native reference fleet175/ship1068 is independently bound. Display H93960/A44787/S167310/speed417/damage5598.57 per day; armor native maximum44787.6 is truncated by the UI. Panel damage is not measured battle DPS. This is a post-economy Jan7 configuration fixture, not Jan1 new-game statistics. Actual Mother upkeep tooltip shows10.07 energy and2.88 alloys/month in this reference-fixture naval context; no free-upkeep claim. Added Relic is a test reference, not an opening reward.',
        'width':size[0],'height':size[1],'format':format_name,
        'bytes':destination.stat().st_size,'sha256':ref(source)['sha256'],
        'selection_approved':True,'selection_date':'2026-10-20',
        'current_040_runtime_acceptance_claimed':False,
        'source_configuration_report':ref(PACKAGE/'bounded-configuration-ui-report-v1.json'),
        'superseded_published_entry':deepcopy(old['images'][3]['superseded_published_entry'])}
    assert proposal['status']=='PROPOSED' and proposal['final_release_selection'] is False
    assert all(proposal['images'][i]==old['images'][i] for i in (0,1,2,4,5,6))
    output=ROOT/'docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v3.json'
    write(output,proposal)
    assert before==[ref(p) for p in protected]
    proof={
        'schema':'eep.1020.rc7-ws03-gallery-selection.v1','status':'LOCAL_READY_PENDING_CASE_REVIEW',
        'source':ref(source),'destination':ref(destination),
        'ocr':ref(source.with_suffix('.ocr.json')),
        'native_save':ref(save),'native_save_audit':ref(save.with_suffix('.audit.json')),
        'native_save_receipt':ref(save.with_suffix('.native-save.json')),
        'source_archive':ref(PACKAGE/'archive-index.json'),
        'source_archive_verification':ref(PACKAGE/'verification-v1.json'),
        'source_configuration_report':ref(PACKAGE/'bounded-configuration-ui-report-v1.json'),
        'same_day_native_reference_image':ref(PACKAGE/'raw/r7cfgui-relic-details-clean.jpg'),
        'original_failed_obscured_v1':ref(PACKAGE/'raw/r7cfgui-mother-details-clean.jpg'),
        'proposed_manifest':ref(output),'untouched_inputs':before,
        'actual_zero_growth':{'C':0,'L':0,'six_ranks':[0]*6,'date':'2201.01.07'},
        'actual_displayed_stats':bounded['actual_panels']['mother'],
        'actual_maintenance':bounded['maintenance'],
        'source_package_unchanged':True,'no_case_promoted':True,
        'no_UI_Steam_Git_Mod_tools_or_active_logs':True}
    write(HERE/'selection.json',proof)
    print(json.dumps({'destination':ref(destination),'proposed_manifest':ref(output)}))


if __name__=='__main__':main()
