import json, logging, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
assert m['version']=='0.2.0';shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-purifier-2287-farm-nextmonth';stage='organic-purifier-2287-real-devour-begin'
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
h.pyautogui.moveTo(*r.desktop_point(648,625));time.sleep(.5)
f=r.gpu_capture(stage+'-actual-decision');rows=[x for x in f['rows'] if x['text']=='\u541e\u566c\uff1a\u732e\u4e8e\u552f\u4e00\u738b\u5ea7' and 115<x['box'][0][1]<150]
assert len(rows)==1,'Actual native decision row unavailable';row=rows[0];box=row['box']
h.click_point(round(sum(p[0] for p in box)/4),round(sum(p[1] for p in box)/4),stage+'-actual-click')
f=r.gpu_capture(stage+'-after-click');print(json.dumps({'labels':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
a=r.native_save(stage,b['date'],(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
cb,ca=b['countries']['0'],a['countries']['0'];source=a['planets']['1855'];active=[(k,v) for k,v in a['situations'].items() if v.get('type')=='situation_eep_devouring']
checks={'same_actual_date':a['date']==b['date'],'source_Q11_T27':source['variables'].get('eep_q')==11 and source['variables'].get('eep_months')==27,'source_active': 'eep_active' in source['flags'],'source_owned':source.get('owner')==source.get('controller')==0,'one_native_situation_progress_zero':len(active)==1 and active[0][1].get('progress')==0,'all_stock_same':ca['stockpile']==cb['stockpile'],'EEP_country_ledger_no_early_reward':ca['variables']==cb['variables'],'no_new_errors':eb==ea}
for k in ('completed_technologies','research_queues','traditions','ascension_perks','government'):checks[k+'_same']=ca[k]==cb[k]
for k in ('pop_groups','pop_jobs','colonies','districts','deposits','species'):checks[k+'_same']=a[k]==b[k]
checks['other_planets_same']={k:v for k,v in a['planets'].items() if k!='1855'}=={k:v for k,v in b['planets'].items() if k!='1855'}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'source_before':b['planets']['1855'],'source_after':source,'actual_situations':active,'scope':'Actual existing owned Q11 source decision only. No seeding required, no calendar or grants; completion and Queen notification pending.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps({k:v for k,v in proof.items() if k not in ('source_before','source_after')},ensure_ascii=False),flush=True)
assert all(checks.values()),'Original native decision FAIL retained'
