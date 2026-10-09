"""One native precursor option; independently verify its bounded actual effects."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
before='terravore-colonization-wait-year1';stage='terravore-precursor-ack'
def read(stem):
    a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
    with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
    pending=[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
    return a,t,roots,pending
b,bt,br,bp=read(before);assert len(bp)==1 and q.scalars(bp[0])['id']==4 and q.scalars(bp[0])['event']=='cstorms.205'
assert q.scalars(q.block(q.block(bp[0],'scope'),'from'))['id']==388
f=r.gpu_capture(stage+'-before');labels=[v['text'] for v in f['rows']]
assert b['date'] in labels and '\u6682\u505c' in labels and '\u4ec1\u5584\u4fe1\u53f7' in labels
rows=[v for v in f['rows'] if v['text']=='\u5f88\u8ff7\u4eba\u3002' and v['score']>=.8];assert len(rows)==1
eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
row=rows[0];h.click_point(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),stage+'-normal-option0')
f2=r.gpu_capture(stage+'-after-option');labels=[v['text'] for v in f2['rows']]
dates=[s for s in labels if re.fullmatch(r'2205\.05\.0[12]',s)]
assert len(dates)==1 and '\u6682\u505c' in labels,'Preserve actual UI; do not replay option'
a=r.native_save(stage,dates[0],(0,));a,at,ar,ap=read(stage)
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
bc,ac=b['countries']['0'],a['countries']['0']
bs={k:v for k,v,o in q.fields(q.block(br['archaeological_sites'],'sites')) if o}
ass={k:v for k,v,o in q.fields(q.block(ar['archaeological_sites'],'sites')) if o}
added={i:v for i,v in ass.items() if i not in bs}
checks={'actual_date_no_month_boundary':a['date'] in ['2205.05.01','2205.05.02'],
 'original_save_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(stage+'.sav'))==a['save_sha256'],
 'only_pending4_removed':not ap,
 'one_native_history':selected_history(at)==selected_history(bt)+[{'player_event':4,'human':1,'option':0}],
 'native_society_bank_reward350':ac['research_stockpile']=={**bc['research_stockpile'],'society_research':350},
 'other_effective_stocks_held':{k:v for k,v in ac['effective_stockpile'].items() if k!='society_research'}=={k:v for k,v in bc['effective_stockpile'].items() if k!='society_research'},
 'tech_status_except_native_bank_held':[(k,v,o) for k,v,o in q.fields(ac['tech_status']) if k!='stored_techpoints']==[(k,v,o) for k,v,o in q.fields(bc['tech_status']) if k!='stored_techpoints'],
 'old_archaeological_objects_held':all(ass.get(i)==v for i,v in bs.items()),
 'one_correct_site_on388':len(added)==1 and all(q.scalars(v).get('type')=='site_adakkaria_the_propaganda_station' and q.scalars(q.block(v,'location'))=={'type':2,'id':388} for v in added.values()),
 'EEP_full_ledger_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'no_new_error_bytes':eb==ea}
for k in ['government','traditions','ascension_perks','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','districts','species','event_targets','deposits','situations','planets']:checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_PRECURSOR_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_date':a['date'],'bank_before':bc['research_stockpile'],'bank_after':ac['research_stockpile'],'added_sites_raw':added,'source_UI_sha256':f['image_sha256'],'scope':'One normal cstorms.205 option, native archaeology and society bank reward only; not an EEP reward or full route acceptance.'}
out=run/(stage+'-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original native option difference retained; do not replay'
