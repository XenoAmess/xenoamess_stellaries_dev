"""Exact second annual POP bite; no future random branch permission."""
import json,logging,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-queen32-acknowledged';after='terravore-annual-bite-22821201';b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bp,ap=[s['planets']['1578'] for s in [ba,aa]]
p=load(before+'-annual-bite2282-preflight.json');x=load(before+'-annual-bite2282-preflight-execution.json');ob=load(after+'-construction-boundary-observation-v4.json');ox=load(after+'-boundary-observation-v4-execution.json');cx=load(after+'-calendar-execution.json');old=load('terravore-three-labs-normal-month-22811201-annual-pop-bite-review-proof.json')
oldarm=set(q.ids(q.block(b['country'],'owned_armies')));newarm=set(q.ids(q.block(a['country'],'owned_armies')));deps=ap['deposits'][len(bp['deposits']):];msgs=ob['new_country0_messages_raw']
def detail(col):
 raw=q.block(q.block(q.block(a['roots']['colony'],col),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(raw));return {q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
checks={
 'preflight4PASS0_source_bound':len(p['checks'])==4 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='696eaceda2ec91404f14d6e43e14a08849be6c015ccbe07cecef8b384480bb78',
 'calendar_observer_actual0_original_SAVs':cx['returncode']==ox['returncode']==0 and all(v is True for v in ob['checks'].values()) and p['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')) and all(v['helper_sha256']==h.sha256(Path(v['command'][1])) for v in [cx,ox]),
 'native_sources_held_prior458token_identity':all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in p['sources']) and old['checks']['native_consume458tokens_identical_except_declared_AI_core_destination'] is True,
 'cooldown30_reset360_only_exact_new_date':bp['flags']['recently_eaten_planet']['flag_days']==30 and ap['flags']['recently_eaten_planet']=={'flag_date':63524400,'flag_days':360},
 'exact_two_lithoid_deposits_old_deposits_held':deps==[150995555,150995554] and ap['deposits'][:len(bp['deposits'])]==bp['deposits'] and all(q.scalars(q.block(a['roots']['deposit'],str(i)))=={'type':'d_lithoid_devastation'} for i in deps),
 'only_native_POP100_plus_natural_growth_no_mother_transfer':detail('30')=={'GROWTH_CAT_GROWTH':1,'GROWTH_CAT_OTHER':100,'GROWTH_CAT_PROMOTION':0} and detail('0')=={'GROWTH_CAT_GROWTH':6,'GROWTH_CAT_PROMOTION':0} and ob['after_state']['species_population_by_colony']=={'0:73':11945,'30:73':498} and oldarm==newarm and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in oldarm),
 'only_native_notification298_POP_no_Queen_or_pending':len(msgs)==1 and q.scalars(msgs[0])=={'type':'MESSAGE_TERRAVORE_CONSUME_WORLD','localization':'MESSAGE_TERRAVORE_CONSUME_WORLD_POP_TEXT','receiver':0,'target_planet':1578,'end':'2283.03.01','date':'2282.12.01','notification':298,'message_type':'none'} and not a['pending'],
 'native_devastation20p01_districts_held_no_false_demolition_claim':bp['bombardment_damage']==20.29 and ap['bombardment_damage']==40.3 and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['30']['districts']),
}
passed=all(v is True for v in checks.values());out=run/(after+'-annual-bite2282-result-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_EXACT_SECOND_ANNUAL_POP_BITE' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'added_deposits':deps,'new_messages':msgs,'sources':p['sources'],'scope':'Exact POP branch only, monthly cash/research/EEP and maintenance require separate business guard. Devastation residual.01 unexplained.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
