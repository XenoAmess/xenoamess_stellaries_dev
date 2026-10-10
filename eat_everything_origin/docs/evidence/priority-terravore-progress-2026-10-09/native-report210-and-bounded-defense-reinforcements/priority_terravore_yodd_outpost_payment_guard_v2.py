"""Read-only exact native constructor outpost order and real payment."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
before,after,system,planet,design,alloys,influence=sys.argv[1:];system,planet,design=map(int,(system,planet,design));alloys,influence=map(D,(alloys,influence))
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
b,bt,bfs,br=read(before);a,at,afs,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bf={k:v for k,v,o in q.fields(br['fleet']) if o};af={k:v for k,v,o in q.fields(ar['fleet']) if o};old,new=bf['2'],af['2']
of,nf={k:(v,o) for k,v,o in q.fields(old)},{k:(v,o) for k,v,o in q.fields(new)};changed={k for k in set(of)|set(nf) if of.get(k)!=nf.get(k)}
order=q.block(q.block(new,'current_order'),'build_orbital_station_order');os=q.scalars(order)
bm,am=q.block(old,'movement_manager'),q.block(new,'movement_manager');ma={'target','target_coordinate','path','time_since_last_path_update','state'}
bcs,acs={k:v for k,v,o in q.fields(br['country']) if o},{k:v for k,v,o in q.fields(ar['country']) if o};c0b,c0a=bcs['0'],acs['0'];cbm,cam=q.block(c0b,'modules'),q.block(c0a,'modules')
eb,ea=q.block(cbm,'standard_economy_module'),q.block(cam,'standard_economy_module')
skip={'country','fleet','random_count','camera_focus'}
bs,ass=q.scalars(bt),q.scalars(at)
checks={
 'same_actual_date':b['date']==a['date'],
 'original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'actual_exact_paid100_alloys225_influence':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==alloys and D(str(bc['effective_stockpile']['influence']))-D(str(ac['effective_stockpile']['influence']))==influence,
 'other_actual_stocks_and_true_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k not in ['alloys','influence']}=={k:v for k,v in ac['effective_stockpile'].items() if k not in ['alloys','influence']},
 'only_original_fleet2_changed':set(bf)==set(af) and [k for k in bf if bf[k]!=af[k]]==['2'],
 'exact_three_fleet_order_fields_changed':changed=={'movement_manager','order_id','current_order'},
 'other_fleet2_fields_raw_held':[(k,v,o) for k,v,o in q.fields(old) if k not in changed]==[(k,v,o) for k,v,o in q.fields(new) if k not in changed],
 'new_order_ids_from_original':q.scalars(new)['order_id']==q.scalars(old)['order_id']+1 and os['order_id']==q.scalars(old)['order_id'] and bool(q.block(q.block(old,'current_order'),'orbit_planet_order')),
 'native_outpost_type_design_target':os['class']=='shipclass_starbase' and q.scalars(q.block(order,'deposit_holder'))=={'type':0,'id':planet} and q.scalars(q.block(order,'ship_design'))=={'design':design,'upgrade':4294967295,'growth_stage':0},
 'native_order_zero_progress_not_started':os['progress']==0 and os['in_progress']=='no' and os['can_reach']=='yes',
 'exact_paid_order_resources':q.scalars(q.block(order,'resources'))=={'alloys':float(alloys),'influence':float(influence)},
 'native_path_target_correct_system':q.scalars(q.block(q.block(q.block(order,'sub_order'),'move_to_system_point_order'),'coordinate'))['origin']==system and q.scalars(q.block(am,'target_coordinate'))['origin']==system,
 'movement_only_five_known_command_fields':[(k,v,o) for k,v,o in q.fields(bm) if k not in ma]==[(k,v,o) for k,v,o in q.fields(am) if k not in ma],
 'original_actual_coordinate_orbit_held':q.block(bm,'coordinate')==q.block(am,'coordinate') and q.block(bm,'orbit')==q.block(am,'orbit'),
 'all_other_top_level_fields_raw_held_including_ships_planets_construction':[(k,v,o) for k,v,o in bfs if k not in skip]==[(k,v,o) for k,v,o in afs if k not in skip],
 'original_random_count_exact_plus2':ass['random_count']==bs['random_count']+2,
 'camera_focus_exact_held_or_original0_removed':([(k,v,o) for k,v,o in bfs if k=='camera_focus']==[(k,v,o) for k,v,o in afs if k=='camera_focus']) or (bs.get('camera_focus')==0 and 'camera_focus' not in ass),
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'country0_other_direct_fields_raw_held':[(k,v,o) for k,v,o in q.fields(c0b) if k!='modules']==[(k,v,o) for k,v,o in q.fields(c0a) if k!='modules'],
 'country0_other_modules_raw_held':[(k,v,o) for k,v,o in q.fields(cbm) if k!='standard_economy_module']==[(k,v,o) for k,v,o in q.fields(cam) if k!='standard_economy_module'],
 'economy_module_only_real_resources_changed':[(k,v,o) for k,v,o in q.fields(eb) if k!='resources']==[(k,v,o) for k,v,o in q.fields(ea) if k!='resources'],
 'no_country_pending':not any(k=='player_event' and q.scalars(v).get('country')==0 for k,v,o in bfs+afs),
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-before.log')).read_bytes(),
}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
pre=json.loads((run/(before+'-recovered-month-boundary-proof.json')).read_text('utf-8'));pex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'));ledger=json.loads((run/(before+'-recovered-month-ledger-proof.json')).read_text('utf-8'));lex=json.loads((run/(before+'-ledger-guard-execution.json')).read_text('utf-8'))
checks['exact_pair_prior36_and17_PASS_exit0']=before=='terravore-raid-recovered-month' and after=='terravore-yodd-outpost-paid' and b['date']==a['date']=='2262.05.17' and pre['status']=='PASS_TERRAVORE_RECOVERED_MONTH_BOUNDARY_COMPONENT' and len(pre['checks'])==36 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and pex['returncode']==0 and ledger['status']=='PASS_TERRAVORE_RECOVERED_MONTH_LEDGER_COMPONENT' and len(ledger['checks'])==17 and all(v is True for v in ledger['checks'].values()) and ledger['after_sha256']==b['save_sha256'] and lex['returncode']==0
checks['exact_actual_target1078_system97_design']=system==97 and planet==1078 and design==201326648 and alloys==100 and influence==225
bres,ares=[q.block(v,'resources') for v in [eb,ea]]
checks['economy_only_two_paid_fields_and_society_mirror_refreshed']=[(k,v,o) for k,v,o in q.fields(bres) if k not in {'alloys','influence','physics_research','society_research','engineering_research'}]==[(k,v,o) for k,v,o in q.fields(ares) if k not in {'alloys','influence','physics_research','society_research','engineering_research'}] and q.scalars(bres)['physics_research']==28.44192 and q.scalars(bres)['engineering_research']==29.99192 and 'physics_research' not in q.scalars(ares) and 'engineering_research' not in q.scalars(ares) and q.scalars(bres)['society_research']==4060.64878 and q.scalars(ares)['society_research']==bc['research_stockpile']['society_research']==ac['research_stockpile']['society_research']==3984.69762
checks['native_move_state_only_move_system_to_idle']=q.scalars(bm)['state']=='move_system' and q.scalars(am)['state']=='move_idle' and q.scalars(bm)['time_since_last_path_update']==638 and 'time_since_last_path_update' not in q.scalars(am)
checks['exact_native_order_fields_and_target_coordinate']=os=={'progress':0,'cost':0,'in_progress':'no','class':'shipclass_starbase','can_reach':'yes','order_id':10,'commissioner':4294967295} and q.scalars(q.block(q.block(q.block(order,'sub_order'),'move_to_system_point_order'),'coordinate'))=={'x':19.19504,'y':-15.00733,'origin':97} and q.scalars(q.block(am,'target_coordinate'))=={'x':19.19504,'y':-15.00733,'origin':97}
checks['true_bank_raw_held_and_ten_original_ship_orders_raw_held']=bc['research_stockpile']==ac['research_stockpile'] and br['construction']==ar['construction']
click=json.loads((run/'terravore-yodd-outpost-paid-click.action.json').read_text('utf-8'))
checks['unique_normal_payment_click_actual_exit0']=click['action']=='left-click' and click['client_point']==[636,479] and json.loads((run/'terravore-yodd-outpost-paid-click-execution.json').read_text('utf-8'))['returncode']==0
checks['normal_save_actual_exit0']=json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0
checks['UI_quote_image_bound']=h.sha256(run/'terravore-yodd-outpost-quote-visible.jpg')==json.loads((run/'terravore-yodd-outpost-quote-visible.ocr.json').read_text('utf-8'))['image_sha256']
original=json.loads((run/(after+'-paid-outpost-proof.json')).read_text('utf-8'));original_ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
checks['bound_original48_exact_one_mirror_FAIL_exit1']=original['status']=='FAIL' and len(original['checks'])==48 and [k for k,v in original['checks'].items() if v is not True]==['economy_only_two_paid_fields_and_society_mirror_refreshed'] and original['before_sha256']==b['save_sha256'] and original['after_sha256']==a['save_sha256'] and original_ex['returncode']==1 and original_ex['helper_sha256']=='e937c733787f103262c3dd7f5a590882f3edfcb56ca3ea1c65c7e6ea7312fcdd' and h.sha256(run/'priority_terravore_yodd_outpost_payment_guard.py')==original_ex['helper_sha256']
p={'status':'PASS_TERRAVORE_YODD_NATIVE_PAID_OUTPOST_V2_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_stocks_before_after':[bc['effective_stockpile'],ac['effective_stockpile']],'original_native_order':order,'native_path_ETA':q.scalars(q.block(am,'path')).get('date'),'scope':'One real paid constructor order; not arrival, outpost completion, colonization or full route. No pre-order influence UI quote claim.'}
out=run/(after+'-paid-outpost-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original outpost guard FAIL retained; no replay or next calendar'
