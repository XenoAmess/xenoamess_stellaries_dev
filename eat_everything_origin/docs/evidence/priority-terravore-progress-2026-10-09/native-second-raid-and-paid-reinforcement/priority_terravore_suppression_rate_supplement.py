"""Source-bound native suppression first-month exact observed rate supplement."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D,ROUND_FLOOR
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-attunement3-native-suppression';after='terravore-native-stage3-suppression-month'
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'))
old=json.loads((run/(after+'-meditate-stage3-proof.json')).read_text('utf-8'));ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
pre=json.loads((run/(before+'-2505-suppression-proof.json')).read_text('utf-8'));pex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
def mods(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 items=q.block(q.block(q.block(q.block(t,'country'),'0'),'timed_modifier'),'items')
 ts=list(q.tokens(items));out=[];depth=0;start=None
 for tok,lo,hi in ts:
  if tok=='{':
   if depth==0:start=hi
   depth+=1
  elif tok=='}':
   depth-=1
   if depth==0:out.append(q.scalars(items[start:lo]))
  elif depth==0:raise ValueError('Expected anonymous modifier')
 assert depth==0
 return out
source=h.GAME_EXE.parent/'common/situations/13_shroud_situations.txt';values=h.GAME_EXE.parent/'common/script_values/07_script_values_shroud.txt'
src=source.read_text('utf-8-sig');monthly=q.block(q.block(src,'situation_breach_shroud'),'monthly_progress');speed=[v for k,v,o in q.fields(monthly) if k=='modifier' and q.scalars(v).get('factor')=='value:breach_the_shroud_situation_progress_speed_factor']
checks={
 'bound_original42_only_rate_FAIL_exit1_other41true':old['status']=='FAIL' and len(old['checks'])==42 and {k for k,v in old['checks'].items() if not v}=={'actual_meditate_exact_observed_rate_per_month'} and ex['returncode']==1,
 'original_SHA_pair':old['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and old['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'bound_actual2505_36_PASS_exit0_sources_unchanged':pre['status']=='PASS_NATIVE_TERRAVORE_2505_SUPPRESSION_COMPONENT' and len(pre['checks'])==36 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and pex['returncode']==0 and all(h.sha256(Path(v['path']))==v['sha256'] for v in pre['native_sources']),
 'unique30day_calendar_exit0':old['days']==30 and b['date']=='2256.09.02' and a['date']=='2256.10.02' and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'actual_exact_saved_rate_and_delta':D(str(b['situations']['16777221']['progress']))==D('877.4778') and D(str(a['situations']['16777221']['progress']))==D('882.6871') and D(str(a['situations']['16777221']['last_month_progress']))==D('5.2093') and D('882.6871')-D('877.4778')==D('5.2093'),
 'native_two_exact_modifier_countdowns':mods(before)==[{'modifier':'psionic_painkillers_gestalt','days':600},{'modifier':'shroud_suppression','days':3600}] and mods(after)==[{'modifier':'psionic_painkillers_gestalt','days':570},{'modifier':'shroud_suppression','days':3570}],
 'native_source_speed_factor_reads_owner_modifier':len(speed)==1 and q.scalars(q.block(values.read_text('utf-8-sig'),'breach_the_shroud_situation_progress_speed_factor'))=={'base':1,'add':'owner.modifier:breach_the_shroud_situation_progress_speed_mult'} and h.sha256(source)==old['native_speed_source']['sha256'],
 'saved_rate_times_point9_five_decimal_floor_matches_observation':(D('5.78812')*D('0.9')).quantize(D('0.00001'),rounding=ROUND_FLOOR)==D('5.2093'),
}
p={'status':'PASS_NATIVE_SUPPRESSION_FIRST_MONTH_RATE_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':True,'actual_rate':5.2093,'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,values]],'scope':'Exact first suppression month rate with prior41 strict checks retained. Observed decimal comparison does not prove internal arithmetic sequence. Separate full month ledger required.'}
out=run/(after+'-suppression-rate-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original rate supplement FAIL retained'
