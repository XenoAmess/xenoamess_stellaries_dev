# 4.5.1 特殊资源生产覆盖复核（2026-09-29）

## 范围与脚本依据

此轮检查《大厦将倾》的阶段修正是否覆盖机械起源国家可能拥有的额外**持续月度生产**。原版 `common/strategic_resources/00_strategic_resources.txt` 另外定义了 `biomass`、`menace`、`integrity`、`advanced_logic`、`feral_insight`、`entropy_crystals`。`common/pop_jobs/13_machine_age_jobs.txt` 的 `neural_chip` 岗位持续产出 `advanced_logic`；机械帝国不被 `ap_cosmogenesis` 的原版潜在条件排除。`common/static_modifiers/13_static_modifiers_nemesis.txt` 的 `relic_vacuum_flower_crisis_empire_star` 给 `country_base_entropy_crystals_produces_add=75`，是帝国固定持续月产出。引擎生成的 `logs/script_documentation/modifiers.log` 含两个 `country_*_produces_mult` 键。

因此四个有效阶段现在对这两种资源设置与其他资源相同的生产百分比，第二阶段无修正。此处的 `country_*_produces_mult` 仍是每资源**唯一一项**本起源阶段生产修正，不再叠加岗位专用修正。其余四种资源此次没有符合起源范围的持续月产出证据：`biomass` 仅对荒野帝国可见，无法与机械主体起源共存；`menace` 使用独立的无 `country` 父类经济类别；`integrity`、`feral_insight` 当前查到的是事件奖励或支出。此结论限定于原版 4.5.1 已审计来源；后来若发现新的合格来源需补测。

## 简中实机：结晶熵的固定月产出

在单 Mod、简中、离线隔离局中，给同一玩家国家施加原版 `relic_vacuum_flower_crisis_empire_star` 国家修正，确认存档中该修正唯一存在，按局势进度切换五个阶段，每次跨月后从存档 `gamestate` 的玩家 `budget.current_month.income.country_base.entropy_crystals` 读取月产出。基础值恒为 `75`，没有市场交易、附庸转移或岗位来源。结果：

| 阶段 | 目标百分比 | 实测固定月产出 | 与 75 的关系 | 证据存档 |
| --- | ---: | ---: | --- | --- |
| I | `+25%` | `93.75` | `75 × 1.25` | [stage1](../assets/shishan-code-origin/evidence/resource_crystals_stage1.03.05.sav) |
| II | `0` | `75` | `75 × 1` | [stage2](../assets/shishan-code-origin/evidence/resource_crystals_stage2.02.05.sav) |
| III | `-25%` | `56.25` | `75 × 0.75` | [stage3](../assets/shishan-code-origin/evidence/resource_crystals_stage3_valid.05.05.sav) |
| IV | `-50%` | `37.5` | `75 × 0.5` | [stage4](../assets/shishan-code-origin/evidence/resource_crystals_stage4.06.05.sav) |
| V | `-75%` | `18.75` | `75 × 0.25` | [stage5](../assets/shishan-code-origin/evidence/resource_crystals_stage5_fixture.01.05.sav) |

五份存档 SHA-256 按 I→V 顺序为 `a05ad0256d32468f04535304fc61be056da9b5ec82b78ce2a547fd8000a667e3`、`ccba52ac9092b1b63adbafb8c5099f2c54eb1cc6f500426a51bb46c65185074a`、`aad34ad08f22fba4cac9850c7adf7172af4d5bea18749e4e480d2aa38aaf28ee`、`928c6f624587f51701bc02886df0e7c8910be6e2b8dffa3d4a4153d500442c66`、`f61cccd6d607052a4d0b0160cb52b6adcac02b72514259319c38a7ca23b97370`。第三阶段的第一次自动化输入被中文输入法合并为无效命令，旧存档仍停在第一阶段，**没有计入证据**；表中 `stage3_valid` 是重新输入并在控制台回显 `500.00` 后跨月保存的有效结果。对 P 语言控制台自动化，必须复核命令回显和存档进度，不能只信任输入脚本退出码。

## 静态检查与待测

本轮 `open_kaishek` 包级检查 `PASS`：19/19 个 P 脚本、13 个 DDS、169 个本地化键，报告 `_runtime/shishan_code/accept_resource_expansion_20260929.json`。兼容特质 19 项检查通过，翻译审计的八种非中非英语言各有 0 项英文残留和 0 项非预期汉字。十种官方语言补齐两个显示键；九种外语由 MiniMax-M3 生成，候选见[翻译原始结果](../assets/shishan-code-origin/evidence/resource_expansion_minimax_2026-09-29.json)。非简中语言**静态校验通过，运行时不在范围内**。

`advanced_logic` 不能以结晶熵的帝国固定月产出测试代替；下文记录了其真实岗位生产的简中实机结果。两种资源的一次性奖励隔离均已检查。Mod 整体验收仍未通过。

## 先进逻辑岗位验收夹具设计

在当前隔离简中存档的副本中，用原版控制台效果给玩家国家添加 `ap_cosmogenesis`，将一颗测试殖民地转换为 `pc_cosmogenesis_world`，设置原版的 `purge_cosmogenesis`，并添加非虚拟主体物种人口组。依据原版 `neural_chip` 的 `possible` 与 `resources` 定义，跨月后应看到 `planet_neural_chips` 的 `advanced_logic` 正产出；若原版仅通过巨构建造回调建立岗位，则改用原版 `cosmogenesis_world` 巨构的完成效果构造星球。测试夹具只存在隔离存档，不加入发布 Mod。

固定同一份有岗位的基线存档，把局势切至五段分别跨月，读取各分支 `gamestate` 的玩家预算 `advanced_logic` 月产出以及岗位数量、局势阶段和其他相关修正。阶段修正的目标是相对同一岗位来源的原始产出加 `+25% / 0 / -25% / -50% / -75%`。引擎会将其他已存在的岗位或资源修正一起结算，所以五份存档的最终收入不必直接等于第二阶段最终收入的 `125% / 100% / 75% / 50% / 25%`；必须先保证来源、岗位人数和其他修正一致，再看五档收入是否呈等差。基线若不稳定或人口组在结算时被清除，不得宣告通过。最后从同基线施加一笔原版一次性 `advanced_logic` 奖励，确认奖励不受阶段修正放大。保留有效分支存档及 SHA-256，失败的输入与夹具要在文档中注明。

首份夹具已按原版 `spawn_planet` 建出星球，并有 97 名人口分配到 `neural_chip`，但月预算没有可读的 `advanced_logic`：原版 `num_chip_slave` 公式先将人口数乘 `0.01`、再除 `20`，因此 97 名人口的基础先进逻辑仅约 `0.0012/月`。接下来在同一测试星球增加人口与原版 `building_lathe_overclocker`，使持续产出达到预算可读数量级，再固定基线；原版超频建筑给神经芯片的先进逻辑基础产出加 `0.5`。夹具新增人口会按原版吞噬规则递减，故五个阶段从同一基线各自分支，不能把不同月份的直接数值当作对照。

执行时发现直接 `add_building=building_lathe_overclocker` 因该星球建筑槽未开放而失败，人口 `+4000` 则成功。第二阶段在下一月一度有 `1.26152` 月产出，但能量库存归零后原版赤字把 `neural_chip` 岗位劳动力清空，第一阶段后一月遂没有先进逻辑产出。该失败说明还须将能源库存固定为足够数值，并验证每份分支存档的 `neural_chip.workforce > 0`、能量无赤字与相同或可换算的岗位人口；第二阶段这份存档暂不作为最终比率证据。由于人口吞噬速度随人口数变化，各分支必须从补足能源后的同一日重新出发。

把能源库存补至约一万后再跨月，`neural_chip` 仍未重新分配劳动力；此时测试星球 2812 人，住房缺口约 531、舒适度缺口约 617、稳定度仅 `10.17`。能源赤字并非唯一条件，原先直接加入四千人的夹具过度拥挤。下一步把测试星球人口降至住房与舒适度容量以内，再跨月核查岗位恢复；若岗位仍停用，逐项检查原版岗位条件，不把赤字推断写成已证实根因。

缩至 981 人并跨月后稳定度回升为 `46.18`、住房和舒适度均有余量，神经芯片岗位却仍未分配；因此能源或拥挤都不能单独解释停工。原版岗位定义使用 `purge=purge_cosmogenesis`，机械主体物种作为玩家本族可能被原版权利系统阻止长期充当待肃清对象。下一项隔离探针将在同一星球使用存档已有的有机物种（编号 `2`，`class=ART` 且有 `trait_organic`）创建人口组，核查原版是否稳定分配神经芯片；该物种仅用于测试来源，不改变起源主体物种条件或正式 Mod。

控制台的 `create_pop_group={species=2}` 把 `2` 解释为物种脚本键，报“无法推断物种”，没有创建人口。改为在同一脚本中以 `random_galaxy_species={limit={has_trait=trait_organic} save_event_target_as=...}` 捕获真实有机物种作用域，再以 `species=event_target:...` 创建；原版脚本文档明确支持事件目标作为该参数。必须以存档确认新增物种人口组实际存在，不能仅凭命令回显。

事件目标法确实创建了 900 名有机人口，但新人口组的 `category` 没有变成 `chip_slave`，而是在跨月后被其他原版权利规则清除；该次实验也不能证明机械或有机物种在正规建造的突触磨炼机中无法产出。下一项探针显式用原版 `create_pop_group` 的 `category=chip_slave` 参数创建有机人口，随后检查岗位和一月存活；若仍失败，需用原版巨构完整建造回调而非继续推断脚本功能有缺陷。

显式类别法在创建当日的存档中确实保存了有机 `chip_slave` 人口，但跨月后这个人口组的类别消失，神经芯片再次停工。原版 `has_virtual_species_trait` 仅检查两个数字化特质，本夹具主体物种均不具备；也不能把停工归咎于该条件。直接 `spawn_planet` 夹具省略了原版巨构回调的 `set_planet_flag=megastructure` 与 `set_carrier_flag=cosmogenesis_world_resettle@from`，故接下来应验证补齐这两个标记能否让原版持续岗位分配；若不行，改用真正完成巨构建造的局面。

补齐原版巨构标记、再次显式创建有机 `chip_slave` 后，跨月仍由引擎重新分类、岗位停工，说明直接 `spawn_planet` 路径不足以仿真正规建造。下一次从 2208.06.05 的无创生夹具旧存档重开，给玩家原版 `ap_cosmogenesis`、`tech_cosmogenesis_world` 和足够建造资源，用建造船在游戏 UI 中建成原版 `cosmogenesis_world_0`，待原版 `on_build_complete` 生成突触磨炼机，再做阶段生产验收。此前人工星球所得唯一一个 `1.26152` 是短暂首月收入，不作为持续生产通过证据。

真实建造已在隔离旧存档中通过原版 UI 成功排入建造船队列，支付 `300` 影响力和 `15000` 合金；目标是首都恒星系一颗无巨构的熔融行星，界面显示“突触磨炼机的建造进度 0%”。原版首阶段建造时间 `2400` 游戏日，验收夹具可用原版控制台 `instant_build` 加速，并在完工后立即关闭该开关；完工证据须出现原版生成的 `pc_cosmogenesis_world`、国家 `cosmogenesis_world_built` 标记和稳定的跨月神经芯片岗位。加速仅用于隔离验收，不进入 Mod。

真实磨炼机的连续月份观察出现了原版合金赤字局势和 `country_defaulted`，并且 `neural_chip` 人口会按清洗规则逐月减少。顺序切换阶段得到的 `advanced_logic` 读数不能直接做倍率断言。下一轮从没有赤字局势的 `2208.08.30` 原版建成存档出发：用控制台补足主要库存，保存单一锚点；每个阶段均重新载入该锚点，仅修改本局势进度，等待完整月结算并保存同日期分支。核对每支的神经芯片岗位劳动力、人口、原版赤字/违约状态与行星产出；若原版随机事件仍使经济条件分叉，就把这项列为受控比较限制，而不是声称倍率已通过。

## 简中实机：真实突触磨炼机的先进逻辑

按原版巨构建造 UI 完成 `cosmogenesis_world_0`，存档确认得到 `pc_cosmogenesis_world` 和 `cosmogenesis_world_built`；经游戏迁入人口 UI 安置约 1300 名人口后，原版 `chip_slave` 类别和 `neural_chip` 岗位持续产生先进逻辑。把能量、合金和消费品库存补足，于 `2208.08.30` 保存[共同锚点](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_baseline.08.30.sav)。每个有效分支均从锚点载入，设局势进度后 `fast_forward 35`，于 `2208.10.05` 保存。五份存档均无原版合金赤字局势或国家违约；突触磨炼机均为 `neural_chip.workforce=1200`、人口组 `amount=1201`。这与前面人工造星球时岗位停工的无效夹具不同。

| 阶段 | 局势进度设值 | 同一岗位月产 `advanced_logic` | 对第二阶段差值 | 有效存档 |
| --- | ---: | ---: | ---: | --- |
| I | 100 | `0.23882` | `+0.04502` | [阶段 I](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage1.10.05.sav) |
| II | 250 | `0.19380` | `0` | [阶段 II](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage2.10.05.sav) |
| III | 500 | `0.14878` | `-0.04502` | [阶段 III](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage3.10.05.sav) |
| IV | 750 | `0.10376` | `-0.09004` | [阶段 IV](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage4.10.05.sav) |
| V | 1000 | `0.05874` | `-0.13506` | [阶段 V](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage5.10.05.sav) |

五档每跨一档相差 `0.04502`，没有叠加第二种来自本起源的岗位产出修正。第二阶段的第一次分支虽然显示 `0.19380`，但在同日又清洗了 47 名人口，只剩 `1153` 劳动力；这份**无效对照**保留在隔离用户目录，未归档为上表证据。重新从锚点加载，像其他阶段一样显式输入 `set_situation_progress=250` 并跨月后，第二阶段劳动力为 `1200`、人口 `1201`、产出仍为 `0.19380`；上表阶段 II 是这份重跑存档。不能用最终收入对第二阶段的直接比率解释阶段百分比，因为原版岗位和国家其他产出修正同时存在；等差值和相同来源、人数、时点证明本阶段修正按加法改变该来源。

在阶段 V 的同一暂停日期，原版控制台一次性给予 `advanced_logic=10`。给予前[存档](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage5.10.05.sav)库存 `40.34492`，给予后[存档](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage5_grant10.10.05.sav)库存 `50.34492`，岗位月产仍为 `0.05874`；一次性资源未被第五阶段的 `-75%` 生产修正削减。五阶段的实机画面与存档同名，扩展名为 `.jpg`。共同锚点、I→V、一次性奖励后存档的 SHA-256 依次为 `f85f9a3b0a9dc16c8f2986c6106338aa632ad2195c69a3205ab5b57060fb596b`、`faf0952c58bb70943eab927314d03d90771efd6ab04fe86c363f0708c52c3f71`、`f61b49f9c7bfb69064c1b6362c3d238914479ae24085b3ed8ee32cfab648d28a`、`d852b61035d4908b677da1ca4dbbb58effb692aa10359391443b953449e1c03f`、`452bdc7ee989e0235b815e8b47477be4619f2a5e1058c739b86f1b688cb64bd7`、`813ec943913873f5440f135f6315a9b6e215cdced17e89ce77803a022e506f43`、`16c890632bac1c6111469f982e668e3375bd1bcc0b7c0eba8f86ed55cf919ff6`。

同样从阶段 V 暂停存档重新加载，输入原版 `effect add_resource={entropy_crystals=10}` 并在同一天保存[奖励后存档](../assets/shishan-code-origin/evidence/resource_entropy_stage5_grant10.sav)。玩家结晶熵库存由 `562.5` 精确升为 `572.5`，固定月产仍为 `18.75`；一次性结晶熵也未受阶段 `-75%` 修正。奖励后存档 SHA-256 为 `8beb49ff88ef187eac264e93e0c008e2d0b49967c1bd524368701e59ef70625c`。
