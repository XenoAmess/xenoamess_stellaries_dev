import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='organic-third-latent-devour-month22';stage='organic-shroud-thread87-preserved';b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));assert b['date']=='2302.11.02' and b['countries']['0']['effective_stockpile']['astral_threads']==87;eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-real-native-tooltip');assert '\u9759\u89c2\u5176\u53d8' in [v['text'] for v in f['rows']];h.click_point(486,234,stage+'-real-native-nothing-click');h.pyautogui.moveTo(700,675);f=r.gpu_capture(stage+'-real-native-selected');print(json.dumps({'image':f['image'],'rows':[v['text'] for v in f['rows']]}),flush=True)
a=r.native_save(stage,b['date'],(0,));bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb,'native_unravel_to_nothing':b['situations']['33554438']['approach']=='approach_situation_breach_shroud_unravel_thread' and a['situations']['33554438']['approach']=='approach_situation_breach_shroud_nothing','audited_shroud_only_approach_changes':{k:v for k,v in b['situations']['33554438'].items() if k!='approach'}=={k:v for k,v in a['situations']['33554438'].items() if k!='approach'},'other_audited_situations_held':{k:v for k,v in b['situations'].items() if k!='33554438'}=={k:v for k,v in a['situations'].items() if k!='33554438'}}
for k in ('effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','native'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','species','event_targets'):checks[k+'_held']=a[k]==b[k]
raw=[]
for name in (before,stage):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 body=q.block(q.block(q.block(t,'situations'),'situations'),'33554438');assert body;raw.append(body)
bf,af=[{k:(v,o) for k,v,o in q.fields(t)} for t in raw];diff={k:{'before':bf.get(k),'after':af.get(k)} for k in set(bf)|set(af) if bf.get(k)!=af.get(k)};checks['nonempty_raw_shroud_only_approach_changes']=set(diff)=={'approach'}
p={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'raw_shroud_before':raw[0],'raw_shroud_after':raw[1],'raw_shroud_diff':diff,'raw_economy_mirror_differences':{k:[bc['stockpile'].get(k),ac['stockpile'].get(k)] for k in set(bc['stockpile'])|set(ac['stockpile']) if bc['stockpile'].get(k)!=ac['stockpile'].get(k)},'scope':'Real UI switch at actual 87-thread reserve, preserving current 385.75 progress and native source task. Monthly upkeep removal/progress still requires next-month proof.'};h.write_json(run/(stage+'-proof.json'),p);print(json.dumps({'checks':checks,'sha':a['save_sha256'],'raw_shroud_diff':diff}),flush=True);assert all(checks.values()),'Original native preservation failure retained'
