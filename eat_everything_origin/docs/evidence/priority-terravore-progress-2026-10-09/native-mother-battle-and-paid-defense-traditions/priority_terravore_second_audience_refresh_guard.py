"""Exact same-day native audience snapshot refresh, with no economic or population effect."""
import copy,json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o};sc={k:q.unquote(v) for k,v,o in fs if not o}
 return a,t,fs,roots,sc
b,bt,bf,br,bsc=read(before);a,at,af,ar,asc=read(after)
pre=json.loads((run/(before+'-second-queen-ack-proof.json')).read_text('utf-8'))
bp=[v for k,v,o in bf if k=='player_event'];ap=[v for k,v,o in af if k=='player_event']
newp=[v for v in ap if q.scalars(v).get('id')==107];bp0=[q.scalars(v) for v in bp if q.scalars(v).get('country')==0]
bm=[v for k,v,o in bf if k=='message'];am=[v for k,v,o in af if k=='message'];newm=[v for v in am if v not in bm]
bplan=q.block(br['planets'],'planet');aplan=q.block(ar['planets'],'planet');b7=q.block(bplan,'7');a7=q.block(aplan,'7')
skip={'planets','message','last_event_id','random_count','player_event'}
checks={
 'bound_original_Queen26_PASS':pre['status']=='PASS_SECOND_TERRAVORE_QUEEN_ACK_COMPONENT' and len(pre['checks'])==26 and all(pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'actual_same_date_and_SHA_pair':b['date']==a['date']=='2233.08.01' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k not in skip]==[(k,v,o) for k,v,o in af if k not in skip],
 'exact_one_new107_eep100_other_pending_held':not bp0 and len(newp)==1 and q.scalars(newp[0])=={'id':107,'event':'eep.100','date':'2235.11.01','country':0} and [v for v in ap if v not in newp]==bp,
 'exact_last_event_id106_to107':bsc['last_event_id']==106 and asc['last_event_id']==107,
 'native_UI_counter_only_plus2':asc['random_count']==bsc['random_count']+2,
 'exact_one_new_report_notice_other_messages_held':len(newm)==1 and am==bm+newm and all(q.scalars(newm[0]).get(k)==v for k,v in {'type':'EVENT_MESSAGE_TYPE','receiver':0,'event':107,'date':'2233.08.01'}.items()),
 'all_countries_raw_held':br['country']==ar['country'],
 'planet_wrapper_other_fields_raw_held':[(k,v,o) for k,v,o in q.fields(br['planets']) if k!='planet']==[(k,v,o) for k,v,o in q.fields(ar['planets']) if k!='planet'],
 'all_other_physical_planets_raw_held':[(k,v,o) for k,v,o in q.fields(bplan) if k!='7']==[(k,v,o) for k,v,o in q.fields(aplan) if k!='7'],
 'core_other_fields_raw_held':[(k,v,o) for k,v,o in q.fields(b7) if k!='variables']==[(k,v,o) for k,v,o in q.fields(a7) if k!='variables'],
 'only_actual_population_snapshot_refresh':b['planets']['7']['variables']['eep_actual_pop']==8683 and a['planets']['7']['variables']=={**b['planets']['7']['variables'],'eep_actual_pop':a['colonies']['0']['actual_pop_sum']} and a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']==8689 and a['planets']['7']['variables']['eep_free_districts']==8,
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['effective_stockpile','variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_SECOND_TERRAVORE_AUDIENCE_REFRESH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_core_variables':a['planets']['7']['variables'],'scope':'Single native same-day read-only audience refresh. Snapshot equals current actual population, no grants; normal report acknowledgement and subsequent month pending.'}
out=run/(after+'-second-audience-refresh-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original audience refresh FAIL retained'
