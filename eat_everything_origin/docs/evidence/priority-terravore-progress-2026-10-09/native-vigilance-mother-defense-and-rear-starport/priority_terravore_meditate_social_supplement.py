"""Read-only scoped native social notification boundary; no calendar clearance."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-breach-meditate';after='terravore-native-meditate-year1'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt,br=read(before);a,at,ar=read(after);orig=json.loads((run/(after+'-meditate-year-proof.json')).read_text('utf-8'));ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
bs,ass=[q.block(q.block(rt['situations'],'situations'),'16777221') for rt in [br,ar]]
pending=[q.scalars(v) for k,v,o in q.fields(at) if k=='player_event' and o and q.scalars(v).get('country')==0];prs=[v for k,v,o in q.fields(at) if k=='player_event' and o and q.scalars(v).get('country')==0]
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';on=h.GAME_EXE.parent/'common/on_actions/00_on_actions.txt';events=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2625'];assert len(events)==1
checks={'bound_original40_exact_two_FAIL_exit1':orig['status']=='FAIL' and len(orig['checks'])==40 and {k for k,v in orig['checks'].items() if not v}=={'no_country0_pending','all_native_breach_raw_except_progress_held'} and ex['returncode']==1,
'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256']==orig['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==orig['after_sha256'],
'calendar_actual_exit0':json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
'actual_native_progress60_at_stage1':b['date']=='2244.08.02' and a['date']=='2245.08.02' and a['situations']['16777221']['progress']==161.25 and b['situations']['16777221']['progress']==101.25 and a['situations']['16777221']['last_month_progress']==5,
'only_exact_social_flag_added':q.scalars(q.block(bs,'flags'))=={'breach_shroud_stage_1_started':63173784,'beneficial_approach':63193224} and q.scalars(q.block(ass,'flags'))=={'breach_shroud_stage_1_started':63173784,'beneficial_approach':63193224,'breach_shroud_social_event_triggered':63200400} and omit(bs,{'progress','last_month_progress','flags'})==omit(ass,{'progress','last_month_progress','flags'}),
'exact_two_native_pending_and_scopes':pending==[{'id':162,'event':'communications_spread.3','date':'2247.04.01','country':0},{'id':165,'event':'shroud.2625','date':'2247.09.01','country':0}] and [q.scalars(q.block(v,'scope')).get('type') for v in prs]==['country','situation'] and [q.scalars(q.block(v,'scope')).get('id') for v in prs]==[0,16777221],
'native_disease_no_immediate_effect':not q.block(events[0],'immediate') and q.scalars(q.block(q.block(events[0],'trigger'),'owner')).get('founder_species_is_organic')=='yes',
'native_on_action_contains_social_disease':'shroud.2625' in q.block(on.read_text('utf-8-sig'),'on_breach_the_shroud_situation_random_social_events_list'),
'EEP_and_actual_ships_population_boundary_already38true':all(v is True for k,v in orig['checks'].items() if k not in ['no_country0_pending','all_native_breach_raw_except_progress_held'])}
p={'status':'PASS_NATIVE_MEDITATE_YEAR_WITH_PENDING_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'pending':pending,'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,on]],'scope':'Only original boundary with exact native social flag and pending. No calendar clearance, original40 FAIL retained.'}
out=run/(after+'-social-pending-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original scoped social supplement FAIL retained'
