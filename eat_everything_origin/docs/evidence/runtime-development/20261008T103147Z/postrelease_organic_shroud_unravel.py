import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
b=json.loads((run/'organic-civilian-policy-nextmonth.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();bc=b['countries']['0']
assert 'tech_astral_harvesting' in bc['completed_technologies'] and bc['effective_stockpile']['astral_threads']>=10
f=r.gpu_capture('organic-shroud-unravel-before-native-select');labels=[v['text'] for v in f['rows']];assert '\u70b9\u51fb\u4e3a\u8be5\u5c40\u52bf\u9009\u62e9\u89e3\u51b3\u65b9\u6848\u3002' in labels
h.click_point(699,234,'organic-shroud-unravel-select-native');h.pyautogui.moveTo(700,675)
f=r.gpu_capture('organic-shroud-unravel-selected-native-ui');print(json.dumps({'image':str(f['image']),'rows':[v['text'] for v in f['rows']]}),flush=True)
a=r.native_save('organic-shroud-unravel-selected',b['date'],(0,));ac=a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/'organic-shroud-unravel-selected-error-after.log').write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb,'native_nothing_to_unravel':b['situations']['33554438']['approach']=='approach_situation_breach_shroud_nothing' and a['situations']['33554438']['approach']=='approach_situation_breach_shroud_unravel_thread'}
bs,ass=b['situations']['33554438'],a['situations']['33554438'];checks['only_audited_situation_approach_changes']={k:v for k,v in bs.items() if k!='approach'}=={k:v for k,v in ass.items() if k!='approach'}
for k in ('stockpile','effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','native'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','species','event_targets'):checks[k+'_held']=a[k]==b[k]
raw=[]
for name in ('organic-civilian-policy-nextmonth','organic-shroud-unravel-selected'):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 raw.append(q.block(q.block(t,'situations'),'33554438'))
bf,af=[{k:(v,o) for k,v,o in q.fields(t)} for t in raw];diff={k:{'before':bf.get(k),'after':af.get(k)} for k in set(bf)|set(af) if bf.get(k)!=af.get(k)}
checks['raw_situation_only_approach_and_flags_changed']=set(diff)<= {'approach','flags'}
old_flags=q.scalars(q.block(raw[0],'flags'));new_flags=q.scalars(q.block(raw[1],'flags'));checks['only_native_chaotic_flag_added']=set(new_flags)==set(old_flags)|{'chaotic_approach'} and all(new_flags[k]==v for k,v in old_flags.items())
p={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'raw_situation_differences':diff,'raw_situation_before':raw[0],'raw_situation_after':raw[1],'scope':'Actual native unravel-thread selection; no immediate resource or EEP reward. Upkeep and monthly progress pending actual next month.'}
h.write_json(run/'organic-shroud-unravel-selected-proof.json',p);print(json.dumps({'checks':checks,'sha':a['save_sha256'],'raw_changed':list(diff)}),flush=True);assert all(checks.values()),'Original native shroud choice failure retained'
