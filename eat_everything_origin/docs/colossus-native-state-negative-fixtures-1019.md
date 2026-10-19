# 1019 殖民中与地面战原生负例夹具方案

## 范围与状态

本任务只读查询本机 Stellaris 4.5.2 的自动生成文档及原版用例，只新增本文档，
不改 Mod／工具／SAV、不操作桌面、不提交。所有命令是交给独占桌面的主线程执行的
待验方案，状态均为 **PENDING**。给 planet flag 命名不能建立这里要求的引擎状态。

夹具在独立原生重载分支执行，不进入经济或武器自然完成的通过矩阵。主线程使用已过
open_kaishek 的冻结包、简体中文、原生 UI 保存 before／after 及动作、截图、日志、
receipt/audit 和 SHA。两例各自从未污染的 base 重载，不串联军队和殖民操作。

当前原生运行是 `20261019T092935Z`，EXE SHA256
`400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。
`eep_mothership0` 是该运行 country0 的母舰全局目标；执行前仍须从当时 SAV 核对它
存在、归属正确，不能沿用旧运行的 fleet ID。本文不依赖控制台当前选中的 ROOT。

## 精确来源

自动生成文档根目录：
`C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261019T092935Z/logs/script_documentation`。

| 文件／行号 | 已确认合同 |
| --- | --- |
| effects.log:1336 | `start_colony = { owner = <country> species = <species> ethos = <...> }`，planet／ship scope，启动殖民过程 |
| effects.log:397 | `create_colony` 是建立 colony，不能只凭它的名字当作“殖民中” |
| effects.log:1332 | `add_colony_progress = <0.0-1.0>`，planet scope，只用于已经进行中的殖民 |
| effects.log:333 | `create_army = { name = <string> owner = <country> species = <species>/random type = <key> }`，planet／ship／colony scope |
| effects.log:1154 | `create_army_transport` 在 fleet scope 建立真实运输船及陆军 |
| effects.log:5443 | `random_planet_within_border` 在 country scope 选择境内 planet，包括未殖民星 |
| triggers.log:308、:1168 | `can_colonize = { who = <country> status = yes }` 与 `is_colonizable = yes` |
| triggers.log:3800、:3811 | `any_ground_combat_attacker`／`any_ground_combat_defender`，planet／ship／colony scope，可核实真正参战双方 |
| events/origin_events_5.txt:732–746 | `origin.7320` 在目标 Carrier 中实际调用 `start_colony`，owner 和 species 从已保存国家目标取得 |
| events/colony_events_1.txt:190–242 | `colony.4`（Rise of the Trees）在殖民地直接 `create_army`，归属新建敌对 faction；不是先生成运输船再调用虚构登陆效果 |
| events/synthetic_dawn_events.txt:1999–2017 | 原版在星球上为机器国家创建 `machine_assault_1` |
| common/armies/01_assault_armies.txt:785 | `machine_assault_1` 适用于 machine empire／trait_machine_unit，并要求 tech_assault_armies |
| common/armies/00_defense_armies.txt:10、:172 | 有机常规 `defense_army`、机器 `machine_defense` |
| events/anomaly_events_2.txt:331–350 | 原版 `create_fleet` → `set_owner` → `create_army_transport` → `set_location` 的备选运输流程 |

`effects.log` SHA256 `206dbf28fb12ffa3e8a8222d1af48d4562ffd2d4b4fe8edc43fd14d1d4d537fb`；
`triggers.log` SHA256 `a4a439ff44a3d0de7145b0db88ce18b1eec0c056a3454ea9d22d43f0afac2615`。
原版 `origin_events_5.txt` SHA256
`6cec34a55027847068fac9c290196c4f664303eaaa3523c80cb54f984580c819`；
`colony_events_1.txt` SHA256
`9ec80a0a7c9dee50fce793946685d05f215fb884589c5d700bf94929fd94205b`。

## 共用作用域绑定

先保存未污染的 base，再由当前真实母舰取得发射国。以下只增加明确命名的夹具 event
target；不是用 flag 伪装殖民／战斗状态。

```text
effect event_target:eep_mothership0 = { owner = { save_global_event_target_as = eep_pk_fixture_actor } }
```

需确认 `eep_pk_fixture_actor` 是当时发射国，且母舰身份、核心归属、EEP 初始账本均正确。
后续用完整 `event_target:` 避免当前选择／ROOT／PREV 层级误认。清理通过原生重载 base，
不通过编辑 SAV 或批量移除生产标记。

## 夹具一：真正 is_under_colonization=yes 的天然星

最短路线是 `start_colony`。先在 actor 境内选一颗正常可殖民、未殖民、未被其它国家
拥有的天然星，再启动真实过程。只选一次，先清空旧夹具目标；没有候选时必须记为
夹具未建立，不得沿用之前目标。

```text
effect clear_global_event_target = eep_pk_fixture_colonizing event_target:eep_pk_fixture_actor = { random_planet_within_border = { limit = { is_colonizable = yes is_colony = no is_under_colonization = no is_artificial = no NOT = { exists = owner } can_colonize = { who = event_target:eep_pk_fixture_actor status = yes } } save_global_event_target_as = eep_pk_fixture_colonizing start_colony = { owner = event_target:eep_pk_fixture_actor species = event_target:eep_pk_fixture_actor.species } } }
```

这是 `origin.7320` 的原生 owner/species 用法，不是 `create_colony` 的改名。不要调用
`add_colony_progress=1`，否则可能直接完成并失去负例。若境内没有合法候选，可由
主线程从原生 SAV／debugtooltip 选定另一颗真实天然空星并正确绑定目标，或使用真实
殖民船的“殖民”命令；不把 `can_colonize=no` 的星硬当正常殖民前提。

暂停，检查该目标存在且实际 owner 为 actor，并用原生 trigger 记录真实状态：

```text
effect if = { limit = { exists = event_target:eep_pk_fixture_colonizing } event_target:eep_pk_fixture_colonizing = { if = { limit = { is_under_colonization = yes } log = "PKFIX COLONIZING TRUE" } else = { log = "PKFIX COLONIZING FALSE" } if = { limit = { is_colony = yes } log = "PKFIX IS_COLONY TRUE" } else = { log = "PKFIX IS_COLONY FALSE" } } } else = { log = "PKFIX COLONIZING TARGET MISSING" }
```

保存 `pk-colonizing-before`，读取实际 colony／进度与 owner、自然 planet_class／
is_artificial，并保留日志中的 `COLONIZING TRUE`。若当日尚未建立状态，最多先推进
一个真实 tick 后重新检查；仍未成立则夹具失败，不伪造字段。

然后仅在已经证实 `is_under_colonization=yes` 的无效目标上调用 FROM 正确的原生完成
入口，验证生产事件的 guard，不冒充发射：

```text
effect event_target:eep_pk_fixture_colonizing = { fire_on_action = { on_action = on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER scopes = { from = event_target:eep_mothership0 } } }
```

同日暂停保存 `pk-colonizing-after`。EEP 的 C/G/D/made/worlds、母星人口／容量与硬件
奖励、目标销毁／信用标记、两项原生危机目标均不能新增；殖民过程和目标本身须保留。
如果引擎同时返回 `is_colony=no`，这只能认证“真实殖民中目标的联合拒绝”，不能声称
单独隔离证明了 `is_under_colonization` 这一项。记录两个原生布尔值，不能把其中一个
手工改成相反值来追求单条件用例。

## 夹具二：真正 has_ground_combat=yes 的天然殖民星

优先从主线程已有的有效敌星 base 分支开始：`eep_colossus_probe_target` 必须是天然
殖民星、有真实 owner，owner 与 actor 真正在交战，不是母星、吞噬中或已结算目标；
它的 `has_ground_combat` 起初为 no。先保存其正常状态，维持目标类型与 owner。

当前 actor 是机器帝国，最短的受控尝试是在该目标上建立真实守军和真实进攻军，
让原生陆战系统判断是否进入战斗。下例守方假定是已核实的普通有机敌国：

```text
effect event_target:eep_colossus_probe_target = { owner = { save_event_target_as = eep_pk_fixture_defender } create_army = { name = "PK fixture defender" owner = event_target:eep_pk_fixture_defender species = event_target:eep_pk_fixture_defender.species type = defense_army } create_army = { name = "PK fixture attacker" owner = event_target:eep_pk_fixture_actor species = event_target:eep_pk_fixture_actor.species type = machine_assault_1 } }
```

守方如果是机器国家，守军改为原生 `machine_defense`；不要对机器攻方误用
`robotic_army`，原版该型的 `potential_country` 明确要求 `is_machine_empire=no`。
生成记录必须显示两队真实 army、不同敌对 owner、正确 planet。无需新 faction、
新物种、额外外交或新 Mod 事件。原版直接在殖民地创建敌方军队的用例证明这是合法
构造路线，但本任务没有实际确认“这两个创建效果执行后立即进入战斗”的引擎时序。

先在暂停的同日求值；若尚未开始，最多推进一个真实 tick 后暂停复查：

```text
effect event_target:eep_colossus_probe_target = { if = { limit = { has_ground_combat = yes any_ground_combat_attacker = { always = yes } any_ground_combat_defender = { always = yes } } log = "PKFIX GROUND COMBAT TRUE WITH BOTH SIDES" } else = { log = "PKFIX GROUND COMBAT NOT ESTABLISHED" } }
```

只有真实 `has_ground_combat=yes` 且两边参战军队存在，才保存 `pk-ground-before` 并
执行下述负例。若军队只是驻扎、立即占领或战斗已经结束，不得算作地战夹具成功。
可从 base 重载并等量增加双方军队延长观察窗口；不能设 `has_ground_combat` 同名 flag。

```text
effect event_target:eep_colossus_probe_target = { fire_on_action = { on_action = on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER scopes = { from = event_target:eep_mothership0 } } }
```

仍同日暂停保存 `pk-ground-after`。比较与殖民中夹具相同的 EEP／危机账本，并确认
目标仍存在、owner 未变、战斗仍进行。任何战斗胜负导致的 owner／objective 变化都
要保留并单独归因，不能当作 EEP 回调奖励或静默忽略。

### 如直接生成军队不触发战斗：原生运输＋真实 UI 登陆后备

此后备更长，但能经由明确的原生登陆动作进入状态。`anomaly.2523` 和佣兵原版用例
证明 `create_army_transport` 可省略 graphical_culture，不能编造 `land_armies` 或
`queue_actions` 内未经本机确认的登陆操作码。

```text
effect event_target:eep_pk_fixture_actor = { create_fleet = { name = "PK ground fixture transports" effect = { set_owner = event_target:eep_pk_fixture_actor create_army_transport = { ship_name = "PK fixture transport" army_name = "PK fixture attacker" army_type = machine_assault_1 species = event_target:eep_pk_fixture_actor.species } set_location = event_target:eep_colossus_probe_target } } }
```

由主线程在简中 UI 选择实际生成的运输舰队，对真实战争敌星下达“登陆陆军”，推进至
陆战开始立即暂停，重复上述状态检查与 before／after 保存。生成运输舰本身、舰队
移动或已完成占领都不等于 `has_ground_combat=yes`。

## 交付边界

原生接口与原版用例已只读核对；两个夹具都尚未执行，本文件不发 guard PASS。
`create_colony`、已驻扎军队、人工 planet flag、缺目标而没有收益，这四种情况都不能
替代所需的真实状态。若真实殖民态无法满足其它 EEP 前提，报告联合拒绝的范围；
若真实地战没有形成，报告夹具未建立，不能因回调无收益给“地战 guard 通过”。
