"""Exact 180-day supplement: 12 paid ships split by native combat, pending120 retained."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,list(q.fields(t)),{k:v for k,v,o in q.fields(t) if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def owned(rt):return [int(x) for x in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))]
b,bf,br=read(before);a,af,ar=read(after);old=json.loads((run/(after+'-defense-boundary-v2-proof.json')).read_text('utf-8'))
bs=q.ids(q.block(q.block(br['fleet'],'16777797'),'ships'));main=q.ids(q.block(q.block(ar['fleet'],'16777797'),'ships'));separate=q.ids(q.block(q.block(ar['fleet'],'593'),'ships'));ships=main+separate;new=[i for i in ships if i not in bs]
sb,sa=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]];pending=[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0];growth=q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'current_month_growth_details')
checks={
 'original23_exact_four_FAIL_retained':old['status']=='FAIL' and len(old['checks'])==23 and [k for k,v in old['checks'].items() if not v]==['original20_paid_batch_conserved','actual_two_paid_shipyards_crew_quarters_held','same_native_owned_fleet_set_and_naval_size','no_country0_pending'] and sum(v is True for v in old['checks'].values())==19 and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==1,
 'exact_original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256']==old['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==old['after_sha256'],
 'all12_original_paid_corvettes_and8_remaining_conserved':len(bs)==5 and len(main)==11 and separate==[16778402] and len(ships)==len(set(ships))==12 and len(new)==7 and len(old['remaining_paid_orders'])==8 and 12+8==20,
 'all_seven_new_original_design_dates_full_hull_native_fleets':all(q.scalars(s:=q.block(ar['ships'],str(i)))['fleet'] in [16777797,593] and q.scalars(s)['hitpoints']==q.scalars(s)['max_hitpoints']==250 and q.scalars(q.block(s,'ship_design_implementation'))['design']==67110548 and '2236.12.02'<q.scalars(s)['construction_date']<='2237.06.02' for i in new) and q.scalars(q.block(ar['ships'],'16778402'))['construction_date']=='2237.06.01',
 'owned_fleets_only_new593_and_total_naval60':set(owned(ar))-set(owned(br))=={593} and set(owned(br))<=set(owned(ar)) and q.scalars(q.block(ar['country'],'0'))['fleet_size']==60,
 'starbase_only_native_updateflag_and_departure':omit(sb,{'update_flag','orbitals'})==omit(sa,{'update_flag','orbitals'}) and q.scalars(sb).get('update_flag')==2048 and 'update_flag' not in q.scalars(sa) and q.scalars(q.block(sb,'orbitals'))=={'0':16777797,'1':4294967295,'2':4294967295} and q.scalars(q.block(sa,'orbitals'))=={'0':4294967295,'1':4294967295,'2':4294967295},
 'both_native_fleets_in_combat_with_same_nymphs':all(q.scalars(q.block(q.block(ar['fleet'],str(i)),'combat'))['start_date']==date and re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(ar['fleet'],str(i)),'combat'),'in_combat_with'))==['16777423'] for i,date in [(16777797,'2237.05.24'),(593,'2237.06.01')]),
 'sole_exact_native_pending120_contact33_country17':len(pending)==1 and q.scalars(pending[0])=={'id':120,'event':'first_contact.1','date':'2239.03.06','country':0} and q.scalars(q.block(pending[0],'scope'))['type']=='first_contact' and q.scalars(q.block(pending[0],'scope'))['id']==33 and q.scalars(c:=q.block(q.block(ar['first_contacts'],'contacts'),'33'))['owner']==0 and q.scalars(c)['country']==17 and q.scalars(q.block(c,'event'))['player_event']==120,
 'last_month_actual_bombardment_minus202_birth5':list(q.fields(growth))==[('key','"GROWTH_CAT_BOMBARDMENT"',False),('value','-202',False),('key','"GROWTH_CAT_GROWTH"',False),('value','5',False),('key','"GROWTH_CAT_PROMOTION"',False),('value','0',False)] and b['colonies']['0']['actual_pop_sum']==8935 and a['colonies']['0']['actual_pop_sum']==8551 and 'infected_by_voidworms' in a['planets']['7']['flags'],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_NATIVE_TWELVE_PAID_SHIPS_COMBAT_BOUNDARY_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual12_ship_ids':ships,'actual7_new_ship_ids':new,'native_pending120_requires_ACK':True,'original_FAIL_sha256':h.sha256(run/(after+'-defense-boundary-v2-proof.json')),'scope':'Original19 PASS plus exact four explanations. Actual native nymph combat and population loss disclosed. Pending120 not ACKed; no next calendar, victory or full-route claim.'}
out=run/(after+'-twelve-ships-combat-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original supplement FAIL retained'
