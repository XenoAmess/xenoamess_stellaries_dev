# RS-03 商业协议收入隔离实机方案（2026-09-29）

## 目标与范围

[验收方案](shishan-code-origin-acceptance-plan.md)要求附庸上缴、贸易协定、月度市场交易不受局势生产倍率放大。附庸税与双边定额资源合同已在[来源审计](shishan-code-origin-resource-source-audit-2026-09-28.md)通过，但原版 `commercial_pacts` 的非零收入尚无样本。这里专门测试原版商业协议，不能把已通过的双边资源合同当作它的替代。只在已隔离的**个体机械**简中游戏中构造，正式 Mod 保持不变。

## 夹具与验收标准

从已归档[个体机械 2203.09.24 基线](../assets/shishan-code-origin/evidence/rs04-tech-anchor-2203.09.24.sav)或同源分支重载。存档可见玩家为 `auth_democratic`、主物种为机械；另一独立 AI 为 `auth_corporate`，适合作为原版商业协议对象。若双方未通讯，用原版已有实例证实的 `establish_communications` 效果建立联系；可用原版 `add_trust`、外交传统和临时 `yesmen` 只满足外交前置，并在协议达成后立即关闭 `yesmen`。每项实际执行效果、错误日志及协议 UI 要记录；若因外交前置仍无法签署，不得把零收入样本记为通过。

协议生效后推进至少一次月结算，确认玩家预算有非零 `commercial_pacts` 贸易收入或明确找出原版实际归属的其他来源。将该局保存为共同锚点；从同一锚点分别进入局势 II/V 阶段，保持协议、双方贸易生产和经济政策一致，在相同日期各跨月结算一次。逐项读取玩家与协议对象的贸易生产、协议贸易收入、影响力维护费、市场交易收支和国家固定生产。转移收入应保持相同（允许双方基础贸易值可解释的 AI 小幅变化，但不得呈局势目标倍率）；国家固定生产应呈 `1:0.25`。若商业协议收入为零、原版只表现为影响力维护费，则以游戏原始经济类别、两份存档与 UI 证明确实无适用的**收入**来源，标记该收入样本 N/A；不能仅靠静态脚本猜测。

证据须包括原生存档、Steam F12 截图、玩家预算来源值、关键外交状态、输入 SHA-256、`error.log` 和正式 Mod `open_kaishek` 结果。结果写回本文件与[总验收报告](shishan-code-origin-acceptance-report-2026-09-27.md)；有实测偏差则先分析分类继承，必要时更新设计后修复正式 Mod 并回归。

## 执行结果

在原版外交界面对 `auth_corporate` 的「欧柏拉克公司」签署商业协议；[外交截图](../assets/shishan-code-origin/evidence/rs03-commercial-pact-ui-2203.10.24.jpg)中的可执行动作已经变成「撕毁商业协议」。为满足前置，仅在隔离局用原版控制台建立通讯、双方互信与好感，授予外交传统，短暂打开 `yesmen` 使 AI 接受后立即关闭；没有修改正式 Mod。`2203.11.08` 的共同[锚点存档](../assets/shishan-code-origin/evidence/rs03-commercial-anchor-2203.11.08.sav)中，玩家已有非零 `budget.current_month.income.commercial_pacts.trade=8.60061`，且 `expenses.commercial_pacts.influence=0.125`。因此本项不是零收入推断。

从锚点独立切换局势进度到 `300/950`，各正常推进至同一 `2203.12.13`，保存[第二阶段存档](../assets/shishan-code-origin/evidence/rs03-commercial-stage2-2203.12.13.sav)/[截图](../assets/shishan-code-origin/evidence/rs03-commercial-stage2-2203.12.13.jpg)、[第五阶段存档](../assets/shishan-code-origin/evidence/rs03-commercial-stage5-2203.12.13.sav)/[截图](../assets/shishan-code-origin/evidence/rs03-commercial-stage5-2203.12.13.jpg)。实际局势进度分别为 `304.8/954.8`。原生存档月预算如下：

| 玩家月预算 | II | V | 判读 |
| --- | ---: | ---: | --- |
| `income.commercial_pacts.trade` | 8.60265 | 8.60265 | 协议转入的贸易值完全相等，不随第五阶段生产倍率缩减 |
| `expenses.commercial_pacts.influence` | 0.125 | 0.125 | 同一协议持续生效 |
| `income.country_base.energy` | 20 | 5 | 第五阶段为第二阶段的 25% |
| `income.country_base.minerals` | 20 | 5 | 第五阶段为第二阶段的 25% |
| `income.orbital_mining_deposits.energy` | 11 | 3.5 | 持续生产来源受阶段影响；原版采矿科技使其绝对比例不必恰为 25% |
| `income.trade_policy.energy` | 11.59154 | 5.57166 | 聚合了玩家自身随阶段改变的贸易生产，不能当作纯协议收入 |

[只读审计脚本](../tools/shishan_code/audit_rs03_commercial_pact.py)核对原生日期、阶段、非零协议收入、协议维护费及固定收入变化，输出[机器可读结果](../assets/shishan-code-origin/evidence/rs03-commercial-pact-audit-2026-09-29.json)为 `PASS`。锚点、II、V 存档 SHA-256 分别为 `a5af06c232502584492dc3c7a8c2d29295f26cd43a1963c8d265e0ff9c06070d`、`64e78832203468e6d4c48fc1427b883191c6da9a9a3f4f74f02975ab2017b42b`、`46985da376acffe928a1c187a45ca3690ce09e224959774638fa1d55f55db3ba`；审计 JSON SHA-256 为 `f99313363cf097ad0d8db957cb0acf31827c828f6488c3c1ecf0ec83c555a1ae`。三张截图 SHA-256 依次为 `948d846b9b55814fde33c2a4d739290a5c5d89834446c40d0c37558ef20e9251`、`d001f95d24290d02b03fe71d0c479d84fb17bc673746bb5f568ea1c94c1ddbf2`、`d01da65ca49fb2ed6171eeefff42fb8b48a583006f4c776524db7fc07b979f33`。

[隔离 `error.log` 快照](../assets/shishan-code-origin/evidence/rs03-commercial-error-2026-09-29.log)只有此前离线缺失 Workshop 文件和原版 `interface/diplomacy_view.gui` 找不到 `ai_acceptance_icon` 的界面提示，没有新起源脚本报错；日志 SHA-256 `a596ca526a4f7bcf91c1fb07884f0c1a726870fba6e07f24798127f177d0c9dd`。正式 Mod `open_kaishek` 再次 `PASS`（19/19 脚本、13 DDS、172 本地化键）；机械兼容奖励 19 项静态检查通过。八种非中非英语言无英语原文或汉字占位；九种非简中语言**静态校验通过，运行时不在范围内**。RS-03 原版商业协议的非零收入排除子项通过；整个 RS-03 尚须合并其他验收证据逐项判定。
