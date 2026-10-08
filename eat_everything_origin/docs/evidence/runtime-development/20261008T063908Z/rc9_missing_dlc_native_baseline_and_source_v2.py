import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();variant=m['dlc_variant'];assert variant in ['nemesis','shroud']
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
stem='rc9-missing-'+variant
b=json.loads((run/(stem+'-legal-fresh-initial.audit.json')).read_text(encoding='utf-8'))
with zipfile.ZipFile(run/(stem+'-legal-fresh-initial.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
tables={k:v for k,v,o in q.fields(t) if o};country=q.block(tables['country'],'0')
assert q.scalars(q.block(country,'government'))['origin']=='origin_heart_of_devouring'
assert 'civic_hive_scorched_earth' in b['countries']['0']['government']
assert b['countries']['0']['ascension_perks']==[]
v=b['countries']['0']['variables'];assert all(v.get(k,0)==value for k,value in {'eep_c':0,'eep_g':0,'eep_d':2,'eep_made':0,'eep_worlds':0,'eep_fleet_stage':0,'eep_psi':0}.items())
h.press_scan_code(0x29,stem+'-controlled-source-console-open',1)
cmd='effect root = { save_event_target_as = eep_probe_country eep_probe_create_source = { SIZE = 8 TARGET = eep_missing_dlc_source START = no } event_target:eep_missing_dlc_source = { set_name = "EEP-DLC-Q8" } }'
h.type_text(cmd,True,stem+'-controlled-Q8-colony-and-100-seed')
r.gpu_capture(stem+'-controlled-source-native-receipt');h.press_scan_code(0x29,stem+'-controlled-source-console-close',1)
a=r.native_save(stem+'-controlled-source-ready','2200.01.01',(0,))
targets=[x for x in a['event_targets'] if x['name']=='eep_missing_dlc_source'];assert len(targets)==1
source=a['planets'][str(targets[0]['id'])];col=a['colonies'][str(source['colony'])]
pop=lambda x:sum(x['colonies'][str(i)]['actual_pop_sum'] for i in x['countries']['0']['owned_colonies'])
checks={'same_date':a['date']==b['date'],'source_Q8':source['planet_size']==8,'source_colonized':col.get('colonizing_species') is None,
 'actual_source_100':col['actual_pop_sum']==100,'actual_total_population_conserved':pop(a)==pop(b),
 'ledger_no_awards':a['countries']['0']['variables']==v,'AP_no_grants':a['countries']['0']['ascension_perks']==[],
 'tech_no_grants':a['countries']['0']['completed_technologies']==b['countries']['0']['completed_technologies'],
 'no_tasks_yet':not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values())}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'source_physical':targets[0]['id'],
 'source_colony':source['colony'],'before_population':pop(b),'after_population':pop(a),'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
 'scope':'Controlled own Q8 volcanic colony; real 100 founder population resettled from initial bound mother. Not natural colonization or AP acquisition.'}
h.write_json(run/(stem+'-controlled-source-preflight.json'),proof);print(json.dumps(proof),flush=True);assert all(checks.values())
