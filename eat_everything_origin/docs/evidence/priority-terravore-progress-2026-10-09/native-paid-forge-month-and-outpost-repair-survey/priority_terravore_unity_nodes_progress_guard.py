"""Native paid capital completion and actual jobs; original full logs retained."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after,expected_generator=sys.argv[1:];expected_generator=int(expected_generator);sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def obj(t):return {k:v for k,v,o in q.fields(t) if o}
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));rt={k:v for k,v,o in fs if o};return a,fs,rt,obj(rt['fleet']),obj(rt['ships'])
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def owned(rt):return [int(x) for x in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))]
def military(rt,fs):return {i:q.ids(q.block(fs[str(i)],'ships')) for i in owned(rt) if q.scalars(fs[str(i)])['ship_class']=='shipclass_military'}
def queue(rt):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),'3')
def items(rt):return obj(q.block(q.block(rt['construction'],'item_mgr'),'items'))
def progress(c):return q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])
b,bf,br,bfl,bsh=read(before);a,af,ar,afl,ash=read(after);bc,ac=b['countries']['0'],a['countries']['0']
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'));days=receipt['days'];validate_native_interval(b['date'],a['date'],days)
pre=json.loads((run/receipt['prior_proof_file']).read_text('utf-8'));ex=json.loads((run/(receipt['prior_execution_stage']+'-execution.json')).read_text('utf-8'))
bm,am=military(br,bfl),military(ar,afl);bs=[s for ss in bm.values() for s in ss];ass=[s for ss in am.values() for s in ss];new=[i for i in ass if i not in bs];lost=[i for i in bs if i not in ass]
bids,aids=[q.ids(q.block(queue(rt),'items')) for rt in [br,ar]];bi,ai=items(br),items(ar);removed=len(bids)-len(aids)
sb,sa=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]];core=a['planets']['7'];nets={k:sum(v.get(k,0) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys','trade']}
control=Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09/native-leader-trait-error-control')
cp=json.loads((control/'leader13-control-fleet-error-reproduction-proof.json').read_text('utf-8'));ce=json.loads((control/'leader13-control-fleet-error-guard-execution.json').read_text('utf-8'))
eb=(run/(after+'-error-before.log')).read_bytes();ea=(run/(after+'-error-after.log')).read_bytes();known=(control/'leader13-control-fleet-effect-error-after.log').read_bytes()[len((control/'leader13-control-fleet-effect-error-before.log').read_bytes()):];delta=ea[len(eb):];normalize=lambda v:re.sub(rb'\[\d{2}:\d{2}:\d{2}\]',b'[TIME]',v)
known_count=len(delta)//144;error_ok=eb==(run/(before+'-error-after.log')).read_bytes() and ea.startswith(eb) and len(known)==144 and len(delta)%144==0 and normalize(delta)==normalize(known)*known_count and cp['status']=='PASS_SCOPED_NO_MOD_LEADER13_ERROR_REPRODUCTION' and len(cp['checks'])==14 and all(cp['checks'].values()) and ce['returncode']==0 and all(h.sha256(Path(s['path']))==s['sha256'] for s in cp['native_sources'])
coord_control=Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09/native-coordinator-capital-payment-error-control')
ccp=json.loads((coord_control/'coordinator-control-paid-error-proof.json').read_text('utf-8'));cce=json.loads((coord_control/'coordinator-control-error-guard-execution.json').read_text('utf-8'))
ck=(coord_control/'coordinator-control-paid-error-after.log').read_bytes()[len((coord_control/'coordinator-control-paid-error-before.log').read_bytes()):]
base_control_valid=cp['status']=='PASS_SCOPED_NO_MOD_LEADER13_ERROR_REPRODUCTION' and len(cp['checks'])==14 and all(cp['checks'].values()) and ce['returncode']==0 and all(h.sha256(Path(v['path']))==v['sha256'] for v in cp['native_sources'])
coord_control_valid=ccp['status']=='PASS_SCOPED_NO_MOD_NATIVE_COORDINATOR_ERROR' and len(ccp['checks'])==33 and all(ccp['checks'].values()) and cce['returncode']==0 and h.sha256(Path(ccp['native_source']['path']))==ccp['native_source']['sha256']=='9469c178efbaa2d8e5bce43545ee6d5a184ee0e764336e85170795d0cc6820ad'
remaining=delta;known_count=0;coordinator_count=0;segments_valid=True
while remaining:
 if len(known)==144 and normalize(remaining[:144])==normalize(known):known_count+=1;remaining=remaining[144:]
 elif len(ck)==255 and normalize(remaining[:255])==normalize(ck):coordinator_count+=1;remaining=remaining[255:]
 else:segments_valid=False;break
error_ok=eb==(run/(before+'-error-after.log')).read_bytes() and ea.startswith(eb) and base_control_valid and coord_control_valid and segments_valid

checks={
 'bound_actual_prior_PASS_execution_zero':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_bounded_native_days_receipt_execution_zero':1<=days<=360 and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'paid_orders_contiguous_completion_other_fields_held':removed>=0 and aids==bids[removed:] and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) and 0<=q.scalars(ai[str(i)])['progress']<60 for i in aids),
 'actual_new_ships_equal_paid_completed_orders':len(new)==removed,
 'actual_all_owned_military_ship_relations_and_design':len(ass)==len(set(ass)) and all(q.scalars(ash[str(i)])['fleet']==fid and q.scalars(q.block(ash[str(i)],'ship_design_implementation'))['design']==67110548 and 0<q.scalars(ash[str(i)])['hitpoints']<=q.scalars(ash[str(i)])['max_hitpoints'] for fid,ss in am.items() for i in ss),
 'old_surviving_real_design_and_construction_dates_held':all(q.scalars(q.block(bsh[str(i)],'ship_design_implementation'))['design']==q.scalars(q.block(ash[str(i)],'ship_design_implementation'))['design'] and q.scalars(bsh[str(i)])['construction_date']==q.scalars(ash[str(i)])['construction_date'] for i in set(bs)&set(ass)),
 'total_naval_size_matches_all_actual_owned_corvettes':q.scalars(q.block(ar['country'],'0'))['fleet_size']==5*len(ass),
 'actual_native_shipyard_modules_and_crews_held':q.scalars(q.block(sb,'modules'))==q.scalars(q.block(sa,'modules'))=={'0':'shipyard','1':'shipyard'} and q.block(sb,'buildings')==q.block(sa,'buildings') and all(q.scalars(sb)[k]==q.scalars(sa)[k] for k in ['level','type','build_queue','shipyard_build_queue','station']),
 'EEP_ledger_and_country_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'unique_core_owned_capacity11_original_modifiers':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11 and b['planets']['7']['modifiers']==core['modifiers'],
 'both_sources_unowned_shattered_no_actual_pop':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned_no_active_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'government_core_and_AP_traditions_held':omit(bc['government'],{'council_agenda_progress','council_agenda_cooldowns'})==omit(ac['government'],{'council_agenda_progress','council_agenda_cooldowns'}) and bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'Theory_selected_not_regressed':all('tech_psionic_theory' not in c['completed_technologies'] and progress(c)['technology']=='tech_psionic_theory' for c in [bc,ac]) and progress(ac)['progress']>=progress(bc)['progress'],
 'true_banks_and_special_points_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints') and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'all_primary_actual_stocks_positive':all(ac['effective_stockpile'][k]>0 for k in nets),
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_errors_held_or_exact_known_native_leader13_only':error_ok,
}
def planet_queue(rt):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),'0')
levels=lambda v:{v['districts'][str(i)]['type']:v['districts'][str(i)]['level'] for i in v['colonies']['0']['districts']}
bl,al=levels(b),levels(a);bpo,apo=[q.ids(q.block(planet_queue(rt),'items')) for rt in [br,ar]]
checks['no_old_paid_ship_losses']=not lost
checks['no_actual_player_fleet_combat']=all(not q.block(q.block(afl[str(fid)],'combat'),'in_combat_with').strip() for fid in am)
checks['mother_no_new_bombardment_or_population_loss']=core['last_bombardment']==b['planets']['7']['last_bombardment']=='2237.05.19' and core['bombardment_damage']<=b['planets']['7']['bombardment_damage'] and a['colonies']['0']['actual_pop_sum']>=b['colonies']['0']['actual_pop_sum']
checks['exact_mother_districts_hive5_mining10_generator6']=al=={'district_hive':5,'district_mining':10,'district_generator':6} and bl=={'district_hive':5,'district_mining':10,'district_generator':6} and expected_generator==6
checks['actual_generator_and_mining_full_workers']=all(j['workforce']==j['max_workforce']==({'technician_drone':expected_generator*200,'mining_drone':2000}[j['type']]) for j in a['pop_jobs'].values() if j['planet']==0 and j['type'] in ['technician_drone','mining_drone'])
for k in ['species','event_targets']:checks[k+'_held']=b[k]==a[k]
def mother_buildings(rt,audit):
 zids=[str(z) for d in audit['colonies']['0']['districts'] for z in audit['districts'][str(d)]['zones'] if z!=4294967295]
 zones={i:q.block(rt['zones'],i) for i in zids}
 buildings={str(i):q.block(rt['buildings'],str(i)) for z in zones.values() for i in q.ids(q.block(z,'buildings'))}
 return zones,buildings
bz,bb=mother_buildings(br,b);az,ab=mother_buildings(ar,a)
bcaps=[i for i,v in bb.items() if q.scalars(v).get('position')==0 and q.scalars(v).get('type') in ['building_hive_capital','building_hive_major_capital']];acaps=[i for i,v in ab.items() if q.scalars(v).get('position')==0 and q.scalars(v).get('type') in ['building_hive_capital','building_hive_major_capital']];assert len(bcaps)==len(acaps)==1;bcid,acid=bcaps[0],acaps[0];bcap,acap=q.scalars(bb[bcid]),q.scalars(ab[acid])
bd,ad=q.block(br['districts'],'1'),q.block(ar['districts'],'1');bzids,azids=q.ids(q.block(bd,'zones')),q.ids(q.block(ad,'zones'));bzone,azone=bzids[2],azids[2];bzt,azt=q.scalars(bz[str(bzone)]).get('type'),q.scalars(az[str(azone)]).get('type')
bnids=q.ids(q.block(bz[str(bzone)],'buildings'));anids=q.ids(q.block(az[str(azone)],'buildings'));newbuild=set(ab)-set(bb);done=len(bpo)-len(apo)
def node_order(v):return q.scalars(v).get('progress_needed')==360 and q.scalars(v).get('paying_country')==q.scalars(v).get('queue')==0 and q.scalars(q.block(v,'resources'))=={'minerals':320} and q.scalars(q.block(v,'buildable_planet_building'))=={'building':'building_hive_node','planet':0,'zone':61}
checks['actual_paid_nodes_contiguous_completed_or_progressed']=done>=0 and apo==bpo[done:] and all(node_order(bi[str(i)]) for i in bpo) and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) and q.scalars(bi[str(i)])['progress']<=q.scalars(ai[str(i)])['progress']<360 for i in apo)
checks['only_zone61_native_nodes_added']=bzone==azone==61 and bzt==azt=='zone_unity' and len(anids)==len(bnids)+done<=3 and anids[:len(bnids)]==bnids and newbuild=={str(i) for i in anids[len(bnids):]} and len(newbuild)==done and all(q.scalars(ab[str(i)])=={'type':'building_hive_node','position':pos} for pos,i in enumerate(anids))
checks['all_mother_zone_relations_except_new_node_refs_held']=bzids==azids==[0,2,61] and bd==ad and all(bz[i]==az[i] for i in ['0','2']) and omit(bz['61'],{'buildings'})==omit(az['61'],{'buildings'})
checks['unique_native_capital_same_raw_held']=bcid==acid and acap.get('type')==bcap.get('type')=='building_hive_major_capital' and bb[bcid]==ab[acid]
checks['all_old_actual_mother_buildings_raw_held']=set(bb)<=set(ab) and all(ab[i]==v for i,v in bb.items())
def job(kind):
 js=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind];assert len(js)==1;return js[0]
checks['actual_coordinator_matches_completed_nodes_full']=job('coordinator')['workforce']==job('coordinator')['max_workforce']==2000+200*len(anids) and job('logistics_drone')['workforce']==job('logistics_drone')['max_workforce']==500
checks['before_coordinator_matches_existing_nodes_full']=len([j for j in b['pop_jobs'].values() if j['planet']==0 and j['type']=='coordinator' and j['workforce']==j['max_workforce']==2000+200*len(bnids)])==1
checks['no_positive_native_fabricator_after_conversion']=not any(j['planet']==0 and j['type']=='fabricator' and (j['workforce']>0 or j['max_workforce']>0) for j in a['pop_jobs'].values())
checks['native_patrol_capacity200']=job('patrol_drone')['max_workforce']==200

home=0
fleet_details={i:{'ship_ids':q.ids(q.block(f,'ships')),'scalars':q.scalars(f),'position':q.scalars(q.block(q.block(f,'movement_manager'),'coordinate')),'combat':q.block(f,'combat'),'owned_by_player':int(i) in owned(ar)} for i,f in afl.items() if (q.scalars(q.block(q.block(f,'movement_manager'),'coordinate')).get('origin')==home or int(i) in am) and q.scalars(f).get('ship_class')=='shipclass_military'}
p={'status':'PASS_NATIVE_TERRAVORE_UNITY_NODES_PROGRESS_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'days':days,'completed_zone61_nodes':len(anids),'remaining_node_orders':apo,'actual_new_node_ids':sorted(newbuild),'known_native_leader13_error_count':known_count,'known_native_coordinator_error_count':coordinator_count,'actual_capital_id':acid,'actual_capital_raw':ab[acid],'actual_coordinator':job('coordinator'),'actual_logistics':job('logistics_drone'),'actual_district_levels':al,'actual_owned_military_fleets':am,'actual_new_paid_ship_ids':new,'actual_lost_ship_ids_requires_native_combat_review':lost,'remaining_paid_orders':aids,'front_order_progress':[q.scalars(ai[str(i)])['progress'] for i in aids[:2]],'actual_own_ship_states':{i:q.scalars(ash[str(i)]) for i in ass},'actual_home_system_military_fleets':fleet_details,'actual_population_before':b['colonies']['0']['actual_pop_sum'],'actual_population_after':a['colonies']['0']['actual_pop_sum'],'last_month_native_growth_raw':q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'native_bombardment_damage':core['bombardment_damage'],'actual_stocks':ac['effective_stockpile'],'current_month_nets':nets,'Theory_queue':progress(ac),'scope':'Native paid zone61 nodes completed or progressed, actual staffed jobs and19 owned military ships. Both independently reproduced native errors counted separately; no unclassified errors, monthly or full-route claim.'}
out=run/(after+'-unity-nodes-progress-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native combat boundary FAIL retained'
