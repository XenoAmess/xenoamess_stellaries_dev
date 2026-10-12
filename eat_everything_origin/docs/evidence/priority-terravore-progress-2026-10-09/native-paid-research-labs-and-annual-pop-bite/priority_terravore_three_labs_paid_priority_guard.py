"""Exact native960 mineral payment for three real labs and normal priority order."""
import json,logging,sys
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-engineer-completed-22810721';after='terravore-three-labs-prioritized';b,a=[read_state(run,s) for s in [before,after]];bc,ac=[v['audit']['countries']['0'] for v in [b,a]]
pre=load(before+'-paid-engineer-completion-v2-proof.json');px=load(before+'-completion-guard-v2-execution.json');labs=[67108899,1644167171,184549419];hives=[268435492,251658284,1191182345,117440553,1476395019,117440546];queue=q.ids(q.block(a['queues']['0'],'items'))
stages=['terravore-paid-research-lab-cost-button1','terravore-paid-research-lab-cost-button2','terravore-paid-materials-workshop-cost-button','terravore-first-lab-physical-priority-to-front','terravore-last-lab-physical-priority-to-front','terravore-second-lab-physical-priority-to-front',after+'-save'];xs=[load(s+'-execution.json') for s in stages]
checks={
 'prior14PASS_actual0_original_source':len(pre['checks'])==14 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(run/'priority_terravore_engineer_completed_guard_v2.py')=='7fddfeb794333f12b0d94d05250dd1e08ddedc1645b2634724b2973a1a19d174',
 'same_paused_date_original_SHA_pair':b['audit']['date']==a['audit']['date']=='2281.07.21' and pre['after_sha256']==b['audit']['save_sha256']==h.sha256(run/(before+'.sav')) and a['audit']['save_sha256']==h.sha256(run/(after+'.sav')),
 'three_paid_and_physical_priority_and_save_actual0_sources':all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs),
 'exact_three_lab_building_items320each360work_zero':set(a['items'])-set(b['items'])==set(map(str,labs)) and all(q.scalars(a['items'][str(i)])=={'queue':0,'paying_country':0,'progress':0,'progress_needed':360} and q.scalars(q.block(a['items'][str(i)],'resources'))=={'minerals':320} and q.scalars(q.block(a['items'][str(i)],'buildable_planet_building'))=={'building':'building_research_lab_1','planet':0,'zone':16777330} for i in labs),
 'all_three_labs_first_six_hives_order_and_original_items_held':len(queue)==9 and set(queue[:3])==set(labs) and queue[3:]==hives and all(a['items'][i]==v for i,v in b['items'].items()),
 'exact960_minerals_all_other_cash_and_research_held':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==960 and all(v==ac['effective_stockpile'][k] for k,v in bc['effective_stockpile'].items() if k!='minerals') and all(bc[k]==ac[k] for k in bc if k not in ['effective_stockpile','stockpile','modules']) and omit(b['country'],{'modules'})==omit(a['country'],{'modules'}),
 'all_planets_pops_jobs_districts_EEP_exact_no_early_buildings':all(b['audit'][k]==a['audit'][k] for k in ['planets','pop_groups','pop_jobs','situations','districts','deposits']) and b['roots']['zones']==a['roots']['zones'] and b['roots']['buildings']==a['roots']['buildings'],
 'only_mother_last_building_changed_bookkeeping':omit(q.block(b['roots']['colony'],'0'),{'last_building_changed'})==omit(q.block(a['roots']['colony'],'0'),{'last_building_changed'}) and q.block(b['roots']['colony'],'30')==q.block(a['roots']['colony'],'30'),
 'all61ships34fleets_armies_messages_pending_war_exact':len(a['ships'])==61 and len(a['fleets'])==34 and all(b[k]==a[k] for k in ['ships','fleets','messages','pending']) and all(b['roots'][k]==a['roots'][k] for k in ['army','war','truce']),
 'original_failed_wrapper_collision_retained_without_false_actual0':load('terravore-first-lab-priority-wrapper-collision-observation.json')['wrapper_returncode']==1 and h.sha256(run/'priority_native_shift_click_terravore_research_v1.py')=='4b46175851a60b20e103cd1296a4c7b539bd1ae712fb0446d8037e0a70ca1c61',
 'same_CN_production41_error_held':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(after+'-three-paid-labs-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_THREE_PAID_LABS_NATIVE_PRIORITY' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'queue':queue,'paid_minerals':960,'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':10 if passed else 0,'scope':'Three actual lab orders, no materials workshop. All construction remains paid and unbuilt; next10 native days only.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'queue':queue}),flush=True);assert passed
