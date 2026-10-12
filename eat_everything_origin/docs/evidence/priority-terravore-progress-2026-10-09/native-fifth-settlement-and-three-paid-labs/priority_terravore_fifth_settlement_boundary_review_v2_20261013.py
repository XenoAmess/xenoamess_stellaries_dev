"""Read-only A:33 to34 month, B:one exact deferred settlement day. No random assumptions."""
import json,logging,sys
from pathlib import Path
phase,before,proof,execution,stage=sys.argv[1:];assert phase in ['A','B']
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
a=read_state(run,before);au=a['audit'];c=au['countries']['0'];p=load(proof);x=load(execution+'-execution.json');days=30 if phase=='A' else 1
start,end=('2283.08.01','2283.09.01') if phase=='A' else ('2283.09.01','2283.09.02')
source=au['planets']['1578'];sit=au['situations']['167772163'];front=str(q.ids(q.block(a['queues']['0'],'items'))[0]);work=q.scalars(a['items'][front])['progress']
rawsit=q.block(q.block(a['roots']['situations'],'situations'),'167772163');delays=[v for k,v,obj in q.fields(rawsit) if k=='delayed_event' and obj]
old=load('terravore-three-labs-normal-month-22811201-annual-pop-bite-review-proof.json')
native=(h.GAME_EXE.parent/'common/scripted_effects/00_scripted_effects.txt').read_text('utf-8-sig');mod=(h.MOD_ROOT/'common/scripted_effects/eep_native_consume.txt').read_text('utf-8-sig');tokens=lambda v:[t[0] for t in q.tokens(v)]
checks={
 'prior19_PASS_actual0_exact_V9_source':len(p['checks'])==19 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='770fe540a37fd1fe36c2de3decbccd4222f4e97e74dce01177295569d9f317aa',
 'original_SAV_SHA_current_exact_date':au['date']==start and p['after_sha256']==au['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_reviewed_fifth_boundary_no_ordinary_continuation':p['boundaries']==['fifth_devour_settlement_review'] and not p['native_devour_calendar_ready'] and p['maximum_days_to_native_bite_boundary']==0,
 'active_original_target_Q14_month34_no_credit_before_settlement':set(au['situations'])=={'167772163'} and sit['progress']==(33 if phase=='A' else 34) and sit['country']==0 and sit['type']=='situation_eep_devouring' and sit['target']['id']==1578 and source['variables']['eep_q']==14 and source['variables']['eep_months']==34 and source['owner']==source['controller']==0 and set(c['owned_colonies'])=={0,30} and all(c['variables'].get(k)==v for k,v in {'eep_c':62,'eep_d':17,'eep_worlds':4,'eep_g':0,'eep_made':0}.items()) and c['effective_stockpile']['menace']==2180 and all(g['key']['species']==73 for g in au['pop_groups'].values()),
 'native_cooldown_lab_and_project_still_outside_other_boundaries':source['flags']['recently_eaten_planet']['flag_days']>days and work+(days*1.4)<360 and p['project3_progress']+300<12000 and all(k in source['flags'] for k in ['eep_active','eep_native','being_devoured']),
 'no_pending_combat_or_error_new_bytes':not a['pending'] and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()) and q.scalars(a['roots']['ground_combat'])=={'150994944':'none'} and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 'native458tokens_preserved_sources_production41_CN':len(tokens(q.block(mod,'eep_native_consume')))==458 and tokens(q.block(mod,'eep_native_consume').replace('event_target:eep_core@event_target:eep_actor','owner.capital_scope'))==tokens(q.block(native,'consume_world')) and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in old['sources']) and m['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'exact_situation_deferred_eep21_day1_scope_no_early_pending':len(delays)==1 and q.scalars(delays[0])=={'event':'eep.21','days':1} and q.scalars(q.block(delays[0],'scope'))=={'type':'situation','id':167772163,'opener_id':4294967295,'random_allowed':'yes'} and 'eep_pending' not in source['flags'],
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':au['save_sha256'],'after_sha256':au['save_sha256'],'start_date':start,'end_date':end,'days':days,'maximum_days':days,'allowed_boundaries':p['boundaries'],'execution_stage':stage,'source_proof_file':proof,'source_proof_sha256':h.sha256(run/proof),'scope':'Only exact next boundary. Settlement random branches, population return, capacity and Queen require independent result acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
