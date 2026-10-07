import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q

run=Path('_runtime/heart-of-devouring/runs/20261007T154144Z')
names=['rc6-mixed-natural-c20-g0-before-species-control',
       'rc6-mixed-trait-conversion-main-precondition',
       'rc6-mixed-mam-new-main-native-precondition',
       'rc6-mixed-generic-q20-real100-seed-before-start',
       'rc6-mixed-generic-q20-current-start-no-native-flag',
       'rc6-mixed-native20-generic20-same-country-completed']
states=[]
raw_countries=[]
players=[]
for name in names:
    sav=run/(name+'.sav')
    with zipfile.ZipFile(sav) as z:
        text=z.read('gamestate').decode('utf-8-sig')
    countries={k:v for k,v,obj in q.fields(q.block(text,'country')) if obj}
    ids=tuple(int(k) for k in countries)
    x=q.audit(sav,ids)
    out=run/(name+'.all-countries.audit.json')
    assert not out.exists()
    out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    states.append(x)
    raw_countries.append(countries)
    players.append(re.findall(r'country=(\d+)',q.block(text,'player')))

original,trait,mam,seed,start,done=states
checks=[]


def check(name,actual,expected):
    same=actual==expected
    def evidence(value):
        encoded=json.dumps(value,ensure_ascii=False,sort_keys=True,default=sorted).encode('utf-8')
        if len(encoded)<=1400:
            return value
        return {'complete_canonical_json_sha256':hashlib.sha256(encoded).hexdigest(),
                'json_bytes':len(encoded),'full_inputs':'retained .all-countries.audit.json and original native .sav files; no fields filtered'}
    checks.append({'check':name,'actual':evidence(actual),'expected':evidence(expected),
                   'status':'PASS' if same else 'FAIL'})


def root_pops(x):
    return sum(g['size'] for g in x['pop_groups'].values() if g['planet'] in x['countries']['0']['owned_colonies'])


def target(x,name):
    return next(t['id'] for t in x['event_targets'] if t['name']==name)


foreign_ids=sorted(k for k in original['countries'] if k!='0')
foreign_colonies={c for i in foreign_ids for c in original['countries'][i]['owned_colonies']}
foreign_planets={i for i,p in original['planets'].items() if p.get('colony') in foreign_colonies}
foreign_groups={i:g for i,g in original['pop_groups'].items() if g['planet'] in foreign_colonies}
foreign_jobs={i:j for i,j in original['pop_jobs'].items() if j['planet'] in foreign_colonies}
foreign_species={str(g['key']['species']) for g in foreign_groups.values()}
for j,x in enumerate(states):
    check('same_native_date_'+str(j),x['date'],'2204.01.02')
    check('actual_root_player_foreign_'+str(j),players[j],['16777218'])
    check('all_native_country_ids_'+str(j),sorted(x['countries']),sorted(original['countries']))
    check('all_foreign_complete_audit_records_'+str(j),{i:x['countries'][i] for i in foreign_ids},{i:original['countries'][i] for i in foreign_ids})
    raw_equal={i:raw_countries[j][i]==raw_countries[0][i] for i in foreign_ids}
    check('all_foreign_full_raw_country_blocks_'+str(j),raw_equal,{i:True for i in foreign_ids})
    check('all_foreign_audited_physical_planets_'+str(j),{i:x['planets'].get(i) for i in foreign_planets},{i:original['planets'][i] for i in foreign_planets})
    check('all_foreign_audited_colonies_'+str(j),{str(i):x['colonies'].get(str(i)) for i in foreign_colonies if str(i) in original['colonies']},
          {str(i):original['colonies'][str(i)] for i in foreign_colonies if str(i) in original['colonies']})
    check('all_foreign_audited_population_groups_'+str(j),{i:x['pop_groups'].get(i) for i in foreign_groups},foreign_groups)
    check('all_foreign_audited_jobs_'+str(j),{i:x['pop_jobs'].get(i) for i in foreign_jobs},foreign_jobs)
    check('all_foreign_shared_audited_species_'+str(j),{i:x['species'].get(i) for i in foreign_species},{i:original['species'][i] for i in foreign_species})
    check('bound_core8_'+str(j),target(x,'eep_core0'),8)
    check('bound_original_size20_'+str(j),x['planets']['8']['planet_size'],20)
    check('old_native_source3_stays_shattered_'+str(j),x['planets']['3']['planet_class'],'pc_shattered')

check('current_mam_actual_main48',mam['countries']['0']['native']['founder_species_ref'],48)
check('current_mam_independent_main_target',target(mam,'eep_probe_mixed_organic_verified_main'),48)
check('current_mam_actual_class',mam['species']['48']['class'],'MAM')
check('current_mam_actual_organic_hive',set(mam['species']['48']['traits']),{'trait_organic','trait_hive_mind','trait_pc_continental_preference'})
log=Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261007T154144Z/logs/game.log').read_text(encoding='utf-8',errors='replace')
check('native_mam_nonlith_and_qualified_verified','EEP_RC6_MIXED_MAM_NONLITH_QUALIFIED' in log,True)
check('failed_trait_only_precondition_retained','EEP_RC6_MIXED_TRAIT_STILL_LITHOID' in log,True)
check('species_control_did_not_mint_population',[root_pops(original),root_pops(trait),root_pops(mam)],[6037]*3)
check('seed_creation_did_not_mint_population',[root_pops(seed),root_pops(start)],[6037]*2)
check('source_id13_actual',target(start,'eep_probe_source'),13)
check('source_colony17_actual_seed100',start['colonies']['17']['actual_pop_sum'],100)
check('source_seed_taken_from_core',mam['colonies']['0']['actual_pop_sum']-seed['colonies']['0']['actual_pop_sum'],100)
check('current_generic_q20_t48',[start['planets']['13']['variables'][k] for k in ['eep_q','eep_months']],[20,48])
check('current_generic_active','eep_active' in start['planets']['13']['flags'],True)
check('current_generic_owned_context','eep_owned_colony_event' in start['planets']['13']['flags'],True)
check('current_generic_not_native','eep_native' in start['planets']['13']['flags'],False)
for label,x in [('original',original),('mam',mam),('seed',seed),('start',start)]:
    v=x['countries']['0']['variables']
    check('same_original_native_ledger_'+label,[v[k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']],[20,0,7,0,1])
    check('same_native_root_stock_'+label,x['countries']['0']['stockpile'],original['countries']['0']['stockpile'])
v=done['countries']['0']['variables']
check('same_country_mixed_final_ledger',[v[k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds','eep_last_capacity','eep_last_manufactured']],[40,20,12,300,2,5,300])
check('actual_physical_capacity12',done['planets']['8']['variables']['eep_capacity_value'],12)
check('actual_only_generic_net_population300',root_pops(done)-root_pops(start),300)
check('actual_core_population6337',done['colonies']['0']['actual_pop_sum'],6337)
check('actual_return100',v['eep_last_return'],100)
check('actual_mixed_source_shattered',done['planets']['13']['planet_class'],'pc_shattered')
check('actual_mixed_source_unowned','owner' in done['planets']['13'],False)
check('actual_root_stock_after_generic_preserved',done['countries']['0']['stockpile'],start['countries']['0']['stockpile'])
check('actual_core_population_all_current_main48',sorted({g['key']['species'] for g in done['pop_groups'].values() if g['planet']==0}),[48])
check('actual_cumulative_generic_remainder2',v['eep_g']%6,2)
check('actual_unique_court_modifier',done['planets']['8']['modifiers'].count('modifier="eep_court"'),1)
result={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','version':'0.2.0-rc.6','language':'l_simp_chinese','checks':checks,
        'saves':{n:x['save_sha256'] for n,x in zip(names,states,strict=True)},'native_country_count':len(original['countries']),'foreign_country_ids':foreign_ids,
        'foreign_raw_hashes':{i:hashlib.sha256(raw_countries[0][i].encode('utf-8')).hexdigest() for i in foreign_ids},
        'scope':'Same country natural nativeQ20 C20/G0 followed by controlled organic-main genericQ20 endpoint C40/G20/D12/made300. Artificial species conversion and constructed source explicitly scoped; not legal natural genetic conversion or second natural48-month completion. All non0 raw country blocks and complete audit fields compared; foreign physical colony/pop/job/species isolation covers audited physical planets, not unparsed Arkship or fleet structures. Failed trait-only precondition retained.'}
out=run/'rc6-same-country-native20-generic20-all-foreign-isolation-proof.json'
assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=list)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'native_countries':len(original['countries']),'failed':[{'check':c['check'],'actual':c['actual'] if isinstance(c['actual'],(str,int,bool,list)) else 'see full raw report'} for c in checks if c['status']=='FAIL']}))
