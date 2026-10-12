"""Paused normal UI purchase of existing native mineral destroyer design; no free hulls."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
before,after,count,prior,execution,*clickstages=sys.argv[1:];count=int(count)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[s['countries']['0'] for s in [ba,aa]]
p=load(prior);px=load(execution+'-execution.json');sx=load(after+'-save-execution.json');ux=[load(st+'-execution.json') for st in clickstages];ob=load(after+'-observation.json')
added=set(a['items'])-set(b['items']);oldids=q.ids(q.block(b['queues'].get('3',''),'items'));newids=q.ids(q.block(a['queues']['3'],'items'));mods=[q.block(s['country'],'modules') for s in [b,a]]
expected_implementation={'design':83887141,'upgrade':4294967295,'growth_stage':0}
checks={
 'prior_allPASS_actual0_exactSAV_source':p['status'].startswith('PASS') and all(v is True for v in p['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and p['after_sha256']==ba['save_sha256'],
 'normal_UI_inputs_save_actual0_source_and_click_order':len(ux)==count and all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in ux+[sx]) and all(x['started_at_utc']>px['finished_at_utc'] for x in ux) and all(h.sha256(Path(v['path']))==v['sha256'] for v in ob['dependency_bindings']),
 'same_date_original_native_SAV_pair_no_clock':ba['date']==aa['date']==ob['date']=='2284.07.04' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,ba),(after,aa)]),
 'only_exact412_5_minerals_per_order_zero_alloy_or_research_charge':all(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))==(-D('412.5')*count if k=='minerals' else D(0)) for k in set(bc['effective_stockpile'])|set(ac['effective_stockpile'])),
 'only_requested_new_paid0work_native60work_orders':len(added)==count and all(a['items'].get(k)==v for k,v in b['items'].items()) and all(q.scalars(a['items'][i])=={'queue':3,'paying_country':0,'progress':0,'progress_needed':60} and q.scalars(q.block(a['items'][i],'resources'))=={'minerals':412.5} and q.scalars(q.block(q.block(a['items'][i],'buildable_ship'),'ship_design_implementation'))==expected_implementation and q.scalars(q.block(q.block(a['items'][i],'buildable_ship'),'orbitable'))=={'starbase':0} for i in added),
 'only_shipyard3_appended_two_parallel_slots_existing_orders_held':set(a['queues'])==set(b['queues'])|{'3'} and all(a['queues'].get(i)==v for i,v in b['queues'].items() if i!='3') and newids[:len(oldids)]==oldids and set(map(str,newids[len(oldids):]))==added and q.scalars(a['queues']['3'])=={'owner':0,'simultaneous':2,'type':'ships'} and q.scalars(q.block(a['queues']['3'],'location'))=={'type':0,'id':0},
 'actual_existing_design_crisis_destroyer_native_stage3_held':b['designs']==a['designs'] and q.scalars(a['designs']['83887141'])['ship_size']=='crisis_destroyer' and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['variables']['eep_crisis']==ac['variables']['eep_fleet_stage']==3,
 'country_all_except_materialized_economy_raw_held':omit(b['country'],{'modules'})==omit(a['country'],{'modules'}) and omit(mods[0],{'standard_economy_module'})==omit(mods[1],{'standard_economy_module'}),
 'all_research_budget_EEP_and_other_country_audit_fields_held':all(bc[k]==ac[k] for k in bc if k not in ['stockpile','effective_stockpile','modules']),
 'all_worlds_population_jobs_mother39_paid27_held':all(ba[k]==aa[k] for k in ba if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes','countries']) and aa['colonies']['0']['actual_pop_sum']==12762 and all(b['roots'][k]==a['roots'][k] for k in ['zones','buildings','districts','situations']),
 'original61ships34fleets15armies_messages_pending_held_no_birth':all(b[k]==a[k] for k in ['ships','fleets','messages','pending']) and len(a['ships'])==61 and len(a['fleets'])==34 and not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['army','war','truce']),
 'actual_native_quote_original_GPU_frame_bound':h.sha256(run/'terravore-crisis-destroyer-native-quote.jpg')=='feb3b90447212779be286cd49f4dcc875645e7a2f9c3b4759036af256d1c9951',
 'CN41_same_production_and_unfiltered_error_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and ob['new_error_bytes']==0 and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-destroyer-paid-order-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_PAID_MINERAL_DESTROYER_ORDER' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'new_paid_order_ids':sorted(added,key=int),'mineral_cost':str(D('412.5')*count),'queue_shipyard3_ids':newids,'boundaries':['paid_destroyer_birth_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Paused normal paid orders only; no completed hull or upkeep claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'new_orders':sorted(added,key=int),'paid_minerals':str(D('412.5')*count)}),flush=True);assert passed
