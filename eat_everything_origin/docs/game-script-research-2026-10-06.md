# Stellaris 4.5.2 吞星、区划、灵飞与武灾代码研究
人口月报和报告快照不是同一个取样时点：第二吞2233.07.02已独立核母星8105+实际返回578=8683；08.01原始last_month_growth_data仍以07.01的8105为month_start_size、growth584，真实GROWTH_CAT_GROWTH6／OTHER478／PROMOTION0，母星8689。因此本月growth包含此前回流，不能要求它的起点等相邻非月首保存的人口8683，也不能把584全称自然出生；原版新POP100来自已核咬合消息，没有在这些分类中作为单独key出现，不声称分类相加能重建总growth。成长通知eep_report人口快照8683，实际当月出生后8689；同日正常母星按钮觐见刷新8689，29项严格检查全部实际经济对象和所有country raw保持，仅快照及原生UI事件记录改变，证明刷新不制造人口。

num_free_districts(type=any)必须扣原生障碍：本次母星尺寸18＋EEP永久容量11=总29，有两个原始d_failing_infrastructure各planet_max_districts_add=-1（01_blocker_deposits.txt:898–909，SHA df9665890f54567b5988857e73baf752f690ad2fc8beb1ab7f543e184e43b11a），已有19个付费区划，所以真实未清障可建27、自由槽8，报告export_trigger_value_to_variable实际也为8。UI各区划条共享5/29、4/29、10/29不能解释为独立可建29。此为当前Stellaris地貌／UI／存档事实，不推广成跨游戏P方言或隐藏引擎实现。

月首年度咬合与预算不能混算：本次噬岩者第二源Q20/T48的2233.06.30→07.01，真实progress47→48仍未EEP结算，原生damage6→8、唯一当日ALLOYS_TEXT消息、库存合金+124.182=普通当月24.182＋原版年度100。母星+7由last_month_growth_data.growth_and_size独立解释，源478保持。after.budget_categories.last_month完整等before.current_month；实际这次月结的八资源变化按after.current_month.balance（影响力固定1000上限）及原版100合金精确核账残差0，三个真实research bank0。新私有门禁误用last_month产生E−0.02019／M−0.09525／U+0.04112／trade+0.15845，原39项FAIL保留，9项独立补证绑定其余38项通过；不是Mod异常或放宽误差。该口径与此前实际通过的native_month_guard、paid_economy_month_guard_v3一致。仅这些当前Stellaris原件事实，不推断所有引擎月结时序或Paradox共通规则。最终次日咬合必须从当日年度消息中分离，以免双计奖励。

议程已就绪时的实际原生UI流程：本次agenda_chart_the_unknown进度7058.25、F2显示免费启动；多次普通点击MOM列表未出现更换确认，另存原SHA与操作前完全一致。普通启动探明未知后，government删除current agenda/progress，冷却列表唯一追加该议程2261.03.02，country0新增timed_modifier唯一agenda_chart_the_unknown_finish／days3600，原生变量focus_agendas_completed0→1；后者由focus_events_1.txt:1050–1069的议程启动事件解释。33项独立核验其余真实经济／人口／完整EEP和原始对象保持。空议程后相同MOM列表按钮一次正常点击即切换，无确认窗；不要沿用其它未成熟议程切换的“是否变更内阁议程”弹窗假设，也不要把列表点击无效归因于已证实输入时长或位置缺陷。本观察不推定未公开引擎实现，也不推广至所有版本。

殖民建立后的原生移民须和Mod启动补种分开核算：第二源124在2229.07.01启动前后母星7958／源102均保持，30项决议守卫通过；次月2229.08.02母星7950／源116，全国+6。原SAV colony.last_month_growth_data中母星current_month_growth_details明确GROWTH_CAT_EMIGRATION14＋GROWTH_CAT_GROWTH6，源为GROWTH_CAT_IMMIGRATION14，实际−8／+14匹配。不能把后续原生移民14归因于EEP决议搬人，也不能将母星净减少当作人口丢失；每次需读原生分类及全国实际pop_groups。仅本机Stellaris存档事实，不推广为P脚本规则或未公开引擎算法。

殖民开始与建立的SAV字段不能混用：本机首源星90的colonization-wait-year1存档physical.colonize_date=2204.01.21、colony.colonizing_species=3321888769、实际人口48；到colonization-wait-halfyear实际102人时colonizing_species字段消失，physical.colonize_date被原生改写为2206.11.01。因此colonize_date不是永久不变的开殖民日期，不能等建立后拿它追述最初抵达；开始日应从之前的原始存档保留，建立须结合colonizing_species消失、真实人口／原生UI合法状态取证，不猜造established标量。本次第二源星124在2227.03.02实际colony24／18人、colonizing_species存在，开始日2226.09.01；只能称殖民中。EEP源星触发器明确is_under_colonization=no（eep_triggers.txt:46），不能因本国母星有足够种子而绕过未建立条件。

同调自发同调效果的完整来源：00_synchronicity.txt:41–58仅直接列自动重新安置几率+30%，但04_gestalt_jobs.txt:2022–2027中maintenance_drone另以owner.has_tradition=tr_synchronicity_integrated_preservation触发planet_amenities_no_happiness_add=250及岗位舒适度乘数；因此2226.03.02实际UI“后勤工蜂+250舒适度”有岗位侧代码来源，不能只读传统modifier就断言无此效果。实际付费1805.83054、UI1806，同日所有真实人口／job对象保持，不把展示增益当新增岗位或免费人口。灵飞采纳仍按01_psionics_shroud.txt:1–24的AP＋tech_psionic_theory判断；00_soc_tech.txt后半及00_scripted_variables.txt:669中已拥有AP会使该稀有科技抽取权重和原生自动研究选择权重乘10，仍不是保证当月抽到。02_council_agendas_ascensions.txt:9–69的agenda_mind_over_matter在合法可用且成熟启动后可正常给未掌握灵能科技25%进度（paragon变量151），作为后续实际UI经营选项；不能用console模拟完成。以上为Stellaris当前文件事实。

原生石质蜂巢付费殖民船（2225.03.02）：实际UI375矿物／150合金，命名确认后country.standard_expansion_module.expansion_list新增唯一匿名记录，target_planet=124／construction_queue=3／construction_queue_item=553648131，与construction.item_mgr.items中同ID的buildable_colony_ship关联；后者含starbase0、物种3321888769、design33554522、progress_needed360、真实resources375／150。旧item槽536870915=none消失，新handle低24位仍3，其余槽／队列原文保持。经济resources中三科研镜像249.864／212.664／268.464被移除，tech_status三个真实stored_techpoints始终0；不可把镜像字段删除当扣科研。该行为仅当前实机SAV／UI事实，匿名列表不得用只读named fields解析器直接忽略，不推广成P脚本语法。


原生科研船自动调查存档事实：正常界面只启用“探索”“调查恒星系”后，fleet.current_order.automate_fleet_order实际settings_explore／settings_survey=yes，其它异常／裂隙／考古／捕获／特殊项目和三类站点建设均no；同日仅fleet1新订单，country全根、ships全根及全部真实经济／人口岗位保持。旧Planet164.planet_orbitals的0=1引用在下命令当日即被删除，即使实际movement_manager.coordinate仍未移动；因此“所有星球root必须raw恒等”的原始调查守卫会FAIL。精确八项补证绑定原唯一FAIL、原29true／原SHA，证明仅旧轨道引用删除，不笼统忽略星球变化，也不追认原30项PASS。舰队现有归属来自country.fleets_manager.owned_fleets的匿名fleet引用块，fleet对象自身没有owner标量；不能用不存在的fleet.owner过滤后错误报告本国没有星站。上述仅本机SAV结构和原生UI行为，不推广为CK3脚本语法。
同调名称实机纠正：2221.01.02正常蜂巢的kinship_gestalt节点实际悬浮显示“同步昼夜节律”，来自wilderness_l_simp_chinese.yml:445的tr_synchronicity_kinship_wilderness，不是基础键的“同步代理”。原版00_synchronicity.txt中此tradition_swap只有name／inherit_icon／inherit_effects，没有trigger限制，故本局也实际采用该显示替换；效果仍为领袖维护−20%／人口帝国规模−5%／难民吸引+20%。后续报告以真实中文UI为准，存档与付费守卫仍要求基础tr_synchronicity_kinship_gestalt；不把基础本地化名当本局必然显示名，也不据此推定本族变成荒野政体。这是本机原版名称替换行为，生产Mod未覆盖该传统。
2026-10-09蜂巢区划真实完工补证：正常450矿物／480基期订单在1.25速度下360日仍450/480，再30日建成。母星蜂巢4→5后coordinator1360→1400、三系calculator各156→180、fabricator400→500且全满，与20×5×1.2+60=180吻合；原建筑引用未新增或改变。再正常270矿物增建发电4，2218.12.02已实建5+10+4=19，大于原始planet_size18，EEP永久额外6后的总容量24真实可用，非仅UI上限。后完整30日采矿2000／发电800全满，实际E+28.943、M+20.133，八类预算按事前固定影响力上限核0残差。各类UI分别5/24、10/24、4/24共享星球总上限24，不能当三类各自独立可建24。

同调官方简中及基础键：traditions_l_simp_chinese.yml:238／242／244／247／253／267为同调、克隆器官、同步代理、自发同调、集体思维、灵活思维。蜂巢自发同调为tr_synchronicity_integrated_preservation的名称替换；collective_reasoning要求它，harmonious_directives要求kinship_gestalt及cloned_organs。adopt普通蜂巢人口维护−10%，finish星球飞升效果+25%及一AP槽。category仅要求格式塔，不等同后续灵飞全合法。当前正式AP科技至上已正常获得，本机实际说明为重点研究政策及稀有科技机会+50%，不是全科研速度+10%。

2026-10-09探索研究岗位140→156的完整本局来源已定位：zone_research_unity调用zone_researchers_add的AMOUNT=20，母星4级district_hive原给每系20×4=80；05_research_buildings.txt:76～80的唯一building_research_lab_1调用researchers_add、AMOUNT=building_static_jobs_3=60，故原每系80+60=140。zone_researchers_add:314起的格式塔普通星球faith_in_science分支是triggered_district_planet_modifier、mult=0.2，只追加区划那80的20%=16；researchers_add:18～28的实验室是普通triggered_planet_modifier，不包含这条区划增益，因此每系实际156=20×4×1.2+60，与原SAV满员值一致。不能把所有建筑科研岗位也乘1.2。正常第5级蜂巢集群悬浮已经显示每系+24，后续实际SAV另验；不会凭此悬浮宣告已经建成或已有实际+科研收入。

2026-10-09正常建筑槽与区划扩张限制：common/zones/00_zones.txt:5的zone_default.max_buildings=6为固定值，不能假定继续增加district_hive等级就能多盖中央节点。zone_research_unity引用zone_unity_jobs_add（scaling_district_unity_4_jobs=40）及zone_researchers_add（researchers_4_jobs=20、LARGE_AMOUNT=60），星球modifier为zone_building_slots_add=3；具体每级真实岗位仍须结合内联脚本、探索完成修正和SAV，不把单一常量当完整岗位结论。正常district_hive基期480日，跟本局矿电240不同；后续如正常购买蜂巢区划必须单独按实际UI／订单核480基期，不能沿用固定240的矿电守卫。

2026-10-09正常满仓月核：原版common/strategic_resources/00_strategic_resources.txt:132～136（SHA140dea921a77f76726f361eca99f59f0c7755e4e728dec4699d3b732457911a4）定义影响力固定上限1000。2215.01.02→02.02实证前后影响力均1000、current净+6.3，未经封顶库存残差−6.3；按实施前固定min(1000,before+net)后残差0，其它七类原残差均0、after.last全分类精确=before.current。不能把固定影响力溢出误报成经济丢失，也不能据此放宽其它未声明资源的核账。

2026-10-09繁荣正常经营实证：官方简中traditions_l_simp_chinese.yml:510／520／549／568／587分别为繁荣、预制建筑、几丁质建筑、效率本能、神经信号增强器；仍以基础key保存。00_prosperity.txt实际adopt为采集站产出+20%，sct为结构费用−10%／建造速度+25%，administrative_operations为结构维护−10%，pursuit_of_profit为岗位产出+5%，interstellar_franchising为岗位维护−5%，public_works蜂巢显示替换，finish另加采集站+25%并给飞升槽。当前四笔实付425.45052／520.66458／625.90113／740.95863，显示426／521／626／741；继续符合这几例向上整数显示，不推导所有UI通用舍入规则。正常采矿两单各实付270，原生progress_needed仍240，UI192日；真实90日首单进度112.5，第二单0，独立证明1.25建造进度，不把显示工期当原始基期。后续360日已建成采矿10、2000岗位满员，发电3／600满员；EEP容量仍额外6，原实际区划是付费建出。

08_unity_buildings.txt:1093～1098的突触节点两座条件只限制AI（OR中玩家is_ai=no已经满足），正常玩家仍可增建；实拍中央zone_default允许突触节点，价格360／UI288日，维护能源1.80、新增200突触子个体岗位。不能因档案馆zone_research_unity三个槽已满就认定全星不可增建，也不能把重工业zone_foundry的绿色加号当档案馆第二排。实际原SAV母星district_hive1引用zones0／2／3，分别default／research_unity／foundry；建筑引用存在zones.buildings及全局buildings根，audit中colony.buildings空不表示母星无建筑。当前研究及节点原建筑38／16777251／41属于zone2，中央0／1／2为蜂巢首府／繁殖池／蜂巢养殖场。

2026-10-09本机正常探索传统实价／时序：UI“超适应进化”203，实际凝聚扣202.98709；下一“突触营养池”UI267、实际266.19181。两例都是向上整数显示，原理论define公式不应直接当精确整数扣费或推导通用引擎舍入。真实付款须记录原SAV小数差，并按购买前固定的显示区间核验。基础key仍为tr_discovery_polytechnic_education／tr_discovery_faith_in_science，完成保存基础tr_discovery_finish；蜂巢中文显示替换不会把SAV键改成_hive。原生三系研究岗位并非140×1.2=168，本局实证各140→156；最终公式需合并各建筑／分区实际脚本，不能只乘显示百分比。正常采纳当日SAV尚未改岗位；首个30日已156满员，但该月预算仍按原140产出，第二30日预算产出才增加，两月实际库存逐月按current余额精确核账。科学家维护12→10.2和万众一心后的凝聚净24.71361→30.05021已实证；首月原严格产出FAIL与第二月独立PASS都保留。

2026-10-09实际月账补充：2212.07.02→08.02的真实30日库存差八类精确等后件budget.current_month.balance，后件budget.last_month的全分类原文严格等前件current_month；原生增长6、无额外收入或EEP变化。本组证据不能无条件将名为last_month的SAV块当最新一次实际入账，之前这样要求的July1守卫原FAIL保留。前日July1→July2实际人口与岗位及全部真实库存不变，但人口组1的housing_usage2508→2514、crime／power25.08→25.14，缓存终值按既有组size2514及/100吻合；若要求这三项也raw恒等会误报“人口改变”。这不表示可以笼统忽略人口组字段，只在精确原SHA和已证缓存字段范围内补证。

2026-10-09扩大只读原版对照范围：真正无Mod初始6c312b601b1bff74c6f66029e5a0e7faaeef9f8e76f8d68d9753496ff18db736（runtime-development/20261007T184149Z/vanilla-shared-world-native-initial.sav）到无Mod同日原生加载保存31def47a0d168b47011f80283923ca538c945e111d250dcac53930f6589ee279（20261008T090850Z/postvanilla-initial.sav），government原文精确只unlocked_civic_council_slots0→4；相应启用Mod列表确为空，已有postvanilla-original-initial-proof认证正常本族／origin_default。119月前件c876fb7ccdc6a6d7ac3448e6b2904d825deb9cbe6ec23208bcc4e614ab229175到同日重载c63a64ec9cfcbeb0e5aa6c2a330af3a42b352c18bb9759e255f667e0f91f7dc9的全colony根另有13／14／15 binary_flags缺失→24，以及colony3 civilian1450→1449；此前仅核审计拥有星球子集漏掉这些类别。它们证明同类字段原版也能刷新，不能单凭类别一致就证明本Mod母星civilian2498→2945的具体数值／经营影响均已独立复现。原4项严格重载FAIL保持；后续应区分资源／实际人口／EEP不变量和这些缓存，不宣告完整首次严格重载通过。

2026-10-09建设续验确认：原生 message 的 date 与 end 应分别核对；本局最后5条吞星通知date2210.04.02、end2210.07.02，在2210.06.01→2211.06.01推进后自然从SAV删除，不能要求跨年原始消息列表恒等来证明没有新奖励。未来守卫只允许已到期旧消息删除，仍拒绝新消息或原消息被修改。已下单实际队列进度每原生日1，三笔300矿物／240日订单串行；第一360日只完成第一采矿，下一采矿120／240、发电0／240，容量加成自身没有生成免费实建区划。

2026-10-09只读原版续查：00_discovery.txt 的完成效果为全科研速度+10%及一个飞升槽。00_ascension_perks.txt 的科技至上仅 rare_tech_draw_chance_mult0.5，万众一心凝聚+10%且排除机械帝国；不能把早期版本的科技至上科研+10%写到本机4.5.2。00_ascension_paths.txt 的ap_mind_over_matter要求已有>1个AP及空传统树等，本版本该AP块未要求tech_psionic_theory；有Shroud DLC时potential允许格式塔／机械，机械还有原生名称替换。后续传统／突破虚境的具体科研条件另按对应块核，不能由此断言整条灵飞不需要科研。发现树蜂巢中文“超适应进化”“突触营养池”逐字来自traditions_l_simp_chinese.yml:492／500；后者本机zone_physicists_add等实际按is_gestalt触发+20%对应分区岗位，旧中文说明文字不能单独当成实机岗位公式。这些结论仅适用当前Stellaris原版文件，不推广到CK3。

## 2026-10-08：自然转换与隔离星系的原生证据

实际pc_volcanic→pc_hive队列在正常付10000能源后为total7200、initial_total_days7200、倍率1；真实五年／十年分别progress1800／3600，未提前完成或再次付款。2299.03.12起点到2309.03.12仍在同一母星physical1／colony0，核心地貌、容量16与court各一份、绑定和EEP五项账本保持；54项只读检查通过，不代表最终转换／真实容量UI通过。

本机序列化timed_modifier.items是匿名对象列表；q.fields仅用于命名字段，直接传匿名列表会抛ValueError。恢复按令牌深度分块后才逐对象读标量，不修改SAV；原失败源码保留。这是当前Stellaris序列化和审计接口事实，不扩展成所有Paradox方言规则。

真实源星隔离核对：原自然2223.01.02的母星1.coordinate.origin=5（EEP-Throne），殖民源84.coordinate.origin=78（Demivideau），两星系不同。galactic_object.<id>将planet序列化为多个重复标量字段，不能用q.scalars只取末个planet或把它当planet列表块读取；必须遍历全部字段。源colony24实际只有69本族，正式开始需补迁31；普通非格式塔外族候选实际country1／species2为MAM有机，不是蜂巢或机械人口的即时清除对照。

快进回执在当前原生面板可裁为“Fast Forwarded 1800 D”；完整days精确匹配会在真实终点反复等待。恢复必须同时读取新鲜实际日期、暂停、正确完整／裁断天数行，并原生保存核真实进度，不只看日历。原监测失败和多等耗时保留，不计性能样本；后续联合判据辅助用独立恢复文件名。Windows本机Python默认GBK读取带中文OCR失败，审计／OCR文件明确UTF-8读取；这不是本地化内容或游戏运行失败。

## 2026-10-08：原生存档、市场和付费操作的实际字段

215509简中离线原生回归确认：国家起源保存在 `country.<id>.government.origin`，不是国家顶层。无本起源蜂巢 country1 的自有首都不显示女王按钮；切换、查看和保存的37国／九组实际数据同日保持。

原生建造订单索引为 `construction.item_mgr.items`，队列关联为 `construction.queue_mgr.queues`；本次queue0.location={type2,id1}指物理planet1，六订单buildable_district.planet=0指colony0。母星colony.districts解引用真实district对象，不按全局列表顺序或未定义的district.planet属性归属。正常下单会改变母星last_district_changed，但不会提前增加实际district.level或岗位劳动力。六240矿物地热订单、真实六队列与全部其它对象69项检查通过，第一年两座完工后劳动力900→1500且全部就业。

4.5.2本次原生国内市场实际以trade库存交易：出售2750合金／5000矿物／10000食物／500异星天然气，正常购买8500能源，能源2460.80332→10960.80332而贸易4957.92942→760.92942。不能沿用旧版本“卖出资源即直接增加能源”的假设；成交价依真实交易与市场变化记录，未推导全游戏版本的价格算法。

最后扩张传统的原生显示成本6155为取整，实际凝聚扣6154.89983。真实选择第五AP ap_hive_worlds；母星容量37由尺寸20、EEP16及原版扩张完成1组成。2299.03.12实际付10000能源启动 pc_hive 改造，物理planet1.terraform_process记录progress0／total7200、paid.energy10000、who0、initial_total_days7200及reroll_deposits=yes；新增has_terraformflag／volcanic_terraform为实际原生旗标，不作EEP结算或提前容量。

两次正常飞升／改造付费操作都观察到三系科研库存下降（改造中520.56604／339.97529／227.49598→缺省0），原因未独立隔离；完整差异和初始严格断言FAIL保留，不宣称正常付费操作全库存保持，也不凭其它已隔离的原生奖励对照推断本次内部原因。本轮女王报告只读另有同日全库存严格对照，与此费用操作分开。

以上均为本机Stellaris4.5.2实际存档／UI事实，不推广为CK3或所有Paradox版本共通接口。官方deposits/99_README_DEPOSITS.txt:25～28的should_swap_deposit_on_terraforming默认no只描述一般地貌交换开关；蜂巢世界reroll_deposits=yes的实际核心地貌结果仍须自然完成检查，不能仅凭默认开关预言保留。

## 2026-10-08：女王按钮非星球上下文的实际求值

203412完整最终日志在05:32:11记录`Wrong scope for trigger is_owned_by`，生产eep_buttons.txt:19的allow当前作用域为country。并列is_scope_type=planet没有在这次UI调用中屏蔽行星专用条件，因此不能据此假定求值会短路；母星报告数据和经济只读通过不等于所有界面作用域日志通过。官方common/button_effects/example.txt:2～5明确This可能为选中对象或玩家country，From为玩家country；00_scripted_triggers.txt:3608～3623、3739之后提供trigger内if／limit／else的真实官方用例。rc.8仅在对象确为Planet时进入归属／绑定判断，否则明确always=no，运行时仍需新进程积极验证。这是本机Stellaris按钮上下文事实，不将其推广为Paradox通用短路规则或CK3方言。

## 2026-10-08：同路径决议覆盖与查询零值告警

通过open_kaishek的控制包仅从本机原版提取`decision_lithoid_swarm_consume_world`，与本Mod使用相同相对文件`common/decisions/zz_eep_native_decision.txt`。201344／202451全新离线简中进程的实际enabled_mods分别`[EEP, 控制包]`与`[控制包, EEP]`，从相同796f…原生SAV在physical1731／colony15／Q20／真实100种子“春天”经决议UI开始：前者实际原版局势，首月8.5；后者EEP局势，Q20/T48、首月1。C/G／制造0、D2和绑定保持，第一支21项／第二支18项范围证明通过，完整日志与初始guardFAIL保留。仅证明本机同路径双包的实际覆盖顺序，不推导所有不同文件／同键Mod的统一优先级或原版118月完整通过。公开说明应提示适配器若被覆盖，会回落原版流程而失去EEP结算；planet_view.gui覆盖须另作界面兼容处理。

193619日志实际两次报`eep_old_damage is not set`，对应`eep_begin`旧损毁导出后的读取；前置set_variable=0不能据此宣称零导出后变量必存在，虽数值仍Q20/T48。后续对查询输出读取加is_variable_set守卫、缺省零不做减法，保留正旧损毁的真实减法和零／半／完整种子迁移实机回归。这是本机Stellaris导出／算术读取的实证与待验证修复，不把推断的引擎内部稀疏实现推广为Paradox通用规则。

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
# 原生移动目标的殖民地／物理星球区别（2026-10-08）

本机4.5.2在国境capital_scope保存事件目标时，原生SAV目标为type=colony／id0；auto_move_to_planet文档明确要求planet目标，直接传该殖民地目标后没有实际移动订单。须经capital_scope={ planet={ save_global_event_target_as=... } }取得physical1，再给现有舰队设置移动。首个无效尝试及一日原生SAV保留，不作为移动成功证据。这是Stellaris当前殖民地拆分规则，不推断其它Paradox方言。

后续原生SAV确认经planet转换的目标为physical1，但本次玩家舰队仍未实际航行；不能把目标类型修正等同功能成功。官方000_fleet_action_examples.txt的queue_actions.orbit_planet在原生SAV真实生成actions.orbit_planet.planet=1／action_initialized，三个月后仍move_idle，原因尚未确定。这里只确认作用域类型和序列化事实，不推断所有舰队行为。

## 真正无Mod吞岩精度与冷却补证（2026-10-08）

首发后RUN20261008T090850Z的实际enabled_mods=[]、默认起源石质吞噬蜂群，Q20原生决议的第1月实际progress与last_month_progress均为8.5；第12／13月为102／110.5，第24／25月为204／212.5。它确认先前“数学1000/(6×20)”不能直接预测当前引擎序列化步长；尚未完成117／118月终点，不能提前宣告最终边界。

`common/decisions/02_special_decisions.txt`和`common/scripted_effects/00_scripted_effects.txt`实际设置recently_eaten_planet的days=360。`events/colony_events_1.txt`的colony.190注释写Every 6 months，但运行合同应以实际脚本和存档为准。2200.01.02启动，第12月2201.01.02冷却已移除而损毁仍0，第13月2201.02.02损毁2并重设冷却359；第24月为损毁2／剩29日，第25月为损毁4／重设359。原生on_monthly和日计时的先后会形成这个观察边界，不能为了凑注释日期增发消费。此结论限本机Stellaris4.5.2，不推断CK3。

源星的实际人口从100自然变为111、237等，包含默认迁徙和增长；实际100种子前置的守恒与后续自然人口不能混为同一断言。原生人口组审计中物种在key.species，误用顶层species的辅助失败与更正只读复核均保留。

本轮真实117／118边界已观察：2209.10.02进度994.5、源仍是Q20大陆星球；2209.11.02真实破碎并没有存活吞岩局势，下一月2209.12.02仍保持。完整22个连续日历检查点238项范围断言通过；只约束无Mod原生边界，不能代替其它Mod政体路线。终点SAV中物理天体保留colony15旧引用，但owner已移除、原殖民地实际无人，因此必须联查全体物理对象／所有权／实际人口，不把单个旧ID当活殖民地。正式完整原件归档正在进行。

原生最后余料计算在00_script_values.txt:2472为ceil(num_free_districts/2)，不是初始Q减障碍数。运行末期Q20／18损毁／level1蜂巢区划，实际完成月矿物库存差363.1788减原生当月收入118.4288并加维护110.25，残差355；普通奖励第37／61／73月为587，第97／109月为592，不能把全程矿物奖励固定为常数。原生合金分支倍率是3、矿物普通分支倍率5、仅余一个区划槽的矿物分支倍率3，均有原生min／max约束；上面的预算残差是实际观察，不能只凭脚本乘法推算引擎取整。

真正无Mod的119月首次原字节重载也出现原生派生缓存差异：母星住房使用从上月实际6359更新为当前6365，设施／犯罪度随之重算，母星及已破碎源星carrier_binary_flags1→3。库存、实际人口组、岗位、科技、研究队列、传统／AP均保持；该完整FAIL保留后从其原字节存档再次重载，22项严格检查全部保持。它证明这类差异也能出现在无Mod过程中，不把此前每一种Mod重载差异都直接归因于这个观察。

普通运行跨月的独立原字节117月观察分支在2209.11.01显示colony.185“星球已吞噬”，原生立即阶段已经破碎源星并回迁人口，但原生局势仍progress1000等待玩家选择。真正点击“我们还是很饿。”后，原生player_event38消失，选择历史新增human1／option0；同日库存、所有人口组／岗位、科技／队列、传统／AP和世界集合25项保持检查通过，局势仍1000。下一真实日2209.11.02才清理，库存与6359母星人口完整保持。确认前或确认同一暂停帧就要求局势已killed的断言均过早，原始FAIL保留。player_event的date2213.08.01在此是将来日期，实际显示与确认是2209.11.01，不能当作通知触发日期。

这次普通跨月观察得到弹窗，而先前连续fast_forward分支118／119月没有待选弹窗；只记录本次两种路径的实际观察，不推定所有快进命令都会吞消息。原生日历普通运行中的事件自动暂停会在选项确认后解除，不能拿“弹窗时显示暂停”当作已手动锁定日期；需要同日保持检查时可实际点击后立即打开原生暂停菜单，仍必须核验最终SAV日期。这里用同一普通待选SAV原字节恢复，未重放事件或奖励效果。

## 旧自然战争存档的原生修复与临时对象（2026-10-08）

RUN20261008T103147Z继承有机洁癖自然2281.01.11旧原件，第一次载入修复地貌50331965。全局原件比对发现它没有type、仅deposit_holder指向外国无主NAME_Gish核废土physical516，随后killed并从该星引用移除；不是实际母星physical7的d_eep_core。保留两条原生战斗逃脱舰返还日志和原始修复，不将它们当新正式版代码修复。

同档species71／specialist／colony38的200人口组在多次同日原字节重载中重分配ID并显示GROWTH_CAT_PROMOTION200；四个pop_group=4294967295的原生虚拟岗位同样重建ID但type、planet和workforce等值保持。真实一日更新后再加载仍有临时ID和stability、civilian、carrier旗标差异。库存、实际各星球／物种／阶层总数、EEP账本和主要固定对象保持并不能自动升级成“所有集合严格保持通过”；该专项原始FAIL与未解决状态保留，允许继续独立合法传统／AP检查而不冒充完整路线通过。这个观察限上述Stellaris旧战争存档，不推断所有存档或其它Paradox方言。

当前有机洁癖自然存档的主体species71带base_ref3321888769／HUM／trait_geleboric_mutations，是本族原生变体。4.5.2原版15_strange_worlds_traits.txt中该特质含寿命、增长与幸福度负修正以及biologist岗位加成；不能只看portrait变化就当作异族，当前是否合格仍须核原生模板／物种关系。

4.5.2原生贡品事件marauder.101.a的能源成本由common/scripted_effects/marauder_tribute_effects.txt的tribute_cost_energy按旗标调用add_resource；本次悬停实际-250、真实能源3170.94638→2920.94638。虽然同日实际科技与研究队列、全部非科研库存／人口／世界集合保持，三系standard_economy_module.resources研究储备发生变化，完整库存比较FAIL保留，不能仅凭脚本只写energy便声称所有科研池保持；尚未证明内部原因，不作Mod补偿。随后原生外交响应与action.39现状和平空选项各16项同日保持通过。外交消息遮住控制台时要保留失败并正常确认或调整界面后核既有完整回执，不能重复发送已完成的fast_forward360。

## 原生法令、建筑区域与灵能议程补证（2026-10-08）

本机4.5.2的00_edicts.txt:884采矿补贴提供miner_jobs_bonus_workforce_mult=0.20，不是直接矿物产出固定乘法；正常撤销后母星miner基础400保持、bonus150→70。1264行敬奉圣人提供pop_bureaucrat_bonus_workforce_mult=0.05及唯心思潮吸引力0.25，实际母星bureaucrat基础840保持、bonus105→147。2290.03.02实际一次费用30.51、UI显示31；法令基金123/141等显示也随帝国规模和寺庙完工更新，不能把显示整数当底层完全整数或视为固定旧版Unity+20%。正常撤销／启用原件19／21项同日检查通过。

4.5.2SAV的建筑位于顶层buildings容器，区域位于zones；区域的buildings是未命名ID列表。母星档案馆实际zone1、zone_research_unity；寺庙building_temple正常下单记录在construction的buildable_planet_building，包含planet=0（殖民地ID）、zone=1，不是物理天体7。实际费用400矿物、needed360，原件已有building2保持；完工后区域列表恰新增一座寺庙、官僚基础840→1040、建造队列清空。这个结构限本机Stellaris，不套用CK3建筑方言。

原生心胜于物议程奖励常量@agenda_award_tech_progress在05_scripted_variables_paragon.txt:151为0.25；原生UI也显示灵能理论+25%。从0进度正常推进后，2291.12.02实际准备3293.83193，主按钮“点击启动议程”可用；旁边提前启动另收6500Unity，两者必须区分。正常点击成熟主按钮后全部库存／人口／世界／EEP完整保持，原生stored_techpoints_for_tech仅增加tech_psionic_theory=1929.19999，alternatives社会候选和标量always_available_tech新增该科技，government记录正常议程冷却至2294.12.02；完成科技集合仍无该科技。实际选择社会研究队列后UI1929/7716、预计37月，研究中不等于灵飞完成。

普通运行中的自动暂停事件确认后，ESC菜单存在并不保证底层日历停住：同一RUN女王成长通知第一次确认保存实际漂移2290.02.01→2290.05.11，完整失败保留。原字节加载待选SAV恢复手动暂停基线后，同一物理选项点击／立即ESC方法23项同日保持检查通过。必须以实际SAV日期和暂停状态核实，不能仅凭菜单或事件自动暂停推断同日操作；这里没有重放事件或经济奖励。这个结论限该运行环境，不推断其它Paradox游戏。

## 原生科研储备与经济镜像（2026-10-08）

本机4.5.2原生SAV中`country.tech_status.stored_techpoints`为未命名三数列表，次序物理／社会／工程；`stored_techpoints_for_tech`是各科技既有部分进度，两者不能混用。`modules.standard_economy_module.resources`中的同名三系字段可能缺失或滞后，原生消费操作会同步它们，不能独用后者判额外科研奖励。实际有机社会研究36个月中科技储备下降而经济镜像累加；同日正常工厂下单只同步镜像，实际三系储备、完整科技系统保持。真正无Mod决议前后也见三系镜像从缺失初始化而实际储备保持。限已核原件，不推断其它版本／游戏或追认所有历史FAIL。详情和原件SHA见[科研储备审计修正](research-stock-audit-correction-2026-10-08.md)，旧原值与失败均保留。

## 原生政策、岗位限制和虚境方案（2026-10-09）

本机4.5.2SAV的局势具体对象位于`root.situations.situations.<id>`，不能省略内层同名容器；只读比较必须先断言真实对象非空，以免空文本产生相等／空差异假证据。`country.<id>.active_policies`是匿名对象列表，单个对象包含policy、selected和可选date，不是以政策名为key的命名容器；2297.11.02正常民用经济确认只改变economic_policy条目并保存该日期，原生UI明确十年内不能再次修改。原生00_policies.txt:3595只排除格式塔；实际次月消费品+48.45080、合金+24.63462，岗位、人口和EEP未获额外奖励。

原生4.5.2母星“经济”页紧凑岗位人数块点击切换优先度；展开专家层后才显示劳动力限制滑条和加减按钮。减号悬停注明Ctrl一次减少一个岗位、Shift设置最小值。本环境一次虚拟Ctrl＋经过聚焦的点击实际冶金师800→760、bonus100→95、max800保持，并将同族40劳动力由专家分配到平民；不能只根据悬停文字便认定100步幅。虚拟修饰键是否被当前游戏收到尚未证实，物理组合动作应先聚焦再发送并核实际存档。原700上限断言失败保留；次月六类预算残差0、矿物净+0.08986和消费品净-1.90462按实际记录。

原生灵能采纳会触发mind_over_matter_immediate（shroud_shadows_scripted_effects.txt:4068）更新己方同源模板和引用。本样本基础3321888769→102、Geleboric变体71→103，仅增潜势灵能，41个己方人口组ID、总数及其他字段保持；187个外部人口组和机械67／77原件保持，非免费人口。原生“解开丝缕”需要tech_astral_harvesting及至少10线程；在本阶段每月线程维护10，轨道实际收入3，500→493，进度5.5、凝聚产出倍率+10%。同日选择只变实际方案和chaotic_approach标记，科研经济镜像同步而真实池保持；静观其变实际3.75，不是自动5。阶段2需要实际活跃灵能军团、阶段3需要大觉醒传统，选树、显示完成效果文案和潜势灵能均不能当最终虚境完成。

本机4.5.2待选消息为根部重复的`player_event={...}`，须逐项筛country0，不能只读取第一个同名块；它的date可能是未来到期时间，不是本次触发日期。选择历史位于`open_player_event_selection_history.selected`匿名对象列表，包含player_event／human／option；原生临时修正位于`country.<id>.timed_modifier.items`匿名对象列表。虚境调谐为`country.<id>.modules.standard_shroud_module.attunement`，本次shroud.2305正常option1使x=0→0.1125、y及其余模块保持，真实凝聚库存恰+2781。marauder.105的两次原生kill_single_pop在physical1672／colony40同一worker组772→572，实际减200；不是两个任意整组删除，也不是两个个体量。实际效果限本次原件，不跨版本或套用CK3。

EEP的eep_tasks／eep_waiting是eep_report重算的报告字段，不是局势运行时每月必然自动刷新。第三源星真实12月时任务进度12，而country变量全集仍等于开始原件，eep_tasks仍0；辅助若未经报告操作强制断言1会制造检查失败。守卫应分别验证实际局势与收益账本，不因这个报告缓存计数假定吞食没运行或有早期收益。原始失败和独立完整变量补核分别保留。

本机4.5.2的destroy_colony／change_pc后，物理1679仍留colony38历史指针，SAV也保留actual_pop_sum0、pop_groups空的旧殖民地对象；实际owner／controller已无、owned_colonies移除38、星球破碎且存款空。审计逻辑销毁须检查这些真实活跃性字段，不能要求所有历史对象从文件物理删除。第三次结算09.01progress32时源星仍有1419同族，09.02真实回迁1419并造200，母星10144→11763、全国27419→27619、102／103逐物种守恒，D8→12含累计余数进位。

本样本所有三系科研队列为空、真实F4速度各+13%。冶金限制次月、静观其变次月两个无EEP结算月及第三结算相邻日，实际tech_status.stored_techpoints增量均等于当月净研究×1.13按五位小数向零截断，完整科技其它字段保持；预算里的研究净额与实际闲置科技储备不能直接一比一。只确认这些空队列／相同速度原件，不将它用于正在研究、部分科技进度或不同加成的全部场景。三系入账与其他非科研库存保持分别核，原完整严格FAIL保留。
群星4.5.2原生犯罪通知同日确认差异（2026-10-09）：crime_events.txt:692的crime.40 immediate已经添加永久criminal_underworld及criminal_underworld_appeared计时标记；普通选项只含tooltip，after:888正常移除criminal_underworld_event_up。真实2305.01.02确认前后物理母星唯一差异就是该显示标记删除，永久修正／计时和全部其它字段保持，不能把这一删除理解为消除犯罪或第二次应用修正。原SAV、真实UI和25项严格FAIL／27项精确补核分开留存，参见发布后验收文档。

同轮辅助读取教训：open_player_event_selection_history.selected是匿名对象列表，每对象有player_event／human／option三字段；q.fields仅用于命名key=value，不能直接用在匿名列表上。用q.tokens按最外层花括号分组后才对单对象用q.scalars，须断言闭合、字段全集及旧history严格前缀，只追加预期human记录；这属于群星原生SAV结构，未推定其它Paradox游戏存档格式。原辅助异常字节与后续严格物理保持FAIL都保留，不通过重放真实选项消除。

本机4.5.2国内市场实际使用trade付款：正常买1000矿物实扣1417贸易，能源及其它全部真实库存保持，不能按旧版本经验假定能源付款。原生传统节点会先打开购买确认框，点击实际“是”才付款，直接ESC会取消；灵能军团真实实扣16695.77881、显示ceil16696。本机母星默认建筑3×2位于大区划图右侧，升级箭头和建筑主体是不同控件；误升级800矿物／0天订单的正常左键取消已全额退款，右键未生效的原FAIL保留。这些是本机Stellaris原生UI及存档实证，不作为跨游戏通用规则。

原生4.5.2建筑替换项目存档为construction.item_mgr.items.<id>.buildable_planet_replace_building，包含building／planet（殖民地ID）／zone／replace_building（原建筑ID）；灵能军团真实500矿物／480天。普通新建筑为buildable_planet_building，寺庙400矿物／360天；区划为buildable_district，采矿300矿物／240天。下单只记录last_building_changed／last_district_changed和真实支付，不提前变建筑／岗位；队列后项在前项完成之前progress0。当前实证仅已付费下单，实际完成及新增岗位必须独立核。

4.5.2的jobs/priests_add.txt实际为上述唯心原生配置加job_bureaucrat_add，02_specialist_jobs.txt的bureaucrat类型再根据bureaucrat_is_priest切换显示与建筑图标。因此本例已有两寺庙的SAV工作类型仍是bureaucrat，而实际UI正式岗位名为“祭司”；新增第三寺庙应验该实际类型容量增200，不能期待并不存在的独立priest类型。jobs/telepaths_add.txt则在普通非格式塔配置直接加job_telepath_add200。此为所读本机版本／配置的事实，不套用历史版本或CK3。

原生风暴改变真实建设工期（2026-10-09）：electric_storm_aftermath_modifier_severity_3在21_static_modifiers_cosmic_storms.txt:192给予planet_building_build_speed_mult=-0.65及planet_jobs_energy_produces_mult=0.3，本机简中正式“余波：极端带电大气”，余波持续3年。2307.05.02母星有剩891日的该原生修正，采矿真实117.15／240、UI剩351天，240基期项目当前UI686天；实际预计工期必须包含0.35速度和未来余波到期，不能把base_buildtime或初始报价当恒定真实天数。EEP吞星月推进与虚境3.75不受这一建筑速度字段影响，本例它们正常推进7月，原完工预测FAIL仍留存，不移除天气赶排期。

同一真实长月段轨道丝缕预算由3变4／支出0，实际7月库存228→253，不等于固定7*3。暂只确认预算类别orbital_research_deposits的原生变化，未独立确定新增轨道来源和变化日；多月库存不要套恒定收入，必须记录变化及相邻真实月预算，不能据不完整年度快照追认逐月累计对账。详见本轮验收原始FAIL与恢复方案。

原生pending上下文与领袖事件（2026-10-09）：player_event.scope.from中的saved_event_target允许重复命名字段，utopia.2606的psionic_leader与marauder.101的raiding_marauder等实际目标在该上下文；全局EEP event_targets审计列表不包含这些目标，不能以全局列表为空判事件无目标。utopia.2606来自utopia_on_action_events.txt:1632，正常选项只向指定领袖添加leader_trait_psionic。本次目标50331766为commander／chief_navigator，族群102仍潜势灵能；该领袖特质在00_special_leader_traits.txt:348起具有舰队、部队及非统治者星球／星域凝聚加成，但没有建筑速度效果，实际预算变化仍须核后续真实月。不能把一个领袖觉醒作为全族灵飞终点。

本项目audit_save国家flags仅保留eep前缀，读取全部原生flag须另取country.<id>.flags原文。marauder.101的拒绝组按目标掠夺国家的marauder_1／2／3原生flag确定，国家12本次为marauder_1，正式选项为内部index3；拒绝只显示回复，已经在immediate生成的劫掠和under_marauder_attack等flags继续存在。此为本机Stellaris脚本／SAV实证，不推定CK3方言或存档。

原生死火山与研究选项（2026-10-09）：cosmic_storms_events_1.txt:3173的cstorms.1735正常选项移除d_active_volcano，矿物奖励为6个月产量、最小100最大1000（00_scripted_variables.txt:49–51）；本次实际正好+1000，不能算作EEP吞星奖励。其原生add_tech_option_or_research_effect（00_scripted_effects.txt:4893）在可研究且没有既有选项分支同时增加always_available_tech、alternatives.society中的tech_volcano和25%部分进度；本次真实F4卡片“地壳深部工程”1116/4464。last_increased_tech实际仍为tech_psionic_theory，不能用该字段判新增选项成功与否。原生after清除源星受风暴旗标，本例只移除affected_by_nexus_storm；母星及吞噬源星不变。原辅助对科技字段的两个错误假设FAIL保留，严格七项补核仅允许上述两处相同选项引用和单项部分进度。

本机4.5.2政府raw包含council_agenda_cooldowns匿名记录，与type／authority／civics／origin等同块；本轮真实跨年后仅删除agenda_evolving_society、start_date2309.02.01的完整冷却块，其余政府raw、传统AP与拥有殖民地保持。冷却日期位于真实前后日期之间，五项独立只读补核通过；只能记为与原生冷却到期一致，不能追认操作议程，也不能把整个政府raw的任何变化一概忽略。此为Stellaris本机原件，未推广到CK3。

群星SAV字符串列表读取（2026-10-09）：government.civics是带引号的国策字符串列表，不能使用本项目q.ids（只筛纯数字引用）。噬岩者原生初始政府raw实际精确含civic_hive_devouring_swarm／civic_hive_ascetic，但用q.ids误得空并产生原26项中的单项FAIL；须q.tokens逐token解引号，和实际简中UI“噬岩者／禁欲主义”独立绑定。这里的工具API限制与Stellaris存档字段对应，不推广其它Paradox方言。

噬岩者原生开局与灵飞资格（2026-10-09）：本机03_civic_governments.txt:784确有gov_devouring_swarm，正式新局原生government实际为该type／auth_hive_mind，国策石质显示替换为“噬岩者”，政府显示“噬杀蜂群”；星系预览出现unknown不能直接推断政府key无效，原生player.name也实际unknown，尚未单独证明预览字段来源。00_ascension_paths.txt:459起ap_mind_over_matter的非合成人路径要求num_ascension_perks>1并排除基因／义体／合成等互斥AP；有Shroud DLC时potential允许格式塔／机械，与无该DLC分支不同。00_soc_tech.txt:3883的tech_psionic_theory也在有Shroud DLC时允许格式塔，实际研究／传统／虚境终点仍需实机；不能把读到potential当作本路线已完成飞升。

首年原生障碍清理：01_blocker_deposits.txt:1248的d_collapsed_burrows，原生base time120、费用energy300（不是矿物300），planet_max_districts_add=-1；on_cleared以owner主体执行create_pop_group。当前噬岩者第一年度确实删除原地貌271，同时EEP制造仍0、核心1573保持；本年人口总增171不能全算出生或EEP制造。实际付款时点／准确受修正费用未逐帧采集，不由base cost声称有独立实付300证据，也不因本年低矿物库存推断该障碍花费矿物。

4.5.2殖民建立期间也存在真实Colony对象与少量人口：00_defines.txt:1939的COLONY_POPS_REQUIRED=100、:2034的COLONY_MONTHLY_GROWTH=3。当前噬岩者2204.03.02原生Planet90已owner0／colony15，colonize_date2204.01.21、人口6，Colony.last_month_growth_data的GROWTH_CAT_COLONIZATION为3，实际简中UI仍“正在殖民行星”。因此有owner／Colony和人口不等于已完成殖民；EEP入口另外要求is_under_colonization=no，不能仅用年度候选列表判可启动。此为Stellaris4.5.2原件，不套用CK3。

原生异常aianom.8（anomaly_events_AI.txt:351）唯一OK选项在from星球随机新增d_physics_2／3／4，并经00_scripted_effects.txt:2956／2979／3002向root.owner国家增加aianom_physics_depoN计数，不是科研库存奖励或科研船变量。当前正常选项实证foreign Planet164新增d_physics_3／国家对应计数1；本项目audit_save按拥有殖民地／EEP关联星球过滤planets及deposits，非己方／非EEP星球的资源须另读完整SAV roots。常规时钟中自然弹出事件后，game_paused true的接受回执不能保证随后选项确认仍保持同日：本次真实04.30→05.01且发生一次正常月结。应以实际SAV日期、真实月预算和历史记录补证，不能修改日期或重放事件。government raw中的council_agenda_progress也会正常推进，本次同一月界2011.05→2077.05而其余government／AP／传统保持；不得用整个government raw恒等代表合法政体保持。

原生先驱者cstorms.205（precursor_events_cosmic_storms.txt:1855）的正式中文“仁善信号”，属于“先驱者——阿达卡利亚”事件链，不能因命名空间简称成天气风暴。pending4的root Ship1055／from Planet388，date2206.09.18是待选到期日，实际确认日2205.05.01。正常“很迷人。”实证社会研究bank0→350；18倍月产12.475=224.55，受00_scripted_variables.txt:87～89的350下限约束。完整SAV archaeological_sites.sites新增对象4，type=site_adakkaria_the_propaganda_station／location type2,id388，原四个考古对象保持；不是EEP奖励。此同日确认后经济模块stockpile镜像完全不变，真实社会研究bank已经增加，必须读取tech_status.stored_techpoints。

噬岩者母星在档案馆zone2（原生type zone_research_unity）正常新建突触节点、研究实验室均实际400矿物／360基期，three-order同日排队0进度、其它EEP和人口岗位保持。真实buildable_planet_building字段planet=0表示Colony0，队列0的location type2,id7表示物理Planet7；不能将两种ID混用。原生colony0.last_building_changed立即变为本次建筑类型，不能把这个真实操作记录当已建成或用整个Colony块相等拒绝正常付费排队；只有精确该字段允许变化，其它字段仍严格核。本轮顺序突触节点／实验室／突触节点，总实付1200，完成与维护另验；本机特有事实不推广CK3。

第一座突触节点实际建成于后续360日端点2206.05.01，building38／zone2；母星pop_job22的coordinator实际workforce／max_workforce均360→560，维护工蜂2834→2707（同时存在人口增长，不能把差127误作恰200转岗）。另外两单仍0进度，本轮月凝聚净17.43599。先付费下单和后续真实建成、劳力入岗有各自原件，不能合并为下单时即有产出。

本机4.5.2起始科技tech_space_exploration（00_phys_tech.txt:7～18）提供feature_flag unlocks_auto_research。F4物理／社会／工程原生齿轮正常点击后，SAV精确仅tech_status.auto_researching_physics／society／engineering三个no→yes，暂停同日仍没有research_queue，完成科技与真实bank未变。正常自动选题需下一段真实日历确认；不能套历史版本的后期AI科技门槛，不能与human_ai或is_ai混为一谈。

第一次接触通知的player_event也可能保存在SAV而不作为普通居中弹窗显示；本机经F1情报日志→发现→显示第一次接触访问，first_contacts.contacts.<id>.event是当前待选、events是既有图文历史。正常first_contact_critters.80选项实证contact0的stage void_clouds_stage_1→2、status locked→in_progress、clues7→0，completed追加实际同日阶段记录，删除当前event，events历史保持；first_contact.1唯一“真是有趣。”仅删除当前event。两次human1／option0历史和完整国家经济／EEP保持另证，不把调查解锁当接触完成。

噬岩者原生完整殖民及吞噬入口（2026-10-09）：Planet90／Colony15正常从建立期人口84再经过180日到2206.11.01人口102、UI成为巢穴星球，colonize_date实际更新为完成日；不能用建立阶段旧日期误算已完整经营的年数。正常点击“吞噬星球”立即启动，没有额外确认弹窗。生产适配任务Q17/T41、progress0，源星102已有本族所以不搬种子，母星5897保持。启动会刷新经济模块科研镜像，但真实tech_status.stored_techpoints保持，须按真实bank守卫。

同一原生任务第12有效月2207.11.02实际progress12，Planet90出现2个d_lithoid_devastation、毁坏19.97882，recently_eaten_planet为前日重新置360后剩359；原始message记录MESSAGE_TERRAVORE_CONSUME_WORLD／MESSAGE_TERRAVORE_CONSUME_WORLD_ALLOYS_TEXT、receiver0／target_planet90／date2207.11.01，可证明真实随机分支为合金。不能仅凭跨年合金总差或源星人口增加猜分支／奖励数额；原版tier1materialmin100／max1000，精确合金奖励仍须与完整月预算隔离核账。此时EEP C/G0／D2／made0／worlds0，正常原生咬合不能算作EEP最终结算或额外制造。

原生first_contact_critters.85的非唯心“远观而不要玩。”内部选项index1，正常启用CLOUDS_PROJECT（实际events.special_project，scope type=colony/id0）、执行finish_first_contact_effect；实际接触对象0保留但status变finished、当前event移除，原生国家新增first_contact_completed20／void_clouds_encountered／had_first_contact。当前非proactive分支采用6个月影响力、20～80限额，预算月收入6.1753的未取整公式37.0518，但同日真实奖励634.66874→671.66874为37整数。此案例只证明实际整数奖励与EEP保持；单个数值同时兼容向下取整／四舍五入等方式，不推广为引擎通用取整规则，不追认原精确小数预测通过。

噬岩者最终补咬次数须按真实num_free_districts计算，不等于只用Q减损毁：本次Q17、6损毁、原生d_toxic_kelp−1（01_blocker_deposits.txt:356）、已有1级蜂巢区划，最终剩9槽、5条真实咬合消息。原生destroy_colony后本次Planet90仍缓存colony15，零人口Colony15对象与一些原生岗位／占位区划记录继续存在，但owner/controller已移除、国有列表不含15、所有实际人口为0、pc_shattered且地貌空；不能将“raw引用／对象仍有”直接等同有实际殖民或重复收益。原任务带killed=yes后下一月自然从集合清掉，与活动任务判断分开。

本次eep_report在国月脉冲按增长前的6470人口取快照，月首SAV实际6477；首次女王通知只显示最近回迁440等结算数，不是漏迁7人口。确认后的下一月原生增长7与全国人口净增精确相等，八类经济差等于真实last_month.balance，无EEP制造／重复奖励。

同日原生重载不能默认所有缓存raw恒等：本次首次待通知重载实际库存／bank、人口组岗位、EEP及事件保持，但government.unlocked_civic_council_slots0→4、部分预算／舒适度／civilian及carrier flags刷新；根因尚未无Mod独立对照，原严格FAIL必须保留。二次同日重载这些字段稳定，完整预算精确仅income_high_water_mark.length7→8，其它raw恒等；只证明二次重载的范围保持，不扩大为首轮或全路线严格重载通过。此为Stellaris4.5.2实证，不推广CK3存档。

2026-10-09只读重查既有真正无Mod RUN20261008T090850Z的119月原件与首次重载：预算current贸易62.98714→63.07004、维护工蜂贸易46.40794→46.49084、人口矿耗63.59→63.65、income_high_water_mark.trade125.97428→126.14008／length2→3；母星amenities25787→25820、free_amenities22737→22770、住房及crime缓存也刷新，Planet3载体flag1→3。其government原文未变。这些原件支持同类预算／舒适度／载体刷新可发生于无Mod；不证明本轮所有数值差异和议会槽位0→4的原因。旧原FAIL与其稳定二次重载结果维持原结论，不改旧审计／scope。
# 2026-10-09 待选事件日期补充

噬岩者原生2223.01.02存档4c3b036515f35e5b997312ce2e7ce900adf9a98136000352cdb6506de3e11c9a的player_event60／toxoids.500写date=2224.12.11。同期简中实际GPU悬浮priority-synchronicity-terraform-alert-ui明确“系统将于2224.12.11自动选择默认选项”，点击可打开已经出现的待选。因此此条date应按自动默认截止期理解，不能以日期在未来排除待选；其它事件仍须具体UI／原件验证，不能据一条泛化所有日期字段。本轮原21项无待选FAIL应保留，正常确认另做独立同日守卫。
# 2026-10-09 原生前哨与4.5.2经营调查

本局第一笔前哨实际扣100合金／37影响力，订单build_orbital_station_order.resources同值；原版defines00_defines.txt:2042的EXPANSION_COST_BASE=75及02_gestalt_civics.txt:265国策影响力−0.5存在，但不能把计算37.5当真实付款。第二笔兹尔克菜单实际明确37／100，原截图保留。第一站完工原生关联是country0.owned_fleets新增477→fleet477.ships1415→starbase76.station1415→system145.starbases76，同时恒星53.controller0／orbital_defence477。starbase及ship对象没有直接owner，不从缺失字段推定归属；SAV字段关联规则只用于当前群星，不是CK3语法结论。

4.5.2的synaptic_reinforcement（00_edicts.txt:654）效果为维护工蜂贸易产出+1，并要求tech_hive_cluster、凝聚力费用及维护，不能套旧版本传闻将其当即时增加凝聚。08_unity_buildings.txt的building_hive_node没有可直接逐座升级的upgrades块；building_hive_cluster是planet_limit1、需要升级首府的新建筑。当前zone_foundry的included_building_sets来自shared_industrial_foundry_zone，仅foundry／urban_automation／origin，不含unity；绿色空槽不证明可放突触节点。00_synchronicity.txt的integrated_preservation实际为自动迁移机会+0.3，collective_reasoning稳定+3／星球飞升费用−10%，不能按旧版本将前者当维护工蜂直接产凝聚。此轮仅只读调查，未启用该法令、改区划组或购买集群；实际经营选择仍须合法简中UI与付费核验。
