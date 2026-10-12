"""Read-only documented native construction inventory; not completion acceptance."""
import json,logging,re,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,end,raw_days=sys.argv[1:];days=int(raw_days)
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
from formal_production_native_calendar_checked_v3 import validate_business_interval
from priority_native_reviewed_error_baseline import reviewed_error_pair
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
        'raw_roots':{k:roots[k] for k in ['districts','zones','buildings','deposit','situations','construction','ship_design','open_player_event_selection_history']},
        'war1_battles_raw':q.block(q.block(roots['war'],'1'),'battles'),
        'first_contact16777275_raw':q.block(q.block(roots['first_contacts'],'contacts'),'16777275'),
        'top_fields_ordered':[(k,o) for k,v,o in fs]}
b,a=read(before),read(after);ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0']
cal=load(after+'-calendar-receipt.json');ce=load(after+'-calendar-execution.json')
pre=load(cal['prior_proof_file']);pe=load(cal['prior_execution_stage']+'-execution.json')
validate_native_interval(ba['date'],aa['date'],days)
business_review_ok=True
if ce['helper_sha256'] in ['c0bd2c1b44adc36b746cc8e13d87754c7bad970cee870d4e87eb63ccbb176589','af7c1d33bebcf2c7763647401c6ba76398bc4e434000374b23fefe1d9cb31f76','736473506dec7a0255508961f4e3a163fbf7b06375528fce2371737a46d595b3']:
    review_name=cal.get('review_file')
    review=load(review_name) if review_name else None
    validate_business_interval(pre,ba['date'],aa['date'],days,review)
    if review is not None:
        review_ex=load(review['execution_stage']+'-execution.json')
        business_review_ok=(review_ex['returncode']==0 and review_ex['helper_sha256']==h.sha256(Path(review_ex['command'][1]))
            and review['after_sha256']==ba['save_sha256'] and cal['review_sha256']==h.sha256(run/review_name))
manifest,tree=h.tree_manifest(h.MOD_ROOT)
checks={
 'actual_date_and_360day_interval':aa['date']==end and cal['start_date']==ba['date'] and cal['date']==end and cal['days']==days,
 'original_SAV_SHA_pair':all(x['save_sha256']==h.sha256(run/(st+'.sav')) for st,x in [(before,ba),(after,aa)]),
 'checked_native_calendar_actual0_source':business_review_ok and cal['status']=='CALENDAR_CONFIRMED' and ce['returncode']==0 and ce['helper_sha256']==h.sha256(Path(ce['command'][1])) and (ce['helper_sha256']=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' or ce['helper_sha256'] in ['c0bd2c1b44adc36b746cc8e13d87754c7bad970cee870d4e87eb63ccbb176589','af7c1d33bebcf2c7763647401c6ba76398bc4e434000374b23fefe1d9cb31f76','736473506dec7a0255508961f4e3a163fbf7b06375528fce2371737a46d595b3'] and cal.get('business_preflight') is True),
 'prior_component_PASS_actual0_original_SHA':pre['status'].startswith('PASS_') and pre['checks'] and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pre['after_sha256']==ba['save_sha256'] and pe['helper_sha256']==h.sha256(Path(pe['command'][1])),
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(manifest)==41 and tree=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered_error_exact_reviewed_native_settings_baseline':reviewed_error_pair((run/(before+'-error-after.log')).read_bytes(),(run/(after+'-error-after.log')).read_bytes(),run) and (run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
if cal.get('evidence_type')=='original_native_autosave_gamestate_date':
 provenance=load(after+'.native-save.json')
 checks['original_native_autosave_provenance_no_manual_UI_claim']=provenance['evidence_type']=='original_native_autosave' and provenance['manual_save_UI_used'] is False and provenance['sha256']==cal['save_sha256']==aa['save_sha256'] and provenance['written_at']==cal['original_native_autosave_source'] and h.sha256(Path(provenance['written_at']))==aa['save_sha256']
new_messages=[v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
resources=set(bc['effective_stockpile'])|set(ac['effective_stockpile'])
proof={'status':'OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'before_date':ba['date'],'after_date':aa['date'],'before_state':b,'after_state':a,'new_country0_messages_raw':new_messages,'new_native_bite_messages_raw':[v for v in new_messages if q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD'],'actual_stock_deltas':{k:str(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))) for k in sorted(resources)},'scope':'Original native construction boundary inventory only, not precise completion, new ship birth, payment, monthly budget reconciliation or full route acceptance.'}
out=run/(after+'-construction-boundary-observation-v4.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':checks,'before_date':ba['date'],'after_date':aa['date'],'after_EEP_variables':ac['variables'],'new_messages':[q.scalars(v) for v in new_messages],'pending':[q.scalars(v) for v in a['pending_country0_raw']],'actual_stock_deltas':proof['actual_stock_deltas'],'species_population_before':b['species_population_by_colony'],'species_population_after':a['species_population_by_colony']}),flush=True)
assert all(checks.values()),'Original observation failure retained; no calendar continuation'
