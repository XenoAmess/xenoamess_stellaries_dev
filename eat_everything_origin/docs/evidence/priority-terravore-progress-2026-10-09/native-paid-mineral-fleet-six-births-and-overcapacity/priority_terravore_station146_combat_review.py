"""One independently reviewed 30-day native rear station battle interval."""
import json,logging,re,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-six-mineral-build-22800201';stage='terravore-station146-combat-interval-review'
pre=load(before+'-campaign-v7-proof.json');px=load(before+'-campaign-guard-v7-execution.json');au=load(before+'.audit.json')
with zipfile.ZipFile(run/(before+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
roots={k:v for k,v,x in fs if x};country=q.block(roots['country'],'0');enemycountry=q.block(roots['country'],'1')
owned=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(country,'fleets_manager'),'owned_fleets'))))
enemyowned=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(enemycountry,'fleets_manager'),'owned_fleets'))))
fleets={k:v for k,v,x in q.fields(roots['fleet']) if x};ships={k:v for k,v,x in q.fields(roots['ships']) if x}
active=[i for i in owned if re.search(r'\bfleet\s*=',q.block(q.block(fleets[str(i)],'combat'),'in_combat_with'))]
station=fleets['67109697'];enemy=fleets['825'];main=fleets['83886903'];combat=q.block(station,'combat')
enemyships=q.ids(q.block(enemy,'ships'));ourship=ships['1882'];ss=q.scalars(ourship)
checks={
 'prior23_PASS_actual0_source_SAV':len(pre['checks'])==23 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==au['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_actual_station146_station_active_boundary':pre['boundaries']==['native_active_combat_review'] and active==[67109697] and q.scalars(q.block(combat,'coordinate')).get('origin')==146 and list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(combat,'in_combat_with'))))==[825] and q.ids(q.block(station,'ships'))==[1882] and ss['hitpoints']>0,
 'known_enemy5_native_country1_military_all_alive':825 in enemyowned and q.scalars(enemy)['ship_class']=='shipclass_military' and set(enemyships)=={16779110,33556025,67109342,16779083,33556209} and all(q.scalars(ships[str(i)])['hitpoints']>0 and q.scalars(ships[str(i)])['construction_date']<au['date'] for i in enemyships),
 'main18_reinforcement_actual96_target188':len(q.ids(q.block(main,'ships')))==18 and q.scalars(q.block(q.block(main,'movement_manager'),'coordinate'))['origin']==96 and q.scalars(q.block(q.block(main,'movement_manager'),'target_coordinate'))['origin']==188 and q.scalars(main)['hit_points']==4860,
 'three_paid_transports_safe_mother0':set(q.ids(q.block(fleets['16778104'],'ships')))=={100664961,50333234,16777713} and q.scalars(q.block(q.block(fleets['16778104'],'movement_manager'),'coordinate'))['origin']==0 and all(q.scalars(ships[str(i)])['hitpoints']>0 for i in [100664961,50333234,16777713]),
 'native_war_no_pending_no_MIA_crossing':bool(q.block(roots['war'],'1')) and au['date']=='2280.02.01' and not any(k=='player_event' and x and q.scalars(v).get('country')==0 for k,v,x in fs) and q.scalars(fleets['2'])['return_date']=='2280.03.16',
 'reviewed_error_exact_held':h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':au['save_sha256'],'after_sha256':au['save_sha256'],'start_date':au['date'],'end_date':'2280.03.01','days':30,'maximum_days':30,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'station_fleet_raw':station,'station_ship_raw':ourship,'enemy_fleet_raw':enemy,'enemy_ships_raw':{str(i):ships[str(i)] for i in enemyships},'scope':'One actual native station battle interval. No victory/loss/Menace outcome pre-approved; original resulting reports require business checks.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
