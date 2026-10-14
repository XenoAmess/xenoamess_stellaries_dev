"""Read-only native save maps; no GUI, calendar, assertions or output writes."""
import json,re,zipfile
import audit_save as q

def read_state(run,stage):
 audit=json.loads((run/(stage+'.audit.json')).read_text('utf-8-sig'))
 with zipfile.ZipFile(run/(stage+'.sav')) as z:fields=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 roots={k:v for k,v,x in fields if x};country=q.block(roots['country'],'0')
 fleet_ids=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(country,'fleets_manager'),'owned_fleets'))))
 fleets={k:v for k,v,x in q.fields(roots['fleet']) if x and int(k) in fleet_ids}
 ship_ids={i for v in fleets.values() for i in q.ids(q.block(v,'ships'))}
 ships={k:v for k,v,x in q.fields(roots['ships']) if x and int(k) in ship_ids}
 queues={k:v for k,v,x in q.fields(q.block(q.block(roots['construction'],'queue_mgr'),'queues')) if x}
 items={k:v for k,v,x in q.fields(q.block(q.block(roots['construction'],'item_mgr'),'items')) if x}
 designs={k:v for k,v,x in q.fields(roots['ship_design']) if x}
 templates={k:v for k,v,x in q.fields(roots['fleet_template']) if x}
 messages=[v for k,v,x in fields if x and k=='message' and q.scalars(v).get('receiver')==0]
 pending=[v for k,v,x in fields if x and k=='player_event' and q.scalars(v).get('country')==0]
 return {'audit':audit,'roots':roots,'country':country,'fleets':fleets,'ships':ships,
         'queues':queues,'items':items,'designs':designs,'templates':templates,'messages':messages,'pending':pending}

def omit(raw,keys):
 return [(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
