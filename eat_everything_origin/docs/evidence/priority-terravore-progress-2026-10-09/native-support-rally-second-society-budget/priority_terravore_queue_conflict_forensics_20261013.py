"""Read-only preservation of a wrapper-failed action; never invent child execution success."""
import json, logging, sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
before='terravore-second-society-ordered-22860501';after='terravore-second-society-priority-22860501'
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];p=load(before+'-second-society-order-proof.json');px=load(before+'-guard-execution.json')
action=load('terravore-second-society-priority-click-22860501-shift-click.action.json');sx=load(after+'-save-execution.json')
checks={
 'prior15PASS_actual0_source_originalSAV':len(p['checks'])==15 and all(v is True for v in p['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and p['after_sha256']==ba['save_sha256'],
 'same_paused_date_original_pair_native_save_actual0':ba['date']==aa['date']=='2286.05.01' and all(h.sha256(run/(s+'.sav'))==au['save_sha256'] for s,au in [(before,ba),(after,aa)]) and sx['returncode']==0 and sx['helper_sha256']==h.sha256(Path(sx['command'][1])),
 'only_exact_one_position_up_queue_change':q.ids(q.block(b['queues']['0'],'items'))==[1191182345,117440553,1476395019,117440546,201326629] and q.ids(q.block(a['queues']['0'],'items'))==[1191182345,117440553,1476395019,201326629,117440546] and omit(b['queues']['0'],{'items'})==omit(a['queues']['0'],{'items'}),
 'all_items_work_resources_and_other_queues_raw_held':b['items']==a['items'] and set(b['queues'])==set(a['queues']) and all(v==a['queues'][i] for i,v in b['queues'].items() if i!='0'),
 'all_other_named_world_roots_exact_raw_held':set(b['roots'])==set(a['roots']) and all(v==a['roots'][k] for k,v in b['roots'].items() if k!='construction'),
 'all_audit_business_held_no_clock_refund_work_or_reward':all(v==aa[k] for k,v in ba.items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']),
 'legacy_source_preserved_without_overwriting_physical_source':h.sha256(run/'priority_native_shift_click_legacy_conflict_20261013.py')=='4b46175851a60b20e103cd1296a4c7b539bd1ae712fb0446d8037e0a70ca1c61' and h.sha256(run/'priority_native_shift_click.py')=='04c3884f627dce1ab4dc48a47797dfc0e60e1b87b28ef0c03e497aebcf4d29f5',
 'action_release_record_preserved_child_execution_receipt_absent':action=={'action':'native_shift_left_click','stage':'terravore-second-society-priority-click-22860501','client_point':[923,477],'hwnd':5770060,'shift_released':True} and not (run/'terravore-second-society-priority-click-22860501-execution.json').exists(),
 'CN41_unfiltered_live_error_exact':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-queue-conflict-forensics-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_QUEUE_CONFLICT_FORENSICS' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'observed_outer_wrapper_returncode':1,'child_returncode':'not retained; unknown','queue_ids':q.ids(q.block(a['queues']['0'],'items')),'boundaries':['normal_verified_physical_priority_required'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Read-only exact state forensics; original wrapper failed and priority not complete.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
