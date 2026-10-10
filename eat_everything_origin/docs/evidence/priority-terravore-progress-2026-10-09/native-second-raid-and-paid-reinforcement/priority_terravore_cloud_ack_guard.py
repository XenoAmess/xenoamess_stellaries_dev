"""Read-only normal Void Cloud first-contact option and isolated EEP state."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-active-month24';after='terravore-cloud-contact-ack'
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 return a,t,roots,[q.scalars(v) for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
b,bt,br,bp=read(before);a,at,ar,ap=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bn,an=q.block(br['country'],'0'),q.block(ar['country'],'0')
bf,af=q.scalars(q.block(bn,'flags')),q.scalars(q.block(an,'flags'))
influence=D(str(ac['effective_stockpile']['influence']))-D(str(bc['effective_stockpile']['influence']))
contacts=q.block(ar['first_contacts'],'contacts');contact0=q.block(contacts,'0')
pos=at.find('CLOUDS_PROJECT')
checks={'same_actual_date':a['date']==b['date']=='2208.11.02','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'only_expected_pending13_removed':[(v['id'],v['event']) for v in bp]==[(13,'first_contact_critters.85')] and not ap,
 'normal_option_once_history':selected_history(at)==selected_history(bt)+[{'player_event':13,'human':1,'option':1}],
 'native_influence_six_months_exact':abs(influence-D('37.0518'))<D('0.00002'),
 'other_true_stock_and_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='influence'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='influence'},
 'native_cloud_and_completed20_flags_added':all(k not in bf and k in af for k in ['void_clouds_encountered','first_contact_completed20']),
 'native_special_project_enabled_once':'CLOUDS_PROJECT' not in bt and at.count('CLOUDS_PROJECT')==1,
 'native_contact0_no_pending_event':not contact0 or not q.block(contact0,'event'),
 'original_task24_held':a['situations'].get('16777223')==b['situations'].get('16777223') and a['situations']['16777223']['progress']==24,
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-active-month24-error-before.log').read_bytes()}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_CLOUD_CONTACT_EEP_ISOLATION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_influence_reward':str(influence),'actual_contact0_scalars':q.scalars(contact0) if contact0 else None,'native_country_added_flags':{k:v for k,v in af.items() if k not in bf},'native_project_excerpt':at[max(0,pos-300):pos+700] if pos>=0 else None,'scope':'One normal Void Cloud completion option, real native influence/project and strict EEP/economic isolation. No project research completion, full route or global diplomatic-state identity claim.'}
out=run/(after+'-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original native contact ACK FAIL retained; no replay'
