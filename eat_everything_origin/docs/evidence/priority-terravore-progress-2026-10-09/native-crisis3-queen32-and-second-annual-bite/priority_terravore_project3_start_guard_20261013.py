"""Same-day native society project9 start, exact research and owned-asset ledger."""
import json,logging,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-native-project3-enabled';after='terravore-native-project3-started';b,a=[read_state(run,s) for s in [before,after]]
p=load(before+'-project3-enabled-v2-proof.json');px=load(before+'-project3-enabled-guard-v2-execution.json');click=load('terravore-project3-start-click-execution.json');sx=load(after+'-save-execution.json')
projects=lambda s:{q.scalars(v)['id']:v for k,v,obj in q.fields(q.block(s['country'],'events')) if obj and k=='special_project'};bp,ap=projects(b),projects(a)
bt,at=[q.block(s['country'],'tech_status') for s in [b,a]]
raw=q.block(at,'society_queue');ts=list(q.tokens(raw));queue=q.scalars(raw[ts[0][2]:ts[-1][1]]) if ts else {}
checks={
 'prior12PASS0_source_SHA_and_actual_click_after_validation':len(p['checks'])==12 and all(v is True for v in p['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1]))=='6befe7e81ab86582ee297cc5cd061f0234432f13fa4b9f7d8377c85288b0deba' and click['started_at_utc']>px['finished_at_utc'] and p['after_sha256']==b['audit']['save_sha256'],
 'normal_click355365_save_actual0_sources_and_same_day_SAV_SHA':click['returncode']==sx['returncode']==0 and load('terravore-project3-start-click.action.json')['client_point']==[355,365] and all(x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in [click,sx]) and all(s['audit']['save_sha256']==h.sha256(run/(stage+'.sav')) for s,stage in [(b,before),(a,after)]) and b['audit']['date']==a['audit']['date']=='2282.10.07',
 'only_society_queue_project9_date_and_no_research_advance':not q.block(bt,'society_queue') and queue=={'special_project':9,'date':'2282.10.07'} and omit(bt,{'society_queue'})==omit(at,{'society_queue'}),
 'project9_only_status_in_progress_all_other_projects_held':bp.keys()==ap.keys() and all(v==ap[i] for i,v in bp.items() if i!=9) and omit(bp[9],{'status'})==omit(ap[9],{'status'}) and q.scalars(ap[9])==dict(q.scalars(bp[9]),status='in_progress') and omit(q.block(b['country'],'events'),{'special_project'})==omit(q.block(a['country'],'events'),{'special_project'}),
 'all_other_country_raw_including_EEP_native_crisis_and_designs_held':omit(b['country'],{'tech_status','events'})==omit(a['country'],{'tech_status','events'}),
 'all_cash_banks_EEP_population_jobs_worlds_business_held':all(b['audit'][k]==a['audit'][k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','situations','event_targets']) and all(b['audit']['countries']['0'][k]==a['audit']['countries']['0'][k] for k in ['effective_stockpile','research_stockpile','variables','flags','budget_categories']),
 'owned61ships34fleets_and_all_armies_paid_orders_held':all(b[k]==a[k] for k in ['ships','fleets','queues','items','designs']) and all(b['roots'][k]==a['roots'][k] for k in ['army','zones','buildings','districts','deposit','situations']),
 'no_new_pending_or_messages':not a['pending'] and b['messages']==a['messages'],
 'CN_production41_exact_error_bytes':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and reviewed_error_pair((run/(before+'-error-after.log')).read_bytes(),(run/(after+'-error-after.log')).read_bytes(),run) and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-project3-start-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_PROJECT3_STARTED_NOT_COMPLETED' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'boundaries':['native_project3_start_and_Queen32_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Native society special project9 start only. Research/cash/pop/owned assets held.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
