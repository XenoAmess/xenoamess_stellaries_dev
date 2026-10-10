"""Exact first native attunement notification boundary; no calendar clearance."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-before-attunement1';after='terravore-native-attunement1-pending'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt,br=read(before);a,at,ar=read(after);orig=json.loads((run/(after+'-meditate-year-proof.json')).read_text('utf-8'));ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
bs,ass=[q.block(q.block(rt['situations'],'situations'),'16777221') for rt in [br,ar]]
pending=[q.scalars(v) for k,v,o in q.fields(at) if k=='player_event' and o and q.scalars(v).get('country')==0];prs=[v for k,v,o in q.fields(at) if k=='player_event' and o and q.scalars(v).get('country')==0]
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';on=h.GAME_EXE.parent/'common/on_actions/00_on_actions.txt';src=source.read_text('utf-8-sig');events=[v for k,v,o in q.fields(src) if o and q.scalars(v).get('id')=='shroud.2420'];control=[v for k,v,o in q.fields(src) if o and q.scalars(v).get('id')=='shroud.2200'];assert len(events)==len(control)==1
checks={'bound_original40_exact_two_FAIL_exit1':orig['status']=='FAIL' and len(orig['checks'])==40 and {k for k,v in orig['checks'].items() if not v}=={'no_country0_pending','all_native_breach_raw_except_progress_held'} and ex['returncode']==1,
'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256']==orig['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==orig['after_sha256'],
'calendar_actual_exit0':json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
'actual_native_30_days_progress5_at_stage1':b['date']=='2248.04.02' and a['date']=='2248.05.02' and orig['days']==30 and a['situations']['16777221']['progress']==326.25 and b['situations']['16777221']['progress']==321.25 and a['situations']['16777221']['last_month_progress']==5,
'only_exact_native_attunement_flags_changed':q.scalars(q.block(bs,'flags'))=={'breach_shroud_stage_1_started':63173784,'beneficial_approach':63193224,'breach_shroud_social_event_triggered':63200400} and q.scalars(q.block(ass,'flags'))=={'beneficial_approach':63193224,'shroud.2420_fired':63225600} and omit(bs,{'progress','last_month_progress','flags'})==omit(ass,{'progress','last_month_progress','flags'}),
'exact_one_native_pending_and_scope':not [v for k,v,o in q.fields(bt) if k=='player_event' and o and q.scalars(v).get('country')==0] and pending==[{'id':174,'event':'shroud.2420','date':'2250.08.01','country':0}] and len(prs)==1 and q.scalars(q.block(prs[0],'scope')).get('type')=='situation' and q.scalars(q.block(prs[0],'scope')).get('id')==16777221,
'native_event_immediate_only_own_fired_flag':q.scalars(q.block(events[0],'immediate'))=={'set_situation_flag':'shroud.2420_fired'} and [(k,o) for k,v,o in q.fields(q.block(events[0],'immediate'))]==[('set_situation_flag',False)] and q.scalars(q.block(events[0],'trigger')).get('exists')=='owner' and q.scalars(q.block(q.block(events[0],'trigger'),'NOT'))=={'has_situation_flag':'shroud.2420_fired'},
'native_balanced_pool_contains_event':'shroud.2420' in q.block(on.read_text('utf-8-sig'),'on_breach_the_shroud_situation_random_balanced_events_list'),
'native_control_removes_stage_and_social_flags':set(v for k,v,o in q.fields(q.block(control[0],'immediate')) if k=='remove_situation_flag')=={'breach_shroud_social_event_triggered','breach_shroud_stage_1_started','breach_shroud_stage_2_started','breach_shroud_stage_3_started'} and 'on_breach_the_shroud_situation_random_balanced_events_list' in q.block(control[0],'immediate'),
'EEP_actual_ships_population_boundary_already38true':all(v is True for k,v in orig['checks'].items() if k not in ['no_country0_pending','all_native_breach_raw_except_progress_held'])}
p={'status':'PASS_NATIVE_MEDITATE_ATTUNEMENT_PENDING_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'pending':pending,'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,on]],'scope':'Only original boundary with exact native first attunement flags and pending174. No calendar clearance; original40 FAIL retained.'}
out=run/(after+'-attunement-pending-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original scoped attunement supplement FAIL retained'
