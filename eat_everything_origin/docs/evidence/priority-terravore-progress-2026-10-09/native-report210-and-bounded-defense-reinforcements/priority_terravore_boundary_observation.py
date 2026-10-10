"""Read-only actual boundary data; observations are not full settlement acceptance."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,date,raw_days=sys.argv[1:];days=int(raw_days)
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 col={k:v for k,v,o in q.fields(roots['colony']) if o and k in ['0','15']}
 growth={i:{k:v for k,v,o in q.fields(raw) if 'growth' in k} for i,raw in col.items()}
 messages=[v for k,v,o in fs if k=='message' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD']
 pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0]
 species_pop={}
 for pop in a['pop_groups'].values():
  key=str(pop['planet'])+':'+str(pop['key']['species']);species_pop[key]=species_pop.get(key,0)+pop['size']
 return a,growth,messages,pending,species_pop
b,bg,bm,bp,bs=read(before);a,ag,am,ap,ass=read(after)
bc,ac=b['countries']['0'],a['countries']['0'];receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text(encoding='utf-8'))
elapsed=lambda s:sum(x*y for x,y in zip(map(int,s.split('.')),[360,30,1]))
checks={'actual_date_and_day_difference':a['date']==date and elapsed(a['date'])-elapsed(b['date'])==days,
 'source_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_native_calendar_receipt':receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==days and receipt['start_date']==b['date'] and receipt['date']==date,
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-native-devour-start-error-before.log').read_bytes()}
resources=set(bc['effective_stockpile'])|set(ac['effective_stockpile'])
proof={'status':'OBSERVED_NATIVE_TERRAVORE_BOUNDARY' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'before_date':b['date'],'after_date':a['date'],
 'before_growth':bg,'after_growth':ag,'before_native_bite_messages':bm,'after_native_bite_messages':am,'before_species_population':bs,'after_species_population':ass,'before_pending':bp,'after_pending':ap,'before_EEP_variables':bc['variables'],'after_EEP_variables':ac['variables'],'after_EEP_flags':ac['flags'],
 'actual_stock_deltas':{k:str(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))) for k in sorted(resources)},'before_budgets':bc['budget_categories'],'after_budgets':ac['budget_categories'],'after_source':a['planets']['90'],'after_situations':a['situations'],
 'scope':'Original native boundary observations only. No full population/budget reconciliation, settlement or route PASS inferred from this observer.'}
out=run/(after+'-boundary-observation.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({k:v for k,v in proof.items() if k in ['status','checks','before_date','after_date','after_EEP_variables','after_pending','actual_stock_deltas','before_species_population','after_species_population']}),flush=True);assert all(checks.values())
