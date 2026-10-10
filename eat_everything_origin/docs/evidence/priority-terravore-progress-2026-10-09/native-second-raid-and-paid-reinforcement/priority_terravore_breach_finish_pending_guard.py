"""Exact native1000 cap/lock/pending201, not yet completed Shroud breach."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-before-breach-finish';after='terravore-native-breach-finish-pending'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt,br=read(before);a,at,ar=read(after);old=json.loads((run/(after+'-meditate-stage3-proof.json')).read_text('utf-8'));ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
failed={'no_country0_pending','one_native_breach_stage3_progress_only','actual_meditate_exact_observed_rate_per_month','all_native_breach_raw_except_progress_held'}
bs,ass=[q.block(q.block(rt['situations'],'situations'),'16777221') for rt in [br,ar]]
pending=[v for k,v,o in q.fields(at) if k=='player_event' and q.scalars(v).get('country')==0];assert len(pending)==1
scope=q.block(pending[0],'scope');local=q.block(q.block(scope,'from'),'saved_event_target');animator=q.block(ar['country'],'33')
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';situ=h.GAME_EXE.parent/'common/situations/13_shroud_situations.txt'
events=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2800'];assert len(events)==1
control=q.block(q.block(situ.read_text('utf-8-sig'),'situation_breach_shroud'),'on_progress_complete');imm=q.block(events[0],'immediate');rc=q.block(imm,'random_country')
checks={
 'bound_original42_exact4FAIL_exit1_other38true':old['status']=='FAIL' and len(old['checks'])==42 and {k for k,v in old['checks'].items() if not v}==failed and ex['returncode']==1,
 'original_SHA_pair':old['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and old['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'actual_unique30day_calendar_exit0':old['days']==30 and b['date']=='2258.08.02' and a['date']=='2258.09.02' and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'exact_native1000_cap_and_last_month_rate':D(str(b['situations']['16777221']['progress']))==D('997.2917') and D(str(a['situations']['16777221']['progress']))==min(D('1000'),D('997.2917')+D('5.2093')) and a['situations']['16777221']['last_month_progress']==5.2093,
 'only_exact_locked_and_progress_change':q.scalars(ass).get('locked')=='yes' and 'locked' not in q.scalars(bs) and omit(bs,{'progress','locked'})==omit(ass,{'progress','locked'}),
 'only_unique201_native_pending_scope_expiry':not [v for k,v,o in q.fields(bt) if k=='player_event' and q.scalars(v).get('country')==0] and q.scalars(pending[0])=={'id':201,'event':'shroud.2800','date':'2260.12.01','country':0} and q.scalars(scope).get('type')=='situation' and q.scalars(scope).get('id')==16777221,
 'local_animator_target_matches_actual_native_country33':q.scalars(local)=={'type':'country','id':33,'opener_id':4294967295,'name':'the_animator_of_clay'} and q.scalars(animator).get('type')=='shroud' and 'animator_of_clay_country_flag' in q.scalars(q.block(animator,'flags')),
 'native_on_complete_source_only_event_and_lock':[(k,o) for k,v,o in q.fields(control)]==[('custom_tooltip',False),('hidden_effect',True),('set_situation_locked',False)] and q.scalars(q.block(q.block(control,'hidden_effect'),'situation_event'))=={'id':'shroud.2800'} and q.scalars(control).get('set_situation_locked')=='yes',
 'native2800_immediate_only_animator_local_target':[(k,o) for k,v,o in q.fields(imm)]==[('random_country',True)] and q.scalars(q.block(rc,'limit'))=={'is_country_type':'shroud','has_country_flag':'animator_of_clay_country_flag'} and q.scalars(rc)=={'save_event_target_as':'the_animator_of_clay'},
 'native_breach_flag_and_EEP_notice_not_yet_present':'breached_shroud' not in q.scalars(q.block(q.block(ar['country'],'0'),'flags')) and old['checks']['no_early_EEP_psi_or_notice'] is True,
}
p={'status':'PASS_NATIVE_TERRAVORE_BREACH_FINISH_PENDING_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,situ]],'scope':'Exact1000 cap, locked situation and native201 pending. Actual breach requires normal option and native after; no Queen notification/full-route claim.'}
out=run/(after+'-finish-pending-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original finish pending FAIL retained'
