# 资源来源隔离补充调查与定点验收设计（2026-09-28）

## 目标、范围与方案

验收阶段 I/III/V 对持续生产的岗位、空间站、巨构和国家固定收入各只施加一次修正，同时排除市场交易、附庸税与贸易协定。本轮先只读比较已归档的同日 `2227.03.03` 第二/第五阶段分支，再从同一暂停存档做定点切阶段复核；若发现真实漏项，先修本文设计和标准，再改 Mod 并重跑 `open_kaishek` 与受影响实机路径。

## 同日存档初读

归档的 `_runtime/shishan_code/trade_stage2_22270303.sav` 与 `trade_stage5_22270303.sav` 是从同一早期基线分别推进的游戏分支。读取玩家预算 `budget.current_month.income`：

| 来源及资源 | 第二阶段 | 第五阶段 | 初步解释 |
| --- | ---: | ---: | --- |
| `country_base.energy` | 40 | 10 | 基础月产出为四分之一。 |
| `country_base.minerals` | 40 | 10 | 基础月产出为四分之一。 |
| `country_base.physics_research` | 10 | 2.5 | 基础研究点为四分之一。 |
| `orbital_research_deposits.physics_research` | 3 | 0.75 | 研究站为四分之一。 |
| `orbital_mining_deposits.energy` | 11 | 3.5 | 方向正确，但两分支合计源数量或原版增益可能不同，须逐站冻结比较。 |
| `country_ruler.influence` | 0.25 | 0.05 | 方向正确，可能受原版影响力精度/其他修正影响。 |
| `country_ethic.influence` | 0.5 | 0.1 | 同上。 |
| `country_power_projection.influence` | 0.2 | 0.2 | 没有观察到变化，须定点查明。 |
| `planet_traders.trade` | 20.25658 | 5.40658 | 已在贸易来源记录中核对一次阶段修正，岗位劳动力略有差异。 |

不能把这两个自然推进分支直接当作相同舰队、相同岗位和相同原版加成的受控实验。原版 `common/economic_categories/00_common_categories.txt` 中 `country_power_projection` 的父类是 `country_container`，再继承 `country`，并单独生成 `country_power_projection_influence_produces_mult`；运行时修正文档同时列有这个键和 `country_influence_produces_mult`。父类继承能否影响该特殊收入，必须由实测决定。原版 `common/country_container/00_country_container.txt` 另定义该收入来源，不能因键存在便假定需要叠加。

## 定点复核与验收标准

1. 从同一已保存暂停状态，记录舰队力量、影响力产生项、空间站数量、岗位、所有生产修正。只改本 Mod 局势进度到第二与第五阶段；各推进恰好一个日结算、保存。必要时从基线重新加载第二支，避免前一支的效果残留。
2. 对预算中的每个来源比较阶段倍率；以每月实际结算和 UI 来源提示交叉验证。若力量投射为零或受舰队规模变动，重建非零且不变的舰队条件后复测。仅在同一基数仍不变时判定漏覆盖。
3. 若确为漏项，增加**只针对该来源**的类别修正，且不对已受 `country_influence_produces_mult` 的其他固定来源再加一次。新修正须在第二阶段为零，I/III/IV/V 分别为 `+25/-25/-50/-75%`；检查其与全国键是加法还是乘法，取能使该笔收入恰好只受一次本起源修正的形式。若无法在原版类别上实现互斥，另设计脚本来源方案，不以多加一个全国键掩盖问题。
4. 记录同一基线的 ZIP 存档哈希、`gamestate` 中 `budget.current_month.income`/`trade_income`、简中截图、`error.log`；源类别不适用的资源标 `N/A`，缺口标 `PENDING` 或 `FAIL`，不写为通过。

目前仅为调查，**尚未据此修改 Mod**，RS-02/RS-03 仍为部分通过、部分待验收。

## 同一基线、下一次月结算的实测

本轮发现 `budget.current_month` 在游戏内切阶段后的**当月**仍记录上一次月结算值。`2203.06.09` 设为第二阶段和 `2203.06.17` 设为第五阶段的两份月内存档，其预算数值相同，不能用于判断修正是否生效。随后分别从两份已保存状态自然推进过 `2203.07.01`，得到[第二阶段存档](../assets/shishan-code-origin/evidence/resource-stage2-2203.07.08.sav)（`2203.07.08`，SHA-256 `d827d010f3a1b050d21ecc25a8ed54e9b3642786bd0bed45968ab91ba272759c`）及[第五阶段存档](../assets/shishan-code-origin/evidence/resource-stage5-2203.07.19.sav)（`2203.07.19`，SHA-256 `c5f791765614a073e4fbe02eeda1671ef055fc3e660454ffcbb6b9a37ae66d33`）。两支均在同一轮七月月结算后取 `country=0` 的预算；不是上面先前自然推进 2227 年的两支。

| `country=0` 持续来源 | II 阶段 | V 阶段 | 比值与判定 |
| --- | ---: | ---: | --- |
| 国家基础能量、矿物 | 各 20 | 各 5 | `0.25`，符合一次阶段修正。 |
| 国家基础三类研究 | 各 10 | 各 2.5 | `0.25`，符合一次阶段修正。 |
| 国家基础消费品 | 15 | 3.75 | `0.25`，符合一次阶段修正。 |
| 国家基础合金 | 5 | 1.25 | `0.25`，符合一次阶段修正。 |
| 国家基础影响力 | 3 | 0.75 | `0.25`，符合一次阶段修正。 |
| 国家基础凝聚力 | 10 | 2.5 | `0.25`，符合一次阶段修正。 |
| 采集站能量、矿物 | 各 10 | 各 2.5 | `0.25`，符合一次阶段修正。 |
| 研究站工程学 | 3 | 0.75 | `0.25`，符合一次阶段修正。 |
| 力量投射影响力 | 1.17646 | 0.2 | 不能按固定来源比值下结论；其原版 `navy_coverage_shortage` 另施加独立乘数，且两支日期、舰队状态有差异。仍标待测。 |
| 矿工矿物 | 41.50784 | 15.10784 | 不等于四分之一；两支的人口劳动力与原版来源修正需要逐岗位对照，不能把总预算差值直接归因于重复加成。 |

这两份存档把国家基础和采集/研究站至少六类资源的**一次**阶段产出修正实机闭环了。仍没有巨构、稀有资源、附庸/协定的受控样本。力量投射不能只因上述 `2227` 分支同为 `0.2` 就判“漏项”：较新受控分支显示它会变化，且游戏静态定义中存在随海军覆盖率而变的 `navy_coverage_shortage`。下一步须冻结或直接读取该修正的实际数值，再定性。

2026-09-29 补充：已用海军覆盖率严格等于 `1`、舰队规模 `75`、帝国规模 `50` 的同基线分支关闭力量投射疑点。第二/第五阶段在同日月结算后的该项影响力收入为 `2/0.5`，恰为 `1:0.25`；此前 `0.2` 受低海军覆盖率与底端截断干扰。证据、存档哈希和截图见[力量投射受控探针](shishan-code-origin-power-projection-probe-2026-09-29.md)。该来源现为通过；本文件后面其他来源的待测描述仍以各自执行结果为准。

## 稀有资源站定点夹具（计划）

在上述 `2203.07.11` 单 Mod 存档的隔离副本上，先以原版 `has_research_station`/`has_mining_station` 过滤**已建站**的未殖民天体，再用控制台效果加入原版矿藏 `d_dark_matter_deposit_2`、`d_living_metal_deposit`、`d_nanites_deposit`、`d_artifacts_research_1`；不要改正式 Mod，也不要把夹具存档覆盖正常验收存档。原版矿藏文件确认四者分别提供暗物质、活体金属、纳米机器和文物的持续轨道产出。若某类站不存在，先只在已拥有星系的适合天体上创建相应站，记录实际脚本和日志。

从同一个夹具基线复制第二/第五阶段分支，各推进到下一次月结算以后，比较玩家国家预算中四类 `orbital_*_deposits` 收入是否以 `1:0.25` 缩放，并读取站点 UI 确认没有把一次性赠与算成月收入。每种资源必须有非零样本；任何一个为零、来源缺失或被潜在条件拒绝时标待测，不能借其他资源的结果代替。

### 执行结果：四类稀有轨道产出

隔离游戏 `2203.07.11` 暂停时，以国家作用域执行 `every_system_within_border` → `every_system_planet`：给已有研究站的天体加入 `d_nanites_deposit`、`d_artifacts_research_1`，给已有采集站的天体加入 `d_dark_matter_deposit_2`、`d_living_metal_deposit`。控制台回显各矿藏已添加；存档内四种矿藏键均非零，星系地图出现暗物质、活体金属、纳米机器和文物图标。注意原版 `d_dark_matter_deposit_2` 实际收入列在 `orbital_research_deposits`，以存档预算分类为准。夹具只存在隔离游戏，未写进正式 Mod。

保留[夹具基线](../assets/shishan-code-origin/evidence/rare-station-baseline-2203.07.11.sav)（SHA-256 `86a8650bed20d1751aa5cd45fdeee01b44dfdcB21eff31e56c422a570a9d1c0e`），从它分别设局势进度 `300` 和 `950`，两支均推进至 `2203.08.03`，保存[第二阶段](../assets/shishan-code-origin/evidence/rare-stage2-2203.08.03.sav)（`6a1a0cdbca32e1d9192ff71fad259ebc8be7a79fa5bb97786b32b6acc0cc88b2`）和[第五阶段](../assets/shishan-code-origin/evidence/rare-stage5-2203.08.03.sav)（`732b9ea81ffb24bf746ddec0dd24be8921b935769d4e20b36958c545dfa9d086`）。读取两份存档玩家 `country=0` 的 `budget.current_month.income`，两支均已跨过 `2203.08.01` 月结算：

| 持续轨道收入 | 第二阶段 | 第五阶段 | 倍率 |
| --- | ---: | ---: | ---: |
| `orbital_mining_deposits.sr_living_metal` | 4 | 1 | 0.25 |
| `orbital_research_deposits.sr_dark_matter` | 8 | 2 | 0.25 |
| `orbital_research_deposits.nanites` | 3 | 0.75 | 0.25 |
| `orbital_research_deposits.minor_artifacts` | 1 | 0.25 | 0.25 |

同预算内采集站能量/矿物 `10→2.5`，研究站工程学 `3→0.75`，与先前正常存档一致。四项是月收入而非一次性加库存，因此在此类来源的第五阶段单次修正通过；巨构、附庸/协定仍待独立取样。

## 巨构建筑定点夹具（计划）

原版 `common/megastructures/01_dyson_sphere.txt` 的完整戴森球 `dyson_sphere_5` 在 `megastructures` 经济类别持续生产 `4000` 能量。下一轮从已有隔离基线载入，用原版 `spawn_megastructure` 效果在本国星系生成一座**归本国所有**的完整戴森球；先保存并确认存档的 `megastructures.energy` 为非零。由该夹具基线分别设第二/第五阶段，跨过下一次月结算，预期同一座戴森球为 `4000→1000`（若存在同类原版修正，先核对同源基数后按 `0.25` 比较）。只在隔离存档执行，保留效果、错误日志、三份存档和哈希；若游戏拒绝在有殖民地星系生成，改用其他已占星系或记录待测，不更动正式 Mod 来掩盖缺口。

第一次夹具尝试在仅有首都星系的 `2203.07.11` 存档中把完整戴森球脚本生成在首都恒星，游戏随即显示该帝国灭亡，殖民地数变成 `0`。这符合原版 `dyson_sphere_5.possible` 要求星系没有自然殖民地；控制台强行跳过此条件使样本失效，**不是本 Mod 的失败**。放弃这份未保存的游戏状态，从此前基线重新载入；下一次只在已有国境内的无殖民地星系生成，不对首都重复该效果。

第二次从 `2227.03.03` 后期存档以 `random_system_within_border` 且排除殖民星系尝试，保存前分支后 `gamestate` 中 `dyson_sphere_5` 与 `Test_Dyson` 均为 `0`：该帝国当前领土没有符合条件的无殖民地星系。此零样本不算通过。下一步可在无殖民地的未宣称星系用 `spawn_megastructure owner=root` 建立单座**明确归玩家国拥有**的测试巨构，再由存档验证 owner 与非零月收入；若无 owner 或收入，须先为测试星系建立本国哨站，不用零样本推断 Mod 表现。

### 执行结果：完整戴森球月收入

分别载入同日 `2227.03.03` 第二、第五阶段分支，并在各自的无殖民地随机星系执行 `random_system={limit={NOT={any_system_planet={is_colony=yes}}} spawn_megastructure={type=dyson_sphere_5 name=Test_Dyson planet=star owner=root}}`。游戏生成的两座戴森球坐标不同，但在各分支均只有一座 `dyson_sphere_5`，名称 `Test_Dyson` 且 `owner=0`（玩家国家）。两支均推进过 `2227.04.01` 月结算并保存于同一日期 `2227.04.06`：[第二阶段](../assets/shishan-code-origin/evidence/dyson-stage2-2227.04.06.sav) SHA-256 `59d1f73d9aa210947cf4fe1f5b9d16c704b5a08c0ab173b53aa96de57a72a31f`；[第五阶段](../assets/shishan-code-origin/evidence/dyson-stage5-2227.04.06.sav) SHA-256 `284844e909da56ce177c8940fc244d6aba2ce723dfbd2419f82eb622b5a408f4`。

两份玩家 `budget.current_month.income.megastructures.energy` 分别为 **`4000` 与 `1000`**，恰好是原版定义的完整戴森球基础产出与一次 `-75%` 修正。顶部净能量因其他收支而分别约 `+3000` 与 `+880`，因此判定采用预算来源而非顶部净额。这里验证的是由玩家拥有的巨构收入类别；为避免消灭唯一殖民地，夹具放在未宣称的无殖民地星系，尚未另测国境内合法建造流程。

## 转移收入的原版经济类别审计

在 Stellaris 4.5.1 原版 `common/economic_categories/00_common_categories.txt` 中，`subjects` 的父类为 `diplomacy`，`commercial_pacts` 同样以 `diplomacy` 为父类，而 **`diplomacy` 本身以 `country` 为父类**。故不能只因本 Mod 没有写 `subjects` 或 `commercial_pacts` 专属键，就推断它们完全不继承全国生产倍率。另一方面，`monthly_trades`、`subject_tax` 和 `overlord_subsidy` 没有 `parent`。后者若确为实际收款类别，应与 `country` 生产倍率分离，但仍须在存档预算里确认真正归属。每月市场交易已有同日实机分支确认数量与支出不变；附庸税和贸易协定的实际收款仍须外交夹具才能标实机通过。此处保留继承风险，不作静态通过结论。

原版 `agreement_term_values/00_agreement_term_values.txt` 的隐藏保护国条款会用 `subjects` 类别额外产出 `0.25` 影响力，它与一般附庸资源税并非同一个已确认来源；`diplomacy_economy/00_diplomacy_economy.txt` 中 `commercial_pact` 在 `commercial_pacts` 类别只定义影响力**维护费**。这进一步说明不能仅靠名称判断收入归属：须在实际成为宗主国/签署协定后的 `budget.current_month.income` 里逐项看来源，才能判断是否被本起源倍率误放大。

### 附庸税受控样本（计划）

从已存 `2227.03.03` 后期夹具载入，按原版 `set_subject_of={who=root preset=preset_tributary}` 将一个正常、独立且有殖民地的 AI 帝国设为玩家的朝贡国；先跨月并确认玩家预算出现非零的附庸税来源，再保存为共同基线。从该基线只切换本局势到第二/第五阶段，各推进一次月结算。预期附庸税来源数值不被第五阶段额外乘 `0.25`；若不同，先核对属国本身的收入是否因 AI 行为变化，再用相同定额合同或脚本收款复测。不能把 `subjects` 的隐藏保护国影响力与资源税混为一谈。若不能造出稳定、非零受控样本，状态保持待测。

### 执行结果：朝贡国资源税

从 `2227.04.06` 第五阶段的戴森球分支，执行 `random_country={limit={is_ai=yes is_country_type=default is_subject=no} set_subject_of={who=root preset=preset_tributary}}`，游戏出现与目标帝国建立通讯的事件。跨过 `2227.05.01` 后，玩家预算确实出现 `subject_tax` 收入：能量 `51.61026`、矿物 `46.43292`、食物 `25.21549`；这证明夹具不是只有关系标记的零税属国。[共同基线](../assets/shishan-code-origin/evidence/subject-tax-baseline-2227.05.11.sav) SHA-256 `f49d6e4990800d8ba934f11b824093f96fddb7db69e442dbbaad0e4416943381`，局势为第五阶段。

从共同基线分别切到第二阶段或保持第五阶段，均跨过 `2227.06.01` 后检查玩家 `budget.current_month.income.subject_tax`：

| 资源税 | 第二阶段，`2227.06.08` | 第五阶段，`2227.06.05` | 第五/第二 |
| --- | ---: | ---: | ---: |
| 能量 | 60.27161 | 60.22479 | 0.9992 |
| 矿物 | 49.63913 | 49.61972 | 0.9996 |
| 食物 | 25.64461 | 26.53138 | 1.0346 |

[第二阶段存档](../assets/shishan-code-origin/evidence/subject-tax-stage2-2227.06.08.sav) SHA-256 `20b10bedb3efec1764eff5bef653b70818954fa2feabfb1e8605d0af89e7ba15`；[第五阶段存档](../assets/shishan-code-origin/evidence/subject-tax-stage5-2227.06.05.sav) SHA-256 `a5de5fe682e6ab5fd1350c7fea4d3986328f7325d5f3de66153b678433146327`。两个分支在同一次六月月结算后取得非零税收，同一来源均没有变成四分之一；几百分点以内的差异与朝贡国 AI 经济在分支中变化相容，故此证据可排除本起源对资源税施加 `-75%`，但不声称逐分固定属国的每项基础产出。游戏类别定义中 `subject_tax` 无 `parent`，与实测一致。

### 双边每月资源交易（计划）

用户此前所说的“贸易协定”在本验收中按**帝国之间的双边每月资源交换**解释；这与原版 `commercial_pacts`（商业协议）的影响力维护费及贸易额政策不同。通过游戏外交界面向已建立通讯的国家提出一份双方每月固定数量的资源交易，在双方同意后至少跨一个月，确认玩家预算出现实际交易收入及支出，保存为共同基线。随后只切换局势阶段并分别跨月结算，要求合同固定的月度交付数量不因生产倍率改变。若无法造出非零收款合同，保持待测，并在报告中区分商业协议与资源贸易合同。

### 执行结果：双边固定月度交易

从已建立朝贡关系的隔离局，在外交界面向马贡尼德同盟提出十年期交易：玩家每月交付 `10` 能量币，对方每月交付 `5` 矿物。AI 原本拒绝这份报价；为了构造非零收支样本，仅在该测试存档中临时打开控制台 `yesmen` 促成协议，随后再次执行 `yesmen` 关闭。游戏外交提示确认接受，且报价窗口明确显示双方交付数量与期限。此夹具只改测试存档，没有改正式 Mod。

跨过下一次月结算后保存[第五阶段交易基线](../assets/shishan-code-origin/evidence/bilateral-trade-baseline-2227.08.06.sav)，SHA-256 `cdf81fb0ce7164feb2f519677b85c343cf712cf13033b4e038ac7e139b6e558b`。随后在同一局内依次将局势设为第二阶段进度 `300`、第五阶段进度 `1000`，各跨过一次月结算并保存[第二阶段](../assets/shishan-code-origin/evidence/bilateral-trade-stage2-2227.09.06.sav) SHA-256 `5567a2dab73fa4730d844cdf3ed354ed75a69e0acb8ee6d180900e5c7fc6a4cd` 和[第五阶段](../assets/shishan-code-origin/evidence/bilateral-trade-stage5-2227.10.06.sav) SHA-256 `a3980bef75d55344e878b7c93e52508efb00aeeaa1b10e3781fe07a419245eb0`。检查玩家国家 `budget.current_month`：

| 项目 | 基线 V | II | 再回 V |
| --- | ---: | ---: | ---: |
| `trade_income.monthly_trades.minerals`（协议收款） | 5 | 5 | 5 |
| `trade_expenses.monthly_trades.energy`（协议付款） | 10 | 10 | 10 |
| `trade_income.monthly_trades.trade`（原有市场交易） | 20 | 20 | 20 |
| `trade_expenses.monthly_trades.minerals`（原有市场交易） | 28 | 28 | 28 |
| `income.country_base.energy` | 10 | 40 | 10 |
| `income.country_base.minerals` | 10 | 40 | 10 |

结论：双边月度资源合同与市场月单均归入 `monthly_trades` 的交易收支，实际固定数量未被本起源阶段生产倍率放大或缩小；国家固定产出则按局势切换。这里验证的是双边资源交易合同；原版 `commercial_pacts` 商业协议收入如需另行主张覆盖，仍须有非零商业协议样本。

## 2026-09-29 同资源混合来源复核方案

已归档的 `power-projection-stage2-2207.11.05.sav` 与 `power-projection-stage5-2207.11.05.sav` 来自相同基线、相同日期和月结算，预算里工程学研究同时有国家基础、轨道研究站、行星工程师岗位三种非零来源。先只读核对三来源、工程师岗位分配人数及原版岗位基础值，判断第二/第五阶段相差的量是否仅等于一次 `-75%` 阶段增量。然后从同一第二阶段存档作为新共同基线，分别设置进度 `0/500/950`，跨过相同月结算，取得 I/III/V 阶段同日三来源对照。岗位人数若不同，必须按实际劳动力和原版岗位基础值归一；不能将总收入的简单比值当作唯一依据。仅在来源各自可解释时把混合来源子项记为通过。

只读解包结果：两支存档的原版工程师岗位均为 `workforce=60`、`bonus_workforce=6`，有效劳动力 `66`；原版 4.5.1 `common/pop_jobs/02_specialist_jobs.txt` 的工程学基础产出为每百劳动力 `3`，即该岗位的阶段前基础项 `66×3/100=1.98`。下表是同一资源在同一国家、同一月结算同时存在的三类来源；第二到第五阶段的**差额**分别恰好是各自基础项的 `75%`：

| 工程学收入来源 | II 阶段 | V 阶段 | 差额 | 一次阶段修正的理论差额 |
| --- | ---: | ---: | ---: | ---: |
| `country_base.engineering_research` | 10 | 2.5 | 7.5 | `10×0.75=7.5` |
| `orbital_research_deposits.engineering_research` | 3 | 0.75 | 2.25 | `3×0.75=2.25` |
| `planet_engineers.engineering_research` | 2.24874 | 0.76374 | 1.485 | `1.98×0.75=1.485` |

总差额 `11.235` 与三来源一次修正的理论差额之和完全一致。岗位一栏的第五/第二比值并非 `0.25`，因为原版和其他既有岗位增产修正的常量仍在；以固定劳动力下的**差额**判断更精确。此对照支持 II→V 混合场景中三笔收入各仅受到一次本起源阶段变化。I/III/V 的共同基线分支仍按上段方案执行。

### I/III/V 同日混合来源实测

从 `2207.11.05` 同一第二阶段暂停存档分别设局势进度 `0/500/950`，三支均正常推进 30 日到 `2207.12.05` 并跨过十二月月结算。存档中的局势进度分别为 `4.9/504.9/954.9`，确属 I/III/V 阶段。三支工程师岗位均为 `workforce=60`、`bonus_workforce=6`，岗位与研究站数未变。`budget.current_month.income` 的工程学收入如下：

| 来源 | I：`+25%` | III：`−25%` | V：`−75%` | 每跨 50 个百分点的实测差额 |
| --- | ---: | ---: | ---: | ---: |
| 国家基础 | 12.5 | 7.5 | 2.5 | 5.0；基础项 `10` 的 `50%` |
| 轨道研究站 | 3.75 | 2.25 | 0.75 | 1.5；基础项 `3` 的 `50%` |
| 工程师岗位 | 2.74334 | 1.75334 | 0.76334 | 0.99；基础项 `1.98` 的 `50%` |
| 三项同存档合计 | **18.99334** | **11.50334** | **4.01334** | **7.49**；`(10+3+1.98)×50%` |

三来源同时存在且每一来源分别符合一次阶段差额；合计差额没有因「岗位产出」与「月度资源」并存而增加第二次修正。工程师岗位 I/V 的简单比值不是 `1.25/0.25`，原因同上：其他增益在两个分支保持相同，只有本起源的阶段项变化。本子项覆盖研究资源的混合来源，不能直接替代所有资源、所有 DLC 来源及各种既有修正的完整矩阵。

[第一阶段存档](../assets/shishan-code-origin/evidence/resource-mixed-stage1-2207.12.05.sav) SHA-256 `2708e5048cf6a4654d0368a52f5f782152a55374772aabd15e1b0172a0c703da`；[第三阶段存档](../assets/shishan-code-origin/evidence/resource-mixed-stage3-2207.12.05.sav) SHA-256 `4dff358a880a97a25b90cc9ee75817621b05265880702abf00845c852113e47d`；[第五阶段存档](../assets/shishan-code-origin/evidence/resource-mixed-stage5-2207.12.05.sav) SHA-256 `c3eafc6c35cff3046057fb4c82a3dddebe1ba9b4ffd8367d6359255ea7432b65`。
