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

03:13 第三个v2切点 native-killed-cleanup-naval-cache-and-sixth-paid-pair 冻结于2026-10-10T19:10:27.975682Z，完整21013源项／816259775字节，复用20644项、新增369项／17809061字节。独立暂存原字节校验PASS／实际0，核21073唯一blob／840383057字节，[回执](evidence/priority-native-killed-cleanup-naval-cache-and-sixth-paid-pair-delta-staged-verification-2026-10-11.json)。V10与V11各原单项FAIL、V11／V12／V5全部源码和实际退出、死亡三端点与第六对出生SAV及两简中过程图完整纳入；基线a61b13c1／其v2清单精确绑定。当前五相关docs／新切点／回执提交推送，远端待核；暂停11.25不等于全路线完成。

02:49 第二个v2切点 native-three-paid-mines-and-v10-defense 已冻结于2026-10-10T18:47:15.657627Z，完整20644源项／798450714字节；复用20168项，新复制476项／22684137字节。独立暂存原字节校验PASS／实际0，核20703唯一blob／822085830字节，含已冻结复用原件、基线清单、准备输入及历史回执；[回执](evidence/priority-native-three-paid-mines-and-v10-defense-delta-staged-verification-2026-10-11.json)。新增三矿付款、V10／V4源码和逐日原件均在清单，旧切点不变；当前五相关docs及本切点／回执进入提交推送，远端待核。游戏仍在2268.11.13暂停，未把切点校验宣称为全路线验收。

02:08 四docs／新切点／回执共413暂存路径及cached diff check实际0，已提交6e1c37d0cecacbcca81d378b84117300b9fdc245；push实际0、独立ls-remote实际0／远端main完整SHA一致。首个v2切点已交付，后续可用本已提交manifest作为新基线继续平铺复用；不再更改本冻结目录。生产Mod与公开0.2.0保持，后续游戏观察仍独立验收。

02:00 已完成两个独立助手，当前游戏在2268.11.01暂停、27项检查PASS／实际0，开始首个native-low-hull-daily-recovery-and-delta-proof切点；基线固定为上述6d9aa5f9与manifest SHA。尚未声称归档或暂存校验通过。

02:01 归档实际退出0，冻结时间2026-10-10T18:00:58.031647Z。完整源清单20168项／775766577字节；复用19762项，实际新增406项／19464086字节，数量及完整字节总和一致。当前仍暂停，下一步独立校验全部实际暂存blob（含复用原件），未宣告校验或远端成功。

02:04 独立暂存字节校验PASS／实际0，20168源项完整核准，20226个唯一blob／794351331字节（含准备输入、基线manifest及历史回执），[独立回执](evidence/priority-native-low-hull-daily-recovery-and-delta-proof-delta-staged-verification-2026-10-11.json)。另独立枚举当前暂停RUN／日志／四配置，实际20168路径与manifest的20168原始source路径集合完全一致，未列出／缺失均0、实际退出0。首轮同时覆盖原件复用与新增复制，未改旧原件；现在只提交四相关docs／本新切点／回执，推送与远端核验待下步。
