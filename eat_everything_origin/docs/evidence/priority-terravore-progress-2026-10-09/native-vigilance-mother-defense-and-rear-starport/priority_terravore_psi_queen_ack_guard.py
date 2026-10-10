"""Normal Queen EEP30 acknowledgement: all other ordered raw state held."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-psi-queen-pending';after='terravore-native-psi-queen-ack'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt=read(before);a,at=read(after);pre=json.loads((run/(before+'-psi-notice-month-proof.json')).read_text('utf-8'));bound=json.loads((run/(before+'-psi-notice-boundary-v2-proof.json')).read_text('utf-8'))
bp,ap=vals(bt,'player_event'),vals(at,'player_event');target=[v for v in bp if q.scalars(v)=={'id':202,'event':'eep.30','date':'2261.01.01','country':0}]
bm,am=vals(bt,'message'),vals(at,'message');removed=[v for v in bm if q.scalars(v).get('event')==202 and q.scalars(v).get('receiver')==0]
source=Path('eat_everything_origin/mod/events/eep_events.txt');ev=[(k,v) for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='eep.30'];assert len(ev)==1
checks={
 'bound_prior17_month_and45_boundary_PASS_exit0':pre['status'].startswith('PASS') and bound['status']=='PASS_TERRAVORE_FIRST_PSI_NOTICE_BOUNDARY_COMPONENT' and len(pre['checks'])==17 and len(bound['checks'])==45 and all(v is True for v in pre['checks'].values()) and all(v is True for v in bound['checks'].values()) and pre['after_sha256']==bound['after_sha256']==b['save_sha256'] and all(json.loads((run/(before+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-month-guard','-guard-v2']),
 'same_date_original_SHA_pair':b['date']==a['date']=='2258.10.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'only_unique202_pending_removed_no_new_country0_pending':len(target)==1 and ap==[v for v in bp if v not in target] and not [v for v in ap if q.scalars(v).get('country')==0],
 'exact_once_human1_option0_history':selected_history(at)==selected_history(bt)+[{'player_event':202,'human':1,'option':0}],
 'only_corresponding_message_removed':len(removed)==1 and am==[v for v in bm if v not in removed],
 'all_other_ordered_top_raw_held':omit(bt,{'player_event','message','open_player_event_selection_history'})==omit(at,{'player_event','message','open_player_event_selection_history'}),
 'native_country_scope_and_EEP_notification_only_name_option':ev[0][0]=='country_event' and len(vals(ev[0][1],'option'))==1 and list(q.fields(vals(ev[0][1],'option')[0]))==[('name','eep.30.a',False)] and not q.block(ev[0][1],'immediate') and not q.block(ev[0][1],'after'),
 'normal_click_save_exit0':all(json.loads((run/(after+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-select','-save']) and json.loads((run/(after+'-select.action.json')).read_text('utf-8'))['client_point']==[510,545],
 'unfiltered_errors_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_TERRAVORE_QUEEN_PSI_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':not [v for v in ap if q.scalars(v).get('country')==0],'eep_source':{'path':str(source.resolve()),'sha256':h.sha256(source)},'scope':'Normal once-only EEP30 acknowledgement after real full breach, all other ordered raw held. No free rewards. Repeat report/stable month/long regression remain.'}
out=run/(after+'-psi-queen-ack-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original Queen ACK FAIL retained'
