import copy,json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
shutil.copyfile(__file__,run/Path(__file__).name)
before='organic-mine5-ordered';stage='organic-third-temple-ordered'
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
def construction(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:raw=z.read('gamestate').decode('utf-8-sig')
    c=q.block(raw,'construction');queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0');items=q.block(q.block(c,'item_mgr'),'items');ids=q.ids(q.block(queue,'items'))
    return ids,{str(i):q.block(items,str(i)) for i in ids},raw
bid,bi,bt=construction(before);assert bid==[167772186,167772187]
f=r.gpu_capture(stage+'-real-native-price');labels=[v['text'] for v in f['rows']]
assert '\u5bfa\u5e99' in labels and '360400' in labels
# Point supplied only after actual native Temple card geometry is verified.
point=json.loads((run/'organic-third-temple-verified-point.json').read_text(encoding='utf-8'))
assert point['building']=='building_temple' and point['minerals']==400 and point['days']==360
h.click_point(*point['client_point'],stage+'-native-build-once')
a=r.native_save(stage,b['date'],(0,));aid,ai,at=construction(stage);bc,ac=b['countries']['0'],a['countries']['0']
item=ai[str(aid[-1])] if len(aid)==3 else '';s=q.scalars(item);expected=copy.deepcopy(b['colonies']);expected['0']['last_building_changed']='building_temple'
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date']=='2305.05.02','actual400_minerals_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==400,'all_other_actual_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},'native_appended_only_one_item':len(aid)==3 and aid[:-1]==bid,'old_two_orders_raw_held':all(ai.get(str(i))==bi[str(i)] for i in bid),'exact_temple_mother_archive_zone':q.scalars(q.block(item,'buildable_planet_building'))=={'building':'building_temple','planet':0,'zone':1},'native0_of360':s.get('progress')==0 and s.get('progress_needed')==360,'native_paying_country_queue0':s.get('queue')==s.get('paying_country')==0,'native_cost400':q.scalars(q.block(item,'resources'))=={'minerals':400},'only_exact_last_building_operation_record':a['colonies']==expected,'all_raw_buildings_held':q.block(bt,'buildings')==q.block(at,'buildings'),'all_raw_zones_held':q.block(bt,'zones')==q.block(at,'zones'),'no_new_errors':eb==ea}
for k in ('research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','planets','districts','deposits','situations','species'):checks[k+'_held']=a[k]==b[k]
p={'status':'PASS_NATIVE_THIRD_TEMPLE_ORDER' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_queue_ids':aid,'native_order_raw':item,'actual_minerals_after':ac['effective_stockpile']['minerals'],'scope':'One real400-mineral/360-day third Temple appended after PsiCorps and Mine5. No early jobs, Unity income or completion.'}
h.write_json(run/(stage+'-proof.json'),p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original third temple order FAIL retained; do not repay'
