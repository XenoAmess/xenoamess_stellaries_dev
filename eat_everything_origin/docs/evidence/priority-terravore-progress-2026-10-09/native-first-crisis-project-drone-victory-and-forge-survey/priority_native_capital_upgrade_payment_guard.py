"""Read-only exact normal native capital-upgrade payment, strict error bytes."""
import copy,json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,prior_file,prior_stage=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 rt={k:v for k,v,o in q.fields(t) if o};c=rt['construction'];qu=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0');it=q.block(q.block(c,'item_mgr'),'items');ids=q.ids(q.block(qu,'items'))
 return a,rt,qu,ids,{str(i):q.block(it,str(i)) for i in ids}
b,br,bq,bids,bi=read(before);a,ar,aq,aids,ai=read(after);bc,ac=b['countries']['0'],a['countries']['0'];item=ai.get(str(aids[0]),'') if len(aids)==1 else ''
pre=json.loads((run/prior_file).read_text('utf-8'));ex=json.loads((run/(prior_stage+'-execution.json')).read_text('utf-8'))
expected=copy.deepcopy(b['colonies']);expected['0']['last_building_changed']='building_hive_major_capital'
checks={
 'bound_prior_PASS_execution0':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_actual_date':b['date']==a['date']=='2238.10.02',
 'original_SHA_pair':all(h.sha256(run/(st+'.sav'))==v['save_sha256'] for st,v in [(before,b),(after,a)]),
 'actual480_minerals_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==480,
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'unique_native_mother_upgrade_order':not bids and len(aids)==1 and q.scalars(item)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':480},
 'native_order_resources480':q.scalars(q.block(item,'resources'))=={'minerals':480},
 'exact_building0_upgrade_in_zone0_colony0':q.scalars(q.block(item,'buildable_planet_upgrade_building'))=={'building':'building_hive_major_capital','planet':0,'zone':0,'upgrade_building':0},
 'physical_mother_planet7_queue_held':q.scalars(q.block(bq,'location'))==q.scalars(q.block(aq,'location'))=={'type':2,'id':7},
 'all_raw_zones_and_buildings_held':br['zones']==ar['zones'] and br['buildings']==ar['buildings'],
 'original_capital_type_and_zone_relation':q.scalars(q.block(br['buildings'],'0'))=={'type':'building_hive_capital','position':0} and 0 in q.ids(q.block(q.block(br['zones'],'0'),'buildings')),
 'colonies_only_exact_operation_record_changed':a['colonies']==expected,
 'unfiltered_error_original_bytes_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
for k in ['research_stockpile','tech_status','variables','flags','government','traditions','ascension_perks','budget_categories','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_CAPITAL_UPGRADE_PAYMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_order_raw':item,'native_queue_ids':aids,'scope':'One normal480-mineral capital upgrade order only, strict original log equality. Any FAIL retained; no repeat payment/calendar.'}
out=run/(after+'-capital-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original strict capital payment FAIL retained'
