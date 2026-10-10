"""Preserve original FAIL, verify the actual native progress.4 option3."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
before='terravore-capital-contact-hostile';after='terravore-capital-progress-ack';original=json.loads((run/(after+'-notice-effect-proof.json')).read_text('utf-8'))
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:return z.read('gamestate').decode('utf-8-sig')
source=h.GAME_EXE.parent/'events/progress_events.txt';ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='progress.4'];opts=[v for k,v,o in q.fields(ev[0]) if k=='option'];option=opts[3]
checks={'original26_exact_history_FAIL_retained':len(original['checks'])==26 and [k for k,v in original['checks'].items() if v is not True]==['exact_once_selection_history'] and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==1,
 'original_SHA_pair_and_source_held':original['before_sha256']==h.sha256(run/(before+'.sav')) and original['after_sha256']==h.sha256(run/(after+'.sav')) and original['native_source']['sha256']==h.sha256(source),
 'actual_option3_effect_free':q.scalars(option).get('name')=='progress.4.d' and all(k in ['name','trigger'] for k,v,o in q.fields(option)),
 'actual_history_only_141_option3':selected_history(read(after))==selected_history(read(before))+[{'player_event':141,'human':1,'option':3}]}
p={'status':'PASS_NATIVE_PROGRESS_OPTION3_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':original['before_sha256'],'after_sha256':original['after_sha256'],'actual_option_index':3,'original_proof':after+'-notice-effect-proof.json','scope':'Only corrects original option index; original other25 checks and FAIL preserved. Two tutorial notices remain.'};out=run/(after+'-option3-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p));assert all(checks.values())
