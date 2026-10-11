"""Read-only documented native construction inventory; not completion acceptance."""
import hashlib,json,logging,re,sys,zipfile
from decimal import Decimal as D
before,after=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8'))
def read(st):
    audit=load(st+'.audit.json')
    with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    roots={k:v for k,v,o in fs if o};country=q.block(roots['country'],'0')
    fleets={k:v for k,v,o in q.fields(roots['fleet']) if o};ships={k:v for k,v,o in q.fields(roots['ships']) if o}
    owned=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(country,'fleets_manager'),'owned_fleets'))))
    ids=sorted({i for fid in owned for i in q.ids(q.block(fleets[str(fid)],'ships'))})
    messages=[v for k,v,o in fs if k=='message' and o and q.scalars(v).get('receiver')==0]
    pending=[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
    pops={}
    for group in audit['pop_groups'].values():
        key=str(group['planet'])+':'+str(group['key']['species']);pops[key]=pops.get(key,0)+group['size']
    return {'audit':audit,'country0_raw':country,'owned_fleets':owned,'owned_ship_ids':ids,
        'owned_fleets_raw':{str(i):fleets[str(i)] for i in owned},'owned_ships_raw':{str(i):ships[str(i)] for i in ids},
        'original_ship16779140_entry':[(v,o) for k,v,o in q.fields(roots['ships']) if k=='16779140'],
        'original_fleet16778062_entry':[(v,o) for k,v,o in q.fields(roots['fleet']) if k=='16778062'],
        'messages_country0_raw':messages,'pending_country0_raw':pending,'species_population_by_colony':pops,
        'planet_raw':{i:q.block(q.block(roots['planets'],'planet'),i) for i in ['7','1085','523']},
        'colony_raw':{i:q.block(roots['colony'],i) for i in ['0','37']},
        'raw_roots':{k:roots[k] for k in ['districts','zones','buildings','deposit','situations','construction','ship_design','open_player_event_selection_history','starbase_mgr','colony']},
        'war1_battles_raw':q.block(q.block(roots['war'],'1'),'battles'),
        'first_contact16777275_raw':q.block(q.block(roots['first_contacts'],'contacts'),'16777275'),
        'countries_raw':{k:v for k,v,o in q.fields(roots['country']) if o},'mother_base0_raw':q.block(q.block(roots['starbase_mgr'],'starbases'),'0'),'colonizer_design150995039_raw':q.block(roots['ship_design'],'150995039'),'enemy825_raw':q.block(roots['fleet'],'825'),'rear153_raw':q.block(q.block(roots['starbase_mgr'],'starbases'),'153'),'top_fields_content_sha256':[(k,o,hashlib.sha256(v.encode('utf-8')).hexdigest()) for k,v,o in fs],'top_fields_ordered':[(k,o) for k,v,o in fs]}

b,a=read(before),read(after);ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0']
pre=load(before+'-target523-colonization-begin-proof.json');pe=load(before+'-colonization-begin-guard-execution.json');se=load(after+'-native-save-execution.json');so=load(after+'-observation.json')
base=lambda st:q.block(q.block(st['raw_roots']['starbase_mgr'],'starbases'),'158')
queues=lambda st:q.block(q.block(st['raw_roots']['construction'],'queue_mgr'),'queues')
items=lambda st:q.block(q.block(st['raw_roots']['construction'],'item_mgr'),'items')
bq,aq=[q.block(queues(st),'2285') for st in [b,a]]
order=q.block(items(a),'1509949442')
manifest,tree=h.tree_manifest(h.MOD_ROOT)
checks={
 'original_begin11_PASS_actual0_SHA':pre['status'].startswith('PASS_') and len(pre['checks'])==11 and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_fourth_colonization_begin_guard.py')=='3e60e32cdb3494d2ad710337498f1a87253098fc818706a19ec575b3dc5846ca' and pre['after_sha256']==ba['save_sha256'],
 'same_native_date_SAV_pair':ba['date']==aa['date']=='2273.11.28' and all(st['audit']['save_sha256']==h.sha256(run/(name+'.sav')) for st,name in [(b,before),(a,after)]),
 'normal_click_save_actual0_source':se['returncode']==0 and se['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and so['status']=='OBSERVED_NATIVE_SAVE' and so['new_error_bytes']==0 and so['save_sha256']==aa['save_sha256'] and load('terravore-front37-paid-starport-upgrade-ui-execution.json')['returncode']==0 and load('terravore-front37-paid-starport-upgrade-ui.action.json')['client_point']==[414,376],
 'exact_alloy125_other_true_stocks_banks_held':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==125 and {k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'} and bc['research_stockpile']==ac['research_stockpile'],
 'mother_colony38_EEP_tech_government_population_held':all(ba[k]==aa[k] for k in ['colonies','planets','pop_groups','pop_jobs','districts','species','event_targets','situations']) and all(bc[k]==ac[k] for k in ['variables','flags','government','ascension_perks','traditions','tech_status','owned_colonies']),
 'native_single_paid_upgrade_order_target158':not q.ids(q.block(bq,'items')) and q.ids(q.block(aq,'items'))==[1509949442] and q.scalars(aq)=={'owner':0,'simultaneous':1,'type':'starbase'} and q.scalars(q.block(aq,'location'))=={'type':0,'id':1931} and q.scalars(order)=={'queue':2285,'paying_country':0,'progress':0,'progress_needed':360} and q.scalars(q.block(order,'resources'))=={'alloys':125} and q.scalars(q.block(order,'buildable_starbase_upgrade'))=={'starbase_upgrade':'starbase_level_starport','starbase':158},
 'original_base158_station1931_fleet849_no_completion':base(b)==base(a) and q.scalars(base(a))['level']=='starbase_level_outpost' and q.scalars(base(a))['station']==1931 and b['owned_ships_raw']['1931']==a['owned_ships_raw']['1931'] and q.scalars(a['owned_ships_raw']['1931'])['fleet']==849,
 'no_new_owned_ship_original_colony38_target_held':set(b['owned_ship_ids'])==set(a['owned_ship_ids']) and b['planet_raw']['523']==a['planet_raw']['523'] and q.block(b['raw_roots']['colony'],'38')==q.block(a['raw_roots']['colony'],'38'),
 'known_pending_and_other_countries_held':b['pending_country0_raw']==a['pending_country0_raw'] and {k:v for k,v in b['countries_raw'].items() if k!='0'}=={k:v for k,v in a['countries_raw'].items() if k!='0'},
 'production41_Chinese_original_error':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(manifest)==41 and tree=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
passed=all(v is True for v in checks.values())
p={'status':'PASS_NATIVE_TERRAVORE_FRONT158_STARPORT_PAYMENT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'before_state':b,'after_state':a,'paid_births':pre['paid_births'],'paid_upgrade_order':1509949442,'paid_upgrade_raw':order,'native_colonization_calendar_ready':passed,'maximum_days_to_colonization_boundary':21 if passed else 0,'scope':'Same-day actual paid starport order only; no completed upgrade, colony completion or full acceptance.'}
out=run/(after+'-front-starport-payment-proof.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed
