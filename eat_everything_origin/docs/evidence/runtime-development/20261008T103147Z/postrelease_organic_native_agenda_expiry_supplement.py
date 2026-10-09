import hashlib,json,re,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z');dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
names=['organic-storm-mine5-nextmonth','organic-temple-year1-cleared'];a=[];sha=[]
for n in names:
    a.append(json.loads((run/(n+'.audit.json')).read_text(encoding='utf-8')));sha.append(hashlib.sha256((run/(n+'.sav')).read_bytes()).hexdigest());assert sha[-1]==a[-1]['save_sha256']
b,c=[v['countries']['0'] for v in a];old,new=b['government'],c['government'];cooldown=q.block(old,'council_agenda_cooldowns');original=json.loads((run/'organic-temple-year1-cleared-temple-weather-proof.json').read_text(encoding='utf-8'));wrong='AP_traditions_government_owned_colonies_held';clean,n=re.subn(r'\n[ \t]*council_agenda_cooldowns=\n[ \t]*\{[^{}]*\}','',old)
checks={'original_FAIL_and_other20_checks_preserved':original['status']=='FAIL' and original['checks'][wrong] is False and len(original['checks'])==21 and all(v for k,v in original['checks'].items() if k!=wrong),'original_SHA_pair_matches':sha==[original['before_sha256'],original['after_sha256']],'AP_traditions_owned_colonies_held':all(b[k]==c[k] for k in ['ascension_perks','traditions','owned_colonies']),'only_exact_evolving_society_cooldown_removed':n==1 and clean==new and not q.block(new,'council_agenda_cooldowns') and q.scalars(cooldown)=={'council_agenda':'agenda_evolving_society','start_date':'2309.02.01'},'recorded_cooldown_date_crossed':a[0]['date']<'2309.02.01'<a[1]['date']}
p={'status':'PASS_NATIVE_COOLDOWN_EXPIRY_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':sha[0],'after_sha256':sha[1],'actual_removed_cooldown_raw':cooldown,'original_status':'FAIL','scope':'Read-only exact native cooldown-record deletion; all civic/authority/other government fields and original20 checkpoint checks retained. No agenda launch, government patch or calendar replay.'};out=run/'organic-temple-year1-native-agenda-expiry-supplement-proof.json';assert not out.exists();out.write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');print(json.dumps(p),flush=True);assert all(checks.values())
