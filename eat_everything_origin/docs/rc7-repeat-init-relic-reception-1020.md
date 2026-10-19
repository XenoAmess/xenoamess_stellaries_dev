# RC7重复初始化与同日Relic配置：接收记录

## 目标、范围、事前判据

2026-10-20主线程已完成fresh Machine全年经济worker；本线程只接收其**稳定年末原件**及随后明确通知保存完成的重复初始化、Relic配置材料。全年12个月解析／startup和economy两组由archive_review负责，此处不重复。仅离线读取已完成文件，不操作UI、Steam或Git，不读活动日志，不改Mod／工具／SAV。

候选固定`0.4.0-rc.7`、59文件树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，实际run `20261019T164112Z`；单生产Mod、简体中文及EXE SHA `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。根线程是唯一桌面操作方，接收报告必须引用真实动作／GPU、receipt／audit及原生SAV；运行结束后的完整日志尚未接收时整case保留PENDING。

## 已授权稳定输入与未来角色

| 角色 | 日期／身份 | 接收状态 |
| --- | --- | --- |
| `r7mcyearui` | 2201.01.01；fresh Machine；Mother fleet151／ship1044，物理core2；SAV SHA `41a19510e73c8e92da7d0877dc29dfbcff6ccacda66457a6a34522a9d388d2db` | 主线程已明确全年worker EXIT0、原件稳定，可只读 |
| `r7initrepeat` | 同暂停日；现有`r6_repeat_initialize`原样生产initialize／startup／sync完整串连续两次 | 已封口，原ZIP与before同SHA，四项限定通过 |
| `r7relic6` | 新参照创建后FF6，实际2201.01.07 | 已封口并接收；reference fleet175／ship1068／design16779116；原生配置20项限定通过 |
| `r7cfgui` | 同暂停日2201.01.07；root82091 EXIT0 | 有效两详情与实际维护已绑定，UI15项限定通过；jump另阶段待收 |

未来角色名不是已经存在或通过的断言；失败／重试原件各自保留。根线程stage为`r7initrepeat-effect1/2`，随后`r7cfg-create-relic`及真实FF6；只在其明确封口后按具体前缀收取，不提前glob读取正在写入的图片或动作。

## 重复初始化四项检查

事前基线为`r7mcyearui`，同日after为实际`r7initrepeat`，全部使用当前原始checker及不忽略字段的严格比较。下列四项必须逐项给结论，不能仅用“幂等”总称：

| 原发布check名 | 本轮最小核对 | 当前结论 |
| --- | --- | --- |
| `no_extra_world` | 物理世界／owned colonies及核心绑定、已有布局／人口、extra-world旗标和目标均无新增或替换 | PASS_SCOPED |
| `no_extra_ship` | 所有本国舰队／舰船的实际ID、Mother唯一性／fleet151／ship1044、设计／位置／船坞和军民舰队均保持 | PASS_SCOPED |
| `no_extra_reward` | EEP全部国家变量、六核tier／paid／pending、core容量／人口、库存、原生危机目标与定时修正无额外收益；不是只看C | PASS_SCOPED |
| `no_extra_civilian_queue` | 真实民用／星基／舰载队列及construction items的ID、付费／进度／内容、parallel queue数保持 | PASS_SCOPED |

若原严格比较发现任何变化，保留原FAIL和完整路径差异，再按实际来源解释；不通过删除缓存字段或修改检查政策使其转绿。只有实际完整两次命令动作已绑定且对应原始SAV有上述证据，才形成四项限定结论；完整repeat_initialization case仍等待本run停止后的完整日志等五类最终引用。

## 同国同日Relic与Mother配置

参照必须通过**`eep_relic_reference_1019`实际全局fleet目标**绑定。夹具fleet名`EEP_Native_Relic_1019`，不能只用`check_1019.mother`的`same_save_relic_fleets`筛`NAME_Relic`来判是否存在。取同一`r7relic6`的真实country owner、两ship／design，并与冻结生产设计和本机原版`NAME_Relic`逐槽绑定。

事前判据：原版Relic 43个section组件槽，Mother50个（共享43＋1原生PK＋6真实AUX core），各6 required；共享43的slot／template对应一致，含22个L防御槽（11装甲＋11暗物质盾）和5个原版AUX（3护盾电容＋2再生组件）；Mother新增六AUX实际存在，不把country镜像当装备。required分别按自身底盘源合同核验，Mother是真`JUMP_DRIVE_1`／juggernaut暗物质反应堆／`COLOSSUS_SHIP_THRUSTER_5`等，不能要求不同底盘required全字节相同。

本轮另核：Mother原fleet／ship身份和原有优势保持、一个实际mobile starbase及其shipyard_build_queue.simultaneous=10；国家技术／研究对象与创建前相同，没有为装配grant全帝国技术；本国其它舰队／设计及普通主宰（实际若存在）保持。若本轮没有其它普通juggernaut，明确运行时该样本不存在，使用冻结源没有override原版ship_size／全局设计的证据作为有限补充，不声称看到了不存在的实舰对照。

UI已由root采同日实际Mother和native Relic详情，并由本线程查看原GPU、核OCR／原SHA，包含三防／速度／闪避／伤害；设计／SAV能验证装配，不替代实际面板。jump的真实订单、windup、到达／冷却尚由root后续独立执行，此接收不会提前填actual_jump。

## 供电来源与实际维护接口

只复用已封存[RC6供电来源推导](mothership-power-source-derived-rc6-1019.md)的逐槽**来源合同**，不把其RC6原生船当RC7通过。此前报告`SOURCE_DERIVED_NOT_UI_MEASURED`，发电14300−消耗4557＝+9743；本轮先核当前Mother56件实际inventory（50＋6 required）与该来源合同、相关power modifier来源完全吻合，再给本轮“实际配置的来源推导余额”，并保存当前SAV／设计和引用来源SHA。若任何组件或适用修正不同，不能直接照抄+9743。

维护必须实际UI归属本轮Mother：root可在其舰船行悬停，确认“舰船维护费／维护费”及资源值；详情“打开设计器”如不可用或仍停原详情，保留事实，不用其它普通设计替代。源推导供电不是UI供电读数，设计器的预估维护也不是实际支付；国家ship_components等聚合预算不能直接分配到单舰。接口和候选坐标复用[既有供电／维护调查](mothership-power-upkeep-rc4-1019.md)，不另造getter或扩大UI矩阵。

## 接收与报告设计

每个角色验证原始receipt.archived／sha256／date、audit同SAV／gamestate日期及SHA、同目录manifest的精确RC7树／语言／EXE／profile；物理core2和Mother151／1044从新SAV重读，不只信本页预告。只读原生ZIP，不能修改源SAV或补写假的native receipt。

现有`receive_functional_1019.py template/receive`可建立本轮新intake，绑定当前接口SHA、三个实际角色和core物理2；调用原`compare`与`mother`／`growth expected_c=0`任务仅产限定观察。模板的18组status保持PENDING，缺项为null。另以独立报告明确四项初始化结论、真实Relic目标／共享43／50与required／10yards／tech隔离、实际UI与source-derived power各自覆盖范围；receiver本身不会自动认证这些UI或最终组。

当前原checker SHA `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`、inspector SHA `1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`、receiver SHA `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`。不得沿用旧RC6／旧publisher接口模板而声称本轮已接受。

## 稳定年末before的首次只读核对

已仅读取获准稳定的`r7mcyearui.sav`及其来源链，核完整ZIP SHA与主线程给定值相同、date2201.01.01、manifest SHA `603236aeedc59d2f0a0308b500ca209f589fb89e2ea5d1928c8bc04d10fedd86`、精确RC7树／版本。实际Mother fleet151／ship1044／design1844，物理core2；C0/G0/D2/made0/worlds0/L0、paid0/pending0、六tier0。实际最大H93960/A44787.6/S167310；core实际pop4859，国家人口缓存4854分别保持原义，不混作同一字段。

原`mother()`范围14个check在该before均为true（仅实际配置、三防底线和10yard）；对应实际ship1044的舰载queue58为simultaneous10、starbase queue57为1、core planet queue0为2，construction items为空。该观察不代表Relic／UI／jump／维护／新阶段已经完成，也不替代archive_review的全年经济组。

## 初始化阶段封口后的接收实施范围

root先明确`r7initrepeat*`全部封口、native UI save完成，after原ZIP与yearUI完整SHA相同；worker转另一个`r7cfg`前缀后才接收本段。建立`docs/evidence/1020-rc7-repeat-initialization-v1/`：after SAV／receipt／audit与该前缀全部44份已完成GPU／OCR／action原字节归档，`* -text`、逐文件SHA和独立复读核验；before及manifest／工具源用canonical引用／明确路径映射，不复制Machine全年。最初私有归档预检查错误预估43份并在复制前停止，随后核实完整实际清单44份；未丢弃或覆盖证据，不涉及Mod／引擎问题。

原`check_1019.compare`实际执行，两个严格check全true、difference=[]，没有忽略字段；两个原ZIP（582932字节）及gamestate完整相同。两条实际submitted action分别UTC18:19:43.566901／18:19:58.670521，文本均与原`r6_repeat_initialize`精确一致，均有物理Enter scan28记录。由完整native end-state同字节与原严格报告联合支持上表四项，不靠仅计数／C变量抽样。整`repeat_initialization` case仍PENDING，尚缺本run结束后的完整日志及最终共同审查，不填写整组PASS。

before三件套／manifest直接引用`docs/evidence/1019-rc7-economy/machine/`，20个当前源码引用通过Machine source closure（SHA `3991e5e08f5dec24cbf221eab790a71028826a733cc2ceeebde33e56dc057989`）复用Pu／growth canonical，全部逐SHA与当前源码核对；只复用源码字节，不继承Machine纯经济执行声明。root session62567的本段scope单独写在新报告。receiver新template和实际bound intake仅准备，未执行receive、不宣称receiver PASS；原`check_1019 compare`已真实执行，不为相同证明再重复parse两份SAV。

- [四项限定报告](evidence/1020-rc7-repeat-initialization-v1/repeat-initialization-report-v1.json)，SHA `6183f75af8ca68575e3a535b0817e275a97e45314943e9a8746e6701f79e47c3`。
- [部分case提案](evidence/1020-rc7-repeat-initialization-v1/partial-case-proposal-v1.json)，SHA `307617a875e188458ce013087cd981f5bfdd766022c26f6861e6bc4117b5aff2`，四check true／case PENDING。
- [归档索引](evidence/1020-rc7-repeat-initialization-v1/archive-index.json)，SHA `39e8fec2415ec672d6ff065eff6687d5581140e74132fe5a04f05eab56d838b5`，52 payload／2599218字节、44原始payload、26 canonical refs；加index／verify共54文件。
- [独立逐字节复读核验](evidence/1020-rc7-repeat-initialization-v1/verification-v1.json)，SHA `0cd0dfc2907ce2c8476dbb6106612b26a499551f20cc4a455c12581f06bef00d`，9／9限定检查通过。

接着root已明确`r7cfg-`创建／FF6／close及`r7relic6*`保存完成、worker EXIT0，允许离线接收。读取范围精确限定`r7cfg-`（带连字符）及`r7relic6`，排除root新阶段`r7cfgui*`与`r7jump*`，后两者仍等待其独立封口信号；不读取活动日志。未操作UI／Steam、未改工具／Mod／Git。

Relic阶段拟建立`docs/evidence/1020-rc7-relic-configuration-v1/`，仅该两已封口前缀的原始文件、原mother checker报告、同日两实际设计及来源推导分析／partial提案。before引用上述repeat-init canonical，不重归档经济。原版／Mod组件源先核已封存power bundle的每件原SHA与当前适用来源一致，存在同SHA canonical时只引用，不复制整套原版。此阶段先交原生装配／来源计算，尚未收到的UI／跃迁／实际维护留null；后续实机新材料另新版本报告，不覆盖限定v1。

root随后明确`r7cfgui*`全前缀封口、worker82091 EXIT0，UI后新SAV SHA `c9d8907c2ebeee3380cc0668cd20e950ac73f48dd6646a3d8a83cd35b5a7caf5`、date2201.01.07，现允许一并接收／归档。有效详情是Mother `r7cfgui-mother-details-clean-v2`与Relic `r7cfgui-relic-details-clean`；Mother v1所谓clean实为第二层crisis遮挡，以及前两次未真正选舰的原帧都保留为输入／遮挡尝试，不能计有效详情。新增原strict same-day比较`r7relic6`→`r7cfgui`，保留全部实际差异；两份配置UI及实际维护分别绑定同日native身份。

root现场报告维护为energy10.07／alloys2.88、tooltip修正−75%，功能海容365／66含新参照250；这与源码−1不等同，验收不宣称免维护或零维护。须看原GPU后再绑定报告。此阶段继续排除尚活动的`r7jump*`；case缺真实jump和终态logs，保持PENDING。

## Relic原生／UI接收完成

实际`r7relic6.sav` SHA `1181ebbae4c00a6affd66c579bebaf54280726274a514b6ed134ef73ee230eff`，2201.01.07、country0；Mother fleet151／ship1044／design1844、reference fleet175／ship1068／design16779116，global reference唯一绑定成功。Mother50、Relic43个section组件共享43逐槽精确相同，各6 required按本身原版底盘合同匹配；22个L防御槽、原五AUX、六真实成长core／PK及10yard均成立。原`mother()`14项限定通过，其`same_save_relic_fleets={}`原样保留；并未改筛选器。

创建前后28项已完成technology／level完全相同，Mother实际design／C0及六tier0不变；但Jan1→Jan7整tech_status有真实三科bank增长：222.08696／258.80696／222.08696→240.53952／280.31952／240.53952。完整差异保留，不拿整块恒等做错误前提，也不修改原checker。

源推导已重新绑定当前56件实装与26份已封存来源，全部当前SHA相同；重新搜索本机原版／当前Mod全部TXT仍是27个非本舰适用power赋值，无适用power add／mult。产生14300、消耗4557、**source-derived +9743**；没有UI功率数字或私造getter。本轮实际inventory／scope状态与RC7新SAV绑定，未继承RC6实机通过。

| 2201.01.07同国同日实际面板 | H | A（显示整数） | S（显示整数） | 速度 | 闪避 | 每日伤害 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Mother | 93960 | 44787 | 167310 | 417 | 22.1% | 5598.57 |
| native Relic | 20000 | 30740 | 138352 | 225 | 22.0% | 2373.28 |

原生精确A为Mother44787.6，原生Relic S138352.5，面板整数截断单列。有效Mother图为`r7cfgui-mother-details-clean-v2.jpg`（SHA `05943ebe60152e07978eedaa8597c97a49fcebaf3152c81af251370de5da2f7f`），Relic图`r7cfgui-relic-details-clean.jpg`（SHA `c00d8d3f95126daf3ef8703f641fc04893684b6d36a874e9c81ea53c7175dc3c`）；两个原图均已实际查看，全部数字与OCR、日期及原生身份对应。

实际Mother维护tooltip经原GPU确认：energy10.07／alloys2.88；“友军光环”下“舰船后勤维护费−75%”也保留其实际名称，不能把不同修正通道与源码`ships_upkeep_mult=-1`混为一项，更不能声称免维护。参照tooltip另图保留，但未显示明确维护金额，不据缺行推断参照0维护。此时海容365／66含夹具参照250，只属于后置功能分支，不回填纯经济。

## UI真实副作用与严格比较边界

原`check_1019.compare(r7relic6,r7cfgui)`实际执行，原选取gameplay字段＋1019字段严格PASS_SCOPED、0diff，没有改工具或删字段。但另外对ZIP全部member／原生全部顶层重复字段按name＋occurrence做完整比较，发现**gamestate不相同，10个根记录变化**（原283根→277根，全部顺序和full raw diff保留）；meta相同，不能把原限定PASS外推成全部原生状态只读。

- country0新增`tech_alloys_1`研究进度165、可用备选／always_available及`research_option_added`／`StoryFirstRewardGiven`／`first_contact_protocol_event_happened`旗标；已完成28项技术未变。原版`story_events.txt:2101–2117`的Machine选项使用`add_tech_option_or_research_effect TECH=tech_alloys_1 PROGRESS=0.1`，after置奖励旗标；实际选择history中的story.7 option10、原点击／图已归档。这是后置原生事件奖励，不是母舰装配grant科技或开局经济补贴。
- 关闭`crisis.4140`后启用`CRISIS_SPECIAL_PROJECT_MACH_1`并增加链counter `crisis_level_reached=1`；原版`nemesis_crisis_events.txt:904`起对应option明示该效果。没有完成项目或据此宣称危机阶段提升。
- 原生message／player_event移除与剩余event记录顺序变化、实际selection history新增、random_count9882987→9882989全部保留。原strict projection不包括这些事件及单项技术进度，因此其0diff只适用于原声明的选取范围。

没有将以上真实原生副作用抹去或标成无变化；它们不使已先封存的纯经济重算，也不归因为Mod故障。两份新需原版事件文件在本项目无同名已封副本，故只复制这两个相关原文件；其它54个canonical引用复用既有原字节，不复制整套安装。

私有诊断第一次用未容纳引号的regex扫描SAV ship_size，错误得到零juggernaut；`OBSERVATION_ONLY` v1原件保留，v2改用现有native growth-stage解析器，真实全局只有ship1044。另一私有断言把空`ship_sizes`目录误当有定义，改为核冻结manifest确无该路径的文件。没有因此改Mod、原checker、power系数或预算。不存在其它普通juggernaut实舰时不编造负对照；partial提案的`other_juggernauts_unchanged=null`留root按源隔离范围决定。归档复读的首次私有遍历还混用index内部bundle-relative与canonical的EAT-relative基准而停止，后按两类既定路径基准分别核验，未改引用SHA／原件。

交付`docs/evidence/1020-rc7-relic-configuration-v1/`共166文件：164 payload／8794308字节，148原始阶段payload（r7cfg- 23、r7relic6 18、r7cfgui 107），54 canonical；原生20、UI15项均为限定PASS。

- [限定配置／UI报告](evidence/1020-rc7-relic-configuration-v1/bounded-configuration-ui-report-v1.json) SHA `f88c1387231c579f6170c59f596b32a0a892d7fa8760cc029c9934f2a04a9b46`。
- [本轮来源推导供电](evidence/1020-rc7-relic-configuration-v1/source-derived-power-report-v1.json) SHA `aa4d9de70fa7f7ee14a1159e4405eebb8acef9940811589dc96ad0ab1a5f8802`，`SOURCE_DERIVED_NOT_UI_MEASURED`。
- [部分case提案](evidence/1020-rc7-relic-configuration-v1/partial-case-proposal-v1.json) SHA `6867f5e5561fc5b971359ec05f8d6a38aae24af594a7249d09c2a7cac10860f9`；case PENDING，actual_jump／other_juggernauts_unchanged仍null，缺完整终态logs。
- [原生完整差异](evidence/1020-rc7-relic-configuration-v1/ui-full-native-raw-differences-v1.json)与[原strict限定结果](evidence/1020-rc7-relic-configuration-v1/ui-same-day-strict-compare-v1.json)并存，不互相覆盖。
- [归档索引](evidence/1020-rc7-relic-configuration-v1/archive-index.json) SHA `aaa439d71053b207d3b92801d27f462b5187e1a6207e80f3d25016300ec42523`；[独立复读](evidence/1020-rc7-relic-configuration-v1/verification-v1.json) SHA `3f609b092447893a76762ccea7cb1bbb913d805208219fb333965c239aebce4e`，15／15限定检查、391个typed refs核对通过。

至此本线程两小包封口，可分别提交；未读取`r7jump*`或活动日志，未操作桌面／Steam／Git，未改Mod／工具。真实jump由root下一阶段补证。
