"""Read-only first native Terravore decision and exact initial task effects."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-colonization-wait-halfyear';after='terravore-native-devour-start'
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'));bc,ac=b['countries']['0'],a['countries']['0'];bp,ap=b['planets']['90'],a['planets']['90']
with zipfile.ZipFile(run/(after+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
pending=[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
newflags={'eep_active','eep_owned_colony_event','colony_event','eep_native','being_devoured','recently_eaten_planet'}
sits={i:s for i,s in a['situations'].items() if s.get('type')=='situation_eep_devouring'}
ignore={'variables','flags','modifiers','save_on_death','carrier_binary_flags','binary_flags'}
checks={'same_actual_date':a['date']==b['date']=='2206.11.01','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'no_pending':not pending,'all_real_economy_and_research_banks_held':bc['effective_stockpile']==ac['effective_stockpile'],
 'exact_Q17_T41_and_existing_seed102':ap['variables']=={'eep_q':17,'eep_months':41,'eep_old_damage':0,'eep_seed_existing':102,'eep_seed_need':-2},
 'source_population102_without_mother_relocation':b['colonies']['15']['actual_pop_sum']==a['colonies']['15']['actual_pop_sum']==102 and b['colonies']['0']['actual_pop_sum']==a['colonies']['0']['actual_pop_sum']==5897,
 'only_exact_six_flags_added':set(ap['flags'])-set(bp['flags'])==newflags and all(ap['flags'].get(k)==v for k,v in bp['flags'].items()),
 'exact_native360_cooldown':ap['flags']['recently_eaten_planet']=={'flag_date':62867040,'flag_days':360},
 'native_permanent_being_devoured_modifier':ap['modifiers'].count('modifier="being_devoured_modifier"')==1 and 'days=-1' in ap['modifiers'],
 'source_native_flags_and_event_target_lifetime':ap['save_on_death']==1 and ap['carrier_binary_flags']==3 and ap['binary_flags']==332,
 'other_source_physical_fields_held':{k:v for k,v in bp.items() if k not in ignore}=={k:v for k,v in ap.items() if k not in ignore},
 'exact_one_task0_progress_for90':len(sits)==1 and all(s['country']==0 and s['progress']==0 and s['approach']=='eep_devour_approach' and s['target']['type']=='planet' and s['target']['id']==90 for s in sits.values()),
 'no_native_duplicate_consume_situation':not any(s.get('type')=='situation_terravore_consume_planet' for s in a['situations'].values()),
 'original_other_situations_held':all(a['situations'].get(i)==v for i,v in b['situations'].items()),
 'exact_task_actor_target_added':a['event_targets']==b['event_targets']+[{'type':'country','id':0,'opener_id':4294967295,'name':'eep_task_actor90'}],
 'all_other_owned_planets_and_mother_held':set(b['planets'])==set(a['planets']) and all(a['planets'].get(i)==v for i,v in b['planets'].items() if i!='90'),
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-colonization-wait-halfyear-error-before.log').read_bytes()}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','districts','deposits','species']:checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_TERRAVORE_START_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_situations':sits,'source_variables':ap['variables'],'source_flags':ap['flags'],'scope':'One native legal decision with actual seed102, Q17/T41 and no rewards. No monthly bites, completion or full route acceptance yet.'}
out=run/(after+'-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original task start difference retained; do not replay decision'
