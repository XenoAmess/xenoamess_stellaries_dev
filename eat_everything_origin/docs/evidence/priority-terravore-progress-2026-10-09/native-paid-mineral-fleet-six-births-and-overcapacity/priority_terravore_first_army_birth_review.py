"""Review exactly one native paid recruitment completion boundary."""
import json,logging,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'));sha=h.sha256
before='terravore-first-assault-army-prebirth';pre=load(before+'-army-wait-v4-proof.json');px=load(before+'-army-wait-guard-v4-execution.json');a=load(before+'.audit.json')
with zipfile.ZipFile(run/(before+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
roots={k:v for k,v,o in q.fields(t) if o};qs=q.block(q.block(roots['construction'],'queue_mgr'),'queues');items=q.block(q.block(roots['construction'],'item_mgr'),'items');c=q.block(roots['country'],'0');pay=load('terravore-three-assault-armies-paid-paid-armies-proof.json');payx=load('terravore-three-assault-armies-paid-guard-execution.json');source=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/armies/01_assault_armies.txt');raw=source.read_bytes();target=run/'terravore-native-assault-army-source.txt'
if target.exists():assert target.read_bytes()==raw
else:target.write_bytes(raw)
checks={
 'prior35_PASS_actual0_exact_source_SAV':len(pre['checks'])==35 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==sha(Path(px['command'][1]))=='d75cd3d94d3746ebb0c21013025322a40648942bcecbdbc726354b8385957134' and pre['after_sha256']==a['save_sha256']==sha(run/(before+'.sav')),
 'exact_one_day22790530_to22790601_review_only':a['date']=='2279.05.30' and pre['boundaries']==['native_first_assault_army_birth_requires_review'] and pre['maximum_days_to_native_bite_boundary']==0 and pre['native_devour_calendar_ready'] is False,
 'genuine_original_three300M_paid21_actual0':len(pay['checks'])==21 and all(v is True for v in pay['checks'].values()) and payx['returncode']==0 and payx['helper_sha256']==sha(Path(payx['command'][1]))=='49f3f7296b6ed96b7b98581c13bd8affd5633a35409277dc0d62d97779a17c74' and pay['actual_paid_minerals']==300,
 'exact_first89_next0_last0_90work_assault73_mother0':q.ids(q.block(q.block(qs,'1'),'items'))==[1375731723,1124073481,117440555] and all(q.scalars(q.block(items,i))=={'queue':1,'paying_country':0,'progress':progress,'progress_needed':90} and q.scalars(q.block(q.block(items,i),'resources'))=={'minerals':100} and q.scalars(q.block(q.block(items,i),'buildable_army'))=={'army_type':'assault_army','species':73,'planet':0,'starbase':4294967295} for i,progress in [('1375731723',89),('1124073481',0),('117440555',0)]),
 'native_army_source_basic90work_100M_1E_preserved':b'time = 90' in raw and b'minerals = 100' in raw and b'energy = 1' in raw and sha(source)==sha(target),
 'current_EEP_C62_M1635_mother_and_error_held':a['countries']['0']['variables']['eep_c']==62 and a['countries']['0']['effective_stockpile']['menace']==1635 and a['colonies']['0']['actual_pop_sum']==11965 and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 'no_current_unknown_pending':not any(k=='player_event' and o and q.scalars(v).get('country')==0 for k,v,o in q.fields(t)) and 'crisis_special_project_2_complete' not in q.scalars(q.block(c,'flags')),
}
passed=all(v is True for v in checks.values());out=run/'terravore-first-army-birth-review-proof.json';assert not out.exists();h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['save_sha256'],'after_sha256':a['save_sha256'],'start_date':'2279.05.30','end_date':'2279.06.01','days':1,'maximum_days':1,'allowed_boundaries':pre['boundaries'],'execution_stage':'terravore-first-army-birth-review','native_source_sha256':sha(source),'scope':'Single native work90 completion boundary and one normal month, no gifts or guarantee of instant auto-embark. Independent post-save audit required.'});print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
