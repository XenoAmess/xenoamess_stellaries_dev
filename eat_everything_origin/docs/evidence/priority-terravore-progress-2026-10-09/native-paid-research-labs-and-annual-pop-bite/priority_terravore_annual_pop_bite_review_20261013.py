"""Read-only review of the exact December native POP bite; preserve original FAIL."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-three-labs-normal-month-22811101';after='terravore-three-labs-normal-month-22811201'
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[s['countries']['0'] for s in [ba,aa]]
pre=load(before+'-three-labs-serial-month-v2-proof.json');fail=load(after+'-three-labs-serial-month-v2-proof.json');ob=load(after+'-construction-boundary-observation-v4.json')
names=[before+'-serial-labs-guard-v2',after+'-serial-labs-guard-v2',after+'-calendar',after+'-boundary-observation-v4'];xs=[load(n+'-execution.json') for n in names]
rels=['common/scripted_effects/00_scripted_effects.txt','common/pop_jobs/04_gestalt_jobs.txt','common/buildings/00_capital_buildings.txt','common/deposits/01_blocker_deposits.txt'];sources=[]
for rel in rels:
 f=h.GAME_EXE.parent/rel;dest=run/('terravore-annual-pop-native-'+f.name)
 if dest.exists():assert dest.read_bytes()==f.read_bytes()
 else:dest.write_bytes(f.read_bytes())
 sources.append({'path':str(f),'preserved':dest.name,'sha256':h.sha256(f)})
native=[Path(v['path']).read_text('utf-8-sig') for v in sources];mod=h.MOD_ROOT/'common/scripted_effects/eep_native_consume.txt';ms=mod.read_text('utf-8-sig')
tokens=lambda raw:[t[0] for t in q.tokens(raw)]
bp,ap=[s['planets']['1578'] for s in [ba,aa]];deps=ap['deposits'][len(bp['deposits']):]
old=set(q.ids(q.block(b['country'],'owned_armies')));new=set(q.ids(q.block(a['country'],'owned_armies')));added=new-old
def detail(col):
 raw=q.block(q.block(q.block(a['roots']['colony'],col),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(raw));return {q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
growth={c:detail(c) for c in ['0','30']};msgs=ob['new_country0_messages_raw'];patrol=[s['pop_jobs']['856'] for s in [ba,aa]]
expected_fail={'old_armies_held_new_only_native_source_defense_within_cap4','source14_34month_situation_advances_one_without_bite','no_new_messages_pending_combat_or_war_changes'}
checks={
 'prior18PASS0_and_original3FAIL15PASS_actual1_preserved':len(pre['checks'])==18 and all(v is True for v in pre['checks'].values()) and xs[0]['returncode']==0 and xs[1]['returncode']==1 and {k for k,v in fail['checks'].items() if v is not True}==expected_fail and sum(v is True for v in fail['checks'].values())==15,
 'calendar_observer_actual0_immutable_sources_and_SAV_pair':all(x['returncode']==0 for x in xs[2:]) and all(x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs) and len(ob['checks'])==7 and all(v is True for v in ob['checks'].values()) and pre['after_sha256']==ob['before_sha256']==h.sha256(run/(before+'.sav'))==ba['save_sha256'] and ob['after_sha256']==h.sha256(run/(after+'.sav'))==aa['save_sha256'],
 'native_consume458tokens_identical_except_declared_AI_core_destination':len(tokens(q.block(ms,'eep_native_consume')))==458 and tokens(q.block(ms,'eep_native_consume').replace('event_target:eep_core@event_target:eep_actor','owner.capital_scope'))==tokens(q.block(native[0],'consume_world')),
 'expired_two_day_cooldown_only_reset360_exact_timed_flag':bp['flags']['recently_eaten_planet']['flag_days']==2 and ap['flags']['recently_eaten_planet']=={'flag_date':63515760,'flag_days':360},
 'two_exact_native_unclearable_lithoid_deposits_capacity_minus1':deps==[134218551,117441124] and ap['deposits'][:len(bp['deposits'])]==bp['deposits'] and all(q.scalars(q.block(a['roots']['deposit'],str(i)))=={'type':'d_lithoid_devastation'} for i in deps) and q.scalars(q.block(q.block(native[3],'d_lithoid_devastation'),'planet_modifier'))=={'planet_max_districts_add':-1,'pop_environment_tolerance':-.1},
 'source_OTHER100_growth1_mother_growth6_all_species73_conserved':growth['30']=={'GROWTH_CAT_GROWTH':1,'GROWTH_CAT_OTHER':100,'GROWTH_CAT_PROMOTION':0} and growth['0'].get('GROWTH_CAT_GROWTH')==6 and ob['after_state']['species_population_by_colony']=={'0:73':11873,'30:73':388} and ba['colonies']['30']['actual_pop_sum']==287 and ba['colonies']['0']['actual_pop_sum']==11867,
 'patrol87_to100_native_one_defense_per100_capital4':patrol[0]['type']==patrol[1]['type']=='patrol_drone' and patrol[0]['workforce']==87 and patrol[1]['workforce']==100 and patrol[0]['bonus_workforce']==4.35 and patrol[1]['bonus_workforce']==5 and q.scalars(q.block(q.block(native[1],'patrol_drone'),'planet_modifier'))['planet_defense_armies_add']==1 and q.scalars(q.block(q.block(native[2],'building_hive_capital'),'planet_modifier'))['planet_defense_armies_add']=='@tier_2_capital_defense_armies' and q.scalars(native[2])['@tier_2_capital_defense_armies']==4,
 'all_old_armies_raw_held_only_one_new_native_source_defense250':old<=new and added=={50331803} and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in old) and q.scalars(q.block(a['roots']['army'],'50331803'))=={'type':'defense_army','health':250,'max_health':250,'jump_drive_cooldown':'0.01.01','owner':0,'species':73,'colony':30,'spawning_colony':30,'morale':250} and sum(q.scalars(q.block(a['roots']['army'],str(i))).get('colony')==30 for i in new)==5,
 'only_original296_POP_notice_no_Queen_or_pending':len(msgs)==1 and q.scalars(msgs[0])=={'type':'MESSAGE_TERRAVORE_CONSUME_WORLD','localization':'MESSAGE_TERRAVORE_CONSUME_WORLD_POP_TEXT','receiver':0,'target_planet':1578,'end':'2282.03.01','date':'2281.12.01','notification':296,'message_type':'none'} and not a['pending'],
 'native_progress13_of34_EEP_C62_D17_worlds4_Menace2180_held':aa['situations']['167772163']==dict(ba['situations']['167772163'],progress=13,last_month_progress=1) and all(bc[k]==ac[k] for k in ['variables','flags','crisis','ascension_perks']) and ac['variables']['eep_c']==62 and ac['variables']['eep_d']==17 and ac['variables']['eep_worlds']==4 and ac['effective_stockpile']['menace']==2180,
 'other15_cash_research_paid_construction_assets_contracts_held':all(v is True for k,v in fail['checks'].items() if k not in expected_fail) and fail['front_lab_progress']==182 and fail['project2_progress']==4549.6339 and all(v=='0.00000' or abs(float(v))<.00005 for v in fail['cash_residual'].values()),
 'observed_source_district_levels_held_devastation20p01_not_false_demolition_claim':all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['30']['districts']) and bp['bombardment_damage']==.17 and ap['bombardment_damage']==20.18,
 'native_sources_and_unchanged_CN41_error627':all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources) and m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and reviewed_error_pair((run/(before+'-error-after.log')).read_bytes(),(run/(after+'-error-after.log')).read_bytes(),run) and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-annual-pop-bite-review-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_EXACT_NATIVE_POP_BITE_REVIEW' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'sources':sources,'original_failed_guard':after+'-serial-labs-guard-v2-execution.json','new_messages':msgs,'added_deposits':deps,'added_armies':sorted(added),'observed_devastation_delta':'20.01; native scripted20, residual0.01 origin unconfirmed','observed_source_districts':'unchanged; no claim that remove_district completed','scope':'Exact original December pair only; not settlement or full route.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
