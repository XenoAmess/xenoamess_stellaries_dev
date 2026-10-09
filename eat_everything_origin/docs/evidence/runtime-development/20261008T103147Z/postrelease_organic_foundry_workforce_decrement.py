import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
b=json.loads((run/'organic-foundry-priority-restored-baseline.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture('organic-foundry-before-native-ctrl-decrease')
labels=[v['text'] for v in f['rows']]
assert '\u51b6\u91d1\u5e08' in labels and '\u964d\u4f4e\u5c97\u4f4d\u52b3\u52a8\u529b\u9650\u5236' in labels
h.pyautogui.keyDown('ctrl')
try:h.click_point(673,463,'organic-foundry-ctrl-decrease-one-native-job')
finally:h.pyautogui.keyUp('ctrl')
f=r.gpu_capture('organic-foundry-after-native-ctrl-decrease')
print(json.dumps({'image':str(f['image']),'rows':[v['text'] for v in f['rows']]}),flush=True)
a=r.native_save('organic-foundry-workforce-limited',b['date'],(0,));bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/'organic-foundry-workforce-limited-error-after.log').write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb}
for k in ('stockpile','effective_stockpile','research_stockpile','tech_status','variables','flags','completed_technologies','research_queues','research_progress_by_tech','traditions','ascension_perks','government','native'):
 checks[k+'_held']=bc[k]==ac[k]
for k in ('districts','deposits','situations','species','event_targets','planets'):
 checks[k+'_held']=a[k]==b[k]
checks['colony_population_counts_held']={k:v['actual_pop_sum'] for k,v in b['colonies'].items()}=={k:v['actual_pop_sum'] for k,v in a['colonies'].items()}
bj,aj=b['pop_jobs']['22'],a['pop_jobs']['22']
checks['target_is_mother_foundry']=bj['type']==aj['type']=='foundry' and bj['planet']==aj['planet']==0
checks['one_native_job_limit_800_to_700']=bj['workforce_limit']==800 and aj['workforce_limit']==700
checks['maximum_capacity_800_held']=bj['max_workforce']==aj['max_workforce']==800
changes={section:{k:{'before':b[section].get(k),'after':a[section].get(k)} for k in set(b[section])|set(a[section]) if b[section].get(k)!=a[section].get(k)} for section in ('pop_jobs','pop_groups','colonies')}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'job_before':bj,'job_after':aj,'raw_differences':changes,'scope':'One actual native Ctrl-minus workforce limit step; every changed raw job/group/colony retained. Monthly cost savings pending next month, not a Mod reward or strict reload.'}
h.write_json(run/'organic-foundry-workforce-limited-proof.json',proof)
print(json.dumps({'checks':checks,'job_after':aj,'changed_ids':{k:list(v) for k,v in changes.items()},'sha':a['save_sha256']}),flush=True)
assert all(checks.values()),'Original workforce limit failure preserved'
