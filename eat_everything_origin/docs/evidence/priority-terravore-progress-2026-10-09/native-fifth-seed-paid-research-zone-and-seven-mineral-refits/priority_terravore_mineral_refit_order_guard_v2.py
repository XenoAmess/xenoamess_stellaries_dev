"""Read-only exact native zero cost seven original ship refit order."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-engineering-zone-paid-order';after='terravore-seven-minerals-refit-order';b,a=[read_state(run,s) for s in [before,after]]
ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0'];br,ar=b['roots'],a['roots']
pre=load(before+'-paid-zone-order-proof.json');px=load(before+'-guard-execution.json');obs=load(after+'-observation.json');sx=load(after+'-save-execution.json');ux=load('terravore-seven-mineral-native-upgrade-order-execution.json');quote=load('terravore-mineral-refit-normal-quote-ui.ocr.json');qx=load('terravore-mineral-refit-normal-quote-execution.json')
minerals={16777746,50333149,50333147,33554923,1960,1961,1962};fid='50332250'
old=b['designs']['184550902'];new=a['designs']['218105405'];replacement=old.replace('SMALL_PLASMA_1','SMALL_MASS_DRIVER_3').replace('MEDIUM_PLASMA_1','MEDIUM_MASS_DRIVER_3')
order=q.block(q.block(a['fleets'][fid],'current_order'),'upgrade_design_at_orbitable_fleet_order')
status_raw=q.block(order,'status');statuses=[];depth=0;start=None
for token,begin,end in q.tokens(status_raw):
 if token=='{':
  if depth==0:start=end
  depth+=1
 elif token=='}':
  depth-=1;assert depth>=0
  if depth==0:statuses.append(status_raw[start:begin])
 else:assert depth>0
assert depth==0
status_valid=lambda v:q.scalars(v).get('ship') in minerals and q.scalars(v).get('status')=='upgrade_waiting' and q.scalars(v).get('build_queue_item')==4294967295 and q.scalars(v).get('value')==.0666 and q.scalars(q.block(v,'upgrade_implementation'))=={'design':218105405}
flags=lambda state:{k:v for k,v,x in q.fields(q.block(state['country'],'flags'))}
f_before,f_after=flags(b),flags(a)
checks={
 'prior12_PASS_actual0_original_paid_zone_SAV':len(pre['checks'])==12 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(run/'priority_terravore_engineering_zone_order_guard.py')=='b8a87911c9c75eff0bdc2f04e132e9914124c6102922d1e025260e33bdf2d95b' and pre['after_sha256']==ba['save_sha256']=='249748727d83ae2f7cf590f10d0396a40a2f398459d3720a838b44db345aff20',
 'native_quote_UI_order_and_save_actual0_source_bound':sx['returncode']==ux['returncode']==qx['returncode']==0 and sx['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and ux['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and qx['helper_sha256']==h.sha256(run/'priority_native_hover_capture.py') and quote['image_sha256']==h.sha256(run/'terravore-mineral-refit-normal-quote-ui.jpg')=='53b3ac617d5670e37322cb42e703c7cf02495d7fe8136641cff57ceeff6f0ec2',
 'same_paused_date_exact_SAV_and_dependency_SHA':ba['date']==aa['date']==obs['date']=='2280.11.03' and all(h.sha256(run/(s+'.sav'))==au['save_sha256'] for s,au in [(before,ba),(after,aa)]) and aa['save_sha256']==obs['save_sha256']=='1e45b47a7bbcc2b140bf5219ae14a16fb468a79386ec77b016178cbd995abf35' and all(h.sha256(Path(v['path']))==v['sha256'] for v in obs['dependency_bindings']),
 'all_audit_business_fields_resources_research_population_EEP_exact_held':all(ba[k]==aa[k] for k in ba if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']),
 'one_new_manual_design_only_two_legal_kinetic_weapons_changed':set(a['designs'])-set(b['designs'])=={'218105405'} and all(a['designs'].get(k)==v for k,v in b['designs'].items()) and omit(replacement,{'auto_gen'})==list(q.fields(new)) and any(k=='technology' and str(v).strip('"')=='tech_mass_drivers_3' for k,v,x in q.fields(q.block(b['country'],'tech_status'))),
 'country_only_design_collection_and_native_tutorial48_changed':omit(b['country'],{'flags','ship_design_collection'})==omit(a['country'],{'flags','ship_design_collection'}) and set(f_after)-set(f_before)=={'tutorial_cleared_early_48'} and all(f_after.get(k)==v for k,v in f_before.items()) and q.block(b['country'],'ship_design_collection').replace('184550902','218105405')==q.block(a['country'],'ship_design_collection'),
 'fleet_template_only_old_design_replaced_no_reinforcement':set(b['templates'])==set(a['templates']) and all(a['templates'][k]==v.replace('184550902','218105405') for k,v in b['templates'].items()),
 'original_seven_ship_ID_birth_health_only_upgrade_reference_changed':set(b['ships'])==set(a['ships']) and all(omit(v,{'ship_design_implementation'})==omit(a['ships'][k],{'ship_design_implementation'}) and q.scalars(q.block(v,'ship_design_implementation'))=={'design':184550902,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(a['ships'][k],'ship_design_implementation'))=={'design':184550902,'upgrade':218105405,'growth_stage':0} if int(k) in minerals else v==a['ships'][k] for k,v in b['ships'].items()),
 'unique_original_seven_status_waiting_at_base0_shipyard3':set(q.ids(q.block(a['fleets'][fid],'ships')))==minerals and len(statuses)==7 and {q.scalars(v)['ship'] for v in statuses}==minerals and all(status_valid(v) for v in statuses) and q.scalars(q.block(order,'orbitable'))=={'starbase':0} and q.scalars(order)['queue']==3 and q.scalars(order)['self_upgrading']=='no',
 'only_selected_fleet_legal_return_order_no_other_fleet_changes':set(a['fleets'])==set(b['fleets']) and all(v==a['fleets'][k] for k,v in b['fleets'].items() if k!=fid) and omit(b['fleets'][fid],{'movement_manager','current_order','order_id'})==omit(a['fleets'][fid],{'movement_manager','current_order','order_id'}) and q.scalars(q.block(q.block(a['fleets'][fid],'movement_manager'),'coordinate'))['origin']==0 and q.scalars(q.block(q.block(a['fleets'][fid],'movement_manager'),'path'))['date']=='2280.11.13',
 'construction_zones_buildings_and_all_army_raw_held_no_early_birth':all(br[k]==ar[k] for k in ['construction','zones','buildings','army']),
 'messages_held_pending_empty':b['messages']==a['messages'] and not b['pending'] and not a['pending'],
 'production41_CN_error_and_readonly_module_exact_bound':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(run/'priority_terravore_native_state.py')==h.sha256(Path(__file__).with_name('priority_terravore_native_state.py')) and obs['new_error_bytes']==0 and obs['error_prefix_held'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(after+'-mineral-refit-order-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NORMAL_NATIVE_ZERO_COST_SEVEN_MINERAL_REFIT_ORDER' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'old_design_raw':old,'new_design_raw':new,'original_order_raw':order,'ships_before':{k:v for k,v in b['ships'].items() if int(k) in minerals},'ships_after':{k:v for k,v in a['ships'].items() if int(k) in minerals},'state_module_sha256':h.sha256(run/'priority_terravore_native_state.py'),'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':1 if passed else 0,'scope':'Native zero cost refit order only. Only next single day observation authorized, not an upgrade completion, devour settlement, Queen or full route acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
