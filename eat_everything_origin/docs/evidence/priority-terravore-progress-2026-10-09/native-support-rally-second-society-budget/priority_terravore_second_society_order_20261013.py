"""Normal paid second society specialization order or same-day priority, no grants."""
import json, logging, sys
from decimal import Decimal as D
from pathlib import Path
kind, before, after, prior, execution, ui_stage = sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools'); sys.argv=['runtime']
import runtime as r, audit_save as q
from priority_terravore_native_state import read_state, omit
logging.disable(logging.INFO); h=r.harness; run,user,meta=h.load_run()
load=lambda name:json.loads((run/name).read_text('utf-8-sig'))
def checked(stage):
    x=load(stage+'-execution.json')
    return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
b,a=[read_state(run,s) for s in [before,after]]; ba,aa=b['audit'],a['audit']; bc,ac=[v['countries']['0'] for v in [ba,aa]]
p=load(prior); old=q.ids(q.block(b['queues']['0'],'items')); new=q.ids(q.block(a['queues']['0'],'items'))
assert kind in ['order','priority']
added=set(a['items'])-set(b['items']); nid=next(iter(added)) if kind=='order' and len(added)==1 else str(old[-1])
item=a['items'].get(nid,''); bm,am=[q.block(s['country'],'modules') for s in [b,a]]
ignored_audit={'save','save_sha256','gamestate_sha256','gamestate_bytes','countries'}
checks={
    'prior_PASS_actual0_source_originalSAV':p['status'].startswith('PASS') and bool(p['checks']) and all(v is True for v in p['checks'].values()) and checked(execution) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')),
    'normal_UI_and_native_save_actual0_sources':checked(ui_stage) and checked(after+'-save'),
    'same_paused_date_original_SAV_pair':ba['date']==aa['date']=='2286.05.01' and aa['save_sha256']==h.sha256(run/(after+'.sav')),
    'cash_exact800_only_order_no_priority_fee':all(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))==(-D(800) if kind=='order' and k=='minerals' else D(0)) for k in set(bc['effective_stockpile'])|set(ac['effective_stockpile'])),
    'only_expected_queue0_change_other_queues_raw_held':set(a['queues'])==set(b['queues']) and all(a['queues'][i]==v for i,v in b['queues'].items() if i!='0') and omit(b['queues']['0'],{'items'})==omit(a['queues']['0'],{'items'}) and new==(old+[int(nid)] if kind=='order' else [old[-1]]+old[:-1]),
    'all_existing_items_progress_cost_type_raw_held':all(a['items'].get(i)==v for i,v in b['items'].items()) and (len(added)==1 if kind=='order' else b['items']==a['items']),
    'one_paid360_society_slot2_order_or_same_item':q.scalars(item)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':360} and q.scalars(q.block(item,'resources'))=={'minerals':800} and q.scalars(q.block(item,'buildable_zone'))=={'zone':'zone_research_society','planet':0,'district':1,'zone_slot':2},
    'original_four_paid_hives_relative_order_and_work_held':(old if kind=='order' else new[1:])==[1191182345,117440553,1476395019,117440546] and q.scalars(a['items']['1191182345'])['progress']==2.8,
    'country_raw_except_exact_materialized_economy_held':(omit(b['country'],{'modules'})==omit(a['country'],{'modules'}) and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(q.block(bm,'standard_economy_module'),{'resources'})==omit(q.block(am,'standard_economy_module'),{'resources'})) if kind=='order' else b['country']==a['country'],
    'all_country_audit_research_banks_budget_EEP_held':all(bc[k]==ac[k] for k in bc if k not in ({'stockpile','effective_stockpile','modules'} if kind=='order' else set())),
    'all_other_country_world_raw_roots_held':set(b['roots'])==set(a['roots']) and all(v==a['roots'][k] for k,v in b['roots'].items() if k not in ['country','construction']) and omit(b['roots']['country'],{'0'})==omit(a['roots']['country'],{'0'}),
    'all_audit_world_population_jobs_capacity_held':all(v==aa[k] for k,v in ba.items() if k not in ignored_audit),
    'original_engineering_zone_and_all_labs_raw_held':b['roots']['zones']==a['roots']['zones'] and b['roots']['buildings']==a['roots']['buildings'] and q.scalars(q.block(a['roots']['zones'],'16777330'))['type']=='zone_research_engineering' and q.ids(q.block(q.block(a['roots']['zones'],'16777330'),'buildings'))==q.ids(q.block(q.block(b['roots']['zones'],'16777330'),'buildings')),
    'all75ships35fleets15armies_messages_pending_held':b['ships']==a['ships'] and b['fleets']==a['fleets'] and len(a['ships'])==75 and len(a['fleets'])==35 and b['roots']['army']==a['roots']['army'] and b['messages']==a['messages'] and not a['pending'],
    'CN41_live_unfiltered_error_exact':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values()); out=run/(after+'-second-society-'+kind+'-proof.json'); assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_SECOND_SOCIETY_'+kind.upper() if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'new_order_id':nid,'order_raw':item,'queue_ids':new,'boundaries':['paid_second_society_priority_or_construction_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Normal same-day paid operation only, not construction/project or full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'new_order_id':nid,'queue':new}),flush=True); assert passed
