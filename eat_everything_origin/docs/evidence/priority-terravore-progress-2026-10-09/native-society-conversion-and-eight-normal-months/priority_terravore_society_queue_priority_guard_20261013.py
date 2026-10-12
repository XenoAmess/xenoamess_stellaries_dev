"""Only normal queue item order changes on same paused day; no refunds/work/grants."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-society-zone-ordered-22831001';after='terravore-society-zone-priority-22831001';b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit']
p=load(before+'-paid-society-zone-order-proof.json');px=load(before+'-paid-society-zone-order-guard-execution.json');ux=load('terravore-society-queue-priority-physical-shift-click-execution.json');sx=load(after+'-save-execution.json');ob=load(after+'-observation.json')
old=q.ids(q.block(b['queues']['0'],'items'));new=q.ids(q.block(a['queues']['0'],'items'));checks={
 'prior13PASS_actual0_exact_source_SAV':len(p['checks'])==13 and all(v is True for v in p['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1]))=='337c78214c7639106f5c40d28e4dd39772ab0aa383761db274eb154ff67a4fac' and p['after_sha256']==ba['save_sha256'],
 'normal_physical_shift_click_and_normal_save_actual0_sources':ux['returncode']==sx['returncode']==0 and ux['helper_sha256']==h.sha256(run/'priority_native_shift_click.py')=='04c3884f627dce1ab4dc48a47797dfc0e60e1b87b28ef0c03e497aebcf4d29f5' and sx['helper_sha256']==h.sha256(run/'priority_native_save.py') and all(h.sha256(Path(v['path']))==v['sha256'] for v in ob['dependency_bindings']),
 'same_paused_native_date_and_originalSAV':ba['date']==aa['date']=='2283.10.01' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,ba),(after,aa)]),
 'only_society_order_moved_front_six_hives_relative_order_held':old[-1]==83886115 and new==[83886115]+old[:-1] and omit(b['queues']['0'],{'items'})==omit(a['queues']['0'],{'items'}) and set(b['queues'])==set(a['queues']) and all(v==a['queues'][i] for i,v in b['queues'].items() if i!='0'),
 'all_original_items_work_resources_type_held_no_refund':b['items']==a['items'] and q.scalars(a['items']['83886115'])['progress']==0 and q.scalars(a['items']['268435492'])['progress']==22.4,
 'all_audit_business_data_held_including_population_research_resources':all(ba[k]==aa[k] for k in ba if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']),
 'all_owned_and_world_raw_data_held_only_construction_root_changed':all(b[k]==a[k] for k in ['country','ships','fleets','messages','pending']) and all(b['roots'][k]==a['roots'][k] for k in ['army','zones','buildings','districts','war','truce','situations','colony']) and not a['pending'],
 'CN_same41_package_error_exact_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and ob['new_error_bytes']==0 and ob['error_prefix_held'] and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-queue-priority-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NORMAL_SOCIETY_QUEUE_PRIORITY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'queue_raw':a['queues']['0'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'boundaries':['normal_research_construction_month_contract_review'],'scope':'Same day order only, no construction or research completion.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
