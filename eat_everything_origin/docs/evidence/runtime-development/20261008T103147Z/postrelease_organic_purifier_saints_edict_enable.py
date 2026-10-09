import json,logging,re,shutil,sys,zipfile
from decimal import Decimal,ROUND_CEILING
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-mining-subsidy-revoked';stage='organic-saints-edict-adopted';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-control');labels=[x['text'] for x in f['rows']];assert '\u656c\u5949\u5723\u4eba' in labels and '91/139' in labels and b['countries']['0']['stockpile']['unity']>31
h.click_point(503,247,stage+'-actual-enable-click');f=r.gpu_capture(stage+'-after-click');print(json.dumps({'labels':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-final.log')).write_bytes(ea)
def edicts(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 raw=q.block(q.block(q.block(t,'country'),'0'),'edicts');return [q.scalars(x) for x in re.findall(r'\{([^{}]*)\}',raw)]
be,ae=edicts(start),edicts(stage);paid=Decimal(str(cb['stockpile']['unity']))-Decimal(str(ca['stockpile']['unity']))
checks={'same_actual_date':a['date']==b['date'],'only_saints_edict_added':be==[x for x in ae if x.get('edict')!='veneration_of_saints'] and len(ae)==len(be)+1,'farming_edict_kept':any(x.get('edict')=='farming_subsidies' for x in ae),'native_unity_cost_positive_affordable_UI31':0<paid<=Decimal(str(cb['stockpile']['unity'])) and paid.to_integral_value(rounding=ROUND_CEILING)==31,'all_other_stock_same':{k:v for k,v in ca['stockpile'].items() if k!='unity'}=={k:v for k,v in cb['stockpile'].items() if k!='unity'},'EEP_ledger_same':ca['variables']==cb['variables'],'EEP_flags_same':ca['flags']==cb['flags'],'actual_population_identity_amount_same':{k:{n:g.get(n) for n in ('planet','key','size')} for k,g in a['pop_groups'].items()}=={k:{n:g.get(n) for n in ('planet','key','size')} for k,g in b['pop_groups'].items()},'native_job_types_base_and_capacity_same':{k:{n:g.get(n) for n in ('type','planet','workforce','max_workforce')} for k,g in a['pop_jobs'].items()}=={k:{n:g.get(n) for n in ('type','planet','workforce','max_workforce')} for k,g in b['pop_jobs'].items()},'no_new_errors':eb==ea}
for k in ('completed_technologies','research_queues','traditions','ascension_perks','government'):checks[k+'_same']=ca[k]==cb[k]
for k in ('planets','districts','deposits','situations','species'):checks[k+'_same']=a[k]==b[k]
def queue(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return q.block(q.block(q.block(q.block(t,'construction'),'queue_mgr'),'queues'),'0')
checks['paid_farm_queue_same']=queue(start)==queue(stage)
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_edicts_before':be,'native_edicts_after':ae,'actual_unity_paid':str(paid),'all_stock_changes':{k:[cb['stockpile'].get(k),v] for k,v in ca['stockpile'].items() if cb['stockpile'].get(k)!=v},'scope':'Native affordable Saints activation; future monthly budget improvement not yet established.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original edict activation FAIL retained'
