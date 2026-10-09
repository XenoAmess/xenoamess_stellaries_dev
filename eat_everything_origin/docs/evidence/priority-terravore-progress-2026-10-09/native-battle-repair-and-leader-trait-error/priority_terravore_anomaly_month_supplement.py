"""Read-only original anomaly plus one real monthly boundary; not same-date ACK."""
import hashlib,json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)

def read(name):
    a=json.loads((run/(name+'.audit.json')).read_text(encoding='utf-8'))
    with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    fs=list(q.fields(t));roots={k:v for k,v,b in fs if b}
    pending=[v for k,v,b in fs if b and k=='player_event' and q.scalars(v).get('country')==0]
    return a,t,roots,pending
b,bt,br,bp=read('terravore-clock-pause-recovered');a,at,ar,ap=read('terravore-native-physics-deposit-ack')
bc,ac=b['countries']['0'],a['countries']['0']
residual={}
for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']:
    net=sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))
    residual[k]=str(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))-net)
bd={i:v for i,v,o in q.fields(br['deposit']) if o};ad={i:v for i,v,o in q.fields(ar['deposit']) if o}
added={i:v for i,v in ad.items() if i not in bd}
bv=q.scalars(q.block(q.block(br['country'],'0'),'variables'));av=q.scalars(q.block(q.block(ar['country'],'0'),'variables'))
expected=dict(bv);expected['aianom_physics_depo3']=bv.get('aianom_physics_depo3',0)+1
planet=lambda roots:q.block(q.block(roots['planets'],'planet'),'164')
checks={'actual_one_day_month_boundary':b['date']=='2204.04.30' and a['date']=='2204.05.01',
        'original_pending3_aianom8_removed':len(bp)==1 and q.scalars(bp[0])['id']==3 and q.scalars(bp[0])['event']=='aianom.8' and not ap,
        'one_original_normal_choice_history':selected_history(at)==selected_history(bt)+[{'player_event':3,'human':1,'option':0}],
        'one_exact_physics3_deposit_added':len(added)==1 and '150996490' in added and q.scalars(added['150996490']).get('type')=='d_physics_3' and q.scalars(q.block(added['150996490'],'deposit_holder'))=={'type':0,'id':164},
        'old_global_deposits_held':all(ad.get(i)==v for i,v in bd.items()),
        'actual_foreign_planet_reference':q.ids(q.block(planet(ar),'deposits'))==q.ids(q.block(planet(br),'deposits'))+[150996490],
        'only_native_anomaly_counter_added':av==expected,
        'eight_actual_month_budget_residuals_zero':all(D(v)==0 for v in residual.values()),
        'complete_EEP_ledger_held':bc['variables']==ac['variables'],
        'EEP_flags_held':bc['flags']==ac['flags'],
        'same_legal_government_AP_traditions':all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions']),
        'mother_size18_capacity2_core_held':a['planets']['7']['planet_size']==18 and a['planets']['7']['variables']==b['planets']['7']['variables'] and a['planets']['7']['modifiers']==b['planets']['7']['modifiers'] and a['deposits']['1573']==b['deposits']['1573'],
        'no_EEP_source_task':not any(s.get('type')=='situation_eep_devouring' for s in a['situations'].values()),
        'source_colonization_growth3':a['colonies']['15']['actual_pop_sum']-b['colonies']['15']['actual_pop_sum']==3,
        'same_native_species':a['species']==b['species'],
        'no_new_errors':(user/'logs/error.log').stat().st_size==2670}
proof={'status':'PASS_SCOPED_ORIGINAL_ANOMALY_AND_NATIVE_MONTH' if all(checks.values()) else 'FAIL','checks':checks,
       'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'budget_residuals':residual,
       'actual_population_before_after':{i:[b['colonies'][i]['actual_pop_sum'],v['actual_pop_sum']] for i,v in a['colonies'].items()},
       'added_deposit_raw':added,'new_native_counter':{'aianom_physics_depo3':av.get('aianom_physics_depo3')},
       'scope':'Original same-date expectation failed and remains failed. Separate one-day/month budget and exact original anomaly effects, not full ACK isolation or clock acceptance.'}
out=run/'terravore-anomaly-month-supplement-proof.json';assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Supplement failure retained; do not replay original choice'
