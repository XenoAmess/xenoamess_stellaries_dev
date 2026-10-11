"""Read-only normal research replacement cancellation and exact progress retention."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bt,at=bc['tech_status'],ac['tech_status']
bcs,acs=[{k:v for k,v,o in q.fields(rt['country']) if o} for rt in [br,ar]]
pre=json.loads((run/(before+'-rear-colonizer2-payment-v2-proof.json')).read_text('utf-8'))
click=json.loads((run/'terravore-physics-bank-change-click.action.json').read_text('utf-8'))
pex=json.loads((run/(before+'-payment-guard-v2-execution.json')).read_text('utf-8'))
clickex=json.loads((run/'terravore-physics-bank-change-click-execution.json').read_text('utf-8'))
checks={
 'bound_actual17_paid_PASS_source_exit0':pre['status'].startswith('PASS_') and len(pre['checks'])==17 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256']=='97b5e5820a11a8c97f2b799c21354af1836fd56ef8ceee83d9b7f82f58eb66b1' and pex['returncode']==0 and pex['helper_sha256']==h.sha256(run/'priority_terravore_rear_colonizer2_payment_guard_v2.py')=='57f829691234a39a07844435be01424365362d0b41ce1598d29ff807bfcb9ae0',
 'same_date_original_SHA_pair':b['date']==a['date']=='2271.12.12' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'normal_change_button_actual_click':click['action']=='left-click' and click['client_point']==[334,247] and clickex['returncode']==0 and clickex['helper_sha256']=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and click['foreground_after']==click['expected_hwnd'],
 'old_physics235_08678_queue_removed':bool(q.block(bt,'physics_queue')) and 'progress=235.08678' in q.block(bt,'physics_queue') and 'technology="tech_cold_fusion_power"' in q.block(bt,'physics_queue') and not any(k=='physics_queue' for k,v,o in q.fields(at)),
 'current_physics235_08678_and_all_prior_progress_retained':q.scalars(q.block(bt,'stored_techpoints_for_tech'))=={'tech_colonization_2':607.25288} and q.scalars(q.block(at,'stored_techpoints_for_tech'))=={'tech_colonization_2':607.25288,'tech_cold_fusion_power':235.08678},
 'native_physics_auto_yes_to_no':q.scalars(bt)['auto_researching_physics']=='yes' and q.scalars(at)['auto_researching_physics']=='no',
 'other_tech_fields_raw_held':omit(bt,['physics_queue','stored_techpoints_for_tech','auto_researching_physics'])==omit(at,['physics_queue','stored_techpoints_for_tech','auto_researching_physics']),
 'other_country0_fields_raw_held':omit(bcs['0'],['tech_status'])==omit(acs['0'],['tech_status']),
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k!='country']==[(k,v,o) for k,v,o in af if k!='country'],
 'true_three_banks_held':q.research_stocks(bt)==q.research_stocks(at)=={'physics_research':0,'society_research':7258.44076,'engineering_research':0},
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['effective_stockpile','completed_technologies','variables','flags','traditions','ascension_perks','budget_categories','owned_colonies','government']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TERRAVORE_RESEARCH_CANCELLATION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'specialized_progress_after':ac['research_progress_by_tech'],'scope':'One normal physics replacement button removes old queue, preserves235.08678 and disables only physics automation. Engineering continues, society bank7258.44076 retained. No new selection, project, free technology or research completion claim.'}
out=run/(after+'-research-cancel-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original cancellation FAIL retained; no calendar'
