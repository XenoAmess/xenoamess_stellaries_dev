# 吞噬之心：噬岩者防御续验与进度

02:38 暂存原字节校验实际退出0，9,546个blob／327,664,272字节全部与源SHA一致，[暂存回执](evidence/priority-second-paid-shipyard-and-parallel-work-staged-verification-2026-10-09.json)。本轮生产41文件没有改动；提交只含当前三份文档、全新暂停快照及该暂存回执。随后继续正常离线防御验收。

02:37 全量暂停快照实际完成，captured_at_utc=2026-10-09T18:37:12.593115Z，9,512份源文件／324,335,836字节，[来源清单](evidence/priority-terravore-progress-2026-10-09/second-paid-shipyard-and-parallel-work/source-snapshot.json)。本文02:38／02:40为书写时人工分钟估计，执行／冻结的准确时刻以原始UTC回执为准，未据此扩大验收范围。仍为活动暂停端点，非退出／重载或完整路线结果。

02:40 v2当前33项全部PASS、实际退出0，源码da272ac09f276b1b0f15e2455ea10bac5f9f554df19917e467c08b69c448a93b；原v1两FAIL及原月两FAIL继续原样保留。12.02源5bc02638454cba563a6902c7b99d722a79018a922e990357feb5d1b7abce016f，五舰／十五原单、Theory484.68777＋650（43.6%），母星8935、damage16.19579，能8832.52292／净5.08692、矿7297.02547／净15.59971、凝聚4396.80259／净57.54998、合金7095.57665／净22.7468。开始冻结全部当前原件，期间保持暂停且不操作GUI。

02:38 12.02确实刷新Theory462.58704→484.68777，专项650仍在（43.6%），全部实际库存／预算／人口8935保持。通用原守卫30项中28项通过、原执行1保留：星港仅新增原始scalar update_flag=2048，其它完整字段保持，双船坞／crew_quarters不变；唯一人口组1的原生缓存power／crime35.38→35.43、housing_usage3538→3543，正好对应已出生后size3543，人口身份／数量／类别和所有其它字段保持。这里仅记录引擎保存事实，不未经验证解释update_flag各比特语义，也不算Mod生产缺陷。

通用守卫v2改进方案（实施前）：保留已执行源码与30项原FAIL，另建`priority_terravore_defense_boundary_guard_v2.py`。星港完整raw比较只允许update_flag这个原生scalar变动，实际模块／建筑／队列和所有其它字段保持；一天的人口组比较保留全部身份、size／planet／key／增长分类等，只允许power／crime／housing_usage缓存变动并逐项输出。当前12.02补核必须额外绑定原30项恰两FAIL／其余28PASS／执行1／两SHA，精确缓存值及星港仅update_flag新增2048，其余raw保持。以后新的正常区间仍复用v2独立检查，每次全新`-defense-boundary-v2-proof.json`，不能覆盖v1。调整的是跨日正确性断言，原raw与差异全部继续保存；不是把人口缓存变化当人口损失或生产Mod修改。

02:36 本轮防御里程碑冻结方案（执行前）：待12.02边界守卫实际结束后暂停一切GUI／日历，使用既有`archive_priority_checkpoint.py`把当前RUN全量原件、未过滤logs与配置复制到全新`evidence/priority-terravore-progress-2026-10-09/second-paid-shipyard-and-parallel-work`，保留本轮错误目标24次观察／原执行1、恢复0、月守卫原FAIL与独立补核、各不可变源码及全部实际SAV／GPU。目录日期沿既有工具约定，实际captured_at_utc记录10月10日北京时间；只称活动暂停端点，不称退出／全路线通过。源字节全核后精确暂存相关三份文档与该新目录，再用既有staged verifier验证Git blob；提交／push并核远端SHA，之后继续防御，不在提交后结束任务。

02:34 两处精确补核10项全部PASS／执行0，原32项FAIL完整保留；原tech_status整个raw也相同，没有队列丢失。接续方案：绑定该补核只推进12.01→12.02一天／`terravore-defense-december-research-update`，读取是否在日2刷新科研，不预先把无增量写成研究损失。

后续通用防御日历守卫方案（实施前）：新建不可变`priority_terravore_defense_boundary_guard.py`，供已授权正常日历边界重复只读使用、每次唯一输出；绑定每次checked_v2回执指定的前PASS及执行退出0、两源SHA、日期算术。原20艘付费批次的军舰数＋剩订单数始终20，订单只允许删除原队首连续已完工项，实际新增军舰数等于完工项数；所有舰船实际design67110548、满舰体250、属舰队16777797且本国owned_fleets关联，日期在原生区间内，原舰日期／design／舰体／归属保持但允许真实运动。剩订单非progress字段raw保持，工作范围0..60，queue3容量2／本国归属和星港模块保持。严格核EEP账本C37/G0/D11/made0/worlds2、唯一核心capacity11／修正／已碎无人口两源、合法政府type／authority／国策／origin／AP传统、真实科研bank／专项650和607.25288不丢失、Theory选题且进度不退。自然人口／轰炸伤害／新增地貌／真实月预算逐项报告；一天且不跨月时全实际库存／经济／人口岗位区划地貌保持，多月时不以最终月净额伪称全期间核账，净能负允许有储备但必须单列预计持续月数，所有实际主库存须正。无新增error和待选，否则保留FAIL并停止后续日历；Native敌军仍在时不宣称胜利。下一次加速最多180日，以已核规则选择边界，不替代完整路线／20年验收。

02:32 原月守卫32项中30项通过，实际退出1／原FAIL保留：`original_four_real_design_hull_held`把舰船全部scalar（含位置朝向）都当舰体不变，1564实际只改变forward_x／forward_y／rotation／speed和coordinate／target_coordinate；前三舰完整raw保持，第四舰design／hull／construction_date／fleet均保持。`Theory_selected_and_growing`在12.01仍462.58704未增加，原生队列选题／专项650／607.25288和真实bank保持，不把本月界未增直接判Mod研究丢失。八资源残差全部0，净能源5.08692、矿15.59971、凝聚57.54998、合金22.74680；未发生待选／新增error。

独立精确补核方案（实施前）：新建`priority_terravore_two_shipyards_month_supplement.py`，只读同一两SHA，绑定原32项恰上述两个失败、其余30项全部true及原执行退出1。前三舰要求完整raw保持；1564只豁免上述六个物理运动字段且坐标origin0／finite，所有其它raw字段、真实舰体250／设计67110548／日期10.13／舰队归属严格保持。社会研究整段队列raw保持462.58704、专项和真实bank保持，明确本段未观察到研究增量，不能追认原32项全通过。补核PASS后才可继续到12.02读取原生科研更新，不能重跑11天或重写原结果。

02:29 11日原生日历实际退出0，12.01后件41189f19fd40dfbd3d972420846fe7999fd0e5e8191a4cf4bd2497fd7e663130，无新增error。先只读原件再执行月守卫：新增真实护卫舰1568／舰队战力417.57812，原剩15项首15／60，其余0；维护确为7.75E／1.875A、模块收入6移除、支出1→2。实际母星8930→8935，growth_and_size明确出生5且分类GROWTH5／PROMOTION0，不能照前月固定出生6。尚未执行的月守卫按该实际分类核5，保留此原生增长变化事实；未重放日期或修改存档。

02:27 118确认31项全部PASS／执行0；双槽一天30项全部PASS／执行0，原生前两订单确为46.25／1.25，另外14项raw保持，人口8930及完整经济保持。分别后件b59e948a…／bcef3d6b…，双槽守卫SHA032c3099742773fb3b971243f4907140b80907224c60ccf665878f584c522910。

完工后首月方案（实施前）：绑定双槽30项及其执行0，仅推进11日到2236.12.01／stage `terravore-defense-two-shipyards-first-month`。新`priority_terravore_two_shipyards_month_guard.py`独立核八资源本月净额桥接（影响力1000封顶）、完整last_month等原current；舰船首单671088646完工，实际新增第五艘原设计护卫舰并核原生12.01建造日／归属／满舰体，原四舰保持，船队容量25；剩15订单顺序保持，首335544337应15／60，其余14未施工，第二船坞全部raw保持。读取并核ships新增第五舰维护0.75E／0.375A、starbase_modules太阳能收入6移除／船坞维护1→2。母星仅本月自然出生、采矿2000／发电600满员、区划／地貌不变、EEP／唯一容量11／已碎两源／AP传统保持；Theory继续科研且专项650／原607.25288与真实bank保持，无待选或新增error。实际舰船完工与月结同日，以原生预算为准；如其维护入账顺序与预测不同，保留原FAIL并只读解释，不重跑日历。

02:24 双槽实际施工方案（实施前）：118确认独立PASS及实际执行退出0后，使用checked_v2只推进2236.11.19→11.20共1原生日，另存`terravore-defense-two-shipyards-working`。新只读`priority_terravore_parallel_shipyards_guard.py`绑定确认前件、原生日历回执及源SHA；queue3容量2／16项顺序不变，首项45→46.25，第二项0→1.25，其余14项完整raw保持；两活动项仅progress变化，starbase0完整raw保持，4艘原舰design／hull／日期／归属保持且无新本国舰；当天不跨月，实际库存／预算、人口岗位区划地貌、研究进度bank、EEP账本与核心修正均应保持，无待选和新增error。正常敌方行动及轰炸伤害按实际读取，不假设敌方整个对象raw不变。此项只证明真实并行施工，不代表防御胜利。

02:16 设施完工守卫实际退出0，34项全部通过，源码SHA c5109e2dc5467fbd9d627fcb08f188397d5da05ef4e82b3518885eb24aba816c。接续118确认的具体实现（实施前）：从已执行且不修改的96确认守卫另建`priority_native_first_contact118_ack_guard.py`；前件改为上述34项PASS／b1cd2892…及其执行退出0，同日固定2236.11.19，待选118、contact32。正常UI确认后，只允许selected_history新增一次{player_event:118,human:1,option:0}、对应event及至多一条原信息消息移除；其它顶层原始序列、所有国家、其它contacts及全实际经济／人口／岗位／EEP／科技不变，无新增error。保存为`terravore-defense-contact118-ack`，通过独立确认守卫前不推进日历。

02:12 完工端点b1cd2892127398367aa32c9c7ab263cfc2ab4151e1edfcd5f4b0e4aef67cdd91／2236.11.19，167日执行退出0、无新增error。第二模块真实shipyard，queue2空，queue3.simultaneous1→2；原19单前三503316491／117440527／822083587完成，原剩16单准确保留，首项671088646进度45／60、其它0。实际本国舰队16777797含原舰16777221及新16778303／16778412／1564，建造日分别7.07／8.25／10.13，符合原单施工48日间隔，战力334.0625。自动完成tech_hyper_drive_2／tech_orbital_arc_furnace，新设计134219419只升级超空间2，旧首两舰仅标记可升级，真实design仍67110548，未支付或完成升级。

原生轰炸损失已确认对象：原district_generator level4→3，母星新增唯一d_ruined_district／33554567，发电岗800→600且600满员，维护工蜂因释放200岗位及本段出生30增加230。原版common/districts/00_DOCUMENTATION.txt:25明确毁坏区划在轰炸时默认放置该地貌，SHA0f18219b65f9e3dfcff20dce4352d23886a37f1b730f35351efa215b88813adc；01_blocker_deposits.txt:819定义该地貌最大区划−1、清除200日／300E。此变化符合原生轰炸损毁规则，EEP容量11／账本／永久修正保持，不能继续称19区划／800发电保持，也不冒称已做无Mod独立复现。当前实际18区划、母星8930，最后月8924＋出生6，损伤15.34338；ships维护7E／1.5A（4艘），能净13.57792仍正。

该端点唯一待选118／first_contact.1，scope first_contact32、from country14（商旅），原版first_contact_events.txt:12～120的唯一选项INTERESTING无效果。新增设施完工只读守卫`priority_terravore_second_shipyard_completion_guard.py`（实施前）：精确核上述付费模块完成／两槽容量、三艘原设计和建造日、旧16单及原舰保持、原生损毁唯一发电区划／新增地貌并对应600满员、EEP及实际资源／科研／出生末月／无新增error。仅允许这一个已确认原生待选，声明还未确认、不得直接推进日历；之后正常打开first_contact32并点唯一选项，同日另存和新ACK守卫严格核history118仅一次、该event／消息移除、其余first_contacts／完整经济国家／所有其它原始对象保持。两槽真正并行工作另验，不用容量2代替施工证据。

02:05 首维护月独立37项全部PASS、实际退出0（246b15468393c32d3e54d572bf43956da6fd9eaeb8d55dd4f6c025a3424cd86e），原目标失败及独立恢复同时绑定保留。实际能净36.67731／矿15.27927／凝聚63.03672／合金26.55729，八资源残差全0；首舰0.75E／0.375A维护真实应用，母星8900仅出生6，模块13／180、船舶16.25／60。当前1e686176…为可继续端点。

设施完工边界方案（实施前）：只使用checked_v2，固定前件维护37项及其wrapper退出0，纯30日历验证6月2日＋167日＝11月19日；唯一stage `terravore-defense-second-shipyard-completed`。独立完工守卫先核模块原付费704643077完成／queue2移除、starbase0第二槽真实变shipyard／crew_quarters及原槽不变、舰船queue3容量按实际原生变化和原19单来源／完工舰船归属建造日期交叉核对。预期本阶段正常完成3艘、原首舰仍存活，剩余原单不退款不重排；新的并行施工对象／进度以原件为准，不能因模块已完工就声称两个船舶槽都已实际工作。保留EEP／唯一容量11／AP传统与无重复女王，真实人口及最后一个月增长、各资源最终正余额／当期舰船维护和科研进展单列；五个多月跨度不能把当前单月budget当整个期间精确总核账，精确预算结论只适用于先前37项短月。无新增error或未解释异常才允许下一段短月证明双槽进度和完工后维护。

02:03 原24次目标检查完整退出1，原始stdout／stderr和原执行回执已形成；独立恢复实际退出0（9f3f475f0edf474e1697f498e47f422fe865d6d310a7a43e4cdcbd125442e464），未发新日历命令，保存6月2日后件1e6861769c40b8744c0985227a44fb428fb5dadf6af3721b27ce1d2e248faff1，无新增error。原生日历13天对应模块13／180、舰船首项16.25／60；十九舰船项保持。母星8894→8900，原生month_start8894／birth6，仅GROWTH6／PROMOTION0，未发生人口损失。原生ships支出4E→4.75E＋0.375A，新增军舰维护实际0.75E／0.375A；八类本月库存桥接（影响力1000封顶）残差0，last_month完整等before.current_month。Theory队列349.78725＋专项650仍未完成，轰炸damage4.39319继续。

首维护守卫具体实现（实施前）：从不可变first-month helper另建`priority_terravore_first_maintenance_guard.py`，替换为上述13日／6.02独立回执、前件付款40项PASS，保留原生月经济／EEP／真实bank／人口和矿2000电800满员检查；准确核19项ID、首0→16.25／其余18 raw保持、模块0→13且其它字段raw保持、实际舰队5容量与舰船存活、维护类别4.75E／0.375A。追加原执行退出1与新恢复退出0／两SHA绑定，严禁以新局部PASS改写原调用失败。临时只读调查末尾误将顶层匿名player列表传q.fields而报delimiter，前部已读取的库存／施工结果有效；正式待选检查继续按顶层player_event独立读取，不解析匿名player为有名字段。

01:59 日历输入防错改进方案（实施前）：另外新建不可变`formal_production_native_calendar_checked_v2.py`，保留原helper及此次失败。新版本必须在任何按键前验证原生每月30日／每年360日的日期算术、目标day1..30、唯一未执行stage、源SAV SHA和指定前件独立PASS／同SHA／其wrapper实际退出0；错误日期或重复stage立即在GUI前拒绝。只正常发一次fast_forward并核对应当次日期／原生回执再另存，输出仍仅OBSERVED，不自授Mod验收通过。日期函数独立抽取静态验证本次5.19＋13＝6.02、5.19＋12＝6.01、年界／360日及非法31日／错误目标拒绝；这些验证不调用任何GUI或推进游戏，记录原始结果后才允许未来真实日历使用。此为私有运行辅助输入校验，不涉及P引擎工具或生产Mod。

01:59 纯日期7项全部PASS／无GUI，v2 SHA66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc，原结果`checked-calendar-v2-date-validation.json`保留。恢复实现细化（实施前）：新建`priority_terravore_observe_existing_calendar_recovery.py`，输入前校验原wrapper非零／命令参数确为原13日、唯一已提交type_text和scan Enter各一次、原后续poll确见6.02暂停／13日回执、付款40项及源SHA／原error基线，调用已验证的纯日期函数；只关闭已实拍控制台并正常保存，不含type_text或fast_forward输入。新独立receipt标记为EXISTING_COMMAND_AFTER_TARGET_FAILURE，引用全部原poll／原失败SHA；任何前提不符立即拒绝操作。随后月维护守卫同时绑定新观察成功与原目标失败，不能隐去原失败。

01:58 日历目标计算错误，原执行仍在等待错误目标：母星5月19日按每月30日推进13日应到6月2日，先前方案误写6月1日。只读原poll3／4／5均显示2236.06.02、暂停、Fast Forwarded13 Days；游戏未继续运行，不重复命令。原`formal_production_native_calendar.py`按传入目标1日等待，不会得到该目标，应保留其最终失败／全部原poll；这是本次传参计算错误，不能称原Mod缺陷或已有工具执行PASS。

独立恢复方案（实施前）：待原wrapper实际非零退出、完整stdout/stderr/执行回执形成后，新建一次观察恢复helper，严格绑定该原失败／前件付款40项PASS／源SAV及本次唯一fast_forward13 action和原poll字节；验证30日历算术得6月2日，重新实拍同一生产进程暂停日期／原13日控制台回执，不发任何新日历命令。仅正常关闭原控制台并独立保存`terravore-defense-first-maintenance-june2`，保留独立限定回执，实际维护／出生／预算／模块13工作及舰船16.25工作仍需后续独立守卫；原失败不可覆盖或冒称通过。此后所有新日历输入在提交前按原生30日历验证起点＋天数＝目标，宁可停止检查而不重复推进。等待原helper退出期间仅做文档和只读调查，不同时操作GUI。

01:54 第二船坞付款守卫40项全部PASS、实际退出0（helper 2f582356e02148b91cb5c478c7bdb45bff8e97d2a1fc2bfb010e7384edd3b3ec），绑定e701bb91…→e8b6a139…。接下来唯一原生日历13日到2236.06.01／stage `terravore-defense-first-maintenance-month`，保留原始回执及error；新只读首维护月守卫核前件40项／SHA、EEP／容量11／两源碎裂／AP传统和研究保持、真实自然增长分类及八资源当月预算精确桥接（影响力1000上限）、上一月预算完整传递。原19单应仅首项从0到16.25／60，模块0→13／180；唯一本国军舰不应丢失，真实舰船维护须从原生budget_categories的ships收入／支出类别读取，不能用UI舍入或预计单价代替。原生轰炸／修复仍按实际状态单列，不因人口尚未损失称威胁解除。

01:53 实际付款观察退出0，同日后件e8b6a13983cca85c14122f694bcfeb5cfde46b77c112e6224083b97967204f2b，无新增error。合金6972.08075→6922.08075，真扣50；starbase0完整raw保持（第一船坞／第二太阳能／crew_quarters和轨道舰队），原舰船队列3保持。模块queue2原空items→[704643077]，原none687865861被同槽下一代704643077替换；新项queue2／paying_country0／progress0／needed180、resources50A、buildable_starbase_module{starbase_module="shipyard",slot1,starbase0}。只有顶层country与construction变化，country仅0的经济资源alloys，完整其它对象保持；本对科研镜像原来已不存在，无需照搬先前删除镜像的豁免。

付款只读守卫细化（实施前）：新建`priority_terravore_second_shipyard_payment_guard.py`，严格按上列唯一对象结构和句柄替换／新项验证，绑定前件首舰32项PASS、原始两SHA及单次585,588点击退出0。country0仅资源alloys变化、其它全country及除country/construction以外全部顶层序列raw保持；construction仅queue2.items及唯一none替换，新模块对象外所有items、queue3十九单、其它queues／mgr字段全部raw保持。另核所有审计人口组／岗位／区划／地貌／母星账本／flags／AP传统政府／研究／budget／有效其它库存及未过滤error相同；只证明付费订单，不称第二船坞已完工或维护已经通过。通过后先唯一13日到2236.06.01，独立检查第一舰当月真实维护、人口出生和八资源核账，再按实际进度选择第二模块完工边界。

01:51 用户要求继续执行且完成前不停，恢复实际生产RUN20261009T044016Z／PID12528，简中GPU日期仍为2236.05.19并暂停，第二模块替换菜单仍打开，未出现离线期间自动推进。接下来按既有第二船坞方案，在实拍船坞项585,588普通左键一次；逐帧确认是否弹出替换确认，实际付款后独立保存`terravore-defense-second-shipyard-paid`。前件固定e701bb91…首舰32项PASS，不能重跑购买或按报价伪造付款。当天新建只读付款守卫须绑定前PASS／真实SHA、模块队列原空2及船舶队列3的十九单raw、实际合金扣款与其它有效库存／真实研究／人口岗位／EEP保持、原模块位置和无新增error；真实建设对象结构先只读调查再精确定义，旧证据不可覆盖。最新本轮没有生产Mod代码修改，0.2.0生产内容保持，原生袭击与已复现前超光速报错不冒称新Mod缺陷。

北京时间2026-10-10 00:04。0.2.0首次发布、远端核验和Git标签已完成；七条主验收路线仅纵火本能完整完成，覆盖率1/7=14.3%，不是项目总工作量百分比。噬岩者完整路线未通过，下一条仍是铁心灭绝者。

当前正式生产0.2.0运行在2236.05.19，原始存档e701bb91415d45c21b5a56b1c0478c43c801eaf9fa6955dadfdc139396a0f290。两次自然吞星及女王通知／确认／防重已核；真实账本C37/G0/D11/made0/worlds2、唯一容量11保持。灵能理论专项650＋队列326.76808／总2600，科技完成37.6%，不是整条路线进度；完整虚境、武灾、母星转换、长期经营和严格重载归并仍待补。

原生虚空虫袭击后，正常实付1792合金排20艘护卫舰。首月31项全部通过，首舰完工32项全部通过；本国fleet16777797／ship16777221，原设计、正常建造日期、满状态、船坞轨道和本国归属均有独立校验，剩19单尚未开工。母星实际人口8894、本段库存与预算保持；默认舰队姿态实拍被动，仍会近距离交战，原生敌舰44仍轰炸母星。防御胜利及完整舰队维护未验，不将付费／首舰完工当成防守成功。

前轮9,060份源文件、306,812,136字节的[暂停端点快照](evidence/priority-terravore-progress-2026-10-09/native-invasion-and-first-paid-corvette/source-snapshot.json)已提交b9e66b0eb5b3fadfcfb0c71a79d1ddd43e68331a。普通push实际退出0，随后ls-remote核origin/main与本地HEAD同一SHA；不是依终端文本推断成功。原FAIL及精确补证均保留，生产及Workshop内容未改。

## 第二船坞调查与后续方案

目标：缩短原生袭击期间的串行造舰时间，使用真实付费设施与真实维护继续验收，不赠舰、不删敌舰、不改存档。范围是本国星港starbase0的第二模块，原第一模块船坞和已付费舰船订单必须保持。

只读普通UI调查：同日打开船坞／指令舱及太阳能电池板模块的替换菜单，尚未选择任何替换项。简中菜单显示太阳能电池板产能6，船坞报价50合金／180天；原版common/starbase_modules/00_starbase_modules.txt的shipyard从第10行起、construction_days第13行也为180。UI报价只是预计，实际扣款、施工和维护均待后续独立保存核验。单船坞每48日完成一舰的本局实证不能直接推广成双船坞的所有排队行为。

执行前验收方案：正常选择替换船坞，逐帧确认是否有原生确认窗；独立同日保存，核真实合金扣款／原生模块订单来源、原模块和原舰船队列是否保持、全实际人口岗位／EEP／科研状态及其它库存不变、无新增error。若界面仅报价或未实际下单，不称已购买。设施完工后另核第二shipyard实际存在、两施工槽的原订单分配、真实舰船生成、原生舰船与星港维护支出；按真实日历短段观察母星人口损失及原版分类，未解释异常保留FAIL并停止继续推进。

证据归档方案（执行前）：将此次六个UI操作／截图stage的原始action、GPU、OCR、执行回执和stdout/stderr复制到全新不可变目录`evidence/priority-terravore-progress-2026-10-10/second-shipyard-options`，附每份源路径／字节／SHA清单，原字节逐份检查再暂存核Git blob。该目录只含报价调查原件，不是全RUN快照，不代表模块购买、完工或防御通过；不重写10月9日已冻结快照。

00:05 实际六个stage执行回执均退出0，指向同一生产RUN；33份源文件／738,483字节已原样归档，[来源清单](evidence/priority-terravore-progress-2026-10-10/second-shipyard-options/source-snapshot.json)与[船坞替换报价原图](evidence/priority-terravore-progress-2026-10-10/second-shipyard-options/terravore-defense-solar-replacement-menu.jpg)可复核。该子集包括三份辅助源，原版模块文件SHA为edeaad451ff4aa5656650a51c94197fdb693cfb241f84dcb2be2a17149d023a5。仍未选择购买、未推进游戏日历。

00:06 暂存原字节校验实际退出0，35个证据blob／750,751字节全部匹配源SHA，[暂存核验回执](evidence/priority-second-shipyard-options-staged-verification-2026-10-10.json)。文档及该选定UI子集作为独立进度补充提交，不扩大为购买通过。

## 滚动目标窗口

| 节点 | 目标窗口（北京时间） | 当前约束 |
| --- | --- | --- |
| 噬岩者处理袭击、稳定母星 | 10月10日上午 | 正常付费造舰／设施、原生战况及月度收支 |
| 噬岩者全套复核 | 10月10日晚首个目标节点 | 灵能理论／完整虚境、武灾、母星转换和回归尚待完成，战况或自然阶段延长则顺延 |
| 铁心灭绝者 | 10月11日至12日上午 | 紧接噬岩者完成后开展 |
| 其余四条主路线 | 10月12日下午至16日 | 优先两路线延长则依次顺延；正式名称和专项范围见兼容清单 |
| 结果归并、工具复核及发布评估 | 10月17日 | 有失败继续修复，不据排期宣告完成；后续发布需新版本 |

完整范围见[官方中文名称、验收顺序与排期](civic-acceptance-roster-2026-10-08.md)。实机仅简体中文；其余九语言静态校验通过、运行时不在范围内。Steam保持离线，只在实际未来上传时上线。
