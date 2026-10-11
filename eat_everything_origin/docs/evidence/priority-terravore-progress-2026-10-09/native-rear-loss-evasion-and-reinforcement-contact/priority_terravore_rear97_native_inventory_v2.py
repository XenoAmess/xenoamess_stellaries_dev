"""Documented read-only enemy825/rear153 native lifecycle inventory, not acceptance."""
import json,sys,zipfile,hashlib,re
from pathlib import Path
before,after=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
import audit_save as q
run=Path(__file__).resolve().parent
known=[67110618,1808,16778809,16778802,16778851,16778905,117441693,67109342,16779083,33556209,33556283,50333407]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(st):
    with zipfile.ZipFile(run/(st+'.sav')) as z:roots={k:v for k,v,o in q.fields(z.read('gamestate').decode('utf-8-sig')) if o}
    audit=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
    f=q.block(roots['fleet'],'825');ids=q.ids(q.block(f,'ships'))
    owner=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(roots['country'],'1'),'fleets_manager'),'owned_fleets'))))
    return {'save_sha256':sha(run/(st+'.sav')),'audit_save_sha256':audit['save_sha256'],'date':audit['date'],
        'enemy825_raw':f,'enemy825_entry':[(v,o) for k,v,o in q.fields(roots['fleet']) if k=='825'],'enemy825_ship_ids':ids,
        'enemy825_ships_raw':{str(i):q.block(roots['ships'],str(i)) for i in sorted(set(ids)|set(known))},
        'enemy825_ships_entries':{str(i):[(v,o) for k,v,o in q.fields(roots['ships']) if k==str(i)] for i in known},
        'enemy825_country1_owned':825 in owner,'rear153_raw':q.block(q.block(roots['starbase_mgr'],'starbases'),'153'),
        'war1_battles_raw':q.block(q.block(roots['war'],'1'),'battles'),'construction_raw':roots['construction'],'native_zones_raw':roots['zones']}
def ordinal(date):
    y,m,d=map(int,date.split('.'));return y*360+(m-1)*30+d-1
b,a=read(before),read(after)
checks={'before_original_SAV_audit_SHA':b['save_sha256']==b['audit_save_sha256'],'after_original_SAV_audit_SHA':a['save_sha256']==a['audit_save_sha256'],
    'bounded_original_dates':'2272.09.13'<=b['date']<a['date']<='2272.09.27' and ordinal(a['date'])-ordinal(b['date'])==1,
    'enemy_ships_complete_native_entry_inventory':all(set(v['enemy825_ships_raw'])>=set(map(str,v['enemy825_ship_ids'])) and len(v['enemy825_ships_entries'])==12 for v in [b,a])}
x={'status':'OBSERVED_NATIVE_TERRAVORE_REAR97_INVENTORY' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],before:b,after:a,'scope':'Read-only original SAV inventory, no GUI, calendar or completion acceptance.'}
out=run/(after+'-rear97-native-inventory.json');assert not out.exists();out.write_text(json.dumps(x,indent=2)+'\n','utf-8')
print(json.dumps({'status':x['status'],'checks':checks,'file':out.name,'sha256':sha(out),'enemy_ship_counts':[len(v['enemy825_ship_ids']) for v in [b,a]],'war_history_held':b['war1_battles_raw']==a['war1_battles_raw']}),flush=True)
assert all(checks.values())
