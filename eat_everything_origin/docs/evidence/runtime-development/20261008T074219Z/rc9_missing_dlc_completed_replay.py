import json,logging,shutil,sys,zipfile
from pathlib import Path
start=sys.argv[1];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();variant=m['dlc_variant'];assert variant in ['nemesis','shroud']
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
stem='rc9-missing-'+variant+'-completed-five-replays'
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'))
def raw(p):
    with zipfile.ZipFile(p) as z:t=z.read('gamestate').decode('utf-8-sig')
    f=list(q.fields(t));tables={k:v for k,v,o in f if o};country=q.block(tables['country'],'0')
    return {'events':[v for k,v,o in f if o and k=='player_event'],'crisis':q.block(country,'crisis_progression')}
br=raw(run/(start+'.sav'));c=lambda a:a['countries']['0']
assert all(c(b)['variables'][k]==v for k,v in {'eep_c':8,'eep_g':8,'eep_d':4,'eep_made':100,'eep_worlds':1,'eep_fleet_stage':0}.items())
assert c(b)['ascension_perks']==[] and 'eep_first_notice' in c(b)['flags']
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stem+'-console-open',1)
for n in range(5):
    h.type_text('effect root = { country_event = { id = eep.2 } every_situation = { limit = { is_situation_type = situation_eep_devouring } situation_event = { id = eep.21 } } }',True,stem+'-callback-'+str(n))
r.gpu_capture(stem+'-native-receipt');h.press_scan_code(0x29,stem+'-console-close',1)
a=r.native_save(stem,b['date'],(0,));ar=raw(run/(stem+'.sav'))
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
checks={'date_same':a['date']==b['date'],'all_root_stock_same':c(a)['stockpile']==c(b)['stockpile'],
 'all_real_pop_groups_same':a['pop_groups']==b['pop_groups'],'ledger_same':c(a)['variables']==c(b)['variables'],
 'EEP_flags_same':c(a)['flags']==c(b)['flags'],'AP_empty_unchanged':c(a)['ascension_perks']==[],
 'technology_same':c(a)['completed_technologies']==c(b)['completed_technologies'],'research_queues_same':c(a)['research_queues']==c(b)['research_queues'],
 'all_colonies_same':a['colonies']==b['colonies'],'all_planets_same':a['planets']==b['planets'],
 'districts_same':a['districts']==b['districts'],'deposits_same':a['deposits']==b['deposits'],
 'situations_same':a['situations']==b['situations'],'global_targets_same':a['event_targets']==b['event_targets'],
 'native_crisis_progression_same':ar['crisis']==br['crisis'],'player_messages_same':ar['events']==br['events'],
 'no_corresponding_unlock_flags':('eep_fleet_notice' if variant=='nemesis' else 'eep_psi_notice') not in c(a)['flags'],
 'no_new_error_bytes':ea==eb}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'variant':variant,'callbacks':5,'scope':'Completed Q8 basic mechanism with actual missing DLC; repeated monthly/settlement callbacks cannot reward or grant absent abilities.'}
h.write_json(run/(stem+'-proof.json'),v);print(json.dumps(v),flush=True);assert all(checks.values())
