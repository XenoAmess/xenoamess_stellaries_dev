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
