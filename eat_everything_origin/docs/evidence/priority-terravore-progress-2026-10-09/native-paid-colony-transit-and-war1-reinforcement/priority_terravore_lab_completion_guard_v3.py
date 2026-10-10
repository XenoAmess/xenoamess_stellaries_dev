"""Native paid capital completion and actual jobs; original full logs retained."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
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
 'actual_bounded_native_days_receipt_execution_zero':1<=days<=360 and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'paid_orders_contiguous_completion_other_fields_held':removed>=0 and aids==bids[removed:] and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) and 0<=q.scalars(ai[str(i)])['progress']<60 for i in aids),
 'actual_new_ships_equal_paid_completed_orders':len(new)==removed,
 'actual_all_owned_military_ship_relations_and_design':len(ass)==len(set(ass)) and all(q.scalars(ash[str(i)])['fleet']==fid and q.scalars(q.block(ash[str(i)],'ship_design_implementation'))['design']==67110548 and 0<q.scalars(ash[str(i)])['hitpoints']<=q.scalars(ash[str(i)])['max_hitpoints'] for fid,ss in am.items() for i in ss),
 'old_surviving_real_design_and_construction_dates_held':all(q.scalars(q.block(bsh[str(i)],'ship_design_implementation'))['design']==q.scalars(q.block(ash[str(i)],'ship_design_implementation'))['design'] and q.scalars(bsh[str(i)])['construction_date']==q.scalars(ash[str(i)])['construction_date'] for i in set(bs)&set(ass)),
 'total_naval_size_matches_all_actual_owned_corvettes':q.scalars(q.block(ar['country'],'0'))['fleet_size']==5*len(ass),
 'actual_native_shipyard_modules_and_crews_held':q.scalars(q.block(sb,'modules'))==q.scalars(q.block(sa,'modules'))=={'0':'shipyard','1':'shipyard'} and q.block(sb,'buildings')==q.block(sa,'buildings') and all(q.scalars(sb)[k]==q.scalars(sa)[k] for k in ['level','type','build_queue','shipyard_build_queue','station']),
 'EEP_all_variables_and_flags_held_no_repeat_notification':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and 'eep_psi_notice' in ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2,'eep_psi':1}.items()),
 'unique_core_owned_capacity11_original_modifiers':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11 and b['planets']['7']['modifiers']==core['modifiers'],
 'both_sources_unowned_shattered_no_actual_pop':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned_no_active_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'government_core_and_AP_traditions_held':omit(bc['government'],{'council_agenda_progress','council_agenda_cooldowns'})==omit(ac['government'],{'council_agenda_progress','council_agenda_cooldowns'}) and bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'all_primary_actual_stocks_positive':all(ac['effective_stockpile'][k]>0 for k in nets),
 'no_country0_pending_after_full_breach':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
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

def newlabs(rt):
 ids=q.ids(q.block(q.block(rt['zones'],'2'),'buildings'));assert len(ids)==3
 return {q.scalars(q.block(rt['buildings'],str(i)))['position']:i for i in ids if i!=16777251 and q.scalars(q.block(rt['buildings'],str(i))).get('type')=='building_research_lab_1'}
bnew,anew=newlabs(br),newlabs(ar);completed_here=set(anew)-set(bnew);total_done=len(anew)
checks['paid_lab_queue_order_and_progress_exact']=0<=done<=2 and apo==bpo[done:] and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) and 0<=q.scalars(ai[str(i)]).get('progress',0)<360 for i in apo)
checks['only_paid_lab_orders_correct_base_and_real_price']=all(q.scalars(bi[str(i)]).get('queue')==q.scalars(bi[str(i)]).get('paying_country')==0 and q.scalars(bi[str(i)]).get('progress_needed')==360 and q.scalars(q.block(bi[str(i)],'resources'))=={'minerals':320} and q.scalars(q.block(bi[str(i)],'buildable_planet_replace_building')).get('building')=='building_research_lab_1' and q.scalars(q.block(bi[str(i)],'buildable_planet_replace_building')).get('planet')==0 and q.scalars(q.block(bi[str(i)],'buildable_planet_replace_building')).get('zone')==2 and q.scalars(q.block(bi[str(i)],'buildable_planet_replace_building')).get('replace_building') in [38,41] for i in bpo)
checks['completed_orders_exact_new_lab_count_and_target_slots']=done==len(completed_here)==len(newbuild) and set(q.scalars(q.block(bi[str(i)],'buildable_planet_replace_building'))['replace_building'] for i in bpo[:done])=={38 if pos==1 else 41 for pos in completed_here} and not set(map(str,bpo[:done]))&set(ai)
bzone_ids=q.ids(q.block(bz['2'],'buildings'));azone_ids=q.ids(q.block(az['2'],'buildings'))
removed_buildings={str(38 if pos==1 else 41) for pos in completed_here}
old_expected=[38,16777251,41] if not bnew else [16777251,bnew[1],41]
new_expected=[16777251]+[anew[pos] for pos in sorted(anew)]+([41] if total_done==1 else [])
checks['zone2_exact_original_lab1_and_two_paid_slot_replacements']=bzone_ids==old_expected and azone_ids==new_expected and q.scalars(bb['16777251'])=={'type':'building_research_lab_1','position':1 if not bnew else 0} and q.scalars(ab['16777251'])=={'type':'building_research_lab_1','position':0} and all(q.scalars(ab[str(i)])=={'type':'building_research_lab_1','position':pos} and ((pos in bnew and bnew[pos]==i and bb[str(i)]==ab[str(i)]) or (pos not in bnew and str(i) in newbuild)) for pos,i in anew.items()) and all((not [(k,v,o) for k,v,o in q.fields(ar['buildings']) if k==old]) if old=='38' else ([(k,v,o) for k,v,o in q.fields(ar['buildings']) if k==old]==[('41','none',False)]) for old in removed_buildings) and (total_done==2 or bb['41']==ab['41'])
checks['all_other_zone_and_district_relations_held']=bzids==azids==[0,2,61] and bd==ad and all(bz[i]==az[i] for i in ['0','61']) and omit(bz['2'],{'buildings'})==omit(az['2'],{'buildings'})
checks['unique_native_capital_same_raw_held']=bcid==acid and acap.get('type')==bcap.get('type')=='building_hive_major_capital' and bb[bcid]==ab[acid]
checks['all_other_actual_mother_buildings_raw_held']=set(ab)==set(bb)-removed_buildings|newbuild and all(ab.get(i)==v for i,v in bb.items() if i not in removed_buildings|({'16777251'} if not bnew else set())) and (bool(bnew) or omit(bb['16777251'],{'position'})==omit(ab['16777251'],{'position'}))
psi=[i for i,v in ab.items() if q.scalars(v).get('type')=='building_psi_corps']
checks['one_psi_native_slot3_raw_held']=len(psi)==1 and q.scalars(ab[psi[0]])=={'type':'building_psi_corps','position':3} and bb[psi[0]]==ab[psi[0]]
checks['exact_expected_lab_completion_checkpoint']=total_done==(1 if after=='terravore-labs-first-year' else 2) and ((total_done==1 and len(apo)==1) or (total_done==2 and not apo))
if after=='terravore-labs-first-year':
 original=json.loads((run/(after+'-paid-lab-completion-boundary-proof.json')).read_text('utf-8'));oldex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
 checks['bound_original53_exact_two_native_reorder_failures_or_prior_V2']=original['status']=='FAIL' and len(original['checks'])==53 and set(k for k,v in original['checks'].items() if v is not True)=={'zone2_exact_original_lab1_and_two_paid_slot_replacements','all_other_actual_mother_buildings_raw_held'} and original['before_sha256']==b['save_sha256'] and original['after_sha256']==a['save_sha256'] and oldex['returncode']==1 and oldex['helper_sha256']=='065f79b0adc0e785cbfb6b801b9f5fd735ed77b5bbda54afab5a032d5561ef82'
else:
 checks['bound_original53_exact_two_native_reorder_failures_or_prior_V2']=pre['status']=='PASS_TERRAVORE_PAID_LAB_COMPLETION_BOUNDARY_V2_COMPONENT' and len(pre['checks'])==54 and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and bnew=={1:83886120}

def job(kind):
 js=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind];assert len(js)==1;return js[0]
checks['actual_coordinator_paid_replacement_logistics500_telepath200_full']=all(job(k)['workforce']==job(k)['max_workforce']==n for k,n in [('coordinator',2400-total_done*200),('logistics_drone',500),('telepath_drone',200)])
checks['before_coordinator_corresponds_actual_replacement_stage']=len([j for j in b['pop_jobs'].values() if j['planet']==0 and j['type']=='coordinator' and j['workforce']==j['max_workforce']==2400-len(bnew)*200])==1
checks['actual_each_research_full_paid_lab_capacity']=all(job(k)['workforce']==job(k)['max_workforce']==180+60*total_done for k in ['calculator_physicist','calculator_biologist','calculator_engineer'])
checks['no_positive_native_fabricator_after_conversion']=not any(j['planet']==0 and j['type']=='fabricator' and (j['workforce']>0 or j['max_workforce']>0) for j in a['pop_jobs'].values())
checks['native_patrol_capacity200']=job('patrol_drone')['max_workforce']==200


checks['both_native_situations_empty_after_full_breach']=not b['situations'] and not a['situations']
checks['native_full_breach_and_psi_report1_held']=bc['variables']['eep_psi']==ac['variables']['eep_psi']==1 and all(q.scalars(q.block(q.block(rt['country'],'0'),'flags')).get(k)==63314904 for rt in [br,ar] for k in ['breached_shroud','psionic_traditions_unlocked'])
checks['one_full_psionic_lithoid_hive_species_old66_rights_held']=set(a['species'])=={'73'} and a['species']['73']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_psionic'] and ac['native']['founder_species_ref']==73 and q.block(br['species_db'],'66')==q.block(ar['species_db'],'66') and q.block(q.block(q.block(q.block(br['country'],'0'),'modules'),'standard_species_rights_module'),'primary')==q.block(q.block(q.block(q.block(ar['country'],'0'),'modules'),'standard_species_rights_module'),'primary')

bsi,asi=[q.block(q.block(rt['situations'],'situations'),'16777221') for rt in [br,ar]]
checks['native_breach_raw_stays_absent']=not bsi and not asi


brc,arc=[q.block(rt['country'],'0') for rt in [br,ar]]
def society(c):
 v=q.block(c['tech_status'],'society_queue').strip();assert v.startswith('{') and v.endswith('}')
 return v[1:-1]
bq,aq=[society(c) for c in [bc,ac]]
draw=D(str(bc['research_stockpile']['society_research']))-D(str(ac['research_stockpile']['society_research']))
gain=D(str(q.scalars(aq).get('progress',0)))-D(str(q.scalars(bq).get('progress',0)))
checks['society_project2_queue_only_progress_increases']=omit(bq,{'progress'})==omit(aq,{'progress'}) and q.scalars(aq).get('special_project')==2 and 0<=q.scalars(bq).get('progress',0)<q.scalars(aq)['progress']<3000
checks['actual_society_stored_draw_project_conservation']=draw>0 and ac['research_stockpile']['society_research']>0 and abs(gain-draw*D('2.33'))<D('0.005')
checks['native_project2_and_all_events_raw_held']=q.block(brc,'events')==q.block(arc,'events')
checks['native_crisis1_no_completion_raw_held']=q.block(brc,'crisis_progression')==q.block(arc,'crisis_progression') and q.scalars(q.block(arc,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and 'crisis_special_project_1_complete' not in q.scalars(q.block(arc,'flags'))
checks['old_special607_25288_and_native_auto_research_held']=bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_colonization_2':607.25288} and all(q.scalars(c['tech_status']).get('auto_researching_'+k)==v for c in [bc,ac] for k,v in [('society','no'),('physics','yes'),('engineering','yes')]) and set(bc['completed_technologies'])<=set(ac['completed_technologies'])
checks['actual_energy_mineral_nets_positive']=nets['energy']>0 and nets['minerals']>0
checks['exact_native_planned_interval']=days==(360 if after=='terravore-labs-first-year' else 180) and after in ['terravore-labs-first-year','terravore-labs-complete']


assert after=='terravore-labs-complete'
oldproof=json.loads((run/(after+'-paid-lab-completion-v2-proof.json')).read_text('utf-8'));oldexec=json.loads((run/(after+'-guard-v2-execution.json')).read_text('utf-8'))
checks['bound_original54_exact_old41_serialization_failure']=oldproof['status']=='FAIL' and len(oldproof['checks'])==54 and [k for k,v in oldproof['checks'].items() if v is not True]==['zone2_exact_original_lab1_and_two_paid_slot_replacements'] and oldproof['before_sha256']==b['save_sha256'] and oldproof['after_sha256']==a['save_sha256'] and oldexec['returncode']==1 and oldexec['helper_sha256']=='86592d30161f48d971a2216480a959ba1673be7cf9f8bb72af7e0190555ab856'

home=0
fleet_details={i:{'ship_ids':q.ids(q.block(f,'ships')),'scalars':q.scalars(f),'position':q.scalars(q.block(q.block(f,'movement_manager'),'coordinate')),'combat':q.block(f,'combat'),'owned_by_player':int(i) in owned(ar)} for i,f in afl.items() if (q.scalars(q.block(q.block(f,'movement_manager'),'coordinate')).get('origin')==home or int(i) in am) and q.scalars(f).get('ship_class')=='shipclass_military'}
source=h.GAME_EXE.parent/'common/situations/13_shroud_situations.txt';monthly=q.block(q.block(source.read_text('utf-8-sig'),'situation_breach_shroud'),'monthly_progress');mods=[v for k,v,o in q.fields(monthly) if k=='modifier'];speed_keys=['tr_psionics_shroud_telekinesis','tr_psionics_shroud_clairvoyance','tr_psionics_shroud_psychometry']
checks['native_three_unique_mult105_source_conditions']=all(len([v for v in mods if q.scalars(v)=={'mult':1.05,'desc':key} and q.scalars(q.block(v,'owner'))=={'has_tradition':key}])==1 for key in speed_keys)
checks['all_five_psionic_traditions_and_finish_actually_paid']=all(key in bc['traditions'] and key in ac['traditions'] for key in speed_keys+['tr_psionics_shroud_psi_corps','tr_psionics_shroud_great_awakening','tr_psionics_shroud_adopt','tr_psionics_shroud_finish'])
eep=Path.cwd()/'eat_everything_origin/mod/events/eep_events.txt';trig=Path.cwd()/'eat_everything_origin/mod/common/scripted_triggers/eep_triggers.txt'
ev=[v for k,v,o in q.fields(eep.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='eep.2'];assert len(ev)==1
active=q.block(q.block(q.block(ev[0],'immediate'),'if'),'else_if');cases=[v for k,v,o in q.fields(active) if k=='if' and o and q.scalars(q.block(v,'country_event')).get('id')=='eep.30'];assert len(cases)==1
checks['EEP_monthly_source_first_notice_gate_no_reward']=q.scalars(q.block(cases[0],'limit'))=={'eep_psionic_ascension_complete':'yes'} and q.scalars(q.block(q.block(cases[0],'limit'),'NOT'))=={'has_country_flag':'eep_psi_notice'} and q.scalars(cases[0])=={'set_country_flag':'eep_psi_notice'} and [(k,o) for k,v,o in q.fields(cases[0])]==[('limit',True),('set_country_flag',False),('country_event',True)]
gate=q.block(trig.read_text('utf-8-sig'),'eep_psionic_ascension_complete');checks['EEP_full_tree_and_breach_source_gate']=q.scalars(gate)=={'has_finished_psionic_tradition':'yes'} and q.scalars(q.block(gate,'OR'))=={'has_shroud_dlc':'no','has_breached_shroud':'yes'}
p={'status':'PASS_TERRAVORE_PAID_LAB_COMPLETION_BOUNDARY_V3_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'days':days,'native_speed_source':{'path':str(source),'sha256':h.sha256(source)},'completed_zone61_nodes':len(anids),'remaining_node_orders':apo,'actual_psi_ids':psi,'actual_telepath':job('telepath_drone'),'known_native_leader13_error_count':known_count,'known_native_coordinator_error_count':coordinator_count,'actual_capital_id':acid,'actual_capital_raw':ab[acid],'actual_coordinator':job('coordinator'),'actual_logistics':job('logistics_drone'),'actual_district_levels':al,'actual_owned_military_fleets':am,'actual_new_paid_ship_ids':new,'actual_lost_ship_ids_requires_native_combat_review':lost,'remaining_paid_orders':aids,'front_order_progress':[q.scalars(ai[str(i)])['progress'] for i in aids[:2]],'actual_own_ship_states':{i:q.scalars(ash[str(i)]) for i in ass},'actual_home_system_military_fleets':fleet_details,'actual_population_before':b['colonies']['0']['actual_pop_sum'],'actual_population_after':a['colonies']['0']['actual_pop_sum'],'last_month_native_growth_raw':q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'native_bombardment_damage':core['bombardment_damage'],'actual_stocks':ac['effective_stockpile'],'current_month_nets':nets,'Theory_queue':q.block(ac['tech_status'],'society_queue'),'native_research_queues':ac['research_queues'],'native_research_bank_before_after':[bc['research_stockpile'],ac['research_stockpile']],'newly_completed_technologies':sorted(set(ac['completed_technologies'])-set(bc['completed_technologies'])),'native_situations':a['situations'],'eep_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [eep,trig]],'actual_paid_lab_completion':{'completed_before':bnew,'completed_after':anew,'remaining_orders':apo,'society_draw':str(draw),'project_gain':str(gain),'project_conservation_residual':str(gain-draw*D('2.33'))},'scope':'Paid lab construction and native research boundary; no full monthly ledger claim. Stable actual interval after full native breach and repeated normal report; no repeated Queen notice or reward. Real workforce and economic state checked. Separate full month ledger required.'}
out=run/(after+'-paid-lab-completion-v3-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native combat boundary FAIL retained'
