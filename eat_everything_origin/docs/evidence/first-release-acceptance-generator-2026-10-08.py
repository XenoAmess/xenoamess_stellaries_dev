import hashlib,json,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path('eat_everything_origin');E=ROOT/'docs/evidence';run='20261008T081542Z';base=E/'runtime-development'/run
draft=json.loads(Path('_runtime/heart-of-devouring/first-release-matrix-draft.json').read_text(encoding='utf-8'))
smoke=json.loads((base/'formal-production-smoke-proof.json').read_text(encoding='utf-8'));git=json.loads((E/f'formal-full-run-{run}-git-object-check.json').read_text(encoding='utf-8'));assert smoke['status']==git['status']=='PASS';assert not draft['missing']
production={p.relative_to(ROOT/'mod').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'mod').rglob('*')) if p.is_file()};assert production==smoke['production_files'];assert (ROOT/'VERSION').read_text().strip()=='0.2.0'
def evidence(path):
 p=ROOT/path;return {'path':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def ref(name):return evidence(f'docs/evidence/runtime-development/{run}/{name}')
cases=draft['cases']
for key,c in cases.items():
 if c['status']!='NOT_APPLICABLE':c['status']='PASS_SCOPED'
for n in [1,2,28]:cases[f'EAT-{n:02}']['evidence'].append(ref('formal-prod-initial-clean-identity.json'))
cases['EAT-28']['evidence'].append(ref('formal-prod-intro-ack-proof.json'))
for n in [14,29,33]:
 cases[f'EAT-{n:02}']['evidence'].extend([ref('formal-prod-native-report-readonly-proof.json'),ref('formal-prod-report-repeat-readonly-proof.json'),ref('formal-prod-native-month-stable-reloaded-proof.json')])
review={'status':'REVIEWED_SCOPED_REFERENCES','scope':'scorched_hive_and_shared_mechanisms','reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'source_review':draft['source_review'],
 'partial_records_policy':'Historical PARTIAL findings keep their original status; only actual named completed subcases are reused. Their pending or failed subcases are not passed by this aggregate. Native audit files bind state only; action and UI proof are paired in each case. Controlled shared checks do not complete another civic route.',
 'subcase_reuse':{'20261006T192819Z/findings.json':['complete_100_seed','half_seed_50','founder_100_guard','native_history_reload','controlled_100_worlds','native_Q3_Q5_remainders','two_Q20_controlled_same_day'],
 '20261006T164008Z/findings.json':['court_thresholds','same_date','same_jobs','same_core_population','job_income_delta'],
 '20261006T224056Z/findings.json':['object_refusal_eight_subcases','native_calendar','native_construction'],
 '20261006T232907Z/findings.json':['controlled_triple_q20','natural_native_initial','natural_colony_devoured','native_paid_building_window','native_war','natural70']},
 'original_failures_retained':True,'final_smoke_original_reloaded_cache_delta_retained':True,'full_other_route_acceptance_claimed':False}
(E/'first-release-matrix-source-review-2026-10-08.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
open_civics=['civic_hive_devouring_swarm','civic_machine_terminator','civic_fanatic_purifiers','civic_scorched_earth','civic_hive_scorched_earth']
remaining={
 'civic_hive_devouring_swarm':'Complete independent organic/lithoid natural ascension, Nemesis, special mother worlds and native Terravore random yield/mixed route; true no-mod117/118 calendar boundary still pending.',
 'civic_machine_terminator':'Complete independent natural psionic/Nemesis combinations, Machine-world conversion/jobs and long peace/economy; controlled shared stress is not full route acceptance.',
 'civic_fanatic_purifiers':'Complete independent organic/lithoid natural ascension/Nemesis and special mother worlds, rights and long-term economy.',
 'civic_scorched_earth':'Complete independent natural ascension/Nemesis and late-game special mother/economy; existing natural36/48/60 common formula checks do not complete this route.'}
receipt={'schema':'heart-of-devouring-scoped-runtime-acceptance-v1','status':'PASS_SCOPED','acceptance_mode':'scorched-hive-first-release','scope':'scorched_hive_and_shared_mechanisms',
 'version':'0.2.0','game_exe_sha256':smoke['game_exe_sha256'],'language':'l_simp_chinese','fully_accepted_civics':['civic_hive_scorched_earth'],'open_civics':open_civics,
 'deferred_civics':{k:{'status':'NOT_COMPLETE','remaining':v} for k,v in remaining.items()},'production_files':production,'cases':dict(sorted(cases.items())),
 'production_smoke':{'status':'PASS','production_files':production,'evidence':[ref('formal-production-smoke-proof.json'),evidence(f'docs/evidence/formal-full-run-{run}-git-object-check.json'),evidence('docs/evidence/package-release.json')]},
 'review_evidence':evidence('docs/evidence/first-release-matrix-source-review-2026-10-08.json'),'production_equivalence_evidence':evidence('docs/evidence/formal-rc9-production-equivalence-2026-10-08.json'),
 'static_other_languages':'静态校验通过，运行时不在范围内','known_limitations':['Native no-fee decision/resource transactions may rebuild or initialize three research stock keys; queues preserved, no compensating grants.','Native first-load derived cache differences retained with original FAIL; strict second original-byte reload passed.','Decision and planet_view.gui overrides require compatibility; performance samples do not prove zero overhead.','Other civic routes and true no-mod117/118 completion are post-release acceptance.'],
 'accepted_at_utc':datetime.now(timezone.utc).isoformat(),'workshop_published':False}
(E/'runtime-acceptance.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
titles={}
for line in (ROOT/'docs/acceptance-plan.md').read_text(encoding='utf-8').splitlines():
 if line.startswith('| EAT-'):parts=[x.strip() for x in line.split('|')];titles[parts[1]]=parts[2]
md=['# 吞噬之心 0.2.0：焦土蜂巢首发验收结果','','2026-10-08 北京时间16:49。按用户批准的首发合同，31项适用合同以焦土蜂巢与共用机制范围通过，EAT-05／08不适用。完整实机验收仅焦土蜂巢；首发推荐焦土蜂巢；其它路线开放但未完成完整实机验收。创意工坊尚未上传。',
 '', '共用机制对照包含受控其它合格政体，不代表它们整条路线通过。旧PARTIAL保留制定时状态，只复用已经完成的具体子项；原始FAIL及后续纠正证明同时保留。Q15／20／25的36／48／60月复用不变通用公式的焦土普通帝国原生检查，焦土蜂巢独立自然Q16／18／23与当前Q8提供自身流程证据，不声称重复跑过独立自然Q20长局。',
 '', '正式生产冒烟只加载41个最终生产文件，未加载testing或探针；继承原字节合法开局，不称重新生成随机世界。Nemesis与虚境之影实际可用，开局女王CG及确认、母星按钮首次／重复报告、真实30日与原字节重载共96项组件检查通过，正常退出。首次重载派生缓存全对象FAIL保留；重算后原字节二次重载27项严格检查通过。整轮389份原件22956019字节、Git391文件23093297字节完整核验；未过滤error.log2670字节，仅21条既有缺工坊文件提示与预期决议覆盖提示，无作用域或无效脚本错误，不声称全局零日志。',
 '', '最终生产包经open_kaishek校验18脚本／12DDS／10语言73键通过，工具只证明解析和包资源；简中实机证据独立提供。其它九语言静态校验通过，运行时不在范围内。',
 '', '无费吞星开始等原生决议可能重建或初始化三系科研库存，完整库存FAIL保留；队列保持且不补发掩盖。覆盖决议与planet_view.gui的兼容限制、单样本性能、其它路线未完成均已写入正式changelog、工坊正文和版本Change Note。',
 '', '| 用例 | 原合同 | 首发状态 | 实际证据范围 |','| --- | --- | --- | --- |']
for identity,c in sorted(cases.items()):md.append(f"| {identity} | {titles.get(identity,'')} | {c['status']} | {c.get('actual_scope',c.get('reason'))} |")
md.extend(['','每项原件路径与SHA见[正式运行时凭证](evidence/runtime-acceptance.json)，历史子项状态审阅见[来源审阅](evidence/first-release-matrix-source-review-2026-10-08.json)。生产冒烟见[整轮原件](evidence/runtime-development/20261008T081542Z/formal-production-smoke-proof.json)和[Git原字节核验](evidence/formal-full-run-20261008T081542Z-git-object-check.json)。',
 '', '下一步：离线发布preflight通过并提交推送后，才将Steam在线；创建新的工坊物品，上传正文／七张冻结图片／Change Note，独立下载全41文件及远端元数据与图片核验后提交发布回执和v0.2.0标签。随后恢复离线，继续四个未完成入口、石质／机械世界及真正无Mod117／118等测试与修复。'])
(ROOT/'docs/first-release-acceptance-result-2026-10-08.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
shutil.copyfile('_runtime/heart-of-devouring/prepare_first_release_matrix.py',E/'first-release-matrix-source-generator-2026-10-08.py');shutil.copyfile(Path(__file__),E/'first-release-acceptance-generator-2026-10-08.py')
p=ROOT/'CHANGELOG.md';text=p.read_text(encoding='utf-8').replace('最终生产包工具检查与独立简中冒烟须在上传前通过。','最终生产包open_kaishek校验18脚本／12DDS／10语言73键通过；独立仅生产包简中冒烟96项组件检查与稳定原字节重载通过，完整未过滤日志和原始FAIL已保留。',1);p.write_text(text,encoding='utf-8')
for name in ['first-release-remaining-runtime-round-2026-10-08.md','runtime-acceptance-progress-2026-10-07.md','first-formal-release-freeze-2026-10-08.md']:
 p=ROOT/'docs'/name;lines=p.read_text(encoding='utf-8').splitlines();lines[1:1]=['','当前状态（2026-10-08 16:49）：焦土蜂巢／共用范围31项及正式生产冒烟已完成，详见[首发验收结果](first-release-acceptance-result-2026-10-08.md)。下方保留各时点历史；其它路线未完整验收，创意工坊上传与核验仍待执行。'];p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'status':receipt['status'],'required_cases':31,'not_applicable':2,'production_files':len(production),'references':sum(len(c.get('evidence',[])) for c in cases.values())}))
