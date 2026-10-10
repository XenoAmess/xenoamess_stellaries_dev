"""Exact normal survey of known Aswiri80 with existing science ship1."""
import json,logging,shutil,sys,zipfile,itertools
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-forge-paid';after='terravore-aswiri-survey-ordered'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def omit(v,ks):return [(k,x,o) for k,x,o in q.fields(v) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);old,new=[q.block(rt['fleet'],'1') for rt in [br,ar]];om,nm=[q.block(f,'movement_manager') for f in [old,new]]
pre=json.loads((run/(before+'-forge-payment-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
orders=[v for block in ['current_order','order'] for k,v,o in q.fields(q.block(new,block)) if k=='survey_planet_order' and o];expected=[912,910,908,909,911,913,917,916,914,915,921,920,918,919]
path=q.block(nm,'path');nodes=[v for k,v,o in q.fields(path) if k=='node' and o];origins=[q.scalars(q.block(v,'coordinate'))['origin'] for v in nodes]
checks={
 'same_date_original_SHA_pair':b['date']==a['date']=='2263.05.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior19_forge_payment_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_NATIVE_FOUNDRY_REPLACEMENT_PAYMENT_COMPONENT' and len(pre['checks'])==19 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='094389416193543c62b16f3f57d8c2d66b6bad77222a264a4f006c7b9a1d2a63',
 'all_other_ordered_top_raw_held':[(k,v,o) for k,v,o in bf if k not in {'fleet','random_count','camera_focus'}]==[(k,v,o) for k,v,o in af if k not in {'fleet','random_count','camera_focus'}],
 'only_original_fleet1_four_command_fields_changed':omit(br['fleet'],{'1'})==omit(ar['fleet'],{'1'}) and omit(old,{'movement_manager','current_order','order','order_id'})==omit(new,{'movement_manager','current_order','order','order_id'}),
 'original_ship1_scientist_and_hp_held':q.ids(q.block(new,'ships'))==[1] and q.scalars(new)['hit_points']==375 and q.scalars(q.block(ar['ships'],'1'))['leader']==150994969 and br['ships']==ar['ships'] and br['leaders']==ar['leaders'],
 'exact14_zero_progress_reachable_native_orders':len(orders)==14 and all(q.scalars(v)=={'progress':0,'can_reach':'yes','order_id':47+i,'commissioner':4294967295} and q.scalars(q.block(v,'deposit_holder'))=={'type':0,'id':expected[i]} for i,v in enumerate(orders)),
 'one_current_thirteen_queued_counter47_to61':[(k,o) for k,v,o in q.fields(q.block(new,'current_order'))]==[('survey_planet_order',True)] and [(k,o) for k,v,o in q.fields(q.block(new,'order'))]==[('survey_planet_order',True)]*13 and not q.block(old,'current_order').strip() and not q.block(old,'order').strip() and q.scalars(old)['order_id']==47 and q.scalars(new)['order_id']==61,
 'all_targets_exact_system80_bodies':set(expected)=={int(v) for k,v,o in q.fields(q.block(ar['galactic_object'],'80')) if k=='planet' and not o} and 0 in q.ids(q.block(q.block(ar['galactic_object'],'80'),'discovery')),
 'only_four_movement_target_path_fields_changed':omit(om,{'path','target','target_coordinate','time_since_last_path_update'})==omit(nm,{'path','target','target_coordinate','time_since_last_path_update'}) and q.block(om,'coordinate')==q.block(nm,'coordinate'),
 'exact_three_nodes97_to80_native_estimate':len(nodes)==3 and origins==[97,80,80] and q.scalars(path)=={'date':'2263.08.12'} and q.scalars(q.block(nm,'target_coordinate'))=={'x':-3.24065,'y':100.82615,'origin':80},
 'exact_random_plus2_camera70_removed':[(v,o) for k,v,o in bf if k=='random_count']==[('113725537',False)] and [(v,o) for k,v,o in af if k=='random_count']==[('113725539',False)] and [(v,o) for k,v,o in bf if k=='camera_focus']==[('70',False)] and not any(k=='camera_focus' for k,v,o in af),
 'all_countries_economy_research_forge_order_raw_held':br['country']==ar['country'] and br['construction']==ar['construction'] and a['countries']==b['countries'],
 'normal_click_and_save_actual_exit0':all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-aswiri-survey-order-click',after+'-save']) and json.loads((run/'terravore-aswiri-survey-order-click.action.json').read_text('utf-8'))['client_point']==[612,435],
 'known_search_result_and_survey_menu_image_SHA_bound':all(h.sha256(run/(st+'.jpg'))==json.loads((run/(st+'.ocr.json')).read_text('utf-8'))['image_sha256'] for st in ['terravore-aswiri-search-result','terravore-aswiri-survey-menu']),
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
p={'status':'PASS_TERRAVORE_KNOWN_ASWIRI_NATIVE_SURVEY_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_targets':expected,'actual_native_estimate':'2263.08.12','calendar_ready':all(checks.values()),'scope':'One normal14-body survey order for already-known80 using existing ship1. Not arrived, surveyed, colonizable or full-route acceptance.'}
out=run/(after+'-aswiri-survey-order-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original survey order FAIL retained'
