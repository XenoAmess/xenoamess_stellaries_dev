"""Bind the original research-year FAIL to its one native non-EEP pending event."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs
b,bf=read(before);a,af=read(after);pre=json.loads((run/(after+'-theory-wait-proof.json')).read_text('utf-8'))
pending=[v for k,v,o in af if k=='player_event' and q.scalars(v).get('country')==0]
bp=[v for k,v,o in bf if k=='player_event' and q.scalars(v).get('country')==0]
event_path=Path('C:/SteamLibrary/steamapps/common/Stellaris/events/grand_archive_events.txt');text=event_path.read_text('utf-8-sig')
events=[v for k,v,o in q.fields(text) if k=='country_event' and o and q.scalars(v).get('id')=='grand_archive.2195']
checks={
 'original27_exact_one_pending_FAIL_and26_valid':pre['status']=='FAIL' and len(pre['checks'])==27 and [k for k,v in pre['checks'].items() if v is not True]==['no_pending_or_repeat_Queen_notice'],
 'original_SHA_pair_bound':pre['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and pre['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'only_native116_pending_not_Queen':not bp and len(pending)==1 and q.scalars(pending[0])=={'id':116,'event':'grand_archive.2195','date':'2238.06.26','country':0},
 'native_event_scope_country0_from_physical7':q.scalars(q.block(pending[0],'scope')).get('type')=='country' and q.scalars(q.block(pending[0],'scope')).get('id')==0 and q.scalars(q.block(q.block(pending[0],'scope'),'from')).get('type')=='planet' and q.scalars(q.block(q.block(pending[0],'scope'),'from')).get('id')==7,
 'actual_native_option_has_names_only':len(events)==1 and [(k,o) for k,v,o in q.fields(q.block(events[0],'option'))]==[('name',True),('name',True)] and 'set_country_flag = bombarded_by_voidworms_event' in q.block(events[0],'immediate'),
 'EEP_full_ledger_flags_held_and_not_ascended':b['countries']['0']['variables']==a['countries']['0']['variables'] and b['countries']['0']['flags']==a['countries']['0']['flags'] and a['countries']['0']['variables']['eep_psi']==0,
 'original_full_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_SCOPED_TERRAVORE_THEORY_YEAR_NATIVE_EVENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'original_valid_checks':{k:v for k,v in pre['checks'].items() if v is True},'native_event_source':{'path':str(event_path),'sha256':h.sha256(event_path)},'native_event_raw':pending,'scope':'Original 27-check FAIL retained; 26 other constraints hold. One actual native Voidworm invasion notification allowed for immediate normal acknowledgement only. Warfare/fleet losses are real; no peaceful economy, no-next-event, Theory completion or full-route claim.'}
out=run/(after+'-native-event-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native-event supplement FAIL retained; no calendar'
