# Stellaris 4.5.2 吞星、区划、灵飞与武灾代码研究

日期：2026-10-06。方法：只读本机游戏文件，结合仓库既有研究，并核对 Paradox 官方公告。未运行游戏或 Mod 验收。

本研究为[设计案](../../docs/eat-everything-origin-design-2026-10-06.md)提供 Stellaris 专有事实，不从 CK3 文档推导 Stellaris 接口。文件路径均相对游戏根目录 `C:\SteamLibrary\steamapps\common\Stellaris`，行号只适用于本次指纹。

## 1. 环境和证据

`launcher-settings.json` 报告 `Cygnus v4.5.2 (9776)`、`rawVersion=v4.5.2`、兼容标识 `4.5`。EXE SHA-256 为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。版本字符串和校验和来自本地安装，不是新开局的运行时确认。

Steam 的库配置将 281990 指向 `C:\SteamLibrary`；旧研究中 C 盘 Program Files 路径和 4.5.1 不适用于这台机器。完整文件大小、SHA-256 和关键定义行号见[基线 JSON](evidence/game-script-baseline-2026-10-06.json)。没有把完整游戏源码复制进仓库。

本轮没有读取实际 DLC 启用播放集，`has_shroud_dlc` / `has_nemesis` 分支存在只说明脚本条件，不能证明用户拥有、此次启用了 DLC 或某组合已经成功加载。

## 2. 可追溯的源码结论

| ID | 文件与定位 | 源码可确认的事实 | 对本案的影响与边界 |
| --- | --- | --- | --- |
| SRC-01 | `common/governments/civics/02_gestalt_civics.txt:227`；`common/scripted_triggers/00_scripted_triggers.txt:1397` | 噬岩者为有效吞噬蜂群＋石质主体的组合，国策有石质显示换名，并不是独立国策键 | 用实际底层键判断；非石质蜂群需要自己的吞星适配 |
| SRC-02 | `common/governments/civics/02_gestalt_civics.txt:1554`；`common/governments/civics/00_civics.txt:1658` | 铁心属机械智能；种族洁癖要求极端排外及军国/唯心之一，排斥格式塔与公司，均不可普通改换 | 不靠起源绕过国策原限制；铁心国策排斥虚境铸造起源 |
| SRC-03 | `common/scripted_triggers/00_scripted_triggers.txt:2284`；`common/governments/civics/00_civics.txt:4162`；`common/governments/civics/02_gestalt_civics.txt:1330` | `is_homicidal` 有三个传统国策、两个 Infernals 焦土国策及 `menp_behemoth_ever_hungry` | 「所有灭绝」应拆开局国策与后期 perk，焦土需要额外区划/经济兼容，不盲用宽触发器 |
| SRC-04 | `common/decisions/02_special_decisions.txt:1704` | 原版吞岩决议只面向噬岩、非游牧、可有适居地貌、非首都、未在被吞噬状态且非纳米殖民规划的星球 | 原版按钮不能直接让铁心/洁癖吞星；不能写成「任意天体都能吃」 |
| SRC-05 | 同文件 `:1741` 起 | 启动时导出物理 `planet_size`，减去 `d_lithoid_devastation` 障碍数，保存 `num_districts_terravore` 并在国家启动目标局势 | 奖励快照区分物理尺寸、旧损毁、区划总容量与已建数量；中断重启不能重新算已吃空间 |
| SRC-06 | `common/situations/02_strategic_situations.txt:833`；`common/script_values/00_script_values.txt:2463` | 局势终点为 1000；月进度表达式是 `1000/(6×N)`；月入口为 `colony.190`，完整入口为 `colony.185`；失去目标所有权中止 | N=20 的理论进度耗时为 120 月；不是六个月吃完一个世界。真实月份边界仍需实机 |
| SRC-07 | `common/scripted_effects/00_scripted_effects.txt:8508` | `consume_world` 先按权重删除一种已建原版区划；有至少两格自由容量时三个奖励分支基础权重均为 10：本族人口、矿物或合金，同时增加两个损毁障碍与破坏度；剩不到两格走矿物分支 | 新容量不等于自动搬运源星已有建筑；人口非保证收益。资源分支按本国月产出及原版 min/max 计算，不能当固定月产出 |
| SRC-08 | 同文件 `:8547`、`:8669` 起；`events/colony_events_1.txt:4623` | 原版人口分支 `create_pop_group` 没显式 size；AI 另有搬运 AMOUNT=100；每次消费末尾设 `recently_eaten_planet` 为 360 日，入口也设同名旗标 | 注释「每六个月」与当前一年旗标不同，未运行前不下定论。也不把缺省创建大小自动断言为已验证的 100 |
| SRC-09 | `events/colony_events_1.txt:4552` | 结束事件先补消费余下自由格，迁走所有正数量人口组至当前首都，`destroy_colony` 后 `change_pc=pc_shattered` 并清地貌；选项在有武灾 AP 时完成摧毁世界目标 | 母星迁都与外族肃清需新合同；不在自己的完成和原版选项两处重复算天灾目标 |
| SRC-10 | `common/deposits/01_blocker_deposits.txt:1538` | 每个损毁障碍有 `planet_max_districts_add=-1` 和 `pop_environment_tolerance=-0.1`；原噬岩者不能清除 | 给母星扩容可用真实区划容量修正；旧障碍并非单纯美术图标 |
| SRC-11 | `common/static_modifiers/00_static_modifiers.txt:629`；`common/static_modifiers/02_static_modifiers.txt:233` | 原版有 `planet_max_districts_add=2` 和 `planet_jobs_produces_mult=0.10` 的使用实例 | 确认容量与产出通道存在；动态大乘子、堆叠和实际经济均另做探针 |
| SRC-12 | `common/scripted_triggers/00_scripted_triggers.txt:4407/:4427/:4452`；`common/districts/02_rural_districts.txt:5/:122/:255` | 原资源区划用 uncapped trigger；三种 trigger 均接受 `uncapped_generator_districts`、`uncapped_mining_districts`、`uncapped_farming_districts` carrier flags，并标注 For Modders | 可在母星解地貌上限而不全局改区划；总容量、不同区划组和真实可建设性还需验证 |
| SRC-13 | `common/districts/02_rural_districts.txt:61` 起、`:86` 起；`common/scripted_variables/100_scripted_variables_zones.txt:11` | 发电区划基础造价 300 矿物、建设 240 日、维护 1 能量；给住房 200，格式塔另加 100；基础资源区划岗位常量为 200 | 新容量没有免费住房或就业；人口、劳动力和区划单位不能混用。其它区划成本按自身定义读取 |
| SRC-14 | `common/districts/00_urban_districts.txt:4`；`common/zones/00_zones.txt:186`；`common/inline_scripts/jobs/zone_researchers_add.txt:3/:251` | 城市区划声明区域槽；科研/凝聚力区域用 `triggered_district_planet_modifier` 放大普通与格式塔的三系科研岗位 | 母星扩城市区划有扩大科研的原版候选渠道，不需先造残疾研究岗位；具体蜂巢/枢纽区域与后期限制仍要探针 |
| SRC-15 | `common/zones/99_HOW_TO_ZONE.txt:51/:69` 起；`common/zone_slots/99_HOW_TO_ZONE.txt:3` 起 | README 区分区域建筑槽上限、按区划解槽、行星类别 cap、按区划等级放大修正；区域槽有自身集合与条件 | 不能用旧固定建筑槽模型直接设计大母星，也不能把多个物理区划误算成多套独立全槽 |
| SRC-16 | `common/ascension_perks/00_ascension_paths.txt:459/:566` 起；`common/scripted_triggers/00_scripted_triggers.txt:487` | 灵飞入口 potential 有 `Shadows of the Shroud` 分支支持 gestalt/machines；无 DLC 的分支排斥格式塔及机械。possible 保留互斥、AP 数量、传统树与 `trait_mechanical` 等条件 | 蜂巢/铁心灵飞不是绝对不可能，但不能赠送它或忽略模板的实际前置；机器人与机器智能的身份/底盘要区分 |
| SRC-17 | `common/ascension_perks/00_ascension_paths.txt:469` 起、`:590` 起；`common/traditions/01_psionics_shroud.txt:1` | 非合成/特殊豁免分支要 >1 个 AP，普通合成分支 >2；机器可显示为 `ap_interdimensional_processing`；灵能传统 adopt 要灵飞 AP 和灵能理论（特殊起源另有分支） | 吞星起源不与另一个原版起源叠加；机器的入口 AP 和通常时序单列，不照抄普通唯心帝国 |
| SRC-18 | `common/inline_scripts/traits/psionic_effects.txt:1` 起；`common/buildings/02_government_buildings.txt:669/:735` 起；`common/script_values/00_script_values.txt:3207/:3223` | 灵能特质对科研/凝聚力/通灵岗位有 workforce 项；灵能军团提供 200 通灵岗位，并按实际已分配通灵岗位导出灵能人口 workforce 奖励；基础为每 100 通灵劳动力 5%，另有传统/理事会条件 | 母星集中共享灵能收益有真实接口基础；空岗不能提供等同增益，也不从人口组个数算通灵收益 |
| SRC-19 | `common/pop_jobs/16_shroud_jobs.txt:2`；`common/inline_scripts/jobs/job_telepath_additional_modifiers.txt:344/:353` | 格式塔有 `telepath_drone` 且要实际灵能物种；赞主条件分支可给冶金或矿工 workforce | 不全局复制赞主效果，不承诺任何灵飞组合都让所有岗位超高效率或零成本 |
| SRC-20 | `common/ascension_perks/00_ascension_perks.txt:194` | 武灾 AP 检查 Nemesis、独立、非银河监管人/皇帝，普通配置 >2 个 AP，排斥既有玩家天灾等；开启 `nemesis_path` | 保留入口与其它天灾的互斥，不把创生天灾当矿物舰来源 |
| SRC-21 | `common/ship_sizes/20_nemesis.txt:3/:94/:189` | 三种威慑舰分别在天灾 2/3/4；基础矿物造价 300/550/900；各 `components_add_to_cost=no`，维护使用能源和矿物 | 主力矿物舰脱钩有源码依据；不是所有船只或所有设施都改为矿物 |
| SRC-22 | `common/scripted_variables/03_scripted_variables_ships.txt:65/:67/:98/:116`；`common/crisis_levels/00_crisis_levels.txt:36/:75/:115` | 三型维护能源/矿物分别 1/1、2/2、4/4；天灾 2/3/4 要 1000/2000/5000 威慑和对应升级项目 | 静态表可以手算，但超舰容、折扣、改装和实际阶段组合仍要运行验证 |
| SRC-23 | `common/on_actions/00_on_actions.txt:1337/:3442`；`events/colony_events_2.txt:1421` | 通用殖民地销毁入口是 Carrier，在 owner/controller 清除前调用；迁都入口 THIS 新殖民地、FROM 旧殖民地（初设可能无 FROM） | 不把这个通用入口当严格噬岩完成后回调，也不以 CK3 作用域经验臆造星球钩子 |
| SRC-24 | `events/shroud_events.txt:12039/:12050`；`common/scripted_effects/00_scripted_effects.txt:8969` | 原版有指定 `size`、`species=owner.owner_main_species` 的造人口实例；`kill_single_pop` 显式操作 100 人口量 | 通用路径可优先验证同类造人口渠道，不用旧 `create_pop` 或把一个组当一个单位 |

## 3. 特别容易误读的地方

原版吞岩人口不是直接从敌人复制。本族人口分支使用局势所有者的主体物种，在被吞星球上生成；结束再搬去首都。原版还搬运所有残留人口组，所以本起源需要明确保留本族模板、等待外族肃清和固定母星，而不是无条件复用全部末次逻辑。

原版 `consume_world` 的少于两格分支没有「一定还剩一格」的显式零格 guard。如果专用局势完成后卡在等待肃清/母星恢复，却继续调用原版月度消费入口，可能错误地产生新损毁或奖励；实施必须冻结月度消费，并用实际剩余容量和状态守卫。此处是根据分支推导的风险，尚未复现。

`planet_max_districts_add` 改的是容量；`district_mining` 等还有地貌/区划组限制。资源区划的 uncapped carrier flag 不创造已经建设好的矿区，也不会自动把人口配置到矿工。城市区划、区域岗位和建筑槽上限也不是同一个数量。

灵能军团的基础 workforce 并非无限：常规建筑数量受原版限制，基础通灵岗位 200 对应的脚本基础增益为 10%，还要真实填岗并计入传统、理事会和赞主等其它项。是否能通过原版合法组合进一步放大，以及增加投入后的净收益，必须按实际配置验证；本起源不能凭「超高岗效」四字宣布单星后期已经无限强。

当前源码对原生 `trait_mechanical` 仍有灵飞 possible 限制，而机械智能入口可以通过 Shroud DLC 分支出现；这不是互相矛盾，机器智能 `trait_machine_unit` 与机器人底盘不应混为一谈。铁心测试必须从合法机器智能模板开局，不能拿造出来的普通机器人模板替代它。

## 4. 外部官方对照

[Paradox 官方发布公告及 4.1 Lyra 更新说明](https://store.steampowered.com/news/posts/?appids=281990&enddate=1759180360&feed=steam_community_announcements)列出蜂巢/机械灵能飞升和新人口/区划 UI。该资料只用于确认改版背景，当前 AP 门槛、舰船造价与区划接口均以本机 4.5.2 文件为准。旧 2022 年飞升重做说明或主机 Wiki 不能覆盖当前 PC 分支。

## 5. 工具现状与未验证事项

只读查看 `D:\workspace\open_kaishek/README.md`、`docs/stellaris-4.4.6-profile.md` 和文件列表，本地 HEAD 为 `890b32d`，README 当前声明受限 Stellaris 4.4.6 静态 profile；未发现 `accept_stellaris_mod.py`。这不是已经执行后得到的工具失败，也不是对远端最新版能力的判断。未来验收先同步核对该工具，再补齐真实缺失能力；不跳过、不冒用旧报告。

待验证：本机 DLC 实际状态、起源选择器资格、决议单键覆写优先级、国家→局势→目标作用域、动态容量乘子、旗标在各区划组的效果、造人口缺省 size 与模板权利、消化站搬运费用和原版迁移系统、末次补消费/销毁/天灾计数顺序、母星失守和重载恢复、超大行星 UI/经济/性能、灵飞与武灾实际组合。

本轮确定的是 Stellaris 的特定脚本定义和设计依据，没有新增 CK3/Paradox 共通语法结论。全部游戏内问题仍在[后续验收设计](acceptance-plan.md)中保持未执行。
