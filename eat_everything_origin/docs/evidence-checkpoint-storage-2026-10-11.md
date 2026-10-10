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
