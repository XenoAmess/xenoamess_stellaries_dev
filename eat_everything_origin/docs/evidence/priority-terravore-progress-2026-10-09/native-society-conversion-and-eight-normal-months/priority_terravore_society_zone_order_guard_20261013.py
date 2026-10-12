"""Read-only native paid800 replacement with three compatible labs retained pending work."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-fifth-postsettlement-22831001';after='terravore-society-zone-ordered-22831001';b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
pre=load(before+'-fifth-postsettlement-month-v2-proof.json');px=load(before+'-fifth-postsettlement-month-guard-v2-execution.json');sx=load(after+'-save-execution.json');ux=load('terravore-society-zone-offer-click-execution.json');ob=load(after+'-observation.json')
added=set(a['items'])-set(b['items']);item=a['items']['83886115'];oldids=q.ids(q.block(b['queues']['0'],'items'))
bmod,amod=[q.block(s['country'],'modules') for s in [b,a]]
checks={
 'prior20PASS_actual0_exactSAV_and_source':len(pre['checks'])==20 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(run/'priority_terravore_fifth_postsettlement_month_guard_v2_20261013.py')=='b11b771d506f80a9976b7c7eff7f9bb1f6770999b69ee6cea405d3610d39414c' and pre['after_sha256']==ba['save_sha256']=='d303f87d6c8b19776aad42509a0129e6509696e5dc1395e47c97c48593c94dd1',
 'normal_UI_save_actual0_sources_observation_bound':ux['returncode']==sx['returncode']==0 and ux['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py') and sx['helper_sha256']==h.sha256(run/'priority_native_save.py') and all(h.sha256(Path(v['path']))==v['sha256'] for v in ob['dependency_bindings']),
 'same_date_original_SAV_pair_no_clock':ba['date']==aa['date']==ob['date']=='2283.10.01' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,ba),(after,aa)]) and aa['save_sha256']=='65ac7a62e2f9e0fa2b8947b50fe8e918962b40efb52987eb0ed241afc300a465',
 'exact_once800_minerals_all_other_effective_resources_held':all(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))==(-D(800) if k=='minerals' else D(0)) for k in set(bc['effective_stockpile'])|set(ac['effective_stockpile'])) and q.scalars(q.block(item,'resources'))=={'minerals':800},
 'one_new_order360work_society_original_hive_slot1':added=={'83886115'} and all(a['items'].get(k)==v for k,v in b['items'].items()) and q.scalars(item)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':360} and q.scalars(q.block(item,'buildable_zone'))=={'zone':'zone_research_society','planet':0,'district':1,'zone_slot':1},
 'only_queue0_appended_old_six_work_held':set(b['queues'])==set(a['queues']) and all(v==a['queues'][k] for k,v in b['queues'].items() if k!='0') and q.ids(q.block(a['queues']['0'],'items'))==oldids+[83886115] and omit(a['queues']['0'],{'items'})==omit(b['queues']['0'],{'items'}),
 'raw_country_all_except_materialized_economy_held':omit(b['country'],{'modules'})==omit(a['country'],{'modules'}) and omit(bmod,{'standard_economy_module'})==omit(amod,{'standard_economy_module'}),
 'research_banks_queues_budget_every_other_audit_country_field_held':all(bc[k]==ac[k] for k in bc if k not in ['stockpile','effective_stockpile','modules']),
 'all_audit_worlds_population_EEP_jobs_capacity_structures_held':all(ba[k]==aa[k] for k in ba if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes','countries']) and aa['colonies']['0']['actual_pop_sum']==12707,
 'old_physics_zone_all_three_original_lab_raws_held_no_early_conversion':b['roots']['zones']==a['roots']['zones'] and b['roots']['buildings']==a['roots']['buildings'] and q.scalars(q.block(a['roots']['zones'],'16777323'))['type']=='zone_research_physics' and q.ids(q.block(q.block(a['roots']['zones'],'16777323'),'buildings'))==[16777251,83886120,16777323],
 'all_owned61ships34fleets_armies_war_truce_messages_held':all(b[k]==a[k] for k in ['ships','fleets','messages','pending']) and len(a['ships'])==61 and len(a['fleets'])==34 and not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['army','war','truce']),
 'actual_quote_preserved800_258days_no_claim_confirm_dialog':h.sha256(run/'terravore-society-zone-replace-list-frame.jpg')=='9fe5521cbf795947c6638a9bedec6364605c9cd2171178fb8cf43eea8f96c400' and h.sha256(run/'terravore-society-zone-offer-frame.jpg')=='1320bd663ecf86ae740fbe976e83c76a6deed4bd891667bd428f2056cf0360cf',
 'CN41_production_error_exact_no_new_bytes':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and ob['new_error_bytes']==0 and ob['error_prefix_held'] and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592',
}
passed=all(v is True for v in checks.values());out=run/(after+'-paid-society-zone-order-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NORMAL_PAID800_SOCIETY_ZONE_ORDER' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'order_raw':item,'queue_raw':a['queues']['0'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'boundaries':['normal_queue_priority_review'],'scope':'Order only; existing labs retained before construction, not completion. Normal UI no confirmation dialog; price captured.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
