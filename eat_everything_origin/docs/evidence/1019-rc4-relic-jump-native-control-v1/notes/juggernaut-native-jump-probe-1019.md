# 1019 原生主宰跃迁与最高推进器只读核验

## 目标、范围与验收（调查前）

核查当前 `NAME_EEP_Baiqi_Mothership_1019` 的 ship_size=juggernaut、
JUMP_DRIVE_1 与 COLOSSUS_SHIP_THRUSTER_5 是否符合本机 Stellaris 4.5.2 的
原版适配／限制，并提出最短“实际跃迁指令 → 原生 FTL 状态 → 到达”验证路径。
只读游戏原版、生成接口文档、已存在 SAV 或归档观察；不启动或操作 UI，不改
生产 Mod、当前 run 或外部工具，不提交。本仓库由主线程统一提交。

每项确定结论记录原始文件、行号与 SHA；区分脚本适配条件、UI／闭源实现的未知
限制与实际运行证据。不得仅凭组件名、图标、已有坐标跳变或控制台 set_location
便宣称真正 jump。候选目标必须来自真实星系和可核实距离；不猜测控制台命令、
FTL effect、SAV 字段含义或隐藏状态值。若原生 UI 操作仍是必要步骤，明确交由
主线程独占桌面执行。

主线程追加范围：在 PK 功能分支完成后，用原生 API 生成同国同日 NAME_Relic
参照船，只生成独立夹具，不混入新局经济；给出定位与完整配置／三防／伤害／维护
比较方法。不新建 candidate，不为此扩展工具或建立大归档。

## 已确认的舰型和组件适配

当前生产全局设计文件 `mod/common/global_ship_designs/eep_mothership.txt:4,194-199`
为 juggernaut，实际引用 `JUMP_DRIVE_1` 与 `COLOSSUS_SHIP_THRUSTER_5`。
文件 SHA256 为 `0e1bc46c7d1d534e0a9d3619cef1d93e366ddc7d5a4d2fde766b0ca111929123`。
这是普通跃迁引擎；原生 PSI_JUMP_DRIVE_1 是其升级，另有 +50% 跃迁范围。

原版 `18_juggernauts.txt:52,58-59` 把主宰分类为 `shipclass_starbase`，要求 ftl_components
和 thruster_components。`07_scripted_triggers_ships.txt:982-992` 的
ship_uses_jump_drives **明确包含 shipclass_starbase**；801-813 的
ship_uses_colossus_thrusters **明确包含 juggernaut**。因此不能因为它是移动星基
就从静态配置断言“不许跃迁”。这些原版脚本没有提供已完成跃迁的运行证据。

`00_utilities_drives.txt:218-259` 的 JUMP_DRIVE_1：ftl=yes、jumpdrive=yes、
potential 要求 ship_uses_jump_drives 与非生物船类别（或 arkship）；prerequisite
为 tech_jump_drive_1。研究前置是组件可选条件，不能由此倒推特殊事件设计现装组件
必然无效；应核原生 SAV 里的实际 required 列表和原生动作提示。主宰单船舰队避免
混入未装备跃迁引擎的其它船，原生中文提示明确要求舰队每船都装备。

`00_utilities_thrusters.txt:833,859,1069-1109` 的 COLOSSUS 家族由第 4 级升级到
第 5 级；本机文件无该家族第 6 级。第 5 级 ship_base_speed_mult=1.25，power
引用同文件 43 行 -600，适配触发器包括主宰，故这是当前原生主宰适配家族最高级。
这证明适配和源参数，不能直接证明最终速度、加速、转向或跟队能力。

## 原生跃迁操作的已知限制与未知部分

- `common/game_rules/00_rules.txt:1685-1689` 的 Fleet 规则 can_jump_drive 只要求
  is_system_locked=no，并注明冷却由代码处理；没有 juggernaut 类别排除。
- 同文件 1717 起的 can_enter_system_by_jump 调用
  `07_scripted_triggers_ships.txt:8-30`：封闭星系需国家已有 entered_sealed_system，
  L-Cluster、formless_system、hyperthermia_system 不可作为普通跃迁目标。
- `common/defines/00_defines.txt:741,1808-1809` 给出基础冷却 200 天、基础预热
  14 天、基础范围 100；具体有效冷却／预热／范围还会受组件、国家、舰船与状态
  影响，不能只套静态乘法宣称实际耗时。当前生产文件未发现专属跃迁范围／冷却
  修正或 disable_jump_drive_cooldown_malus 设置。
- 原生 `main_1_l_simp_chinese.yml:1463,4183,4320-4324` 提供“启动跃迁”、
  点击后选恒星系、范围外、舰队组件缺失、冷却中的具体提示。普通右键移动会走
  超空间航道，不能替代该明确动作。本次没有从 GUI 源或既有实机证据确认快捷键，
  不提供猜测的 J 键或无来源的 `jump_to` 控制台命令。
- 未取得闭源 UI／可用性判断的反汇编或实机结果。作战、受命执行其它动作、未知
  目标可见性或其它代码限制都应通过**实际按钮悬停拒绝原因**确认，不能从上述
  脚本未禁止便写成“实际一定可跳”。

## 最短真实 jump 探针（交主线程，尚未执行）

1. 从 PK 已完成后的独立功能分支暂停保存 before。定位全局 target
   `eep_mothership0`，核其唯一实际船、country0、当前星系、实际设计中
   JUMP_DRIVE_1；记录母舰队列。确认没有仍在执行的 planet_killer fire／windup，
   不对仍在验证中的 PK 分支发移动命令。
2. 选中唯一母舰，进入银河图，悬停原生“启动跃迁”，保存完整中文提示。只有按钮
   可用才点击该动作，再点范围圈内的真实目标星系；保留动作与目标提示。若禁用，
   保存原因即停止，不用 set_location、伤害／冷却变量写入或传送命令绕过限制。
3. 下令后仍暂停保存 queued；按实际界面的预热倒计时逐日推进，至少取得一份
   windup 中 SAV，再保存到达后 SAV。记录日期、同一船／舰队 ID、出发和目标
   系统、舰队 order、movement_manager 完整原文、所有新增 jump／ftl／cooldown
   字段以及三防和队列。若产生短暂 in_ftl／其它状态，原样记录实际字段与数值；
   若未捕到，明确“未捕到”，不得凭空补 `in_ftl=yes`。
4. 到达后实际坐标 origin 应为所点目标，母舰身份与队列保持，跃迁按钮出现真实
   冷却提示。原生 `triggers.log:44-46` 明确支持 Fleet／Ship 的
   `has_fleet_order = jumpdrive_order`、`has_fleet_order = jumpdrive_windup`。
   如需辅助日志，可在暂停时使用下述只查询 order 的 effect；它不下跃迁指令：

```text
effect event_target:eep_mothership0 = { if = { limit = { has_fleet_order = jumpdrive_windup } log = "EEP_JUMP_NATIVE_WINDUP_TRUE" } if = { limit = { has_fleet_order = jumpdrive_order } log = "EEP_JUMP_NATIVE_ORDER_TRUE" } }
```

原生 `00_on_actions.txt:4151-4153` 存在 ship scope 的 on_jump_drive，但本探针不为
此增加生产回调或夹具 Mod。有效证据应由原生 UI 明确 jump 指令、真实预热 order、
同一母舰到达和实际冷却共同形成；不能把普通超空间 FTL 当作跃迁通过。

已有只读基线 `20261019T112808Z/pk2base.sav`（SHA
`be5a344439dafe105d4959b4afa31143331b1daaaf915dba28bc70ee23f6f2e2`）中，母舰
fleet159／ship997 位于 system8，movement.state=move_idle；其
last_ftl_jump.to=13、jump_method=jump_count 是已有记录，且当前实际位置仍为 8。
**这条记录不是成功跃迁证据**。该 SAV 没有 in_ftl 字段，不能预设下一次成功跃迁
一定用此名字或预设 jump_method 枚举。

这个特定银河中，system8 坐标 (-18.83,-122.13)，直接超空间邻居为 33、43、96。
system196 的 NAME_Vapob（原生中文“瓦珀博”，paragon_2_l_simp_chinese.yml:1570）
坐标 (5.23353,-121.0006)，欧氏距离约 24.0900，**不是直接超空间邻居**；没有
上述禁跳星系旗标，是适合在当前银河原生 UI 中核对的近距离目标候选。该候选仍需
实际可见、范围与按钮确认；若母舰已换星系，从新 before 重新算距离和邻接，
不照搬 ID。距离取 galactic_object 的银河坐标，不使用船在星系内的 x/y。

## 原生银河目标搜索与返回母舰（只读补充）

本节只补原生 GUI 已声明的快捷键与按钮路径；没有执行搜索、点击或跃迁。

搜索的精确快捷键是 **F**：`interface/main_bottom.gui:425-435` 的
button `toggle_gotobox` 明确 `shortCut="f"`，438-439 的配套图标为
GFX_search_icon，位置在原生右下工具栏。没有 Ctrl 修饰键，不使用凭记忆的
Ctrl+F。`interface/gotobox.gui:67-91` 明确有名为 edit 的输入框与 list 结果列表，
104-114 的 gotobox_entry/button 是结果行按钮；98 行为关闭窗口的 Escape。
`main_2_l_simp_chinese.yml:3574-3575` 明确该窗为“搜索”“搜索已知恒星系”。

最短操作方案：

1. 保持暂停；若当前处于星系内视图，点击底部打开银河图按钮：
   `main_bottom.gui:96-105` 的 leave_system_window/button 使用
   GFX_open_galaxy_map。该按钮本段 GUI 没有显式快捷键，因此这里使用按钮，
   不猜 E／M。银河视图中的反向按钮在 239-249，名为 change_camera_mode_button，
   使用 GFX_open_system_map。
2. 按 F，点击搜索输入框 edit，输入 **瓦珀博**，点击实际出现的同名结果行。
   该中文名来自原生 paragon_2_l_simp_chinese.yml:1570 的 NAME_Vapob；本次银河
   SAV 的 system196 正是该 name key。输入框没有 GUI 级 ASCII 限制，因此中文
   是合理输入，但过滤算法和是否已知由闭源代码决定，本调查不能声称结果已经
   出现。若无结果，记录无结果，不改语言、伪造可见性或把 numeric 196 当作已
   支持的 ID 搜索模式。结果行 GUI 也没有声明 Enter 快捷键，故使用可见结果按钮。
3. 核对定位到的实际中文星系名；若当前既有 debug tooltip 能显示 ID，则再核
   system196。关闭仍打开的搜索窗（Escape），释放输入焦点，才继续舰队热键。
4. 需要返回母舰时，在概览／已有舰队列表重新选中 **白绮的裁决**（生产简中
   eep_l_simp_chinese.yml:88 的 NAME_EEP_Baiqi_Mothership），核对确是 Mother
   而非新 Relic，再按 **Q**。`fleet_view.gui:517-522` 的 focus_on 明确
   `shortCut="q"`；移动星基面板对应 1873-1879 也声明 Q。中文
   main_2_l_simp_chinese.yml:1497 的 FOCUS_ON_FLEET 明确是“前往”，把视角切至
   该舰队位置。Q 不改变舰队位置，不是移动／跃迁命令；搜索框焦点未释放时，
   不把输入 q 误当作舰队定位。
5. Q 后若需要银河图，再用上述 GFX_open_galaxy_map 按钮。发真正 jump 时必须
   重新确认 Mother 仍被选中，然后执行“启动跃迁”并点已核对的目标星系；不能
   将搜索定位、Q 镜头移动或普通右键移动写成实际跃迁。

搜索结果会否保留之前的舰队选择、Q 会否同时切换局部／银河视图，均没有在上述
GUI 声明动作实现；方案要求操作后检查实际面板，不替代码猜测。这组路径仅是
主线程待执行的原生 UI 方案，不是实机校准结果。

## 同国同日原生 Relic 参照命令

实际夹具分析任务（实施前追加）：主线程从已恢复的 RC4 pk2base（C0／2200.03.07）
执行下述完整原生命令，计划保存 r4relic0。待 r4relic0.native-save.json 与对应 SAV、
audit、manifest 就绪后，本子任务只读验证 eep_relic_reference_1019 绑定唯一新舰队／
船且 owner0；与 pk2base 比较只能新增该一舰一船，逐项核对 Mother50／Relic43 槽和
6 required 映射，记录同日 C0 实际三防、原生 modifier／auras。输出新的独立分析报告
并绑定源 SAV、receipt、audit、manifest、工具 SHA，不改原证据或原报告。SAV 未存
DPS／最终维护金额时明确未覆盖；只报告实际名字供主线程打开界面，不代替 UI 结果。

原版 `common/global_ship_designs/leviathans_designs.txt:1663-1850` 有全局设计
NAME_Relic，舰型 npc_warship_01，一段 automated_dreadnought_key，**43 个组件槽
与 6 个 required**。当前 Mother 为 50 个槽与 6 个 required，新增槽不能掩盖原版
43 个槽的缺失，比较时逐槽映射，而非只比总数。

原生 effects.log:316-318、351-379 明确 create_fleet 可在 all scope 创建，
effect 中为 fleet，create_ship 支持 fleet／starbase、design 为 ship design key；
set_owner 接收 country target，set_location 支持 fleet。原版
leviathans_events_2.txt:4420-4467 真实用 create_fleet → set_owner → create_ship →
set_location 构造可归玩家的无畏舰。caravaneer_scripted_effects.txt:81-96 还明确
使用 `event_target:<fleet>.solar_system.star` 定位链；scopes.log:26、86、334
分别确认 star、owner、solar_system 的输入输出。

因此给主线程的命令为（只在独立功能夹具执行一次，前提 global target 已验证）：

```text
effect create_fleet = { name = "EEP_Native_Relic_1019" effect = { set_owner = event_target:eep_mothership0.owner create_ship = { name = "NAME_Relic" design = "NAME_Relic" graphical_culture = "npf_01" } set_location = { target = event_target:eep_mothership0.solar_system.star distance = 30 angle = 0 } save_global_event_target_as = eep_relic_reference_1019 } }
```

命令使用明确的原生接口，不依赖 `add_ship NAME_Relic` 参数猜测；本调查没有执行
该命令。`eep_relic_reference_1019` 会直接绑定实际新 fleet，再从其唯一 ships 成员
找到真实新 ship；与 before 的 country0 owned_fleets／ship IDs 求差，要求恰新增
该一舰一船，不能只按 UI 舰名或设计序号猜实体。它在母舰所在系统生成并归同一
国家，graphical_culture 与原生无畏舰事件相同。保留同日原生 SAV，不能把免费
生成参照当自然建造支付或新局赠品。

同一 SAV 至少比较每个 section 的 template／slot、每个 component 的 slot／template
与 required 列表；native current/max hull／armor／shield、实际 fleet/ship modifier、
auras 和 country 修正。Relic 的 required 为 BATTLESHIP_DARK_MATTER_REACTOR、
SENSOR_4、JUMP_DRIVE_1、COMBAT_COMPUTER_LINE_SAPIENT、SHIP_THRUSTER_5、
SHIP_AURA_INSPIRING_PRESENCE；Mother 仅反应堆／推进器适配到主宰家族，其余可逐项比。

`11_leviathans.txt:473-510` 的 npc_warship_01 本身带 ship_weapon_damage=2、
ships_upkeep_mult=-1、ship_shield_mult=3、ship_armor_add=5000 等；Mother 的专属
fleet 修正在生产 eep_modifiers.txt:8-24，包含 damage=3.8、fire_rate=.8 与维护修正。
所以武器 CSV 或军事力量不能替代实际 DPS，维护修正 -1 也不能替代原生实际费用。
需要时在这个已污染的独立夹具里，使用已文档化的
`export_modifier_to_variable = { modifier = ship_weapon_damage variable = eep_reference_damage }`
（effects.log:549-551，支持 ship／fleet）导出实际修正；同法可分别导出 fire_rate、
upkeep multiplier。导出的是修正值，不是每击伤害或最终每月能量／合金金额。

最终原生伤害／DPS 和逐船维护优先由同日中文舰船界面取值，再与该 SAV 绑定。
若仅采一份 SAV 而没有对应可复核字段／UI，明确伤害或维护数值未覆盖，不能拿
military_power 或静态组件和当成实际值。生成 Relic 还可能改变本国已用海容和超容
维护；记录 before／after 的 used/max capacity，在同一 post-spawn 国家环境比较
两船，不把该分支预算用于自然新局经济结论。此参照也不等于野生守护者难度修正下
的战斗基准，不要求给参照额外发任何 EEP 修正。

## r4relic0 同日实际存档结果

已只读完成 [独立原生参照报告](evidence/1019-analysis/rc4-relic-reference-v1.json)，
复现入口为 [只读分析脚本](evidence/1019-analysis/rc4-relic-reference-v1.py)。17 项
检查全部满足，范围只限同日实体、实际设计与存档三防，不是最终 UI DPS／维护通过。
源 before 为 pk2base（上述 be5a3444…）；after r4relic0 原生 SHA256 为
`d29d0956d181198e87254e9c1c9d280f9f470576d479057c8621076a1a055201`，
对应原始 native-save receipt、audit、run manifest 与分析工具／源文件 SHA 均在报告。
两档都是 2200.03.07、C0、同一 RC4 tree06485dc5…。

全球实体与 country0 实际 owned_fleets 清单均只新增 fleet16777221／ship16777223，
没有删除，所有旧本国舰队成员保持。global target eep_relic_reference_1019 恰绑定
该新 fleet，唯一新 ship 归其所有；原母舰仍为 fleet159／ship997。
Mother 名称原生 key 对应“白绮的裁决”；参照 fleet 为 EEP_Native_Relic_1019，
ship 原生名块 PREFIX_NAME_FORMAT(NAME=NAME_Relic,PREFIX=EEP)，按中文原文格式
组合为“EEP遗迹”。这是名块与本地化重建，报告保留 ui_verified=false。

| 实际 Mar7 C0 字段 | Mother 997 | Relic 16777223 |
| --- | ---: | ---: |
| 当前／最大 hull | 93960 / 93960 | 20000 / 20000 |
| 当前／最大 armor | 44787.6 / 44787.6 | 30740 / 30740 |
| 当前／最大 shield | 167310 / 167310 | 138352.5 / 138352.5 |
| 组件槽／required 数 | 50 / 6 | 43 / 6 |

两船实际 design 均逐项匹配各自冻结 Mod／原版源；Relic 的全部 43 个 slot/template
在 Mother 中逐槽相同，Mother 额外为六个自适应核心 AUX6–11 与一个巨像武器。
required 四项共有：SENSOR_4、JUMP_DRIVE_1、COMBAT_COMPUTER_LINE_SAPIENT、
SHIP_AURA_INSPIRING_PRESENCE；仅反应堆与推进器按各自舰型不同。实际存储的
Mother timed fleet modifier 有 eep_mothership，Relic 无此专属修正。just-spawn
Relic 的 aura_modifier 缓存为空，Mother 存有 +.05 fire_rate／-.75 logistics；
两船都没有可直接当最终 DPS／维护金额的 native scalar。本报告不由这些差异推算
最终面板，也不从 military_power 推断 DPS。

普通 raw 比较没有隐藏：旧 fleet raw 全部相同；16 个旧 ship raw 改变。进一步
[独立 raw 差异报告](evidence/1019-analysis/rc4-relic-reference-raw-delta-v1.json)
确认全部仅 ship_design_implementation.design 的 ID 改变，所引用的**完整 design
body 字节相同**，实现其它字段与其它 ship 原生字段也逐项 raw 相同。例如 Mother
997 从 design1495 变为1511，但 body SHA前后均为
`be9562535dd559dbc4c74de4b8687d2075bbdd1b41b897e6b771ac98627129d9`。
该补充明确 strict_existing_ship_raw_equal=false，不把专项核对替换为 raw 全等通过，
也不猜测引擎具体重编索引原因。国家库存与 native 直接字段相同，used_naval_capacity
仍缓存为115；不能声称新 Relic 已刷新计容或没有实际维护。

## 六天刷新后原生面板对照方案（实施前追加）

主线程确认实际 Mother hover 为原生“启动跃迁”，提示基础200天冷却和伤害／速度
-50%惩罚；另一个 Move 按钮不能混用。接下来先从已保存 Mar7 C0 夹具正常推进6天
至 Mar13（超过本项目既有至少5天刷新窗口），保存 **r4relic6**，作为跳跃前且已
经过刷新时间的参照。不是新候选，不混入自然新局经济。

读取 r4relic6 时重新核实际日期差6、C仍0、global target与 Mother159/997、
Relic16777221/16777223 身份均保持；重新记录实际三防、aura／timed modifier、
设计体、国家已用／上限海容。不能拿 r4relic0 空 aura 的即时缓存和 Mar13 刷新后
面板直接当同一时点。正常6天可能推进造船、人口或其它原生内容，不能要求整份
SAV raw 与 Mar7 全等，仍须保留所有差异及比较范围。

主线程分别采 **r4mother**、**r4ref** 前缀的两舰原生详情（实际 DPS、速度、维护），
以该原生 SAV 与各截图／动作时间、当前舰名／身份绑定；**jump** 前缀另属真正跃迁
动作／预热／到达证据。三个阶段证据独立归类：Mar7 即时生成和配置、Mar13 刷新
后同日 UI 比较、随后真实 jump。没有看到并绑定对应字段前，各 UI 项均保持待验，
不将 C0 配置专项 PASS 写成面板或机动通过。

六天实际存档已只读核完，见
[r4relic6 独立刷新报告](evidence/1019-analysis/rc4-relic-six-day-refresh-v1.json)。
原生 SHA256 为 `b067c749c7389dd830995aa8e1b14bdfae58ab10f8afa67c6cf4004e0ec70f81`，
实际日期 2200.03.13、距 Mar7 恰6天、C仍0，两艘船／舰队 ID、全部槽与 required、
完整设计体均保持。13项专项检查满足；两舰三防仍为上表数值。此时 Relic 原生
aura_modifier 已实际存有与 Mother 同样的 +.05 fire_rate／-.75 logistics，不再使用
just-spawn 空缓存比较。经过6天只证明已经给出该刷新时间且实际字段如报告所存，
不宣称每一种闭源缓存都已经证明刷新。

国家 **used_naval_capacity 从115刷新到365**，即该原生 Relic 参照带来250实际
海容占用；最大海容和两舰最终维护仍需对应 UI 证据，不能套早期其它分支 HUD 的
上限。这个强超容环境只能用于同一 post-spawn 国家环境的参照，不是新局经济预算。
该报告保持 ui_verified=false；本子任务未打开或操作面板，也未将后续 r4mother／
r4ref／jump 截图预先判为通过。

## Mar13 UI 与真实跃迁预热只读分析方案（实施前追加）

主线程提供本轮实际 UI 证据：r4mother13-verified-details 才是真正 Mar13 Mother
配置图；r4mother13-details 旧尝试没有打开详情，是全景图，保留失败且不引用为
船舶 stats。r4ref13-details 才是真正同日 Relic 配置图。待原始图片／OCR稳定后，
本子任务仅查看原始 GPU 图与原始 OCR，逐项记录可见舰名、三防、DPS、速度和
维护字段及缺失项，绑定 r4relic6；不能由名称相似或 OCR猜测判为同船面板。

中文搜索实际失败亦保留：pyautogui 输入和 Ctrl+V 均留下空框，不把上述 GUI
支持中文输入的方案写成运行通过。主线程已仅将同一颗具有唯一
legendary_leader_1st_system 旗标的实际 system196 改为 ASCII 名 EEP_JUMP_196，
绑定 global target eep_jump_destination_1019 并 survey 揭示。此步骤是原生 UI
目标可选性夹具，主线程明确没有移动母舰、改坐标或改跃迁冷却；后续从实际 SAV
独立核对原始 system8／196 的坐标、目标旗标／绑定和 Mother身份。

实际顺序由主线程操作：ASCII 搜索结果定位 → 原生“启动跃迁”按钮（实际145,339）
→ 目标绿色框（实际512,386）下令 → 正常推进1天至Mar14并保存 r4jumpwind1。
待 receipt／SAV／audit 完整后，只读核 actual jumpdrive_windup 的 source、dest、
progress／duration及日期；用真实字段和 GPU／OCR倒计时给下一步推进天数，
不套基础14天或预设 SAV 状态名。报告与此前静态设计、镜头定位、即时／六天缓存
对照分开；本子任务不操作 UI，不改变目标、船或运行分支。

主线程随后按实际 `end_date` 从 Mar14 推进13天，在 Mar27 保存
`r4jumpedge14` 并悬停原生跃迁按钮。只读分析将以该边界档核对 Mother/Relic
身份、C0、成长账本和队列、真实位置、原生 last_ftl_jump 与冷却；若仍是过渡，
明确保留该事实，由主线程另推进一天取档，不回写为已到达。无需增加 Mar26 样本。

## 同日配置与跃迁实测只读结论

独立 [Relic／UI／jump 报告](evidence/1019-analysis/rc4-relic-ui-jump-v1.json)
19项原生存档断言全部为真，SHA256
`5e849e167c16057d6f529f74ec0c7d491ebd1e28382844ffb846e17e7de85b64`。
报告记录三份SAV、receipt、audit、canonical manifest、读取工具和六组原图／OCR指纹，
可由同名 `.py` 只读重算；输出采用独占新建，不覆盖既有报告。

| Mar13 同国 C0 可见配置字段 | Mother 白绮的裁决 | 原版参照 EEP遗迹 |
| --- | ---: | ---: |
| 船体 | 93960 | 20000 |
| 装甲 | 44787 | 30740 |
| 护盾 | 167310 | 138352 |
| 速度 | 417 | 225 |
| 闪避 | 22.1% | 22.0% |
| 伤害／原生时间图标 | 5598.57 | 2373.28 |

上述为亲读实际 GPU 图并与OCR核对的显示值；精确原生装甲44787.6、参照护盾
138352.5仍见SAV，不把界面整数截位写回存档。伤害数值的原生格式为
`main_2_l_simp_chinese.yml:1684` 的 `SHIP_STAT_DAMAGE_VALUE`，斜线后是
resource_time 图标；不是163.8k等舰队军力。两张图均为Mar13、HUD365/69，
经过六天缓存刷新后的同国参照夹具。图上没有维护金额或供电字段，仍未验证；
不能从全局预算、源码修正量或其它原型图补填当前UI数据。

真实跃迁：Mar14 `r4jumpwind1` 的 Mother159/997仍在system8，原生订单是
`jumpdrive_order.system=196`、`jumpdrive_windup.windup_time=14`、
start_date=2200.03.13、end_date=2200.03.27、can_reach=yes。由该命令计算
Mar14剩余13天；不是套用defines。Mar27 `r4jumpedge14`（SHA256
`a76691e76b2bea8fbcbe06072a6be1a1eb546cfcf6fce621e8517dadf1be1db3`）中，
相同Mother的ship与fleet位置origin均为196，订单已完成，原生船字段新增
`jump_drive_cooldown=yes` 与 `last_jump_date=2200.03.27`；参照舰仍在8。
同日原生按钮悬停图明确显示200天后可再次跃迁、武器伤害-50%、亚光速-50%。
据此确认该真实juggernaut装配可经原生UI完成此次8→196跃迁及进入冷却。

三档country0全部成长变量逐值相同且C0，11条country0队列逐字节相同且全部空；
两舰身份、设计／槽位／required、三防与舰队／船成长账本保持。system8／196
银河坐标未变，唯一legendary_leader_1st_system仍是196，ASCII名称与global target
均指向该原对象。没有独立瞬态 `in_ftl` 样本；旧 `last_ftl_jump.to=13`／jump_count
缓存没有更新，明确排除于此次路径证明。未测200天到期或最大距离边界，不扩为
完整Mod、维护、供电、新局经济或所有跃迁情境的验收。

## phase-A Relic／jump／原版回调对照归档方案（归档前追加）

主线程确认PID36644已正常退出并由独立线程冻结全日志后，新增独立目录
`docs/evidence/1019-rc4-relic-jump-native-control-v1/`。只收本run中
pk2nativecontrol、r4relic、r4mother13、r4ref13、r4jump五个明确前缀的原生
SAV／audit／receipt、动作、GPU／OCR、原始阶段日志副本与等待观察记录；
附本轮Relic配置／rawdelta／六天刷新／UI与jump只读报告、原版CRACKER回调对照
分析／verify／分析源码和本说明。保留未打开详情的全景图、两次中文空框、错误
Move悬停与原始严格rawdelta失败，不删除失败或扩写为PASS。

既有pk2base、manifest、59文件Mod、原始2e静态报告及工具来源优先引用
`1019-rc4-pk2-duration/archive-index-v3.json` canonical，逐SHA验证后复用，
不重复整份Mod，也不复制同目录无关UI或活动日志。若独立CRACKER分析引用的
原生脚本不在canonical中，仅把该已明确引用的primary原字节附入sources。
phase-A最终全日志归档单独引用，不重新冻结或改写该包。

每份载荷排他新建，读取前后stat与两次源SHA一致、目标字节一致。索引记录
源路径、相对目标、字节数、SHA、分类和canonical引用；验收重新枚举完整指定
前缀集合、复读全部源／目标、验证所有SAV ZIP CRC／gamestate／audit／receipt、
每个OCR→原图SHA，以及既有v3索引和59文件来源未变。设置`* -text`并独立核对
Git clean-filter所得blob仍等于原字节。只宣布上述归档字节及受限观察成立，
原版CRACKER是**手动完成回调**对照，绝不是原版武器实际发射或90日验收。

## 来源指纹

原版路径相对 `C:\SteamLibrary\steamapps\common\Stellaris`；本机 EXE SHA 为
`400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。

| 文件 | SHA256 |
| --- | --- |
| common/ship_sizes/18_juggernauts.txt | 3402b13978de2bbcc36c6d4eedab9e4a9ac7f5160183fa2b908029f10842f11f |
| common/scripted_triggers/07_scripted_triggers_ships.txt | 1ec342d3bbd2bf3e5bebc91922b0811686d8fea0d8eb3c79a8771b231720de69 |
| common/component_templates/00_utilities_drives.txt | 7db6b11cc78d37e6c16eab98b0c8960e336a1f860c8aca2b1c4033d3b5475889 |
| common/component_templates/00_utilities_thrusters.txt | c743cd84aab451b8d43259c46249c3a476f28819b417e9bf99aaadbc0721448c |
| common/game_rules/00_rules.txt | 1bcd16731633bc2f2411a868b4a626572f1722068e53875193e12a4c41920566 |
| common/defines/00_defines.txt | 82eebd807eb54af347025b061af2991fc40a1b1059e39c2cb8ee135dca02b7cc |
| common/global_ship_designs/leviathans_designs.txt | b34a781443d03abbc9a5842ea9b6ec556b04e2cd380faa84c560a67bc8e5640e |
| common/ship_sizes/11_leviathans.txt | a000ae956dec3b510084c78fe3268b864b91893bfb10e5a604eea9dc54c1da62 |
| events/leviathans_events_2.txt | 24acfd2d4c9d441a6b2b7384aee8cf7a82b2ff49d90904e11e2debd80f3dd58e |
| common/scripted_effects/caravaneer_scripted_effects.txt | 1f7ea862aef165fb0074de96fef11441b65c6915b290796467c36bee722d955c |
| common/on_actions/00_on_actions.txt | 7693e64fbe974f37db0c68969d10f7bdeec585ce59ca497b5e27ecd69ff8f306 |
| localisation/simp_chinese/main_1_l_simp_chinese.yml | bb9843957cd341d0f39beed436bd17e2e07ecb1fd515b3a86f36673c35ca08c5 |
| interface/main_bottom.gui | 42d1056b69ea84dc0a3499fefa317974b505d4aac3d1ba8bad189b23c7e9b87b |
| interface/gotobox.gui | 05585bc0c7623edc0000424caaade0427b6bf3ee546fc2d97e980c5519904c8c |
| interface/fleet_view.gui | 4ec4caa29edb0dad78db7da606495e979f5fe2407e17c33f833c3bc14648e3ff |
| localisation/simp_chinese/main_2_l_simp_chinese.yml | 34af90279d8fbcf373469e6521e0b51d4109ca1ab0c2f713281fe3e778c3c72e |
| localisation/simp_chinese/paragon_2_l_simp_chinese.yml | a3ff071a3f4fd40ee86fbc3ea85c3e3c0b042c195179ce1b0aa5ff6a6f17a73d |

接口文档来自 `runs/20261019T092935Z/logs/script_documentation`：effects.log SHA
`206dbf28fb12ffa3e8a8222d1af48d4562ffd2d4b4fe8edc43fd14d1d4d537fb`；
triggers.log SHA `a4a439ff44a3d0de7145b0db88ce18b1eec0c056a3454ea9d22d43f0afac2615`；
scopes.log SHA `0ca542261993867fbb5860b806e85f0a445c2e934301cdbaf394f7b9998c3970`。
生产修正文件 eep_modifiers.txt SHA 为
`a5fd09db86cf418fb0a95f0d28fb8347003c9fd513e64d8d90ced067ddc2129d`。

本任务完成只读调查与方案文档，未操作 UI、执行生成／跃迁、修改生产代码或外部
工具，未提交。真正 jump、实际到达、Relic 同日伤害／维护对照均仍待主线程实测。

### Unicode search input observation

At r4jump-vapob-search-result, the search edit remained visibly empty: the generic pyautogui.write wrapper records intended Chinese text but cannot generate those characters. Preserve that failed input and GPU/OCR, never treat its action JSON as successful typing. The next probe writes only the public test system name to CF_UNICODETEXT and physically pastes Ctrl+V into the observed native search edit; successful input and an actual matching result row must be confirmed in fresh GPU/OCR before selecting a destination. This changes no production code, game language or target state.

### ASCII destination alias after two rejected Unicode input probes

Both pyautogui Unicode typing and physical CF_UNICODETEXT/Ctrl+V left the observed native search edit empty; their screenshots are failures, not selected destinations. To avoid dependence on the desktop IME, the independent functional fixture will survey visibility and give the existing system marked legendary_leader_1st_system the ASCII name EEP_JUMP_196, also saving eep_jump_destination_1019. Verify the unique matching actual system is 196, original NAME_Vapob, coordinates (5.23353,-121.0006), before execution. This changes only its test name/visibility; do not move either ship, change coordinates, remove cooldown or bypass actual jump controls. Search ASCII EEP_JUMP_196, confirm the real result and destination UI, then use the native jump button and native time advance. Actual movement/order/arrival must still be proved from SAVs.
