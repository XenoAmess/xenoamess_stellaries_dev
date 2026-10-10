"""Exact full-body native coordinator error reproduced by real empty-mod payment."""
import copy,json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,{k:v for k,v,o in q.fields(t) if o}
b,br=read('coordinator-control-hover');a,ar=read('coordinator-control-paid');bc,ac=b['countries']['0'],a['countries']['0']
prod=Path(json.loads(Path(m['production_pointer_backup']).read_text('utf-8'))['artifact_dir']);pp=json.loads((prod/'terravore-ascension-capital-paid-capital-payment-proof.json').read_text('utf-8'));pe=json.loads((prod/'terravore-ascension-capital-paid-guard-execution.json').read_text('utf-8'))
pre=json.loads((run/'coordinator-control-loaded-proof.json').read_text('utf-8'));ho=json.loads((run/'coordinator-control-hover-observation.json').read_text('utf-8'));obs=json.loads((run/'coordinator-control-paid-observation.json').read_text('utf-8'));click=json.loads((run/'coordinator-control-paid-normal-upgrade-click-once.action.json').read_text('utf-8'))
pb=(prod/'terravore-ascension-capital-paid-error-before.log').read_bytes();pa=(prod/'terravore-ascension-capital-paid-error-after.log').read_bytes();cb=(run/'coordinator-control-paid-error-before.log').read_bytes();ca=(run/'coordinator-control-paid-error-after.log').read_bytes();pd,cd=pa[len(pb):],ca[len(cb):];norm=lambda v:re.sub(rb'\[\d{2}:\d{2}:\d{2}\]',b'[TIME]',v)
co=ar['construction'];qu=q.block(q.block(q.block(co,'queue_mgr'),'queues'),'0');ids=q.ids(q.block(qu,'items'));it=q.block(q.block(q.block(co,'item_mgr'),'items'),str(ids[0])) if len(ids)==1 else ''
expected=copy.deepcopy(b['colonies']);expected['0']['last_building_changed']='building_hive_major_capital';source=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/pop_jobs/04_gestalt_jobs.txt')
checks={
 'actual_empty_mod_configuration':m['enabled_mods']==json.loads((user/'dlc_load.json').read_text('utf-8'))['enabled_mods']==[],
 'original_production_strict30_only_error_FAIL_exit1':pp['status']=='FAIL' and len(pp['checks'])==30 and [k for k,v in pp['checks'].items() if v is not True]==['unfiltered_error_original_bytes_held'] and pe['returncode']==1,
 'original_production_SHA_pair':h.sha256(prod/'terravore-ascension-generator5-month.sav')==pp['before_sha256']=='4371182e222afb2b0ad278c0b1e06f8b767ac28049ad39d1edccf6f6e10b6214' and h.sha256(prod/'terravore-ascension-capital-paid.sav')==pp['after_sha256']=='b5deb05a847f7463e2cf64c7cd1e3f15fc04381245bfe74f07bbbeda85f0f53c',
 'control_load8_PASS_exit0':pre['status']=='PASS_COORDINATOR_CONTROL_LOAD_ONLY' and len(pre['checks'])==8 and all(v is True for v in pre['checks'].values()) and json.loads((run/'coordinator-control-load-execution.json').read_text('utf-8'))['returncode']==0,
 'hover_exact_same_SAV_no_error_exit0':ho['before_sha256']==ho['after_sha256']==pre['after_sha256']==b['save_sha256'] and ho['new_error_bytes']==0 and json.loads((run/'coordinator-control-hover-observe-execution.json').read_text('utf-8'))['returncode']==0,
 'original_control_SHA_pair':h.sha256(run/'coordinator-control-hover.sav')==b['save_sha256'] and h.sha256(run/'coordinator-control-paid.sav')==a['save_sha256'],
 'one_native_upgrade_click_paid_observation_exit0':click['action']=='click_point' and click['client_point']==[151,335] and obs['before_sha256']==b['save_sha256'] and obs['after_sha256']==a['save_sha256'] and json.loads((run/'coordinator-control-paid-observe-execution.json').read_text('utf-8'))['returncode']==0,
 'same_actual_date':a['date']==b['date']=='2238.10.02',
 'actual480_minerals_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==480,
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'native_exact480_order_and_target':len(ids)==1 and not q.ids(q.block(q.block(q.block(q.block(br['construction'],'queue_mgr'),'queues'),'0'),'items')) and q.scalars(it)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':480} and q.scalars(q.block(it,'resources'))=={'minerals':480} and q.scalars(q.block(it,'buildable_planet_upgrade_building'))=={'building':'building_hive_major_capital','planet':0,'zone':0,'upgrade_building':0},
 'original_all_zones_buildings_raw_held':br['zones']==ar['zones'] and br['buildings']==ar['buildings'],
 'only_exact_colony_operation_record_changed':a['colonies']==expected,
 'original_error_prefixes_held':pa.startswith(pb) and ca.startswith(cb) and cb==(run/'coordinator-control-hover-error-after.log').read_bytes(),
 'exact255_increment_both':len(pd)==len(cd)==255,
 'entire_error_body_same_timestamp_only':norm(pd)==norm(cd),
 'exact_one_native_error_and_invalid_colony':cd.count(b'Script Error:')==1 and b'common/pop_jobs/04_gestalt_jobs.txt line: 562' in cd and b'Invalid context switch [colony] from  [colony]' in cd and b'id=4294967295\r\nopener_id=4294967295' in cd,
 'native_source_SHA_held':h.sha256(source)=='9469c178efbaa2d8e5bce43545ee6d5a184ee0e764336e85170795d0cc6820ad',
}
for k in ['tech_status','variables','flags','government','traditions','ascension_perks','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_SCOPED_NO_MOD_NATIVE_COORDINATOR_ERROR' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_source':{'path':str(source),'sha256':h.sha256(source)},'production_error_sha256':__import__('hashlib').sha256(pd).hexdigest(),'control_error_sha256':__import__('hashlib').sha256(cd).hexdigest(),'error_increment_bytes':len(cd),'native_order_raw':it,'scope':'Same255-byte original coordinator error reproduced by normal480-mineral upgrade in empty enabled_mods, full body differs only timestamp. No clean vanilla-generation/internal root-cause/original strict no-error PASS claim.'}
out=run/'coordinator-control-paid-error-proof.json';assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original control failure retained'
