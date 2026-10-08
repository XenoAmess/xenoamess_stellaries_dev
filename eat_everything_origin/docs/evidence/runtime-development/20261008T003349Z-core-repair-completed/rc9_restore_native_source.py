import json
import logging
from pathlib import Path
import shutil
import sys
alias,stage=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,manifest=h.load_run()
copy=run/Path(__file__).name
if not copy.exists():
 shutil.copyfile(Path(__file__),copy)
assert copy.read_bytes()==Path(__file__).read_bytes()
sources=[]
for name in ['rc9-original-native-source-preflight.json','rc9-recovery-extra-source-preflight.json']:
 sources.extend(json.loads((run/name).read_text(encoding='utf-8'))['sources'])
source=next(v for v in sources if v['alias']==alias)
before=json.loads(Path(source['source']).with_suffix('.audit.json').read_text(encoding='utf-8'))
receipt=r.native_load(alias,stage+'-original-load')
assert receipt['source_sha256']==source['sha256']
after=r.native_save(stage,source['date'],(0,))
b,a=before['countries']['0'],after['countries']['0']
keys=['eep_c','eep_g','eep_d','eep_made','eep_worlds']
checks={
 'original_actual_civic':'civic_hive_scorched_earth' in a['government'],
 'original_origin':'origin_heart_of_devouring' in a['government'],
 'original_stockpiles':a['stockpile']==b['stockpile'],
 'original_ledger':{k:a['variables'].get(k) for k in keys}=={k:b['variables'].get(k) for k in keys},
 'original_owned_colonies':set(a['owned_colonies'])==set(b['owned_colonies']),
 'actual_owned_population':all(after['colonies'][str(i)]['actual_pop_sum']==before['colonies'][str(i)]['actual_pop_sum'] for i in b['owned_colonies']),
 'original_core_and_actor_targets':[{k:v for k,v in t.items()} for t in after['event_targets'] if t.get('name') in ('eep_core0','eep_core_actor1')]==[{k:v for k,v in t.items()} for t in before['event_targets'] if t.get('name') in ('eep_core0','eep_core_actor1')],
}
if alias=='focus-base23':
 checks['source69']=after['colonies']['24']['actual_pop_sum']==69
 checks['only_two_colonies']=set(a['owned_colonies'])=={0,24}
elif alias=='fleet2-war80':
 checks['actual_menace135']=a['stockpile'].get('menace')==135
 checks['no_first_fleet_notice']='eep_fleet_notice' not in a['flags']
elif alias=='core-dead':
 checks['actual_death_flag']='eep_core_dead' in a['flags']
 checks['actual_shattered_core']=after['planets']['1']['planet_class']=='pc_shattered'
elif alias in ('hive-fixed','hive-missing-core'):
 checks['actual_hive']=after['planets']['1']['planet_class']=='pc_hive'
 checks['core_deposit_expected']=sum(after['deposits'][str(i)]['type']=='d_eep_core' for i in after['planets']['1']['deposits'])==(1 if alias=='hive-fixed' else 0)
result={'status':'SOURCE_RESTORED' if all(checks.values()) else 'FAILED_PRECONDITION','alias':alias,'date':after['date'],'source_sha256':source['sha256'],'save_sha256':after['save_sha256'],'checks':checks,'scope':'Native original-byte reload and authoritative preconditions; no whole-object cache equality claim.'}
h.write_json(run/(stage+'-source-precondition-proof.json'),result)
print(json.dumps(result,ensure_ascii=True),flush=True)
assert all(checks.values())
