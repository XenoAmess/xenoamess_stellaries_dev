# 1019 巨像原生接口与共同结算审查

## 目标与范围（实施前）

审查 0.4.0 候选的母舰原生 planet_killer 组件、目标规则、完成回调，以及普通殖民拆解与巨像共享的收益结算。目标是完整原生充能发射后，允许无需陆军消灭敌国天然殖民星并把收益交给发射国母星；本国合资格非核心殖民星也可使用。

本轮仅修改巨像专属 scripted effects、trigger、event、component，以及共同 settlement effect。主线程独占桌面、游戏和运行时验收；本审查不启动游戏，不以直接调用事件冒充原生发射。

## 设计方案

1. 对照本机精确 4.5.2 原生 planet killer 组件、weapon CSV、目标规则、on_action 和引擎自动生成文档，确认字段与作用域；区分已查证的原生接口与仍需实测的底盘支持。
2. 发射完成重新核验发射国、母星所有权、战争和目标类型；共享结算使用显式受益国绑定，不向敌方星主发放收益。
3. 复核有效规模 q、C/G/D、普通材料造人、原生噬岩者分支、危机目标与持久防重复标记。普通 situation 拆解的种子及工期保留。
4. 如修复需要超出独占文件，先告知主线程，避免并发覆盖。本地化只通过独立 authored JSON 交付。

## 验收标准

- 修改候选先通过 open_kaishek；静态通过只证明该工具覆盖的语法和结构。
- 原生接口结论包含本机源码/自动生成文档的具体证据位置。实际充能、取消、战争结束/母星丢失、完整发射、敌星销毁、收益归属、重复回调与重载由主线程简中实机确认。
- 普通殖民拆解与巨像 C/G/D、人口和容量口径一致；原生噬岩者不再叠加普通材料造人；不返还敌国人口。
- 未做的实机项目明确保留为待验收，不能宣告功能已通过。

## 调查与实施记录

- 2026-10-19：已读取任务需求与仓库规则，开始只读代码和本机原生脚本审查。
- 本机 `common/on_actions/01_planet_destruction.txt:1`、`common/scripted_triggers/01_scripted_triggers_planet_killers.txt:1` 均明确 THIS/ROOT 是被击星球，FROM 是发射舰队。`carrier_event` 与 planet/Carrier trigger 的入口方向一致；未接 queued/unqueued 回调，取消不结算。
- 本机 `common/component_templates/weapon_components.csv:194` 的原生碎星炮行包含 min_windup=90、cooldown=30；专用 TXT 只有类型和图形，不能拿它作为数值完整的证据。原生 `mutation_weapon_components.csv` 提供独立 CSV 的已存在例子。本轮新增仅含专属键的 `eep_weapon_components.csv`，保留90/30；采用原生 `PLANET_KILLER_MAW` 行已有的 power=0。主线程已确认，这是开局母舰自带能力，避免标准巨像的 -7500 供能拖垮既有战斗配置。完整90/30流程及独立CSV加载仍须实机确认。
- 目标有效规模门槛复用本项目已经实机调查的 `planet_size > value:eep_damage_count`，证据见 `implementation-test-release-2026-10-06.md:639`；不以空闲区划数替代物理尺寸减旧损耗。
- 本机 `events/nemesis_crisis_menace_objective_events.txt:155` 的 crisis.5015 在毁星目标之外，对星主无其它殖民星时还发 `crisobj_destroy_empires`。本轮只在既有防重块中，为敌国最后殖民星补同条件；本国普通拆解不发灭国奖励。
- 静态工具边界：最初审查时 open_kaishek 包入口不扫描 CSV；已告知主线程，并暂停新增候选验收。随后工具负责人在 open_kaishek 提交并推送 `d5e61a9` 补CSV合同、`45cc68d` 记录目标包证据：工具全量离线验收PASS，目标包CSV files=1、keys=1、errors=[]，整包静态PASS。该结果不替代真实完整发射；最终冻结包由主线程再次执行门禁。
- 已实施：专属CSV、q>0目标门槛与共享结算护栏、敌国最后殖民星原生灭国目标、销毁后清理巨像临时标记。已有发射国显式绑定、敌国人口不返还、噬岩者随机新人口直接进入发射国母星保持不变。普通拆解仍调用原 situation 的种子和工期，未修改普通入口封装。
- 作用域证据：本次自动生成 `effects.log:432` 确认 destroy_colony 支持 planet/ship/colony，`triggers.log:992` 确认 has_planet_flag 在 colony/Carrier/ship 读取载体标记，`scopes.log:22` 确认 planet 可从 planet/ship/colony 跳转。本轮没有把 CK3 方言假设当作 Stellaris 证据。
- 底盘风险：原生 colossus/toxic_god/star_eater 均为 shipclass_military_special，juggernaut 为 shipclass_starbase；未查到可声明的 planet-killer 开关。原生毒圣有普通军事单位加巨像槽的先例，但不能据此断言移动星堡类主宰也能使用命令。须通过真实UI和存档证明。
- 十语言目标提示交付至 `localization/colossus-1019-authored.json`，只覆盖既有 eep_colossus_target_required，由本地化负责人集成；非中文运行时不在范围内。
- 危机实存字段调查：既有原生 [第四次吞噬后存档](evidence/priority-terravore-progress-2026-10-09/native-fourth-settlement-C60-and-crisis2-notices/terravore-fourth-devour-final-settlement-date.sav)（meta为Cygnus v4.5.2、2278.10.02，SHA256 `7e13a140ff372bb916ac3e06f97c6dfe2bdc32a7439fe76e669f2360a2c9f939`）的 country0.crisis_progression 使用重复 objective 块，块内 `objective="crisobj_destroy_worlds" progress=1500`。另一份 [stage4原生档](evidence/runtime-development/20261007T100241Z/rc4-native-stage4-queen-confirmed.sav)（4.5.2、2296.03.02，SHA256 `67239321c3e20d85b0d32b7cc9122f763b04782e337ef46a34f7ead23f894b9e`）对应毁星2250、灭国550。progress是目标累积奖励点而非完成次数；`common/crisis_objectives/00_crisis_objectives.txt:73` 的毁星奖励受星系数/宜居倍率影响，灭国奖励受现存可玩国家数量影响。已交给只读checker负责人按真实重复块提取，不能用Mod防重flag代替原生进度。SAV meta版本标签本身不证明EXE SHA。

## 主线程简中实机步骤（工具修复通过后）

1. 冻结带专属CSV的新快照。记录 package PASS、生产树SHA、EXE SHA；旧缺CSV快照只可用于其它接口调查，不能用作本功能验收。
2. 独立功能夹具保存母舰、母星、敌国目标星、C/G/D/made/worlds、人口与危机进度基线。确认母舰实际存档设计含专属组件，UI有巨像指令；允许用 `valid_planet_killer_target` 和 `has_fleet_order` 作只读观察，不直接调用完成事件作为发射证据。
3. 真实原生下令后保留 windup/fire 两阶段动作和截图/存档；充能/发射中C/G/D不变。取消一次，推进日期后仍无收益；再完整发射，目标变pc_shattered且殖民地销毁。核对发射国母星收益，敌方C/G/D与人口不获奖励，无陆军或占领要求。
4. 普通材料差值：q=尺寸-旧噬岩损耗；C增加q，G增加q，D=2+floor(C/4)，制造总额为100*floor(G/6)，只发制造总额与历史made的差值。自有源星返还合格本族人口，敌国源星返还0。噬岩者C增加q但G不增加，新人口只来自原生随机分支并直接进母星。
5. 最后一颗敌国殖民星使毁星与灭国原生危机目标各完成一次。重复回调/同日保存重载后q、C/G/D/made/worlds与危机进度不再变化。
6. 无效矩阵：本国/他国任何EEP核心、人工星、未殖民/殖民中、地面战斗、正在吞噬、q<=0、中立友邦。另检查发射过程战争结束、目标转让和发射国母星丢失，完成时不得收益或销毁。
7. 普通 situation 拆解回归一颗天然自有殖民星，确认种子与工期保留、正常收益、原生噬岩者路径与防重标记仍有效。原始SAV不编辑。

## 081638Z 原型的原生下令调查（只读）

调查源为 `C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T081638Z/pmm00.sav`，SHA256 `2fddab313229b4bddf493cb53fd484aa3897a4c7f163838188dead442ea6e6be`，日期2200.01.01。本轮只读解包，不修改原SAV、不操作UI、不修改Mod。

可作为独立战争夹具的三个真实普通AI首都：

| 原生国家引用 | 首都殖民地ID | 物理星球ID | 类型/尺寸/有效规模q | 星系ID | 星系内坐标 | 起源/性格 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 15 | pc_ocean / 19 / 19 | 0 | -15.026, 99.089 | origin_default / ruthless_capitalists |
| 16777218 | 2 | 24 | pc_tundra / 19 / 19 | 22 | 61.95055, -58.20715 | origin_common_ground / hive_mind |
| 16777219 | 3 | 39 | pc_arctic / 19 / 19 | 3 | -106.1159, -29.4602 | origin_cybernetic_creed / spiritual_seekers |

三国均type=default、各只有这一颗自有殖民星；物理星球owner/controller均对应各国，无eep_core标记，地貌实际类型列表中均无d_lithoid_devastation。country.capital记录殖民地ID，必须经过colony.carrier.reference转到物理星球；不能直接把首都1/2/3当物理星球。三颗都是最后殖民星，故成功吞噬同时覆盖原生灭国目标分支。以上是SAV事实，完整目标trigger仍须实机在战争建立后求值。

本次新运行自动生成文档确认：

```text
valid_planet_killer_target - Checks if the scoped fleet can target the given planet with its planet killer weapon
valid_planet_killer_target = <planet>
Supported Scopes: fleet

has_status = <colossus status> #charging/firing
Supported Scopes: ship fleet

queue_actions = { repeat = { <fleet actions> } }
Supported Scopes: fleet
```

`queue_actions` 文档仅给泛型。已搜索本机游戏TXT/GUI，未找到 `destroy_planet =`、`perform_jump =` 或 `jump_to =` 实例。原生 `events/000_fleet_action_examples.txt` 明列orbit_planet、move_to、wait、effect、repeat、find_closest_planet，未给毁星/主动跃迁动作参数。因此不猜测 `queue_actions` 的毁星或跃迁拼法；真正下单使用原生UI。

可复制的旧原生UI证据在 [碎星夹具目录](evidence/runtime-development/20261008T003349Z-star-cracker-completed)：选真实噬星者后右键恒星，“引爆恒星”的新鲜简中图为 `rc9-external-star-native-detonate-command.jpg`，动作文件为同前缀 `-click.action.json`。以下原生SAV均使用fleet50331809，`actions`块为空；订单写在current_order中，并非scripted fleet actions：

- `rc9-external-star-real-fire-order.sav`，SHA256 `15ca75a346082a7e9dc7ef83e85829c2a43fd7f5db43c748fcd8729384cfc1bd`：destroy_planet_order.planet=83，子订单move_to_system_point_order，尚未充能。
- `rc9-external-star-real30days-before-charge.sav`，SHA256 `255e11477967bb6e32b8bc8ca6cfbdabde0cb95ae5a0217f43d62a9714161ac0`：destroy_planet_order下windup=28、windup_time=90。
- `rc9-external-star-real91days-windup-boundary.sav`，SHA256 `6282cd430cdbfdf890af4dfefd5dcf38634ae57e5128f422b5f91bd98f169362`：windup=89/90。
- `rc9-external-star-real93days-fire-phase.sav`，SHA256 `e881d670e55f1038195bdfbf6618eac4f00ab09f652f710b253017a1b0b5bf04`：planet_killer_weapon_fire_order，fire=1、fire_time=30。

这些旧档证明90/30真实订单结构和UI下单路径，不证明本次主宰底盘可行，也不应把它们的SAV字段拼成手工订单。

### 主线程受控夹具配方

先冻结/保存基线并单列此受控功能夹具。优先使用country1：本项目既有原生 `play 1` 成功证据，而完整国家引用16777218不能直接当console play参数；既有调查中 `play 2` 才映射到16777218，见 `game-script-research-2026-10-06.md:214`，当前新运行仍须保存验证实际player.country。不要推定编码映射是通用P语言规则。

在经确认的country scope先后保存发射国和country1目标国，并用目标国 `capital_scope = { planet = { save_global_event_target_as = eep_colossus_probe_target } }` 保存物理目标。恢复实际player.country0后，以原生documented effect建立战争：

```text
declare_war = {
    target = event_target:eep_colossus_probe_victim
    attacker_war_goal = wg_cleansing
}
```

`declare_war`在本次effects.log记录为country effect，参数为target、可选name、attacker_war_goal；`wg_cleansing`在原生war_goals/00_war_goals.txt实际存在，使用cb_purification/total_war，适合当前灭绝国。先确认战争实际双方，之后才在已绑定母舰fleet scope执行documented `set_location = { target = event_target:eep_colossus_probe_target distance = 40 angle = 0 }` 作为明示的受控放置。旧firestorm夹具已证明先放在敌境再宣战会产生MIA，不能把此状态误判为巨像失效；先战争、后放舰更稳妥。放置不计作主动跃迁验收。

在fleet scope求值 `valid_planet_killer_target = event_target:eep_colossus_probe_target`，再选母舰右键物理星球15，点击本包专属巨像指令。保存新鲜UI和原生SAV，要求出现current_order.destroy_planet_order.planet=15，再真实推进并观察charging/firing及90/30子订单。取消、重下单、完成和防重复仍按前述矩阵，不能调用eep.50、destroy_colony或手写保存订单充当真实武器成功。

## 主宰UI条件、原生自有星与附属器备用设计（只读，未实施）

### 当前证据与能力边界

本机 `ship_sizes/18_juggernauts.txt:52` 是shipclass_starbase，`01_colossi.txt:26`、toxic_god及star_eater是shipclass_military_special。`section_templates/colossus.txt` 与目前母舰都使用原生invisible_planet_killer_fixed槽；组件定义均type=planet_killer。但interface的舰队GUI文件未暴露毁星按钮的脚本条件；精确EXE只读字符串可见原生CDestroyPlanetFleetOrderButton类名、can_destroy_planet_with_%s动态钩子及组件本地化报错，未找到可供脚本配置的is_planet_killer/has_planet_killer开关。没有反编译调用图或公开C++源码，不能据此判定星堡class必定被拒。现有原生真实SAV只证明star_eater底盘能下UI毁星单；母舰仍优先实际验证，不先切备用，不修改原生juggernaut class，以免破坏十移动船坞。

关于原生 `can_destroy_planet_general`：起初因其条件“不存在owner或owner hostile”提出自有星前置风险，但完整本机TXT/GUI搜索仅有自身定义，没有调用；EXE的ASCII和UTF16字符串都不存在此名，而确有can_destroy_planet_with_%s动态钩子。原生DELUGE专属trigger（同文件:423）明确有自有边境内、owner为from.owner的分支，按非水生种族/肃清政策决定资格，说明原生脚本设计允许自有殖民星。DEVOLUTION本机脚本反而限定hostile/pc_ai/primitive，不是自有星先例。故没有证据把general当作必经前置，不覆盖它，也不据其名字判自有星必定受阻。当前专属武器的自有分支先原生实测；如确有引擎限制，按主线程指示本国保留既有普通决议，优先完成敌星原生武器，不扩大对全局规则的覆盖。

### 仅在母舰真实UI失败时启用的最小备用

这是一份未实施的历史备用设计；随后真实母舰已出现专属原生UI命令，主线程明确不实现附属巨像。保留以下内容仅作为调查记录，不是当前实现计划或已发布能力。

- 每个已绑定母舰只附属一艘“解构器”，使用原生colossus船型、SHIP_COLOSSUS_SECTION固定事件设计，只有EEP_PLANET_KILLER_DEVOURER这一门武器；六大防御槽和动力采用实际合法原生组件，不增加普通武器、光环、船坞、运兵或自带其它巨像武器。原生COMBAT_COMPUTER_COLOSSUS使用colossus行为，原生colossus也被can_orbital_bombard明确排除，避免额外轰炸能力。
- 使用原生现有组件，如COLOSSUS_DARK_MATTER_REACTOR、COLOSSUS_SHIP_THRUSTER_5、JUMP_DRIVE_1、COMBAT_COMPUTER_COLOSSUS；这里记录已存在的键，最终防御配置、维护和速度须在实施前确定并验供能。原生fallen_empire NAME_Omega与事件NAME_mardak_vol_haters_colossus可作固定colossus设计格式参考；后者有重复防御槽，不能照抄其错误。
- create_fleet固定设置沿用当前母舰已有已验接口：can_upgrade=no、can_change_composition=no、can_change_leader=no、uses_naval_capacity=no、spawn_debris=no；create_ship.upgradable=no。不授予tech_colossus、AP或全帝国科技。专属组件使用不可获得的已有专属技术门槛隔离设计器；事件固定设计是否仍正常创建须实测。
- 国家在创建前先存一次性发放标记，fleet/ship持久专属标记，加全局eep_deconstructor@发放国绑定；加载或月度补同步不因为目标不存在而免费新造。副器损毁/解散不免费重生，母舰销毁也不重造母舰或副器。旧档只在母舰确实存在、仍归原国、未发副器时迁移一次，不修改SAV。
- 目标规则仅允许原来绑定母舰fleet，或本国持久绑定的唯一解构器fleet；后者仍要求母舰存在且同归发放国、核心可用、当前国家资格合法。不能因某艘普通colossus有相同组件就获得收益。主权转移、母舰丢失或国策失效立即令目标检查失败；后续月度只清理本Mod已标记的孤立副器，不误删普通巨像。
- 保留普通舰队可选操作，使用原生自动跟随移动，不以月度set_location传送模拟跟随。真实本机effects.log:1476有 `auto_follow_fleet = { target = <fleet> attack_fleet = yes }`，支持ship/fleet；原生biogenesis_crisis_events.txt:1691实际使用auto_follow_fleet追随winning_behemoth。副器采用attack_fleet=no，只在idle、非战斗、非充能/发射、没有玩家作业命令时恢复跟随。明确玩家毁星订单可优先中断跟随；queued回调可用已记录的remove_auto_move_target停止自动跟随，完成/取消后待idle再恢复，不能清玩家毁星订单。自动跟随持久化、主宰跃迁后追随和玩家命令优先级是待验接口，不把effect存在当行为通过。
- 副器原生90天充能、30天发射及eep.50共同结算不变；所有奖励仍给发射国绑定母星。不另给第二份成长、材料、危机或其它通用巨像收益。

备用验收除原有敌星武器矩阵外，增加：新局/旧档迁移/同日重载均恰一艘；普通同国及他国巨像不能使用此能力；跨星系真实跟随与玩家目标命令互不覆盖；取消后恢复跟随；副器死亡不免费重生；母舰死亡/转手或核心丢失中止资格；实际库存/维护/供能记录；母舰身份、面板、移动船坞和队列完全保留。若真实自有星受引擎限制，报告本国走普通决议，而不篡改全局规则凑通过。

### 最后敌国殖民地与回调复审

当前共享结算在destroy_colony前完成所有源owner/战争/最后殖民地判断，C/G/D与人口始终使用保存的eep_actor与eep_bound_core；敌国不回迁人口。所有危机判断和两类目标发放也在源owner清除之前；destroy_done在destroy_colony前写入。销毁后只操作仍存在的源planet标记、地貌和任务清理；返回后的母舰同步使用已保存actor，不从已经失去owner的星球找国家。未发现需要手工destroy_country的路径；不要增加此调用或另外触发crisis.5015。

原生on_colony_destroyed在owner/controller清除前触发（00_on_actions.txt:1337），on_country_destroyed的FROM是可选destroyer（:3601），该回调确实包括crisis.4020；crisis.4020对default/fallen/awakened且存在具备危机AP的FROM时发灭国奖励。因此理论上存在原生额外奖励的检查点，但不能静态断言destroy_colony会把原事件FROM舰队转成destroyer国家。原生碎星顺序本来就先crisis.5015手工发毁星/最后殖民地灭国奖励，再planet_destruction.100销毁人口/星球，是同类策略。当前eep_crisis_done只保证Mod的手工块不重入，不能证明原生总奖励恰一次；最后敌星必须比较native crisis_progression中对应objective.progress奖励点差值，并保存on_country_destroyed前后结果。未发现当前EEP on_actions订阅国家销毁或其它重复收益事件。

## 081638Z 母舰与真实噬星者原生属性对比

主线程已创建独立受控战争，`pkbefore.sav`（2200.01.06，SHA256 `981ae76af169bfba18c27aeb95cfcc6c5750096c5debe2637cfe3dc074738566`）中country0与country1处于cleansing战争，母舰fleet138/ship808位于目标planet15所在system0，并与fleet4/5/6/7真实交战。本分支只读对比该档与既有真实噬星者档，没有操作桌面或更改SAV。

| 原生字段 | 母舰pkbefore | 旧噬星者准备档 | 旧噬星者真实28/90充能档 |
| --- | --- | --- | --- |
| fleet.ship_class | shipclass_starbase | shipclass_military_special | shipclass_military_special |
| properties.weapon/mobile/valid_for_combat | 均yes | 均yes | 均yes |
| properties.station | yes | 无 | 无 |
| properties.planet_killer | 无 | 无 | 无 |
| 实际ship.section.weapon巨像项 | index101，EEP_PLANET_KILLER_DEVOURER，PLANET_KILLER_GUN_01 | index0，PLANET_KILLER_STAR_CRACKER，同槽名 | 同准备档 |
| 订单/状态 | 当前战斗，尚未下毁星单 | idle，无毁星单 | destroy_planet_order→planet_killer_weapon_windup_order，28/90 |

母舰专用武器存在于实际ship.section.weapon实现中，已经超出“只有设计树里写了组件”的证据。旧噬星者在准备和真实充能时也没有planet_killer属性，所以不能以缺这个字段判母舰武器未注册。class/station不同是事实，并非由此得出能力禁用。

已只读查看主线程新鲜 `pk-probe-v2-native-planet-menu.jpg`：选中白骑母舰后右键伊巴尔主星，原生菜单确实提供可点的 `EEP_PLANET_KILLER_DEVOURER_ACTION 伊巴尔主星` 和“进入轨道”。原型rc1b缺该命令译键是已知问题，主线程已在下一候选修复。这个画面直接证明移动星堡类母舰可以获得专属native planet-killer菜单，不需要附属巨像，也不需要改原生juggernaut class。当前证据仍只是UI命令出现；实际下单、90/30两阶段、收益、毁星与防重由主线程继续验收，不提前宣称完整武器成功。

## 原生巨像派生回调补齐（实施前）

真实点击原生命令后，081638Z已正常停止运行的原始 `logs/error.log:52` 在17:05:52记录 `Could not find on action 'on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER_queued'`。整份停止后原始日志SHA256为 `1673e693de7b058ff9476e6dee39f332ab9dac8a9b3d97452ff8affef41fb147`；stop.json确认2026-10-19 09:08:33 UTC自然退出、forced=false、running_after=false。这是实际下令暴露的生产回调遗漏，与此前控制台WrongScope失败分开记录；真实pkqueued订单存在不等于已经发射。

目标是补齐引擎隐式排队/撤单回调，消除这两类缺名错误，同时保证排队或取消不支付任何收益。范围仅 `mod/common/on_actions/eep_on_actions.txt` 新增两个专属空定义，现有块不改；已冻结rc2包不变，修复进入下一候选。

原生依据：`common/on_actions/01_planet_destruction.txt:10-12`明确queued在下令时触发，即使原队列为空；unqueued在充能期间取消也触发，作用域同完成。原生CRACKER完整三回调位于:14/:27/:33，其中unqueued为空；DEVOLUTION与MAW同样声明空queued和空unqueued。全本机on_actions搜索没有这个族的_once/_fired派生命名，精确EXE存在on_destroy_planet_with_基础前缀；目前有依据的三个名字是：

```text
on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER
on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER_queued
on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER_unqueued
```

设计：只有无后缀完成回调继续触发eep.50；两个派生回调均为空，不调用事件、共同结算或原生碎星奖励。验收：修复文件先过Kaishek语法检查，工具负责人补回调完整性合同后重新跑完整包；最终新候选真实下令/取消/重新下令/90+30完成分别查日志与C/G/D，确保排队/取消无收益、完成只支付一次。静态通过不能替代这些实机行为。

已实施仅两个空派生定义和一行用途注释，原有完成事件及其它块保持。open_kaishek CLI对该文件返回exit0、PARSED、470 bytes、136 tokens、12 blocks、diagnostics=[]、roundTrip=true。完整包的新增回调合同由工具负责人先修复验证并提交推送，之后主线程再冻结执行；本分支没有把单文件解析或旧rc2包当修复后的实机通过。

## RC3 实际时长失败与RC4最小数值修复

RC3真实下令后仅6日目标已毁，不能通过90/30要求；详见 [时长与载入调查](colossus-pk-duration-loader-1019.md)。此前独立CSV格式正确的静态结论不证明该文件名被native载入。已按主线程授权把专属武器数值改为有现代作者真实PK原文支持的TXT内联：power0、零damage、windup90/90、total_fire_time30、range0/accuracy1/tracking0，并删除专属CSV，不覆盖任何原版表。只改专属组件的数值来源，结算/回调/目标规则不变。新TXT SHA256 `0bf1314f69f410ffcbf14875680d2689453295ee317b16d47ae219920b62dd92`，单文件lossless解析通过；完整包新gate和RC4实际windup_time90/fire_time30及完整完成仍待验，原失败快照不改。
