"""Normally acknowledge the real opening event once and check exact state isolation."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
for source in [Path(__file__),Path('_runtime/heart-of-devouring/native_selected_history.py')]:
    dest=run/source.name
    if dest.exists():assert dest.read_bytes()==source.read_bytes()
    else:shutil.copyfile(source,dest)
before='terravore-queen-opening-pending';stage='terravore-queen-opening-ack'
def raw(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    fields=list(q.fields(t));objects={k:v for k,v,o in fields if o}
    pending=[q.scalars(v) for k,v,o in fields if k=='player_event' and o and q.scalars(v).get('country')==0]
    return t,objects,pending
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));bt,br,bp=raw(before)
assert len(bp)==1 and bp[0]['event']=='eep.10' and bp[0]['id']==1
f=r.gpu_capture(stage+'-before-click');labels=[v['text'] for v in f['rows']]
assert '2200.01.03' in labels and '暂停' in labels and '唯一的王座' in labels
rows=[v for v in f['rows'] if v['text']=='王座之外，皆可吞噬。' and v['score']>=0.8]
assert len(rows)==1
eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
row=rows[0];h.click_point(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),stage+'-normal-option0')
h.press_scan_code(0x01,stage+'-menu-after-normal-option',1)
a=r.native_save(stage,'2200.01.03',(0,));at,ar,ap=raw(stage)
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
bh,ah=selected_history(bt),selected_history(at)
checks={'same_paused_date':a['date']==b['date']=='2200.01.03','no_new_errors':ea==eb,
        'only_opening_pending_removed':len(bp)==1 and not ap,
        'one_normal_opening_history_record':len(ah)==len(bh)+1 and ah[:len(bh)]==bh and ah[-1]['player_event']==1 and ah[-1]['option']==0,
        'empty_EEP_tasks':not any(v.get('type')=='situation_eep_devouring' for v in a['situations'].values())}
bc,ac=b['countries']['0'],a['countries']['0']
for key in ['effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies','native']:
    checks[key+'_held']=bc[key]==ac[key]
for key in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:
    checks[key+'_held']=b[key]==a[key]
for key in ['country','construction','buildings','zones','leaders','player']:
    checks['raw_'+key+'_held']=br[key]==ar[key]
proof={'status':'PASS_NATIVE_TERRAVORE_OPENING_ACK' if all(checks.values()) else 'FAIL','checks':checks,
       'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
       'actual_new_history':ah[len(bh):],'source_UI_image_sha256':f['image_sha256'],
       'scope':'Normal opening option once at the same paused date; exact native economy and EEP isolation. Not full route acceptance.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original opening-ACK failure retained; no replay'
