"""Strict independent native integer reward observation; retains original decimal FAIL."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
old=json.loads((run/'terravore-cloud-contact-ack-proof.json').read_text(encoding='utf-8'))
b=json.loads((run/'terravore-active-month24.audit.json').read_text(encoding='utf-8'));a=json.loads((run/'terravore-cloud-contact-ack.audit.json').read_text(encoding='utf-8'))
bc,ac=b['countries']['0'],a['countries']['0'];actual=D(str(ac['effective_stockpile']['influence']))-D(str(bc['effective_stockpile']['influence']))
formula=sum((D(str(v.get('influence',0))) for v in bc['budget_categories']['current_month']['income'].values()),D(0))*6
with zipfile.ZipFile(run/'terravore-cloud-contact-ack.sav') as z:raw=z.read('gamestate').decode('utf-8-sig')
roots={k:v for k,v,o in q.fields(raw) if o};country=q.block(roots['country'],'0');projects=[v for k,v,o in q.fields(q.block(country,'events')) if o and k=='special_project']
cloud=[v for v in projects if q.scalars(v).get('special_project')=='CLOUDS_PROJECT']
contact=q.block(q.block(roots['first_contacts'],'contacts'),'0')
checks={'original_FAIL_exactly_decimal_reward':old['status']=='FAIL' and [k for k,v in old['checks'].items() if not v]==['native_influence_six_months_exact'] and len(old['checks'])==27,
 'same_original_pair_SHA':old['before_sha256']==b['save_sha256']==h.sha256(run/'terravore-active-month24.sav') and old['after_sha256']==a['save_sha256']==h.sha256(run/'terravore-cloud-contact-ack.sav'),
 'actual_integer37_observed':actual==37 and actual==actual.to_integral_value(),
 'within_native_bounds_and_subunit_formula_difference':20<=actual<=80 and D(0)<=formula-actual<D(1),
 'actual_contact0_finished':q.scalars(contact)['status']=='finished' and not q.block(contact,'event'),
 'one_actual_project_at_mother_colony0':len(cloud)==1 and q.scalars(q.block(cloud[0],'scope')).get('type')=='colony' and q.scalars(q.block(cloud[0],'scope')).get('id')==0}
p={'status':'PASS_STRICT_NATIVE_INTEGER_REWARD_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'actual_reward':str(actual),'unrounded_formula':str(formula),'scope':'Original 27-check decimal FAIL retained, other 26 true. Actual +37 native reward and EEP isolation; does not establish general engine rounding rule or retrospectively pass the decimal expectation.'}
out=run/'terravore-cloud-contact-ack-corrections.json';assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values())
