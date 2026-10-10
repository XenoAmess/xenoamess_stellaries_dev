"""Exact same-day native homicidal caravan exit, no economic effects."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-route-drone-travel150';after='terravore-caravan-homicide-acked'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after)
pre=json.loads((run/(before+'-travel150-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
def selection(v):return re.findall(r'\{\s*player_event=(\d+)\s+human=(-?\d+)\s+option=(\d+)\s*\}',q.block(v,'selected'))
def retained(fs):return [(k,v,o) for k,v,o in fs if k!='open_player_event_selection_history' and not(k=='player_event' and o and q.scalars(v).get('id')==224) and not(k=='message' and o and q.scalars(v).get('event')==224)]
checks={
 'same_date_original_SHA_pair':a['date']==b['date']=='2263.04.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior29_travel_observation_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_PAID_SHIP_COMPLETION_AND_TRAVEL150_OBSERVATION' and len(pre['checks'])==29 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and pre['calendar_ready'] is False and ex['returncode']==0 and ex['helper_sha256']=='74be8f23dca18103598f7f6e7827d256ceb1d673c4a61d082c9946e117dba9f9',
 'all_other_ordered_top_raw_held':retained(bf)==retained(af),
 'unique224_cara2020_removed':len([v for k,v,o in bf if k=='player_event' and o and q.scalars(v).get('id')==224 and q.scalars(v).get('event')=='cara.2020' and q.scalars(v).get('country')==0])==1 and not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('id')==224],
 'only_event224_message_removed':len([v for k,v,o in bf if k=='message' and o and q.scalars(v).get('event')==224])==1 and not[v for k,v,o in af if k=='message' and o and q.scalars(v).get('event')==224],
 'only_exact_native_choice3_human1_appended':selection(ar['open_player_event_selection_history'])==selection(br['open_player_event_selection_history'])+[('224','1','3')],
 'all_countries_economy_research_EEP_raw_held':br['country']==ar['country'] and a['countries']==b['countries'],
 'all_ships_fleets_construction_planets_pop_species_raw_held':all(br[k]==ar[k] for k in ['ships','fleet','construction','planets','colony','pop_jobs','pop_groups','species']),
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'native_caravan_source_SHA_bound':h.sha256(Path('C:/SteamLibrary/steamapps/common/Stellaris/events/caravaneer_events.txt'))=='2d14f409322d493271577c7bc2a7c3fd679f7022cc1a9b96b16729cf52d74c8d',
 'normal_click_and_save_actual_exit0':all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-caravan-homicide-exit-click',after+'-save']) and json.loads((run/'terravore-caravan-homicide-exit-click.action.json').read_text('utf-8'))['client_point']==[692,462],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
p={'status':'PASS_TERRAVORE_NATIVE_CARAVAN_HOMICIDAL_EXIT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':all(checks.values()),'scope':'Only normal empty-effect native choice3 clears caravan224. No economic benefit, crisis upgrade or full-route claim.'}
out=run/(after+'-caravan-ack-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original caravan ACK FAIL retained'
