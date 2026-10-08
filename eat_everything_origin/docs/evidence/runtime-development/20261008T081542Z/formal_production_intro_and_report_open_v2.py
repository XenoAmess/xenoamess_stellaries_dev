import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0'
shutil.copyfile(Path(__file__),run/Path(__file__).name)
b=json.loads((run/'formal-prod-native-intro-pending.audit.json').read_text(encoding='utf-8'))
eb=(user/'logs/error.log').read_bytes()
def events(stem):
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return [v for k,v,o in q.fields(t) if k=='player_event' and o]
f=r.gpu_capture('formal-prod-intro-before-ack');option='\u738b\u5ea7\u4e4b\u5916\uff0c\u7686\u53ef\u541e\u566c\u3002'
rows=[x for x in f['rows'] if h.normalized(x['text'])==h.normalized(option) and x['box'][0][1]>500];assert len(rows)==1
box=rows[0]['box'];r.gpu_click(round((box[0][0]+box[2][0])/2),round((box[0][1]+box[2][1])/2),'formal-prod-intro-normal-option')
a=r.native_save('formal-prod-intro-acknowledged',b['date'],(0,));c=lambda x:x['countries']['0']
checks={'same_date':a['date']==b['date'],'all_stock_same':c(a)['stockpile']==c(b)['stockpile'],'all_pop_groups_same':a['pop_groups']==b['pop_groups'],
 'all_EEP_variables_same':c(a)['variables']==c(b)['variables'],'all_EEP_flags_same':c(a)['flags']==c(b)['flags'],'AP_unchanged_empty':c(a)['ascension_perks']==c(b)['ascension_perks']==[],
 'traditions_same':c(a).get('traditions')==c(b).get('traditions'),'technology_same':c(a)['completed_technologies']==c(b)['completed_technologies'],'queues_same':c(a)['research_queues']==c(b)['research_queues'],
 'colonies_same':a['colonies']==b['colonies'],'planets_same':a['planets']==b['planets'],'districts_same':a['districts']==b['districts'],'deposits_same':a['deposits']==b['deposits'],'situations_same':a['situations']==b['situations'],
 'only_intro_ack':events('formal-prod-intro-acknowledged')==[x for x in events('formal-prod-native-intro-pending') if q.scalars(x).get('event')!='eep.10'],'no_new_errors':(user/'logs/error.log').read_bytes()==eb}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Final production normal intro acknowledgement, same-day exact economic state, no grants.'};h.write_json(run/'formal-prod-intro-ack-proof.json',v);print(json.dumps(v),flush=True);assert all(checks.values())
f=r.gpu_capture('formal-prod-mother-outliner');rows=[x for x in f['rows'] if x['text']=='EEP-Core' and x['box'][0][0]>850 and 220<x['box'][0][1]<260];assert len(rows)==1
box=rows[0]['box'];r.gpu_click(round((box[0][0]+box[2][0])/2),round((box[0][1]+box[2][1])/2),'formal-prod-mother-native-open')
f=r.gpu_capture('formal-prod-mother-native-panel');h.write_json(run/'formal-prod-mother-native-panel-summary.json',{'image':f['image'],'rows':[x['text'] for x in f['rows']]})
r.native_save('formal-prod-report-before',b['date'],(0,))
print('NATIVE_MOTHER_BASELINE_SAVED',flush=True)
