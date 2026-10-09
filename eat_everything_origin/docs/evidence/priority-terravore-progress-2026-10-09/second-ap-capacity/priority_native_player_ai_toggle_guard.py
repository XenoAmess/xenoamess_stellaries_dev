"""Read-only exact paused-state check of an observed native player-AI toggle."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after,command_stage,receipt_stage,mode=sys.argv[1:];assert mode in ['on','off']
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'))
a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'))
ob=json.loads((run/(after+'-observation.json')).read_text(encoding='utf-8'))
action=json.loads((run/(command_stage+'.action.json')).read_text(encoding='utf-8'))
f=json.loads((run/(receipt_stage+'.ocr.json')).read_text(encoding='utf-8'))
labels=[v['text'] for v in f['rows']]
receipts=[s for s in labels if h.normalized(s) in ['humanaiisnow'+mode,'humanalisnow'+mode]]
def raw(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    fields=list(q.fields(t));obj={k:v for k,v,o in fields if o}
    pending=[q.scalars(v) for k,v,o in fields if k=='player_event' and o and q.scalars(v).get('country')==0]
    return t,obj,pending
bt,br,bp=raw(before);at,ar,ap=raw(after)
checks={'same_expected_paused_date':a['date']==b['date'] and a['date'] in labels and '暂停' in labels,
        'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
        'actual_one_human_ai_command':action['text']=='human_ai' and action['submitted'] is True,
        'full_bound_native_toggle_receipt':len(receipts)==1 and h.sha256(Path(f['image']))==f['image_sha256'],
        'no_new_errors':ob['new_error_bytes']==0 and ob['error_prefix_held'] is True,
        'no_country0_pending':not bp and not ap,'selection_history_held':selected_history(bt)==selected_history(at)}
bc,ac=b['countries']['0'],a['countries']['0']
for key in ['effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies','native']:
    checks[key+'_held']=bc[key]==ac[key]
for key in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:
    checks[key+'_held']=b[key]==a[key]
for key in ['country','construction','buildings','zones','leaders','player']:
    checks['raw_'+key+'_held']=br[key]==ar[key]
proof={'status':'PASS_NATIVE_PLAYER_AI_TOGGLE_ISOLATION' if all(checks.values()) else 'FAIL','checks':checks,
       'mode':mode,'actual_full_receipt':receipts,'source_UI_sha256':f['image_sha256'],
       'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
       'scope':'Native player automation toggle; exact same-date economy held. Not is_ai true-country branch acceptance.'}
out=run/(after+'-toggle-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original toggle check failure retained; do not replay'
