import json
from pathlib import Path
import shutil
import sys
import zipfile
sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
dest=run/Path(__file__).name
assert not dest.exists()
shutil.copyfile(Path(__file__),dest)
before=json.loads((run/'rc9-native-heavy-industry800-paid.audit.json').read_text(encoding='utf-8'))
after=json.loads((run/'rc9-hiveworld-heavy-industry-natural-complete.audit.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(run/'rc9-hiveworld-heavy-industry-natural-complete.sav') as z:
 text=z.read('gamestate').decode('utf-8-sig')
roots={k:v for k,v,b in q.fields(text) if b and k in ('construction','zones')}
queue=q.block(q.block(q.block(roots['construction'],'queue_mgr'),'queues'),'0')
zone_ids=after['districts']['113']['zones']
zones=[q.scalars(q.block(roots['zones'],str(i))) for i in zone_ids]
def job(a,kind):
 return next(a['pop_jobs'][str(i)] for i in a['colonies']['0']['pop_jobs'] if a['pop_jobs'][str(i)]['type']==kind)
ui=json.loads((run/'rc9-native-hive-heavy-industry-complete-ui.ocr.json').read_text(encoding='utf-8'))
labels=[x['text'] for x in ui['rows']]
b,a=before['countries']['0'],after['countries']['0']
checks={
 'actual_calendar_220_days':after['date']=='2319.10.22',
 'original_native_queue_finished':not q.ids(q.block(queue,'items')),
 'original_physical_mother_owner0':after['planets']['1'].get('colony')==0 and after['planets']['1'].get('owner')==0,
 'one_native_hive_foundry':zones==[{'type':'zone_foundry_hive'}],
 'same_six_districts':after['districts']['113']['level']==6,
 'same_total34':sum(after['districts'][str(i)]['level'] for i in after['colonies']['0']['districts'])==34,
 'native_fabricator_capacity_plus3600':job(after,'fabricator')['max_workforce']-job(before,'fabricator')['max_workforce']==3600,
 'actual_fabricator_workforce_zero':job(after,'fabricator')['workforce']==0,
 'eep_ledger_kept':all(a['variables'][k]==b['variables'][k] for k in ('eep_c','eep_g','eep_d','eep_made','eep_worlds')),
 'core_binding_kept':after['event_targets']==before['event_targets'],
 'one_core_deposit':sum(after['deposits'][str(i)]['type']=='d_eep_core' for i in after['planets']['1']['deposits'])==1,
 'ui_capacity37':all(t in labels for t in ('19/37','9/37','6/37')),
 'ui_native_foundry_and_node':all(t in labels for t in ('\u94f8\u9020\u96c6\u7fa4','\u5236\u9020\u8282\u70b9')),
}
result={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','scope':'Actual native paid foundry completion after220 calendar days, capacity and UI. Wartime empty jobs are not full employment or peace economy.','save_sha256':after['save_sha256'],'checks':checks,'ui_image_sha256':ui['image_sha256'],'actual_foundry_job':job(after,'fabricator'),'actual_population':after['colonies']['0']['actual_pop_sum'],'district_maintenance':a['budget_categories']['last_month']['expenses'].get('planet_districts_cities'),'budget_categories':a['budget_categories'],'stockpile':a['stockpile']}
(run/'rc9-native-heavy-industry-completed-proof.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':checks,'save_sha256':after['save_sha256']},ensure_ascii=True))
assert all(checks.values())
