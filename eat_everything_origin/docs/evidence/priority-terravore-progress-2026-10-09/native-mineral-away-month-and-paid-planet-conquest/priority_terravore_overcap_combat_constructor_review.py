"""Four native days: known military battle and original constructor return."""
import json,logging,re,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-six-mineral-build-22800313';stage='terravore-overcap-combat-constructor-review'
pre=load(before+'-campaign-v8-proof.json');px=load(before+'-campaign-guard-v8-execution.json');a=load(before+'-construction-boundary-observation-v4.json')['after_state']
with zipfile.ZipFile(run/(before+'.sav')) as z:roots={k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
fleets={k:v for k,v,x in q.fields(roots['fleet']) if x};ships={k:v for k,v,x in q.fields(roots['ships']) if x};main=fleets['83886903'];enemy=fleets['825'];constructor=fleets['2']
active=[i for i,raw in a['owned_fleets_raw'].items() if re.search(r'\bfleet\s*=',q.block(q.block(raw,'combat'),'in_combat_with'))]
enemyowned=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(roots['country'],'1'),'fleets_manager'),'owned_fleets'))))
delays=[q.scalars(v) for k,v,x in q.fields(q.block(q.block(a['country0_raw'],'modules'),'standard_event_module')) if k=='delayed_event' and x]
checks={
 'prior24_PASS_actual0_source_SAV':len(pre['checks'])==24 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'exact_three_reviewed_boundaries':set(pre['boundaries'])=={'original_native_naval_overcapacity_review','native_active_combat_review','original_native_MIA_return_review'} and a['audit']['date']=='2280.03.13',
 'known_main18_vs_enemy825_five_in146':active==['83886903'] and len(q.ids(q.block(main,'ships')))==18 and q.scalars(q.block(q.block(main,'combat'),'coordinate'))['origin']==146 and list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(main,'combat'),'in_combat_with'))))==[825] and 825 in enemyowned and set(q.ids(q.block(enemy,'ships')))=={16779110,33556025,67109342,16779083,33556209} and all(q.scalars(ships[str(i)])['hitpoints']>0 for i in q.ids(q.block(main,'ships'))+q.ids(q.block(enemy,'ships'))),
 'seven_genuinely_paid_mineral_ships_actual133_naval':pre['mineral_ship_count']==7 and a['audit']['countries']['0']['native']['used_naval_capacity']==133 and len(q.ids(q.block(fleets['50332250'],'ships')))==7 and not pre['completed_paid_army_orders'],
 'original_constructor2_MIA_date0316_only':q.ids(q.block(constructor,'ships'))==[2] and q.scalars(constructor)['return_date']=='2280.03.16' and q.scalars(q.block(constructor,'properties'))['mia']=='yes' and q.scalars(ships['2'])['fleet']==2 and q.scalars(fleets['33555278'])['return_date']=='2281.06.27',
 'three_transports_safe0_no_unknown_near_delay':set(q.ids(q.block(fleets['16778104'],'ships')))=={100664961,50333234,16777713} and q.scalars(q.block(q.block(fleets['16778104'],'movement_manager'),'coordinate'))['origin']==0 and all(s.get('event')=='pirate.6' or s.get('days',0)>4 for s in delays),
 'CN_no_pending_error_exact_held':m['language']=='l_simp_chinese' and not a['pending_country0_raw'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'start_date':'2280.03.13','end_date':'2280.03.17','days':4,'maximum_days':4,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'main_fleet_raw':main,'enemy_fleet_raw':enemy,'constructor_fleet_raw':constructor,'constructor_ship_raw':ships['2'],'scope':'Only observe four actual days. No victory, returned state, resources, monthly overcapacity fees or Menace pre-approved.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
