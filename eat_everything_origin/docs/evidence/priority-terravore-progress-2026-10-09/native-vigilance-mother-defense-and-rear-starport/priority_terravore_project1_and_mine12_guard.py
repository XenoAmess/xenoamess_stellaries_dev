"""Native PSIONIC_1 completed, second prepaid mine completed, real monthly ledger."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-caravan-homicide-acked';after='terravore-mine12-project1-threshold30'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def objects(v):return {k:x for k,x,o in q.fields(v) if o}
def omit(v,ks):return [(k,x,o) for k,x,o in q.fields(v) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
bfl,afl=objects(br['fleet']),objects(ar['fleet']);bsh,ash=objects(br['ships']),objects(ar['ships']);bb,ab=objects(br['buildings']),objects(ar['buildings']);bz,az=objects(br['zones']),objects(ar['zones'])
own=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(acr,'fleets_manager'),'owned_fleets'))));ships=[s for i in own if q.scalars(afl[str(i)])['ship_class']=='shipclass_military' for s in q.ids(q.block(afl[str(i)],'ships'))]
pre=json.loads((run/(before+'-caravan-ack-v2-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-v2-execution.json')).read_text('utf-8'));rc=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
proj=lambda cr:{q.scalars(v)['id']:v for k,v,o in q.fields(q.block(cr,'events')) if k=='special_project' and o}
bp,ap=proj(bcr),proj(acr);pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
nets={};residuals={}
for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']:
 nets[k]=sum(D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values());expected=D(str(bc['effective_stockpile'].get(k,0)))+nets[k]
 if k=='influence':expected=min(D('1000'),expected)
 residuals[k]=D(str(ac['effective_stockpile'].get(k,0)))-expected
src=Path('C:/SteamLibrary/steamapps/common/Stellaris');spec=src/'common/special_projects/00_projects_nemesis.txt';events=src/'events/nemesis_crisis_events.txt'
checks={
 'original_SHA_pair_dates':b['date']=='2263.04.17' and a['date']=='2263.05.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior13_caravan_ACK_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_NATIVE_CARAVAN_HOMICIDAL_EXIT_COMPONENT_V2' and len(pre['checks'])==13 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='fc9c560aa1ebf058f1ed66272643260f6a5277cc93c73a7b8dae52ebe764283b',
 'unique30_calendar_actual_exit0':rc['days']==30 and rc['status']=='CALENDAR_CONFIRMED' and rc['start_date']==b['date'] and rc['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'native_psionic_project2_only_status_completed':q.scalars(bp[2])['special_project']==q.scalars(ap[2])['special_project']=='CRISIS_SPECIAL_PROJECT_PSIONIC_1' and q.scalars(bp[2])['status']=='in_progress' and q.scalars(ap[2])['status']=='completed' and omit(bp[2],{'status'})==omit(ap[2],{'status'}) and bp[1]==ap[1] and set(bp)==set(ap)=={1,2},
 'society_queue_cleared_old_stored_tech607_held':bool(q.block(bc['tech_status'],'society_queue').strip()) and not q.block(ac['tech_status'],'society_queue').strip() and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_colonization_2':607.25288},
 'actual_society_bank_draw26_1595':D(str(bc['research_stockpile']['society_research']))-D(str(ac['research_stockpile']['society_research']))==D('26.15950'),
 'two_native_completion_flags63355224':all(k not in q.scalars(q.block(bcr,'flags')) and q.scalars(q.block(acr,'flags')).get(k)==63355224 for k in ['crisis_special_project_1_complete','first_special_project_finished']),
 'exact_native_crisis4120_pending225':pending==[{'id':225,'event':'crisis.4120','date':'2265.08.02','country':0}],
 'native_level1_no_menace_held':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'},
 'source_projects_and_events_SHA_bound':h.sha256(spec)=='b09f648917aa4e91cdfe2d9a8af7a09901846f16212ba957a5606d3c82aa0a25' and h.sha256(events)=='7c037b46e8b6cb8e31dab8dd69bbd34d5902cf212a5fb5c206d175aa676e7d13',
 'mining_same_object_level11_to12_others_held':q.scalars(q.block(br['districts'],'3'))=={'type':'district_mining','level':11} and q.scalars(q.block(ar['districts'],'3'))=={'type':'district_mining','level':12} and all(q.block(br['districts'],i)==q.block(ar['districts'],i) for i in ['1','2']),
 'final_paid_mine771_completed_none_empty_queue':q.ids(q.block(q.block(q.block(q.block(br['construction'],'queue_mgr'),'queues'),'0'),'items'))==[771751943] and not q.ids(q.block(q.block(q.block(q.block(ar['construction'],'queue_mgr'),'queues'),'0'),'items')) and q.scalars(q.block(q.block(ar['construction'],'item_mgr'),'items')).get('771751943')=='none',
 'all_mother_buildings_and_three_zones_raw_held':all(bz[i]==az[i] for i in ['0','2','61']) and all(bb[str(i)]==ab[str(i)] for zid in ['0','2','61'] for i in q.ids(q.block(az[zid],'buildings'))),
 'native_all_expected_workers_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2400),('technician_drone',1200)]),
 'all17_same_paid_fleet_memberships_full_design_health':len(ships)==len(set(ships))==17 and all(q.ids(q.block(bfl[str(i)],'ships'))==q.ids(q.block(afl[str(i)],'ships')) for i in own if q.scalars(afl[str(i)])['ship_class']=='shipclass_military') and all(q.scalars(ash[str(s)])['hitpoints']==270 and q.block(bsh[str(s)],'ship_design_implementation')==q.block(ash[str(s)],'ship_design_implementation') and q.scalars(bsh[str(s)])['construction_date']==q.scalars(ash[str(s)])['construction_date'] for s in ships),
 'main14_now171_attack_held_no_combat':q.block(bfl['33555034'],'current_order')==q.block(afl['33555034'],'current_order') and q.scalars(q.block(q.block(afl['33555034'],'movement_manager'),'coordinate'))=={'x':138.77038,'y':-315.16202,'origin':171} and all(not q.block(q.block(afl[str(i)],'combat'),'in_combat_with').strip() for i in own),
 'enemy_constructor_science_raw_held':all(bfl[i]==afl[i] for i in ['33555206','2','1']),
 'actual_month_growth6_only':a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+6==10314 and q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':10308,'growth':6},
 'all_eight_actual_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residuals.values()),
 'independent_last_month_equals_prior_current':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'EEP_variables_flags_species_targets_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and b['species']==a['species'] and b['event_targets']==a['event_targets'] and a['planets']['7']['modifiers']==b['planets']['7']['modifiers'] and ac['owned_colonies']==[0] and not a['situations'],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
checks={k:bool(v) for k,v in checks.items()};p={'status':'PASS_TERRAVORE_PSIONIC_PROJECT1_AND_PAID_MINE12_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'current_month_nets':{k:str(v) for k,v in nets.items()},'budget_residuals':{k:str(v) for k,v in residuals.items()},'actual_pending':pending,'calendar_ready':False,'scope':'Native project3000 completed, prepaid mine12 and real month ledger. Event225 pending; level1 and no menace. No level2, victory, outpost or full-route claim.'}
out=run/(after+'-project1-mine12-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original completion FAIL retained'
