# 离线验收证据切点的原字节复用

## 目标与范围

长期实机验收每次完整切点约756 MB，当前D盘可用3762925568字节。后续继续保留全部SAV、原始失败、截图、未过滤日志、配置和执行回执，但避免反复复制相同原件。只新增私有归档与Git暂存校验助手，不改生产Mod、P引擎验收工具、游戏、旧冻结目录或旧校验器；不清理既有证据，不使用指向活动RUN的硬链接。

首个复用基线为已提交并独立核准远端的6d9aa5f906d2eae5137efa9094411c24e75bae28，目录native-report210-and-bounded-defense-reinforcements，其source-snapshot.json的SHA为d650e19a9f2a8056efdef1fa269f1a868485047649148cf79907e8915c72e5bb。新切点仍为暂停运行状态，不能替代退出、重载或路线完整验收。

## 方案

archive_priority_delta_checkpoint.py接收唯一新标签、基线标签和固定基线commit。先核基线manifest原字节与该commit的Git blob一致，且commit为当前HEAD祖先；目标目录必须不存在。复制自身及配套校验助手到RUN后，与既有全量归档一样独占GUI／RUN写入窗口。逐一读取当前全部RUN、userdir日志及四份配置，记录原路径、相对文件名、字节数和SHA。

同相对文件名若与基线的大小／SHA相同，重新核基线实际原件字节，记录指向已冻结原件的仓库相对evidence_path；不同或新增者复制到新切点并逐字节核对。每条evidence_path必须解析到本仓库的priority-terravore-progress-2026-10-09证据树内。新manifest使用active-run-partial-checkpoint-v2，平铺列出全部源文件和实际原件路径，另记录基线commit／manifest SHA、完整源文件数／字节、实际新增存储数／字节及复用数。后续可用已提交的v2基线，其平铺路径直接继承，不递归推测内容。旧原件缺失、变化、Git基线不匹配或未知路径均FAIL，不自动重建或覆盖。

verify_priority_delta_checkpoint_git.py独立读取新manifest，核所有源条目计数／总字节、无重复相对文件名、路径约束、基线manifest与固定commit绑定，并通过git cat-file --batch逐个比较实际暂存blob的字节数及SHA。覆盖全部源文件（包括复用原件）、新manifest／属性文件、准备输入及历史priority回执；仅重复路径去重读取，计数分别报告源条目与唯一blob。对复用条目还核基线中的同名条目／实际原件路径／大小／SHA一致，确保不存在未声明的复用。输出独立PASS回执后才能提交新切点。

## 验收标准

先完成当前既有单日批次并暂停，实际创建一个唯一新切点；核完整源清单、实际新增与复用之和、每个原件来源及未过滤日志齐全。只暂存本任务文档／新切点／新回执，独立暂存字节校验PASS且实际退出0，提交推送并核远端完整SHA。所有旧完整切点及源码保持不变，生产文件和版本不变；任何校验失败保留原件、不得宣告切点交付或继续并行写RUN。

## 结果

04:35 第六切点及七任务docs／回执共456路径已提交af0fbce1ee913f5edeb0aabf70175c57d89556bb，cached diff check／commit／push／独立ls-remote均实际0，远端main同完整SHA。旧冻结原件保持不变，后续后方升级观察及RUN新回执属于下一切点。

04:34 第六v2切点独立暂存原字节校验PASS／实际0，完整22046源项、22109唯一blob／888851729字节（含复用原件／基线／历史回执）均核准，[回执](evidence/priority-native-two-platform-completions-and-order-generation-reuse-delta-staged-verification-2026-10-11.json)。仅七任务docs／本切点／回执进入提交推送；远端核准前仍暂停，生产Mod与既有冻结原件不变。

04:32 第六v2切点`native-two-platform-completions-and-order-generation-reuse`归档实际退出0，冻结2026-10-10T20:31:37.702059Z。完整22046源项／863570073字节，复用21600、新复制446／19749240字节；基线fd7720055428de96701108b5ec8376b23a2ad8e5及manifest SHAb185391dd77ea56c41ae0977bee16005f7d9e3b7d41b52a2a2da373331476d12。含两实际付费平台、原V16单FAIL／V9actual1、V17／V10全部源码及退出、正常第八九对出厂和简中平台／殖民UI。当前2269.03.25暂停，独立暂存原字节校验待执行；七任务docs／新切点／回执提交推送、核远端后才推进后方完工前日。生产Mod和旧冻结原件不变。

04:07 第五切点及七份任务 docs／回执共 284 路径已提交 fd7720055428de96701108b5ec8376b23a2ad8e5；cached diff check／commit／push／独立 ls-remote 均实际 0，远端 main 同完整 SHA。冻结原件不再改写，后续 RUN 新增属于下个切点。

04:05 第五切点独立暂存原字节校验 PASS／实际退出 0，21600 源项、21662 唯一 blob／868686121 字节全部核准（含复用原件、基线与历史回执），[独立回执](evidence/priority-native-battle-retreat-and-postbattle-paid-birth-delta-staged-verification-2026-10-11.json)。当前七份任务 docs、新切点和回执准备提交推送；生产文件不变，暂停快照不等于重载或完整路线验收。

04:03 第五个 v2 切点 `native-battle-retreat-and-postbattle-paid-birth` 已生成完整 manifest，归档进程已结束；冻结时间 2026-10-10T20:00:07.225799Z，21600 源项／843820833 字节，复用 21326 项、新复制 274 项／12537515 字节。基线为已核远端的 d97fc617310d343c4ed2664e418e8ad9b6c45a9c。本次覆盖战斗撤退、原 V13 单项 FAIL、V14／V15／V8、战后第七对付费护卫舰及简中战报图片。下一步独立校验暂存原字节；在校验结束前不写 RUN、不操作游戏。原归档调用输出在上下文切换时丢失，不能据此补称其进程退出码；以已生成清单和独立逐字节检查作为交付依据。

03:36 第四v2切点及六相关docs／回执共322路径已提交d97fc617310d343c4ed2664e418e8ad9b6c45a9c，push实际0、独立ls-remote实际0且远端main同完整SHA。冻结目录不再改写；后续新原生日历属于下一切点。

03:35 第四个v2切点native-two-paid-platforms-and-bounded-three-day-defense冻结于2026-10-10T19:32:43.150080Z，完整21326源项／831283318字节，复用21013、新复制313项／15023543字节。独立暂存原字节校验PASS／实际0，核21387唯一blob／855807903字节，[回执](evidence/priority-native-two-paid-platforms-and-bounded-three-day-defense-delta-staged-verification-2026-10-11.json)。覆盖两平台正常付款27项、V13首33项／常规32项、V6／V7源码及所有端点／战损／UI／日志，基线d3b4e1a9及清单精确绑定；当前六相关docs／本切点／回执提交推送，远端待核。生产Mod和旧冻结原件不变。

03:14 第三个v2切点和五相关docs／回执共377路径已提交d3b4e1a994f2ec077b72b17baeb368fbace2233a，push实际0，独立ls-remote实际0且远端main完整SHA一致。冻结目录保持不变；后续正常经营调查与日历属于下一切点，未改公开0.2.0或完整推荐范围。

03:13 第三个v2切点 native-killed-cleanup-naval-cache-and-sixth-paid-pair 冻结于2026-10-10T19:10:27.975682Z，完整21013源项／816259775字节，复用20644项、新增369项／17809061字节。独立暂存原字节校验PASS／实际0，核21073唯一blob／840383057字节，[回执](evidence/priority-native-killed-cleanup-naval-cache-and-sixth-paid-pair-delta-staged-verification-2026-10-11.json)。V10与V11各原单项FAIL、V11／V12／V5全部源码和实际退出、死亡三端点与第六对出生SAV及两简中过程图完整纳入；基线a61b13c1／其v2清单精确绑定。当前五相关docs／新切点／回执提交推送，远端待核；暂停11.25不等于全路线完成。

02:49 第二个v2切点 native-three-paid-mines-and-v10-defense 已冻结于2026-10-10T18:47:15.657627Z，完整20644源项／798450714字节；复用20168项，新复制476项／22684137字节。独立暂存原字节校验PASS／实际0，核20703唯一blob／822085830字节，含已冻结复用原件、基线清单、准备输入及历史回执；[回执](evidence/priority-native-three-paid-mines-and-v10-defense-delta-staged-verification-2026-10-11.json)。新增三矿付款、V10／V4源码和逐日原件均在清单，旧切点不变；当前五相关docs及本切点／回执进入提交推送，远端待核。游戏仍在2268.11.13暂停，未把切点校验宣称为全路线验收。

02:08 四docs／新切点／回执共413暂存路径及cached diff check实际0，已提交6e1c37d0cecacbcca81d378b84117300b9fdc245；push实际0、独立ls-remote实际0／远端main完整SHA一致。首个v2切点已交付，后续可用本已提交manifest作为新基线继续平铺复用；不再更改本冻结目录。生产Mod与公开0.2.0保持，后续游戏观察仍独立验收。

02:00 已完成两个独立助手，当前游戏在2268.11.01暂停、27项检查PASS／实际0，开始首个native-low-hull-daily-recovery-and-delta-proof切点；基线固定为上述6d9aa5f9与manifest SHA。尚未声称归档或暂存校验通过。

02:01 归档实际退出0，冻结时间2026-10-10T18:00:58.031647Z。完整源清单20168项／775766577字节；复用19762项，实际新增406项／19464086字节，数量及完整字节总和一致。当前仍暂停，下一步独立校验全部实际暂存blob（含复用原件），未宣告校验或远端成功。

02:04 独立暂存字节校验PASS／实际0，20168源项完整核准，20226个唯一blob／794351331字节（含准备输入、基线manifest及历史回执），[独立回执](evidence/priority-native-low-hull-daily-recovery-and-delta-proof-delta-staged-verification-2026-10-11.json)。另独立枚举当前暂停RUN／日志／四配置，实际20168路径与manifest的20168原始source路径集合完全一致，未列出／缺失均0、实际退出0。首轮同时覆盖原件复用与新增复制，未改旧原件；现在只提交四相关docs／本新切点／回执，推送与远端核验待下步。

### 后方星港与首付费矿区切点：实施前范围
拟新唯一标签native-rear-starport-and-first-paid-mining-completion，基线native-two-platform-completions-and-order-generation-reuse／已核远端af0fbce1ee913f5edeb0aabf70175c57d89556bb。目标冻结所有活动RUN、日志和配置，包括后方04.13真实完工、V18缩进误比原FAIL、V19成功、V11后续、首矿05.01真实完工、V20内部刷新标记原FAIL、V21首40PASS与简中UI原图。仅使用现有delta归档/暂存字节核验助手；无Mod改动。整个归档与独立暂存检查期间暂停GUI/日历/RUN写入。验收为完整manifest逐源SHA、独立暂存所有blob PASS/actual0、仅相关文档/新原件提交推送、独立核远端SHA；暂停切点不代替退出重载或完整路线。

05:11 第七v2切点冻结于2026-10-10T21:09:57.298110Z，22386源项／877527573字节，复用22046、新复制340／13957500字节；归档actual0。独立暂存原字节校验PASS／actual0，22450唯一blob／903265846字节，见[独立回执](evidence/priority-native-rear-starport-and-first-paid-mining-completion-delta-staged-verification-2026-10-11.json)。所有后方／首矿完成证据、两次私有观察器原FAIL和修正成功及中文UI保留；相关五docs／新切点／回执准备提交推送。后续新V12及续推原件进入下轮切点。

05:30 第七切点348相关路径已提交2a2afa5778ef9f64f86f765814e887277cd7140e，push／独立ls-remote实际0、远端main同完整SHA。下一第八唯一v2标签native-paid-births-budget-cycle-survey-and-leader1-error，基线native-rear-starport-and-first-paid-mining-completion／2a2afa5778ef9f64f86f765814e887277cd7140e；目标覆盖V12/idle10、idle11原V21日志FAIL/外层actual1、V22换行常量FAIL、V23首42PASS、V13/idle12、首矿预算17PASS、真实贸易容量UI与亚蒙中文源。仍完整源manifest与独立暂存blob核验；归档/核验期间不动GUI/日历/RUN。所有新原件及五任务docs提交推送后核远端，再继续预计08.21边界，不能修改冻结旧切点或宣称完整路线。

05:33 第八切点归档actual0，冻结2026-10-10T21:32:00.959582Z，22675源项／890708108字节，复用22385、复制290／13183205字节。独立暂存原字节检查PASS／actual0，22740唯一blob／916810368字节；[独立回执](evidence/priority-native-paid-births-budget-cycle-survey-and-leader1-error-delta-staged-verification-2026-10-11.json)。五任务docs及新切点／回执提交推送，旧原件保持；不宣称严格零原版错误或完整路线通过。


### 第九切点实施前计划（10月11日06:14）
第八切点已提交27e1ce458bc65870eb67f0491279295ca1d6632b，push与独立ls-remote均actual0、远端main同完整SHA。新唯一标签native-yomon-paid-outpost-and-early-transit，基线native-paid-births-budget-cycle-survey-and-leader1-error／上述commit。目标为2269.10.01暂停端点固化完整源manifest，范围包括idle13全系调查／第13对舰、正常报价图及唯一支付、付款V1异常/V2准备失败/V2原FAIL/V3独立22PASS、V24与V14、09.29第14对出生及10.01的42PASS、原始日志和全部实际退出。私人助手缺陷与原生错误原件一并保留，不据此宣称整路线完成。
使用既有不可变archive_priority_delta_checkpoint.py与verify_priority_delta_checkpoint_git.py；完整源逐条绑定既有冻结原字节或新复制原字节，独立git暂存blob校验必须PASS/actual0。归档及字节核验独占期间不进行GUI／日历／RUN写入。仅本次四任务docs、新切点、独立回执纳入提交；push后独立核远端main完整SHA，再继续唯一三日开工边界。不得修改旧切点或把暂停归档称正常退出/重载验收。

第九切点归档actual0，冻结2026-10-10T22:15:53.323192Z；23055完整源项／907084528字节，复用22674，新增381／16384728字节。独立暂存原字节核验PASS／actual0，23121唯一blob／933569806字节；[独立回执](evidence/priority-native-yomon-paid-outpost-and-early-transit-delta-staged-verification-2026-10-11.json)。仅四任务docs及本新切点／回执提交推送，既有冻结原件保持。下一仍须独立核远端后才派唯一三日开工边界。

### 第十切点实施前计划
待当前最后两艘付费护卫舰的唯一idle16及V26独立核验全部PASS/actual0后，在2269.11.07暂停端点归档；若异常则先调查，不为取得计划端点重跑日历。新唯一标签native-yomon-percent-construction-second-mine-and-final-paid-births，基线native-yomon-paid-outpost-and-early-transit／f38cb76077001394cf8051eeb0abc746edca4a1d。范围包含抵达初始化V25首43PASS、实际施工1→2%及简中UI证据、V26/V15固定源码/真实退出、第二矿完工满员住房和末对付费出生，以及本轮用户整路线约60%的低把握工作量/12—24小时排期说明。不得把工程估算替代合同通过率或扩大工坊推荐。
沿用既有完整manifest复用及独立暂存blob检查，两个工具actual0且回执PASS才提交。冻结/核验期间不动GUI/日历/RUN；仅五任务docs、新切点与独立回执提交推送并核远端。旧切点及生产41文件0.2.0保持。之后继续当前殖民预测完成前日2269.12.30边界，再单独一日核实际殖民完成，不强跑旧still_colonizing观察器。

第十切点归档actual0，冻结2026-10-10T22:33:37.292074Z；完整23269源项／916952535字节，复用23055、新复制214／9868007字节。独立暂存原字节核验PASS／actual0，23336唯一blob／943782397字节；[独立回执](evidence/priority-native-yomon-percent-construction-second-mine-and-final-paid-births-delta-staged-verification-2026-10-11.json)。五任务docs及新切点／回执提交推送并核远端后，再继续唯一idle17；原件冻结后不追加写入。

### 第十一切点实施前计划
第十切点已提交b8959e3229a36f995c3e159de1f41fa6d522260f，push与独立ls-remote均actual0、远端同完整SHA。新唯一标签native-yomon-outpost-completed-and-colony-forecast-rollover，基线native-yomon-percent-construction-second-mine-and-final-paid-births／上述commit。目标暂停于2270.01.13/V27首44PASS/actual0，完整保存idle17/18、原殖民预测01.01未兑现与新02.01简中UI、两批真实回返字段/原生MIA类型保留、前哨99%→完整归属链/模板实体化、V27执行源码和全部原始日志/退出。不把预测和计划时间当完成，不扩大完整路线/推荐范围。
沿用既有完整manifest原字节复用与独立暂存blob校验，两个工具actual0且回执PASS才提交推送核远端；归档/核验独占期间不动GUI/日历/RUN。仅五任务docs、新切点与独立回执提交；旧冻结原件/生产41文件0.2.0保持。核远端后才实施V16并执行唯一idle19到01.30，不提前启动新正常殖民订单。

第十一切点归档actual0，冻结2026-10-10T23:02:14.059458Z；完整23633源项／934155819字节，复用23268、新复制365／17211730字节。独立暂存原字节核验PASS／actual0，23701唯一blob／961333893字节；[独立回执](evidence/priority-native-yomon-outpost-completed-and-colony-forecast-rollover-delta-staged-verification-2026-10-11.json)。五任务docs及新切点/回执提交推送并核远端后，才实施V16并继续唯一idle19；不修改已冻结原件。

### 第十二切点实施前计划
第十一切点已提交99b3e6097b0e0b919df8bbf6aba8af2b726c3370，push及独立ls-remote实际0/远端完整SHA核准。新唯一标签native-colony-completed-and-third-devour-started，基线native-yomon-outpost-completed-and-colony-forecast-rollover／上述commit。暂停2270.02.01，范围包括V16/idle19、真实殖民完成/建筑killed保留/V28单FAIL与V29 46PASS、简中完成/吞噬入口图、唯一第三源决议及同日SAV、V1 raw别名单FAIL/V2 35PASS、原库存/科研镜像/负月净经营事实与全部原始日志/实际退出。
沿用既有完整manifest原字节复用与独立暂存blob校验，归档/核验期间禁止GUI/日历/RUN写入。两个工具actual0且回执PASS后，仅五相关docs、新切点和独立回执提交推送并核远端。旧冻结原件与生产41文件0.2.0保持。不把暂停切点当重载验收，不扩大推荐或完整路线数。远端核准后才继续正常母星清障报价与订单。

第十二切点归档actual0，冻结2026-10-10T23:44:35.055566+00:00；23837完整源项／942951756字节，复用23633、新复制204／8795937字节。独立暂存原字节校验PASS／actual0，23906唯一blob／970468897字节；[独立回执](evidence/priority-native-colony-completed-and-third-devour-started-delta-staged-verification-2026-10-11.json)。全部首次失败与后继成功原件保留；仅五相关docs、新切点和回执提交推送核远端，当前生产0.2.0未改。

### 第十三切点实施前计划
第十二切点27af1de8d9dc08807c48934887348511b981c1f6已push及独立ls-remote实际0/远端SHA核准。新唯一标签native-three-mines-budget-clear-work-and-colony-quote，基线native-colony-completed-and-third-devour-started／该commit。暂停2270.05.15，冻结清障300E付款V1墓碑误报原FAIL/V2 17PASS、V30 raw类型异常/实际1/V31 49PASS、V17/18调度与三矿实际全完工、吞噬首14日/月时序、原生自动迁移、清障工速V32 50PASS/V19、全三矿30日预算16PASS、白绮吞噬CG原图候选、亚蒙正常物种375M150A报价、全部原始日志/退出和完整源manifest。下一殖民尚未付款，不把报价图当订单。
沿用既有delta完整原字节复用与独立暂存blob校验；归档/核验期间不进行GUI/日历/RUN写入。两个工具actual0且回执PASS后，仅五相关docs、新切点/独立回执提交推送并核远端，之后才正常点击殖民。旧冻结原件/生产0.2.0不改，当前非完整路线/重载验收。

第十三切点归档actual0，冻结2026-10-11T00:22:49.143818+00:00；完整24298源项／962330322字节，复用23837、新复制461／19378566字节。独立暂存原字节核验PASS／actual0，24368唯一blob／990236193字节；[独立回执](evidence/priority-native-three-mines-budget-clear-work-and-colony-quote-delta-staged-verification-2026-10-11.json)。旧原件保持，五相关docs/本新切点/回执提交推送并核远端后，才继续同暂停日期下一正常殖民。

### 第十四切点实施前计划
基线第十三切点native-three-mines-budget-clear-work-and-colony-quote／959f20ef0623bb61b472bacde64d501319106611已push及独立核远端actual0。新唯一标签native-yomon-colony-and-heavy-conversion-paid。待当前唯一idle23全部独立核验后暂停（若异常，先调查、保留原始FAIL，不重跑）；冻结亚蒙523原生375M150A实际付款17PASS、母星800M实际重工业付款14PASS、两次正常确认/新订单/none槽换代/科研镜像与住房解释、双民用首工作1.33/1日V33 56PASS/V20及后续逐端全部原件。该切点不包含未实际完成的重工业/殖民，不扩大推荐或完整路线数。
沿用现有完整source manifest复用与独立暂存blob原字节校验；归档/校验独占期间不动GUI/日历/RUN。两个工具actual0且PASS回执后，仅五相关docs、新切点/回执提交推送并核远端；原冻结原件、生产41文件0.2.0保持。远端核准后，再唯一单日核敌舰预计2270.07.07返场实际状态，不将预测当返场、不强跑旧MIA守卫。

第十四切点归档actual0，冻结2026-10-11T00:54:21.081447+00:00；完整24547源项/973863649字节，复用24298、新复制249/11533327字节。独立暂存原字节核验PASS/actual0，24618唯一blob/1002182068字节；[独立回执](evidence/priority-native-yomon-colony-and-heavy-conversion-paid-delta-staged-verification-2026-10-11.json)。原冻结文件未追加；仅本轮五相关docs/切点/回执提交推送并独立核远端后继续原生单日。

### 第十五切点实施前计划
第十四切点已提交178848862fa2c3737793cdf1d7634514fbb9234f并push及独立ls-remote实际0/完整SHA核准。新唯一标签native-first-annual-consumption-clear-completed-and-heavy-work，基线native-yomon-colony-and-heavy-conversion-paid/该commit。待首年度下一日独立PASS/actual0后冻结，若未知FAIL需调查则先冻结失败。完整保存敌825实际预测日期仍MIA/次日返场、源人口200/216及岗位分配、清障272真实swap/重工首日1.4、V34以后全部观察/驱动/逐月SAV/原始日志退出、年度12/29/两毁损/20破坏度/100合金与科研单端账、V39 target路径TypeError原actual1及V40 65PASS，下一日科研/破坏恢复实际结果；不重复原生日历/订单，也不扩大推荐范围。
沿用现有完整source manifest原字节复用和独立暂存blob校验；归档/核验独占期间不动GUI/日历/RUN。两个工具实际0且PASS回执后，仅五相关docs、新切点和独立回执提交推送核远端，旧冻结文件及生产41文件0.2.0保持。远端核准后再适配后年度预出厂阶段，殖民船出生边界须单独核准。

第十五切点归档actual0，冻结2026-10-11T01:53:58.862445+00:00；完整25214源项/1005796939字节，复用24546、新复制668/31942003字节。独立暂存原字节校验PASS/actual0，25286唯一blob/1034652438字节；[独立回执](evidence/priority-native-first-annual-consumption-clear-completed-and-heavy-work-delta-staged-verification-2026-10-11.json)。旧原件未追加，下一先提交推送并核远端，再执行已记录的唯一殖民船出厂前边界。

### 第十六切点实施前计划
第十五切点f3e33a7bc4f6d5f257bb78acfd54de8c00fa0cb9已push及独立ls-remote实际0/完整SHA核准。新唯一标签native-colonyship-born-and-postannual-job-reallocation，基线native-first-annual-consumption-clear-completed-and-heavy-work/该commit。暂停2271.03.16、V44首67PASS/actual0；因年度后首次未知岗位分配提前冻结，完整保存出生前359.1/订单none/新舰和原生航线、V42 raw名字缩进单FAIL/V43首65PASS、V25与首月65项2FAIL/实际1/未派发第二步、原生后勤factor10完整源/同282人口岗位重分配/V44首67PASS、两轮Git实际退出、所有原始日志/源码/SAV/原始错误，不遗漏失败，不把正常殖民舰宣传成矿物舰。
沿用完整manifest原字节复用与独立暂存blob检查；归档/校验期间不动GUI/日历/RUN。两个工具实际0且PASS回执后，仅五任务docs/新切点/独立回执提交推送核远端，旧冻结原件和生产41文件0.2.0保持。之后再实施V26并继续重工业出厂前推进，不缩减完整路线/语言范围或扩大工坊推荐。

第十六切点归档actual0，冻结2026-10-11T02:13:14.557007+00:00；完整25350源项/1012376797字节，复用25213、新复制137/6588709字节。独立暂存原字节校验PASS/actual0，25423唯一blob/1041706904字节；[独立回执](evidence/priority-native-colonyship-born-and-postannual-job-reallocation-delta-staged-verification-2026-10-11.json)。当前只读失败/后继成功原件均完整保留，提交推送并核远端后再推进。

### 第十七切点实施前计划
基线第十六切点native-colonyship-born-and-postannual-job-reallocation/da7f04ea5e388790c5603b975b6fba7b7da91428，已push及独立完整SHA核验。新标签native-heavy-completed-and-rear-shipyard-paid。重工真实完成，殖民任务未自动恢复，UI不可达；目前正常付费一座后方船坞，尚未完工。待首工速及首新月预算独立检查完成后暂停冻结（若出现需先处理未知FAIL则提前冻结），保留V26/idle30各端和原FTL单FAIL/原V45 NameError及V46/V47、固定pyflakes包与全部源manifest/静态退出、全部恢复UI尝试及原生不可达、当前route blocker只读JSON、后方50A实际付款/首18单FAIL与19PASS及全部后续原始SAV/日历/未过滤错误/源码/退出，不能漏失败或把当前殖民路线称恢复。
沿用全manifest原字节复用/独立暂存Git blob检查；归档与校验期间不动GUI/日历/RUN。actual0及独立PASS后只提交五任务docs/该新完整切点/回执，push后独立ls-remote完整SHA，再继续真实船坞完工和后方正常军事补充。生产仍同41文件0.2.0，完整路线仍1/7，当前变更仅经营验收和证据，不称Mod修复或追加工坊发布。

第十七切点归档actual0，冻结2026-10-11T03:17:33.946849+00:00；完整25886源项/1031039110字节，复用25350、新复制536/18662313字节。独立暂存原字节核验PASS/actual0，25960唯一blob/1060761738字节；[独立回执](evidence/priority-native-heavy-completed-and-rear-shipyard-paid-delta-staged-verification-2026-10-11.json)。本轮全部原始失败/后继成功/静态包与图像候选均已冻结，生产未改；提交推送并独立核远端后才继续已记录的一格发电报价。

### 第十八切点实施前计划
基线第十七切点native-heavy-completed-and-rear-shipyard-paid/0a9e8555d10ae1df5f40ba7632d7160da3f8297d，已push及独立完整SHA核验。新唯一标签native-generator-paid-and-second-war-battle-boundary。暂停2271.08.02且首V51独立82PASS/actual0，冻结两Git原退出、七发电正常单次付款/后置报价按钮误解记录/18PASS、首1.4日V50 80PASS、双建设driver原源/静态/首30日calendar0/80三FAIL/driver1/未派发step2、全新战斗与退休建筑换代JSON、V51原源/静态/82PASS、所有原始SAV/UI/OCR/未过滤错误/stdout/stderr/退出与完整source manifest。生产41文件0.2.0保持，不称新Mod修复或完整验收。
沿用既有完整manifest原字节复用和独立暂存Git blob检查；归档/校验期间不动GUI/日历/RUN。两个actual0且独立PASS后仅本轮五任务docs/新切点/回执提交推送，并独立ls-remote完整SHA；之后才执行已记录唯一一日08.03校准，不重启旧双建设批量driver或重复任何购买/日历。旧冻结原件保持。

第十八切点归档actual0，冻结2026-10-11T03:44:01.396132+00:00；完整26035源项/1037658223字节，复用25885、新复制150/6628101字节。独立暂存原字节校验PASS/actual0，26110唯一blob/1067778649字节；[独立回执](evidence/priority-native-generator-paid-and-second-war-battle-boundary-delta-staged-verification-2026-10-11.json)。原80三FAIL和新82PASS均完整冻结，提交推送并核远端后再执行唯一单日。

### 第十九切点实施前计划
基线第十八切点native-generator-paid-and-second-war-battle-boundary/47d50ba9d5793d1debaa9af38472eb10de378302已push及独立完整SHA核验。新唯一标签native-second-outpost-capture-and-supremacy-quote。暂停2271.08.11且V53首85PASS/actual0；完整保存两Git原退出、08.03省略零字段V51原82两FAIL/V52 83PASS、所有逐单日SAV/83PASS/driver1与V2/source/static、外围真实capture238报告/原调查JSON/原83两FAIL/driver1及未派发step2/V53源/静态/85PASS、全部未过滤日志/命令stdoutstderr/实际退出，以及传统F4科技/F3真实传统/空组/至高6467悬浮报价/原版完整源。尚未购买至高，不把报价或源码效果当实际舰容提升。
沿用完整manifest原字节复用与独立暂存Git blob检查，归档/校验独占期间不动GUI/日历/RUN；两个actual0及独立PASS后仅本轮五任务docs/新切点/回执提交推送核远端，再执行唯一正常采用。旧冻结原件和生产41文件0.2.0保持，本轮非Mod修复、非完整路线。

第十九切点归档actual0，冻结2026-10-11T04:15:13.719437+00:00；完整26430源项/1055805438字节，复用26035、新复制395/18147215字节。独立暂存原字节校验PASS/actual0，26506唯一blob/1086247791字节；[独立回执](evidence/priority-native-second-outpost-capture-and-supremacy-quote-delta-staged-verification-2026-10-11.json)。原零字段FAIL/后继83PASS、真实失守FAIL/后继85PASS与正常至高报价均完整保留，尚未购买；提交推送核远端后继续。

### 第二十切点实施前计划
基线第十九切点native-second-outpost-capture-and-supremacy-quote/c3d2662c1bd0cb641555b5f9e956f4013ccaa6d4，已push及独立完整SHA核验。新唯一标签native-paid-supremacy-capacity-and-inner-outpost-battle。待当前唯一10.13诊断日实际结束并暂停、原V54和pending调查保存后，完整冻结：两Git原退出；至高正常点击/确认/单笔6466.21278/19PASS/原源静态/原生135131 UI与首单日85PASS；全civics/source；新双建设driverV2/source/static/首30日85PASS与第二30日原三FAIL/driver1/未派发step3；103实际battle调查、旧1090原生恢复/report到期、V54源静态/原87PASS；两假小行星pending原scope与首次截图/原版完整来源/正常一次选择265、36PASS及所有导航/无第二选项/仍pending264；本唯一诊断日实际结果，包括任何FAIL或未知变化，不预设通过或原生重复已消除。全部SAV/UI/OCR/未过滤错误/命令原stdoutstderr/实际退出和私有静态草稿回执均不漏。
沿用全manifest原字节复用/独立暂存Git blob校验；归档与校验独占期间不操作GUI/日历/不写RUN，两个actual0且独立PASS后仅五任务docs、新切点、回执提交推送并独立ls-remote核完整SHA。生产41文件0.2.0保持，未新增Mod或P工具缺陷；完成切点后继续103逐日战斗、后方船坞出厂补兵清路、第三吞噬/真正武灾矿物舰与长期重载，非完成路线/非新公开发布。

第二十归档actual0，首独立校验actual1：新RUN内native_selected_history import产生__pycache__/native_selected_history.cpython-314.pyc已纳入完整manifest，但默认git add受忽略规则影响未暂存该原件。该轮验证还在git add子进程实际退出前启动，流程顺序失误须纠正；不能凭启动调用当完成。原失败和完整报错另存回执。先确认git add实际0，再仅对本唯一新切点目录git add -f，等待实际0，然后重新执行只读独立校验并保存实际结果；不是重跑GUI/购买/日历，也不改原失败。所有manifest原件都必须进索引，不删pycache或缩范围绕过。

补齐切点pycache并等待git add -f实际0后，第二校验actual1指出新建的首失败回执本身尚未暂存。只读核源码确认校验器还遍历evidence根目录所有priority-*.json，因此新增任何任务回执均须先暂存。第二原失败另存，先明确暂存本轮五docs和两失败回执、确认实际0，再第三次独立只读校验；期间不新增未暂存回执、不动GUI/RUN。两次均为本任务归档执行顺序/暂存遗漏，不能写成Mod或P验收工具缺陷。

第二十切点归档actual0，冻结2026-10-11T04:58:47.256812+00:00；完整26758源项/1069588391字节，复用26429、新复制329/13792435字节。补齐两次暂存遗漏后第三次独立原字节校验PASS/actual0，26837唯一blob/1100461470字节；[独立回执](evidence/priority-native-paid-supremacy-capacity-and-inner-outpost-battle-delta-staged-verification-2026-10-11.json)。原暂存失败回执一并保留；未重复游戏日历或购买，生产未改。提交推送核远端后继续已记录V55与第三战短步。

### 第二十一切点实施前计划
基线第二十切点native-paid-supremacy-capacity-and-inner-outpost-battle/1b2c2dcabc77d93f3104c255a75288194af505d6，已push及独立完整SHA实际0核验。新唯一标签native-inner-outpost-capture-and-capacity-ledger。待当前唯一10.24校准实际结束/暂停且V56实际结果保存后，完整冻结：两Git原退出；V55未执行SyntaxError草稿与最终静态0/原89PASS；第三战3单日89PASS/原driver/source/static、健康3日校准89PASS/单日critical1三段89PASS、原capture单日89三FAIL/driver1/未派发下一日；完整103归属/report245原调查/同原SAVV56 91PASS/原源静态/单日10.24实际结果；真实至高后30日维护/月账15PASS及完整源码/静态/执行；所有SAV/UI/OCR/原未过滤错误/stdoutstderr/实际退出及原生来源。任何新FAIL/未知边界也完整记录，不预设10.24通过或全路线完成。
归档/校验独占期间不动GUI/日历/不写RUN。沿用完整manifest复用与独立Git blob校验；从一开始仅对本新切点目录git add -f（包含被忽略的原始pycache），等实际0后再暂存全部本轮任务docs及存在的新priority回执，等实际0才启动独立校验，期间不创建新的未暂存priority回执。两个actual0且独立PASS后补回执/五docs、检查任务范围、提交推送并独立核远端。旧切点原件不改，生产41文件0.2.0/Steam离线保持；核远端后继续船坞11.03候选真实出厂与补兵清路，不能以归档替代后续验收。

第二十一切点归档actual0，冻结2026-10-11T05:27:46.309721+00:00；完整27133源项/1087127457字节，复用26758、新复制375/17539066字节。按顺序force仅本切点并暂存五docs后，首独立原字节校验PASS/actual0，27213唯一blob/1118417033字节；[独立回执](evidence/priority-native-inner-outpost-capture-and-capacity-ledger-delta-staged-verification-2026-10-11.json)。本轮未重复购买/日历，原89三FAIL与91后继PASS、真实30日维护均保留；提交推送核远端后继续已记录V3建设边界。

### 第二十二切点实施前计划
基线第二十一切点native-inner-outpost-capture-and-capacity-ledger/6ddf14f0b8e24d5f9a151dfc98bd9482354b14eb，push与独立完整SHA实际0已核。新唯一标签native-rear-shipyard-completed-and-six-clearing-ships-paid。待当前V60首日观察实际退出并暂停后，冻结：两Git原退出；V3/source/static与原唯一前缀拒绝actual1/无GUI/新label4实际8日91PASS；原11.03船坞完整native差异/source/退休订单与section武器重排调查、V57两FAIL实际1/同原SAV V58 94PASS；正常打开船坞/护卫舰真实报价截图OCR/当前完整设计与quote manifest；六正常click各actual0/唯一同日SAV/101.5每单609总付款/原28PASS；首11.04原生日实际0/所有原始SAV/UI/OCR/1.58工作/发电172.2；V59 UndefinedName静态0但原KeyError actual1且未生成proof、V60新源静态及实际结果，不预设其通过。原全部stdoutstderr/退出/未过滤错误及新source原件一并保留。
归档与校验独占期间不动GUI/日历/不写RUN；沿用完整manifest复用与独立暂存Git blob原字节校验，先仅对新切点git add -f并等待实际0，再暂存全部本轮五docs及存在的新priority回执并等待actual0才验证；期间不新建未暂存priority JSON。archive actual0及独立PASS actual0后补最终计数、提交推送/独立ls-remote核完整SHA。生产41文件0.2.0不变/Steam离线；此为船坞完成、六单真实付款与首日造速证据，尚未六舰出生/维护、清路殖民恢复或真正武灾矿物舰，不能提升为整路线通过。切点核远端后继续首舰出生前观察及新出生边界验收。

第二十二范围追加：首日V60原98单prior-SHA FAIL/actual1与V61分离ledger_pre后新source/static/实际结果一并冻结；不得遗漏后发现失败或把V59/V60写成通过。当前游戏仍同一11.04，未再推进。

第二十二归档actual0，冻结2026-10-11T06:14:22.940412+00:00；完整27379源项/1096762986字节，复用27133、新复制246/9635529字节。首次独立暂存原字节核验PASS/actual0，27460唯一blob/1128420774字节；[独立回执](evidence/priority-native-rear-shipyard-completed-and-six-clearing-ships-paid-delta-staged-verification-2026-10-11.json)。原V57两FAIL、V59 KeyError、V60单SHA FAIL与最终V61 99PASS及六付款28PASS均完整冻结；未重放游戏操作/未改生产Mod。提交推送并核远端后继续已记录首出生前30日观察。

### 第二十三切点实施前计划
基线第二十二切点native-rear-shipyard-completed-and-six-clearing-ships-paid/98a2f5be1e0436b720694e01f858c9e1fc469148，push及独立完整SHA实际0核验。新唯一标签native-mother-defense-and-first-rear-corvette-birth。待当前唯一12.12原生日及V65实际结束并暂停后冻结：两Git退出；首30日12.04 calendar0/原V61 99六FAIL1；母星防御报告247原文/4→2敌实体/两MIA/目标30/war1真实battle enemy2损/16本国军raw调查；V62静态/101单FAIL1及V63静态/103PASS、12.05单日/12.10五日全部实际结果；首12.11单日原生出生/唯一117441817/fleet16778073/原订单none/5余单/归属/真实140naval/库存未重扣的完整调查；V64原105两FAIL1/V65新source/static/106PASS、所有实际校准结果（不预设本12.12通过），全部SAV/GPU/OCR/未过滤错误/source/stdoutstderr/实际退出及任何新异常完整保留。
归档与独立校验独占期间不动GUI/日历/不写RUN。沿用完整manifest复用及独立暂存Git原字节校验：新切点git add -f等actual0、五docs和存在的所有priority根回执暂存等actual0、才独立验证；期间不创建未暂存priority JSON。archive actual0+独立PASS actual0后记录最终计数/提交推送并独立ls-remote核完整SHA。生产41文件0.2.0/Steam离线保持，本轮未修Mod或P工具。之后继续发电完成/年度/后方清路与真正矿物舰；另先只读核后方直接殖民和真实科研扩建是否能减少原殖民船长途受阻/物理研究储备等待，未先假定新航线可达、未购买或取消现有订单。


第二十三切点归档actual0，冻结2026-10-11T07:00:00.175128+00:00；完整27593源项/1107935924字节，复用27379、新复制214/11172938字节。首次独立暂存原字节核验PASS/actual0，27675唯一blob/1139869494字节；[独立回执](evidence/priority-native-mother-defense-and-first-rear-corvette-birth-delta-staged-verification-2026-10-11.json)。原V61六FAIL/V62一FAIL/V64两FAIL及最终V65 106PASS、真实母星两敌损/首普通舰出生/次日1.58均冻结；无生产Mod修改。提交推送核完整远端SHA后继续已记录只读经营优化。
