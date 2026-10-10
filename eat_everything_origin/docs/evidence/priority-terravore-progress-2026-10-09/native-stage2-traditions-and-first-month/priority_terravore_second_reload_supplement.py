"""Strict one-field second-reload supplement; neither original raw FAIL is rewritten."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-queen-notice-reloaded';after='terravore-queen-notice-reloaded2'
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'));old=json.loads((run/(after+'-proof.json')).read_text(encoding='utf-8'))
bb,ab=b['countries']['0']['budget'],a['countries']['0']['budget'];bw,aw=q.block(bb,'income_high_water_mark'),q.block(ab,'income_high_water_mark')
checks={'original24_FAIL_exactly_budget':old['status']=='FAIL' and len(old['checks'])==24 and [k for k,v in old['checks'].items() if not v]==['budget_held'],
 'original_pair_SHA':old['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and old['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'same_date_actual':b['date']==a['date']=='2210.05.01',
 'highwater_exact_length7_to8':q.scalars(bw).get('length')==7 and q.scalars(aw).get('length')==8,
 'every_other_highwater_field_held':[(k,v,o) for k,v,o in q.fields(bw) if k!='length']==[(k,v,o) for k,v,o in q.fields(aw) if k!='length'],
 'budget_outside_highwater_raw_held':bb.replace(bw,'__EXACT_HIGHWATER__',1)==ab.replace(aw,'__EXACT_HIGHWATER__',1),
 'current_and_last_month_raw_held':all(q.block(bb,k)==q.block(ab,k) for k in ['current_month','last_month']),
 'first_reload_FAIL_retained':json.loads((run/'terravore-queen-notice-reloaded-proof.json').read_text(encoding='utf-8'))['status']=='FAIL'}
p={'status':'PASS_SECOND_RELOAD_SCOPED_NO_REWARD_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Original second raw24 retains23 true/one budget FAIL; exactly high-water history length7 to8. No first-reload root-cause or full strict/full-route acceptance claim.'}
out=run/(after+'-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values())
