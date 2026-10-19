"""Prepare three unedited local gallery candidates and an independent v2 draft."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import shutil
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
        f.write('\n')


def ref(path):
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':digest(path),'bytes':path.stat().st_size}


def main():
    untouched = [ROOT/p for p in ('VERSION','mod/descriptor.mod','CHANGELOG.md',
        'workshop/description.bbcode','workshop/images-manifest.json',
        'workshop/images/06-purifier-single-homeworld-0.4.0-2201.jpg',
        'docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v1.json')]
    original = [ref(p) for p in untouched]
    old_path = untouched[-1]
    previous = read(old_path)
    proposal = deepcopy(previous)
    proposal.update({'purpose':'Independent RC7 proposal only. Three unedited local sources prepared; WS03 and final case review remain PENDING.',
        'previous_proposal':ref(old_path),'status':'PROPOSED','final_release_selection':False,
        'ws06_selection_approved':True,'selection_date':'2026-10-20',
        'actual_media_archive':ref(HERE/'index.json')})
    definitions = (
        ('WS-04','04-mothership-growth-stress-0.4.0.jpg',
         ROOT/'docs/evidence/1020-rc7-high-level-ui-v1/raw/r7ev-mother-details-clean.jpg',
         ROOT/'docs/evidence/1020-rc7-high-level-ui-v1/raw/r7evready.sav','2202.08.07',
         '成长压力测试：L2050母舰实际属性面板（人为构造，非开局数值）。',
         'Controlled C20500/L2050 pressure branch after deferred rewards and six-day native cache refresh. Not natural campaign growth, opening stats, first-year economy or measured battle DPS.'),
        ('WS-05','05-growth-report-stress-0.4.0.jpg',
         ROOT/'docs/evidence/1020-rc7-high-level-ui-v1/raw/r7ev-report-top.jpg',
         ROOT/'docs/evidence/1020-rc7-high-level-ui-v1/raw/r7evreport.sav','2202.08.07',
         '成长压力测试：C20500／L2050，六核心累计410次随机升级，待补0。',
         'Controlled pressure fixture, not natural campaign or opening stats. Native report six ranks shield/armor/hull/damage/tracking/regen=63/74/76/63/56/78. Report display caches changed; economic business state unchanged, full raw strict equality is not claimed.'),
        ('WS-06','06-purifier-single-homeworld-0.4.0-rc7-2201.jpg',
         HERE/'raw/r7pucmedia-single-colony-clean.jpg',HERE/'raw/r7pucmedia.sav','2201.01.01',
         '实机验收预设：种族洁癖单母星，首年12个月净电均为正；2201.01.01，殖民地1。',
         'Actual RC7 Purifier acceptance preset, after the independent twelve-month economy boundary. Frame shows one relic colony, rounded +46 and empty construction queue. The twelve positive monthly budgets are separately sealed in docs/evidence/1019-rc7-economy/purifier/native-branch-report.json; four operation constraints remain separately reviewed. Native popup acknowledgements subsequently added minerals/research and a crisis special project; media save is not strict-equal to yearUI. Parent follow-up assertion failed after this media save; parent exit0 not claimed.'))
    copies=[]
    for identity,name,source,save,date,caption,notes in definitions:
        destination=ROOT/'workshop/images'/name
        assert not destination.exists(),destination
        before=digest(source)
        shutil.copyfile(source,destination)
        assert digest(destination)==before==digest(source)
        with Image.open(destination) as img:
            size,format_name=img.size,img.format
            img.verify()
        assert destination.stat().st_size<1_000_000
        old=next(e for e in proposal['images'] if e['id']==identity)
        historic=deepcopy(old)
        entry={'id':identity,'file':'images/'+name,'role':'gallery','caption':caption,
            'source':'../'+source.relative_to(ROOT).as_posix(),
            'status':'LOCAL_READY_PENDING_CASE_REVIEW','evidence_kind':'native_screenshot',
            'game_date':date,'native_save':'../'+save.relative_to(ROOT).as_posix(),
            'native_save_date':date,'run_id':'20261019T164112Z','notes':notes,
            'width':size[0],'height':size[1],'format':format_name,
            'bytes':destination.stat().st_size,'sha256':before,
            'selection_approved':True,'selection_date':'2026-10-20',
            'current_040_runtime_acceptance_claimed':False,
            'superseded_published_entry':historic.get('superseded_published_entry',historic)}
        if identity=='WS-06':
            entry['superseded_local_rc6_candidate']=historic
            entry['separate_annual_economy_report']=ref(ROOT/'docs/evidence/1019-rc7-economy/purifier/native-branch-report.json')
            entry['post_economy_media_observation']=ref(HERE/'media-observation.json')
        proposal['images'][proposal['images'].index(old)]=entry
        copies.append({'id':identity,'source':ref(source),'destination':ref(destination),
                       'native_save':ref(save),'raw_bytes_identical':True})
    assert len({e['destination']['sha256'] for e in copies})==3
    assert [ref(p) for p in untouched]==original
    output=ROOT/'docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v2.json'
    write(output,proposal)
    write(HERE/'local-media-selection.json',{'schema':'eep.1020.rc7-three-local-gallery-candidates.v1',
        'status':'THREE_UNEDITED_CANDIDATES_READY_NOT_FORMAL_RELEASE',
        'copies':copies,'proposed_manifest':ref(output),'untouched_inputs':original,
        'official_inputs_unchanged':True,'previous_v1_unchanged':True,
        'ws03_status':'PENDING_NATIVE_SOURCE','all_cases_status':'PENDING',
        'UI_Steam_Git_Mod_tools_operations':False})
    print(json.dumps({'copied_images':len(copies),'proposal':ref(output)}))


if __name__=='__main__':
    main()
