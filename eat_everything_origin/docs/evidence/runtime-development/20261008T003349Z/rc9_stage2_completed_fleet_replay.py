import json, logging, shutil, sys, zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run()
copy=run/Path(__file__).name
assert not copy.exists();shutil.copyfile(Path(__file__),copy)
stem='rc9-stage2-native-first-queen-five-replays'
b=json.loads((run/'rc9-stage2-native-first-queen-acknowledged.audit.json').read_text(encoding='utf-8'))
ids=tuple(int(i) for i in b['countries'])
def raw_state(path):
    with zipfile.ZipFile(path) as z:t=z.read('gamestate').decode('utf-8-sig')
    fields=list(q.fields(t));tables={k:v for k,v,o in fields if o}
    events=[{'scalars':q.scalars(v),'scope':q.scalars(q.block(v,'scope'))} for k,v,o in fields if o and k=='player_event']
    cp=q.block(q.block(tables['country'],'0'),'crisis_progression')
    return {'player_events':events,'crisis_raw':cp,'core_raw':q.block(q.block(tables['planets'],'planet'),'1'),'source_raw':q.block(q.block(tables['planets'],'planet'),'660')}
br=raw_state(run/'rc9-stage2-native-first-queen-acknowledged.sav')
pre={'actual_native_level2':'level="crisis_level_2"' in br['crisis_raw'],
     'actual_first_notice_flag':'eep_fleet_notice' in b['countries']['0']['flags'],
     'fleet_stage2':b['countries']['0']['variables']['eep_fleet_stage']==2,
     'queen31_already_acknowledged':not any(x['scalars'].get('event')=='eep.31' for x in br['player_events']),
     'source_shattered':b['planets']['660']['planet_class']=='pc_shattered',
     'only_original_mother_owned':b['countries']['0']['owned_colonies']==[0],
     'no_live_eep_tasks':not any(v.get('type')=='situation_eep_devouring' and v.get('killed')!='yes' for v in b['situations'].values())}
h.write_json(run/(stem+'-preconditions.json'),{'status':'PASS_SCOPED' if all(pre.values()) else 'FAILED_PRECONDITION','checks':pre,'save_sha256':b['save_sha256']})
assert all(pre.values())
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stem+'-console-open',1)
for n in range(5):
    h.type_text('effect root = { country_event = { id = eep.2 } every_situation = { limit = { is_situation_type = situation_eep_devouring } situation_event = { id = eep.21 } } }',True,stem+'-replay-'+str(n))
r.gpu_capture(stem+'-native-receipt');h.press_scan_code(0x29,stem+'-console-close',1)
a=r.native_save(stem,b['date'],ids);ar=raw_state(run/(stem+'.sav'))
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
groups=lambda v:{k:{f:z.get(f) for f in ['planet','size','key']} for k,z in v['pop_groups'].items()}
checks={'actual_same_date':a['date']==b['date'],
        'all45_country_stock_same':all(a['countries'][i]['stockpile']==b['countries'][i]['stockpile'] for i in b['countries']),
        'all_actual_population_groups_same':groups(a)==groups(b),
        'root_all_eep_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
        'root_eep_flags_same':a['countries']['0']['flags']==b['countries']['0']['flags'],
        'root_AP_same':a['countries']['0']['ascension_perks']==b['countries']['0']['ascension_perks'],
        'root_tech_same':a['countries']['0']['completed_technologies']==b['countries']['0']['completed_technologies'],
        'root_research_queues_same':a['countries']['0']['research_queues']==b['countries']['0']['research_queues'],
        'all_situations_same':a['situations']==b['situations'],
        'all_event_targets_same':a['event_targets']==b['event_targets'],
        'source_full_native_same':ar['source_raw']==br['source_raw'],
        'core_full_native_same':ar['core_raw']==br['core_raw'],
        'native_crisis_and_objectives_same':ar['crisis_raw']==br['crisis_raw'],
        'player_events_same_no_queen31_repeat':ar['player_events']==br['player_events'] and not any(x['scalars'].get('event')=='eep.31' for x in ar['player_events']),
        'new_error_bytes_zero':ea==eb}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'monthly_callbacks':5,
   'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'country_count':len(ids),'population_groups':len(b['pop_groups']),
   'before_raw':br,'after_raw':ar,'error_delta_bytes':len(ea)-len(eb),'scope':'Completed natural first fleet notification and Q12 world settlement; no new rewards or messages on repeated callbacks.'}
h.write_json(run/(stem+'-proof.json'),v)
print(json.dumps({k:z for k,z in v.items() if k not in ['before_raw','after_raw']}),flush=True)
assert all(checks.values())
