# 母舰无限成长与五级组件调查（2026-10-19）

## 目标与范围

本子任务负责母舰成长同步、固定设计迁移接口审查，以及每五级随机正面组件的原生可行性研究。主任务负责全部 Windows 桌面和简体中文实机操作；本子任务不启动、停止或操控游戏。不修改基础 `eep_mothership` 数值，也不覆盖其它工作线程的本地化源。

最终规则是 `L=floor(C/10)`，不设等级上限；每级额外武器伤害、舰体、装甲、护盾各 +5%，舰体和装甲固定日恢复各 +0.1。成长使用单个永久修正，以倍率 L 替换同步。每五级应随机升级一个真实舰体组件或增加随机正面效果组件；不能把普通静态修正称作真实组件。

## 实施前设计

1. 继续以结算后的国家变量 C 为唯一成长输入；不得从事件次数推导等级。
2. 重复同步、同日重载时不重复发放成长；每次需要同步时先移除旧倍率，再添加唯一的新倍率。
3. 固定设计以原生 `set_ship_design` 在原舰船对象上替换，并使用舰船设计版本标记防止重复迁移。保持旧母舰被毁后不重生。身份、位置、队列及损伤能否保持必须由实机证据确认。
4. 优先研究原生 `add_starbase_component`。如果普通 standalone utility 对固定母舰不产生属性收益，则测试真正的 aura 组件。未经原生探针确认，不自动发放组件奖励，也不宣称功能完成。
5. 若 aura 附加和重复堆叠都有效，随机池可选护盾、装甲、舰体、武器伤害、命中或恢复等正面核心；组件本身承载正面效果，不另发同名普通 modifier 冒充组件。奖励计数应持久化并与 `floor(L/5)` 比较，仅补发差额。
6. 若同名 aura 被去重，则先查实 `stack_info` 的行为；不得假定无 `stack_info` 必然堆叠，也不得引入有限阶梯并掩盖无上限要求。需要在文档中明确组件次数或阶梯边界。

## 原生依据与已知事实

证据仅来自本机 Stellaris 4.5.2 原版脚本及本次启动导出的 engine script documentation，不能使用 CK3 方言推断。

- `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T072723Z\logs\script_documentation\effects.log:480`：`add_modifier` 支持 fleet、ship、starbase，`multiplier` 接受变量。
- 同文件第 2058/2062 行：`add_starbase_component` / `remove_starbase_component` 仅支持 starbase，操作 standalone 组件。
- 同文件第 2575 行：`set_ship_design` 支持 ship/fleet，可指定预定义 design key 或 design target；接口未提供任意组件替换、添加槽位的参数。
- 同文件第 3240 行：`create_ship_design` 从预定义设计创建，非运行时任意组件设计器。
- 同目录 `scopes.log:266`：ship/fleet 可转入 starbase；`scopes.log:94`：starbase 可转入其 ship。
- 原版 `common/component_templates/00_utilities_auras.txt` 对 `stack_info` 的注释明确：相同 id 只采用优先级最高的 aura。注释不证明省略 `stack_info` 时重复同型 aura 的结果。
- 原版 `events/ancient_relics_archaeotech_events.txt:103` 使用 `starbase.ship.has_component` 检查 standalone aura，再调用 `add_starbase_component`；因此可借助真实 `has_component` 守卫进行存在性核验，不能仅凭国家变量认定组件已安装。
- [普通 SHIELD_BOOSTER 原生探针](evidence/1019-requirements/component-probe-observations.json)：两份 standalone 条目均保存且重载保留，但护盾仍为 48370.608，设计未变；这条普通 utility 路线尚未产生正面收益。
- 已有 `EEP_SYMBIOTIC_SHIELD_CORE` 为专用真实 utility aura 原型：无成本、无供能；`friendly_aura` 为 `apply_on=fleets`，仅绑定母舰，护盾 +10%，省略 `stack_info`。当前不得从定义推断它已经生效。

## 验收标准

- 修改后的 P 候选须先由 `open_kaishek` 包级检查通过，再执行简中原生实机；本子任务仅提供静态证据与审查，UI 探针由主任务执行。
- C=0、9、10、19、20、100、10000 应分别得 L=0、0、1、1、2、10、1000，单一成长修正倍率正确；重复同步和重载不叠加。
- 若接入随机奖励，跨越五级边界每次一份，跨越多个边界补齐差额，重载不重抽；奖励真实存于组件列表，属性有正向变化，其他舰队不受影响，组件和计数均重载保持。
- 固定设计迁移保留身份、舰名、位置、队列，损伤变化需实测；旧档无免费复生或额外开局奖励。
- 本子任务新增本地化只写 `localization/evolution-1019-authored.json`，至少提供简体中文、英文、德文；外语仅做静态验收，运行时不在范围内。

## 当前状态

2026-10-19：先完成上述设计与只读调查，尚未对本子任务负责的生产脚本作改动。等待专用护盾 aura 的原生附加、重复附加和重载探针结果后决定组件实现；成长与迁移继续审查。

### 成长同步补强设计

审查发现当保存的 `eep_applied_level=0` 且实际仍挂有成长修正时，原条件不会移除多余修正。实施时补充 `L<=0 且 has_modifier` 修复条件，使零级实际没有成长修正；正等级缺少修正和倍率变量不匹配的既有自愈仍保留。这不改变正常正等级数值，不触碰基础 `eep_mothership`。该分支的验收是零级脏状态一次清除，第二次同步无效果。

已补充该条件。`open_kaishek` 自包含 CLI 对本文件返回 `PARSED`、2582 bytes、680 tokens、37 blocks、`diagnostics=[]`、`roundTrip=true`。这仅证明当前单文件 P 语法保真解析；整包检查和原生行为仍由主任务在冻结快照完成。

### 设计迁移审查

原版 `events/biogenesis_crisis_events.txt:2317` 和 `:2358` 在已有 behemoth 舰船上使用 `set_ship_design`，支持该接口用于原舰船转换的设计方向。接口文档未承诺保存损伤、建造队列或 standalone 列表，因此这些仍是原生验收事项。

现有 `eep_mothership_design_1019` 同时用于 startup 新舰和 sync 旧舰迁移。若预发布开发期间修改相同 design key 的内容，已经带该标记的开发档将跳过迁移。最终固定设计发生变化时必须协调递增 startup 与 sync 的设计版本标记；不能将开发档的旧设计体当作新配置证据。该风险已通知主任务。

### 第二路 aura 探针设计（实施前）

主任务暂时因武器 CSV 的工具验收缺口暂停新实机，修复工具后再恢复。为同一冻结快照一次比较两路，新增独立 `EEP_SYMBIOTIC_SHIELD_CORE_SHIP`，保留已有 `EEP_SYMBIOTIC_SHIELD_CORE` 的 fleet 路径。新组件使用 `apply_on=ships`，条件为 `exists=owner`、`exists=fleet`、`fleet` 等于绑定母舰。组件名、说明和 aura 名只写独立 `evolution-1019-authored.json`，由本地化线程集成。

不能仅从 `000_documentation.txt` 的 “requirements for this aura” 断言 limit 在接收方执行。支持接收方解释的进一步原生依据是 `00_utilities_auras.txt:731` 的科学船电磁干扰敌方 aura：`apply_on=ships`，limit 检查机械帝国舰船或智慧／自主电脑。如果条件只查发射方科学船，就无法按敌方舰船配置选择性产生效果；这是设计意图推断，仍须实测。

探针同时保留同星系其它有护盾舰队作控制：先保存母舰和控制舰实际最大护盾；附加 fleet 型，运行每日刷新、保存、重复附加、保存和重载；移除或回到纯净功能档后依次测试 ship 型。必须核对真实 standalone 条目、母舰属性、控制舰属性与错误日志。若 ship 型母舰有效但其它舰队也增加，则不能认定过滤正确；若单份有效而重复同型无第二次增加，则不得接入无限奖励循环。

静态资产调查发现旧原型写了 `GFX_ship_part_shield_booster`，本机原版 `interface` 没有此名称；原版 `SHIELD_BOOSTER` 使用 `GFX_ship_part_shield_recharger`，在 `interface/icons.gfx:2771` 定义。实施时更正这个图标引用，避免无关 missing sprite 报错污染组件探针。

继续核对发现 `component_set="aux"` 也不是原版定义；`aux` 是 `size`，不是组件集键。原版 `common/component_templates/00_starbase_building_auras.txt` 的 standalone aura 均不写 `component_set`。两个探针将同样省略组件集，避免无效引用，也不把探针挂到原版设计器组件列表。

### 随机池预备方案（尚不自动发放）

若原生路线通过，六个等权真实核心拟为护盾 +10%、装甲 +10%、舰体 +10%、武器伤害 +5%、索敌 +3、舰体及装甲固定日恢复各 +0.2。无无限提速；索敌使用原版 `ship_tracking_add` 的百分点单位。各核心以真实 aura 自带效果，不同步发普通修正。

每次国家同步推导应发奖励数 `B=floor(L/5)`；已发计数持久化于绑定母舰 fleet。仅在母舰存在、仍归属绑定国家且存在可用 starbase 时补发 `B-已发` 的正差额；每完成一次原生附加才增加计数。同日重复同步不重抽、重载不重抽。多级跨越应补齐；恢复组件的物理存在性可用原生 `starbase.ship.has_component` 检查，但这不足以证明重复数量正确，因此重复数量仍需 SAV 对照。探针未确认前不连接此循环，不制造虚假的已发计数。

### 本轮交付与静态证据

已交付零级成长修正自愈、独立 ship 型探针及三个简中／英／德作者键；现有 fleet 型只更正两个无效引用，保留其原始接口行为。未接自动随机组件发放。

[静态复核记录](evolution-components-1019-static.json) 保存两份实际脚本 SHA256 和 `open_kaishek` 无诊断、逐字节 round-trip 解析结果。作者 JSON 三语言键集一致，英／德未发现简体中文占位。英／德为作者源静态检查通过；最终 YML 由本地化线程集成并静态验收，运行时不在范围内。

原生 UI、组件实际正向收益、重复堆叠、接收过滤、重载及固定设计迁移尚由主任务执行；不能据此静态记录宣告 Mod 验收完成。

## 旧档迁移：健康与真实排队夹具调查

本轮只读调查不改生产代码、不启动游戏、不编辑 SAV。`set_ship_design` 的原生文档只说明替换 ship／fleet 的设计，没有宣称保持当前值、损失绝对值或健康比例，因此必须用同日真实 before／after／reload 对照确认。此前普通组件探针已经观察到重载使 design ID 1666 变为 1800，而设计体 SHA 不变；不能只因 design ID 改变就认定迁移成功，应比较完整设计体。舰船、舰队、starbase 和队列身份仍按验收要求单独核对。

### 健康接口

以下均来自本次 4.5.2 导出的 `effects.log`／`triggers.log`，接口存在与执行语义验证分开记录。

| 需求 | 原生接口 | 边界 |
| --- | --- | --- |
| 读当前舰体／护盾 | `has_hp`、`has_shield_hp` | ship scope；可供 `export_trigger_value_to_variable`，尚未在本次迁移探针验证导出值 |
| 读最大舰体／装甲 | `has_max_hp`、`has_max_armor_hp` | ship scope；原版 `events/grand_archive_events.txt:7942` 确实导出这两个触发器值 |
| 读三防比例 | `has_hp_percentage`、`has_armor_percentage`、`has_shield_percentage` | ship／fleet；恢复比例前先保存为变量的方案仍需原生证明 |
| 降低舰体 | `reduce_hp`、`reduce_hp_percent` | ship；固定损伤夹具优先用明确绝对值的 `reduce_hp` |
| 降低护盾 | `reduce_shield` | ship；绝对量 |
| 全部修复舰体 | `repair_ship=yes` | ship；不是三防全修复承诺 |
| 按比例恢复 | `repair_percentage`、`repair_armor_percentage`、`repair_shield_percentage` | ship／fleet；文档示例 0.1 |
| 按绝对量恢复 | `repair_amount`、`repair_armor_amount`、`repair_shield_amount` | ship／fleet |
| 一般伤害 | `damage_ship` | ship／fleet；可带 attacker 并产生 on-action 归因，不可未经实测当作精确装甲设置器 |

未发现直接 `set_hp`／`set_armor`／`set_shield`、`reduce_armor` 或最大护盾值触发器。原版未找到负数 `repair_*` 的用法；不能靠负修复假定可精确降低装甲。`reduce_hp_percent` 在原版存在 0.15 与 15 两种写法，文档示例为 0.25；本任务不推断这些用例一致正确，更不能用未校准的百分比制作验收 fixture。

若原生迁移本身保持比例，就不额外写健康补偿代码。若原生不保持，先从实际 before／after 确认改变的是当前值、最大值还是比例，再设计最小恢复方案；尤其不能为了补装甲而调用未经验证的广义伤害。任何修补必须先更新本文设计并重新实测，当前未添加该类代码。

### 已核实的历史母舰 SAV

[只读调查原始表](evolution-components-1019-old-save-candidates.json) 直接解包仓库已归档原生 SAV，保存 SHA256、日期、母舰实际三防、舰名、坐标、设计实现、starbase 原体、队列原体以及每笔已付订单的设计、进度和资源。25 份 v13／v10 档的 SAV SHA、gamestate SHA 与历史 audit 及 native-save receipt 全部匹配。**这 25 份档中母舰本体三防始终全满**，没有“母舰已受损＋正在排队”的现成夹具；`j13hurt`／`yard10hurt` 伤的是其它小船，不能冒称母舰伤害证据。

优先复用 v13，避免将历史 v10 失败候选用作最终配置证明：

| 原生档 | 日期／SHA256 | 已有真实 before |
| --- | --- | --- |
| [j13paid.sav](evidence/1015-2026-10-15/v13-shipyard-runtime/j13paid.sav) | 2200.01.02；`fd40e00c219a17145e53c26d57b4272f9387a5b3ef0af1210c11366727361b79` | 11 笔已付订单，item 0～10 全为 0/60，每件 81 合金 |
| [j13ten.sav](evidence/1015-2026-10-15/v13-shipyard-runtime/j13ten.sav) | 2200.01.12；`834ea5325f93e3d3e92a44aabccd87195564cd4f1292d4439ae865eba5af8d2e` | item 0～9 各 10/60，item 10 为 0/60；适合验证进行中队列未重置 |
| [j13hurt.sav](evidence/1015-2026-10-15/v13-shipyard-runtime/j13hurt.sav) | 2200.03.12；`c78fdc192cfab01841abdf4917f8b1ab1cd95e6fc07f704ce625b079b97d37fe` | 尚有 item 10 为 10/60，母舰全满；其余小船损伤不能代替母舰损伤 |

三档母舰均为 fleet 146／ship 822／starbase 13，舰名 `NAME_EEP_Baiqi_Mothership`，旧设计实现 1725；当前值等于最大值：舰体 101460、装甲 24429.6、护盾 48370.608。starbase 的 build_queue=53、shipyard_build_queue=54；queue 54 的 owner=0、type=ships、location={type=0 id=822}、simultaneous=10；每笔船订单的设计实现 1702、orbitable.starbase=13、paying_country=0。`j13paid` 坐标为 origin 2／(-64.224,-73.7753)，`j13ten` 和 `j13hurt` 为 origin 2／(-146.51378,-160.06316)。

原始 artifact 目录均为 `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1015-implementation\runs\20261014T223819Z`，文件名相同；仓库归档与 receipt 中的原始 SHA 一致。

可行的下一步方案是先用最终候选原生暂停加载 `j13ten`，检查是否已经触发迁移；如果加载本身尚未迁移，可直接在这个旧设计＋真实排队现场通过原生命令对母舰制造可核的固定舰体／护盾损伤，保存新的 before，然后显式运行同步并保存 after／reload，无需再启动旧 Mod 包。若原生加载已立即迁移，则不得把之后制造的损伤当作迁移 before，必须另建真实旧包夹具。上述是待主任务实测的条件方案，未执行也未宣称通过。

## Aura 作用链：fleet 型首次原生失败之后

主任务已完成 fleet 型单次原生附加并推进一天；本子任务只读解包对应 SAV：`aurafleet1.sav`，2200.01.02，SHA256 `18bf58153e1e85c2b569107f424e6eeb5bb1e8f60f50fc96691967bb174dd683`。starbase 19 的 standalone 确有 `EEP_SYMBIOTIC_SHIELD_CORE`，但母舰 ship 808 的最大／当前护盾仍为 167310。未把此失败认定为有效组件奖励。

[作用链原始观察](evolution-components-1019-aura-chain-observations.json) 对照 `pmm00.sav` 与 `aurafleet1.sav`，直接保留 ship 的 `auras`、`aura_modifier`、设计体 SHA 和 starbase 原体。两档母舰实际设计均为 1875，设计体 SHA256 `e160208906964b8bd295963d5695283ceb3608f324ae6ace4baaed59aca47d4b`；没有共生核心组件。所有观察到的舰船中均没有共生核心 aura 接收条目。

母舰自身却确实有原版 `aura_inspiring_presence` 与 `juggernaut_logistics`，两条 `source.ship=808`；实际 `aura_modifier={ship_fire_rate_mult=0.05 ships_logistics_mult=-0.75}`。这排除了“原生 aura 普遍不能作用于发射舰自身”的解释。原版物流光环来自主宰反应堆组件（`00_utilities_reactors.txt`），说明实际已装备组件到 source 再到 receiver 的链路在该母舰存在。

当前仍需区分两种原因，不能从失败次数直接认定引擎不存在真实组件能力：

1. starbase standalone 只进入自动设计器输入，固定事件设计没有把它装备为可生效组件；原版 `starbase_modules/00_example.txt` 描述模块变化会重建设计，建筑的 equipped_component 会直接装备，但未承诺固定事件设计的 standalone 行为。
2. 两个试验 aura 都省略 `stack_info`；查到的原版实际 aura 都提供该块。省略后可能导致 source 未注册，尚没有原生证据允许排除此原因。此前“省略后可能可重复叠加”只是待验证假设。

### 最小辨别探针（实施前，交由主任务）

- 优先直接给同一母舰 starbase 原生添加现有 `STARBASE_AURA_BULWARK_ARRAY`。该原版组件有明确 stack_info、没有目标 limit、护盾 +100%，无需改包即可将自定义 aura 定义问题与 standalone 路径问题区分。检查 Mother 和同星系控制舰的 `auras.source`、`aura_modifier`、最大盾，随后移除或回纯净功能档。该探针预计影响友方控制舰，不能作为过滤成功证据。
- 如果原版 aura 可用，再为自定义探针补明确且不冲突的 stack_info，并重新做绑定过滤、同型重复与重载；在这之前不新增随机池代码。
- 如果原版 aura 也只存列表而不产生 source，可在独立功能档调用 `rebuild_owned_starbase_designs=yes` 检查是否物化；该 country effect 文档仅承诺重新选择非可设计星基的自动设计，普通 juggernaut 在原版是可设计舰型，因此它可能不覆盖当前母舰。不能把这个全国家设计重建作为未经验证的生产修复。
- 预定义多个真实设计并用 `set_ship_design` 切换是已知原生接口，但任意组合、槽位和无限阶数没有运行时 API；有限设计表只能提供明确有限的组件阶梯，不能掩盖每五级持续奖励的边界。

### 诚实的最小备选（仅设计，未获准实施）

若上述真实组件路径经原生验证都不可用，最小备选是公开称为“持久共生强化”的随机正面修正，明确说明它不是舰体组件、不会新增组件槽位，也不满足原始真实组件要求。六类可用护盾、装甲、舰体、武器伤害、射速、固定日恢复，不增加无限速度。

该备选仅在用户接受能力边界后实施：以 `floor(C/50)` 推导总抽取次数，母舰 fleet 保存六个分类计数与已抽总数，每次补差只抽一次并立即记账；每类仅挂一个永久修正，以该类计数为倍率替换。总抽取数必须等于六类计数之和；重载、重复同步无新抽取，母舰摧毁不免费复生，其他舰队无收益。验收直接检查原生计数、唯一修正及三防／伤害变化，并在对外文字中始终称修正强化。本子任务没有擅自新增这一降级实现。

### 原版 aura 对照已执行后的结论更新

主任务继续完成 ship 型与原版 BULWARK 探针。本子任务直接读 SAV，SHA 与主任务提供一致：

| 原生保存 | 日期／SHA256 | 真实结果 |
| --- | --- | --- |
| `auraship1.sav` | 2200.01.03；`a396ad1273536baf7ba771b6eda9f572e9002e854c9a87682afd53ab4168eac3` | 仅 SHIP 型 standalone；Mother最大盾167310，未出现任何共生核心 aura 接收者 |
| `auranative1.sav` | 2200.01.04；`d6f985643b249e80239a0574c7ba2a51e45182b38a482f14c8b60b68ddb3af24` | 仅原版 BULWARK standalone；Mother最大盾167310，未出现任何 BULWARK aura 接收者 |

两档 Mother808 实际设计体仍为 SHA `e160208906964b8bd295963d5695283ceb3608f324ae6ace4baaed59aca47d4b`，设计与实际 ship 原体均不含试验组件或 BULWARK 组件；Mother 的 `aura_modifier` 仍只有 `ship_fire_rate_mult=0.05`、`ships_logistics_mult=-0.75`。普通控制舰 1～5 的最大三防也未变化，未观察到护盾外溢。

因此“仅仅是自定义 aura 省略 stack_info 或自定义 limit 写错”不足以解释原版 BULWARK 也不生效。现有证据更支持该固定事件母舰的 standalone 条目没有被实际装备成可作用的舰船组件；这是从三种附加结果和实际设计／作用链作出的推断，不宣称掌握闭源引擎内部实现。

主任务将执行最后一次 `rebuild_owned_starbase_designs=yes` 加一日刷新并保存后收敛；不无限扩展接口试验。目前仍未添加随机奖励或启用降级备选。

### 最后重建探针与有限能力结论

主任务完成原生 country effect `rebuild_owned_starbase_designs=yes` 并再推进一天：`aurarebuild1.sav`，2200.01.05，SHA256 `a5a6fbccb957953cfb278a949e7841b38cd6d2b9cbb070041cf12e0521988cd0`。本子任务已直接读取并追加至作用链观察 JSON：

- starbase 19 仍只保存一份原版 BULWARK standalone。
- Mother808 仍为实际 design 1875，完整设计体 SHA 不变，最大／当前舰体 93960、装甲 44787.6、护盾 167310。
- Mother 的作用修正仍只有原版 +0.05 射速、-0.75 物流；普通控制舰护盾未改变。
- 整个 gamestate 中共生 aura 名、BULWARK aura 名与其 stack id 的出现次数均为 0，不只是漏查 ship 而忽略 fleet 接收字段。

**有限结论：本轮 4.5.2 固定事件设计母舰的 standalone 追加路径未产生有效真实组件收益；每日刷新、两个自定义 aura、原版有 stack_info 的无条件 aura，以及一次全国家自动星基设计重建均未改变这一结果。** 因此当前不能接入每五级真实随机组件发放。该结论不外推全部 Stellaris 引擎、一般自动设计星基或其它舰型，也不把脚本静态解析通过当作组件成功。

两个自定义组件目前保留为等待主任务决策的候选；正式包不得携带未经验证却宣称有效的原型。用户正在选择接受明确命名的永久随机共生修正，或继续要求真实硬件组件；回答之前不修改候选代码，不实现降级方案。

## 永久随机强化的六计数同步预研（仅设计）

如果用户接受上述备选，建议保持真实实现边界：UI／文案称“共生强化”，公开说明使用永久修正，不使用“已新增舰体组件／槽位”表述。以下为可审查设计，尚无代码。

### 状态与不变量

国家只从已结算 C 推导 `L=floor(C/10)`、应得抽取次数 `B=floor(L/5)=floor(C/50)`。绑定且仍归该国的唯一 Mother fleet 保存六个非负整数计数 `N_hull`、`N_armor`、`N_shield`、`N_damage`、`N_rate`、`N_regen`，以及已完成抽取总数 R。新变量仅在不存在时初始化为 0，不能每月重置。

核心不变量为 `R=sum(N_i)`、`R<=B`（真实 C 单调不减）。每个新奖励仅执行一次等权六选一，所选 `N_i` 与 R 同一段同步效果中各加 1；完成后随机结果以计数持久化，后续同步不重新推导随机分布。原生保存发生在效果执行完成后，before／after／reload 仍须检查不变量，不能以作者推断代替实际证据。人工将 C 降低不是合法结算输入，不应因此回滚并重抽已发结果。

六类候选数值是舰体／装甲／护盾各 +10%，伤害／射速各 +5%，舰体和装甲固定日恢复各 +0.2；无无限提速。每类使用自己唯一的永久 fleet modifier，倍率为 N_i；每类的“上次已应用计数”单独保存，计数变化或修正缺失时才移除旧修正并按最新倍率添加，零计数却挂修正时清除。这样重复同步不会堆叠，同日原生重载后也不会重抽或重新应用相同倍率。

R、六类计数、六个已应用计数都存同一个 Mother fleet，不以全国家属性发放，不凭事件次数累计，不因旧母舰被毁创建新船。原生验收逐类核对实际 modifier 的数量、永久期限和倍率；仅凭计数增加不能宣布属性生效。

### 批量跨级与无设计上限

正常结算一次可能跨多个五级边界，补发差额 `P=max(0,B-R)`，不能只执行一次 random_list 然后把 R 直接设置为 B。每一份奖励都必须有独立随机结果。C=10000 时 L=1000、B=200，应有恰好 200 份分类计数总和，而非三级封顶或仅一份奖励。

为了避免历史高 C 导致单帧极长循环，可将单次抽取工作预算设为最多 200 次：`X=min(P,200)`，执行 X 次真实抽取，结束后统一同步六类实际修正。该数值仅限制每次工作量，不限制 B、L 或分类计数。P 仍为正时保留真实待补差额，后续既有月度同步继续处理；如果产品要求短于一月的补发延迟，再设计唯一的延期事件及调度标记并原生验证，不能随意加入重复事件。C=10000 的规定验收在一次预算内完成。

这意味着极大历史 C 的首次接入可能分批兑现，必须在报告中明确已发／应发／待发，不能把尚未发完说成全部同步完成。第二次调用若继续消化未发差额，是完成尚欠奖励；待差额为零后重复调用必须完全不增加计数。数学上的无穷与引擎数值精度不是同一承诺，本设计不设置人为等级或累计奖励上限。

### 必要原生验收

阈值前后至少覆盖 C=49／50／99／100 与规定的 C=0／9／10／19／20／100／10000，并从干净功能档验证，避免人工降低 C 混入已发奖励。跨界检查 R 与六计数增量恰好等于 `floor(C_after/50)-floor(C_before/50)`；一次跨多界逐份抽取。保存、同日重载、再次同步后 R、六计数、实际六类唯一 modifier 完全保持。另测分类修正缺失的自愈不会新增随机抽取；高于单次预算的历史 C 明确显示待补量并最终清零。母舰消失时国家 C 和报告可继续保留，但不得复生、给其它舰队发奖励或凭无效任务增加 C。

## 用户扩大授权：优先动态硬件研究与最小探针（实施前）

用户最新明确要求优先研究动态组件，扩大互联网与原版文件调查，仅在真实硬件路线仍不可行时条件接受随机共生强化。此前“等待偏好选择”已由这条新授权取代，不能直接启用备选。

扩大检索首先发现官方 [Dev Diary #253（3.4 Cepheus，2022-05-05）](https://store.steampowered.com/news/posts/?appids=281990&enddate=1652371652&feed=steam_community_announcements) 说明 triggered modifiers 可以使用 `mult`，乘数来自 modifier 或 script value。短摘录：“define a ‘mult’ value”。这不是组件专用原生实测证据，但提供区别于 standalone 的新路径。

本机原版 `component_templates/000_documentation.txt:18` 对组件 `triggered_ship_modifier` 明确写 “Use like triggered modifiers elsewhere”，并说明 ship scope。原版生物装甲在 `00_biogenesis_utilities.txt:673/762/851` 按实际装甲比例动态启用恢复；隐形装置在 `00_utilities_aux_first_contact.txt:46` 按 `is_cloaked` 动态减少护盾。原版 script value 文档允许 `scope.variable`，并示范先确认变量存在才读取。此组合使“实际装备组件，自身动态倍率升级”值得先做最小原生测试，而不再将新组件仅写入 standalone 列表。

主任务已授权如下最小生产候选改动，先验证语法与引擎，不接随机发放：

1. 移除已失败的两个 aura 组件定义，改为唯一真实 utility 组件 `EEP_ADAPTIVE_SHIELD_CORE`；无成本、无功耗、`hidden=yes`，阻止其它国家设计器手动选择。
2. 组件的 `triggered_ship_modifier` 只允许属于绑定 Mother fleet 的实际舰船，直接声明 `ship_shield_mult=0.10`，以 `mult=value:eep_component_shield_level_value` 缩放。它不是另行 `add_modifier` 的普通舰队修正，效果必须来自已装备组件本身。
3. 新 `common/script_values/eep_evolution_values.txt` 在 ship scope 读取 `fleet.eep_component_shield_level`；舰队或变量不存在时返回 0，不设置上限。
4. 主任务保留遗迹基准五个辅助组件，另加专属 AUX6 并在固定设计中装入核心；本子任务不改舰段／设计／基准修正。
5. 新文本仅追加本子任务作者 JSON 的简中、英、德三键，不编辑 YML；旧探针文本由本地化线程清理。

验收顺序是冻结快照通过 open_kaishek，然后在实际设计与 ship 对象确认 AUX6 真正装有核心。依次设 fleet 层数为未设／0、1、2，逐日刷新并保存，核对最大盾增量与实际 ship triggered 属性；同日重复赋值和原生重载不产生额外倍数，普通舰队不受影响。只改变变量、完全不调用 `add_modifier`，是此探针对组件自身动态效能的关键辨别。若需要重载才刷新，也必须如实记录；失败时不得称作硬件升级成功。

## 扩大互联网研究：实际组件代码已找到

完整代表查询、原始 URL、短摘录、适用版本、来源边界和五条探针路线保存在 [互联网研究台账](evolution-components-1019-web-research.json)。官方 Wiki 的 Effects／Ship_modding 页面本轮返回 Internal Error，grep.app 返回 429；检索到的转载 Wiki 和二手教程只用于发现线索，技术结论改查官方开发日志、本机原生文件与作者原始源码。

最强新增证据是 Gigastructures 作者仓库，固定 commit `436812fb3acd9dc7d6cb5e666268a3a1d8135aa7`：其 [组件源码第28行起](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_templates/giga_eawaf_components.txt#L28) 的四个 `GIGA_EAWAF_DISENCHANTER` utility 组件实际在 `triggered_ship_modifier` 内使用持久变量作为 mult。短摘录：`mult = event_target:giga_eawaf_country.giga_eawaf_field_potency_multiplier`。这已不是仅从通用 triggered modifier 示例推测组件语法。

同 commit 的 [descriptor](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/descriptor.mod) 声明 Mod 3.40.4 DEV、Stellaris `v4.5.*`；[实际效果定义](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/static_modifiers/giga_eawaf_static_modifiers.txt#L78) 给这些组件引用的 named modifier 提供真正 upkeep 数值，排除了只是未定义的自创字段。它是开发分支实际源码，不等于外部正式版运行认证，也不等于本机母舰已经通过；护盾属性、变量实时刷新、保存和拆件仍由最小探针证明。

已用作者固定 commit 扫描 158 份实际 component／scripted effect／event 文件，读取错误 0，结果见 [源码扫描记录](evolution-components-1019-giga-web-source-scan.json)。除上述组件 mult 外，扫描找到多处从预定义 key 创建 ship design 的实例；未在该限定文件集发现任意运行时组件数组构造接口，不能把这个有限扫描说成全引擎不存在该能力。

其余路径也有明确边界：

- 官方 [DD380](https://store.steampowered.com/news/posts/?appids=281990&enddate=1745492418&feed=steam_community_announcements) 说明深空擎天堡每阶段是独立真实设计，并在建造／升级／降级时选择；这支持“原生真实设计迁移”方向，但不等同于脚本任意拼装组件。
- [Designable Starbases 作者说明](https://steamcommunity.com/sharedfiles/filedetails/?id=3125931110) 明确要求光环仍需建筑且实际装进设计，采用 dummy 设计架构，且有单设计和周期切换限制。它是历史 Mod 作者对自己实现的说明，不是当前 4.5 母舰能力认证。
- [CWTools 的固定版本组件规则](https://github.com/cwtools/cwtools-stellaris-config/blob/99147efe8072b331005b50536762dcc0b8573224/config/common/components_consolidated.cwt#L206) 把组件 triggered modifier 定义为 ship scope；这是维护者自己的校验器规则，不冒充闭源游戏实现。
- 星基建筑 `equipped_component` 与模块 section／component_set 是区别于 standalone 的实际硬件链，已由另一只读线程查到原版 Arkship 和作者 Mod 的实例，交主任务做隔离探针。本子任务没有重复操作桌面。
- `upgrades_to` 配合自动设计更新可以表达有限真实组件阶梯，但任意高阶继续成长仍需动态组件倍率；不得向全帝国授予最高科技或改原版全部主宰来绕过隔离规则。

目前优先级已经调整为“已装组件自身动态 mult”第一、建筑／模块真实装载链第二、有限预定义设计迁移第三。最小动态核心与 script value 已实施并分别通过 `open_kaishek` 保真解析（747／359 bytes，无 diagnostics）；正式包级及原生结果仍待主任务，不提前切换到随机普通修正备选。

若最小核心没有改变最大盾，需先辨别动态 multiplier 是否未被求值，以及 `ship_shield_mult` 是否已进入实际 ship 总修正但没有触发最大盾重算。原版常规护盾增幅器将此字段写在 design 的 modifier，而 Giga 当前实例使用 upkeep 字段；两者都不能单独保证盾字段的运行时刷新。可在原生 ship scope 导出 `ship_shield_mult` 总值对照，必要时用已知 runtime 字段做后继最小对照；不能把单个字段失败扩大为所有真实动态组件都不可行。

## 六个真实动态核心候选（实施前设计）

主任务最新授权在工具修复窗口完成可原生检验的完整候选，不等待单核心证明才编写随机状态机；这并不将候选视为已生效。保留遗迹基准五辅助件，主任务另加六个真实辅助槽，分别固定装备 `EEP_ADAPTIVE_SHIELD_CORE`、`EEP_ADAPTIVE_ARMOR_CORE`、`EEP_ADAPTIVE_HULL_CORE`、`EEP_ADAPTIVE_DAMAGE_CORE`、`EEP_ADAPTIVE_TRACKING_CORE`、`EEP_ADAPTIVE_REGEN_CORE`。本子任务仅改自身组件、script value、同步 effect 和独立作者 JSON，不改舰段／设计、YML 或基础母舰修正。

每个组件零资源成本、零功耗，隐藏且不可由普通设计器选择；自身 `triggered_ship_modifier` 限定 owner 存在且 ship 的 fleet 等于该 owner 绑定的 Mother。六种效果依次为每层护盾／装甲／舰体 +10%、武器伤害 +5%、索敌 +3 点、舰体与装甲固定日恢复各 +0.2。各自 mult 仅读取本 fleet 对应的 `eep_component_<shield|armor|hull|damage|tracking|regen>_level`，不存在时返回 0。不得通过额外 `add_modifier` 发组件奖励；现有每级成长的唯一 `eep_mothership_evolution` 仍独立保留。

本机生成的 modifiers.log 证实使用 `ship_shield_mult`、`ship_armor_mult`、`ship_hull_mult`、`ship_weapon_damage`、`ship_tracking_add`、`ship_hull_regen_add_static`、`ship_armor_regen_add_static`；原生组件实际有索敌加 5／10 的用例，故索敌数值为点数而非 0.03。字段存在与类别正确仍不能代替本舰型动态刷新测试。

### 随机发放、持久化和批量预算

country 同步首先从 C 推导 L 与距下一级余量，再计算 `eep_component_entitled=floor(C/50)`（B）。仅当绑定 Mother fleet 存在、仍归当前国且只有一艘实际主宰时才迁移设计、同步基础成长、发放随机升级。绑定对象无效时不创建、寻找或绑定替代舰。

Mother fleet 保存六层数和 `eep_component_rewards`（R）；仅在变量未设置时初始化为 0，已有值绝不重置。每次调用设置临时工作预算 200，循环条件为 R<B 且预算>0；每次独立 random_list 六分支同权重 1，仅所选层数加 1，随后 R 加 1、预算减 1。循环结束清除临时预算。正常游戏应保持 R 为六层数总和；不设总等级／总抽取／单类层数上限。超出本次 200 的欠额留待后续既有月度同步继续处理。

控制实验会在 C0、R0 的同一档人工设 shield 层数 1／2，以隔离组件求值；这是故意偏离自然抽取不变量的夹具。因此同步绝不从层数总和反算 R，也不因 R0 抹去已有 shield 层数。真实自然路径的 R=sum(N) 必须另从干净档验证。若调试使 C 下降，不回滚既有随机结果，待发量取 max(B-R,0)。

### 报告镜像与母舰损毁

有效 Mother 完成同步后，六层数和 R 镜像到 country 同名变量；country 保存 `eep_component_entitled`（应得 B）、`eep_component_pending`（待发 P=max(B-R,0)）。country 的 `eep_component_snapshot_state` 为 0＝本次有效母舰、1＝母舰不可用但有历史快照、2＝尚无有效快照；只有真实读取母舰后才设置 `eep_component_snapshot_available` flag。缺失镜像初值为 0，不声称实际装备了零级核心。

母舰被毁／不归属时保留最后确认的六层数和 R，更新 B/P，但停止发放。报告将六层数明确标为“最近确认记录”，文字说明母舰不可用时保留历史记录且欠额未兑现；不以历史计数宣称仍有实物，不将奖励发给普通舰队，不复活。报告只是读 country 镜像，不触发抽取；本地化线程把独立 `eep_component_report` 插入现有报告。状态变量供后续条件化文本使用，当前报告无需暴露内部数值状态。

### 原生刷新与验收

本机 Stellaris 4.5.2 `common/defines/00_defines.txt:574` 明确 `TRIGGERED_MODIFIER_UPDATE_DELAY = 5`，即每个对象的 triggered modifier 每五日更新。安装后与每次变量变更后至少等五日再判断；RC3实际采用六日步长（hw0 2200.01.07、hw1 01.13，后续hw2再六日），取代早期30日组合夹具计划。一天无增益不足以否定本路线。组件文档明确 triggered_ship_modifier 不在设计器展示，因此 tooltip 缺失也不是失败；必须核对真实 slot 装备、原生 ship 总修正及实际属性。

先在 C0（B0，无随机发放）保持另外五核心零层，按 shield0→1→2→reload 检验实际盾增量，保存原生档和 SHA；负面对照为其它舰队，以及拆件／回退层数。通过后再从自然计数档覆盖 C49→50、99→100、C10000（200次），同日重复、保存重载不重复；另用大于200待补值确认分批兑现、无总上限，以及母舰消失不发奖。所有 P 候选先 open_kaishek 解析和整包门禁，本子任务仅提交静态证据，原生结论仍由主任务采集后回写。

### 候选实施与静态结果

六核心、六 script value 和持久 RNG 已按上述设计实施。三个 P 文件通过当前 open_kaishek CLI 保真解析，依次为 effects 8271 bytes／2498 tokens／135 blocks、components 3426／1028／36、values 1409／394／18；均 roundTrip=true、0 diagnostics。实际源结构检查确认六个同权重分支、每次仅一层数与总数各加一、预算减一并清除、只初始化缺失层数、六个正确归属过滤、零奖励 add_modifier（仅原有基础成长一处）。证据和准确源码 SHA 存在 [静态记录](evolution-components-1019-static.json) 的 `six_dynamic_core_candidate`，上方旧单核心记录明确保留为历史。

独立作者 JSON 已更新简中／英／德各19键（六组件各名称／描述／别名，加只读报告）；三语键集与受保护引用 token 一致，英德未发现简中占位。其余七语和所有 YML 由本地化线程集成；非中文运行时不在范围内。该结果只证明源结构与静态语法，不证明实际装备、随机引擎语义或动态属性生效；整包门禁与简中原生硬件／RNG测试仍由主任务执行。

主任务审查要求在最终冻结前把产品文案与开发状态分开：游戏中六核心描述只介绍目标机制、每层数值与不额外消耗供能／维护，不出现“实验／原生／待实机确认”；报告保留 B/R/P 与六层数，称大量积压“分批补发”，不暴露200次工作预算和同步实现。母舰不可用保留历史且停止升级的说明保留。此为候选机制文案，不是测试通过声明；开发待验状态仍以本文和静态证据为准，不降低发布门禁。

## RC3动态硬件一级原生成功（后续仍待验）

RC3生产树冻结 SHA `178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116`，先通过open_kaishek 36P／131键／独立CSV／3派生回调门禁。开发检查点为 `2e020d137`；本节更新不修改冻结生产树，也不改写历史观察JSON。

主线程在机器开局的受控C0／L0／R0夹具中，保持其它五核心为0。零级基线hw0（2200.01.07）最大盾167310；一级hw1（01.13，经过六日）最大盾171492.75，增加4182.75。ship scope导出的核心script value为1、`ship_shield_mult`为3.1，未增加普通奖励modifier，普通控制舰没有同期变化。此证据支持实际装备核心的tier0→1动态属性已生效；hw2与同日重载仍待主线程完成，不能写六类核心／随机发放全部通过。

早期诊断误用 `every_ship` 没有获得有效ship导出，之后改为本机原生支持的 `every_owned_ship`，在Mother fleet内进入真正ship scope导出。诊断命令失败不能被归因为组件倍率失败；无导出值也不等于导出值为0。

### 设计层与舰船层的独立原始依据

以下事实直接来自本机4.5.2原版文件，而非按hw1结果倒推参数：

- `common/component_templates/000_documentation.txt:12-18` 分开说明 `modifier` 影响设计器数值、`ship_modifier` 影响实际舰船、`triggered_ship_modifier` 在ship scope；:24进一步把 `triggered_ship_design_modifier` 明确区分为design scope。
- `00_utilities_shields.txt:906-907` 的 `LARGE_DARK_MATTER_DEFLECTOR` 在 `modifier` 中给出 `ship_shield_add=@shield_L6`；`common/scripted_variables/02_scripted_variables_component_cost.txt:389` 定义 `@shield_L6=2925`。11件原始盾合计32175。
- `00_utilities_aux.txt:99-100` 的 `SHIELD_BOOSTER` 把 `ship_shield_mult=0.1` 放在设计层 `modifier`；本设计真实装备三份。
- 同一原版文件:439-441的 `CRADLE_MARK` 把相同 `ship_shield_mult=0.10` 放在 `ship_modifier`。这是原版自身使用同一属性的两条不同修正管道，独立支持分层理解；无需用第三方讨论冒充引擎公式。

原始文件证明了字段、数值和修正层归属，但没有公开闭源引擎的完整计算函数。因此乘法顺序作为“源分层推导，并由原生导出／实际值验证”的模型，而非声称读到引擎实现：本设计盾值为 `32175 × (1+3×0.1) × (1+ship层总修正)`。hw0的ship层3.0给出167310，hw1的3.1给出171492.75，均一致；在查看hw2前该模型预测tier2／ship层3.2为175675.5。实际hw2和reload必须独立核对，不硬凑预测。每层组件声明的+10%是该层修正增量，不是相对当前面板总值+10%。

## 六频道源数据预期（生成证据前范围）

下一阶段从干净fmm00做自然成长边界，拟覆盖C=0／9／10／19／20／49／50／200／10000，必要时20500验证200次工作预算的补差。本子任务在读取这些未来成长SAV前固定原版及RC3源码的独立预期，新增 `evidence/1019-analysis/six-core-source-expectations-v1.json`，不改生产Mod或其它验收报告。

预期范围包括舰体／装甲／护盾的设计层基值与ship层修正、武器伤害、索敌、舰体／装甲固定日恢复；逐项记录实际原始文件、行号、SHA、RC3固定装备对来源的贡献，以及可在一次Mother fleet的 `every_owned_ship` 内导出的确切modifier键。等级贡献用L=floor(C/10)，随机核心贡献用实际持久六层数N表示，不能预先猜测随机分布；外部科技、领袖、帝国或临时修正明确作为额外项，避免把特定新局的未知来源当成固定常数。源参数与已知层次支持的预测和仍待原生确认的计算部分分开标注，不按未来SAV调参。

预期证据现已生成：[六核心源预期](evidence/1019-analysis/six-core-source-expectations-v1.json)。直接读取RC3不可变snapshot，六份Mod源SHA与manifest逐项一致；固定设计56件（含required）／22种实际组件定义均已追溯，未来自然C档未读取。无外部加成时，三个最大值模型为 `H=30000×(3.132+0.05L+0.10Nh)`、`A=25740×(1.74+0.05L+0.10Na)`、`S=41827.5×(4+0.05L+0.10Ns)`。每级增量为H1500／A1287／S2091.375；相应核心每层增量为H3000／A2574／S4182.75。这些是源固定参数的可检验预测，其余频道仍须原生验证。

伤害修正预期 `3.8+0.05L+0.05Nd`，索敌修正 `15+3Nt`（SENSOR4的本地原版 `@hit4=15`），固定日恢复为舰体 `1.392+0.1L+0.2Nr`、装甲 `2.088+0.1L+0.2Nr`，均另加真实外部项。两个AUTO_REPAIR只在设计层提供独立的百分比恢复字段，合计hull `ship_hull_regen_add_perc=0.10`、armor `ship_armor_regen_add_perc=0.20`；不能把这些百分比填进固定恢复预期，也不能以满血时实际恢复0否定固定字段生效。伤害修正不是面板DPS，索敌修正也不是每门武器的最终有效索敌。

JSON包含一次country→绑定Mother fleet→`every_owned_ship` 导出十个关键字段的完整effect片段，另给五个百分比／恢复倍率／索敌倍率的可选分离字段；所有键均核对原生modifiers.log，export effect支持ship scope。超额C20500从R200开始时，B410，第一调用最多发200至R400／P10，后续调用再发10至R410／P0；这证明设计没有总200上限，原生结果仍需保存验证。

硬件后续状态：验收线程已完成hw2与同日reload限定检查，最大盾依次167310→171492.75→175675.5→175675.5，实际script value和ship盾倍率为1／3.1、2／3.2、重载后2／3.2；见 [RC3硬件v2报告](evidence/1019-analysis/rc3-hardware-case-report-v2.json)。这仅是硬件限定范围PASS_SCOPED；严格整档重载差异仍保留FAIL，不将其写成全量字节／业务字段完全一致，也不代替自然RNG或其它五核心验收。

### 源预期v2适用说明（生成前设计）

主线程在尚未取得自然C0伤害aggregate前，指出当前Machine预设的原版 `civic_machine_terminator` 另有country级 `ship_weapon_damage=0.25`。v1已把3.8标为“无外部项”的母舰专属来源，但该参考项不能直接当本预设实际绝对值。保留v1原始字节，新增 `six-core-source-expectations-v2.json` 专门记录已知country项、剩余供能来源及模型边界；不修改冻结Mod，不读取未来自然成长SAV。

v2优先推荐先以真实C0原生aggregate建立固定对照，再验证由源码事先确定的增量：伤害 `Δ=0.05ΔL+0.05ΔNd`，索敌 `Δ=3ΔNt`，固定日恢复各 `Δ=0.1ΔL+0.2ΔNr`。前提是其它帝国／科技／领袖／临时修正及实际装备保持稳定，经过至少五日刷新；不能用未来随机结果调整这些系数。三防设计基值可沿用既有源与护盾硬件证据，但跨不同政体或新外部加成时仍须重新检查baseline。

[源预期v2适用说明](evidence/1019-analysis/six-core-source-expectations-v2.json)已生成，v1 SHA仍为 `bd3b4d48eeb5de98b34a8ba104f55c23f17cb43a723a216934f2c2a1c4a2099f`，未改字节。原版 `02_gestalt_civics.txt:1593` 给机器灭绝政体伤害+0.25，因此母舰来源3.8加此已知country来源的阶段小计为4.05，仍不是完整实际aggregate承诺。同文件:266-268的吞噬蜂巢另有舰体+0.25和舰体／装甲百分比恢复各+0.05；普通 `00_civics.txt:1720` 洁癖政体给的是射速+0.33，不能混作伤害+0.33。这些按实际启用政体分别应用，不同时叠加到机器预设。

剩余供能也有直接原版来源：`common/static_modifiers/02_static_modifiers.txt:985-989` 的 `ship_excess_power` 给伤害、速度倍率、闪避倍率各0.1；`common/defines/00_defines.txt:1838-1839` 以MAX=1.0／MIN=0.05控制其按剩余供能缩放，注释明确缩放named modifier。它是独立命名来源，但“独立来源”不能直接推成“独立乘区”；公开脚本没有给出引擎计算函数，也不足以认定ship导出是否包含完整供能项。v2保留此归属待C0诊断确认，不套用二手Wiki公式或用未来层数结果回算供能系数。

六核心各层功耗均固定为0，成长只改变属性修正而不改固定设计、反应堆或组件功耗。因此在其它条件固定时可以用真实C0导出作截距，事先固定的L/N增量仍保持；不把一个无法归因的C0残差命名为“测得的供能加成”。v2没有读取自然成长C0或后续伤害导出，不宣称新的频道实机通过。
