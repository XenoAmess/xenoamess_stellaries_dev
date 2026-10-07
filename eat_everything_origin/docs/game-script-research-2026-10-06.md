# Stellaris 4.5.2 吞星、区划、灵飞与武灾代码研究

## 2026-10-08：焦土蜂巢的合法蜂巢世界与轰炸条件

本机`common/ascension_perks/00_ascension_perks.txt:2227`的ap_hive_worlds要求蜂巢、非游牧、非石质噬岩蜂巢且非荒野；possible要求tech_climate_restoration及至少两个已有飞升天赋。焦土蜂巢并未在此被禁止，不能把石质噬岩蜂巢的禁止条件套用给它。`common/terraform/02_special_terraform_links.txt:6083`附近的pc_volcanic→pc_hive链接要求owner有ap_hive_worlds，condition为tech_volcanic_terraforming；此文件的hiveCost=10000能源、hiveTime=7200日。实际自然焦土蜂巢2297.03.12保存中已研究tech_climate_restoration与tech_volcanic_terraforming，已有四个AP，扩张传统尚差一项；后续须通过实际传统／AP界面及付费改造取证，不能用受控改星球类型代替合法完成。

原版`events/infernals_1_events.txt:147`的infernals.20为每日on_planet_bombarded的Carrier事件，只在烈焰风暴立场且毁灭度<100时给实际在轨焦土帝国舰队的owner凝聚奖励，按真实fleet_size计。此原生轰炸收益与EEP吞星结算应分开检查，不要求合法轰炸的所有库存都固定来证明没有EEP发奖。Native脚本文档effects.log:1900明确set_fleet_bombardment_stance为fleet作用域；不能在Planet上下文误用。infernals.30仍要求world-forger及熔炉建筑，不能冒称所有焦土蜂巢能免费火山改造。这些是Stellaris特有链接与Carrier／舰队事实，不推广CK3。

## 2026-10-08：非本起源原生局势进度的实际精度

172235离线简中、origin_default的Q20通过原生决议开始，2200.01.02保存87724df…中situation_terravore_consume_planet进度0、source9.num_districts_terravore20／num_lithoid_blockers0；真实29日后2200.02.01保存92dbe853f46256a5a3c4df8d92e0a875996bc63e8c742ec8eb6be481a66a1a10实际progress与last_month_progress均8.5。官方00_script_values.txt:2463的terravore_progress是base6×target.num_districts_terravore、pow=-1、mult1000，数学表达约8.333333，但本机实际执行不能由数学浮点直接代替。原生界面也显示8.5；当前EEP生产只适配单个决议，未定义同名原生script_value或局势。后续记录117／118及119／120真实边界，并与真正无Mod环境核实；未完成无Mod积极对照前，不断言内部舍入算法或所有版本均118月。设计与验收表中的“原版120月”是制定时公式预测，尚未通过独立实测，不为凑该数字修改原生路径。这是Stellaris实际表达式执行事实，不推广CK3。

## 2026-10-08：真实AI、控制台国家引用与原生人口回迁

物种类型前提补充：同国modify_species移除trait_lithoid、添加trait_organic并实际更新主体为47后，class仍LITHOID，Native is_lithoid_devouring_swarm仍yes；移除食性特质不等于改变原生物种类型。明确create_species为MAM／有机／蜂巢并change_dominant_species change_all=yes后，实际主体48、母星6037人口量保持，Native非噬岩且EEP资格有效。此人工控制用于混合账本测试，不证明合法自然改造可把石质种族转为有机，也不推广CK3。

自然月历补充：2203.12.30实际进度47／未结算，真实一日到2204.01.01进度48／未结算，再一日到01.02结算，无额外等待月。资源完整比较发现三系库存85.2408／73.2408／91.2408归零；独立取消后真实日历保持库存且研究队列与结算分支相同，否定正常研究推进解释。随后同日以实际Situation上下文调用官方colony.190→consume_world，原生合金随机收益+100及损毁6→8时复现完全相同三系归零，研究队列不变，EEP C/G0D2未结算。此为本机4.5.2原生材料奖励的实测行为，不推断内部原因，不豁免未知差额，原始FAIL保持；本Mod保留原生收益渠道时也保留这一限制，不外推其它Paradox游戏。

154144场的SAV国家完整引用16777218存在，但console的play 16777218明确返回Invalid country ID，原玩家仍country0；不能由SAV引用存在推断玩家切换成功。实测play 2成功，后续原生保存的根player为16777218，原country0的Native is_ai条件为yes。该结论只记录这份Stellaris存档的实际映射，不外推所有国家编码或CK3。

第二受控终点试验同2200.01.04，Source为实际首都colony15，绑定母星physical8／colony0。母星实际5200→5400，国家实际人口净新增100，最终回迁账本100，G与通用制造均0；原生随机收益另有矿物400／合金500，外国完整国家和全部人口组相同。结合唯一原生人口分支、已核实AI条件和最终种子回迁100，推断新增100已由原生AI搬迁分支送绑定母星，而不是当前首都。此为明确实证推论，不称保存过原生人口分支的中间瞬间，也不把受控终点当自然48月。五轮重复请求后实际人口、库存、账本及容量保持；自然月历进度另行验证。

## 2026-10-07：母星转交与岗位修正缓存

本机官方`common/on_actions/00_on_actions.txt:3373`的`on_colony_transfer`对象为Colony，From为新owner，FromFrom为旧owner；`action.89`和`cyber.7015`用`carrier_event`处理，不使用虚构planet-owner钩子。`effects.log:549`可在物理Planet导出`planet_jobs_produces_mult`，但同日添加静态修正仍读旧缓存，必须积极对照真实次日；Colony同项读数不等于物理岗位修正。原子节的触发地貌修正在实时外国持有时仍0.10，而相同存档原字节重载后为0；原主取回、地貌重建及batch begin/end也未在真实次日恢复。原版`planetary_workshift_deployed`受控添加后真实次日物理读0.10、移除后真实次日0，原型幸福度-0.05不进入生产。rc.6将相同+0.10合同交给幂等静态`eep_court`，初始化／月度／真实转交同步，保留实体容量与王座地貌。新进程实际转交、取回和重载仍需验收；原始FAIL与INCONCLUSIVE均保留。本事实针对Stellaris 4.5.2 Carrier及其缓存，不推广为CK3语法。

## 2026-10-07 模板与国家主体引用前提

134815实际复验补充：change_dominant_species之后founder_species_ref从3321888769变为48，独立owner_main_species目标也为48；旧子模板47及外国共享组仍保留。随后EEP制造300确实使用48，原子模板100回迁保留47／原类别，外国完整国家、殖民地、人口组及共享物种块严格保持，33项范围检查通过。由此更正“founder_species_ref固定不可变”的猜测：它在本次显式国家主体变更后改变；此前单独modify_species只换境内人口而没有改变它。

本机原生effects.log:854的modify_species/change_scoped_species在country范围实际改变本国人口模板，但此夹具不更新国家主体引用：131538的母星4700已为48，国家founder_species_ref仍3321888769，按owner.owner_main_species制造的新300也为3321888769。多数人口采用的新模板不能直接等同owner_main_species；该次模板期望FAIL及原始SAV已保留，不单凭这一前提未成立的测试认定生产缺陷。

同文档:1437～1439提供country的change_dominant_species，change_all额外替换境内对应物种；原版shroud_shadows_scripted_effects.txt:95／4088把它与后续每个人口组change_species分别调用。测试62补change_dominant_species={species=新模板 change_all=no}并另在实际owner_main_species范围保存验证目标，才能证明“当前主体模板”前提。保持旧子模板及外国共享组后复测；这是Stellaris国家／模板接口事实，不外推CK3。

## 2026-10-07 首次报告决议与研究库存差异

原版免费decision_end_population_control_gestalt同源同日复现相同三系库存差额，科研队列不变；下一真实日亦未发现队列结转或新增科技。此结论只定位到决议执行路径，不认证引擎内部扣费／上限机制。官方common/button_effects/example.txt明确This为选中对象、From为玩家国，建议allow使用is_scope_type保护多面板作用域；本机fleet_view.gui使用effectbuttonType／buttonText／tooltipText／effect的实际原生接口。计划据此改只读报告入口，界面显示与库存须实机验证。open_kaishek旧入口遗漏.gui，已先修复、全量静态检查通过并推送80ec924，之后才恢复Mod验收；解析通过不等于界面运行时认证。

同一原生2283.03.03存档的简中A/B/C/D隔离：不打开母星、只打开母星及决议列表、直接诊断调用既有eep.100均保持全部库存；只有首次通过原生觐见女王决议执行后，物理研究10661.75204及工程研究5480.3411归零，社会研究37379.85079→23382.89218。科技队列、母星岗位／人口／区划及EEP经济账本保持。此为可重现运行差异，不以“原生缓存”先行解释，原始失败在082017归档中。

Stellaris原版部分决议完全省略resources块（02_special_decisions.txt的decision_reorganize_leviathan_parade，05_ancient_relics_decisions.txt的decision_baol_life_seed）；另外一些免费决议保留只有category=decisions的resources块。当前证据只支持这两种语法存在，不足以判定引擎具体扣点原因。rc.3对只读报告移除空资源表作为修复候选，包级检查及新原生首次执行均需验证；不推广为CK3或所有Paradox游戏的共同规则。

日期：2026-10-06。方法：只读本机游戏文件，结合仓库既有研究，并核对 Paradox 官方公告。未运行游戏或 Mod 验收。

本研究为[设计案](../../docs/eat-everything-origin-design-2026-10-06.md)提供 Stellaris 专有事实，不从 CK3 文档推导 Stellaris 接口。文件路径均相对游戏根目录 `C:\SteamLibrary\steamapps\common\Stellaris`，行号只适用于本次指纹。

## 2026-10-07 原生舰船建造与缓存补充

方舟对象分类不能只看名字：29_nomads_dlc_ships.txt的military_arkship_tier_3在1130行明确carries_colony=pc_ark；1252行military_arkship_champions_forge没有此声明。原版NAME_Champions_Forge_Arkship全局设计使用后者，受控resettle_pop_group可给它形成100人口舰载殖民地，但实际is_planet_class=pc_ark仍为假。验证方舟拒绝必须检查真实船型、殖民地Carrier引用及pc_ark运行触发条件，不能以名字含Arkship或已经有殖民地代替。

真实舰船设计的section内component为重复命名块，组件标量是slot和template；name.key仅为名称本地化引用，不是组件ID。巡洋舰真实LARGE_GUN_01槽对应template="LARGE_UV_LASER"。读取时须先按真实growth_stage选择阶段，再解析section／component和准确slot，不能搜索name.key或忽略多阶段结构。

4.5.2原生SAV的建造队列在`construction.queue_mgr.queues`，实际建造项目在`construction.item_mgr.items`，二者ID引用相连；不能把项目当作construction的直接子字段。驱逐舰真实三个550矿物／60基础工作项目及27日完工保留在031421原生存档，具体速度来自该局原版修正，不能把27日当全局固定工期。

原版`common/scripted_variables/03_scripted_variables_ships.txt`的护卫舰能源／矿物基值各1.0，驱逐舰各2.0（65／67／96／98行）；`20_nemesis.txt`实际船型引用这些变量。当前国家设计显示0.90／1.80已包含帝国修正，图库口径改为“当前帝国修正后的设计维护”。原始截图不修改，不把修正后的设计值称全局基础维护。

原生单舰解散会先移除舰队引用，当日国家`used_naval_capacity`及维护提示仍可保留旧缓存；本次11.12舰船已移出但舰容404，11.13真实一天后刷新396，UI404/399→396/399，剩余同型舰维护各1.82→1.80。必须核对实际对象和刷新日期，不能仅凭当日界面或缓存统计断言解散没有生效。解散前原字节重载已恢复三舰与原账本。

rc.4巡洋舰复现同一刷新行为：实际八舰7200矿物付费并完成，舰容487/480；解散50332304后同日舰队引用只剩四艘已集结、三艘增援，原对象killed=yes／fleet4294967295仍暂留，国家缓存487与维护3.44保持；真实下一日变为471/480，剩余同型舰维护3.40。全库存与EEP经济凭证保持。存档里的killed对象及当日缓存不能被计作仍实际拥有的活动舰船。

巡洋舰原版能源／矿物维护基值各4.0（同一变量文件114／116行），本局当前设计显示3.40，实际驻港1.98／离港超容3.44／低于上限刷新后3.40；三种数值必须区别标注。ship_design的船型位于匿名growth_stages条目中，实际ship_design_implementation还带growth_stage索引，不仅凭设计顶层标量查找船型。新舰可能省略original_owner，归属使用country.fleets_manager.owned_fleets的fleet引用与实际ship.fleet连接；三艘MIA增援仍由本国拥有，原生return_date及merge订单说明其状态，不能把未集结等同于未建造。以上为Stellaris 4.5.2存档与实机事实，不推广为CK3方言。

## 1. 环境和证据

`launcher-settings.json` 报告 `Cygnus v4.5.2 (9776)`、`rawVersion=v4.5.2`、兼容标识 `4.5`。EXE SHA-256 为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。版本字符串和校验和来自本地安装，不是新开局的运行时确认。

Steam 的库配置将 281990 指向 `C:\SteamLibrary`；旧研究中 C 盘 Program Files 路径和 4.5.1 不适用于这台机器。完整文件大小、SHA-256 和关键定义行号见[基线 JSON](evidence/game-script-baseline-2026-10-06.json)。没有把完整游戏源码复制进仓库。

本轮没有读取实际 DLC 启用播放集，`has_shroud_dlc` / `has_nemesis` 分支存在只说明脚本条件，不能证明用户拥有、此次启用了 DLC 或某组合已经成功加载。

2026-10-06 后续用户确认拥有 Nemesis 和「虚境之影」，设计据此将两项同时启用作为主验收配置。该确认来自用户，实际播放集与游戏加载仍待实施验收时核验。用户同时选定偏强爽玩与 3～5 年普通星球周期；设计专用局势改为默认 Q=20 用 48 月，下面 SRC-06 的原版 120 月仅是公式名义结论，实际精度与完成边界以2026-10-08新实测及无Mod对照为准。

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

待验证：验收启动时的 DLC 实际加载状态、本起源 48 月进度的精度与日期边界、起源选择器资格、决议单键覆写优先级、国家→局势→目标作用域、动态容量乘子、旗标在各区划组的效果、造人口缺省 size 与模板权利、消化站搬运费用和原版迁移系统、末次补消费/销毁/天灾计数顺序、母星失守和重载恢复、超大行星 UI/经济/性能、灵飞与武灾实际组合。

本轮确定的是 Stellaris 的特定脚本定义和设计依据，没有新增 CK3/Paradox 共通语法结论。全部游戏内问题仍在[后续验收设计](acceptance-plan.md)中保持未执行。

## 6. 实施阶段补充（不追改历史调查）

对象限制补充：本机 `common/planet_classes/00_planet_classes.txt:1704/:1726` 分别定义 `pc_broken` 与 `pc_shattered`，不存在 `pc_cracked`。错误的类别会在引擎加载 `change_pc` 时报告找不到对象；静态 P 解析通过不能替代游戏定义引用的运行检查。居住站、环世界和突触凝练器类别显式有 `is_artificial_planet=yes`，拒绝条件仍须实际存档验证。本项为 Stellaris 具体对象定义，不推定 CK3 同名类别。

2026-10-06 后续已同步验收工具到 `522ac2d`，全仓工具回归通过；本 Mod 的最新包级报告为 [package-rc1.json](evidence/package-rc1.json)，16 个 P 文件、12 张 DDS、10 语言各 71 键静态检查通过。中文实机仍在实施中，进度 48 的失败开发探针见 [原生存档与日志](evidence/runtime-development/20261006T144810Z/findings.json)，不升级 EAT 用例状态。

| ID | 原版／实机证据 | 已确认的 Stellaris 事实与边界 |
| --- | --- | --- |
| SRC-25 | `common/situations/99_README_SITUATIONS.txt:105`；本机首次及第二次启动 error.log | 4.5.2 支持 total_progress 与 section_weight；动态值必须放脚本值表达式，base 只能是字面数字。本候选为 base=0、modifier add=target.eep_months。动态终点的实际完成仍待最终回归。 |
| SRC-26 | `events/unplugged_events.txt`／`common/scripted_effects/unplugged_effects.txt` 原版 ceiling_variable 用例；变量 README | 向上取整使用 ceiling_variable，检查变量是否存在使用 is_variable_set，不把 CK3 方言的猜测键搬入游戏。 |
| SRC-27 | 原版 `common/deposits/02_special_deposits.txt:42` 与地貌 README；开发局地貌错误 | triggered_planet_modifier 的 potential 后直接写 modifier 字段。独立 UI 修正评估上下文中的 prev 索引不可依赖；Carrier 与当前 owner 绑定母星的直接比较在重载后不再产生 ERROR_FLAG_INDEX。产出数值仍需经济验证。 |
| SRC-28 | 2200.01.01 及 2204.01.01 原生存档；create_colony 原版用例；实际迁移后日志 | 当前 create_colony 不自动造人口。真实迁入 100 后才构成有效殖民地；初始母星容量修正序列化为 multiplier=2，绑定母星为同一 Carrier。种子及完整回迁还需最终验收。 |
| SRC-29 | 开发局真实 count_deposits 导出和 error.log | 零结果导出可能不建立未设置变量，使用前显式置零，避免把缺变量提示当成有效统计。 |
| SRC-30 | situations README:66；真实 48 月进度和 pending=no；重载普通局势的 incorrectly ended 日志 | permanent=yes 不运行自动终点结束；普通局势若未成功结算会被引擎结束。本候选用持久局势，月度真实推进次日核验进度达到冻结 T 后手动结算，阻塞时保留；最终回归仍待执行。 |
| SRC-31 | 4.5.2 国策、行星类别与原版触发器 | 机械复制国策实际键为 civic_machine_replication；突触凝练器类别为 pc_cosmogenesis_world。武灾玩家阶段使用 has_crisis_level，而非全局终局天灾 has_crisis_stage；灵飞完成使用 has_finished_psionic_tradition。 |
| SRC-32 | 本机 EXE 原生选项表及 vanilla Chinese -quick 实际运行；Steam F12 帧 | -quick 自动生成原版新局；它不是新 Mod 指定预设已支持的证明。GDI／PrintWindow／DXGI 空帧并非本机游戏渲染失败，实际 GPU 帧由离线 Steam F12 生成，坐标从客户区转到屏幕。 |
| SRC-33 | 2204.02.03 原生存档与 `capital_scope` / `capital_scope.planet` 控制台日志对照 | capital_scope 保存为 Colony，而数值变量实际保存于承载 Planet。直接本地化 Colony 变量为空，在 planet 子作用域读出5992/12；报告引用须归一到 Planet。新开局母星绑定采用 Planet，不把殖民地 ID 当作物理星球 ID。 |
| SRC-34 | 原版`common/scripted_loc/000_example.txt`；C60王庭阶段实际错误显示 | defined_text默认random=yes，在所有有效text间按权重随机选择；random=no按最高权重、同权重首项。固定阶段须用互斥条件或非随机选择，不能假定无条件兜底只在其它分支均失败时运行。候选同时互斥并显式random=no，中文重载仍需复验。 |
| SRC-35 | [噬岩原生决议和日历归档](evidence/runtime-development/20261006T165559Z/findings.json) | 实际殖民地UI决议进入EEP后局势target序列化为Planet；其Q15/20/25按36/48/60真实月递增，次日完成且不重复发通用人口。原生存档区分物理Planet ID与Colony ID，不能混用。 |
| SRC-36 | 同组native-at36及native-after36原生存档 | Q15结算前源星实际151人口，补消费后回迁351，母星从4981增至5332，G与制造0；两次默认噬岩人口分支各贡献100实际人口。原版损毁对象位于根deposit、星球deposits引用，其deposit_holder.type=0/id为物理星球；已建区划在根districts记录type和level。 |
| SRC-37 | 铁心20261006T180749Z的purge-foreign-created／next-day／next-month原生存档 | 测试create_pop_group创建首次外族时，其category当日／次日尚未设置；原版月度更新后转为purge并实际减员。受控等待探针必须先保存真实肃清组，不把刚创建而尚未刷新职业的组当成已验证肃清；此事实不推定自然征服的刷新时序或CK3人口机制。 |
| SRC-38 | 原版00_scripted_effects.txt:9067～9090；seed-refill-active失败与192819的seed-final-active／seed-half-active原生人口 | resettle_pop_group宏在目标create_pop_group的effect作用域执行transfer_pop_amount。AMOUNT传裸调用方变量时，变量在目标新人口组解析而报未设置；跨作用域动态数量传已保存目标的完整变量引用后实际分别迁100／50，库存及总量保持。每次宏调用另守卫正数量，迁后重计真实需求；不能把宏展开等同于捕获调用方变量值。 |
| SRC-39 | 本机原版tools/commands_at_date.txt:1～12；20261006T202737Z实际GPU与原生存档 | 官方随包示例说明复制至用户目录才生效，日期格式为2200.01.01 = "observe"等；已越过日期的重载不会补执行，铁人及多人不可用。示例含game_speed4和2300.01.01的game_paused。种族洁癖实机已证实2200.01.04执行true及暂停，日更新后UI为2200.01.05；同进程重载初始2200.01.01后该命令确实再次执行，控制台两次日期记录。3/4/5/10/20/40/80年定时节点也实际暂停并保存。不据此假定运行中修改文件立即生效。 |
| SRC-40 | 原版traits/16_infernals_traits.txt:1～84、species_classes/01_base_species_classes.txt:352～379、planet_classes/00_planet_classes.txt:430～463 | 炎灵基础人口维护使用合金，火山宜居+20%、火山生存底线+50%；INF物种类明确added_planet_types=pc_volcanic，因此不能只凭行星类starting_planet=no断言预设非法。测试炎灵源星用火山类型，保持原版饮食、岗位和维护；实际DLC／编辑器合法性仍需实机。武灾矿物舰不会取消炎灵人口或其它设施的合金成本。 |

以上属于 Stellaris 的接口和本机运行经验，没有新增可无条件推广到 CK3 的共同脚本语法规则。

- 4.5.2原生生成的effects.log:1395～1397记录country作用域`set_origin = <origin>`，并明确不会运行银河生成阶段效果。这提供受控运行对照接口，但不等于正常新局重新生成；原版开局人口、区划与起源临时修正必须另行记录。尚未把文档存在当作实机切换通过。

- SRC-39补充实测：运行224056启动manifest的scheduled_commands为空，启动后在隔离userdir新增commands_at_date.txt，原生重载2200.01.01存档后2200.01.04命令实际执行并暂停在2200.01.05；恢复存档另经原生保存确认4800人口、C/G0/D2。因此本机4.5.2可以在原生重载后重新读取新增定时文件，不推定无需重载的即时热读取。
- 4.5.2原生载入UI在当前1024×768／0.75缩放会把长文件名截成省略号；精确OCR不能据此识别完整分组名。实际失败hive-scorched-natural23-source-ready后，仅把原生SAV原字节复制为hs-natural23-base，SHA-256保持，重新打开列表即可按完整短名成功载入2223.01.02。此是文件名与UI可读性限制，后续快照尽量使用短名；副本不是新游戏状态，原始meta／gamestate不得重写。源／副本哈希及原生载入回显保留。
- 4.5.2方舟Carrier接口补充（2026-10-07实机修正）：nomads_effects.txt:321使用NAME_Champions_Forge_Arkship设计，但本机该设计是military_arkship_champions_forge，没有carries_colony=pc_ark；旧推断错误，122536实际前提FAIL已归档。真正military_arkship_tier_3在29_nomads_dlc_ships.txt:1130声明carries_colony=pc_ark，125146四段实机确认真实方舟、人工对象、殖民地及本族种子，39项底层拒绝／独立100搬迁检查通过。本次创建路径初始1000人口另有仅创建SAV，不推广为其它船型通则。effects.log:361～374说明create_colony默认yes；nomad_assimilate_displaced_pops_effect:3189的PLANET指向方舟capital_scope，因此参数名并不限物理星球。pc_ark人工属性使生产源星触发器拒绝，但rc.4通用决议potential没有筛选而仍显示入口，实际UI FAIL须另修复，不能用底层拒绝替代。上述均为Stellaris Carrier具体事实，不外推CK3。
- 焦土与火山改造条件补充：本机infernals_1_events.txt:147～177的infernals.20是烈焰风暴轰炸按真实舰队规模生成凝聚的原版路径；:217起infernals.30／31的熔炉自动改造明确要求is_world_forger_empire及has_anvil_building，不能归为所有焦土国策的免费能力。普通continental→volcanic改造在01_advanced_terraform_links.txt:2609起要求allow_terraforming_into_volcanic，此旗标在infernals_crisis_events.txt:207的原版银河高温阶段3事件设置。吞噬之心不赠送这些条件；兼容测试应核对实际合法入口，不用控制台改类冒充原版改造完成。


- 4.5.2实机补充：母星真实空余区划需计入原版障碍。洁癖物理尺寸20、EEP额外D17、区划等级合10，还有d_decrepit_dwellings一个与d_failing_infrastructure两个（原版01_blocker_deposits.txt:898/967均planet_max_districts_add=-1），原生num_free_districts为24，不应仅减已建区划后误报27。
- 4.5.2原生human_ai控制台已真正开启，洁癖玩家国家is_ai只读探针仍NO，不可以此代替需is_ai=yes的原版自动回迁分支验收。真实三年后舰队/系统基地/传统已增长；完成科技仍为31项，但F4原生UI显示蓝激光472/1375、基因图谱472/1100、纳米力学899/1650，三系已正常研究。审计必须区分完成项和当前研究进度，不能以完成数未变判断AI没有研究。

后续灵能时序核对：原版common/scripted_variables/09_scripted_variables_shroud.txt:32–34将破入虚境三阶段终点设为500、750、1000；13_shroud_situations.txt:293起基础月增5，默认方案乘.75，凝聚方案会带原版凝聚产出代价。第二阶段需实际活跃通灵部队，第三阶段需Great Awakening传统，不用直接赋予进度绕过。common/traditions/01_psionics_shroud.txt:134起的Great Awakening在第二阶段可合法付费采纳，但仍有虚境局势相关tradition_swap/on_enabled分支；实际物种特性何时替换以原生SAV为准，不仅从按钮名称宣称完整灵飞。

2026-10-07灵能实机修正SRC-31：has_finished_psionic_tradition只证明传统已完成；拥有虚境之影DLC时还须has_breached_shroud才代表最终虚境仪式完成。本机原版08_scripted_triggers_shroud.txt、shroud_situation_events.txt的shroud.2800 after及shroud_shadows_scripted_effects.txt提供对应旗标／效果。实际蜂巢在传统完成、潜势／完整特质及局势954进度时均未发EEP完成通知；2280.12.23原生最终仪式结束，2281.01.01才实际通知。EEP完成守卫保留传统要求，DLC分支再检查已破入虚境；无该DLC不新增蜂巢／机械入口。这是Stellaris特有时序，不向CK3推广。此段修复先前PowerShell直接传中文造成的问号文本。

- 4.5.2原生吞星终点保存补充：2288.09.02星球112已经破碎并完整结算，但其旧局势16777221仍序列化且killed=yes，随后原生清理，2288.10.02存档已无该对象。不能把所有序列化局势都计为活动任务，也不能凭暂留对象断言重复结算。源星完成凭证、killed状态与后续对象清理须联查。
- 同场真实战争中的星球53在2288.10.02有ground_combat318767104，原生colony3引用同一战斗，攻击方leader16777219；EEP进度44、last_month_progress0、报告阻塞2、人口／容量未预发。owner和controller均为0不能独自证明没有地面战斗；阻塞月须与有效推进月分开记录。
