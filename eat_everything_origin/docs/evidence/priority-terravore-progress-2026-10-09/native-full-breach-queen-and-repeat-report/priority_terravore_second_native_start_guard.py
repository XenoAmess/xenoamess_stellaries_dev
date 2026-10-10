"""Read-only first native Terravore decision and exact initial task effects."""
import json,logging,shutil,sys,zipfile,math
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'));bc,ac=b['countries']['0'],a['countries']['0'];bp,ap=b['planets']['124'],a['planets']['124']
with zipfile.ZipFile(run/(after+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
pending=[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
newflags={'eep_active','eep_native','being_devoured','recently_eaten_planet'}
if 'colony_event' not in bp['flags']:newflags|={'colony_event','eep_owned_colony_event'}
seed=b['colonies']['24']['actual_pop_sum'];damage=sum(b['deposits'][str(i)]['type']=='d_lithoid_devastation' for i in bp['deposits']);qvalue=bp['planet_size']-damage;months=math.ceil(qvalue*2.4)
sits={i:s for i,s in a['situations'].items() if s.get('type')=='situation_eep_devouring'}
ignore={'variables','flags','modifiers','save_on_death','carrier_binary_flags','binary_flags'}
checks={'same_actual_date':a['date']==b['date'],'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'no_pending':not pending,'all_real_economy_and_research_banks_held':bc['effective_stockpile']==ac['effective_stockpile'],
 'exact_actual_Q_T_and_existing_founder_seed':ap['variables']=={'eep_q':qvalue,'eep_months':months,'eep_old_damage':damage,'eep_seed_existing':seed,'eep_seed_need':100-seed} and seed>=100 and all(g['key']['species']==3321888769 for g in b['pop_groups'].values() if g['planet']==24 and g['size']>0),
 'actual_source_population_without_mother_relocation':b['colonies']['24']['actual_pop_sum']==a['colonies']['24']['actual_pop_sum']==seed and b['colonies']['0']['actual_pop_sum']==a['colonies']['0']['actual_pop_sum'],
 'only_exact_required_flags_added':set(ap['flags'])-set(bp['flags'])==newflags and all(ap['flags'].get(k)==v for k,v in bp['flags'].items()),
 'exact_native360_cooldown':ap['flags']['recently_eaten_planet']=={'flag_date':ap['flags']['eep_active'],'flag_days':360},
 'native_permanent_being_devoured_modifier':ap['modifiers'].count('modifier="being_devoured_modifier"')==1 and 'days=-1' in ap['modifiers'],
 'source_native_flags_and_event_target_lifetime':ap['save_on_death']==1 and ap['carrier_binary_flags']==bp['carrier_binary_flags'] and ap['binary_flags']==bp['binary_flags'],
 'other_source_physical_fields_held':{k:v for k,v in bp.items() if k not in ignore}=={k:v for k,v in ap.items() if k not in ignore},
 'exact_one_task0_progress_for124':len(sits)==1 and all(s['country']==0 and s['progress']==0 and s['approach']=='eep_devour_approach' and s['target']['type']=='planet' and s['target']['id']==124 for s in sits.values()),
 'no_native_duplicate_consume_situation':not any(s.get('type')=='situation_terravore_consume_planet' for s in a['situations'].values()),
 'original_other_situations_held':all(a['situations'].get(i)==v for i,v in b['situations'].items()),
 'exact_task_actor_target_added':a['event_targets']==b['event_targets']+[{'type':'country','id':0,'opener_id':4294967295,'name':'eep_task_actor124'}],
 'all_other_owned_planets_and_mother_held':set(b['planets'])==set(a['planets']) and all(a['planets'].get(i)==v for i,v in b['planets'].items() if i!='124'),
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','districts','deposits','species']:checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_TERRAVORE_START_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_situations':sits,'source_variables':ap['variables'],'source_flags':ap['flags'],'scope':'Second native decision on124 with actual founder seed, Q/T and no rewards. No monthly bites, completion or full route acceptance yet.'}
out=run/(after+'-second-start-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original task start difference retained; do not replay decision'
