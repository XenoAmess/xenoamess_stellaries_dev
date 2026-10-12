"""Independently review a bounded next project2 calendar interval with native piracy delay."""
import json,logging,re,sys,zipfile
from pathlib import Path
stage,end,rawdays,proof,execution,outstage=sys.argv[1:];days=int(rawdays)
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring/runs/20261009T044016Z'];sys.argv=['runtime']
import runtime as r,audit_save as q
from formal_production_native_calendar_checked_v3 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'));sha=h.sha256
pre,ex=load(proof),load(execution+'-execution.json');a=load(stage+'.audit.json');c=a['countries']['0'];start=a['date'];validate_native_interval(start,end,days)
with zipfile.ZipFile(run/(stage+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
roots={k:v for k,v,o in q.fields(t) if o};country=q.block(roots['country'],'0');module=q.block(q.block(country,'modules'),'standard_event_module');ds=[v for k,v,o in q.fields(module) if k=='delayed_event' and o];known=[v for v in ds if q.scalars(v).get('event')=='pirate.6'];flags=q.scalars(q.block(country,'flags'))
projects=[v for k,v,o in q.fields(q.block(country,'events')) if k=='special_project' and q.scalars(v).get('id')==8];assert len(projects)==1
inv=load('terravore-mineral-corvette-first-full-month-date-native-pirate6-delayed-investigation.json');source=Path(r'C:/SteamLibrary/steamapps/common/Stellaris/common/special_projects/00_projects_nemesis.txt');preserved=run/'terravore-project2-native-projects-source.txt'
if preserved.exists():assert preserved.read_bytes()==source.read_bytes()
else:preserved.write_bytes(source.read_bytes())
owned=q.block(q.block(country,'fleets_manager'),'owned_fleets');fids=re.findall(r'\bfleet\s*=\s*(\d+)',owned);fleets={i:q.block(roots['fleet'],i) for i in fids};mia={'2':'2280.03.16','33555013':'2280.01.03','33555278':'2281.06.27'}
remaining=q.scalars(known[0])['days'] if len(known)==1 else None
checks={
 'prior_all_PASS_actual0_SHA_source_current':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and ex['returncode']==0 and ex['helper_sha256']==sha(Path(ex['command'][1])) and pre['after_sha256']==a['save_sha256']==sha(run/(stage+'.sav')),
 'physical_project8_in_progress_not_completed':q.scalars(projects[0]).get('special_project')=='CRISIS_SPECIAL_PROJECT_PSIONIC_2' and q.scalars(projects[0]).get('status')=='in_progress' and 'crisis_special_project_2_complete' not in flags and 'special_project=8' in re.sub(r'\s+','',q.block(c['tech_status'],'physics_queue')),
 'known_pirate_only_delay_scope_days_reviewed':len(ds)==len(known)==1 and 1<=remaining<=18 and q.scalars(q.block(known[0],'scope')).get('type')=='country' and q.scalars(q.block(known[0],'scope')).get('id')==0 and all(sha(Path(s['path']))==sha(run/s['preserved_file'])==s['sha256'] for s in inv['native_sources']),
 'interval_before_or_exact_known_delay_and_first_tick_only_if_unobserved':1<=days<=min(7,remaining) and (stage!='terravore-project2-started' or (days==1 and end=='2279.01.02')) and start[:7]==end[:7],
 'no_pending_combat_unknown_MIA_or_other_owned_orders':not [v for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0] and not any(re.search(r'\bfleet\s*=',q.block(q.block(v,'combat'),'in_combat_with')) for v in fleets.values()) and {i for i,v in fleets.items() if q.scalars(q.block(v,'properties')).get('mia')=='yes'}==set(mia) and all(q.scalars(fleets[i]).get('return_date')==date for i,date in mia.items()),
 'EEP62_17_4_queen2_mother35_colony0_holds':all(c['variables'].get(k)==v for k,v in {'eep_c':62,'eep_d':17,'eep_worlds':4,'eep_psi':1,'eep_stage':2,'eep_crisis':2,'eep_fleet_stage':2,'eep_g':0,'eep_made':0}.items()) and c['owned_colonies']==[0] and a['planets']['7']['variables']['eep_capacity_value']==17 and c['native']['used_naval_capacity']==109,
 'production41_020_CN_and_error_original':meta['language']=='l_simp_chinese' and meta['version']=='0.2.0' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and sha(run/(stage+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
passed=all(v is True for v in checks.values());out=run/(outstage+'-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['save_sha256'],'after_sha256':a['save_sha256'],'start_date':start,'end_date':end,'days':days,'maximum_days':days,'allowed_boundaries':pre['boundaries'],'execution_stage':outstage,'source_proof_file':proof,'source_proof_sha256':sha(run/proof),'native_delay_remaining':remaining,'native_project_source_sha256':sha(source),'scope':'Next exact bounded native project2 research and known original pirate6 countdown; any actual event or unexpected state requires independent observation.'});print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'start':start,'end':end}),flush=True);assert passed
