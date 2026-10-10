"""Exact normal survey command for visited Yodd Bem; no simulation or grants."""
import itertools,json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-labs-stable-month';after='terravore-yodd-survey-ordered'
def read(stage):
 a=json.loads((run/(stage+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stage+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bf,af=[{k:v for k,v,o in q.fields(rt['fleet']) if o} for rt in [br,ar]];old,new=bf['1'],af['1'];os,ns=q.scalars(old),q.scalars(new)
allowed={'movement_manager','order_id','order','current_order','auto_movement'}
od,nd=[{k:(v,o) for k,v,o in q.fields(v)} for v in [old,new]];changed={k for k in set(od)|set(nd) if od.get(k)!=nd.get(k)}
current=q.block(q.block(new,'current_order'),'survey_planet_order');queued=[v for k,v,o in q.fields(q.block(new,'order')) if k=='survey_planet_order' and o];orders=[current]+queued
ids=[q.scalars(q.block(v,'deposit_holder')).get('id') for v in orders];expected=[1083,1081,1086,1078,1079,1084,1085,1080,1082,2072]
bm,am=[q.block(v,'movement_manager') for v in [old,new]];move_keys={'target','target_coordinate','path','orbit','time_since_last_path_update'}
bp,ap=[{k:v for k,v,o in q.fields(q.block(rt['planets'],'planet')) if o} for rt in [br,ar]]
path=q.block(am,'path');origins=[q.scalars(q.block(v,'coordinate'))['origin'] for k,v,o in q.fields(path) if k=='node' and o];route=[k for k,g in itertools.groupby(origins)]
pre=json.loads((run/(before+'-labs-stable-month-ledger-proof.json')).read_text('utf-8'));boundary=json.loads((run/(before+'-labs-stable-month-boundary-proof.json')).read_text('utf-8'))
checks={
 'bound_stable_month17_and_boundary53_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_LABS_STABLE_MONTH_LEDGER_COMPONENT' and len(pre['checks'])==17 and all(v is True for v in pre['checks'].values()) and boundary['status']=='PASS_TERRAVORE_LABS_STABLE_MONTH_BOUNDARY_COMPONENT' and len(boundary['checks'])==53 and all(v is True for v in boundary['checks'].values()) and pre['after_sha256']==boundary['after_sha256']==b['save_sha256'] and all(json.loads((run/(before+suffix+'-execution.json')).read_text('utf-8'))['returncode']==0 for suffix in ['-ledger-guard','-guard']),
 'same_date_original_SHA_pair':b['date']==a['date']=='2260.07.02' and all(h.sha256(run/(st+'.sav'))==v['save_sha256'] for st,v in [(before,b),(after,a)]),
 'only_original_fleet1_changes':set(bf)==set(af) and [k for k in bf if bf[k]!=af[k]]==['1'],
 'exact_five_command_fields_and_other_fleet_raw_held':changed==allowed and omit(old,allowed)==omit(new,allowed),
 'all_ships_and_scientists_raw_held':br['ships']==ar['ships'] and br['leaders']==ar['leaders'] and q.scalars(q.block(ar['ships'],'1'))['leader']==150994969,
 'native_existing_science_ship_and_counter37_to47':os['ship_class']==ns['ship_class']=='shipclass_science_ship' and q.ids(q.block(old,'ships'))==q.ids(q.block(new,'ships'))==[1] and os['order_id']==37 and ns['order_id']==47,
 'exact10_native_zero_progress_reachable_targets':ids==expected and len(orders)==10 and all(q.scalars(v)=={'progress':0,'can_reach':'yes','order_id':37+i,'commissioner':4294967295} and q.scalars(q.block(v,'deposit_holder'))=={'type':0,'id':expected[i]} for i,v in enumerate(orders)),
 'only_one_current_and9_queued_survey_orders':[(k,o) for k,v,o in q.fields(q.block(new,'current_order'))]==[('survey_planet_order',True)] and [(k,o) for k,v,o in q.fields(q.block(new,'order'))]==[('survey_planet_order',True)]*9 and not q.block(old,'current_order') and not q.block(old,'order'),
 'targets_exact_all_system97_planets':set(ids)=={int(v) for k,v,o in q.fields(q.block(ar['galactic_object'],'97')) if k=='planet' and not o},
 'current_orbit_suborder_correct_planet1083_star1078':q.scalars(q.block(q.block(q.block(current,'sub_order'),'orbit_planet_order'),'orbitable'))=={'planet':1083} and q.scalars(q.block(q.block(q.block(current,'sub_order'),'orbit_planet_order'),'star'))=={'planet':1078},
 'actual_native_path_and_target97':route==[0,103,151,188,139,171,70,30,80,97] and q.scalars(path)['date']=='2262.01.16' and q.scalars(q.block(am,'target_coordinate'))['origin']==97,
 'noncommand_movement_raw_and_current_position_held':omit(bm,move_keys)==omit(am,move_keys) and q.block(bm,'coordinate')==q.block(am,'coordinate'),
 'old_arrived_auto_move7_removed':q.scalars(q.block(old,'auto_movement'))=={'type':'auto_move_planet','auto_move_target':7,'clear_on_new_orders':'yes','has_arrived':'yes'} and not q.block(new,'auto_movement'),
 'old_orbit7_cleared':q.scalars(q.block(q.block(bm,'orbit'),'orbitable'))=={'planet':7} and not q.block(am,'orbit').strip(),
 'all_planets_except_exact_mother_orbit_raw_held':set(bp)==set(ap) and [k for k in bp if bp[k]!=ap[k]]==['7'] and omit(bp['7'],{'planet_orbitals'})==omit(ap['7'],{'planet_orbitals'}) and omit(br['planets'],{'planet'})==omit(ar['planets'],{'planet'}),
 'physical7_only_fleet1_orbit_sentinel_change':q.scalars(q.block(bp['7'],'planet_orbitals'))=={'0':1,'1':171} and q.scalars(q.block(ap['7'],'planet_orbitals'))=={'0':4294967295,'1':171},
 'all_countries_ordered_raw_held':br['country']==ar['country'],
 'all_other_top_ordered_raw_held':omit(bt,{'fleet','planets','random_count','camera_focus'})==omit(at,{'fleet','planets','random_count','camera_focus'}),
 'actual_navigation_and_order_random_plus4':q.scalars(bt)['random_count']==74970664 and q.scalars(at)['random_count']==74970668,
 'only_old_camera_focus0_removed':q.scalars(bt).get('camera_focus')==0 and 'camera_focus' not in q.scalars(at),
 'all_true_stocks_and_research_banks_held':bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile'],
 'no_country0_pending':not [v for t in [bt,at] for k,v,o in q.fields(t) if k=='player_event' and q.scalars(v).get('country')==0],
 'normal_order_click_and_save_actual_exit0':json.loads((run/('terravore-yodd-survey-order-click.action.json')).read_text('utf-8'))['client_point']==[618,434] and all(json.loads((run/(stage+'-execution.json')).read_text('utf-8'))['returncode']==0 for stage in ['terravore-yodd-survey-order-click',after+'-save']),
 'unfiltered_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
proof={'status':'PASS_TERRAVORE_YODD_NATIVE_SURVEY_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_route':route,'actual_first_arrival_estimate':q.scalars(path)['date'],'actual_survey_targets':ids,'calendar_ready':True,'scope':'One normal native order only; no arrival, completed survey, colonization, menace or full route claim.'}
out=run/(after+'-yodd-survey-order-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original survey order FAIL retained; no repeated order'
