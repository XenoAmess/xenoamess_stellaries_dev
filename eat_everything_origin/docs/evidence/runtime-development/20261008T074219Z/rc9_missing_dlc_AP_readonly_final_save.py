import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();variant=m['dlc_variant'];assert variant in ['nemesis','shroud']
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
stem='rc9-missing-'+variant+'-native-AP-readonly-finished'
start='rc9-missing-'+variant+'-completed-five-replays';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'))
def events(p):
    with zipfile.ZipFile(p) as z:t=z.read('gamestate').decode('utf-8-sig')
    return [v for k,v,o in q.fields(t) if k=='player_event' and o]
be=events(run/(start+'.sav'));c=lambda a:a['countries']['0']
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
r.gpu_click(730,185,stem+'-close-native-preview');r.gpu_capture(stem+'-preview-closed')
a=r.native_save(stem,b['date'],(0,));ae=events(run/(stem+'.sav'))
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
remaining=[x for x in be if q.scalars(x).get('event') not in ['eep.10','eep.11']]
checks={'same_date':a['date']==b['date'],'all_root_stock_same':c(a)['stockpile']==c(b)['stockpile'],'all_real_pop_groups_same':a['pop_groups']==b['pop_groups'],
 'all_EEP_variables_same':c(a)['variables']==c(b)['variables'],'all_EEP_flags_same':c(a)['flags']==c(b)['flags'],
 'AP_empty_unchanged':c(a)['ascension_perks']==[],'traditions_no_purchase':c(a).get('traditions')==c(b).get('traditions'),
 'technology_same':c(a)['completed_technologies']==c(b)['completed_technologies'],'research_queues_same':c(a)['research_queues']==c(b)['research_queues'],
 'all_colonies_same':a['colonies']==b['colonies'],'all_physical_planets_same':a['planets']==b['planets'],
 'districts_same':a['districts']==b['districts'],'deposits_same':a['deposits']==b['deposits'],'situations_same':a['situations']==b['situations'],
 'global_targets_same':a['event_targets']==b['event_targets'],'only_native_intro_and_first_swallow_messages_acknowledged':ae==remaining,
 'no_corresponding_notice':('eep_fleet_notice' if variant=='nemesis' else 'eep_psi_notice') not in c(a)['flags'],'no_new_errors':ea==eb}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
 'before_messages':[q.scalars(x) for x in be],'after_messages':[q.scalars(x) for x in ae],
 'scope':'Native unavailable-inclusive AP preview and normal acknowledgement of intro/first swallow, with all economic state and no purchases/grants.'}
h.write_json(run/(stem+'-proof.json'),v);print(json.dumps(v),flush=True);assert all(checks.values())
