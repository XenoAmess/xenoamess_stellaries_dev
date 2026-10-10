"""Actual native capital object replacement; pending notices explicitly remain."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-ascension-capital-resumed';after='terravore-ascension-capital-complete';readj=lambda p:json.loads(p.read_text('utf-8'))
def read(st):
 a=readj(run/(st+'.audit.json'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after);old=readj(run/(after+'-capital-completion-proof.json'));omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
bz,az=[q.block(rt['zones'],'0') for rt in [br,ar]];bi,ai=[q.ids(q.block(z,'buildings')) for z in [bz,az]];pending=[(q.scalars(v)['id'],q.scalars(v)['event']) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
checks={'original32_exact_four_FAIL_other28_true':old['status']=='FAIL' and len(old['checks'])==32 and [k for k,v in old['checks'].items() if v is not True]==['no_country0_pending','all_mother_zones_raw_held','same_native_capital0_type_upgraded_other_fields_held','all_other_actual_mother_buildings_raw_held'] and readj(run/(after+'-guard-execution.json'))['returncode']==1,
 'original_SHA_pair_calendar_exit0':h.sha256(run/(before+'.sav'))==old['before_sha256']==b['save_sha256'] and h.sha256(run/(after+'.sav'))==old['after_sha256']==a['save_sha256'] and readj(run/(after+'-observe-execution.json'))['returncode']==0,
 'exact_native_capital_old0_none_new33554466':[(v,o) for k,v,o in q.fields(ar['buildings']) if k=='0']==[('none',False)] and q.scalars(q.block(br['buildings'],'0'))=={'type':'building_hive_capital','position':0} and q.scalars(q.block(ar['buildings'],'33554466'))=={'type':'building_hive_major_capital','position':0},
 'zone0_only_first_capital_reference_replaced':bi==[0,1,2,45,46,48] and ai==[33554466]+bi[1:] and omit(bz,{'buildings'})==omit(az,{'buildings'}),
 'all_other_mother_buildings_and_zone2_3_raw_held':all(q.block(br['buildings'],str(i))==q.block(ar['buildings'],str(i)) for i in [1,2,45,46,48,38,16777251,41]) and all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['2','3']),
 'exact_five_native_notices_remain':pending==[(137,'tutorial.63'),(135,'tutorial.63'),(136,'action.13'),(138,'cara.3020'),(139,'apoc.5')],
 'native_coordinator_and_logistics_real_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('coordinator',1500),('logistics_drone',500)]),
 'actual_building_energy_upkeep18_9':a['countries']['0']['budget_categories']['current_month']['expenses']['planet_buildings']['energy']==18.9}
p={'status':'PASS_NATIVE_CAPITAL_NEW_OBJECT_COMPONENT_PENDING_NOTICES' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'native_pending':pending,'scope':'Original28 valid construction checks plus exact native replacement of capital object and unchanged other mother buildings. Five native notices remain. No calendar/complete-month/full-route clearance.'};out=run/(after+'-capital-new-object-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original new-object supplement FAIL retained'
