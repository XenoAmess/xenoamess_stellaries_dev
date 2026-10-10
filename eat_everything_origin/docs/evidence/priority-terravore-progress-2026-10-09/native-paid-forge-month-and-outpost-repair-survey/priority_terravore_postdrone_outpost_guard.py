"""Exact new paid native outpost order after actual drone victory."""
import sys,json,logging,shutil,zipfile,itertools
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-postdrone-repair-ordered';after='terravore-postdrone-outpost-paid'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
old,new=[q.block(rt['fleet'],'2') for rt in [br,ar]];om,nm=[q.block(f,'movement_manager') for f in [old,new]]
pre=json.loads((run/(before+'-repair-order-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
order=q.block(q.block(new,'current_order'),'build_orbital_station_order');move=q.block(q.block(order,'sub_order'),'move_to_system_point_order');coords={'x':18.13646,'y':-24.60951,'origin':97}
cb,ca=[q.block(rt['country'],'0') for rt in [br,ar]];mb,ma=[q.block(t,'modules') for t in [cb,ca]];eb,ea=[q.block(t,'standard_economy_module') for t in [mb,ma]];rb,ra=[q.block(t,'resources') for t in [eb,ea]]
nodes=[v for k,v,o in q.fields(q.block(nm,'path')) if k=='node' and o];route=[k for k,g in itertools.groupby(q.scalars(q.block(v,'coordinate'))['origin'] for v in nodes)]
checks={
 'original_SHA_pair_same_date':a['date']==b['date']=='2263.11.17' and b['save_sha256']=='3938fdb2e24435d7bf561eeb817ec500a5363a74ef61e7c4ddf7fd273c1fc5a1' and a['save_sha256']=='9f85a96d9485b62cb207a8be96e3a06a9a0052306d689e84487dbb3b660dd0db' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior14_repair_order_PASS_actual0':pre['status']=='PASS_TERRAVORE_NATIVE_REPAIR_ORDER_COMPONENT' and len(pre['checks'])==14 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='9537f63d2f47ef5e9c4f689548381239e7eeab4fe2893fafd31823866bfcdf1b',
 'all_other_ordered_top_raw_held':[(k,v,o) for k,v,o in bf if k not in {'fleet','country','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'fleet','country','random_count'}],
 'only_original_constructor_three_order_fields_changed':omit(br['fleet'],{'2'})==omit(ar['fleet'],{'2'}) and omit(old,{'movement_manager','order_id','current_order'})==omit(new,{'movement_manager','order_id','current_order'}),
 'only_four_movement_fields_changed_position_state_held':omit(om,{'target','target_coordinate','path','time_since_last_path_update'})==omit(nm,{'target','target_coordinate','path','time_since_last_path_update'}) and q.scalars(om)['time_since_last_path_update']==18 and 'time_since_last_path_update' not in q.scalars(nm),
 'unique_native_outpost_order_counter11_to12':q.scalars(old)['order_id']==11 and q.scalars(new)['order_id']==12 and not q.block(old,'current_order').strip() and [(k,o) for k,v,o in q.fields(q.block(new,'current_order'))]==[('build_orbital_station_order',True)] and q.scalars(order)=={'progress':0,'cost':0,'in_progress':'no','class':'shipclass_starbase','can_reach':'yes','order_id':11,'commissioner':4294967295} and not q.block(new,'order').strip(),
 'native_design_holder_resources_exact':q.scalars(q.block(order,'deposit_holder'))=={'type':0,'id':1078} and q.scalars(q.block(order,'ship_design'))=={'design':201326648,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(order,'resources'))=={'influence':225,'alloys':100},
 'native_destination_reachable_system97':q.scalars(move)=={'can_reach':'yes','commissioner':4294967295} and all(q.scalars(t)==coords for t in [q.block(move,'coordinate'),q.block(nm,'target_coordinate'),q.block(q.block(nm,'target'),'coordinate')]),
 'nine_nodes_native_hyperlanes_and_estimate':len(nodes)==9 and route==[171,70,30,80,97] and all('to='+str(y) in q.block(q.block(ar['galactic_object'],str(x)),'hyperlane') for x,y in zip(route,route[1:])) and q.scalars(q.block(nm,'path'))=={'date':'2264.09.08'},
 'only_country0_resources_changed':omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(cb,{'modules'})==omit(ca,{'modules'}) and omit(mb,{'standard_economy_module'})==omit(ma,{'standard_economy_module'}) and omit(eb,{'resources'})==omit(ea,{'resources'}),
 'only_real100_alloys225_influence_payment':omit(rb,{'alloys','influence'})==omit(ra,{'alloys','influence'}) and D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==100 and D(str(bc['effective_stockpile']['influence']))-D(str(ac['effective_stockpile']['influence']))==225,
 'all_other_true_stock_banks_and90menace_held':{k:v for k,v in bc['effective_stockpile'].items() if k not in {'alloys','influence'}}=={k:v for k,v in ac['effective_stockpile'].items() if k not in {'alloys','influence'}} and bc['research_stockpile']==ac['research_stockpile'] and ac['effective_stockpile']['menace']==90,
 'random_exact_plus2':[(v,o) for k,v,o in bf if k=='random_count']==[('120528969',False)] and [(v,o) for k,v,o in af if k=='random_count']==[('120528971',False)],
 'UI_quote_original_image_bound':h.sha256(run/'terravore-postdrone-outpost-price-visible.jpg')==json.loads((run/'terravore-postdrone-outpost-price-visible.ocr.json').read_text('utf-8'))['image_sha256'],
 'normal_paid_click_and_save_actual0':all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-postdrone-outpost-paid-click',after+'-save']) and json.loads((run/'terravore-postdrone-outpost-paid-click.action.json').read_text('utf-8'))['client_point']==[635,516],
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered2670_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
p={'status':'PASS_TERRAVORE_POSTDRONE_NEW_OUTPOST_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'new_actual_payment':{'alloys':100,'influence':225},'native_path':route,'native_estimate':'2264.09.08','calendar_ready':all(checks.values()),'scope':'New actual payment and legal native constructor order only. Old refund not credited; no arrival, outpost completion or colony claim.'}
out=run/(after+'-new-outpost-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original new outpost FAIL retained'
