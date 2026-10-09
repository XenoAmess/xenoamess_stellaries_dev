"""Bind the sole original wait FAIL to five genuinely expired native messages."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-generator3-paid';after='terravore-paid-economy-year1'
proof=json.loads((run/(after+'-paid-wait-proof.json')).read_text('utf-8'))
audits=[];messages=[]
for stem in [before,after]:
 audits.append(json.loads((run/(stem+'.audit.json')).read_text('utf-8')))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 messages.append([q.scalars(v) for k,v,o in q.fields(t) if k=='message' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD'])
b,a=audits;bm,am=messages
checks={'original_unique_FAIL_retained':proof['status']=='FAIL' and [k for k,v in proof['checks'].items() if not v]==['no_new_bite_message'],
 'both_original_SHA_bound':h.sha256(run/(before+'.sav'))==b['save_sha256']==proof['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==proof['after_sha256'],
 'exact_five_final_messages':len(bm)==5 and all(x['date']=='2210.04.02' and x['end']=='2210.07.02' and x['target_planet']==90 for x in bm),
 'all_five_expired_during_this_calendar':all(b['date']<x['end']<a['date'] for x in bm),
 'no_message_after_and_no_new_message':am==[],
 'all_other_original19_true':len(proof['checks'])==20 and sum(proof['checks'].values())==19}
p={'status':'PASS_SCOPED_EXPIRED_MESSAGE_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_native_messages_before_after':messages,'scope':'Only five expired original notifications; original wait FAIL unchanged. No full route or long-term economy claim.'}
out=run/(after+'-expired-message-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values())
