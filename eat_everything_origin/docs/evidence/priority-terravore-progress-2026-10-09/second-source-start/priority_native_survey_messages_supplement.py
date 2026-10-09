"""Bind original FAIL to removal of exactly two acknowledged event notices."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-synchronicity-year4';after='terravore-survey-events-ack'
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,list(q.fields(t))
b,bf=read(before);a,af=read(after);original=json.loads((run/(after+'-survey-events-proof.json')).read_text('utf-8'))
bm=[v for k,v,o in bf if k=='message'];am=[v for k,v,o in af if k=='message'];removed=[v for v in bm if q.scalars(v).get('event') in [54,60]]
skip=['player_event','open_player_event_selection_history','first_contacts','message']
checks={
 'bound_exact_original_one_FAIL_other26_true':len(original['checks'])==27 and [k for k,v in original['checks'].items() if not v]==['all_other_top_level_fields_raw_held'] and original['status']=='FAIL',
 'bound_original_SHA_pair':original['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and original['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'same_actual_date':a['date']==b['date']=='2223.01.02',
 'all_other_top_level_fields_raw_held':[(k,v,o) for k,v,o in bf if k not in skip]==[(k,v,o) for k,v,o in af if k not in skip],
 'exact_two_original_event_notices':[(q.scalars(v).get('receiver'),q.scalars(v).get('event'),q.scalars(v).get('type')) for v in removed]==[(0,54,'EVENT_MESSAGE_TYPE'),(0,60,'MESSAGE_TERRAFORM_CANDIDATE_FOUND')],
 'all_other_messages_exact_held':am==[v for v in bm if v not in removed],
 'two_confirmed_event_notices_absent':not any(q.scalars(v).get('event') in [54,60] for v in am),
}
p={'status':'PASS_EXACT_ACKNOWLEDGED_TWO_NOTICE_REMOVAL' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'removed_original_messages':removed,'scope':'Original FAIL retained; exact informational notice removal only, no replay or full route.'}
out=run/(after+'-messages-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Exact supplement FAIL retained; no next action'
