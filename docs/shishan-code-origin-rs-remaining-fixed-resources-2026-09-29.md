# RS-02 剩余战略资源与星界线固定月产探针（2026-09-29）

## 目标、范围与设计

验收计划要求每种有合法持续来源的资源留下可观察样本。现有存档已覆盖活体金属、暗物质、纳米机器、文物、结晶熵和先进逻辑，但易燃微粒、异星天然气、稀有水晶、泽珞、星界线的独立持续生产样本尚未归档。本轮补这五项的**帝国固定月产出**，不将测试扩展为每一种资源的所有原版来源，也不改正式 Mod。

Stellaris 4.5.1 本体 `common/static_modifiers/13_static_modifiers_nemesis.txt` 中的 `relic_vacuum_flower_T_dwarf`、`relic_vacuum_flower_lightbringer`、`relic_vacuum_flower_M` 分别提供 `country_base_volatile_motes/exotic_gases/rare_crystals_produces_add=30`；`relic_vacuum_flower_pulsar`、`relic_vacuum_flower_rift_star` 分别提供 `country_base_sr_zro/astral_threads_produces_add=15`。这五种原版修正均是固定月产出来源。另有岗位或矿藏来源：三种普通战略资源可由原版提炼岗位或星球矿藏持续产出；泽珞有研究站矿藏及岗位；星界线有矿藏及研究岗位。因此固定月产探针通过后，仍需单独判定其他来源类别在本计划中是否已有足够覆盖，不能声称五种资源的每个来源都实机测过。

从正式单 Mod 的简中、离线、已暂停的第五阶段原生存档出发，仅用原版控制台给玩家国家添加上述五个原版修正，并确认回显后保存共同锚点。之后每次从同一锚点重新载入，单独把局势进度设为第一、第三、第五阶段的稳定内部点，推进过同一个月结算，在同日期保存原生存档。若游戏在推进中引入赤字、事件或其他来源变化，须以原生预算分类逐项核对；不满足同来源、同基础量的分支不计入结果。控制台输入失败必须由回显和存档识别，不能以自动化脚本退出码代替游戏成功。

通过标准：三个分支均有唯一原版修正和正确局势阶段；`budget.current_month.income.country_base` 的五种资源按 `1.25/0.75/0.25` 乘基础 `30/15` 呈 `37.5/22.5/7.5` 或 `18.75/11.25/3.75`，没有第二次叠加。记录日期、输入存档/输出存档 SHA-256、简中 Steam F12 截图、`error.log` 中本 Mod 错误、正式 `open_kaishek` 结果。若已有其他同资源固定月产来源，先记录基值再按其总量计算，不能硬套上述纯净数值。

## 执行结果

正式单 Mod 校验和 `fe44`、Steam 离线、简中隔离存档。从 `sv01-stage5-reloaded-2229.10.15.sav` 载入并添加五个原版修正后保存[共同锚点](../assets/shishan-code-origin/evidence/rs02-fixed-five-anchor-2229.10.15.sav)，SHA-256 `ee4a6f95e56a205a40408cb6d3863157e75f3e9b5ed2a25d5b2fa90dd241d5be`。原生存档确认五个修正各一份。各分支都从该锚点重新载入；第一、第三阶段分别将局势进度设为 `0/500`，第五阶段直接使用锚点 `950`，再各 `fast_forward 35` 天。三个分支都于 `2229.11.20` 暂停，局势进度分别为 `7/507/957`，维护次数均为 `n=2`。游戏弹出的原版星界线教程在三个分支同样出现，关闭后保存，不改变资源产出来源。

| `country_base` 月收入 | 原版基础量 | I 阶段 | III 阶段 | V 阶段 |
| --- | ---: | ---: | ---: | ---: |
| 易燃微粒 `volatile_motes` | 30 | 37.5 | 22.5 | 7.5 |
| 异星天然气 `exotic_gases` | 30 | 37.5 | 22.5 | 7.5 |
| 稀有水晶 `rare_crystals` | 30 | 37.5 | 22.5 | 7.5 |
| 泽珞 `sr_zro` | 15 | 18.75 | 11.25 | 3.75 |
| 星界线 `astral_threads` | 15 | 18.75 | 11.25 | 3.75 |

三份同日期[阶段 I](../assets/shishan-code-origin/evidence/rs02-fixed-five-stage1-2229.11.20.sav)、[阶段 III](../assets/shishan-code-origin/evidence/rs02-fixed-five-stage3-2229.11.20.sav)、[阶段 V](../assets/shishan-code-origin/evidence/rs02-fixed-five-stage5-2229.11.20.sav)的 SHA-256 依次为 `9f1fbade7c0de47ef292df6e95ae0f4ccacebf40b1c48e27d9930e3e3c7b4b9c`、`b55bc666ef653b4994f336b998b07e53c80a93d2157b785caaabba94300b76ee`、`f2383221c6f2f91b25ed4395b6ce4af9d93949d0887bb0e5d0b74ac615da94d2`。对应 Steam F12 画面与存档同名、扩展名为 `.jpg`。只读脚本 [`audit_rs02_fixed_resources.py`](../tools/shishan_code/audit_rs02_fixed_resources.py) 对日期、进度、次数、五个原版修正唯一性、五项固定收入精确值以及五项无其他收入来源共七组断言均返回 `PASS`；完整输入和结果见[JSON](../assets/shishan-code-origin/evidence/rs02-fixed-five-audit-2026-09-29.json)。共同锚点添加修正后尚未月结算，其预算中的五项为 `null`，不作为对照值。

[隔离日志](../assets/shishan-code-origin/evidence/rs02-fixed-five-error-2026-09-29.log)在本轮月结算时新增一条原版 `events/caravaneer_events.txt:2819` 的 `auto_move_to_planet` 无效目标报错；未出现本 Mod 脚本报错。日志还保留此前加载重构存档时的 `Invalid timed modifier` 提示，不归因于本轮资源产出；本轮五个原版修正和收入仍在原生存档中逐项吻合。正式 Mod 的 `open_kaishek` 为 `PASS`：19/19 个 P 脚本、13 DDS、172 个本地化键，报告 `_runtime/shishan_code/accept_rs02_fixed_five_20260929.json`。

**结论：这五项帝国固定持续月产出的 I/III/V 来源隔离子项通过。** 本轮不声称已对五项各自的所有岗位、矿藏和建筑来源逐项完成实机测试；这些来源的组合覆盖仍须与既有 RS 来源矩阵合并判断。非简中语言仍只做静态验收，运行时不在范围内。
