"""Independent native month population/report/blocked-slot facts; retains notice-month FAIL."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'))
old=json.loads((run/(after+'-second-notice-month-proof.json')).read_text('utf-8'))
settle=json.loads((run/(before+'-second-settlement-proof.json')).read_text('utf-8'))
july1=json.loads((run/'terravore-second-month48-day1.audit.json').read_text('utf-8'))
with zipfile.ZipFile(run/(after+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
g=q.block(q.block(q.block(t,'colony'),'0'),'last_month_growth_data');growth=q.scalars(q.block(g,'growth_and_size'))
ds=list(q.fields(q.block(g,'current_month_growth_details')))
assert len(ds)%2==0 and all(ds[i][0]=='key' and ds[i+1][0]=='value' for i in range(0,len(ds),2))
cats={q.unquote(ds[i][1]):q.unquote(ds[i+1][1]) for i in range(0,len(ds),2)}
src=h.GAME_EXE.parent/'common/deposits/01_blocker_deposits.txt'
mod=q.scalars(q.block(q.block(src.read_text('utf-8-sig'),'d_failing_infrastructure'),'planet_modifier'))
blocks=[(i,a['deposits'][str(i)]) for i in a['planets']['7']['deposits'] if a['deposits'][str(i)]['type']=='d_failing_infrastructure']
districts=sum(a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts'])
free=a['planets']['7']['planet_size']+a['planets']['7']['variables']['eep_capacity_value']+len(blocks)*mod['planet_max_districts_add']-districts
birth=cats['GROWTH_CAT_GROWTH'];returned=settle['actual_return']
checks={
 'bound_original_only_two_FAIL_other23_valid':old['status']=='FAIL' and len(old['checks'])==25 and [k for k,v in old['checks'].items() if not v]==['core_only_correct_report_display_change','native_growth_only_no_additional_manufacture'] and old['before_sha256']==b['save_sha256'] and old['after_sha256']==a['save_sha256'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'bound_original_second_settlement35_PASS':settle['status']=='PASS_SECOND_NATIVE_TERRAVORE_SETTLEMENT_COMPONENT' and len(settle['checks'])==35 and all(settle['checks'].values()) and settle['after_sha256']==b['save_sha256'] and settle['before_sha256']==july1['save_sha256']==h.sha256(run/'terravore-second-month48-day1.sav'),
 'native_independent_birth_category6_other478_promotion0':cats=={'GROWTH_CAT_GROWTH':6,'GROWTH_CAT_OTHER':july1['colonies']['24']['actual_pop_sum'],'GROWTH_CAT_PROMOTION':0},
 'month_start_pre_return_and_total_growth_exact':growth['month_start_size']==july1['colonies']['0']['actual_pop_sum'] and growth['growth']==returned+birth and b['colonies']['0']['actual_pop_sum']==growth['month_start_size']+returned and a['colonies']['0']['actual_pop_sum']==growth['month_start_size']+growth['growth']==b['colonies']['0']['actual_pop_sum']+birth,
 'all_real_population_founder_only_on_mother':sum(g['size'] for g in a['pop_groups'].values())==a['colonies']['0']['actual_pop_sum'] and all(g['planet']==0 and g['key']['species']==3321888769 for g in a['pop_groups'].values() if g['size']>0),
 'original_failing_infrastructure_two_and_modifier_minus1':len(blocks)==2 and mod['planet_max_districts_add']==-1,
 'all_original_mother_deposits_raw_held':b['planets']['7']['deposits']==a['planets']['7']['deposits'] and all(b['deposits'][str(i)]==a['deposits'][str(i)] for i in b['planets']['7']['deposits']),
 'actual_free8_from29_less2_blocked_less19_built':districts==19 and free==8 and a['planets']['7']['planet_size']+a['planets']['7']['variables']['eep_capacity_value']==29,
 'core_exact_prebirth_population_snapshot_and_correct_free8':a['planets']['7']['variables']=={**b['planets']['7']['variables'],'eep_actual_pop':b['colonies']['0']['actual_pop_sum'],'eep_free_districts':free},
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_SECOND_TERRAVORE_NOTICE_GROWTH_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_month_growth':growth,'native_growth_categories':cats,'prior_verified_return':returned,'actual_birth':birth,'actual_free_districts':free,'blocker_source_sha256':h.sha256(src),'scope':'Only exact native growth/report snapshot and blocked-slot reconciliation plus original23 valid checks. Original25-check FAIL retained; notification acknowledgement and fresh audience snapshot pending.'}
out=run/(after+'-second-notice-growth-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original notice growth supplement FAIL retained'
