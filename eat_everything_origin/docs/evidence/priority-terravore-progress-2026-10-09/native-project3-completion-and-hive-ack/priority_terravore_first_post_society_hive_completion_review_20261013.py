"""Preflight the exact 29-day first prepaid hive completion after society conversion."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-post-second-society-month-22871201';s=read_state(run,before);a=s['audit'];c=a['countries']['0']
p=load(before+'-post-second-society-month-v3-proof.json');x=load(before+'-post-second-society-month-guard-v3-execution.json')
ids=q.ids(q.block(s['queues']['0'],'items'));head=q.scalars(s['items']['1191182345'])
raw=c['research_queues']['society_queue'];ts=list(q.tokens(raw));project=q.scalars(raw[ts[0][2]:ts[-1][1]])
inc=sum((D(str(v.get('society_research',0))) for v in c['budget_categories']['current_month']['income'].values()),D(0))
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(s['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
checks={
 'prior18PASS_actual0_source_original_SAV':p['status']=='PASS_NATIVE_SECOND_SOCIETY_NORMAL_MONTH' and len(p['checks'])==18 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='89bbc8a0c27a36c912fea5b71391a1fc197d2dcdd8babf2b54af58af02109e41' and p['after_sha256']==a['save_sha256']==h.sha256(run/(before+'.sav')),
 'exact_first_completion_day29_only_400minerals_paid':a['date']=='2287.12.01' and ids==[1191182345,117440553,1476395019,117440546] and head['progress']==439.6 and head['progress_needed']==480 and head['progress']+28*1.4<480<=head['progress']+29*1.4 and all(q.scalars(q.block(s['items'][str(i)],'resources'))=={'minerals':400} for i in ids) and all(q.scalars(s['items'][str(i)])['progress']==0 for i in ids[1:]),
 'district7_built29_two_society_zones_jobs_before':a['districts']['1']=={'type':'district_hive','level':7,'zones':[0,67108970,119]} and sum(a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts'])==29 and [a['pop_jobs'][i]['workforce'] for i in ['23','24','25']]==[360,2040,360],
 'one_project3_tick_under12000_no_pending_delays_combat':project['special_project']==9 and D(str(project['progress']))+inc*D('2.35')<12000 and not s['pending'] and not delays and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in s['fleets'].values()) and not q.ids(q.block(s['queues'].get('3',''),'items')),
 'CN41_same_production_and_live_error':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());stage=before+'-first-hive-completion-review';out=run/(stage+'.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['save_sha256'],'after_sha256':a['save_sha256'],'start_date':'2287.12.01','end_date':'2287.12.30','days':29,'maximum_days':29,'allowed_boundaries':p['boundaries'],'execution_stage':stage,'scope':'Only the first prepaid hive completion, before next month ledger.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'project3':project['progress'],'hive':head['progress']}),flush=True);assert passed
