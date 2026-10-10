"""Exact native marauder3 contact transitions only to marauder15."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-drone-survey-forge180';after='terravore-marauder15-opened'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after);pre=json.loads((run/(before+'-battle-forge-survey-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
pending=lambda fs:[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
bp,ap=pending(bf),pending(af);assert len(bp)==len(ap)==1
bs,ass=[q.block(v,'scope') for v in [bp[0],ap[0]]];parent=q.block(ass,'from')
def retained(fs):return [(k,v,o) for k,v,o in fs if k not in {'last_event_id','open_player_event_selection_history'} and not(k=='player_event' and o and q.scalars(v).get('id') in [227,230]) and not(k=='message' and o and q.scalars(v).get('event') in [227,230])]
sel=lambda v:re.findall(r'\{\s*player_event=(\d+)\s+human=(-?\d+)\s+option=(\d+)\s*\}',q.block(v,'selected'))
tok=lambda v:[x for x,s,e in q.tokens(v)]
source=Path('C:/SteamLibrary/steamapps/common/Stellaris/events/marauder_events.txt')
checks={
 'same_date_original_SHA_pair':b['date']==a['date']=='2263.11.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior21_battle_observation_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_NATIVE_DRONE_BATTLE_AND_ONGOING_FORGE_SURVEY_OBSERVATION' and len(pre['checks'])==21 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='65220987080cc69b90061b9e3279e272d57f70cdb8dfa96e1fd16f9b276b6703',
 'all_other_ordered_top_raw_held':retained(bf)==retained(af),
 'exact227_marauder3_to230_marauder15':q.scalars(bp[0])=={'id':227,'event':'marauder.3','date':'2265.08.18','country':0} and q.scalars(ap[0])=={'id':230,'event':'marauder.15','date':'2266.02.17','country':0},
 'only_original_choice227_option0_appended':sel(ar['open_player_event_selection_history'])==sel(br['open_player_event_selection_history'])+[('227','1','0')],
 'last_event_counter229_to230':[(v,o) for k,v,o in bf if k=='last_event_id']==[('229',False)] and [(v,o) for k,v,o in af if k=='last_event_id']==[('230',False)],
 'new_scope_same_country0_and_original_from9_targets':q.scalars(ass)==q.scalars(parent)=={'type':'country','id':0,'opener_id':4294967295,'random_allowed':'yes'} and tok(q.block(parent,'from'))==tok(q.block(bs,'from')) and q.scalars(q.block(q.block(parent,'from'),'saved_event_target'))['id']==9,
 'exact_native_scope_randoms':q.ids(q.block(bs,'random'))==[0,2620921191] and q.ids(q.block(parent,'random'))==[0,2620921192] and q.ids(q.block(ass,'random'))==[0,3946207847],
 'matching_native_message_replaced':len([v for k,v,o in bf if k=='message' and o and q.scalars(v).get('event')==227])==1 and len([v for k,v,o in af if k=='message' and o and q.scalars(v).get('event')==230 and q.scalars(v).get('date')=='2263.11.17' and q.scalars(v).get('receiver')==0])==1,
 'all_countries_economy_fleets_forge_raw_held':all(br[k]==ar[k] for k in ['country','fleet','ships','construction','planets','colony','pop_jobs','pop_groups','species_db']),
 'native_source_SHA_bound':h.sha256(source)=='a64e4e59b1ddeb93729135fff1411d9543bb1ac3291d593a5c7fe748d1d51bf3',
 'normal_click_and_save_actual_exit0':all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-marauder3-contact-click',after+'-save']) and json.loads((run/'terravore-marauder3-contact-click.action.json').read_text('utf-8'))['client_point']==[509,544],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
p={'status':'PASS_TERRAVORE_NATIVE_MARAUDER_CONTACT_CHAIN_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_pending':q.scalars(ap[0]),'calendar_ready':False,'scope':'Only normal native227 contact opens230 introduction. All other ordered top held; no economy or crisis reward. Introduction pending.'}
out=run/(after+'-marauder-contact-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original contact FAIL retained'
