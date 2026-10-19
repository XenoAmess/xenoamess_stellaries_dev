# 1019 原生巨像独立目标批量负例

## 目标、范围、设计与验收

用不同的原生物理星球分别承载目标拒绝条件，在回调真正评估之前持续保留负例状态，避免同一 effect 里 set flag → fire_on_action → clear flag 导致事件稍后看到已恢复有效的目标。本文仅提供源码支持的主线程操作配方，不新增 Mod、测试事件或工具，不编辑 SAV，不操作桌面。夹具星球由原生 effect 创建，明确只用于功能守卫，不用于开局经济、普通殖民拆解或真实武器发射验收。

每颗星只设置自己的拒绝条件；直到完成回调、推进一天并保存之后都不清理。清理采用实际重载原始 base，不在活动夹具中逐星移除拒绝条件。所有回调显式 FROM=唯一母舰 fleet。验收要求：七个物理目标身份不同、均真实形成殖民地并有实际人口、各自拒绝状态在保存中仍然存在、回调派发日志七条、无缺失回调或作用域错误；派发后 EEP 账本、两项原生危机 objective 和结算 receipts 没有新增，星球没有被误毁。

本文仍为 PENDING 方案。生产 `eep.50` 回调只会因 trigger 失败而不执行 immediate，负例不能证明真实充能发射。真实武器仍由主线程另行验收。

## 本机来源与边界

使用 RC3 `20261019T092935Z/logs/script_documentation`，精确 EXE SHA256 为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。

- effects.log:397：`create_colony = { owner = <target> species = <target/key> ethos = ... }`，planet/ship scope。
- effects.log:384：`create_pop_group = { species = <target> size = <number> }`，planet/ship/colony scope；未传原有 pop_group 时 species 必填。未找到名为 `create_pop` 的当前公开 effect，使用当前 4.5.2 接口。
- 原版 `events/origin_events_3.txt:335` 的实际顺序是 create_colony（owner=space_owner、species=space_owner.species）后 create_pop_group（size100、species=owner_main_species）。原版 `events/namarian_events.txt:2381` 同样先建殖民地再建1400人口。
- 既有实机 [实施验收记录](implementation-test-release-2026-10-06.md) :622 确认 create_colony 不自动生成有效人口；没有人口时 is_colony 仍然不成立。不能将这种构造失败当作某个指定 guard 拒绝成功。
- 既有 [1015实施记录](implementation-1015-2026-10-15.md) 证实 create_colony 会生成殖民地名称，若需命名应放在 create_colony 之后。
- effects.log:188：`set_carrier_flag = <key>` 支持 planet/ship/colony，colony 中的标记实际存于载体。普通无期限 flag 保持到显式移除。
- effects.log:409、:3599：`change_pc = <class>`、`set_planet_size = <int>` 支持 planet/ship/colony。
- effects.log:5368、:5389：random_system_planet/every_system_planet 都在 galactic_object scope 遍历物理 planet（不限已殖民星），有 limit；故在绑定母星的 solar_system 中使用。
- scopes.log:86、:130、:334：owner、owner_main_species、solar_system 均支持 fleet/planet；可以显式从 `event_target:eep_mothership0` 取国与主种，不依赖控制台当前选中对象。
- effects.log:2317：fire_on_action 允许 scopes.from 覆盖；原版 `common/scripted_effects/nomads_effects.txt:4724` 是真实 Carrier planet-destruction 回调转发先例。
- triggers.log:2827 的 is_artificial 读取 planet_classes 中实际属性。原版 `common/planet_classes/00_planet_classes.txt:1584` 的 pc_habitat 在 :1616 明确 `is_artificial_planet = yes`。把空星转为此类只构造真实人工类型 guard 夹具，不证明完整居住站建筑、区划、轨道或巨构生命周期可玩。

## 目标选择与七个持续状态

本轮只读 `pk1base.sav`（SHA256 `dccb1e17d6f76c915e3f0a916e627f068c559d381e7a6962becc21c77093b38a`）中，country0 母星是物理 planet2，system13；同系统有七颗无殖民地的自然对象：1/molten22、3/toxic18、4/toxic13、5/barren29、6/gas_giant25、7/frozen6（月亮）、8/barren_cold9（月亮）。只读枚举不是授权原地污染经济主线；在明确的独立 guard 分支使用，并从当时 SAV 复核。这些空星中有原有开采站，转换和清 deposits 会改变夹具经济，故不能复用为预算验收。

选择器始终排除恒星、已殖民、正在殖民、任何 eep_core，以及已经带 eep_guard_batch 的对象。每次选择立刻加 eep_guard_batch，所以后续命令不会抽到同一星。保留各自全局目标方便存档定位；不要把所有案例反复保存到同名 target。

| 全局目标 | 唯一拒绝条件 | 类型和额外设置 |
| --- | --- | --- |
| eep_guard_active | eep_active | pc_machine |
| eep_guard_devouring | being_devoured | pc_machine |
| eep_guard_credit | eep_credit_done | pc_machine |
| eep_guard_destroy | eep_destroy_done | pc_machine |
| eep_guard_secondary_core | eep_core | pc_machine，不改 eep_core0 绑定 |
| eep_guard_artificial | 原生 is_artificial=yes | 建殖民地前 change_pc=pc_habitat |
| eep_guard_qzero | q=0 | pc_machine、size2、清 deposits 后添加两份 d_lithoid_devastation |

artificial 的其它类型条件也可能失败，因此该案只证明真实人工目标整体被拒绝；若需证明仅由 is_artificial 条件导致，必须额外逐项观测其它谓词，不能据复合 trigger 的总结果反推单个条件。secondary_core 是第二颗真实带 EEP 物理核心标记的功能夹具，验证“所有核心都排除”，没有伪造第二套国家账本或解绑真实核心。

## 最少原生命令片段

以下是 active 案的完整单条 effect。其余六案复制同一结构，只按上表替换全局 target、拒绝 flag、类型和 qzero 的额外设置。artificial/qzero 不添加表中其它拒绝 flag。每次命令之后保持暂停；完成七案前不派发回调。

```text
effect event_target:eep_core0 = { solar_system = { random_system_planet = { limit = { is_colony = no is_under_colonization = no is_star = no is_artificial = no NOT = { has_carrier_flag = eep_core } NOT = { has_carrier_flag = eep_guard_batch } } set_carrier_flag = eep_guard_batch set_carrier_flag = eep_active save_global_event_target_as = eep_guard_active change_pc = pc_machine clear_deposits = yes create_colony = { owner = event_target:eep_mothership0.owner species = event_target:eep_mothership0.owner_main_species } create_pop_group = { species = owner_main_species size = 100 } } } }
```

qzero 案的建殖民地前类型段替换为：

```text
change_pc = pc_machine
set_planet_size = 2
clear_deposits = yes
add_deposit = d_lithoid_devastation
add_deposit = d_lithoid_devastation
```

原版噬岩者消费效果实际连续两次 add 同一 devastation deposit，所以此处不是假设 deposits 只能有单一键。qzero 必须从实际 deposit 实体数量和实际尺寸复核，不能写 eep_q=0 代替：生产入口会重新计算 eep_q。若创建后 is_colony=no、人口没有实际出现、q 仍大于0，该案例是夹具失败，不发护栏 PASS。

建立后先原生推进一天，确认所有新殖民地与状态保持；在非月底保存 `guard-ready`。先不回调再推进一天保存 `guard-idle-day1`，随后实际重载 guard-ready。此同日对照可以区分正常人口增长、组装、AI和新殖民地事件与回调收益；不直接把一天内所有人口变化填0。

实际重载 guard-ready 后，一条命令派发全部七案：

```text
effect event_target:eep_core0 = { solar_system = { every_system_planet = { limit = { has_carrier_flag = eep_guard_batch } log = "EEP_GUARD_BATCH_DISPATCH" fire_on_action = { on_action = on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER scopes = { from = event_target:eep_mothership0 } } } } }
```

log 是 effects.log:3902 的原生调试 effect。使用常量字符串按七条计数，并用 SAV 的七个全局 target 确认对象，避免把名称格式当作验收依赖。日志须保留实际执行范围；没有七条派发、出现缺 callback/Wrong scope，或脚本不执行时均为夹具失败。

保持七案条件，原生推进一天再保存 `guard-fired-day1`。只在两个 day1 档间比较同日人口与一般模拟字段，在 guard-ready→fired 中核对每案拒绝状态、殖民身份和持久账本；任何非目标差异保留原始值，不能静默过滤。若原生事件队列中仍有待执行 eep.50，继续保存至队列清空，状态仍不能移除。完成后实际重载未经夹具污染的原始 base。

## 每案最少检查表

1. 七个全局 target 均存在且物理 planet ID 互异；都不是实际 eep_core0，真实核心仍归country0且母舰仍唯一。
2. 每颗实际 owner=country0、is_colony=yes、pop_group 合计大于0；来源为 Mother 主种，非种族肃清造成的空殖民地。
3. active/devouring/credit/destroy/secondary_core 对应 flag 真实存在；artificial 的原生 planet_class=pc_habitat；qzero 尺寸2、d_lithoid_devastation 实体计数2。各项必须在 ready 和 fired 存档都保持。
4. 实际 on_action 名称及 scopes.from 已由原始输入记录，game.log 七次 dispatch，error.log 没有新增缺回调、非法 effect 或作用域错误。日志不能单独代替状态证据。
5. C/G/D/made/worlds、last_return/last_manufactured、六核心等级及 R/B/P、原生 worlds/empires objective.progress 均无结算新增；除人工预设 credit/destroy 案外，没有新增结算 receipts、没有 pc_shattered、没有目标人口被搬走/销毁。
6. 母星人口、容量与舰船配置对同日 idle 对照无结算变化；若自然模拟存在其它差异，逐项解释，不把无出处的补偿数填入预期。该夹具不检验全经济。

其它 guard（未殖民、友好中立、普通 fleet、真实 colonization/ground combat、核心归属失效）另用独立已有对象/分支，不能因本批七案通过就宣告全部覆盖。

## 真实核心转手：备份殖民地与绑定审查

先实际重载未造七案的 base，在一颗独立自然空星用前述 create_colony + create_pop_group100 建立普通 country0 备份，不加任何 EEP 拒绝标记，保存 `eep_guard_backup` 全局目标。推进一天并保存，必须从 SAV 确认 country0 至少有真实核心和备份两颗殖民地，备份有人口、当前非肃清/毁灭状态；之后才能转手真实核心。只创建 owner 但没有人口不构成保命备份。

保持 eep_initialized；不要移除此标记，不调用 eep_migrate_core 或迁移决议，也不手工改 eep_core0。已绑定真实敌星仍有 owner 时，可把其原星主保存为接收国，然后真实 set_owner 核心：

```text
effect event_target:eep_colossus_probe_target = { owner = { save_global_event_target_as = eep_guard_receiver } }
effect event_target:eep_core0 = { set_owner = event_target:eep_guard_receiver }
```

effects.log:45 的 set_owner 支持 planet/colony，原版 on_colony_transfer（00_on_actions.txt:3369）说明会进入新/旧 owner 的转手处理。转手会产生原版修正清理、人口权利/首都等副作用，均属于该独立功能分支；保留原始状态。接收国须真实存在，不能用已被上一轮发射消灭的 country1。使用仍存活的目标原星主，必须先重载到发射前 base。

本包源码查明：

- eep_on_actions.txt 只把 on_colony_transfer 接到 eep.3；eep_events.txt:13 的 eep.3 只在 eep_core 标记上执行 eep_sync_court，没有重新保存 core 全局目标。
- eep_effects.txt:2 的 eep_initialize 只有 NOT eep_initialized 才从资本绑定 core。已初始化国家换首都不会走初次绑定块。其后仅尝试修复原绑定核心的 deposit/宫廷。
- eep_migration_effects.txt:2 的 eep_migrate_core 才重绑新核心，唯一生产调用是玩家迁移决议（eep_decisions.txt:50），未发现自动转手调用。
- 月度 eep.2 会检测原核心缺失/不再殖民，或 eep_core_available=no 后标记 lost；它不把新首都改为新 core。
- eep_core_available 直接检查 eep_core@this 的 is_colony、is_owned_by=prev、未被占领和无地面战。核心物理对象仍存、owner改变时，这个判断已经失败，无需等月度 lost 通知。

因此，原生可能为country0选取备份为新首都，这是正常原生行为，不能误判成 EEP 重绑。SAV 必查 eep_core0 是否仍指旧物理星、旧核心 owner 是否为接收国、country0 备份是否仍殖民、eep_initialized 是否仍在，以及 Mother fleet owner 是否仍country0。若实际出现 EEP 重绑，先查是否误调用迁移或删了初始化标记，不据首都字段推定。

可以在真实发射 fire29/30 的独立分支转手并推进至边界，记录原生订单是否取消或进入完成；两者必须零结算。若引擎先取消订单，这仅证明原生中止，尚未覆盖 eep.50 完成 trigger。随后在核心仍转手、备份仍保命的状态，显式 FROM=Mother 对仍有效敌星派发一次专属完成回调，推进一天核对零结算，才补齐业务完成重验负例。整个分支只验中断/拒绝，不计作有效武器完成。

归档与报告必须区分：普通首都变化、原生订单取消、EEP core 全局绑定、业务回调拒绝。完成后重载原始 base，不在夹具里夺回核心或清旗后继续经济主线。

## 原生命令 JSON 夹具生成设计（先于实施）

主线程授权生成 `testing/colossus_1019_native_commands.json`，仅作为可审查、可复用的原生控制台文字资产，不自动执行、不修改生产包。顶层及每条命令均标记 PENDING，记录原生 EXE、基准 SAV、精确来源、前提与验收；所有 command 为 ASCII 单行 effect，命令中不使用 ROOT/PREV 隐式层级。

资产包含一条七独立目标合并 setup、一条有持续负例检查且 FROM 严格为 Mother 的合并 dispatch；真正 start_colony 的 setup/inspect/dispatch；敌国天然殖民地创建原生地战双方的 setup/inspect/dispatch；独立备份殖民地创建、原核心物理引用和接收国绑定、转手、检查、负例派发。辅助目标采用 eep_guard_ 前缀；不清除生产核心绑定、EEP初始化标记或任一拒绝条件。所有世界创建选择器加 eep_guard_reserved 后立即排除已用目标，防止不同片段误用同一物理对象。

殖民与地战的精确依据及构造边界沿用 [原生状态负例研究](colossus-native-state-negative-fixtures-1019.md)：start_colony 为 effects.log:1336、原版 origin.7320；create_army 为 :333，原版 colony.4 直接在殖民地生成敌方军队。当前 Machine actor 用 machine_assault_1，原版 `01_assault_armies.txt:785`；有机敌方守军用 defense_army。生成军队不等于已经 has_ground_combat，实际布尔、参战双方、持续状态必须另查，未成立不得调用负例或标通过。殖民中若同时 is_colony=no，报告联合拒绝，不声称隔离单条件。

实施静态验收：JSON可解析；全部命令ASCII且无CR/LF；大括号/引号平衡；七setup目标与七持续状态互异；所有完成调用使用同一专属回调与显式 scopes.from；不存在移除拒绝flag、写生产核心绑定、清初始化标记、直接调用结算或武器完成效果；每条命令前提/验收/来源齐全。可用既有 open_kaishek Stellaris解析器检查提取的 effect 文本，报告仅语法范围，不能自发实机PASS。主线程确认前不在当前run中执行。

### 控制台长度与分条优先路径（先于补充实施）

本机原版 `interface/console.gui:22–30` 的console_edit没有max_characters或max_text_length配置；其它GUI中出现的100/1000限制属于其它控件，不能套给控制台。没有可靠原生控制台长度上限证据。原4555字符合并setup保留，但标注长度尚未校准，不优先物理输入。

按主线程追加要求，资产增加一个显式Mother→actor/species绑定命令、七个分别小于1000 ASCII字符的独立setup。每条直接选择当前未殖民、非恒星、非人工、非核心且未reserved的物理对象，立即reserve并各存独立全局target，再建立带持续拒绝条件的殖民地；类型、人口、原核心绑定要求与合并版相同。优先按顺序分条输入，每条保存/核对新目标身份和对应状态，不把静态PARSED当作控制台已接收。分条路线与合并路线二选一，不在同一分支先后执行两套。

此次只读pk1base还确认actor已有tech_assault_armies，country1为auth_dictatorial而非Machine，符合地战片段使用machine_assault_1攻方及defense_army守方的前提；更换运行或接收国后仍需重新核查。

已生成22条全部PENDING的命令资产，文件SHA256 `7ec14b4fb1813e29441ce09063e4738fa5b10d3b9506745bbf563470014f0c79`。绑定命令780字符；分条active/devouring/credit/destroy/secondary_core/artificial/qzero分别691/704/696/700/713/718/790字符。合并setup4555、dispatch906字符。既有open_kaishek lossless parser以stdin batch解析22条、全部PARSED/diagnostics=[]/roundTrip=true；这些结果和工具JAR SHA存于JSON的static_validation，仅认证语法/ASCII/字段完整性。没有执行控制台、原生长度校准、建星或护栏实机，全部runtime_result仍为null。
