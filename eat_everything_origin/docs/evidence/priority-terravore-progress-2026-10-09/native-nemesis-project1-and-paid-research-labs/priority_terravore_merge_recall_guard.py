"""Same-day actual 12-corvette merge and normal return-to-starbase0 order."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));rt={k:v for k,v,o in fs if o};return a,fs,rt,{k:v for k,v,o in q.fields(rt['ships']) if o}
def owned(rt):return [int(x) for x in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))]
b,bf,br,bsh=read(before);a,af,ar,ash=read(after);bc,ac=b['countries']['0'],a['countries']['0'];pre=json.loads((run/(before+'-native-combat-boundary-proof.json')).read_text('utf-8'))
bs=[i for fid in [16777797,593,598] for i in q.ids(q.block(q.block(br['fleet'],str(fid)),'ships'))];fleet=q.block(ar['fleet'],'16777797');ass=q.ids(q.block(fleet,'ships'));order=q.block(q.block(fleet,'current_order'),'return_fleet_order')
checks={
 'same_actual_date':b['date']==a['date']=='2237.07.02',
 'bound_original21_PASS_actual_exit0':pre['status']=='PASS_NATIVE_TERRAVORE_COMBAT_BOUNDARY_COMPONENT' and len(pre['checks'])==21 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))['returncode']==0,
 'exact_original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'original12_owned_ships_all_merged_no_duplicate':len(bs)==len(ass)==len(set(ass))==12 and set(bs)==set(ass),
 'only_original593_598_owned_references_removed':owned(ar)==[i for i in owned(br) if i not in [593,598]] and 16777797 in owned(ar),
 'old_two_fleets_no_actual_ships_and_shipclass_none':all(not q.ids(q.block(f:=q.block(ar['fleet'],str(i)),'ships')) and q.scalars(f)['ship_class']=='none' and q.scalars(f)['military_power']==0 for i in [593,598]),
 'all12_same_real_design_dates_hull_shields_armor':all(q.scalars(ash[str(i)])['fleet']==16777797 and q.block(bsh[str(i)],'ship_design_implementation')==q.block(ash[str(i)],'ship_design_implementation') and all(q.scalars(bsh[str(i)])[k]==q.scalars(ash[str(i)])[k] for k in ['construction_date','hitpoints','max_hitpoints','shield_hitpoints','armor_hitpoints']) for i in ass),
 'original_entire_paid_construction_raw_held':br['construction']==ar['construction'],
 'actual_naval60_held':q.scalars(q.block(br['country'],'0'))['fleet_size']==q.scalars(q.block(ar['country'],'0'))['fleet_size']==60,
 'real_return_home_order_targets_original_starbase0':q.scalars(order)['home_base']=='yes' and q.scalars(q.block(q.block(q.block(order,'sub_order'),'orbit_planet_order'),'orbitable'))['starbase']==0 and q.scalars(q.block(q.block(fleet,'movement_manager'),'target_coordinate'))=={'x':19.61,'y':-21.61,'origin':0},
 'no_active_native_enemy_combat':not q.block(q.block(fleet,'combat'),'in_combat_with'),
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['effective_stockpile','budget_categories','variables','flags','government','traditions','ascension_perks','tech_status']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TWELVE_SHIPS_MERGED_RETURN_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual12_ships':ass,'native_return_order_raw':order,'scope':'Same-day normal merge and return order only. No resource/pop/research changes. Arrival, repairs, upkeep and full-route acceptance still pending.'}
out=run/(after+'-merge-recall-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original merge/return FAIL retained'
