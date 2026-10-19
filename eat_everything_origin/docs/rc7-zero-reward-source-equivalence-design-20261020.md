# RC7零奖励分支证据复用设计（仅设计，PENDING）

> **2026-10-20主线程最终决定：不采用本文提出的跨树v2桥，也不增加桥gate。现有exacttree原则保留；RC7重新完成三类新开局／全年及两类迁移。RC6只能复用旧基线、原始fixture、事前政策和参考来源，不能当RC7结果。下文方案仅保留为已评估但未采用的设计沿革，不是执行授权。**

## 目标、范围与已核边界

2026-10-20主线程确认真实生产缺陷：RC6在20500物质／410应得奖励的受控路径中仅兑现300、pending110；预定RC7只给组件奖励while增加literal `count=200`，并更新候选版本元数据。主线程要求只读设计未受影响RC6证据的诚实复用方案，成长、相关原生PK联动及重载仍在RC7重新验收。本轮不改生产、gate、checker、版本、metadata、旧证据、媒体、Git或UI，不提前声称RC7已冻结／通过。

已核现状：RC6冻结59文件树为`cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`；当前奖励函数已有`eep_component_work_budget=200`及按应得／实得判断的while，但没有显式count。当前根VERSION仍为0.4.0-rc.6。RC7完整树／SHA尚未交付，本文不填造。未来必须对两个完整冻结目录独立重算、验证实际差异，不能以主线程的预定修改代替真实字节审计。

## 当前发布门禁不能直接跨树

现`eep-1019-acceptance-v1`要求顶层production tree、static gate、所有runs manifest的repository/copied tree及完整文件索引、所有case tree／run_id均属于同一个最终候选。经济`candidate_months`必须是该候选case的原生SAV；组件归因另锁RC6树和四模型tuple；迁移v2 release合同／checker也显式锁RC6、原工具SHA和原case／manifest。

因此，**不能**把RC6 manifest加入RC7的`runs`，不能改RC6 report／SAV receipt的tree、version或run，不可把RC6月度SAV直接称为RC7原生预算，不可在现v1门禁里多加一段说明就默认为通过。metadata-only正式化只允许descriptor版本替换，不覆盖while改动。当前门禁保留原样时，所有候选runtime结论只能在RC7实机重做。

## 建议：只给六个C0开局／经济组建立窄桥

可以合理审阅的复用仅限三政府startup与economy共六组。依据是单一while循环上限变更在`rewards=entitled=0`时没有循环体执行；此时六个随机频道、账本、就业、建筑／区划、人口、普通维护等源与调用外围应逐字节相同。它证明限定状态下代码等价，不声称RC7已经原生跑过十二个月，也不推广到所有随机种子／战役。

建议用“完整RC6原生轨迹＋精确源码等价＋RC7同输入零奖励分支补测”替代重复三套全年采样。若主线程不接受显式跨树schema，或者下述任一条件缺失，就重跑相应三类全年；不能只把现v1的tree判断放宽。

### 桥必须同时满足的条件

1. **完整包差异封闭。** 两个冻结包均实际59文件、无新增／删除，完整文件哈希表和目录树独立核对。唯一生产语义差异为目标函数中唯一while位置增加精确literal `count=200`；descriptor仅候选版本文本不同，外部VERSION单独记录。不允许同时改注释、换行、条件、RNG权重、奖励自增、清理、公式或其它文件。删除这一处实际新语句及替回descriptor版本后，剩余字节须等于RC6原件。任何额外差异都使窄桥失效，必须重新评估或重跑。
2. **源依赖明确。** 原样保留并绑定startup／economy布局、静态modifier、真实六core／ship design／section、on_actions／events、加载修复helper，以及奖励函数外围；额外绑定原版EXE、经济类别定义与实际DLC／语言／单Mod配置。RNG六权重与数值公式未改只是源码事实；整个组件同步函数已因count变化而不同，v5不能把该函数整块宣称逐字节等同。
3. **旧轨迹实际满足零分支。** 每组RC6原生Jan1、十二个月及年末UI样本逐个验证C0／L0、entitled0／rewards0／pending0、六tier0，country／bound fleet镜像一致、没有遗留work_budget、没有source settlement／奖励注入。缺字段不得仅凭截图或“未见成长”默认0。所有三×十二日期／净电、初始200、母星／岗位／人口和真实正常成本继续按原报告审查。
4. **RC6原结果先完整审查。** 三个startup七项与三个economy七项均必须真实完成；现在四操作约束仍为null的提案不能被桥自动升级。源run停止后的完整日志与受控worker输入链由主线程审查，保留未解决错误及观察范围。源六组应另建限定验收报告，不要求RC6其它已失败／未完成的成长组先PASS，也不能把六组报告写成整Mod通过。历史baseline继续保留其真实0.3.1／历史profile身份。
5. **RC7补测而非纯静态豁免。** 新候选先通过新的open_kaishek完整检查和EXE／profile门禁。每政府直接加载其已冻结RC6 C0起点，在新run原生保存，验证实际设计、stock／population／layout／jobs／flags／ledger、C/L/R/P／六tier零及原非优惠成本；实际推进一次本来所需的月度回调、原生再保存，证实零循环分支没有奖励、组件／普通舰／维护布局没有改变且净电非负。输入旧SAV保留RC6身份，输出SAV必须为真实RC7。可与RC7其它必要C0分支共用，不能用新随机地图冒称逐字段复现原轨迹。此补测本身不称RC7新游戏或RC7十二个月；新游戏／全年结论明确来自受限源等价。
6. **最终说明可审。** RC6原报告、FAIL、manifest、SAV、工具源和原active-run局限不改；桥报告同时写源tree／源run／源case和目标tree／目标run／新补测，说明哪些结果是直接观察、哪些是源等价推论。最终发布记录明确“三类全年为RC6原生轨迹，经RC7零奖励源码等价与实际补测复核”，不写“RC7已原生完成三套十二个月”。

source bridge不消除本次RC6真实300／110失败，不把旧growth或高pending轨迹列入零分支。count解析／执行是否真正生效，由新的RC7预算／成长原生测试证明，不能只凭P语言静态PASS。

### 十八组的最小处理矩阵

| 组 | RC7建议处理 |
| --- | --- |
| hive／machine／purifier_startup（3组） | 仅在上述六条件完成后允许显式零奖励源等价；RC6真实新局＋RC7同输入C0补测分别标明。否则新局重测。 |
| hive／machine／purifier_economy（3组） | 同上；RC6十二个月仍叫RC6 observed source months，不retree。四个操作约束及最终日志未完成就保持PENDING；否则重跑相应RC7全年。 |
| lithoid_hive_first_month | RC6未完成，不能继承不存在的结果；RC7按原计划直接验收。 |
| mothership_configuration | 原版参考／完整布局／供电来源可作为未改依赖保留，已有原图保持原tree。实际RC7 Mother、同国同日Relic／jump及尚缺项沿既定功能分支核对，不以六组桥整体晋级此case。 |
| unlimited_growth、random_components | **必须RC7重跑完整既定18原生phase及预算、repeat／reload、真实RNG六种非零tier、源归因与普通舰负对照。** 新v5模型须精确绑定RC7新源；v1～v4与旧FAIL保留，系数／HP政策不变。不能把RC6小节点或旧预算FAIL改为通过。 |
| colossus_enemy_fire、colossus_guards、colossus_cancel_idempotence、common_settlement | **必须RC7直接证据。** 结算会调用已变的sync；将既定有效发射中至少一条与真实奖励／pending变化联动，兼收完成、回调去重与重载，避免另跑无意义重复发射。旧时长／数学／源码可作历史参考，不替代目标候选实际行为。 |
| normal_dismantle_regression | 完成路径同样调用sync且原组尚未完成；RC7直接验收，复用真实before夹具，不重复制造夹具。 |
| old_save_migration | **建议不做整组跨树豁免。** 未改的layout helper／旧伤工程政策及RC6真实输出可复用为源对照；原0.3.1／paid旧伤fixture、baseline不必重造。但RC7实际public／paid load→save→reload→save和同日helper重复应与必做重载合并执行，重新核身份／旧伤／队列／实际设计。现迁移checker与typed合同硬锁RC6，不能硬填新tree；下一步须另明确支持精确RC7分支并产新报告，保留旧v1 FAIL和旧v2字节。 |
| candidate_reload | **必须RC7实际重启／加载／高等级RNG与账本持久性；** C0迁移reload只能覆盖对应局部，不能代替高pending或高L。 |
| repeat_initialization | 采用RC7直接同日重复；可与上述C0补测或迁移功能分支合并。原RC6 exact ZIP/41checks保留参考，不扩六组桥到该组，避免额外接口复杂度。 |

整组迁移在代码上也有零分支／helper隔离依据，但其实际加载、伤害舍入、原生设计缓存与当前固定RC6工具合同使整组继承的证明成本更高。主线程已经要求RC7重载，因此建议把最少两类旧输入的目标输出收在同一必做重载路径，实际验收比再设计迁移跨树例外更简单。不能为省时跳过付费队列、受损public或旧mobilebase限制。

## 推荐的显式schema（尚未实施）

最清楚的方案是新增最终索引`eep-1019-acceptance-v2`及专门case discriminator；保留v1原有精确tree合同，不改变其含义。新schema只给上述**六个固定名称**开放受限源等价，所有其它case继续原直接原生合同。不要把旧`production_tree_sha256`字段悄悄改成“虽然证据来自另一树但视为这一树”。

```text
top:
  schema = eep-1019-acceptance-v2
  status = PASS_SCOPED_WITH_SOURCE_EQUIVALENCE
  production_tree_sha256 / production_files / static_gate = actual RC7
  runs = actual RC7 manifests only (unique run_id)
  equivalence_bridges = [{path, sha256}]

native case:
  status = PASS_SCOPED
  production_tree_sha256 = actual RC7 observation tree
  run_ids / checks / evidence = current strict native contract

source-equivalent case (only the named six):
  status = PASS_SOURCE_EQUIVALENT_SCOPED
  target_production_tree_sha256 = actual RC7
  source_case = {path, sha256, observed_tree_sha256:actual RC6,
                 observed_run_ids:[actual RC6 run]}
  equivalence_bridge = {path, sha256}
  target_native_smoke = [{path, sha256, run_id:actual RC7}]
  check_basis = each required check -> source observation ref + bridge + smoke scope

bridge:
  schema = eep.1019.zero-reward-source-equivalence.v1
  state = PENDING until both real trees and all reviews exist
  source_tree / source_full_manifest / source_cases / source_tools / source_logs
  target_tree / target_full_manifest / target_static_gate / target_native_smoke
  exact_delta = one count=200 insertion + version metadata only
  dependency_file_and_body_hashes / zero_branch_preconditions / checks
```

经济源等价分支使用明确的`observed_source_months`（RC6真实tree／run／日期／net／native_save）及`target_smoke`，不把旧SAV塞进v1含义为“最终候选原生十二个月”的candidate_months。baseline_months仍是独立历史输入。旧source manifest只在typed source／archives中出现，不能绕过顶层新runs的精确RC7校验。桥只证明相应六case的限定等价，不代表旧RC6整体已接受。

最小可信来源报告可采用新限定schema（例如`eep.1019.c0-startup-economy-source-acceptance.v1`），含六组现有check的完整真实结论及证据，不借用一个不存在的RC6整矩阵final-result。纯手填true、缺收据／缺日志／操作约束null、未经source归档绑定的旧report一律拒绝。

## 未来实现范围与验收标准

若主线程采用桥，建议后续只改：`publish_1019.py`／定向测试（新typed桥验证及v2分派）、独立源等价证书／限定源报告／目标smoke证据、进度组装helper对v2的独立支持。RC7成长v5精确分支、迁移RC7精确分支另按各工具授权实施，不能通过publish全局忽略tree来回避。正式化仍只对最终已验证RC7作descriptor版本元数据转换；图库源也保留其实际RC6或RC7身份与日期。

必须覆盖正反例：额外生产文件差异／非唯一while／count非200／descriptor其它字节变化、未知source或target树、旧manifest混入新runs、任一R/P/tier非零或缺零分支证明、源四操作约束null／假source PASS／缺log、目标smoke缺原生收据／错EXE或语言、多给第七个继承组、旧SAV假称RC7月份、桥替代成长／PK／reload、baseline和observed source共用路径、原FAIL被改status。所有这些应拒绝；现有v1精确tree测试、迁移旧FAIL及HP／模型／18case要求继续保持。

当前结论仅为**可审阅设计**：六个C0组具备严格窄桥的合理性；迁移／重载与受影响成长、PK不强凑复用。RC7未实际冻结，四操作链／源日志和目标smoke未完成，任何桥仍PENDING。若不能完成该typed来源与精确差异证明，建议直接重跑，不放宽现门禁。

## 最终处置与封口

主线程明确选择重跑，原因是保留现有exacttree门禁比增加跨树schema／限定来源报告／smoke桥更简单、可审，且不让“代码等价”误读为新的实际全年。后续不实施本文v2结构，也不把RC6三类年度SAV塞入RC7 candidate_months。

RC7真实流程从导入RC6干净C0开始成长，只作为带原输入来源的growth entry，不是RC7新游戏／开局经济证据。三类RC7新局与全年另行真实采样；public／paid旧伤fixture保留原始字节，RC7生成新的迁移／reload输出。RC6真实300／110失败、原v1精度FAIL、旧RC6 v2及全部历史归档保持。

本设计写作起点RC7尚未冻结；其后线程交付真实RC7树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`与v5源模型，但这不改变主线程不采用跨树runtime桥的决定。生产语义差异的真实来源见`1019-rc7-static`及`six-core-source-expectations-v5.json`；新源证书是公式／来源绑定，不继承旧runtime PASS。本文自此封口，不改任何gate或旧证据。
