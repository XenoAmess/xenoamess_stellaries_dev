"""Independent native month accounting and safe idle-wait boundaries."""
import json,logging,math,sys
from collections import Counter
start,end=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
a,b=[read_state(run,s) for s in (start,end)]
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
cash=('energy','minerals','alloys','unity','trade','rare_crystals')
budget=bc['budget_categories']['current_month']
net={k:sum(float(v.get(k,0)) for v in budget['income'].values())-sum(float(v.get(k,0)) for v in budget['expenses'].values()) for k in cash}
delta={k:float(bc['effective_stockpile'].get(k,0))-float(ac['effective_stockpile'].get(k,0)) for k in cash}
residual={k:delta[k]-net[k] for k in cash}
lost=set(a['ships'])-set(b['ships']);born=set(b['ships'])-set(a['ships'])
ship_checks=[]
for sid in set(a['ships'])&set(b['ships']):
 old,new=q.scalars(a['ships'][sid]),q.scalars(b['ships'][sid])
 checks=[q.block(a['ships'][sid],'ship_design_implementation')==q.block(b['ships'][sid],'ship_design_implementation')]
 checks += [old.get(k)==new.get(k) for k in ('max_hitpoints','max_shield_hitpoints','max_armor_hitpoints','construction_date')]
 for hp,mx in [('hitpoints','max_hitpoints'),('shield_hitpoints','max_shield_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
  ov,nv,maximum=old.get(hp,0),new.get(hp,0),new.get(mx,0)
  checks.append(all(isinstance(x,(float,int)) and math.isfinite(x) for x in (ov,nv,maximum)) and -0.001<=nv<=maximum+0.001 and (nv+0.001>=ov or (hp=='shield_hitpoints' and nv==0 and q.scalars(q.block(b['ships'][sid],'coordinate')).get('origin')==39 and 'turbulent_nebula' in q.block(q.block(b['roots']['galactic_object'],'39'),'timed_modifier') and old.get('last_damage')==new.get('last_damage'))))
 ship_checks.append(all(checks))
def armies(s):return {k:v for k,v,x in q.fields(s['roots']['army']) if x and q.scalars(v).get('owner')==0}
aa,ba=armies(a),armies(b)
all_army_born={k:q.scalars(v) for k,v in ba.items() if k not in aa}
army_born={k:v for k,v in all_army_born.items() if v.get('type')=='assault_army'}
defense_births={k:v for k,v in all_army_born.items() if v.get('type')!='assault_army'}
items_a={k:v for k,v in a['items'].items() if q.scalars(v).get('paying_country')==0}
items_b={k:v for k,v in b['items'].items() if q.scalars(v).get('paying_country')==0}
done=set(items_a)-set(items_b)
new_messages=[q.scalars(v) for v in b['messages'] if v not in a['messages']]
new_tech=set(bc['completed_technologies'])-set(ac['completed_technologies'])
pop_delta={str(cid):b['audit']['colonies'][str(cid)]['actual_pop_sum']-a['audit']['colonies'][str(cid)]['actual_pop_sum'] for cid in ac['owned_colonies'] if str(cid) in b['audit']['colonies']}
planets=[q.scalars(q.block(q.block(s['roots']['planets'],'planet'),'544')) for s in (a,b)]
army_done={k for k in done if q.block(items_a[k],'buildable_army')}
ship_done={k for k in done if q.block(items_a[k],'buildable_ship_reinforcement')}
army_ships={str(v.get('ship')) for v in army_born.values()}
military_born=born-army_ships
paid_designs=Counter(tuple(sorted(q.scalars(q.block(q.block(items_a[k],'buildable_ship_reinforcement'),'ship_design_implementation')).items())) for k in ship_done)
born_designs=Counter(tuple(sorted(q.scalars(q.block(b['ships'][k],'ship_design_implementation')).items())) for k in military_born)
births_accounted=(done==army_done|ship_done and not(set(items_b)-set(items_a)) and set(aa)<=set(ba)
 and len(army_born)==len(army_done)==len(army_ships) and army_ships<=born
 and all(v.get('type')=='assault_army' and v.get('species')==73 and q.scalars(b['ships'][str(v['ship'])]).get('army')==int(k) for k,v in army_born.items())
 and all(q.scalars(q.block(items_a[k],'resources'))=={'minerals':100} and q.scalars(q.block(items_a[k],'buildable_army')).get('army_type')=='assault_army' and q.scalars(q.block(items_a[k],'buildable_army')).get('species')==73 and q.scalars(q.block(items_a[k],'buildable_army')).get('planet') in (0,40) and q.scalars(a['queues'][str(q.scalars(items_a[k])['queue'])]).get('owner')==0 and q.scalars(q.block(a['queues'][str(q.scalars(items_a[k])['queue'])],'location')).get('id')=={0:7,40:544}[q.scalars(q.block(items_a[k],'buildable_army'))['planet']] for k in army_done)
 and len(military_born)==len(ship_done) and born_designs==paid_designs
 and all(q.scalars(q.block(items_a[k],'resources'))=={'minerals':412.5} and q.scalars(q.block(q.block(items_a[k],'buildable_ship_reinforcement'),'ship_design_implementation')).get('design')==83887141 and q.scalars(q.block(items_a[k],'buildable_ship_reinforcement')).get('fleet_template') in (33554475,268435546) for k in ship_done)
 and all(a['audit']['date']<=q.scalars(b['ships'][k])['construction_date']<b['audit']['date'] for k in born))
old_situations={k:v for k,v in a['audit']['situations'].items() if v.get('type')=='situation_eep_devouring' and v.get('country')==0}
new_situations={k:v for k,v in b['audit']['situations'].items() if v.get('type')=='situation_eep_devouring' and v.get('country')==0}
old_source,new_source=[s['audit']['planets']['544'] for s in (a,b)]
added_deposits=set(new_source['deposits'])-set(old_source['deposits'])
bite=len(added_deposits)==2 and all(q.scalars(q.block(b['roots']['deposit'],str(i))).get('type')=='d_lithoid_devastation' for i in added_deposits)
unchanged_deposits=old_source['deposits']==new_source['deposits']
levels=[sum(s['audit']['districts'][str(i)]['level'] for i in s['audit']['colonies']['40']['districts']) for s in (a,b)]
native_messages=[v for v in new_messages if v.get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD' and v.get('target_planet')==544 and v.get('date')==b['audit']['date']]
branch=None
if bite and len(native_messages)==1:
 branch={'MESSAGE_TERRAVORE_CONSUME_WORLD_POP_TEXT':'pop','MESSAGE_TERRAVORE_CONSUME_WORLD_MINERALS_TEXT':'minerals','MESSAGE_TERRAVORE_CONSUME_WORLD_ALLOYS_TEXT':'alloys'}.get(native_messages[0].get('localization'))
cash_accounted=(all(abs(v)<0.001 for v in residual.values()) if branch in (None,'pop') else 100<=residual[branch]<=1000 and all(abs(v)<0.001 for k,v in residual.items() if k!=branch))
devastation=[v.get('bombardment_damage',0) for v in (old_source,new_source)]
damage_accounted=(abs(devastation[1]-min(100,devastation[0]+20))<.001 if bite else -2<=devastation[1]-devastation[0]<=.001)
digest_held=(set(old_situations)==set(new_situations)=={'67108877'} and new_situations['67108877']['progress']==old_situations['67108877']['progress']+1 and new_situations['67108877']['target']['id']==544 and new_situations['67108877']['approach']=='eep_devour_approach'
 and old_source['variables']==new_source['variables'] and new_source['variables']['eep_months']==48
 and set(old_source['deposits'])<=set(new_source['deposits']) and ((bite and branch is not None and levels[1]-levels[0] in (-1,0)) or (unchanged_deposits and levels[1]==levels[0]))
 and damage_accounted and old_source.get('last_bombardment')==new_source.get('last_bombardment') and all(k in new_source['flags'] for k in ('eep_active','eep_native','being_devoured','recently_eaten_planet')))
defense_accounted=all(v.get('type')=='defense_army' and v.get('owner')==0 and v.get('species')==73 and v.get('colony')==v.get('spawning_colony')==40 and v.get('health')==v.get('max_health')==250 and v.get('morale')==250 and not v.get('ship') for v in defense_births.values())
growth_evidence={}
for cid in ac['owned_colonies']:
 colony=q.block(b['roots']['colony'],str(cid))
 raw=q.block(colony,'last_month_growth_data')
 summary=q.scalars(q.block(raw,'growth_and_size'))
 fs=list(q.fields(q.block(raw,'current_month_growth_details')))
 details={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
 species=[q.scalars(q.block(q.block(b['roots']['pop_groups'],str(pid)),'key')).get('species') for pid in q.ids(q.block(colony,'pop_groups'))]
 other=details.get('GROWTH_CAT_OTHER',0)
 native_other=(100 if cid==40 and branch=='pop' else 0)
 calculated=details.get('GROWTH_CAT_GROWTH',0)+details.get('GROWTH_CAT_IMMIGRATION',0)-details.get('GROWTH_CAT_EMIGRATION',0)+other
 valid=(summary.get('month_start_size')==a['audit']['colonies'][str(cid)]['actual_pop_sum'] and summary.get('growth')==pop_delta[str(cid)]==calculated and abs(calculated)<=200 and other==native_other and all(v==73 for v in species) and set(details)<={'GROWTH_CAT_GROWTH','GROWTH_CAT_IMMIGRATION','GROWTH_CAT_EMIGRATION','GROWTH_CAT_PROMOTION','GROWTH_CAT_OTHER'} and details.get('GROWTH_CAT_PROMOTION',0)==0)
 growth_evidence[str(cid)]={'summary':summary,'details':details,'calculated':calculated,'pass':valid}
population_accounted=all(v['pass'] for v in growth_evidence.values()) and sum(v['details'].get('GROWTH_CAT_IMMIGRATION',0)-v['details'].get('GROWTH_CAT_EMIGRATION',0) for v in growth_evidence.values())==0
checks={
 'digest_progress_and_material_exact':digest_held,
 'native_month_sources':b['audit']['date'].endswith('.01') and all(h.sha256(run/(s+'.sav'))==v['audit']['save_sha256'] for s,v in [(start,a),(end,b)]),
 'six_cash_exact_month_and_solvent':cash_accounted and all(bc['effective_stockpile'].get(k,0)>=0 for k in cash),
 'mod_crisis_and_colonial_identity_held':ac['variables']==bc['variables'] and ac['owned_colonies']==bc['owned_colonies']==[0,40] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression') and all(p.get('owner')==p.get('controller')==0 and p.get('colony')==40 and p.get('planet_size')==20 for p in planets),
 'old_ships_retained_repaired_and_unmodified':not lost and all(ship_checks),
 'paid_army_and_reinforcement_births_accounted':births_accounted and defense_accounted,
 'population_natural_and_no_pending_or_errors':population_accounted and not b['pending'] and (run/(end+'-error-before.log')).read_bytes()==(run/(end+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes(),
}
boundaries=[]
if born and not any(q.scalars(v).get('type')=='assault_army' for v in aa.values()):boundaries.append('paid_army_birth_needs_UI_review')
if len(new_messages)!=len(native_messages) or (native_messages and not bite):boundaries.append('unknown_native_messages')
if new_tech:boundaries.append('native_research_completed')
if not digest_held:boundaries.append('digest_boundary_or_deviation')
if bc['effective_stockpile']['minerals']<700:boundaries.append('mineral_supply')
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'date':b['audit']['date'],'calendar_ready':all(checks.values()) and not boundaries,'boundaries':boundaries,'cash_delta':delta,'current_month_net':net,'residual':residual,'population_delta':pop_delta,'growth_evidence':growth_evidence,'native_bite':bite,'native_branch':branch,'added_deposits':sorted(added_deposits),'source_district_levels':levels,'source_devastation':devastation,'native_defense_births':defense_births,'lost_ships':sorted(lost),'digest_progress':new_situations.get('67108877',{}).get('progress'),'born_ships':sorted(born),'born_military_ships':sorted(military_born),'completed_reinforcement_items':sorted(ship_done),'born_armies':army_born,'completed_paid_items':sorted(done),'new_messages':new_messages,'new_tech':sorted(new_tech)}
out=run/(end+'-native-bite-v7-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof,ensure_ascii=False),flush=True)
sys.exit(0 if proof['pass'] else 1)
