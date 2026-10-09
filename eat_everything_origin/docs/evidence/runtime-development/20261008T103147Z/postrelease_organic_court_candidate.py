import copy, json, logging, shutil, sys, time, zipfile
from pathlib import Path
before,stage=sys.argv[1:]; sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r, audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();source=Path(__file__);dest=run/source.name
if not dest.exists():shutil.copyfile(source,dest)
assert dest.read_bytes()==source.read_bytes()
history_source=source.parent/'native_selected_history.py';history_dest=run/history_source.name
if not history_dest.exists():shutil.copyfile(history_source,history_dest)
assert history_dest.read_bytes()==history_source.read_bytes()
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
def raw(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:return z.read('gamestate').decode('utf-8-sig')
def pending(t):return [q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
def history(t):return selected_history(t)
bt=raw(before);assert not pending(bt),'Normal pending events must be handled before image collection'
f=r.gpu_capture(stage+'-actual-outliner');labels=[x['text'] for x in f['rows']];assert b['date'] in labels and '\u6682\u505c' in labels
rows=[x for x in f['rows'] if x['text']=='EEP-Core' and x['box'][0][0]>810];assert rows
box=max(rows,key=lambda x:x['box'][0][1])['box'];h.click_point(round((box[0][0]+box[2][0])/2),round((box[0][1]+box[2][1])/2),stage+'-native-mother-open')
f=r.gpu_capture(stage+'-actual-mother');rows=[x for x in f['rows'] if x['text']=='\u89d0\u89c1\u5973\u738b\u00b7\u767d\u7eee'];assert len(rows)==1
box=rows[0]['box'];h.click_point(round((box[0][0]+box[2][0])/2),round((box[0][1]+box[2][1])/2),stage+'-native-court-open')
h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(.4);f=r.gpu_capture(stage+'-clean-native-court');labels=[x['text'] for x in f['rows']]
assert any('\u738b\u5ead\u8d26\u7c3f' in t for t in labels),'Native court image must identify the actual report'
rows=[x for x in f['rows'] if h.normalized(x['text'])==h.normalized('\u9000\u4e0b\u3002')];assert len(rows)==1
box=rows[0]['box'];h.click_point(round((box[0][0]+box[2][0])/2),round((box[0][1]+box[2][1])/2),stage+'-native-court-ack');h.press_scan_code(0x01,stage+'-explicit-paused-close',1)
a=r.native_save(stage,b['date'],(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea);ac,bc=a['countries']['0'],b['countries']['0'];at=raw(stage)
def nondisplay_planets(s):
    p=copy.deepcopy(s['planets'])
    for obj in p.values():
        for k in ('eep_actual_pop','eep_free_districts'):obj['variables'].pop(k,None)
    return p
checks={'same_actual_date':a['date']==b['date'],'all_actual_stocks_held':ac['effective_stockpile']==bc['effective_stockpile'],'native_research_banks_held':ac['research_stockpile']==bc['research_stockpile'],'full_tech_status_held':ac['tech_status']==bc['tech_status'],'EEP_variables_held':ac['variables']==bc['variables'],'EEP_flags_held':ac['flags']==bc['flags'],'AP_traditions_government_owned_colonies_held':all(ac[k]==bc[k] for k in ('ascension_perks','traditions','government','owned_colonies')),'all_nondisplay_planet_data_held':nondisplay_planets(a)==nondisplay_planets(b),'mother_report_actual_pop_exact':a['planets']['7']['variables']['eep_actual_pop']==a['colonies']['0']['actual_pop_sum'],'mother_free_capacity_exact':a['planets']['7']['variables']['eep_free_districts']==34-sum(a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts']),'ledger_actual40_12_600_3':all(ac['variables'][k]==v for k,v in {'eep_c':40,'eep_g':40,'eep_d':12,'eep_made':600,'eep_worlds':3}.items()),'no_pending_native_events':not pending(at),'no_new_errors':ea==eb}
for k in ('pop_groups','pop_jobs','districts','colonies','situations','species','deposits'):checks[k+'_held']=a[k]==b[k]
bh,ah=history(bt),history(at);added=ah[len(bh):] if ah[:len(bh)]==bh else [];checks['one_actual_human_report_ack']=len(added)==1 and added[0].get('human')==1 and added[0].get('option')==0
p={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_date':a['date'],'candidate_image':f['image'],'candidate_image_sha256':f['image_sha256'],'actual_mother_display':a['planets']['7']['variables'],'actual_EEP_variables':ac['variables'],'actual_history_added':added,'scope':'Normal native Queen court screenshot and ACK; display-only population and capacity refresh. Partial organic route, candidate not uploaded and published recommendation unchanged.'}
h.write_json(run/(stage+'-proof.json'),p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original court capture/ACK proof retained; do not repeat'
