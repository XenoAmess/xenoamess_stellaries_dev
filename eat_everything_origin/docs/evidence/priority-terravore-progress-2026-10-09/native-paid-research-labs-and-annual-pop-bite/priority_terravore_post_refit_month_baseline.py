"""Read-only bounded first resource month after the seven original mineral refits."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
stage='terravore-mineral-refit-day-22801114';s=read_state(run,stage);a=s['audit'];c=a['countries']['0']
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
p=load(stage+'-mineral-refit-completion-proof.json');x=load(stage+'-completion-guard-execution.json')
minerals={16777746,50333149,50333147,33554923,1960,1961,1962}
pops={}
for v in a['pop_groups'].values():
 key=str(v['planet'])+':'+str(v['key']['species']);pops[key]=pops.get(key,0)+v['size']
checks={
 'independent_completion10_PASS_actual0_bound_original_source':len(p['checks'])==10 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(run/'priority_terravore_mineral_refit_completion_guard.py')=='2254d14ed35d0adefe5e68bc3fe86bc631aba1cc73674310573851d303ea40dd',
 'current_original_paused_stage_date_SHA':a['date']=='2280.11.14' and a['save_sha256']==p['after_sha256']==h.sha256(run/(stage+'.sav'))=='c69c105ac4faabfc7fec602cf45ae25f2b3b30d906faf489c9b7b273ced4683d',
 'exact_original_seven_real_new_designs_mother0_orbit_no_orders':set(q.ids(q.block(s['fleets']['50332250'],'ships')))==minerals and all(q.scalars(q.block(s['ships'][str(i)],'ship_design_implementation'))=={'design':218105405,'upgrade':4294967295,'growth_stage':0} for i in minerals) and not q.block(s['fleets']['50332250'],'current_order') and q.scalars(q.block(q.block(q.block(s['fleets']['50332250'],'movement_manager'),'orbit'),'orbitable'))=={'starbase':0},
 'one_paid_engineering_zone_order15p4_of360_no_ship_or_army_orders':q.ids(q.block(s['queues']['0'],'items'))==[1627389955] and q.scalars(s['items']['1627389955'])['progress']==15.4 and q.scalars(s['items']['1627389955'])['progress_needed']==360 and q.scalars(q.block(s['items']['1627389955'],'resources'))=={'minerals':800} and not q.ids(q.block(s['queues']['1'],'items')) and not q.ids(q.block(s['queues']['3'],'items')),
 'mother_capacity35_paid27_exact_species_no_foreign_mother':a['planets']['7']['planet_size']+a['planets']['7']['variables']['eep_capacity_value']==35 and sum(a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts'])==27 and pops=={'0:73':11975,'30:73':100,'30:61':27,'30:2':366},
 'fifth_source_only_Q14_34months_progress0_no_credit':set(a['situations'])=={'167772163'} and a['situations']['167772163']['progress']==0 and a['situations']['167772163']['target']['id']==1578 and a['planets']['1578']['variables']['eep_months']==34 and all(c['variables'][k]==v for k,v in {'eep_c':62,'eep_d':17,'eep_worlds':4,'eep_stage':2,'eep_fleet_stage':2}.items()) and c['effective_stockpile']['menace']==2135,
 'no_pending_combat_and_next_native_delay_beyond17days':not s['pending'] and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in s['fleets'].values()) and all(q.scalars(v)['days']>17 for k,v,obj in q.fields(q.block(q.block(s['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event'),
 'production41_CN_and_original_unfiltered_error_module_held':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(stage+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850' and p['state_module_sha256']==h.sha256(run/'priority_terravore_native_state.py')==h.sha256(Path(__file__).with_name('priority_terravore_native_state.py')),
}
passed=all(v is True for v in checks.values());out=run/'terravore-post-refit-first-month-baseline-proof.json';assert not out.exists()
h.write_json(out,{'status':'PASS_POST_REFIT_FIRST_RESOURCE_MONTH_BASELINE' if passed else 'FAIL','checks':checks,'after_sha256':a['save_sha256'],'date':a['date'],'end_date':'2280.12.01','boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':17 if passed else 0,'state_module_sha256':h.sha256(run/'priority_terravore_native_state.py'),'scope':'Only17 native days to first resource month. Requires independent monthly population, purge, cash, research, maintenance, construction and message review afterward. Not complete30day maintenance or route acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
