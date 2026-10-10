"""Actual native drone victory with9 losses,90 menace; paid forge and survey still ongoing."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-aswiri-survey-ordered';after='terravore-drone-survey-forge180'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def obj(v):return {k:x for k,x,o in q.fields(v) if o}
def omit(v,ks):return [(k,x,o) for k,x,o in q.fields(v) if k not in ks]
def anon(t):
 out=[];depth=0
 for token,start,end in q.tokens(t):
  if token=='{':
   if depth==0:beg=end
   depth+=1
  elif token=='}':
   depth-=1
   if depth==0:out.append(t[beg:start])
 assert depth==0
 return out
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
bfl,afl=obj(br['fleet']),obj(ar['fleet']);bsh,ash=obj(br['ships']),obj(ar['ships']);bb,ab=obj(br['buildings']),obj(ar['buildings']);bz,az=obj(br['zones']),obj(ar['zones'])
pre=json.loads((run/(before+'-aswiri-survey-order-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'));rc=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
messages=[v for k,v,o in af if k=='message' and o and q.scalars(v).get('type')=='COMBAT_STATS' and q.scalars(v).get('receiver')==0];assert len(messages)==1
stats=q.block(messages[0],'combat_stats');counts=lambda side:{q.scalars(v)['fleet']:(q.ids(q.block(v,'ship_size_count')),q.ids(q.block(v,'ship_size_count_lost'))) for v in anon(q.block(stats,side))}
old=q.ids(q.block(bfl['33555034'],'ships'));survivors=q.ids(q.block(afl['33555034'],'ships'));lost=[i for i in old if i not in survivors];dead={k:v for k,v,o in q.fields(ar['ships']) if not o}
own=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(acr,'fleets_manager'),'owned_fleets'))));mil={i:q.ids(q.block(afl[str(i)],'ships')) for i in own if q.scalars(afl[str(i)])['ship_class']=='shipclass_military'}
holders=lambda cr:re.findall(r'\{\s*type=(\d+)\s+id=(\d+)\s*\}',q.block(cr,'surveyed_deposit_holders'))
bh,ah=holders(bcr),holders(acr);newholders=[i for i in ah if i not in bh];bi,ai=[q.block(q.block(q.block(rt['construction'],'item_mgr'),'items'),'83886102') for rt in [br,ar]]
pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0];nets={k:sum(D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys']}
checks={
 'exact_original_SHA_pair_dates':b['date']=='2263.05.17' and a['date']=='2263.11.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior16_survey_order_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_KNOWN_ASWIRI_NATIVE_SURVEY_ORDER_COMPONENT' and len(pre['checks'])==16 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='7091168b424e26e79d1e0d64ffda11f61c1122422bcdd069572fae95e4125ec9',
 'unique180_calendar_actual_exit0':rc['days']==180 and rc['status']=='CALENDAR_CONFIRMED' and rc['start_date']==b['date'] and rc['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'native_battle_message_dates_reason_and_exact_counts':q.scalars(messages[0])['date']=='2263.11.16' and q.scalars(stats)=={'date':'2263.06.08','reason':'no_more_enemies'} and counts('fleets')=={33555034:([14],[9])} and counts('enemy')=={33555206:([6],[6]),779:([1],[0])},
 'actual_exact_nine_original_ship_losses':len(old)==14 and lost==[50333102,50332844,33554476,33555618,83887261,1804,1805,1806,1809] and all(str(i) not in ash and dead.get(str(i)) in [None,'none'] for i in lost),
 'actual_five_survivors_design_dates_and_damaged_health':survivors==[33556208,33556207,50332878,1807,1810] and [q.scalars(ash[str(i)])['hitpoints'] for i in survivors]==[270,115.53034,110.49532,270,107.57356] and all(q.block(bsh[str(i)],'ship_design_implementation')==q.block(ash[str(i)],'ship_design_implementation') and q.scalars(bsh[str(i)])['construction_date']==q.scalars(ash[str(i)])['construction_date'] for i in survivors),
 'three_home_ships_held_eight_actual_naval40':mil=={788:[1816,1817],33555013:[33555519],33555034:survivors} and all(bfl[i]==afl[i] for i in ['788','33555013']) and q.scalars(acr)['fleet_size']==40,
 'main_idle70_no_owned_active_combat':q.scalars(q.block(q.block(afl['33555034'],'movement_manager'),'coordinate'))=={'x':71.77801,'y':-4.01341,'origin':70} and not q.block(afl['33555034'],'current_order').strip() and all(not q.block(q.block(afl[str(i)],'combat'),'in_combat_with').strip() for i in own),
 'enemy_main_and_station_none_science_still_present':q.scalars(ar['fleet']).get('33555206')=='none' and q.scalars(ar['fleet']).get('779')=='none' and '16777613' in afl,
 'native_menace90_objective90_level1':D(str(bc['effective_stockpile'].get('menace',0)))==0 and ac['effective_stockpile']['menace']==90 and q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and q.scalars(q.block(q.block(acr,'crisis_progression'),'objective'))=={'objective':'crisobj_destroy_enemy_ships','progress':90},
 'same_prepaid_forge_only_progress252':omit(bi,{'progress'})==omit(ai,{'progress'}) and q.scalars(ai)['progress']==252,
 'all_original_mother_buildings_zones_districts_held':all(bz[i]==az[i] for i in ['0','2','61']) and all(bb[str(i)]==ab[str(i)] for zid in ['0','2','61'] for i in q.ids(q.block(az[zid],'buildings'))) and all(q.block(br['districts'],i)==q.block(ar['districts'],i) for i in ['1','2','3']),
 'all_native_expected_workers_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2400),('technician_drone',1200)]),
 'exact_five_new_survey_holders_no_removal':len(bh)==273 and len(ah)==278 and set(bh)<=set(ah) and newholders==[('0',str(i)) for i in [908,909,910,911,912]],
 'science1_alive_same_leader_in80_survey913_progress8_05':q.ids(q.block(afl['1'],'ships'))==[1] and q.scalars(ash['1'])['hitpoints']==375 and q.scalars(ash['1'])['leader']==150994969 and q.scalars(q.block(q.block(afl['1'],'movement_manager'),'coordinate'))['origin']==80 and q.scalars(q.block(q.block(afl['1'],'current_order'),'survey_planet_order'))['progress']==8.05 and q.scalars(q.block(q.block(q.block(afl['1'],'current_order'),'survey_planet_order'),'deposit_holder'))=={'type':0,'id':913},
 'constructor_safely_halted171_raw_held':bfl['2']==afl['2'],
 'population10352_last_month10346_plus6':a['colonies']['0']['actual_pop_sum']==10352 and q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':10346,'growth':6},
 'EEP_species_targets_fullpsi_held_no_EEP_task':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and b['species']==a['species'] and b['event_targets']==a['event_targets'] and a['planets']['7']['modifiers']==b['planets']['7']['modifiers'] and ac['owned_colonies']==[0] and not a['situations'],
 'exact_marauder3_pending227':pending==[{'id':227,'event':'marauder.3','date':'2265.08.18','country':0}],
 'actual_positive_nets_recorded_not_attributed_to_forge':nets=={'energy':D('36.265'),'minerals':D('30.8035'),'unity':D('149.88550'),'alloys':D('0.32')},
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
checks={k:bool(v) for k,v in checks.items()};p={'status':'PASS_TERRAVORE_NATIVE_DRONE_BATTLE_AND_ONGOING_FORGE_SURVEY_OBSERVATION' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_lost_ship_ids':lost,'actual_survivor_ids':survivors,'actual_native_menace':90,'native_battle_counts':{side:counts(side) for side in ['fleets','enemy']},'actual_new_survey_holders':newholders,'current_month_nets':{k:str(v) for k,v in nets.items()},'calendar_ready':False,'scope':'Native victory with9 paid losses and90 menace, forge252/360 and5/14 new surveys. Marauder227 pending. No six independent monthly ledgers, construction completion, level2, outpost or full-route acceptance.'}
out=run/(after+'-battle-forge-survey-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original battle observation FAIL retained'
