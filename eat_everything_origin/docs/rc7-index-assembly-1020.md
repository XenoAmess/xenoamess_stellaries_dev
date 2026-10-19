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
