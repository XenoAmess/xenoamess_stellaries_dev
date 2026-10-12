"""Read-only16 native days to the monthly receipt, without extra research tick."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-third-paid-lab-completed-22830915';a=read_state(run,before);p=load(before+'-third-paid-lab-completion-proof.json');x=load(before+'-third-paid-lab-completed-guard-execution.json');c=a['audit']['countries']['0'];front=str(q.ids(q.block(a['queues']['0'],'items'))[0])
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event'];trade=sum(v.get('trade',0) for v in c['budget_categories']['current_month']['income'].values())
checks={
 'prior16PASS_actual0_fixed_source_SAV':len(p['checks'])==16 and all(p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='905dc1deb1d989447424b81fedd901144e1235fb5db479dfe25e14120a608b6f' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'exact16day_notice_boundary_no_lab_or_research_completion':a['audit']['date']=='2283.09.15' and p['boundaries']==['queen_monthly_notice'] and 'eep_notice_pending' in c['flags'] and c['owned_colonies']==[0] and a['audit']['colonies']['0']['actual_pop_sum']==12701 and q.scalars(a['items'][front])['progress']+22.4<q.scalars(a['items'][front])['progress_needed'] and not a['pending'],
 'no_unreviewed_delayed_events_or_timed_projects_in16days':all(v['event']=='cstorms.1815' and v['days']>16 or v['event']=='pirate.6' and trade<300 for v in delays) and all(q.scalars(v).get('days_left',100000)>16 for k,v,obj in q.fields(q.block(a['country'],'events')) if obj and k=='special_project'),
 'CN_production41_error627_original_three_labs_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and q.ids(q.block(q.block(a['roots']['zones'],'16777330'),'buildings'))==[33554447,50331690,16777354],
}
passed=all(v is True for v in checks.values());out=run/(before+'-fifth-notice-month-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2283.09.15','end_date':'2283.10.01','days':16,'maximum_days':16,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-fifth-notice-month-review','scope':'Only first monthly receipt after fifth settlement; no additional research tick or construction completion.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
