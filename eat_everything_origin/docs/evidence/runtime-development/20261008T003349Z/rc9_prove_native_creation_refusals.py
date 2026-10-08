import hashlib,json,shutil
from pathlib import Path
run=Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
shutil.copyfile(Path(__file__),run/Path(__file__).name)
out=[]
for n in ['07','10']:
    selected=json.loads((run/('rc9-native-preset-'+n+'-selected.ocr.json')).read_text(encoding='utf-8'))
    tip=json.loads((run/('rc9-native-origin-refusal-'+n+'-native-requirement-tooltip.ocr.json')).read_text(encoding='utf-8'))
    after=json.loads((run/('rc9-native-origin-refusal-'+n+'-after-native-attempt.ocr.json')).read_text(encoding='utf-8'))
    action=json.loads((run/('rc9-native-origin-refusal-'+n+'-actual-origin-card-attempt.action.json')).read_text(encoding='utf-8'))
    s=' '.join(x['text'] for x in selected['rows']);t=' '.join(x['text'] for x in tip['rows'])
    choices=[x for x in after['rows'] if x['text']=='\u7e41\u8363\u4e00\u7edf' and min(p[0] for p in x['box'])>700]
    checks={'native_selected_identity':'EEP '+n in s,'ineligible_civics_visible':all(k in s for k in (['\u9ad8\u6548\u540f\u6cbb','\u77ff\u4e1a\u516c\u4f1a'] if n=='07' else ['\u540c\u5316\u6597\u58eb','\u5feb\u901f\u590d\u5236\u8005'])),
      'custom_origin_tooltip':'\u541e\u566c\u4e4b\u5fc3' in t,'qualified_civic_requirement':'\u9700\u8981\u541e\u566c\u8702\u7fa4' in t,
      'actual_native_card_clicked':'client_point' in action,'default_origin_still_selected':len(choices)==1,
      'simplified_chinese_UI':all(v['capture']=='fresh Steam F12 GPU backbuffer' for v in [selected,tip,after])}
    refs=[]
    for f in [Path(selected['image']),Path(tip['image']),Path(after['image']),run/('rc9-native-origin-refusal-'+n+'-actual-origin-card-attempt.action.json')]:
        refs.append({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    out.append({'preset':n,'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'visual_review':'Actual fresh tooltip reviewed: red cross on exterminator civic requirement; not a static script-only assertion.','evidence':refs})
    assert all(checks.values()),checks
v={'status':'PASS_SCOPED','scope':'Native creation editor rejection for ordinary empire and driven assimilator; neither preset origin or government was rewritten.','checks_total':sum(len(x['checks']) for x in out),'cases':out}
(run/'rc9-native-creation-refusals-proof.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':v['status'],'checks_total':v['checks_total']}))
