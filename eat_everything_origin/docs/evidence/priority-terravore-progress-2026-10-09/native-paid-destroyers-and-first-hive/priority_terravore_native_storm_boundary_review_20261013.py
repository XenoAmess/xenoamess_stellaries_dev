"""Three normal native days to the documented drift-capsule callback."""
import json,logging,sys,shutil
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-society-first-budget-22840701';a=read_state(run,before);p=load(before+'-society-first-budget-proof.json');x=load(before+'-society-first-budget-guard-execution.json')
base=Path('C:/SteamLibrary/steamapps/common/Stellaris');sources=[]
for rel in ['events/cosmic_storms_events_1.txt','localisation/simp_chinese/cosmic_storms_l_simp_chinese.yml']:
 src=base/rel;dest=run/('storm-callback-native-'+src.name)
 if dest.exists():assert src.read_bytes()==dest.read_bytes()
 else:shutil.copyfile(src,dest)
 sources.append({'path':str(src),'preserved':dest.name,'sha256':h.sha256(src)})
native=Path(sources[0]['path']).read_text('utf-8-sig');ev={q.scalars(v).get('id'):v for k,v,obj in q.fields(native) if obj and k in ['country_event','system_event']}
delay=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
checks={
 'prior23PASS_actual0_SAV_source':len(p['checks'])==23 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_three_days_exact_storm_boundary_no_pending':p['boundaries']==['native_storm1815_due_review'] and a['audit']['date']=='2284.07.01' and not a['pending'] and [v for v in delay if v['event']=='cstorms.1815'][0]['days']==3 and all(v['event'] in ['cstorms.1815','pirate.6'] for v in delay),
 'native_hidden_callback_and_only_investigate_option_preserved':'random_system_within_border' in ev['cstorms.1815'] and 'cstorms.1816' in ev['cstorms.1815'] and q.scalars(q.block(ev['cstorms.1816'],'option'))['name']=='cstorms.1816.a' and q.scalars(q.block(q.block(ev['cstorms.1816'],'option'),'enable_special_project'))['name']=='STORM_IN_A_BOX_INVESTIGATE_PROJECT' and 'add_resource' not in ev['cstorms.1816'],
 'CN_package_unfiltered_error_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(before+'-native-storm-boundary-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2284.07.01','end_date':'2284.07.04','days':3,'maximum_days':3,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-native-storm-boundary-review','sources':sources,'scope':'Normal native callback only, stop pending capsule event for independent review.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
