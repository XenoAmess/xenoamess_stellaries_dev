"""Exact normal native attack-follow orders for the two existing paid fleets."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-raid-contact214-ack';after='terravore-raid-attack-ordered'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after)
omit=lambda v,ks:[(k,x,o) for k,x,o in q.fields(v) if k not in ks]
objects=lambda v:{k:x for k,x,o in q.fields(v)}
pre=json.loads((run/(before+'-multiple-first-contact-info-v2-proof.json')).read_text('utf-8'))
checks={
 'same_actual_date':b['date']==a['date']=='2261.07.02',
 'original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'bound31_contact_clearance_PASS_actual_exit0':pre['status']=='PASS_NATIVE_MULTIPLE_FIRST_CONTACT_INFORMATION_ACK_COMPONENT' and len(pre['checks'])==31 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and pre['remaining_country0_pending']==[] and json.loads((run/(before+'-guard-v2-execution.json')).read_text('utf-8'))['returncode']==0,
 'all_other_top_level_ordered_raw_held':[(k,v,o) for k,v,o in bf if k not in {'fleet','starbase_mgr','random_count','camera_focus'}]==[(k,v,o) for k,v,o in af if k not in {'fleet','starbase_mgr','random_count','camera_focus'}],
 'exact_two_orders_random_count_plus4':[(v,o) for k,v,o in bf if k=='random_count']==[('88314279',False)] and [(v,o) for k,v,o in af if k=='random_count']==[('88314283',False)],
 'exact_navigation_camera0_added':not [(v,o) for k,v,o in bf if k=='camera_focus'] and [(v,o) for k,v,o in af if k=='camera_focus']==[('0',False)],
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'all_countries_raw_held':br['country']==ar['country'],
 'all_actual_ships_raw_held':br['ships']==ar['ships'],
 'all_actual_leaders_raw_held':br['leaders']==ar['leaders'],
 'unfiltered_error2670_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
bfl,afl=[objects(rt['fleet']) for rt in [br,ar]]
checks['exact_two_fleets_only_changed']=set(bfl)==set(afl) and {i for i,v in bfl.items() if v!=afl[i]}=={'16777797','602'}
enemypos={'x':-91.07622,'y':-77.58861,'origin':0}
for fid,oid,n in [('16777797',1,18),('602',0,1)]:
 old,new=bfl[fid],afl[fid];movement=q.block(new,'movement_manager');oldmovement=q.block(old,'movement_manager');order=q.block(q.block(new,'current_order'),'follow_order');path=q.block(movement,'path')
 checks[fid+'_all_non_command_raw_held']=omit(old,{'current_order','order_id','movement_manager'})==omit(new,{'current_order','order_id','movement_manager'})
 checks[fid+'_exact_follow_attack18_order']=not q.block(old,'current_order') and [(k,o) for k,v,o in q.fields(q.block(new,'current_order'))]==[('follow_order',True)] and q.scalars(order)=={'fleet':18,'attack_when_in_range':'yes','can_reach':'yes','order_id':oid,'commissioner':4294967295} and q.scalars(q.block(order,'coordinate'))=={'x':0,'y':0,'origin':4294967295} and q.scalars(new)['order_id']==oid+1 and q.scalars(old).get('order_id',0)==oid
 checks[fid+'_exact_movement_target_and_path']=q.scalars(q.block(q.block(movement,'target'),'target'))=={'type':3,'id':18} and q.scalars(q.block(movement,'target_coordinate'))==enemypos and q.scalars(path)=={'date':'2261.07.19'} and [(k,o) for k,v,o in q.fields(path)]==[('node',True),('date',False)] and q.scalars(q.block(path,'node'))=={'ftl':'jump_hyperlane'} and q.scalars(q.block(q.block(path,'node'),'coordinate'))==enemypos
 checks[fid+'_original_position_formation_ftl_held_orbit_cleared']=omit(oldmovement,{'target','target_coordinate','path','orbit','time_since_last_path_update'})==omit(movement,{'target','target_coordinate','path','orbit','time_since_last_path_update'}) and not q.block(movement,'orbit').strip() and 'time_since_last_path_update' not in q.scalars(movement) and q.scalars(q.block(q.block(oldmovement,'orbit'),'orbitable'))=={'starbase':0}
 checks[fid+'_same_original_paid_ships_no_active_combat']=q.ids(q.block(old,'ships'))==q.ids(q.block(new,'ships')) and len(q.ids(q.block(new,'ships')))==n and not q.block(q.block(new,'combat'),'in_combat_with')
bs,ass=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]]
checks['exact_starbase_orbitals_two_departures_only']=q.scalars(q.block(bs,'orbitals'))=={'0':16777797,'1':602,'2':4294967295} and q.scalars(q.block(ass,'orbitals'))=={'0':4294967295,'1':4294967295,'2':4294967295} and omit(bs,{'orbitals'})==omit(ass,{'orbitals'}) and omit(q.block(br['starbase_mgr'],'starbases'),{'0'})==omit(q.block(ar['starbase_mgr'],'starbases'),{'0'}) and omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'})
for k in ['effective_stockpile','research_stockpile','budget_categories','variables','flags','government','traditions','ascension_perks','tech_status']:
 checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:
 checks[k+'_held']=b[k]==a[k]
for st in ['terravore-raid-main-attack','terravore-raid-second-attack']:
 action=json.loads((run/(st+'.action.json')).read_text('utf-8'))
 checks[st+'_actual_right_click_exit0']=action['action']=='right-click' and action['client_point']==[625,280] and action['foreground_after']==action['expected_hwnd'] and json.loads((run/(st+'-execution-execution.json')).read_text('utf-8'))['returncode']==0
checks['actual_unique_save_exit0']=json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0
p={'status':'PASS_TERRAVORE_NATIVE_RAID_ATTACK_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':all(checks.values()),'actual_attack_fleets':[16777797,602],'actual_target_fleet':18,'scope':'Exact normal orders only. 30-day combat observation is allowed; no arrival, victory, casualties, repair or full-route acceptance claimed.'}
out=run/(after+'-raid-attack-order-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original raid attack order FAIL retained'
