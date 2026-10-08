import json,logging,shutil,sys,time,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run()
shutil.copyfile(Path(__file__),run/Path(__file__).name)
def raw(p):
    with zipfile.ZipFile(p) as z:t=z.read('gamestate').decode('utf-8-sig')
    fs=list(q.fields(t));ts={k:v for k,v,o in fs if o}
    planets=q.block(ts['planets'],'planet');core=q.block(planets,'1')
    return {'core':core,'events':[v for k,v,o in fs if k=='player_event' and o]}
def compare(bs,ass,refresh=False):
    b=json.loads((run/(bs+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(ass+'.audit.json')).read_text(encoding='utf-8'))
    br=raw(run/(bs+'.sav'));ar=raw(run/(ass+'.sav'))
    c=lambda x:x['countries']['0']
    planets=all(a['planets'][i]==p for i,p in b['planets'].items() if i!='1')
    bp=dict(b['planets']['1']);ap=dict(a['planets']['1']);bp['variables']=dict(bp['variables'])
    if refresh:bp['variables']['eep_actual_pop']=71270
    checks={'same_date':a['date']==b['date'],'stockpile_including_research':c(a)['stockpile']==c(b)['stockpile'],
      'population_groups':a['pop_groups']==b['pop_groups'],'colonies':a['colonies']==b['colonies'],
      'ledger':c(a)['variables']==c(b)['variables'],'flags':c(a)['flags']==c(b)['flags'],
      'AP':c(a)['ascension_perks']==c(b)['ascension_perks'],'technologies':c(a)['completed_technologies']==c(b)['completed_technologies'],
      'queues':c(a)['research_queues']==c(b)['research_queues'],'situations':a['situations']==b['situations'],
      'event_targets':a['event_targets']==b['event_targets'],'deposits':a['deposits']==b['deposits'],
      'districts':a['districts']==b['districts'],'other_planets':planets,'core_expected_snapshot':bp==ap,
      'one_capacity_and_court':ar['core'].count('modifier="eep_devoured_capacity_multiplier"')==1 and ar['core'].count('modifier="eep_court"')==1,
      'core_values':ap['variables']=={'eep_actual_pop':71270,'eep_capacity_value':1002,'eep_free_districts':1011}}
    proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Controlled Terminator high-capacity Chinese report; not full government acceptance.','allowed_display_cache_refresh':refresh}
    h.write_json(run/(ass+'-readonly-proof.json'),proof)
    print(json.dumps(proof),flush=True);assert all(checks.values())
compare('rc9-highcap-native-before-current-report','rc9-highcap-native-current-report-pending',True)
r.gpu_click_text('\u9000\u4e0b','rc9-highcap-native-current-report-close')
f=r.gpu_capture('rc9-highcap-native-current-mother-row')
choices=[x for x in f['rows'] if x['text']=='EEP-Core' and min(p[0] for p in x['box'])>850 and 280<sum(p[1] for p in x['box'])/4<300]
assert len(choices)==1,choices
x=choices[0];r.gpu_click(round(sum(p[0] for p in x['box'])/4),round(sum(p[1] for p in x['box'])/4),'rc9-highcap-native-repeat-mother-open')
h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(1)
r.gpu_capture('rc9-highcap-native-current-mother-capacity-unobstructed')
r.gpu_click_text('\u89d0\u89c1\u5973\u738b','rc9-highcap-native-repeat-report-button')
h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(1)
r.gpu_capture('rc9-highcap-native-repeat-report-unobstructed')
r.native_save('rc9-highcap-native-repeat-report-pending','2200.02.02',(0,))
compare('rc9-highcap-native-current-report-pending','rc9-highcap-native-repeat-report-pending')
source=run/'rc9-highcap-native-repeat-report-pending.sav';alias=user/'save games/acceptance-fixtures/cap100-report.sav'
alias.parent.mkdir(parents=True,exist_ok=True);assert not alias.exists();shutil.copyfile(source,alias)
assert h.sha256(alias)==h.sha256(source)
h.write_json(run/'rc9-highcap-native-repeat-report-alias.json',{'source':str(source),'alias':str(alias),'sha256':h.sha256(alias)})
r.native_load('cap100-report','rc9-highcap-native-report-byte-reload')
h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(1)
f=r.gpu_capture('rc9-highcap-native-reloaded-report-unobstructed')
rows=' '.join(x['text'] for x in f['rows'])
assert all(str(v) in rows for v in [4000,1002,66600,71270,1011]),rows
r.native_save('rc9-highcap-native-report-reloaded','2200.02.02',(0,))
compare('rc9-highcap-native-repeat-report-pending','rc9-highcap-native-report-reloaded')
