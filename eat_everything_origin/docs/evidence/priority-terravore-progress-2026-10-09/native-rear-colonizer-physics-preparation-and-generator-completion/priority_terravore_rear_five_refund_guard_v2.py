"""Read-only five native cancellations and exact refund; no gameplay actions."""
import json, logging, sys, zipfile
from decimal import Decimal as D
from pathlib import Path

before, after = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO)
h = r.harness; run, user, metadata = h.load_run()

def load(name): return json.loads((run / name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        fs = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage + '.audit.json'), fs, {k:v for k,v,o in fs if o}
def omit(raw, names): return [(k,v,o) for k,v,o in q.fields(raw) if k not in names]
def fmap(raw): return {k:(v,o) for k,v,o in q.fields(raw)}

b, bf, br = read(before); a, af, ar = read(after)
bc, ac = b['countries']['0'], a['countries']['0']
pre = load(before + '-war1-battle-v65-proof.json')
pex = load(before + '-battle-v65-execution.json')
paid = load('terravore-rear-clearing-six-paid-rear-six-payment-proof.json')
paidex = load('terravore-rear-clearing-six-paid-payment-guard-execution.json')
actions = [(load('terravore-rear-five-cancel-' + str(i).zfill(2) + '.action.json'),
            load('terravore-rear-five-cancel-' + str(i).zfill(2) + '-execution.json')) for i in range(1,6)]
cancelled = [83886123,33554472,33554471,1241513995,67108908]
cb, ca = br['construction'], ar['construction']
qm = [q.block(t,'queue_mgr') for t in [cb,ca]]
qs = [q.block(t,'queues') for t in qm]
bq, aq = [q.block(t,'2287') for t in qs]
im = [q.block(t,'item_mgr') for t in [cb,ca]]
items_raw = [q.block(t,'items') for t in im]
bi, ai = [fmap(t) for t in items_raw]
bcs, acs = [dict((k,v) for k,v,o in q.fields(t['country']) if o) for t in [br,ar]]
bm, am = [q.block(t['0'],'modules') for t in [bcs,acs]]
be, ae = [q.block(t,'standard_economy_module') for t in [bm,am]]
fleets = [fmap(t['fleet']) for t in [br,ar]]
fb, fa = [t['65'][0] for t in fleets]
legacy = load(after+'-rear-five-refund-proof.json')
legacy_ex = load(after+'-refund-guard-execution.json')
checks = {
 'original16_single_camera_assumption_FAIL_actual1_bound':len(legacy['checks'])==16 and [k for k,v in legacy['checks'].items() if v is not True]==['all_other_top_raw_held_including28_ships_colonizer_core_population_wars'] and legacy_ex['returncode']==1 and legacy_ex['helper_sha256']==h.sha256(run/'priority_terravore_rear_five_refund_guard.py')=='7eb0bf4b5e303e0091c88d41ed75d3aeea06f13c1d2de15dbecb67973cf1e575' and legacy['before_sha256']==b['save_sha256'] and legacy['after_sha256']==a['save_sha256'],
 'only_known_UI_camera_focus_added_system37':not any(k=='camera_focus' for k,v,o in bf) and [(v,o) for k,v,o in af if k=='camera_focus']==[('37',False)],
 'prior106_PASS_actual0_source_and_before_SHA':pre['status'].startswith('PASS_') and len(pre['checks'])==106 and all(v is True for v in pre['checks'].values()) and pex['returncode']==0 and pex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v65.py')=='e63467e1b2c8727301715616037ff8e9b32237673c357eb7b1f4378d65c52cf9' and pre['after_sha256']==b['save_sha256']=='acfad1a21cad0c3936bf4378f18bad9f1de0ef6a8e79cee1e7009d2b082385c3',
 'original_six_actual609_payment28_PASS_bound':paid['status'].startswith('PASS_') and len(paid['checks'])==28 and all(v is True for v in paid['checks'].values()) and paidex['returncode']==0 and paidex['helper_sha256']==h.sha256(run/'priority_terravore_rear_six_payment_guard.py')=='cd80a984d203fa72288da3059b774e49914488a3ceb7bc10ec5656376e4cb2e1' and paid['native_order_ids'][1:]==cancelled and paid['actual_per_ship_alloys']=='101.5',
 'same_actual_day_and_original_SHA_pair':b['date']==a['date']=='2271.12.12' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav'))=='70334c9e1b86e3ba37ebf8d1a68de1c9369b9dcba3f248cb2324588696630056',
 'five_unique_normal_cancels_actual0':all(c['action']=='left-click' and c['client_point']==[300,470] and c['foreground_after']==c['expected_hwnd'] and e['returncode']==0 and e['helper_sha256']=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' for c,e in actions),
 'native_save_actual0':load(after+'-native-save-execution.json')['returncode']==0,
 'exact507point5_refund_all_other_real_stocks_held':D(str(ac['effective_stockpile']['alloys']))-D(str(bc['effective_stockpile']['alloys']))==D('507.5') and {k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'},
 'five_original_orders_exact_native_price_work_and_design':all(q.scalars(bi[str(i)][0])=={'queue':2287,'paying_country':0,'progress':1.58 if n==0 else 0,'progress_needed':60} and q.scalars(q.block(bi[str(i)][0],'resources'))=={'alloys':101.5} and q.scalars(q.block(q.block(bi[str(i)][0],'buildable_ship'),'orbitable'))=={'starbase':153} and q.scalars(q.block(q.block(bi[str(i)][0],'buildable_ship'),'ship_design_implementation'))=={'design':134219607,'upgrade':4294967295,'growth_stage':0} for n,i in enumerate(cancelled)),
 'five_exact_none_retirements_no_added_or_removed_handles':bi.keys()==ai.keys() and all(ai[str(i)]==('none',False) for i in cancelled) and omit(items_raw[0],set(map(str,cancelled)))==omit(items_raw[1],set(map(str,cancelled))),
 'original_queue2287_five_to_empty_other_fields_held':q.ids(q.block(bq,'items'))==cancelled and not q.ids(q.block(aq,'items')) and omit(bq,{'items'})==omit(aq,{'items'}),
 'all_other_queues_and_managers_raw_held':omit(qs[0],{'2287'})==omit(qs[1],{'2287'}) and omit(qm[0],{'queues'})==omit(qm[1],{'queues'}) and omit(im[0],{'items'})==omit(im[1],{'items'}) and omit(cb,{'queue_mgr','item_mgr'})==omit(ca,{'queue_mgr','item_mgr'}),
 'only_economy_alloys_change_no_research_or_mirror_mutation':omit(q.block(be,'resources'),{'alloys'})==omit(q.block(ae,'resources'),{'alloys'}) and omit(be,{'resources'})==omit(ae,{'resources'}) and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and bc['research_stockpile']==ac['research_stockpile'],
 'country0_other_fields_all_other_countries_raw_held':omit(bcs['0'],{'modules'})==omit(acs['0'],{'modules'}) and bcs.keys()==acs.keys() and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'only_foreign65_exact_cloak_dirty_flag_all_other_fleets_held':fleets[0].keys()==fleets[1].keys() and all(v==fleets[1][k] for k,v in fleets[0].items() if k!='65') and omit(fb,{'properties'})==omit(fa,{'properties'}) and q.scalars(q.block(fb,'properties'))=={'weapon':'yes','mobile':'yes','valid_for_combat':'yes'} and q.scalars(q.block(fa,'properties'))=={'weapon':'yes','mobile':'yes','valid_for_combat':'yes','dirty_cloaking_strength':'yes'},
 'all_other_top_raw_held_including28_ships_colonizer_core_population_wars':[(k,v,o) for k,v,o in bf if k not in {'country','construction','fleet','camera_focus'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','fleet','camera_focus'}],
 'exact_unfiltered_original_error_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'production41_same_tree_simp_chinese':metadata['version']=='0.2.0' and metadata['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
out = run/(after+'-rear-five-refund-v2-proof.json'); assert not out.exists()
p = {'status':'PASS_TERRAVORE_NATIVE_REAR_FIVE_REFUND_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'cancelled_order_ids':cancelled,'actual_alloys_refund':'507.5','remaining_rear_orders':q.ids(q.block(aq,'items')),'retained_rear_ship_id':117441817,'next_paid_colonizer_ready':all(checks.values()),'calendar_ready':False,'scope':'Five ordinary orders normally cancelled, full refund; one original rear birth retained. Not six-ship completion, maintenance, clearance, colony recovery or mineral-fleet acceptance.'}
h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert all(checks.values()), 'Original refund FAIL retained; no replay or calendar'
