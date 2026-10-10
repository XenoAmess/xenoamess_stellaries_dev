"""Exact scoped recovery proof for native caches/history and unrelated typeless deposit."""
import copy,json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
control=Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09/native-preftl-error-control')
def read(stem,base=run):
 a=json.loads((base/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(base/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,{k:v for k,v,o in q.fields(t) if o}
def obj(v):return {k:x for k,x,o in q.fields(v) if o}
def only(v,exclude):return [(k,x,o) for k,x,o in q.fields(v) if k not in exclude]
b,br=read('terravore-second-psionic-wait-year1');a,ar=read('terravore-production-resumed');s,sr=read('terravore-production-resumed-stable');cb,cr=read('terravore-second-postsettlement-month');cv,vr=read('preftl-control-loaded',control)
f=json.loads((run/'terravore-production-resumed-proof.json').read_text('utf-8'));g=json.loads((run/'terravore-production-resumed-stable-proof.json').read_text('utf-8'));yp=json.loads((run/'terravore-second-psionic-wait-year1-native-preftl-error-supplement.json').read_text('utf-8'))
bc,ac,sc=[v['countries']['0'] for v in [b,a,s]];expected_col=copy.deepcopy(b['colonies']);expected_col['0'].update(amenities=21271.2,free_amenities=16018,civilian=3178)
for i in ['15','24']:expected_col[i]['binary_flags']=24
expected_plan=copy.deepcopy(b['planets'])
for i in ['7','124']:expected_plan[i]['carrier_binary_flags']=3
expected_budget=copy.deepcopy(bc['budget_categories'])
for side,value in [('income',46.07464),('balance',46.07464)]:expected_budget['current_month'][side]['planet_maintenance_drones']['trade']=value
for side,value in [('expenses',0.29837),('balance',-0.29837)]:expected_budget['current_month'][side]['planet_resource_deficit']['trade']=value
for side,value in [('expenses',78.93),('balance',-78.93)]:expected_budget['current_month'][side]['planet_pops_traits']['minerals']=value
for side in ['income','expenses']:expected_budget['current_month'][side]['trade_policy']['trade']=63.17387
bh,ah,sh=[q.block(c['budget'],'income_high_water_mark') for c in [bc,ac,sc]];bd,ad,cd,vd=[obj(roots['deposit']) for roots in [br,ar,cr,vr]]
eb=(run/'terravore-production-resumed-error-before.log').read_bytes();ea=(run/'terravore-production-resumed-error-after.log').read_bytes();sb=(run/'terravore-production-resumed-stable-error-before.log').read_bytes();sa=(run/'terravore-production-resumed-stable-error-after.log').read_bytes()
checks={
 'bound_first24_exact4_FAIL_other20_true':f['status']=='FAIL' and len(f['checks'])==24 and {k for k,v in f['checks'].items() if not v}=={'no_new_error','budget_held','colonies_held','planets_held'},
 'bound_second24_only_raw_budget_FAIL_other23_true':g['status']=='FAIL' and len(g['checks'])==24 and [k for k,v in g['checks'].items() if not v]==['budget_held'],
 'original_three_SHA_chain':h.sha256(run/'terravore-second-psionic-wait-year1.sav')==f['before_sha256']==b['save_sha256'] and h.sha256(run/'terravore-production-resumed.sav')==f['after_sha256']==g['before_sha256']==a['save_sha256'] and h.sha256(run/'terravore-production-resumed-stable.sav')==g['after_sha256']==s['save_sha256'],
 'bound_native_year_error12_PASS':yp['status']=='PASS_SCOPED_NATIVE_PRE_FTL_ERROR_ATTRIBUTION' and len(yp['checks'])==12 and all(yp['checks'].values()) and yp['after_sha256']==b['save_sha256'],
 'all_same_actual_date':b['date']==a['date']==s['date']=='2234.09.01',
 'first_only_exact_colony_cache_and_ghost_flags_changes':a['colonies']==expected_col,
 'first_only_exact_tracked_carrier_flags_changes':a['planets']==expected_plan,
 'first_exact_eight_budget_leaf_changes_only':ac['budget_categories']==expected_budget,
 'first_budget_noncurrent_nonhighwater_RAW_held':only(bc['budget'],['current_month','income_high_water_mark'])==only(ac['budget'],['current_month','income_high_water_mark']),
 'first_highwater_only_original_empty_current_init_and_length':not q.scalars(q.block(bh,'current')) and q.scalars(q.block(ah,'current'))=={'energy':128.0756,'minerals':187.676,'physics_research':20.92892,'society_research':17.82892,'engineering_research':22.47892,'influence':6.4,'unity':82.84817,'trade':126.64611,'alloys':27.737} and q.scalars(bh)['length']==0 and q.scalars(ah)['length']==1 and only(bh,['current','length'])==only(ah,['current','length']),
 'second_all_actual_budget_categories_held':ac['budget_categories']==sc['budget_categories'],
 'second_RAW_budget_only_highwater_length1_to2':only(ac['budget'],['income_high_water_mark'])==only(sc['budget'],['income_high_water_mark']) and only(ah,['length'])==only(sh,['length']) and q.scalars(ah)['length']==1 and q.scalars(sh)['length']==2,
 'global_deposits_same_IDs_and_only218103836_changed':set(bd)==set(ad) and [k for k in bd if bd[k]!=ad[k]]==['218103836'],
 'exact_untyped_native1485_object_became_killed':q.scalars(bd['218103836'])=={} and q.scalars(q.block(bd['218103836'],'deposit_holder'))=={'type':0,'id':1485} and q.scalars(ad['218103836'])=={'killed':'yes'},
 'original_core1573_raw_held':bd['1573']==ad['1573'] and q.scalars(bd['1573'])['type']=='d_eep_core',
 'same_native_typeless_object_cleared_in_no_mod_control':set(cd)==set(vd) and {k for k in cd if cd[k]!=vd[k]}=={'218103836','1573'} and cd['218103836']==bd['218103836'] and q.scalars(vd['218103836'])=={'killed':'yes'} and q.scalars(vd['1573'])=={'killed':'yes'},
 'no_mod_same_highwater_length0_to1_observed':q.scalars(q.block(cb['countries']['0']['budget'],'income_high_water_mark'))['length']==0 and q.scalars(q.block(cv['countries']['0']['budget'],'income_high_water_mark'))['length']==1,
 'first_only_exact80_native_invalid_deposit_cleanup_error':ea.startswith(eb) and len(ea)-len(eb)==80 and bool(re.fullmatch(rb'\[\d{2}:\d{2}:\d{2}\]\[gamestate.cpp:1839\]: Repaired savegame, cleared 1 invalid deposits!\r?\n\r?\n',ea[len(eb):])),
 'second_unfiltered_log_entirely_held':sb==sa==ea,
 'production_single_unchanged_package':m['enabled_mods']==json.loads((user/'dlc_load.json').read_text('utf-8'))['enabled_mods']==['mod/ugc_eep-local.mod'] and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'actual_mother_and_LEDGER_held':s['colonies']['0']['actual_pop_sum']==8770 and all(sc['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_worlds':2,'eep_made':0}.items()) and q.scalars(sc['government'])['council_agenda_progress']==3024,
 'original19_and_full_mining_generator_held':sum(s['districts'][str(i)]['level'] for i in s['colonies']['0']['districts'])==19 and all(len(js:=[j for j in s['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',800)])}
p={'status':'PASS_SCOPED_TERRAVORE_PRODUCTION_RECOVERY' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'first_reload_sha256':a['save_sha256'],'after_sha256':s['save_sha256'],'first_and_second_original_FAILs_retained':True,'unfiltered_resumed_error_bytes':len(sa),'scope':'Exact original economic state preserved through restart/reloads. First native cache and unrelated typeless deposit cleanup explained; second only income history length increments. Original strict24 failures remain; not raw-byte all-world equality, pure vanilla-generation cause, long-term or full route completion.'}
out=run/'terravore-production-resumed-stable-recovery-supplement.json';assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original scoped recovery supplement FAIL retained; no next calendar'
