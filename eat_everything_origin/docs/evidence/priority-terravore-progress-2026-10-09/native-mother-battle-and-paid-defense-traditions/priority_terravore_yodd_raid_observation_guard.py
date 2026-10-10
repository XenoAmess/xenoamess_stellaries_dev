"""Exact investigation of the retained failed transit boundary; NOT calendar clearance."""
import hashlib,json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-yodd-survey-ordered';after='terravore-yodd-transit-year1'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after)
pfile=after+'-yodd-transit-boundary-proof.json';p=json.loads((run/pfile).read_text('utf-8'))
failed={'no_country0_pending_after_full_breach','mother_no_new_bombardment_or_population_loss','one_psi_native_slot3_replaces45','all_other_actual_mother_buildings_raw_held','actual_coordinator2000_logistics500_telepath200_full','first_native_survey_order1083_only_movement_suborder_changes','all9_queued_survey_orders_raw_held'}
checks={
 'original_53_exact_7_FAIL_46_true_and_exit1':p['status']=='FAIL' and len(p['checks'])==53 and {k for k,v in p['checks'].items() if v is False}==failed and all(v is True for k,v in p['checks'].items() if k not in failed) and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==1,
 'original_transit_guard_immutable':h.sha256(run/'priority_terravore_yodd_transit_guard.py')==h.sha256(Path('_runtime/heart-of-devouring/priority_terravore_yodd_transit_guard.py'))=='ac1a0ad83ac33600807f183246ff81e4adfaa0661227490c69433f4b7f8a3342',
 'original_SHA_pair_exact':p['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav'))=='8b04fb45d304d067f4eda6c1d9ddd974c34857f026959606885b9f211e6f1054' and p['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav'))=='1703afb5959528e6f8a2b447f3bc690aeb0e5ca72c9eb71931a6c54954fba109',
 'unique_actual_date_and_population':b['date']=='2260.07.02' and a['date']=='2261.07.02' and b['colonies']['0']['actual_pop_sum']==10101 and a['colonies']['0']['actual_pop_sum']==10177,
}
bc,ac=[q.block(rt['country'],'0') for rt in [br,ar]]
pending=[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
checks['exact_three_original_native_pending']= [(q.scalars(v)['id'],q.scalars(v)['event']) for v in pending]==[(211,'first_contact.1'),(213,'paragon.571'),(214,'first_contact.1')]
checks['exact_native_event_scopes']=all(q.scalars(q.block(v,'scope')).get('type')==ty and q.scalars(q.block(v,'scope')).get('id')==i for v,ty,i in zip(pending,['first_contact','country','first_contact'],[51,0,16777263])) and q.scalars(q.block(q.block(pending[1],'scope'),'from'))=={'type':'leader','id':150995190,'opener_id':4294967295,'random_allowed':'yes'}
bb,ab=[{k:v for k,v,o in q.fields(rt['buildings'])} for rt in [br,ar]]
omit=lambda v,ks:[(k,x,o) for k,x,o in q.fields(v) if k not in ks]
checks['only_mother_node83_new_ruined_exact']=q.scalars(bb['83'])=={'type':'building_hive_node','position':0} and q.scalars(ab['83'])=={'type':'building_hive_node','ruined':'yes','position':0} and omit(ab['83'],{'ruined'})==list(q.fields(bb['83']))
mother_ids=[str(i) for zid in ['0','2','61'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))]
checks['all_other_actual_mother_buildings_raw_held']=all(ab.get(i)==bb.get(i) for i in mother_ids if i!='83')
checks['actual_psi33554454_exact_raw_held']=ab['33554454']==bb['33554454'] and q.scalars(ab['33554454'])=={'type':'building_psi_corps','position':3}
checks['three_paid_labs_same_raw_slots']=q.ids(q.block(q.block(ar['zones'],'2'),'buildings'))==[16777251,83886120,16777323] and all(ab[str(i)]==bb[str(i)] and q.scalars(ab[str(i)])=={'type':'building_research_lab_1','position':pos} for pos,i in enumerate([16777251,83886120,16777323]))
def job(kind):
 js=[v for v in a['pop_jobs'].values() if v['planet']==0 and v['type']==kind];assert len(js)==1;return js[0]
checks['exact_native_ruin_coordinator1800_others_full']=all(job(k)['workforce']==job(k)['max_workforce']==n for k,n in [('coordinator',1800),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2000),('technician_drone',1200)])
core=a['planets']['7']
checks['exact_actual_bombardment_state']=core['last_bombardment']=='2261.07.02' and core['bombardment_damage']==11.54032
enemy=q.block(ar['fleet'],'18');worm=q.block(ar['ships'],'44');epos=q.scalars(q.block(q.block(enemy,'movement_manager'),'coordinate'))
checks['actual_enemy18_ship44_in_home_alive']=q.ids(q.block(enemy,'ships'))==[44] and q.scalars(enemy)['bombardment_stance']=='voidworm_invasion' and q.scalars(worm)['fleet']==18 and q.scalars(worm)['hitpoints']==12000 and epos['origin']==0
checks['nineteen_paid_ships_no_actual_losses']=p['actual_lost_ship_ids_requires_native_combat_review']==[] and sum(len(v) for v in p['actual_owned_military_fleets'].values())==19
science=q.block(ar['fleet'],'1');current=q.block(q.block(science,'current_order'),'survey_planet_order');cs=q.scalars(current)
checks['original_science1_actual_arrived97_alive']=q.ids(q.block(science,'ships'))==[1] and q.scalars(q.block(q.block(science,'movement_manager'),'coordinate'))['origin']==97 and q.scalars(q.block(ar['ships'],'1'))['leader']==150994969 and q.scalars(q.block(ar['ships'],'1'))['hitpoints']>0
checks['actual_current1078_progress10_35']=q.scalars(q.block(current,'deposit_holder'))=={'type':0,'id':1078} and cs=={'progress':10.35,'can_reach':'yes','order_id':40,'commissioner':4294967295}
orders=[v for k,v,o in q.fields(q.block(science,'order')) if k=='survey_planet_order' and o]
checks['exact_six_remaining_native_orders']=len(orders)==6 and all(q.scalars(q.block(v,'deposit_holder'))=={'type':0,'id':i} and q.scalars(v)=={'progress':0,'can_reach':'yes','order_id':orderid,'commissioner':4294967295} for v,i,orderid in zip(orders,[1079,1084,1085,1080,1082,2072],range(41,47)))
holders=lambda c:re.findall(r'\{\s*type=(\d+)\s+id=(\d+)\s*\}',q.block(c,'surveyed_deposit_holders'))
bh,ah=holders(bc),holders(ac)
checks['exact_three_native_survey_results_not_order_inference']=len(bh)==263 and len(ah)==266 and set(ah)-set(bh)=={('0',str(i)) for i in [1081,1083,1086]} and set(bh)<=set(ah)
checks['unfiltered_error2670_no_increment']=(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670
sources={}
for rel,sha in [('events/paragon_events.txt','5dc68cbce05d753590dba3d33d5d3e1c41ccaac7106a239c6cbc64f84dbccdc1'),('events/first_contact_events.txt','17e6402267e019f25b65a419cb2d8afd6666ebb362f9020e747c57551648ca46')]:
 path=h.GAME_EXE.parent/rel;sources[rel]={'path':str(path),'sha256':h.sha256(path)};checks['native_source_'+Path(rel).stem]=h.sha256(path)==sha
proof={'status':'PASS_TERRAVORE_NATIVE_RAID_OBSERVATION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'retained_failed_proof':{'file':pfile,'sha256':h.sha256(run/pfile),'failures':sorted(failed)},'actual_pending':[(q.scalars(v)['id'],q.scalars(v)['event']) for v in pending],'native_sources':sources,'scope':'Observed exact native raid, node83 ruin and three actual survey results. Does not clear pending, accept combat, assert no deaths, complete crisis, or clear calendar.'}
out=run/(after+'-raid-observation-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original raid observation FAIL retained'
