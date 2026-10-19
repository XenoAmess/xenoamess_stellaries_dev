# RC7 严格运行时索引的离线组装

## 目标、范围与设计

2026-10-20，本轮仅使用现有 `publish_1019.py scaffold-index` 和
`runtime_index_1019.py`，在 `docs/evidence/1019-requirements` 新建
`rc7-reference-plan-v1.json` 与 `rc7-runtime-progress-v1.pending.json`。
不修改 Mod、验收工具、已有报告或原始样本，不创建 `final-result.json`。

来源固定为 0.4.0-rc.7、59 文件树
`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，
采用 `eep-1019-acceptance-v1` 原 18 组，全部整组与组件状态继续 PENDING。
只登记已经归档的静态、成长矩阵及高等级 UI 字节，并用成长归档的唯一
`run/manifest.json` 作为 `20261019T164112Z` canonical manifest。
其它归档内相同 run 的 manifest 不重复登记。

参考计划只含工具允许的证据引用，不提供状态、check、预算或成长观测。
后续 helper 只登记报告直接覆盖的单项观测；本次从保守原则出发，所有
check 留 null，避免把报告覆盖范围或尚未取得的最终停止日志推定为通过。
未完成的实机、完整组件组、启动、经济、迁移、原生开火和重启仍待主线程收口。
RC6 来源仍保留为历史输入，不加入 RC7 runs 或 candidate 月份。

## 验收标准

1. 新索引具备原 18 组、正确 RC7 树和静态报告，所有状态仍 PENDING。
2. 每个引用是项目内已存在文件、SHA 与真实字节一致；不引用活动 artifact
   或活动 run 日志，不伪造未来归档路径。
3. 唯一 canonical manifest 通过现有 helper 的候选来源校验。
4. 成长及 UI 报告按实际 scope 附加；没有最终停止日志的组继续缺 log。
5. 通过 helper `missing` 明确列出缺口；不运行发布、不生成最终验收结果，
   不改旧报告、阈值政策、18 组或迁移 typed 合同。

## 执行记录

本文件先于新 JSON 写入。已按上述方案执行：

```powershell
python -B tools/publish_1019.py scaffold-index --output docs/evidence/1019-requirements/rc7-runtime-progress-v1.pending.json --reference-plan docs/evidence/1019-requirements/rc7-reference-plan-v1.json
python -B tools/runtime_index_1019.py --index docs/evidence/1019-requirements/rc7-runtime-progress-v1.pending.json add-run --manifest docs/evidence/1019-rc7-growth-v1/run/manifest.json --case random_components --case unlimited_growth
python -B tools/runtime_index_1019.py --index docs/evidence/1019-requirements/rc7-runtime-progress-v1.pending.json missing
```

命令工作目录为 `eat_everything_origin`。Scaffold 返回正确 RC7 树与 18 组；
`add-run` 返回 `changed=false`，证实参考计划中的唯一 manifest 已登记并通过
现有 helper 的 59 文件、静态报告、EXE、语言和 profile 身份检查。

参考计划 SHA 为
`518bb2f162bdb35f83839317f15e80fd241cd25cf6dc97995e169f2cf184f00f`。
初次生成的 pending 索引 SHA 为
`6d988076a2f5f113b04c934054021d44d38b2e8fe99ca80629b7e30b6b12cc11`。
独立只读校验逐一重新读取 1,080 处引用，对应 546 个唯一项目文件，所有
SHA 与真实字节一致。索引仍有 18 个 PENDING case、PENDING component_rewards，
138 个 check 全为 null，growth_samples 为空，三个分支的 baseline/candidate
月份均为零；没有引用任何 `.log` 或活动 artifact 路径，没有 final-result。

`unlimited_growth` 登记 539 个引用，`random_components` 登记 524 个引用。
两组共用成长归档内实际 23 个 SAV、原生 action、GPU 截图、观察／审计／报告，
不会复制为新的样本或改写报告内部路径；原绝对路径通过已封口的归档映射追溯。
五版固定来源模型只作为 analysis。UI v1 的前点击取样失败与 v2 的作用域通过
均保留；原全严格比较 21 处显示缓存差异的 FAIL 也保留。

`missing` 仍将两组的 `log` 列为缺失；其它 16 组维持无证据的初始占位。
这只是文件可用性和来源绑定结果，不是实机验收结论、组件交付结论，亦不证明
source 模型中的再生系数已经通过受损舰体实际恢复测试。

## 后续合并边界

逐 check 的 partial proposal 由另一个离线任务准备，实际封口后可通过
`attach --kind analysis` 加入对应 case；本次不据此自动设置 check、
`component_attribution_report`、组件 IMPLEMENTED 或整组 PASS。
主线程审查之后，才使用 `observe-check` 记录明确证明的单项结论。真正完成的
新 RC7 月份再用 `baseline`／`budget` helper 导入，严禁将 RC6 candidate 月份
改作本轮值。最终停止日志需在主线程真正停止进程后冻结，再按实际作用域附加。

最终仍须依照 `rc7-final-index-closeout-20261020.md` 满足完整 18 组、各组全部
原检查、三分支年度经济、真实重启及 typed 组件／迁移合同后另建最终结果。
`missing` 将迁移原 strict `damage_preserved=false` 也列缺时，不得把该值改 true；
应保留固定 v2 工程预算和 typed scope，由原最终门禁按合同判断。

## 第二轮已封口提案的合并设计

主线程另行授权把已封口的 `r7puc` 独立正常新局和完整首年记录、独立操作审查，
以及两份成长 partial proposal 合入本 pending 索引。本节先于相应 JSON 改动。
来源限于以下三份已经存在的提案及其归档引用；不读取仍活动的 Hive、媒体或日志：

- `docs/evidence/1019-analysis/rc7-r7puc-startup-economy-partial-proposal-v1.json`
- `docs/evidence/1019-analysis/rc7-unlimited-growth-partial-case-proposal-v1.json`
- `docs/evidence/1019-analysis/rc7-random-components-partial-case-proposal-v1.json`

既有 helper 的 `attach`、`add_budget`、`observe_check` 和 `update_progress` 将登记
真实引用、原生观察月份和提案中明确为 true 的原名单项检查。Pu 七项 startup 与
七项 economy 的来源分别区分原始 native report 和补充四项受控操作审查；原始报告
中的四个 null 保持原样。成长仅登记原提案明确覆盖的 6／10 和 12／13 项，不把
静态再生导出当作真实受损舰恢复，也不扩大普通舰负对照到未测的伤害／追踪／再生。

Pu 历史 0.3.1 baseline 与本轮 RC7 candidate 各只导入 12 个真实月份；不导入
Hive／Machine 候选月份。唯一 canonical run manifest 保持不变。参考计划只扩展
证据库存，不携带状态、检查结果或月份，并同步其在 pending 内的真实 SHA 引用。

如原提案中的 `component_attribution_report` 通过既有严格归因验证器，则登记该
typed 引用。`growth_samples` 仅按最终门禁原定 7 个 C/L 形状，从原报告 18 个真实
refresh/final 样本逐项核对后登记，不将 18 个阶段压成虚构样本、也不新增节点。
所有整组状态和 component_rewards 均维持 PENDING，最终停止日志仍列缺；不建
final-result、不改工具、Mod、报告、预算和迁移政策，也不执行 Git 或 UI。

### 第二轮合并结果

已通过既有 helper 的原方法合入 Pu 和成长三份提案。Pu startup 7／7、economy
7／7，unlimited_growth 6／10、random_components 12／13 的明确单项 true 已记录；
其余 106 项保持 null。Pu 历史 baseline 与 RC7 candidate 各 12 月，后者净电
`46.23969` 至 `46.75291`，其它分支月份仍为零。baseline 的旧 OBSERVATION_ONLY
JSON 保留原二进制浮点表示，如 `31.483040000000017`，不改写成提案显示的短小数。

typed component_attribution_report 通过未修改的严格归因验证器，18 个原生阶段及
五个来源模型全部匹配。最终门禁原定七个 C/L 观测已从对应 refresh/final 的真实
country/fleet 观测核对后登记，额外的 C49／C50 仍留在完整 18 阶段归因证据内。
所有 18 组和组件交付状态仍 PENDING；Pu 两组与成长两组仍缺停止日志。

截至该合并点，reference-plan SHA 为
`0035143fbf50ad554503fe7cbd8f45ea0b4ed41407e77c3c7ca2f6c5c3767a7d`，
pending SHA 为
`cdabc9ba64ef828b091f08555cc31e6e41b8daa852a4a10fa2bfd6f6805d1abb`。
1,238 处引用／623 个唯一项目文件重新逐字节 SHA 校验通过。原活动 source 路径
`tools/publish_1019.py` 在提案中保留原样；索引改引用成长归档中具有相同 SHA 的
`source/eat_everything_origin/tools/publish_1019.py`，不依赖活动工具文件。

## 已封口画廊来源的后续绑定设计

主线程另行授权在发布文案任务封口 `1020-rc7-purifier-gallery-v1` 后，将其
真实 clean screenshot、同日后置原生 SAV、receipt、audit、输入与 analysis
引用只附到 `purifier_startup`，以供将来的 gallery.source 验证来源。
该媒体记录位于纯经济 yearUI 之后；弹窗关闭可能产生矿物等实际结算差异，
不得作为第 13 个月、替换原经济末月或表述为与 yearUI 严格相等。
先确认归档和文档封口，再读取其实际字节；不读取活动媒体、日志或 Hive。
整组 PENDING、唯一 canonical run 和原静态／月份／数值政策保持不变。

本任务新增／维护的 authored JSON 使用 UTF-8 和 LF，避免 Windows 文本写入的
CRLF 在 evidence 的 `-text` 规则下形成 Git whitespace 噪声。只规范本任务两个
可变索引文件的换行；已有报告、SAV、action、原始证据及其 SHA 不变，更新索引
中的 reference-plan SHA 后重新校验。

### 画廊绑定与最终离线封口

主线程确认媒体任务已封口并提交后，读取并校验归档 index
`03f25af162663a14a172217921440d6423e4bb363ea8dda21ed8c66abf3670d4` 与
verify `3d8a05ad96a04b2298b93882a0acb9fadae133ec36ff127a9a160d978f0a6db5`。
已把固定 58 个媒体 raw、两份 authored analysis 和 index／verify，共 62 个引用，
仅通过 helper 附到 `purifier_startup`。其中 clean 图 SHA
`86bbe9b5e435fae8667e44a3cca349c2e9eef97c8c3f8c7c932b9d416de3fa6e`，
后置媒体 SAV SHA `d170383d77f516a21da859e606a4061e6b0ffcc245b69c61ed267ee346263574`；
实际 receipt、audit、GPU／OCR、输入和差异报告共同保留来源链。
原 23 处 yearUI／media 差异及严格不等结论保留，没有增加 true 检查、月份或 run。

本轮最终 reference-plan SHA：
`47d2e06a19a982798bd9aa4d6425fc706512c970810a073d34e74ac1116c4ec7`。
pending SHA：
`72e805ae88a8151dead9066a5eae850144decd35bcc725f5d7ba0a9da62b440e`。
Pu startup 当前 98 个证据引用、Pu economy 58 个，成长两组分别 544／527 个。
四组均具备 native_save／screenshot／actions／analysis，仍缺停止日志；所有状态
仍 PENDING、原 32 项 true／106 项 null 和 12＋12 Pu 月份保持不变。
封口前重新校验 1,302 处引用／685 个唯一文件 SHA、既有 pending loader、完整
typed 组件归因验证器及 UTF-8／LF，全部通过。`git diff --check` 通过。
两份可变 JSON 原来已有的 CRLF 也一并规范为 LF，因此普通 diff 行数较大；
使用 `git diff --ignore-space-at-eol` 可以查看本轮内容变化，未改动任何 raw 字节。

## 第三轮 Hive 已封口提案的合并设计

主线程确认 Hive 原生包与 UI／操作归档已经独立封口，授权仅合并
`docs/evidence/1019-analysis/rc7-r7hvc-startup-economy-partial-proposal-v1.json`
及其真实归档引用。此节先于本轮 JSON 改动。不读取活动 Machine、UI 或日志，
不改已有报告、工具、Mod，不执行 Git。

既有 helper 将登记 Hive startup 七项与 economy 七项原名单项 true、历史
0.3.1 baseline 12 月及本轮 RC7 candidate 12 月。四个操作约束只依据受控工作流
独立审查，其原始 native report 四个 null 保持不变。m00 的缓存净电
`65.48168` 不作首月；候选月份从 m01 的 `23.14466` 开始。
本局原生初始人口 5300、core 11／pc_hive／Mother 152／971 与该 preset 自身
baseline 对照，不借用 Pu 人口或其它来源。

仍复用已有唯一 canonical run manifest，保留整组、组件与全局 PENDING。
参考计划只扩充证据库存并更新 pending 内的引用 SHA；Pu 月份、成长 typed
数据、已有 32 项 true 和各原始失败结果保持原义。验收本次合并应增加 14 项
明确 true，两个 Hive 组四类归档证据齐备但最终停机日志仍列缺。

### 第三轮合并结果

Hive startup 与 economy 已各记录 7 项原名单项 true，分别附加 36／58 个真实
归档引用；两组均仍 PENDING，仅缺最终停止日志。Hive baseline 12 月与 candidate
12 月通过原 `add_budget` 导入，保存原 OBSERVATION_ONLY JSON 数字不变；例如
首月 balance 实际 JSON 为 `23.144660000000002`，没有据显示短小数重写数据。
最初只读复核将该浮点值与短小数 `23.14466` 精确比较而失败，已改为直接与原
观察 JSON 逐值精确比较，全部月份一致；未修改报告、观察或任何验收数值政策。

索引现为 46 项 true／92 项 null。18 组、组件及全局状态均 PENDING；唯一
canonical run 不变，Pu、画廊、typed 成长与其他组数据保持原样。Machine 月份
仍为零，没有读取其活动材料或运行日志。最终 reference-plan SHA：
`b63f3c80045659561e977f2d1cfd535135fb886b995bb91ca1951ef68e3c5239`；
pending SHA：
`e300c2709fff4d0040fe4887e8b6c9d9fb1aa0cc00eb3285a5fe0ef78fe6674a`。
1,449 处引用／755 个唯一文件逐字节 SHA、原 pending loader、既有完整组件归因
验证器、连续月份和原观察值一致性均通过；`git diff --check` 通过。未建立最终结果。

## 第四轮 Machine 与重复初始化提案合并设计

主线程已确认 Machine 原生／UI／独立操作包封口并提交推送，本轮仅读取
`docs/evidence/1019-analysis/rc7-r7mc-startup-economy-partial-proposal-v1.json`
及其既有真实归档。先按现有 helper 合并 Machine startup 与 economy 原名共
14 个明确 true、0.3.1 baseline 12 月及 RC7 candidate 12 月。原始 report 中四个
操作 null 不改，四项额外结论只取受控工作流独立审查。初始缓存净电 `88.90835`
不混作首月；真实 m01 `2.85755` 至年末 `8.77273`，4800 人口、pc_machine、
Mother 151／1044 以该局自身原生材料为准。未知政府预览原 UI 仍保留，不宣称
所有画面均无原始 key。

另获授权合并 `1020-rc7-repeat-initialization-v1` 内实际封口的 partial proposal
及其四项明确检查。只有实际 index／verify／提案出现并核对后才登记；现存 raw
和报告本身不提前视为完整封口。两次完整 initialize／startup／sync 的同日观察
按其真实 ZIP／SAV／输入链证明幂等，不冒充重启、重载或其它成长分支测试。

仍只修改本任务原三文件，引用同一 canonical run，所有整组与组件保持 PENDING、
最终停止日志列缺。Pu、Hive、画廊和成长 typed 来源不改义；不读取活动 cfgui、
jump 或日志，不执行 Git／UI，不修改工具、Mod、其它报告或数值合同。

### 第四轮合并结果

Machine 已合并 14 项 true、baseline 12 月与 candidate 12 月，两个组分别
36／58 个证据引用。原报告四个操作 null、缓存净电与未知政府预览原 UI 均保留。
三类政体现在都有原生 baseline 12 月及本轮候选 12 月，逐月值与各原始
OBSERVATION_ONLY JSON 精确一致，没有对显示小数重新取整。

重复初始化归档的实际文件名为 `archive-index.json`、`verification-v1.json` 和
`partial-case-proposal-v1.json`，已据此核对实际 52 payload／54 总文件及独立
9／9 检查。最初使用假定 basename `index.json`／`verify.json` 的查找未找到，
并非实际缺包；已按主线程提供的真实名称纠正读取，没有重造或修改任何原件。

已给 repeat_initialization 附加 57 个引用并记录原四项 true；两份原生 ZIP
逐字节完全一致，SHA 均为
`41a19510e73c8e92da7d0877dc29dfbcff6ccacda66457a6a34522a9d388d2db`。
该观察仅证明同日两次完整初始化幂等，candidate_reload 四项仍全部 null。
Machine 两组和 repeat_initialization 均只缺最终停止日志，整组状态仍 PENDING。

当前 64 项 true／74 项 null、18 组与组件均 PENDING，仍唯一 canonical run。
reference-plan SHA：
`25b2ecb496ed9aaf09e9ff25a62ee7962904c3597070b713dc551f79117f3fcc`；
pending SHA：
`57e49c1d4b714858086b197b2f7ca9c331fc6b048034d356f1d750ecc2f60ca3`。
1,656 处引用／880 个唯一文件逐字节 SHA、原 pending loader、完整 typed 组件归因、
三分支 72 个基准／候选月份来源与连续性均通过；`git diff --check` 通过。
没有读取活动配置／jump／日志，没有建立最终结果或执行发布。

## 第五轮配置、来源隔离及已封口跳跃的合并设计

主线程授权把已封 `1020-rc7-relic-configuration-v1` 的 10／12 项配置提案、
独立 SOURCE_SCOPED 主宰隔离提案合入同一个 PENDING 配置组。本节先于本轮
JSON 修改。来源隔离准确路径为
`docs/evidence/1019-analysis/rc7-juggernaut-source-isolation-partial-proposal-v1.json`，
SHA `baeb7f512ac15534f0480102db469ab45b2bd8101a307c6feb0daf009f54e5d8`；
限定报告 SHA `ac037a88b450ac1ccef012daa57cc62c9d814a9ab07f3d3050a6c317c1451e35`。

只通过既有 helper 登记原提案明确 true 的检查和已封字节。其它主宰一项仅表示
原版定义未被全局覆盖、EEP 专属装配／基线／成长限定绑定 Mother；来源结论的
SOURCE_SCOPED、没有普通主宰实舰样本、保留原生友军光环影响等边界随报告保留，
不能外推“所有友舰属性绝无变化”。配置中实际维护与源推导供电各保留来源，不把
正供电推算写为 UI 电力观察，不抹去早先失败诊断或十条原生 raw 差异。

真实跳跃 raw 已由主线程停止该段收集，离线接收者尚在独立封口。只有收到该包
真实提案／index／verify 后再合并 `actual_jump`，以及其它组经提案明确支持的原名
检查；不读取尚未封的 jump raw 或活动日志。未有其提案前 actual_jump 仍 null。
唯一 run、既有三分支月份、成长 typed、18 组与组件 PENDING、最终日志缺口保持。
不创建 final-result、不修改 Mod／工具／报告、不执行 Git／UI。

### 第五轮配置与来源隔离的阶段结果

已通过原 helper 登记配置 10 项及隔离 1 项，原两份提案中的 null 没有被回写。
配置组有 177 个真实引用，`actual_jump` 仍 null，日志仍列缺。当前全索引 75 项
true／63 项 null，18 组及组件状态均 PENDING，三分支 72 个月份、成长 typed、
候选重启四个 null 和唯一 canonical run 全部保持。

阶段引用复核 1,837 处／1,056 个唯一文件 SHA 通过。其余主宰单项的来源明确
指向独立 `evidence_mode=SOURCE_SCOPED` 报告，而非原 mother14 项自动通过。
真实跳跃提案尚待离线接收者封口，未据未封材料填值。

接收者现已明确封口 `1020-rc7-native-jump-v1`：实际提案
`partial-case-proposal-v1.json` SHA
`8ce2de79a060220775393a957220fbdb34a0ec0e7aa8777589fe137851903dac`，
只支持配置 `actual_jump=true`；185 raw／193 payload、25 项观察及独立 18 项归档
检查通过。按该原提案范围继续合并：C0 Mother 从 system5 到 system7、14 日蓄能、
原生实际抵达／冷却记录及 UI 200 日读数。`unlimited_growth.jump_and_shipyards_preserved`
仍 null，不从 C0 跳跃替代高成长状态的原定证据；原失败抵达尝试仍保留。

### 第五轮最终封口

已合入该实际跳跃提案，配置组现在原名 12／12 个检查均为 true，371 个真实
引用具备 native_save／screenshot／actions／analysis，仍缺最终停止日志，整组
继续 PENDING。其中其它主宰仅为 SOURCE_SCOPED 结论，jump 为独立实际原生观察；
没有把二者混为普通主宰实舰对照，也没有覆盖旧提案历史 null。

全索引现为 76 项 true／62 项 null；18 组及组件仍 PENDING、run 仍唯一。
`unlimited_growth.jump_and_shipyards_preserved` 及候选重启四项继续 null，三分支
72 个月份、完整成长归因／固定七 C/L 观测与其它组保持原样。
reference-plan SHA：
`bc49c11d530ce44204028b5c7099bbacc8ed184ff445b4999979499c78025055`；
pending SHA：
`50fbab133db3d462204f11eebef0e717bc69e8ae40704be8174d4023e06568c4`。
封口复核 2,034 处引用／1,250 个唯一文件 SHA、原 pending loader、既有完整
typed 组件归因、三分支原观察月份及 Git whitespace 均通过。未生成最终结果，
未读取活动 PK／其它实机片段或日志，未执行 Git／UI。

## 第六轮成长跳跃／船坞原合同组合证据

主线程明确授权按原合同合并已封口的
`docs/evidence/1019-analysis/rc7-growth-jump-yard-partial-case-proposal-v1.json`，
SHA `eebdc0eae3f328934561eca949e3b8c5aec0b4267b170dafeff258f69c7ea9d4`；
独立合同复核报告 SHA
`1d5c2a875934d89ecb25744ef8dd6a97d2e345b0c7728fcbd2cfa69152fc517e`。
本节先于本轮 JSON 改动，只追加原名 `jump_and_shipyards_preserved=true` 一项。

依据是同一精确 RC7 装备的实际 C0 跳跃与成长样本中推进／船坞能力保持的组合，
不新增高等级实跳或付费造舰要求。Mother 151／1044 的真实 14 日跃迁 5→7 和
200 日 UI 冷却，与另一真实 Mother 125／809 的 18 个成长状态分别明确标注；
后者 jump-drive 装备及 mobile starbase15／shipyard queue48／owner0／type ships／
simultaneous10 在全部原生样本稳定，180／180 字段检查通过。

只按提案通过既有 helper 附加封口引用、登记这一项。旧 partial 中的历史 null
与此前阶段记录不回写；新记录说明当前原合同结论升级而非补造高等级实跳。
受损恢复、毁母不重生、无效／取消不成长三项仍 null，组件 PENDING 与最终日志
缺口保持，不读活动 PK／日志、不操作 UI 或 Git 写入、不创建最终结果。

### 第六轮封口结果

原 helper 已登记该单项 true，成长组原名 7／10 项已明确；剩余三个检查及最终
日志仍列缺。旧成长／jump partial 的 null 保留；本轮组合依据和两艘实际 Mother
身份通过新报告说明。提案中的四个活动工具／parser 路径只在索引改为成长归档内
同 SHA 的 source 副本，原提案和报告均未修改。

现为 77 项 true／61 项 null、18 组和组件 PENDING、唯一 run，候选重启四项仍 null。
reference-plan SHA：
`7998a38cd3e5260b587384d68ccaf4e2f55ceeb70021215cdc81a6039d2930da`；
pending SHA：
`dc2adbee3d090fccbd07750dce93b0189ec789ffe7a7572941917eadc526ebb9`。
2,061 处引用／1,258 个唯一文件 SHA、原 loader／完整组件归因、三分支 72 月
原观察一致性及只读 `git diff --check` 均通过。未写 Git、未操作 UI、未读取活动
PK 或日志，未创建最终结果。
