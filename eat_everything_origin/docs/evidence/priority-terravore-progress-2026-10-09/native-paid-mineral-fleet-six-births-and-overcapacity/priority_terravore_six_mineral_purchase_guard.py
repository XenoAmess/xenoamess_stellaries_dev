"""Six normal paid mineral ship orders, exact same-day complete world checks."""
import json,logging,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-original-corvette-return-22800104';after='terravore-mineral-six-paid'
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(st+'.audit.json'),fs,{k:v for k,v,x in fs if x}
b,bf,br=read(before);a,af,ar=read(after);bc,ac=[au['countries']['0'] for au in [b,a]]
omit=lambda raw,keys:[(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
cs=[q.block(rr['country'],'0') for rr in [br,ar]];mods=[q.block(c,'modules') for c in cs];econ=[q.block(c,'standard_economy_module') for c in mods];res=[q.scalars(q.block(c,'resources')) for c in econ]
qs=[q.block(q.block(rr['construction'],'queue_mgr'),'queues') for rr in [br,ar]];items=[{k:(v,x) for k,v,x in q.fields(q.block(q.block(rr['construction'],'item_mgr'),'items'))} for rr in [br,ar]]
ids=q.ids(q.block(q.block(qs[1],'3'),'items'));orders={str(i):items[1][str(i)][0] for i in ids};removed=items[0].keys()-items[1].keys();added=items[1].keys()-items[0].keys()
pre=load(before+'-campaign-v6-proof.json');px=load(before+'-campaign-guard-v6-execution.json');iv=load(after+'-native-purchase-investigation.json')
checks={
 'prior19_PASS_actual0_source_SAV':len(pre['checks'])==19 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==b['save_sha256'],
 'same_day_original_SAVs_and_bound_independent_INV':a['date']==b['date']=='2280.01.04' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]) and h.sha256(run/(after+'-native-purchase-investigation.json'))=='dc86d807e0ce8a9b540c56059bc7c19c57d63b26f7e4bd54ed4661ab0c48e5a2' and iv['after_sha256']==a['save_sha256'],
 'exact1350M_paid_zero_alloys_other_true_stocks_held':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==1350 and {k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'} and bc['research_stockpile']==ac['research_stockpile'],
 'economy_only1350M_and_true_research_mirror_rebuild':D(str(res[0]['minerals']))-D(str(res[1]['minerals']))==1350 and {k:v for k,v in res[0].items() if k not in {'minerals',*q.RESEARCH_RESOURCES}}=={k:v for k,v in res[1].items() if k not in {'minerals',*q.RESEARCH_RESOURCES}} and all(res[1].get(k,0)==ac['research_stockpile'][k] for k in q.RESEARCH_RESOURCES) and omit(econ[0],{'resources'})==omit(econ[1],{'resources'}),
 'country0_other_raw_modules_and_other_countries_held':omit(cs[0],{'modules'})==omit(cs[1],{'modules'}) and omit(mods[0],{'standard_economy_module'})==omit(mods[1],{'standard_economy_module'}) and omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'queue3_six_unique_orders_base0_two_parallel':len(ids)==len(set(ids))==6 and not q.block(q.block(qs[0],'3'),'items') and omit(q.block(qs[0],'3'),{'items'})==omit(q.block(qs[1],'3'),{'items'}) and q.scalars(q.block(qs[1],'3'))=={'owner':0,'simultaneous':2,'type':'ships'} and q.scalars(q.block(q.block(qs[1],'3'),'location'))=={'type':0,'id':0} and omit(qs[0],{'3'})==omit(qs[1],{'3'}),
 'six_native_orders225M_work30_original_design184550902':all(q.scalars(v)=={'queue':3,'paying_country':0,'progress':0,'progress_needed':30} and q.scalars(q.block(v,'resources'))=={'minerals':225} and q.scalars(q.block(q.block(v,'buildable_ship'),'ship_design_implementation'))=={'design':184550902,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(q.block(v,'buildable_ship'),'orbitable'))=={'starbase':0} for v in orders.values()),
 'only_six_retired_none_handles_next_generation_reused':added==set(orders) and len(removed)==6 and all(items[0][i]==('none',False) and str(int(i)+16777216) in added for i in removed) and all(items[0][i]==items[1][i] for i in items[0].keys()&items[1].keys()),
 'all_other_world_raw_held_no_birth_no_order_or_structure_change':[(k,v,x) for k,v,x in bf if k not in {'country','construction'}]==[(k,v,x) for k,v,x in af if k not in {'country','construction'}],
 'all_audit_business_except_exact_economy_held':all(b[k]==a[k] for k in b if k not in {'save','save_sha256','gamestate_sha256','gamestate_bytes','countries'}) and all(b['countries'][i]==a['countries'][i] for i in b['countries'] if i!='0') and all(bc[k]==ac[k] for k in bc if k not in {'stockpile','effective_stockpile','modules'}),
 'six_normal_clicks_and_native_save_actual0':all(load('terravore-mineral-six-order-click'+str(i)+'-execution.json')['returncode']==0 and load('terravore-mineral-six-order-click'+str(i)+'.action.json')['client_point']==[565,404] for i in range(1,7)) and load(after+'-native-save-execution.json')['returncode']==0,
 'CN_020_production_and_error_exact_held_no_pending':m['version']=='0.2.0' and m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes() and not any(k=='player_event' and x and q.scalars(v).get('country')==0 for k,v,x in af),
}
passed=all(v is True for v in checks.values());out=run/(after+'-purchase-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_SIX_PAID_MINERAL_SHIP_ORDERS' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'order_ids':ids,'orders_original':orders,'paid_minerals':1350,'paid_alloys':0,'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':27 if passed else 0,'scope':'Paid orders only. Next interval may contain original paid births; they require independent checks and are not yet accepted.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
