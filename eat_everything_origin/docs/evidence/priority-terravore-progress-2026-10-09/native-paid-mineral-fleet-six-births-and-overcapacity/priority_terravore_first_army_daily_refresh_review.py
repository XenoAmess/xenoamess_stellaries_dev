"""Exactly one daily native modifier/research refresh after genuine paid birth."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'));sha=h.sha256
before='terravore-first-assault-army-native-birth-date';pre=load(before+'-first-paid-army-birth-v3-proof.json');px=load(before+'-first-paid-army-birth-guard-v3-execution.json');a=load(before+'.audit.json');obs=load(before+'-construction-boundary-observation-v2.json')
checks={
 'birth21_PASS_actual0_fixed_source_SAV':len(pre['checks'])==21 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==sha(Path(px['command'][1]))=='f2c3bc27b8383e127d9add02b35f444618c6cdee546c16d18d96779694752892' and pre['after_sha256']==a['save_sha256']==sha(run/(before+'.sav')),
 'one_date6_01_to6_02_and_exact_review_boundary':a['date']=='2279.06.01' and pre['boundaries']==['native_first_army_daily_modifier_and_research_refresh_review_required'] and pre['maximum_days_to_native_bite_boundary']==0 and pre['native_devour_calendar_ready'] is False,
 'genuine_linked_army_transport_fleet':(pre['army'],pre['transport'],pre['fleet'])==(50331728,100664961,16778104),
 'no_unknown_pending_or_new_message':not obs['after_state']['pending_country0_raw'] and not obs['new_country0_messages_raw'],
 'EEP_C62_M1635_current_mother11972':a['countries']['0']['variables']['eep_c']==62 and a['countries']['0']['effective_stockpile']['menace']==1635 and a['colonies']['0']['actual_pop_sum']==11972,
 'original_error_current_held':(user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 'production_CN020':m['language']=='l_simp_chinese' and m['version']=='0.2.0',
}
passed=all(v is True for v in checks.values());out=run/'terravore-first-army-daily-refresh-review-proof.json';assert not out.exists();h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['save_sha256'],'after_sha256':a['save_sha256'],'start_date':'2279.06.01','end_date':'2279.06.02','days':1,'maximum_days':1,'allowed_boundaries':pre['boundaries'],'execution_stage':'terravore-first-army-daily-refresh-review','scope':'One native research tick, queued work1 and native health modifier refresh; independent after audit required. No rewards.'});print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
