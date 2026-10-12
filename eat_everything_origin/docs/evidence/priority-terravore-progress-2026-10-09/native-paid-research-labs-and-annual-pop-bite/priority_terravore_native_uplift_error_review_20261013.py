"""Exact single native pre_fun13 lookup error; retain failed calendar and endpoint."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
from priority_native_reviewed_error_baseline import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-three-labs-normal-month-22810901';after='terravore-three-labs-normal-month-22811001';b,a=[read_state(run,s) for s in [before,after]];pre=load(before+'-three-labs-serial-month-proof.json');px=load(before+'-serial-labs-guard-execution.json');cx=load(after+'-calendar-execution.json')
eb=(run/(after+'-error-before.log')).read_bytes();ea=(run/(after+'-error-after.log')).read_bytes();sources=[]
for rel in ['common/species_classes/00_species_classes.txt','common/portrait_sets/00_portrait_sets.txt','gfx/portraits/portraits/07_portraits_presapient.txt']:
 p=h.GAME_EXE.parent/rel;dest=run/('terravore-native-uplift-original-'+p.name)
 if dest.exists():assert dest.read_bytes()==p.read_bytes()
 else:dest.write_bytes(p.read_bytes())
 sources.append({'path':str(p),'preserved':dest.name,'sha256':h.sha256(p)})
classes=Path(sources[0]['path']).read_text('utf-8-sig');sets=Path(sources[1]['path']).read_text('utf-8-sig');portraits=Path(sources[2]['path']).read_text('utf-8-sig')
autos=[p for p in (user/'save games').rglob('autosave_2281.10.01.sav') if h.sha256(p)==a['audit']['save_sha256']];species=q.block(a['roots']['species_db'],'46');pops={}
for v in a['audit']['pop_groups'].values():
 k=str(v['planet'])+':'+str(v['key']['species']);pops[k]=pops.get(k,0)+v['size']
checks={
 'original_calendar_actual1_exact_error_assert_source_retained':cx['returncode']==1 and cx['helper_sha256']==h.sha256(Path(cx['command'][1]))=='736473506dec7a0255508961f4e3a163fbf7b06375528fce2371737a46d595b3' and "assert ea==eb,'New error retained; no continuation'" in (run/(after+'-calendar-stderr.txt')).read_text('utf-8'),
 'unique_exact128byte_native_error_delta_original_prefix_current_same':len(eb)==3723 and len(ea)==3851 and ea.startswith(eb) and ea[len(eb):]==b"[00:54:06][species_portrait_set.cpp:621]: Failed to find uplifted portrait for portrait 'pre_fun13' of species class 'PRE_FUN'\r\n\r\n" and h.sha256(user/'logs/error.log')==h.sha256(run/(after+'-error-after.log'))=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and reviewed_error_pair(eb,eb,run),
 'native_PRE_FUN_class_portrait_and_existing_uplift_mapping':q.scalars(q.block(classes,'PRE_FUN'))['uplifted_into']=='FUN' and q.scalars(q.block(sets,'pre_fungoids'))['species_class']=='PRE_FUN' and all(v in q.block(sets,'pre_fungoids') for v in ['"pre_fun13"','"fun13"']) and 'pre_fun13' in portraits and not any('PRE_FUN' in p.read_text('utf-8-sig') or 'pre_fun13' in p.read_text('utf-8-sig') for p in h.MOD_ROOT.rglob('*.txt')),
 'original_species46_raw_held_nonowned_species_all_owned_pops73':species==q.block(b['roots']['species_db'],'46') and q.scalars(species)['class']=='PRE_FUN' and q.scalars(species)['portrait']=='pre_fun13' and q.scalars(species)['sapient']=='no' and q.scalars(q.block(species,'home_planet'))['reference']==1723 and set(pops)=={'0:73','30:73'},
 'actual_fresh_original_autosave_endpoint_SHA_date_no_fake_actual0':len(autos)==1 and a['audit']['save_sha256']==h.sha256(run/(after+'.sav'))=='f7abeb1ae5dcbbd644f63d69d98f59359003dd987baf25e583bea0ff62f96c46' and a['audit']['date']=='2281.10.01' and autos[0].stat().st_mtime_ns>(run/(before+'.sav')).stat().st_mtime_ns,
 'prior18PASS_actual0_unchanged_EEP_no_new_messages_pending':len(pre['checks'])==18 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and pre['after_sha256']==b['audit']['save_sha256']==h.sha256(run/(before+'.sav')) and b['audit']['countries']['0']['variables']==a['audit']['countries']['0']['variables'] and not a['pending'] and not [v for v in a['messages'] if v not in b['messages']],
 'all_three_native_sources_preserved_same_CN_production41':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(after+'-native-uplift-review-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_EXACT_NATIVE_UPLIFT_LOOKUP_ERROR_REVIEW' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'sources':sources,'old_error_file':after+'-error-before.log','new_error_file':after+'-error-after.log','original_calendar_returncode':1,'original_autosave':str(autos[0]) if autos else None,'after_state':{'species_population_by_colony':pops},'new_country0_messages_raw':[v for v in a['messages'] if v not in b['messages']],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Exactly one native resource lookup error attributed to original species and assets; engine root cause remains unknown. Existing autosave recovered, no false calendar actual0 or route claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
