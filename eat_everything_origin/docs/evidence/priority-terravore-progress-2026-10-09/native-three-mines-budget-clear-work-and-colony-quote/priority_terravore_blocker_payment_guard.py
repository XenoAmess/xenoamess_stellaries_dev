"""Exact same-day native 300-energy payment for blocker272, behind paid mine."""
import json, logging, shutil, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-colony1085-devour-started';after='terravore-mother-blocker-clear-paid'
load=lambda name:json.loads((run/name).read_text('utf-8'))
def read(stage):
 with zipfile.ZipFile(run/(stage+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(stage+'.audit.json'),fs,{k:v for k,v,o in fs if o}
def omit(raw,keys):return [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=load(before+'-third-start-v2-proof.json');ex=load(before+'-guard-v2-execution.json')
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bm,am=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(m,'standard_economy_module') for m in [bm,am]]
bcon,acon=br['construction'],ar['construction'];bqm,aqm=[q.block(c,'queue_mgr') for c in [bcon,acon]]
bqs,aqs=[q.block(m,'queues') for m in [bqm,aqm]];bq,aq=[q.block(qs,'0') for qs in [bqs,aqs]]
bim,aim=[q.block(c,'item_mgr') for c in [bcon,acon]];bi,ai=[q.block(m,'items') for m in [bim,aim]]
order=q.block(ai,'1224736779')
click=load('terravore-mother-blocker-clear-click-execution.json');action=load('terravore-mother-blocker-clear-click.action.json');save_ex=load(after+'-native-save-execution.json')
checks={
 'production02_Chinese_exact_date_SHA_pair':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and b['date']==a['date']=='2270.02.01' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='e030634f1d921a002869cff7a5a3639e0aae56fb9b5a93455d4158572b10281a' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='14c59f182e97cbfff4d46a4cb7d444b027c6cbc2a8009a812b1d19f68c5be4e1',
 'prior_third_start35_PASS_actual0_source_bound':pre['status']=='PASS_TERRAVORE_THIRD_NATIVE_START_COMPONENT' and len(pre['checks'])==35 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_third_native_start_guard_v2.py')=='801ddc424c827482d5b3f2bdf5c0f312da784d1215ecb501b74c1ab1bc8fe4b6',
 'normal_one_click_and_one_save_actual0_bound':click['returncode']==save_ex['returncode']==0 and click['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and save_ex['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and action['action']=='left-click' and action['client_point']==[270,421],
 'exact300_energy_only_real_payment_all_research_banks_held':D(str(bc['effective_stockpile']['energy']))-D(str(ac['effective_stockpile']['energy']))==300 and all(ac['effective_stockpile'][k]==v for k,v in bc['effective_stockpile'].items() if k!='energy'),
 'same_serial_queue0_only_appended_clear_order':omit(bq,{'items'})==omit(aq,{'items'}) and q.ids(q.block(bq,'items'))==[905969668] and q.ids(q.block(aq,'items'))==[905969668,1224736779],
 'exact_new_clear272_order_120_work_0_progress_300_energy':q.scalars(order)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':120} and q.scalars(q.block(order,'resources'))=={'energy':300} and q.scalars(q.block(order,'buildable_clear_deposit_blocker'))=={'deposit':272,'planet':0} and [(k,o) for k,v,o in q.fields(order)]==[('queue',False),('paying_country',False),('progress',False),('progress_needed',False),('resources',True),('buildable_clear_deposit_blocker',True)] and not any(k=='1224736779' for k,v,o in q.fields(bi)),
 'all_other_queues_and_old_items_raw_held':omit(bqs,{'0'})==omit(aqs,{'0'}) and list(q.fields(bi))==omit(ai,{'1224736779'}),
 'construction_other_manager_fields_held':omit(bcon,{'queue_mgr','item_mgr'})==omit(acon,{'queue_mgr','item_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
 'existing_mine_exact137point2_held':q.block(bi,'905969668')==q.block(ai,'905969668') and q.scalars(q.block(ai,'905969668'))['progress']==137.2,
 'all_other_countries_and_country0_fields_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(bcr,{'modules'})==omit(acr,{'modules'}),
 'only_economic_energy_field_changed':omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}) and omit(q.block(be,'resources'),{'energy'})==omit(q.block(ae,'resources'),{'energy'}) and D(str(q.scalars(q.block(be,'resources'))['energy']))-D(str(q.scalars(q.block(ae,'resources'))['energy']))==300,
 'every_other_top_level_full_field_held':[(k,v,o) for k,v,o in bf if k not in {'country','construction'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction'}],
 'exact_native_quote_image_bound':h.sha256(run/'terravore-energy-recovery-blocker-quote-visible.jpg')==load('terravore-energy-recovery-blocker-quote-visible.ocr.json')['image_sha256']=='3c6bbff5d7ba6d42673958f76b5e33411d2e3983671d06f3dd520aee8b9c4f08',
 'no_pending_and_strict2814_error_bytes':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0] and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
native_source=Path('C:\\SteamLibrary\\steamapps\\common\\Stellaris\\common\\deposits\\01_blocker_deposits.txt');native_sha='df9665890f54567b5988857e73baf752f690ad2fc8beb1ab7f543e184e43b11a';native_copy=run/'native-blocker-clear-01_blocker_deposits.txt'
if native_copy.exists():assert native_copy.read_bytes()==native_source.read_bytes()
else:shutil.copyfile(native_source,native_copy)
checks['native_blocker_definition_actual_source_bound']=h.sha256(native_source)==h.sha256(native_copy)==native_sha
anchor=load('terravore-colony1085-completion-boundary2-war1-battle-v29-proof.json');anchor_ex=load('terravore-colony1085-completion-boundary2-battle-v29-execution.json')
checks['exact_completed_military_report_anchor46_PASS_actual0_bound']=len(anchor['checks'])==46 and all(v is True for v in anchor['checks'].values()) and anchor_ex['returncode']==0 and anchor_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v29.py')=='7643c09fc6e6b1cce4dbb04c4ec1a4ce9ac6b3a8aaa6b2d052bf6c3d3014e35d' and anchor['after_sha256']=='ae5c07eb6112d217a7e9163c4b1ed8f4610083a8700ede82b73527c9b357202f'
proof={'status':'PASS_TERRAVORE_NATIVE_BLOCKER_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'actual_paid_energy':300,'actual_clear_order_id':1224736779,'actual_deposit_id':272,'actual_order_raw':order,'actual_stockpiles':ac['effective_stockpile'],'calendar_ready':all(checks.values()),'scope':'One paid clear-blocker order behind original third mine; not started or completed, no new generator or economy recovery claim.'}
for k in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids','actual_pending_destroyed_ship_ids','actual_naval_death_cache_credit']:proof[k]=anchor[k]
out=run/(after+'-blocker-payment-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert all(checks.values()),'Original payment differences retained; never repeat purchase'
