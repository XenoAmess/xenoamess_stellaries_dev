import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(Path(__file__),run/Path(__file__).name)
def center(x):return [round(sum(p[i] for p in x['box'])/4) for i in [0,1]]
f=r.gpu_capture('postvanilla-native-begin-initial-frame')
if any('\u63a5\u89e6\u62a5\u544a' in x['text'] for x in f['rows']):
 rows=[x for x in f['rows'] if x['text'].startswith('\u730e\u7269') and 460<x['box'][0][1]<540];assert len(rows)==1
 r.gpu_click(*center(rows[0]),'postvanilla-native-contact-normal-ack');f=r.gpu_capture('postvanilla-native-contact-acknowledged')
rows=[x for x in f['rows'] if x['text'].startswith('Native-Q20-Boun') and x['box'][0][0]>800];assert len(rows)==1,rows
r.gpu_click(*center(rows[0]),'postvanilla-native-source-select');f=r.gpu_capture('postvanilla-native-source-selected');assert any('Native-Q20' in x['text'] and x['box'][0][0]<300 for x in f['rows'])
r.gpu_click_text('\u51b3\u8bae','postvanilla-native-decisions-open');h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(.6);f=r.gpu_capture('postvanilla-native-decision-row')
rows=[x for x in f['rows'] if x['text']=='\u541e\u566c\u661f\u7403' and x['box'][0][0]>700 and x['box'][0][1]<160];assert len(rows)==1,rows
b=json.loads((run/'postvanilla-source-native-nextday.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/'postvanilla-begin-error-before.log').write_bytes(eb)
r.gpu_click(*center(rows[0]),'postvanilla-native-actual-consume-begin');a=r.native_save('postvanilla-native-Q20-begun',b['date'],(0,));c=lambda x:x['countries']['0'];p=a['planets']['1641'];tasks=[s for s in a['situations'].values() if s.get('type')=='situation_terravore_consume_planet' and s.get('country')==0 and s.get('killed')!='yes'];research={'physics_research','society_research','engineering_research'}
delta={k:[c(b)['stockpile'].get(k),c(a)['stockpile'].get(k)] for k in c(a)['stockpile'].keys()|c(b)['stockpile'].keys() if c(a)['stockpile'].get(k)!=c(b)['stockpile'].get(k)}
checks={'one_native_terravore_task':len(tasks)==1,'native_task_progress0':len(tasks)==1 and tasks[0]['progress']==0,'native_target_source1641':len(tasks)==1 and tasks[0]['target']['id']==1641,'native_Q20_remaining':p['variables']['num_districts_terravore']==20,'being_devoured_native_flag':'being_devoured' in p['flags'],
 'all_real_pop_groups_same':a['pop_groups']==b['pop_groups'],'AP_empty_unchanged':c(a)['ascension_perks']==c(b)['ascension_perks']==[],'technology_same':c(a)['completed_technologies']==c(b)['completed_technologies'],'queues_same':c(a)['research_queues']==c(b)['research_queues'],
 'no_EEP_variables':not any(k.startswith('eep_') for k in c(a)['variables']),'no_EEP_flags':not any(k.startswith('eep_') for k in c(a)['flags']),'all_nonresearch_stock_same':not(set(delta)-research),'no_new_errors':(user/'logs/error.log').read_bytes()==eb}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'full_stock_check':'FAIL' if delta else 'PASS','all_stock_differences':delta,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Actual CN original no-fee decision in enabled_mods=[] process; normal native first-contact acknowledgement also recorded, no EEP adapter or forced progress.'};h.write_json(run/'postvanilla-native-begin-proof.json',v);print(json.dumps(v),flush=True);assert all(checks.values())
