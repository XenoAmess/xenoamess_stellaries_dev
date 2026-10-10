"""One normal original anomaly choice with an exact same-date native audit."""
import json, logging, shutil, sys, zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.path.insert(0,'_runtime/heart-of-devouring')
sys.argv=['runtime']
import runtime as r, audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO)
h=r.harness; run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists(): assert dest.read_bytes()==Path(__file__).read_bytes()
else: shutil.copyfile(__file__,dest)
before='terravore-clock-pause-recovered';stage='terravore-native-physics-deposit-ack'

def raw(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    fields=list(q.fields(t));roots={k:v for k,v,b in fields if b}
    pending=[v for k,v,b in fields if k=='player_event' and b and q.scalars(v).get('country')==0]
    return t,roots,pending

b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'))
bt,br,bp=raw(before)
assert len(bp)==1 and q.scalars(bp[0])['id']==3 and q.scalars(bp[0])['event']=='aianom.8'
f=r.gpu_capture(stage+'-before-click');labels=[v['text'] for v in f['rows']]
assert '2204.04.30' in labels and '\u6682\u505c' in labels and '\u7269\u7406\u5b66\u7814\u7a76\u50a8\u5907' in labels
rows=[v for v in f['rows'] if v['text']=='\u786e\u8ba4' and v['score']>=.8];assert len(rows)==1
eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
row=rows[0];h.click_point(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),stage+'-normal-option0')
h.press_scan_code(0x01,stage+'-menu-after-option',1)
a=r.native_save(stage,'2204.04.30',(0,));at,ar,ap=raw(stage)
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
added={i:v for i,v in a['deposits'].items() if i not in b['deposits']}
assert len(added)==1, 'Preserve original unexpected deposit set'
did,dep=next(iter(added.items()))
n=str(dep['type']).removeprefix('d_physics_'); assert n in ['2','3','4']
var='aianom_physics_depo'+n
bcraw=q.block(br['country'],'0');acraw=q.block(ar['country'],'0')
bv=q.scalars(q.block(bcraw,'variables'));av=q.scalars(q.block(acraw,'variables'))
expected=dict(bv);expected[var]=bv.get(var,0)+1
bh,ah=selected_history(bt),selected_history(at)
checks={'same_date':a['date']==b['date']=='2204.04.30','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(stage+'.sav'))==a['save_sha256'],
        'no_new_errors':eb==ea,'only_original_pending_removed':not ap,
        'one_normal_history_record':ah==bh+[{'player_event':3,'human':1,'option':0}],
        'one_correct_foreign_physics_deposit':dep.get('deposit_holder')=={'type':0,'id':164},
        'original_deposits_held':all(a['deposits'].get(i)==v for i,v in b['deposits'].items()),
        'foreign_planet_deposit_reference':a['planets']['164']['deposits']==b['planets']['164']['deposits']+[int(did)],
        'only_one_native_country_counter':av==expected,
        'country_except_variables_held':[(k,v,o) for k,v,o in q.fields(bcraw) if k!='variables']==[(k,v,o) for k,v,o in q.fields(acraw) if k!='variables']}
for key in ['effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies','native']:
    checks[key+'_held']=b['countries']['0'][key]==a['countries']['0'][key]
for key in ['pop_groups','pop_jobs','colonies','districts','situations','species','event_targets']:
    checks[key+'_held']=b[key]==a[key]
checks['all_planets_except_one_deposit_reference_held']=all(
    a['planets'].get(i)==v if i!='164' else {k:x for k,x in a['planets'][i].items() if k!='deposits'}=={k:x for k,x in v.items() if k!='deposits'}
    for i,v in b['planets'].items()) and set(a['planets'])==set(b['planets'])
for key in ['ships','construction','buildings','zones','leaders','player']:
    checks['raw_'+key+'_held']=br[key]==ar[key]
proof={'status':'PASS_NATIVE_ANOMALY_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
       'added_deposit':added,'counter':var,'before_counter':bv.get(var,0),'after_counter':av.get(var),
       'source_UI_sha256':f['image_sha256'],'scope':'Normal original aianom.8 option; foreign deposit and one native counter only. No EEP reward or clock validation.'}
out=run/(stage+'-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original anomaly difference retained; do not replay'
