"""Review each 30-day post-conversion window before any native calendar input."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
before,end,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
s=read_state(run,before);a=s['audit'];c=a['countries']['0'];p=load(prior);x=load(execution+'-execution.json')
y,m,d=map(int,a['date'].split('.'));ny,nm=(y+1,1) if m==12 else (y,m+1)
expected_end=f'{ny:04}.{nm:02}.01'
ids=q.ids(q.block(s['queues']['0'],'items'));head=q.scalars(s['items']['1191182345'])
raw=c['research_queues']['society_queue'];ts=list(q.tokens(raw));project=q.scalars(raw[ts[0][2]:ts[-1][1]])
income=sum((D(str(v.get('society_research',0))) for v in c['budget_categories']['current_month']['income'].values()),D(0))
delay=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(s['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
orbitals=q.scalars(q.block(q.block(q.block(s['roots']['planets'],'planet'),'1732'),'planet_orbitals'))
support={}
for fid,index in [('917',1),('50332250',2)]:
    fleet=s['fleets'][fid];mm=q.block(fleet,'movement_manager')
    support[fid]=not q.block(fleet,'current_order') and q.scalars(q.block(mm,'coordinate'))['origin']==164 and q.scalars(q.block(mm,'orbit'))=={'index':index} and q.scalars(q.block(q.block(mm,'orbit'),'orbitable'))=={'planet':1732} and orbitals.get(str(index))==int(fid)
checks={
 'prior_PASS_actual0_source_originalSAV':p['status'].startswith('PASS') and p['checks'] and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and p['after_sha256']==a['save_sha256']==h.sha256(run/(before+'.sav')),
 'one_next_native30day_month_ends_no_later_than_Oct1':d==1 and end==expected_end and '2287.02.01'<=a['date']<end<='2287.10.01' and p['boundaries']==['project3_normal_months_and_next_paid_hive_review'],
 'four_paid_hives_front_under480_and_project3_safe_one_tick':ids==[1191182345,117440553,1476395019,117440546] and head['progress']+42<480 and all(q.scalars(q.block(s['items'][str(i)],'resources'))=={'minerals':400} for i in ids) and project['special_project']==9 and D(str(project['progress']))+income*D('2.35')<12000 and not list(q.tokens(c['research_queues']['engineering_queue'])),
 'two_society_zones_six_old_labs_original_jobs_both_support_orbits':a['districts']['1']['zones']==[0,67108970,119] and all(q.scalars(q.block(s['roots']['zones'],str(z)))=={'type':'zone_research_society'} for z in [67108970,119]) and q.ids(q.block(q.block(s['roots']['zones'],'67108970'),'buildings'))==[16777251,83886120,16777323] and q.ids(q.block(q.block(s['roots']['zones'],'119'),'buildings'))==[33554447,50331690,16777354] and [a['pop_jobs'][i]['workforce'] for i in ['23','24','25']]==[360,2040,360] and all(support.values()),
 'no_pending_combat_or_known_delayed_event_before_next_month':not s['pending'] and not delay and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in s['fleets'].values()) and not q.ids(q.block(s['queues'].get('3',''),'items')),
 'CN41_live_error_same':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());stage=before+'-post-second-society-month-review';out=run/(stage+'.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['save_sha256'],'after_sha256':a['save_sha256'],'start_date':a['date'],'end_date':end,'days':30,'maximum_days':30,'allowed_boundaries':p['boundaries'],'execution_stage':stage,'scope':'Only one next normal month with paid hive under480 and project3 under12000.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'start':a['date'],'end':end,'project3':project['progress'],'hive':head['progress']}),flush=True);assert passed
