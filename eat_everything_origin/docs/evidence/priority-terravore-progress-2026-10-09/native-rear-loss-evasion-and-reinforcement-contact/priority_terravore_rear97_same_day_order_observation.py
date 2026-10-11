"""Read-only documented native construction inventory; not completion acceptance."""
import hashlib,json,logging,re,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
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
        'enemy825_raw':q.block(roots['fleet'],'825'),'rear153_raw':q.block(q.block(roots['starbase_mgr'],'starbases'),'153'),'top_fields_content_sha256':[(k,o,hashlib.sha256(v.encode('utf-8')).hexdigest()) for k,v,o in fs],'top_fields_ordered':[(k,o) for k,v,o in fs]}
b,a=read(before),read(after);ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0']
pre=load(before+'-birth-v2-proof.json');pe=load(before+'-observer-v2-execution.json');se=load(after+'-native-save-execution.json');so=load(after+'-observation.json')
manifest,tree=h.tree_manifest(h.MOD_ROOT)
checks={
 'fixed_same_native_date':before=='terravore-rear-colonizer-born' and after=='terravore-rear97-idle-reinforcement-ordered' and ba['date']==aa['date']=='2272.09.13',
 'original_SAV_SHA_pair':all(v['save_sha256']==h.sha256(run/(st+'.sav')) for st,v in [(before,ba),(after,aa)]),
 'native_save_actual0_original_source':se['returncode']==0 and se['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and so['status']=='OBSERVED_NATIVE_SAVE' and so['new_error_bytes']==0 and so['save_sha256']==aa['save_sha256'],
 'prior_birth46_PASS_actual0_original_SHA_and_source':pre['status']=='PASS_NATIVE_TERRAVORE_REAR_COLONIZER_BIRTH_IN_COMBAT_COMPONENT' and len(pre['checks'])==46 and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_rear_colonizer_birth_observer_v2.py')=='ed9b38a96bc838d3340d82d8c272dd883dba7a9595f1f27b67818384c21516fa' and pre['after_sha256']==ba['save_sha256'],
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(manifest)==41 and tree=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
p={'status':'OBSERVED_NATIVE_TERRAVORE_REAR97_SAME_DAY_ORDER' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'before_state':b,'after_state':a,'scope':'Read-only complete same-day normal-order observation; no attack-order or full-route acceptance.'}
out=run/(after+'-same-day-order-observation.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':checks,'changed_owned_fleets':[i for i in b['owned_fleets_raw'] if b['owned_fleets_raw'][i]!=a['owned_fleets_raw'].get(i)],'changed_owned_ships':[i for i in b['owned_ships_raw'] if b['owned_ships_raw'][i]!=a['owned_ships_raw'].get(i)],'date':aa['date']}),flush=True)
assert all(checks.values())
