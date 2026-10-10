"""Exact native full-Psi reload cache changes; original strict24 FAIL retained."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name);readj=lambda p:json.loads(p.read_text('utf-8'))
before='terravore-native-stage3-ack';after='terravore-native-stage3-resumed';b=readj(run/(before+'.audit.json'));a=readj(run/(after+'.audit.json'));original=readj(run/(after+'-proof.json'));bc,ac=b['countries']['0'],a['countries']['0'];omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
income={('trade_policy','trade'):(88.45845,88.56342),('planet_jobs','unity'):(1.28136,1.37256),('planet_bureaucrats','unity'):(126.45,140.868),('planet_telepaths','unity'):(15.80625,17.6085),('planet_maintenance_drones','trade'):(40.96932,41.08104),('planet_physicists','physics_research'):(8.9775,9.3366),('planet_biologists','society_research'):(8.9775,9.3366),('planet_engineers','engineering_research'):(8.9775,9.3366),('country_ruler','influence'):(None,.5)}
expenses={('planet_resource_deficit','trade'):(.39087,.39762),('trade_policy','trade'):(88.45845,88.56342),('planet_bureaucrats','energy'):(57,59.28),('planet_bureaucrats','minerals'):(57,59.28),('planet_telepaths','energy'):(2.375,2.47),('planet_physicists','minerals'):(8.55,8.892),('planet_biologists','minerals'):(8.55,8.892),('planet_engineers','minerals'):(8.55,8.892),('planet_pops_traits','minerals'):(86.931,86.994)}
def flat(d):return {(k,x):v for k,values in d.items() for x,v in values.items()}
def exact_cells(kind,expected):
 x,y=[flat(c['budget_categories']['current_month'][kind]) for c in [bc,ac]]
 return {k:(x.get(k),y.get(k)) for k in set(x)|set(y) if x.get(k)!=y.get(k)}==expected
cur=ac['budget_categories']['current_month'];inc,exp,bal=[flat(cur[k]) for k in ['income','expenses','balance']]
balances_ok=all(abs(D(str(inc.get(k,0)))-D(str(exp.get(k,0)))-D(str(bal.get(k,0))))<=D('.00002') for k in set(inc)|set(exp)|set(bal))
bh,ah=[q.block(c['budget'],'income_high_water_mark') for c in [bc,ac]];hw=q.scalars(q.block(ah,'current'))
highwater_ok=all(abs(D(str(hw.get(k,0)))-sum((D(str(values.get(k,0))) for values in cur['income'].values()),D(0)))<=D('.00002') for k in set(hw)|{k for values in cur['income'].values() for k in values})
ca={'housing_usage':(9659,9666),'free_housing':(4141,4134),'amenities':(24071.6,24159.2),'free_amenities':(17543.4,17631)}
colonies_ok=set(b['colonies'])==set(a['colonies']) and all(({k:v for k,v in c.items() if k not in ca}=={k:v for k,v in a['colonies'][i].items() if k not in ca} and all((c[k],a['colonies'][i][k])==values for k,values in ca.items())) if i=='0' else (c.get('binary_flags') is None and a['colonies'][i].get('binary_flags')==24 and {k:v for k,v in c.items() if k!='binary_flags'}=={k:v for k,v in a['colonies'][i].items() if k!='binary_flags'} and c['actual_pop_sum']==a['colonies'][i]['actual_pop_sum']==0) if i in ['15','24'] else c==a['colonies'][i] for i,c in b['colonies'].items())
planets_ok=set(b['planets'])==set(a['planets']) and all(({k:v for k,v in p.items() if k!='carrier_binary_flags'}=={k:v for k,v in a['planets'][i].items() if k!='carrier_binary_flags'} and p['carrier_binary_flags']==1 and a['planets'][i]['carrier_binary_flags']==3) if i=='7' else p==a['planets'][i] for i,p in b['planets'].items())
attr=readj(run/(before+'-known-native-error-supplement.json'));control=Path(attr['control_snapshot']);cp=readj(control/'shroud2780-control-error-proof.json')
checks={
 'original24_exact_three_FAIL_exit1':original['status']=='FAIL' and len(original['checks'])==24 and {k for k,v in original['checks'].items() if not v}=={'budget_held','colonies_held','planets_held'} and readj(run/'shroud2780-production-resume-load-execution.json')['returncode']==1,
 'remaining21_original_checks_all_true':all(v is True for k,v in original['checks'].items() if k not in ['budget_held','colonies_held','planets_held']),
 'original_SHA_pair_date_alias':h.sha256(run/(before+'.sav'))==b['save_sha256']==original['before_sha256']==original['alias_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==original['after_sha256'] and b['date']==a['date']=='2254.11.02',
 'bound_ACK8_native_error_PASS_exit0':attr['status']=='PASS_NATIVE2780_ACK_KNOWN_NATIVE_ERROR_COMPONENT' and len(attr['checks'])==8 and all(attr['checks'].values()) and attr['after_sha256']==b['save_sha256'] and readj(run/(before+'-error-supplement-execution.json'))['returncode']==0,
 'bound_frozen_noMod14_PASS_sources_held':cp['status']=='PASS_SCOPED_NO_MOD_NATIVE2780_TOOLTIP_ERROR' and len(cp['checks'])==14 and all(cp['checks'].values()) and readj(control/'shroud2780-control-error-guard-execution.json')['returncode']==0 and all(h.sha256(Path(v['path']))==v['sha256'] for v in cp['native_sources']),
 'only_exact_colony_caches_changed':colonies_ok,
 'only_mother_carrier_flag1_to3':planets_ok,
 'budget_outside_current_highwater_raw_held':omit(bc['budget'],{'current_month','income_high_water_mark'})==omit(ac['budget'],{'current_month','income_high_water_mark'}),
 'exact_predeclared_income_expense_cells_only':exact_cells('income',income) and exact_cells('expenses',expenses),
 'all_budget_balances_income_minus_expense':balances_ok,
 'highwater_only_length6_to7_and_current_equals_income':q.scalars(bh)['length']==6 and q.scalars(ah)['length']==7 and omit(bh,{'length','current'})==omit(ah,{'length','current'}) and highwater_ok,
 'actual9666_population_and_housing_amenity_arithmetic':a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']==9666 and a['colonies']['0']['housing_usage']==9666 and a['colonies']['0']['total_housing']-9666==a['colonies']['0']['free_housing'] and D(str(a['colonies']['0']['amenities']))-D(str(a['colonies']['0']['amenities_usage']))==D(str(a['colonies']['0']['free_amenities'])),
 'fresh_unfiltered_error_baseline_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
def raw(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return {k:v for k,v,o in q.fields(t) if o}
br,ar=raw(before),raw(after)
checks['all_construction_and_mother_building_zone_raw_held']=all(br[k]==ar[k] for k in ['construction','buildings','zones','districts'])
leader_source=h.GAME_EXE.parent/'common/traits/00_special_leader_traits.txt';ls=q.block(leader_source.read_text('utf-8-sig'),'leader_trait_psionic')
checks['native_psionic_ruler_influence_half_source']=any(q.scalars(v).get('country_ruler_influence_produces_add')==.5 and q.scalars(q.block(v,'potential'))=={'is_ruler':'yes'} for k,v,o in q.fields(ls) if k=='triggered_councilor_modifier')
p={'status':'PASS_NATIVE2780_PRODUCTION_RESUME_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':True,'income_changes':{str(k):v for k,v in income.items()},'expense_changes':{str(k):v for k,v in expenses.items()},'actual_current_month_nets':{k:sum(v.get(k,0) for v in cur['balance'].values()) for k in ['energy','minerals','unity','alloys','trade']},'native_leader_source':{'path':str(leader_source),'sha256':h.sha256(leader_source)},'scope':'21 original checks mandatory plus exact same-date full-Psi budget/housing/amenity/carrier reload caches, no actual stock/population/reward change. Original24 FAIL retained. Full month, complete breach and route still pending.'};out=run/(after+'-resume-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original resume supplement FAIL retained'
