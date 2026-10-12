"""Independent original-game source and exact battle/decade instance review."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
stage='terravore-rear188-battle-source-review';after='terravore-rear188-campaign-22800101'
o=load(after+'-construction-boundary-observation-v4.json');b,a=o['before_state'],o['after_state'];old=load(after+'-campaign-v4-proof.json');ox=load(after+'-campaign-guard-v4-execution.json')
with zipfile.ZipFile(run/(after+'.sav')) as z:roots={k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
enemy=q.block(roots['country'],'1');enemyids=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(enemy,'fleets_manager'),'owned_fleets'))))
removed=set(b['owned_ship_ids'])-set(a['owned_ship_ids']);transfers=[]
for i in removed:
 before=b['owned_ships_raw'][str(i)];later=q.block(roots['ships'],str(i));bs,as_=[q.scalars(s) for s in [before,later]]
 transfers.append({'ship':i,'before_raw':before,'after_raw':later,'valid':bs['fleet']==as_['fleet'] in enemyids and as_['construction_date']==bs['construction_date'] and q.scalars(q.block(later,'coordinate'))['origin']==188 and as_['hitpoints']>0})
sources=[];game=Path('C:/SteamLibrary/steamapps/common/Stellaris')
for rel in ['events/paragon_events.txt','common/on_actions/00_on_actions.txt','common/defines/00_defines.txt','localisation/simp_chinese/messages_l_simp_chinese.yml','common/crisis_objectives/00_crisis_objectives.txt']:
 src=game/rel;dest=run/('terravore-rear188-native-'+src.name);assert not dest.exists();shutil.copyfile(src,dest);sources.append({'path':str(src),'preserved':dest.name,'sha256':h.sha256(src)})
texts={Path(s['path']).name:Path(s['path']).read_text(encoding='utf-8-sig') for s in sources}
events={q.scalars(v).get('id'):v for k,v,x in q.fields(texts['paragon_events.txt']) if k=='country_event' and x}
ds=[v for k,v,x in q.fields(q.block(q.block(a['country0_raw'],'modules'),'standard_event_module')) if k=='delayed_event' and x and q.scalars(v).get('event')=='paragon.999']
msg=o['new_country0_messages_raw'];combat=[v for v in msg if q.scalars(v).get('type')=='COMBAT_STATS'];leader=[v for v in msg if q.scalars(v).get('type')=='LEADER_POOL_REFRESHED_MESSAGE_TYPE']
checks={
 'original17_only_three_FAIL_actual1_source_preserved':len(old['checks'])==17 and {k for k,v in old['checks'].items() if v is not True}=={'existing_original_ships_designs_alive_no_removal_or_revival','only_documented_zero_loss_native_route_reports_and_real_storm_visibility','known_pirate_delay_only_no_birth'} and ox['returncode']==1 and ox['helper_sha256']==h.sha256(Path(ox['command'][1])),
 'four_existing188_stations_transferred_country1_not_destroyed':removed=={67110520,50333076,50332983,50333335} and all(v['valid'] for v in transfers) and not set(a['owned_ship_ids'])-set(b['owned_ship_ids']),
 'actual_disabled_outpost_report_native188':len(combat)==1 and q.scalars(q.block(combat[0],'combat_stats'))['reason']=='we_disabled' and q.scalars(combat[0])['date']=='2279.12.09' and q.scalars(q.block(combat[0],'coordinate'))['origin']==188 and 'fleet=33555300' in combat[0] and 'fleet=825' in combat[0],
 'decade_source_on_action998_schedules999_native164':len(ds)==1 and q.scalars(ds[0])=={'event':'paragon.999','days':164} and q.scalars(q.block(ds[0],'scope'))['id']==0 and q.scalars(q.block(ds[0],'scope'))['type']=='country' and re.search(r'id\s*=\s*paragon\.999\s+days\s*=\s*1\s+random\s*=\s*1800',q.block(events['paragon.998'],'immediate')) is not None and 'paragon.998' in q.block(q.block(texts['00_on_actions.txt'],'on_decade_pulse_country'),'events') and a['audit']['date']=='2280.01.01',
 'native_five_year_pool_message_owned_leaders_held':len(leader)==1 and q.scalars(leader[0]).get('message_type')=='leader_pool' and q.scalars(leader[0]).get('localization')=='LEADER_POOL_REFRESHED_TITLE' and 'LEADER_POOL_REFRESH_TIME = 1800' in texts['00_defines.txt'] and 'LEADER_POOL_REFRESHED_TITLE:' in texts['messages_l_simp_chinese.yml'] and q.block(b['country0_raw'],'owned_leaders')==q.block(a['country0_raw'],'owned_leaders'),
 'all_other14_original_business_checks_PASS':all(v is True for k,v in old['checks'].items() if k not in {'existing_original_ships_designs_alive_no_removal_or_revival','only_documented_zero_loss_native_route_reports_and_real_storm_visibility','known_pirate_delay_only_no_birth'}),
 'original_source_copies_SHA_equal':all(h.sha256(Path(s['path']))==h.sha256(run/s['preserved'])==s['sha256'] for s in sources),
}
passed=all(v is True for v in checks.values());out=run/(stage+'.json');assert not out.exists()
h.write_json(out,{'status':'PASS_ORIGINAL_NATIVE_BATTLE_AND_DECADE_SOURCE' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'transfers':transfers,'combat_message_original':combat,'leader_message_original':leader,'paragon999_delay_original':ds,'sources':sources,'scope':'Exact observed native station defeat and native decade/pool refresh; no production mod defect confirmed and no general event whitelist.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
