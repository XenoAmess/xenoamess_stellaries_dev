import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();assert m['dlc_variant']=='nemesis'
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
stem='rc9-missing-nemesis';b=json.loads((run/(stem+'-legal-fresh-initial.audit.json')).read_text(encoding='utf-8'))
old=json.loads((run/(stem+'-controlled-source-ready.audit.json')).read_text(encoding='utf-8'))
assert set(old['countries']['0']['owned_colonies'])=={0,13} and old['colonies']['13']['actual_pop_sum']==100
h.press_scan_code(0x29,stem+'-source-bookmark-recovery-console-open',1)
h.type_text('effect root = { every_owned_planet = { limit = { is_capital = no } planet = { save_global_event_target_as = eep_missing_dlc_source set_name = "EEP-DLC-Q8" } } }',True,stem+'-source-bookmark-recovery')
r.gpu_capture(stem+'-source-bookmark-recovery-receipt');h.press_scan_code(0x29,stem+'-source-bookmark-recovery-console-close',1)
a=r.native_save(stem+'-controlled-source-ready-recovered','2200.01.01',(0,))
targets=[x for x in a['event_targets'] if x['name']=='eep_missing_dlc_source'];assert len(targets)==1 and targets[0]['id']==10
source=a['planets']['10'];col=a['colonies']['13'];pop=lambda x:sum(x['colonies'][str(i)]['actual_pop_sum'] for i in x['countries']['0']['owned_colonies'])
checks={'same_date':a['date']==b['date'],'source_Q8':source['planet_size']==8,'source_colonized':col.get('colonizing_species') is None,
 'actual_source100':col['actual_pop_sum']==100,'real100_from_mother':a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']-100,
 'population_conserved':pop(a)==pop(b),'ledger_no_awards':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'AP_no_grants':a['countries']['0']['ascension_perks']==[],'tech_no_grants':a['countries']['0']['completed_technologies']==b['countries']['0']['completed_technologies'],
 'no_tasks_yet':not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'recovery_population_unchanged':a['pop_groups']==old['pop_groups'],'recovery_all_stock_unchanged':a['countries']['0']['stockpile']==old['countries']['0']['stockpile']}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'source_physical':10,'source_colony':13,'before_population':pop(b),'after_population':pop(a),'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Controlled Q8 mature colony and real 100 seed; recovery only corrects native target/name, no new colony or population.'}
h.write_json(run/(stem+'-controlled-source-recovered-preflight.json'),v);print(json.dumps(v),flush=True);assert all(checks.values())
