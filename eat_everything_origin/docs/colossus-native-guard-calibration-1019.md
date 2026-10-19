# 1019 原生巨像护栏、重复回调与危机归因校准

## 目标、范围与验收

在 RC3 的真实母舰原生巨像发射之前，明确只读检查所需的作用域，以及危机目标单次奖励的实际单位；用独立原生引擎分支排除最后殖民地重复灭国奖励。主线程独占桌面，本文作者只查源文件、SAV 和文档，不操作游戏、不修改 SAV、不修改生产 Mod。本文中的控制台配方是待执行方案，不能当作运行结果。

所有引擎操作由主线程在已经通过 open_kaishek 的不可变候选、简体中文隔离运行中执行。夹具可以通过明确的原生 effect 建立控制条件，必须保存原始动作、截图、日志、SAV、receipt/audit 及 SHA；这种调用仅验证护栏或奖励归因，不证明武器充能发射。真正的武器验收始终来自母舰右键命令、90 日充能、30 日发射和自然完成。

验收标准：排队、取消、无效目标和完成后重复回调均不改变 EEP 收益或两项原生危机目标；真实完成只产生一次 q 对应结算、一份毁星奖励，最后敌国殖民地额外恰一份灭国奖励。归因探针必须核实源殖民地与原星主确实消失，不能把“销毁未发生所以无奖励”作为通过。未实际执行的项目保留 PENDING。

## 本次精确来源

原版目录为 `C:/SteamLibrary/steamapps/common/Stellaris`。本轮 EXE SHA256 为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，自动生成文档来自 `C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261019T092935Z/logs/script_documentation`。

| 本机原始文件 | SHA256 |
| --- | --- |
| events/nemesis_crisis_menace_objective_events.txt | f38d1c9291767ea4b1845214198fd2d84686db9e3a89d3e49180d6a6d2f2b261 |
| events/planet_destruction_events.txt | b0e7521d7ef7cc925e033c12c7fdb8e6d1c09aa624be1d45c8cad998e3c13e87 |
| common/on_actions/01_planet_destruction.txt | 6ba54afe8c56225641311aa64f3daa358097a0adbbdaad0328eb5d260822325c |
| common/on_actions/00_on_actions.txt | 7693e64fbe974f37db0c68969d10f7bdeec585ce59ca497b5e27ecd69ff8f306 |
| common/scripted_effects/nomads_effects.txt | b42b9f72f341e1e1a6bb624cf5d438677893c1e47bc0f4040844f15ac5e7ba96 |

- `effects.log:2317`：`fire_on_action = { on_action = <string> scopes = { from = X fromfrom = Y } }`，所有 scope 可用。
- `effects.log:3227`：`carrier_event` 支持 planet/ship/colony，允许 `scopes = { from = fromfrom }` 覆盖；普通 console 的 ROOT 或当前选择不能代替 FROM。
- `effects.log:432`：`destroy_colony = yes` 支持 planet/ship/colony，没有公开的 destroyer 参数。
- `triggers.log`：`valid_planet_killer_target = <planet>` 是 fleet trigger；不能在 planet scope 直接使用这个引擎触发器。
- `common/scripted_effects/nomads_effects.txt:4724`：原版 Carrier 内实际使用 `fire_on_action = { on_action = on_destroy_planet_with_arkship_reprocess_planet scopes = { from = from } }`。同文件 :4735、:4808 也显式转发 FROM。不是从 CK3 类比的语法。
- `common/scripted_effects/00_scripted_effects.txt:4627`：原版 `destroy_star_system` 通过 `scopes = { from = event_target:crisis_country }` 将事件目标交给原生回调。
- `common/on_actions/01_planet_destruction.txt:1`：原生完成回调 THIS/ROOT 是目标 planet、FROM 是发射 fleet；:10 声明 queued 和 unqueued 使用相同 scope。

RC3 初始 `fmm00.sav`（2200.01.01，SHA256 `18cae5e75b189ee8739cdadd3fc63d5c2929fad7a1d892e5382d0750d36c33d9`）只读观察：country0 母舰是全局目标 `eep_mothership0`，fleet159；母星是 `eep_core0`，物理 planet2；country1 的首都 colony1 对应物理 planet17，pc_alpine、size19、无原生吞噬损耗。不能沿用上一轮 fleet138/planet15。之后主线推进或建立夹具时必须从当时 SAV 重新确认 ID、战争和唯一最后殖民地。

## crisis.4020 的全部逻辑及重复风险边界

`events/nemesis_crisis_menace_objective_events.txt:12–33` 中，crisis.4020 是隐藏、仅触发的 country_event。它的全部 trigger 为：被毁国家类型是 default、fallen_empire 或 awakened_fallen_empire；存在 FROM；FROM 拥有 ap_become_the_crisis。immediate 仅令 FROM 执行一次 `complete_crisis_objective = crisobj_destroy_empires`。该事件没有 once flag、5015 排除条件、巨像武器分支或 EEP 检查。

`common/on_actions/00_on_actions.txt:3601` 定义 `on_country_destroyed`：THIS 为被毁国家、FROM 为可选的灭国者 country，事件表包含 crisis.4020（:3613）。这证明存在第二入口；它不证明 `destroy_colony` 会将外层 FROM fleet 的 owner 填入新的国家毁灭回调。

`common/on_actions/01_planet_destruction.txt:14` 中 CRACKER 的次序明确是 crisis.5015 在前、planet_destruction.100 在后；原注释说明后者可能杀死国家，破坏后续判断。SHIELDER 和 TOXIFIER 也先调用 5015。crisis.5015（同一 crisis 事件文件 :155–187）只要求 FROM.owner 有危机 AP、目标仍为殖民地；先发毁星奖励，若原星主无其它殖民地，再发灭国奖励。没有调用 4020 或写去重标记。

planet_destruction.100（`events/planet_destruction_events.txt:21`）在 :282 的 every_owned_pop_group 中 kill_all_pop，然后处理 orbital_defence/buildings 和 change_pc；它没有显式 destroy_country 或 destroy_colony。相对地 NEUTRON 的 on_action 不调用 5015（`01_planet_destruction.txt:60`），planet_destruction.300 在 :979 直接 destroy_colony，并另外发人口净化奖励。当前 EEP 结算使用显式 destroy_colony，再 change_pc，与 CRACKER 的具体销毁序列不同。

因此，不能仅凭原版先 5015 后 .100 就证明 EEP 的 destroy_colony 不会额外归因，也不能仅凭存在 4020 就断言已经 double。原版和自动生成文档没有公开 C++ 对可选 destroyer 的赋值规则。当前 `eep_crisis_done` 只能防 EEP 手工块重入。若需要立即判断，采用下面独立引擎分支；在结论出来前不擅自删除手工奖励或覆盖全局 4020。

## 单次危机奖励校准：最少两份 SAV

在暂停、已具备危机 AP 的真实候选分支，保存 `crisis-cal-before`。记录 country0.crisis_progression 的 path、level 和全部重复 objective 块；缺目标项仅在已确认 native Nemesis 路径时解释为零，保留原始体。

执行一条显式国别命令，不依赖当前选择：

```text
effect event_target:eep_mothership0 = { owner = { complete_crisis_objective = crisobj_destroy_worlds complete_crisis_objective = crisobj_destroy_empires } }
```

仍暂停且同日保存 `crisis-cal-after`。两个不同 objective 的 progress 各自差值，分别是当时条件下毁星、灭国的一份原生奖励。这只需 before/after 两份 SAV；执行失败、目标块异常或其它 EEP 收益变化时校准 FAIL。读取 objective 内的 `objective="crisobj_destroy_worlds" progress=...` 和对应 empires，不能用总 menace、country.eep_worlds 或 eep_crisis_done 替代。

`common/crisis_objectives/00_crisis_objectives.txt:30` 的灭国 reward 以700为基数，每个可玩国家减25、round_to50、至少100；:73 的毁星 reward 受星系数、宜居倍率影响。progress 表示累计奖励点，不是完成次数。灭国之后可玩国家数量变化，潜在第二份奖励未必和第一份数值相同，不能只查是否恰好两倍。

校准后实际重载未经校准污染的 before；另存重新加载证据并检查两项目标与 EEP 账本恢复，再继续真实发射主线。原校准档不覆盖。

## 尽早定位归因的两个原生分支

前提是主线程已在原生引擎建立真实战争、绑定 `eep_colossus_probe_target` 为普通敌国唯一殖民地的物理 planet，并保存独立 base。所有分支从同一 base 原生重载，不能串联。以下命令会真实销毁殖民地，仅用于明确标记的独立归因夹具；不把这些分支计作武器成功。若主线程不执行，保持 PENDING。

1. **原版 CRACKER 对照**：

   ```text
   effect event_target:eep_colossus_probe_target = { fire_on_action = { on_action = on_destroy_planet_with_PLANET_KILLER_CRACKER scopes = { from = event_target:eep_mothership0 } } }
   ```

   保存 after，核实 country1/目标殖民地毁灭，worlds/empires 分别与校准的一份奖励比较。该分支运行原版的 5015 → .100，而不是 EEP。若原版本身也产生超过一份灭国奖励，应记录原始事实，不能据“原版一定不会”倒推通过。

2. **原版 NEUTRON 的显式 destroy_colony 对照**：

   ```text
   effect event_target:eep_colossus_probe_target = { fire_on_action = { on_action = on_destroy_planet_with_PLANET_KILLER_NEUTRON scopes = { from = event_target:eep_mothership0 } } }
   ```

   保存 after，核实原星主确实被消灭。该 on_action 没有手工灭国奖励，若 empires 增长，说明这一原生 Carrier 事件的 destroy_colony 路径存在额外归因；若不增长，只能在确实销毁国家的前提下支持“脚本 destroy_colony 不提供合格灭国者”。purge_pops 的增长属于原版 .300，不能混作灭国奖励，也不能把总 menace 差作为判断。

如果国家销毁延后到下一 tick，额外留同日刚执行档与一天后档；核实没有其它灭国或战斗目标来源。两分支完成仍需恢复 base。最终 EEP 真实完整发射必须单独核对 empires 增量，才能排除 EEP 自身调用上下文差异。

## 正确 FROM 的护栏和重复回调

对已毁目标或人为建立的独立无效目标，可用原生回调评估生产事件的真实 trigger：

```text
effect event_target:eep_colossus_probe_target = { fire_on_action = { on_action = on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER scopes = { from = event_target:eep_mothership0 } } }
```

该写法先以目标物理 planet 为 THIS/ROOT，再用已绑定母舰 fleet 作为 FROM。生产 eep.50 的 Carrier trigger 直接执行 eep_colossus_target_valid；触发器失败就不进入 immediate。这是负例/重复回调夹具，绝不能在未加护栏的有效敌星上调用，因为成功执行会直接结算，不能冒充原生发射完成。

最小经济负例顺序：真实完成后原星球回调一次、再次回调一次、同日重载后回调一次；每次独立 SAV，比较源星 destroyed/credit/population/crisis 等 receipts，C/G/D/made/worlds、六核等级与奖励计数、母星人口/容量、两个原生 objective 和实际星球类型。已毁星的 colony 可能不存在，所以保留物理 planet 全局目标，不从旧 colony ID 找星。

需要隔离每个 guard 时，从真实有效且尚未结算的 base 分支恢复，再只改变一项条件并调用上述负例：源星分别设 eep_core、eep_active、being_devoured、eep_credit_done、eep_destroy_done；发射国设 eep_core_dead；FROM 换为已确认不属于母舰的普通 fleet；战争前友好目标、未殖民星、人工星使用真实已有对象。q=0 须让原生损耗 deposit 数达到实际尺寸，不能只写 eep_q，因为入口会重新计算。under_colonization/ground_combat/核心转手使用实际原生对象状态或清楚标记的夹具，不凭给标记冒充真实地面战。每案保存处理前后，源/收益不变才通过；若错误进入结算，按 guard FAIL 记录并恢复 base。

原生 `valid_planet_killer_target` 可在母舰 fleet 的 effect/if/limit 中只读求值并 log，但它还包含引擎类别、组件、外交等条件，不能将其结果单独当作指定 EEP guard 的布尔输出。未确认控制台 trigger 命令或直接改 FROM 的 effect，不编造语法；已有 fire_on_action 和 carrier_event scope 覆盖已经足够进行上述真实负例。

## 最短真实武器矩阵

| 阶段 | 必须保留的实际证据 | 收益预期 |
| --- | --- | --- |
| 受控战争 base | 真实双方、有效敌星、唯一母舰、实际组件、初始账本 | 无新增 |
| 真实右键下令 | current_order.destroy_planet_order 指向物理目标 | 无新增 |
| 充能与取消 | windup/90 原生字段、实际取消动作、同日取消后 SAV | 全部收益/危机目标不变 |
| 真实重下令 | 新订单、windup89/90、fire1/30 | 无新增 |
| 完成临界 | fire29/30 及下一日自然完成，避开月结或保留独立人口增长对照 | 一份结算 |
| 完成后重复/重载 | 上节 FROM 正确的回调负例、实际重载 | 无新增 |

若实际源 q19、Machine 普通材料、初始 C/G/made/worlds 为0且D2，则结算期望 C19/G19/D6、made300、worlds1、last_return0；L1，尚未达到每5级组件奖励。母星净人口应扣除实际增长/组装/迁入等独立变化。不能把未经观察的增长量直接填0。这个单例不覆盖噬岩者随机 bites、本国普通 situation 拆解、所有无效目标或母星丢失分支。

## 当前状态

源码和接口调查完成；本文件全部新增运行夹具仍为 PENDING，未修改生产 Mod，未执行桌面动作或编辑 SAV。真实完成/取消、归因校准和静态工具结果由主线程及只读检查器分别记录，不将本方案表述为已通过实机。
