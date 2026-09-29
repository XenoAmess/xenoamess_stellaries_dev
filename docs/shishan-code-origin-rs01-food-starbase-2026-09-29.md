# RS-01/02 星港食物生产对照（2026-09-29）

## 目标与范围

补足资源来源矩阵中缺少的食物持续生产样本。Stellaris 4.5.1 原版 `common/starbase_buildings/00_starbase_buildings.txt` 的 `hydroponics_bay` 每月生产 `food = 10`，其 `possible` 对玩家国家使用 `is_ai = no` 分支，因此机械主体玩家也能拥有该生产来源。正式「屎山代码」阶段修正包含每阶段唯一的 `country_food_produces_mult`。本测试只使用简体中文、Steam 离线、正式单 Mod 隔离局；不修改发布包。

## 设计与验收标准

从没有临时修正引用的正式机械起源原生存档加载，为玩家授予原版 `tech_hydroponics`，在玩家拥有的已升级星港用游戏 UI 建造一座原版水培舱，必要时仅用原版时间加速等待完工。确认存档中该建筑确实存在，`budget.current_month.income.starbase_buildings.food` 或原版实际记录类别有非零食物收入，再保存共同锚点。任何控制台辅助只作用于测试存档，须注明并核对脚本日志。

从同一锚点独立设局势第二与第五阶段，跨过同一个月结算并保存同日原生存档；若可行，再加入第一、三阶段。核对建筑数量、其他食物来源、局势进度、主物种、岗位劳动力和收入类别稳定。原版水培舱基础 `10` 时，第二/第五阶段该来源应为 `10/2.5`；如果原版其他固定增益存在，按同基线差额与基础产出核算，不直接拿净收入比值推断。临时给库存的食物不得计入月产出。保留 UI、ZIP 存档、SHA-256、`open_kaishek` 和日志证据。

若建造条件、控制台加速或原版产出类别不符合预期，则保持该资源子项待测并调整夹具，不把零收入当作通过。

## 执行结果

在正式单 Mod `fe44`、简体中文、Steam 离线的隔离局，从 `pr01-threshold-formal-reloaded-2230.04.20.sav` 载入。原版控制台执行 `research_technology tech_hydroponics` 与 `research_technology tech_starbase_3`；`tech_starbase_2` 也执行了一次，但该科技原已是起始科技。游戏星港 UI 先升级为星垒，再在空建筑槽选择「水培舱」。原版 `instant_build` 仅在升级和建筑施工期间开启，施工后明确关闭，控制台回显 `Instant build mode is OFF`。UI 证据为[可建水培舱](../assets/shishan-code-origin/evidence/rs01-food-ui-build-menu-2230.09.20.jpg)与[水培舱完工](../assets/shishan-code-origin/evidence/rs01-food-ui-built-2230.09.25.jpg)。建筑自身提示基础食物 `10`、第一阶段实际 `12.50`。

跨自然月结算后保存[第一阶段共同锚点](../assets/shishan-code-origin/evidence/rs01-food-anchor-2230.10.17.sav)。从此锚点分别经控制台 `effect every_situation={set_situation_progress=300}` 和 `...=1000` 切入第二、第五阶段，再各自自然推进到同一 `2230.11.01` 月结算，保存[第二阶段](../assets/shishan-code-origin/evidence/rs01-food-stage2-2230.11.01.sav)与[第五阶段](../assets/shishan-code-origin/evidence/rs01-food-stage5-2230.11.01.sav)。两张简中[II 阶段截图](../assets/shishan-code-origin/evidence/rs01-food-stage2-2230.11.01.jpg)、[V 阶段截图](../assets/shishan-code-origin/evidence/rs01-food-stage5-2230.11.01.jpg)与原生存档日期一致。

| 存档 | 日期 | 局势进度 | `starbase_buildings.food` | SHA-256 |
| --- | --- | ---: | ---: | --- |
| 第一阶段共同锚点 | `2230.10.17` | `48` | `12.5` | `179385a514701c94442e48af63380569dc41bc7b8a15e672c56b59df65970913` |
| 第二阶段 | `2230.11.01` | `308` | `10` | `bc54137880a2c4b4ccb72eece8505ca825cd0ed0dc8d5165a5fc9369629f067e` |
| 第五阶段 | `2230.11.01` | `1000` | `2.5` | `400735e386da4efa8f9321131593a62e9220c4dd8809e0ba4239ad95b67217bb` |

三份原生存档均为「屎山代码」起源、相同的主体物种特质和维护次数 `n=3`，玩家首都星垒建筑槽 `1` 均为唯一的 `hydroponics_bay`。玩家预算里食物收入只有 `starbase_buildings` 一类，没有其他食物生产来源；三份存档均不引用科研加速夹具。[只读审计结果](../assets/shishan-code-origin/evidence/rs01-food-audit-2026-09-29.json)为 **7/7 PASS**，由 `py tools/shishan_code/audit_rs01_food_starbase.py --output assets/shishan-code-origin/evidence/rs01-food-audit-2026-09-29.json` 可重跑。三个收入值与 `10 × (1.25 / 1 / 0.25)` 完全一致；第二、第五阶段同日分支将食物持续生产的单次阶段修正与无加成、`-75%` 分开验证。

`open_kaishek` 使用项目根目录 `shishan_code_origin` 重跑为 **PASS**：19/19 P 脚本、13 DDS、172 本地化键，报告 `_runtime/shishan_code/accept_rs01_food_20260929.json`。第一次把参数指向 `mod` 内容目录，得到 `MOD_METADATA_MISSING`；纠正为含 `VERSION` 的项目根后通过，这是测试调用错误。隔离局 `error.log` 未出现本 Mod 文件或水培舱脚本错误；旧创意工坊路径缺失和原版 `GetName` 文本提示不归因于本 Mod。非中文翻译**静态校验通过，运行时不在范围内**。本测试没有逐阶段重复建造或验证每一个食物设施，结论限定为一座原版水培舱的持续生产来源。
