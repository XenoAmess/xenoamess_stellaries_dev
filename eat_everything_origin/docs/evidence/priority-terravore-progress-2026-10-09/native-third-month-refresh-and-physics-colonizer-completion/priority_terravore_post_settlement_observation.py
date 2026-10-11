"""Read-only documented same-date recovery inventory; no game input."""
import json,logging,re,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:];days=29;end="2272.08.01"
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
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
original='terravore-third-post-settlement-month'
ce=load(original+'-calendar-execution.json');se=load(original+'-recovered-save-execution.json')
pre=load('terravore-third-settlement-native-third-settlement-proof.json');pe=load('terravore-third-settlement-native-observer-fullpath-execution.json')
action=load(original+'-native-days.action.json');enter=load(original+'-native-days-enter.action.json')
recovered=load(original+'-recovered-console-receipt.ocr.json');labels=[v['text'] for v in recovered['rows']]
validate_native_interval(ba['date'],aa['date'],days)
manifest,tree=h.tree_manifest(h.MOD_ROOT)
checks={
 'fixed_original_pair_and_360day_interval':before=='terravore-third-settlement-native' and after==original+'-recovered' and ba['date']=='2272.07.02' and aa['date']==end,
 'original_SAV_pair_SHA':all(x['save_sha256']==h.sha256(run/(st+'.sav')) for st,x in [(before,ba),(after,aa)]),
 'prior_settlement51_PASS_actual0_source':pre['status']=='PASS_NATIVE_TERRAVORE_THIRD_SETTLEMENT_COMPONENT' and len(pre['checks'])==51 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==ba['save_sha256'] and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_third_settlement_observer.py')=='97bcc09b4f2474b1c75d7863988d03eea67718ef0e9c193b8d46b0ecf462587f',
 'original_calendar_interrupted_polling_actual_nonzero_retained':ce['returncode']==4294967295 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and not (run/(original+'-calendar-receipt.json')).exists() and not (run/(original+'.sav')).exists(),
 'only_one_original29_day_command_and_single_enter':action['action']=='type_text' and action['text']=='fast_forward 29' and action['submitted'] is True and enter['action']=='press_scan_code' and enter['scan_code']==28 and enter['repeat']==1 and len(list(run.glob(original+'-native-days.action.json')))==1,
 'fresh_recovered_console29_receipt_date_and_paused':end in labels and chr(0x6682)+chr(0x505c) in labels and 'Fast Forwarded 29 Days' in labels and h.sha256(Path(recovered['image']))==recovered['image_sha256']=='ee53e10d956927381f1a893a670894661ac8e3326de62aef43f2f8f1c63e83fb',
 'same_date_normal_save_actual0_source':se['returncode']==0 and se['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and load(after+'-observation.json')['date']==end,
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(manifest)==41 and tree=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(original+'-error-before.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
new_messages=[v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
resources=set(bc['effective_stockpile'])|set(ac['effective_stockpile'])
proof={'status':'OBSERVED_NATIVE_TERRAVORE_POST_SETTLEMENT_RECOVERED_MONTH' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'before_date':ba['date'],'after_date':aa['date'],'before_state':b,'after_state':a,'new_country0_messages_raw':new_messages,'new_native_bite_messages_raw':[v for v in new_messages if q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD'],'actual_stock_deltas':{k:str(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))) for k in sorted(resources)},'original_calendar_returncode':ce['returncode'],'scope':'Same-date save and raw original interval observed after polling-only child interruption. Original calendar failure remains nonzero. No day replay. Not business component or full route acceptance.'}
out=run/(after+'-post-settlement-observation.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':checks,'after_date':aa['date'],'after_EEP_variables':ac['variables'],'new_messages':[q.scalars(v) for v in new_messages],'pending':[q.scalars(v) for v in a['pending_country0_raw']],'actual_stock_deltas':proof['actual_stock_deltas'],'species_population_before':b['species_population_by_colony'],'species_population_after':a['species_population_by_colony'],'housing':{k:aa['colonies']['0'].get(k) for k in ['actual_pop_sum','housing_usage','free_housing','total_housing']}}),flush=True)
assert all(checks.values()),'Recovery observation retained; do not replay calendar'
