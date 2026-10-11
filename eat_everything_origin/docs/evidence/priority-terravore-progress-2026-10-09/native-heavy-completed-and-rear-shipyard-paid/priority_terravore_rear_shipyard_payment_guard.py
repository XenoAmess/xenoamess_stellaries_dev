"""Exact paused native rear shipyard payment, no actions or calendar."""
import json, logging, shutil, sys, zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO); h = r.harness; run, user, meta = h.load_run()
dest = run / Path(__file__).name
if dest.exists(): assert dest.read_bytes() == Path(__file__).read_bytes()
else: shutil.copyfile(__file__, dest)
load = lambda n: json.loads((run / n).read_text('utf-8'))
before = 'terravore-mother-heavy-completed-boundary'; after = 'terravore-rear-shipyard-paid'
def read(st):
 with zipfile.ZipFile(run / (st + '.sav')) as z: fs = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(st + '.audit.json'), fs, {k:v for k,v,o in fs if o}
def omit(t, ks): return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br = read(before); a,af,ar = read(after)
bc,ac = b['countries']['0'],a['countries']['0']
cb,ca = [q.block(t['country'],'0') for t in [br,ar]]
mb,ma = [q.block(t,'modules') for t in [cb,ca]]
eb,ea = [q.block(t,'standard_economy_module') for t in [mb,ma]]
bcon,acon = br['construction'],ar['construction']
bqm,aqm = [q.block(t,'queue_mgr') for t in [bcon,acon]]
bim,aim = [q.block(t,'item_mgr') for t in [bcon,acon]]
bqs,aqs = [q.block(t,'queues') for t in [bqm,aqm]]
bis,ais = [q.block(t,'items') for t in [bim,aim]]
bq,aq = [q.block(t,'2278') for t in [bqs,aqs]]
item = q.block(ais,'33554473')
pre = load(before + '-war1-battle-v47-proof.json'); ex = load(before + '-battle-v47-execution.json')
source = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/starbase_modules/00_starbase_modules.txt')
native = run / 'native-rear-shipyard-00_starbase_modules.txt'
if native.exists(): assert native.read_bytes() == source.read_bytes()
else: shutil.copyfile(source,native)
checks = {
 'production02_simp_chinese_unchanged_tree':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'prior72_PASS_actual0_exact_source_bound':len(pre['checks'])==72 and all(v is True for v in pre['checks'].values()) and pre['status'].startswith('PASS_') and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v47.py')=='4e3e07a0e52eec4872db56faa273d15a21c0f1776208c39d079578d2940637fa',
 'same_date_exact_original_SHA_pair':b['date']==a['date']=='2271.05.03' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='c72e7f7036e47c2326cff3e07abce631b33b4ae46469eaf70a5fdca167f09d77' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='ae606587d8731ed5ddc940c9c86cd835b27bbe544d1f77ec567f0e2cbd296454',
 'exact50_alloy_debit_other_true_banks_held':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==50 and {k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'} and bc['research_stockpile']==ac['research_stockpile'],
 'other_countries_and_country0_non_economy_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(cb,{'modules'})==omit(ca,{'modules'}) and omit(mb,{'standard_economy_module'})==omit(ma,{'standard_economy_module'}) and omit(eb,{'resources'})==omit(ea,{'resources'}),
 'economy_only_alloy_scalar_changed':omit(q.block(eb,'resources'),{'alloys'})==omit(q.block(ea,'resources'),{'alloys'}) and q.scalars(q.block(ea,'resources'))['alloys']==ac['effective_stockpile']['alloys'],
 'only2278_empty_queue_one_append':omit(bqs,{'2278'})==omit(aqs,{'2278'}) and omit(bq,{'items'})==omit(aq,{'items'}) and q.ids(q.block(bq,'items'))==[] and q.ids(q.block(aq,'items'))==[33554473] and q.scalars(aq)=={'owner':0,'simultaneous':1,'type':'starbase'} and q.scalars(q.block(aq,'location'))=={'type':0,'id':67109591},
 'only_heavy_retired_none_slot41_reused':omit(bis,{'16777257'})==omit(ais,{'33554473'}) and [(v,o) for k,v,o in q.fields(bis) if k=='16777257']==[('none',False)] and not any(k=='33554473' for k,v,o in q.fields(bis)) and not any(k=='16777257' for k,v,o in q.fields(ais)) and 33554473-16777257==16777216,
 'exact_native_shipyard_order_schema':q.scalars(item)=={'queue':2278,'paying_country':0,'progress':0,'progress_needed':180} and q.scalars(q.block(item,'resources'))=={'alloys':50} and q.scalars(q.block(item,'buildable_starbase_module'))=={'starbase_module':'shipyard','slot':0,'starbase':153} and [k for k,v,o in q.fields(item)]==['queue','paying_country','progress','progress_needed','resources','buildable_starbase_module'],
 'all_other_construction_fields_held':omit(bcon,{'queue_mgr','item_mgr'})==omit(acon,{'queue_mgr','item_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
 'only_exact_two_fleet_dirty_cache_append':omit(br['fleet'],{'64','16778062'})==omit(ar['fleet'],{'64','16778062'}) and all(omit(q.block(br['fleet'],fid),{'properties'})==omit(q.block(ar['fleet'],fid),{'properties'}) and list(q.fields(q.block(q.block(ar['fleet'],fid),'properties')))==list(q.fields(q.block(q.block(br['fleet'],fid),'properties')))+[('dirty_cloaking_strength','yes',False)] for fid in ['64','16778062']),
 'all_other_ordered_top_raw_held':[(k,v,o) for k,v,o in bf if k not in {'country','construction','fleet'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','fleet'}],
 'all_world_population_EEP_technology_structures_held':all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','event_targets','situations']) and all(bc[k]==ac[k] for k in ['flags','variables','government','tech_status','owned_colonies']),
 'normal_one_click_and_save_actual0':load('terravore-rear-shipyard-paid-click-execution.json')['returncode']==load(after+'-native-save-execution.json')['returncode']==0 and load('terravore-rear-shipyard-paid-action.action.json')['client_point']==[592,587],
 'UI50_180_quote_original_image_bound':h.sha256(run/'terravore-rear-shipyard-module-quote-visible.jpg')==load('terravore-rear-shipyard-module-quote-visible.ocr.json')['image_sha256'],
 'native_full_module_source_bound':h.sha256(source)==h.sha256(native)=='edeaad451ff4aa5656650a51c94197fdb693cfb241f84dcb2be2a17149d023a5',
 'full_unfiltered_error2814_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2814,
 'no_pending_country0':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
}
passed=all(v is True for v in checks.values())
proof={'status':'PASS_TERRAVORE_NATIVE_REAR_SHIPYARD_PAYMENT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'paid_alloys':50,'native_order_id':33554473,'native_order_raw':item,'short_idle_war_calendar_ready':False,'calendar_ready':False,'colony523_order_recovery_pending':True,'scope':'One paid rear shipyard order, no completion or restored colony route. Only next separately documented one-day work calibration allowed.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids']:proof[key]=pre[key]
out=run/(after+'-shipyard-payment-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed,'Preserve failed payment guard; do not repeat purchase'
