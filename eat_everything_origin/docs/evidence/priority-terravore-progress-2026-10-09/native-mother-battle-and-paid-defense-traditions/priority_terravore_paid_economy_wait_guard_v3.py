"""Read-only post-settlement paid construction; no UI or calendar mutation."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,end,days,mining,generator,hive=sys.argv[1:];days,mining,generator,hive=map(int,(days,mining,generator,hive));assert hive>0
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0]
 messages=[v for k,v,o in fs if k=='message' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD']
 cons=roots['construction'];queue=q.block(q.block(q.block(cons,'queue_mgr'),'queues'),'0')
 items={k:v for k,v,o in q.fields(q.block(q.block(cons,'item_mgr'),'items')) if o}
 orders={str(i):items[str(i)] for i in q.ids(q.block(queue,'items'))}
 return a,pending,messages,orders
b,bp,bm,bo=read(before);a,ap,am,ao=read(after);bc,ac=b['countries']['0'],a['countries']['0'];core=a['planets']['7'];source=a['planets']['90']
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
def levels(v):return {v['districts'][str(i)]['type']:v['districts'][str(i)]['level'] for i in v['colonies']['0']['districts']}
def workers(v):return {j['type']:{k:j[k] for k in ['workforce','max_workforce','workforce_limit']} for j in v['pop_jobs'].values() if j['planet']==0 and j['type'] in ['mining_drone','technician_drone','maintenance_drone']}
bl,al=levels(b),levels(a);bw,aw=workers(b),workers(a)
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['last_month']['balance'].values()),D(0)) for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']}
checks={'actual_total_districts_within_original_size_plus_permanent_capacity':sum(al.values())<=core['planet_size']+core['variables']['eep_capacity_value'],'actual_calendar_date_and_receipt':a['date']==end and receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==days and receipt['start_date']==b['date'] and receipt['date']==a['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'no_country_pending':not bp and not ap,
 'all_EEP_ledger_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'C17_G0_D6_made0_worlds1':all(ac['variables'][k]==v for k,v in {'eep_c':17,'eep_g':0,'eep_d':6,'eep_made':0,'eep_worlds':1}.items()),
 'no_new_bite_message':all(am.count(x)<=bm.count(x) for x in am) and all(am.count(x)==bm.count(x) or q.scalars(x).get('end','9999.12.30')<=a['date'] for x in bm),
 'no_new_active_task':not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'source_still_unowned_shattered':source.get('owner') is None and source.get('controller') is None and source['planet_class']=='pc_shattered' and not source['deposits'],
 'source_no_actual_population':not any(p['planet']==15 and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned':bc['owned_colonies']==ac['owned_colonies']==[0],
 'native_AP_and_traditions_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'unique_original_core_capacity6_size18':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==6,
 'one_permanent_capacity6':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*6\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])),
 'court_and_original_deposit_held':core['modifiers'].count('modifier="eep_court"')==1 and [(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'exact_paid_completed_district_levels':al.get('district_mining')==mining and al.get('district_generator')==generator and al.get('district_hive')==hive and {k:v for k,v in al.items() if k not in ['district_mining','district_generator','district_hive']}=={k:v for k,v in bl.items() if k not in ['district_mining','district_generator','district_hive']},
 'paid_native_queue_prefix_only_consumed':list(ao)==list(bo)[len(bo)-len(ao):] and all(q.block(ao[i],'resources')==q.block(bo[i],'resources') and q.block(ao[i],'buildable_district')==q.block(bo[i],'buildable_district') for i in ao),
 'mining_and_generator_workers_not_reduced':all(aw[k]['workforce']>=bw[k]['workforce'] and aw[k]['max_workforce']>=bw[k]['max_workforce'] for k in ['mining_drone','technician_drone']),
 'all_actual_stocks_nonnegative':all(D(str(v))>=0 for v in ac['effective_stockpile'].values()),
 'source_species_and_binding_held':a['species']==b['species'] and a['event_targets']==b['event_targets'],
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-postsettlement-month-error-after.log').read_bytes()}
proof={'status':'PASS_TERRAVORE_PAID_CONSTRUCTION_WAIT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'pending_before_after':[bp,ap],'actual_district_levels_before_after':[bl,al],'actual_workers_before_after':[bw,aw],'actual_queue_before_after':[bo,ao],'actual_stockpile':ac['effective_stockpile'],'actual_last_month_net':{k:str(v) for k,v in net.items()},'actual_population_before_after':[b['colonies']['0']['actual_pop_sum'],a['colonies']['0']['actual_pop_sum']],'newly_completed_technologies':sorted(set(ac['completed_technologies'])-set(bc['completed_technologies'])),'scope':'Paid native construction period and end state only. No multi-month budget residual, long-term closure or full civic route claim.'}
out=run/(after+'-paid-wait-v3-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original paid construction period FAIL retained; no next calendar'
