"""Exact same-day native six paid hive orders, including two disabled no-ops."""
import json,logging,sys
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-native-white-peace-acknowledged';after='terravore-hive8-paid-order'
b,a=[read_state(run,s) for s in [before,after]];bc,ac=[s['audit']['countries']['0'] for s in [b,a]]
ids=[268435492,251658284,1191182345,117440553,1476395019,117440546];old=1627389955
pre=load(before+'-native-peace-review-v2-proof.json');px=load(before+'-review-v2-execution.json')
clicks=[load('terravore-hive8-paid-order-click-'+str(i)+'-execution.json') for i in range(1,9)]
sources=[]
for rel in ['common/deposits/01_blocker_deposits.txt','common/districts/00_urban_districts.txt']:
 p=h.GAME_EXE.parent/rel;dest=run/('terravore-six-hives-native-source-'+p.name)
 if dest.exists():assert dest.read_bytes()==p.read_bytes()
 else:dest.write_bytes(p.read_bytes())
 sources.append({'path':str(p),'preserved':dest.name,'sha256':h.sha256(p)})
blockers=Path(sources[0]['path']).read_text('utf-8-sig')
checks={
 'prior9PASS_actual0_source_SHA':len(pre['checks'])==9 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(run/'priority_terravore_native_white_peace_review_v2.py'),
 'same_day_original_save_SHA_actual0':b['audit']['date']==a['audit']['date']=='2281.04.01' and pre['after_sha256']==h.sha256(run/(before+'.sav'))==b['audit']['save_sha256'] and a['audit']['save_sha256']==h.sha256(run/(after+'.sav'))=='9a547b65efc28afd3063a1468c38e6642205ec705cf4a505cb7ce9ce7c3f4b2b' and load(after+'-save-execution.json')['returncode']==0,
 'eight_normal_click_receipts_actual0_bound_sources':all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in clicks),
 'queue_original_engineer_first_then_exact_six_paid_hives':q.ids(q.block(b['queues']['0'],'items'))==[old] and q.ids(q.block(a['queues']['0'],'items'))==[old]+ids and b['items'][str(old)]==a['items'][str(old)] and set(a['items'])-set(b['items'])==set(map(str,ids)) and all(q.scalars(a['items'][str(i)])=={'queue':0,'paying_country':0,'progress':0,'progress_needed':480} and q.scalars(q.block(a['items'][str(i)],'resources'))=={'minerals':400} and q.scalars(q.block(a['items'][str(i)],'buildable_district'))=={'district':'district_hive','planet':0} for i in ids),
 'exact2400_minerals_only_all_research_and_EEP_held':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==2400 and all(bc[k]==ac[k] for k in bc if k not in ['effective_stockpile','stockpile','modules']) and {k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'} and omit(b['country'],{'modules'})==omit(a['country'],{'modules'}),
 'all_planets_pops_jobs_districts_situations_deposits_held':all(b['audit'][k]==a['audit'][k] for k in ['planets','pop_groups','pop_jobs','districts','situations','deposits']) and all(q.block(b['roots']['colony'],i)==q.block(a['roots']['colony'],i) for i in bc['owned_colonies'] if str(i)!='0') and omit(q.block(b['roots']['colony'],'0'),{'last_district_changed'})==omit(q.block(a['roots']['colony'],'0'),{'last_district_changed'}),
 'all61ships34fleets_armies_buildings_messages_pending_exact':len(a['ships'])==61 and len(a['fleets'])==34 and all(b[k]==a[k] for k in ['ships','fleets','messages','pending']) and all(b['roots'][k]==a['roots'][k] for k in ['army','zones','buildings','war','truce']),
 'gross35_built27_hive5_two_native_capacity_blockers':sum(a['audit']['districts'][str(i)]['level'] for i in a['audit']['colonies']['0']['districts'])==27 and a['audit']['districts']['1']['level']==5 and all(q.scalars(q.block(q.block(blockers,k),'planet_modifier'))['planet_max_districts_add']==-1 for k in ['d_failing_infrastructure','d_ruined_district']),
 'production_CN_version_tree_error_held':m['version']=='0.2.0' and m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(after+'-six-paid-hives-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_SIX_NATIVE_PAID_HIVES' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'queue':q.ids(q.block(a['queues']['0'],'items')),'paid_minerals':2400,'disabled_no_charge_clicks':[7,8],'sources':sources,'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Six paid construction orders only; no completed districts or route acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
