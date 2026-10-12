"""Exact original native event295 confirmation, with recorded validation-order mistake."""
import json,logging,re,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-native-project2-completed-22821003';after='terravore-native-project2-event-acknowledged';b,a=[read_state(run,s) for s in [before,after]]
p=load(before+'-project2-completed-v3-proof.json');px=load(before+'-project2-completed-guard-v3-execution.json');click=load('terravore-native-project2-original-event-ack-click-execution.json');sx=load(after+'-save-execution.json')
history=lambda s:[q.scalars(v) for v in re.findall(r'\{([^{}]*)\}',s['roots']['open_player_event_selection_history'])];bh,ah=history(b),history(a)
removed=[v for v in b['messages'] if q.scalars(v).get('event')==295];levels=[q.unquote(v) for k,v,obj in q.fields(q.block(a['country'],'crisis_progression')) if k=='level' and not obj]
checks={
 'original_completion16PASS0_source_SHA_and_late_validation_explicit':len(p['checks'])==16 and all(v is True for v in p['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1]))=='2b2c058b4b499af0575a51179196b6c7394ab4064f80502dbdd7b4b51d7074a9' and click['started_at_utc']<px['started_at_utc'] and p['after_sha256']==b['audit']['save_sha256'],
 'only_normal_click_and_save_actual0_bound_sources_SAV_same_date':click['returncode']==sx['returncode']==0 and all(x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in [click,sx]) and all(s['audit']['save_sha256']==h.sha256(run/(stage+'.sav')) for s,stage in [(b,before),(a,after)]) and b['audit']['date']==a['audit']['date']=='2282.10.03',
 'country0_raw_and_all_audit_business_exact_held':b['country']==a['country'] and all(v==a['audit'][k] for k,v in b['audit'].items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']),
 'all_owned_ships_fleets_armies_worlds_orders_exact_held':all(b[k]==a[k] for k in ['ships','fleets','queues','items']) and all(b['roots'][k]==a['roots'][k] for k in ['army','zones','buildings','districts','deposit','situations']),
 'only_original_pending295_and_corresponding_message_consumed':len(b['pending'])==1 and q.scalars(b['pending'][0])['id']==295 and not a['pending'] and len(removed)==1 and a['messages']==[v for v in b['messages'] if v not in removed],
 'history_only295_human1_actual_native_option3_added':ah==bh+[{'player_event':295,'human':1,'option':3}],
 'native_crisis_progression_still_level2_no_early_Queen_reward':levels==['crisis_level_1','crisis_level_2'] and a['audit']['countries']['0']['variables']['eep_fleet_stage']==2,
 'CN_same_production_exact_error627_no_new_bytes':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and reviewed_error_pair((run/(before+'-error-after.log')).read_bytes(),(run/(after+'-error-after.log')).read_bytes(),run) and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-event-ack-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_ORIGINAL_PROJECT2_EVENT_ACKNOWLEDGEMENT' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'native_crisis_levels':levels,'boundaries':['native_level3_unlock_and_delayed4150_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'known_validation_order_mistake':'Normal click occurred before completion guard V3 passed. All original failures retained; this is subsequent independent verification, not an in-order claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
