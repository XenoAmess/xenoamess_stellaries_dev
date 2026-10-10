"""Read-only production Terravore legal-start component checks."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
stage='terravore-legal-initial-pending'
a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'))
ob=json.loads((run/(stage+'-observation.json')).read_text(encoding='utf-8'))
with zipfile.ZipFile(run/(stage+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
roots=list(q.fields(t));objects={k:v for k,v,o in roots if o}
c=a['countries']['0'];gov=q.scalars(c['government']);gal=q.scalars(objects['galaxy'])
core=a['planets']['7'];col=a['colonies']['0'];founder=str(c['native']['founder_species_ref'])
species=a['species'][founder]
expected={'eep_c':0,'eep_g':0,'eep_d':2,'eep_made':0,'eep_worlds':0,'eep_stage':0,
          'eep_last_capacity':0,'eep_last_return':0,'eep_last_manufactured':0,'eep_fleet_stage':0}
checks={
'actual_initial_date':a['date']=='2200.01.01',
'original_SHA_bound':a['save_sha256']==ob['save_sha256']==h.sha256(run/(stage+'.sav')),
'formal_production41_exact':len(m['repository_mod_files'])==41 and h.tree_manifest(Path(m['copied_mod']))[1]==m['copied_mod_tree_sha256']=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
'only_formal_mod':json.loads((user/'dlc_load.json').read_text(encoding='utf-8'))=={'enabled_mods':['mod/ugc_eep-local.mod'],'disabled_dlcs':[]},
'no_seed_or_scheduled_commands':m['seeded_save'] is None and m['scheduled_commands']==[],
'no_probe_gamestate':'eep_probe' not in t,
'legal_hive_government':gov['type']=='gov_devouring_swarm' and gov['authority']=='auth_hive_mind',
'legal_civics':q.ids(q.block(c['government'],'civics'))==['civic_hive_devouring_swarm','civic_hive_ascetic'],
'actual_origin':gov['origin']=='origin_heart_of_devouring',
'zero_reward_initial_ledger':c['variables']==expected,
'one_owned_colony_and_bound_core':c['owned_colonies']==[0] and c['native']['capital']==0 and core['colony']==0 and core['owner']==0 and core['controller']==0,
'unique_core_flag':[(i,v) for i,v in a['planets'].items() if 'eep_core' in v['flags']]==[('7',core)],
'unique_bound_event_targets':sorted((v['name'],v['type'],v['id']) for v in a['event_targets'])==[('eep_core0','planet',7),('eep_core_actor7','country',0)],
'one_original_core_deposit':[(i,v['deposit_holder']) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core']==[('1573',{'type':0,'id':7})],
'original_size18_extra_capacity2':core['planet_size']==18 and core['variables']['eep_capacity_value']==2 and core['modifiers'].count('modifier="eep_capacity"')==1 and 'multiplier=2' in core['modifiers'],
'one_permanent_court':core['modifiers'].count('modifier="eep_court"')==1 and core['modifiers'].count('days=-1')==2,
'legal_lithoid_hive_founder':species['class']=='LITHOID' and species['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference'],
'actual5300_native_initial_population':col['actual_pop_sum']==5300 and all(a['pop_groups'][str(i)]['key']['species']==int(founder) for i in col['pop_groups']),
'no_initial_AP_or_traditions':c['ascension_perks']==[] and c['traditions']==[],
'no_EEP_situation':not any(v.get('type')=='situation_eep_devouring' for v in a['situations'].values()),
'no_country0_pending':not [q.scalars(v) for k,v,o in roots if k=='player_event' and o and q.scalars(v).get('country')==0],
'actual_tiny_elliptical_galaxy':gal['template']=='tiny' and gal['shape']=='elliptical',
'actual_ai3_advanced0':gal['num_empires']==3 and gal['num_advanced_empires']==0,
'actual_native_cost_multipliers':gal['technology']==0.5 and gal['traditions']==0.25,
'actual_ensign_nonironman':gal['difficulty']=='ensign' and gal['ironman']=='no',
'no_new_save_errors':ob['new_error_bytes']==0 and ob['error_prefix_held'] is True}
proof={'status':'PASS_LEGAL_TERRAVORE_INITIAL_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,
       'save_sha256':a['save_sha256'],'actual_galaxy':gal,'actual_government':gov,
       'actual_founder':species,'actual_population':col['actual_pop_sum'],'actual_stockpile':c['effective_stockpile'],
       'scope':'This native production-only initial state; not Queen completion, natural economy, full route or default1 cost acceptance.'}
h.write_json(run/'terravore-legal-initial-proof.json',proof);print(json.dumps(proof,ensure_ascii=False),flush=True)
assert all(checks.values()),'Original initial check failure retained'
