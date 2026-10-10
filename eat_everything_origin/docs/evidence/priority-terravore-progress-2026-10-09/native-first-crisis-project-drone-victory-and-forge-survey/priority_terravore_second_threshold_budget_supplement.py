"""Independent exact current-month reconciliation, retaining original threshold FAIL."""
import json,logging,shutil,sys
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'))
bc,ac=b['countries']['0'],a['countries']['0']
old=json.loads((run/(after+'-second-threshold-proof.json')).read_text('utf-8'))
obs=json.loads((run/(after+'-second-boundary-observation.json')).read_text('utf-8'))
src=h.GAME_EXE.parent/'common/strategic_resources/00_strategic_resources.txt'
spec=q.scalars(q.block(src.read_text('utf-8-sig'),'influence'))
net={};residual={}
for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']:
 net[k]=sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))
 expected=D(str(bc['effective_stockpile'].get(k,0)))+net[k]+(D(100) if k=='alloys' else D(0))
 if k=='influence':expected=min(D(1000),expected)
 residual[k]=D(str(ac['effective_stockpile'].get(k,0)))-expected
banks=lambda c:[D(t) for t,_,_ in q.tokens(q.block(c['tech_status'],'stored_techpoints'))]
msgs=[q.scalars(v) for v in obs['after_native_bite_messages']]
checks={
 'original_unique_budget_FAIL_and_other38_bound':old['status']=='FAIL' and len(old['checks'])==39 and [k for k,v in old['checks'].items() if not v]==['eight_monthly_budget_residuals_zero_with_native100'] and old['before_sha256']==b['save_sha256'] and old['after_sha256']==a['save_sha256'],
 'original_actual_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_June30_July1_boundary_bound':b['date']=='2233.06.30' and a['date']=='2233.07.01' and obs['status']=='OBSERVED_NATIVE_TERRAVORE_BOUNDARY' and all(obs['checks'].values()) and obs['before_sha256']==b['save_sha256'] and obs['after_sha256']==a['save_sha256'],
 'independent_last_month_equals_prior_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'native_fixed_influence_cap1000':spec.get('max')==1000 and spec.get('fixed_max_amount')=='yes',
 'all_eight_current_month_exact_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'three_true_research_banks_held_zero':banks(bc)==banks(ac)==[D(0),D(0),D(0)],
 'exact_one_native_alloy100_award_message':not obs['before_native_bite_messages'] and len(msgs)==1 and all(msgs[0].get(k)==v for k,v in {'date':'2233.07.01','receiver':0,'target_planet':124,'localization':'MESSAGE_TERRAVORE_CONSUME_WORLD_ALLOYS_TEXT'}.items()),
 'unfiltered_error_bytes_held':(run/(after+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_NATIVE_TERRAVORE_SECOND_THRESHOLD_BUDGET_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'current_month_net':{k:str(v) for k,v in net.items()},'exact_budget_residuals':{k:str(v) for k,v in residual.items()},'original_wrong_last_month_residuals':old['annual_boundary_residuals'],'resource_source_sha256':h.sha256(src),'scope':'Only independent current-month accounting and bound original38 valid threshold checks. Original39-check FAIL retained; not settlement or full route acceptance.'}
out=run/(after+'-second-threshold-budget-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original threshold budget supplement FAIL retained'
