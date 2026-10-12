"""One 24-day native month boundary, expected EEP32 and report snapshots only."""
import json,logging,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-native-project3-started';a=read_state(run,before);p=load(before+'-project3-start-proof.json');x=load(before+'-project3-start-guard-execution.json')
sources=[]
for rel in ['events/eep_events.txt','common/scripted_effects/eep_effects.txt','common/on_actions/eep_on_actions.txt']:
 src=h.MOD_ROOT/rel;dst=run/('terravore-queen32-source-'+src.name);raw=src.read_bytes()
 if dst.exists():assert dst.read_bytes()==raw
 else:dst.write_bytes(raw)
 sources.append({'path':str(src),'preserved':dst.name,'sha256':h.sha256(src)})
levels=[q.unquote(v) for k,v,obj in q.fields(q.block(a['country'],'crisis_progression')) if k=='level' and not obj];c=a['audit']['countries']['0']
checks={
 'prior9PASS0_source_SHA_and_original_SAV':len(p['checks'])==9 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='dbbe0d366047570c4dd7a89604c842245515e12d31f7b5f965d79c9d7f13a4bc' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'native3_EEP2_and_existing_first_notice_no_pending':levels==['crisis_level_1','crisis_level_2','crisis_level_3'] and c['variables']['eep_fleet_stage']==c['variables']['eep_crisis']==2 and 'eep_fleet_notice' in c['flags'] and not a['pending'] and p['boundaries']==['native_project3_start_and_Queen32_review'],
 'only24day_no_lab_settlement_or_annual_bite_before_next_month':a['audit']['date']=='2282.10.07' and q.scalars(a['items']['184549419'])['progress']==249.2 and 249.2+24*1.4<360 and a['audit']['situations']['167772163']['progress']==23 and a['audit']['planets']['1578']['flags']['recently_eaten_planet']['flag_days']==54,
 'CN_production_sources_held_error627':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and all(h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(before+'-queen32-month-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2282.10.07','end_date':'2282.11.01','days':24,'maximum_days':24,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-queen32-month-review','sources':sources,'scope':'24 normal native days; EEP32 and report snapshots independently checked, no research tick presumed at month1.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
