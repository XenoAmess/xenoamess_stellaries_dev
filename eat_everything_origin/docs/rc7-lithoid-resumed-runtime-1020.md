# RC7 石质蜂巢剩余验收执行记录

最终补充：同EEP05、同EXE及同预设字节的真实0.3.1新局已正常保存/退出；新旧
母星本族人口均5300，物种/portrait/traits/政府/起源/国策相同。旧版另有赠星，
不混入母星人口比较。原生档、19份停机日志、CRC/receipt/GPU原件已归档至
evidence/1020-lithoid-population-baseline-v1，最后population_preserved检查通过。
首个离线比较误用另一inspector的nested结构而KeyError，未写报告/索引；改按
实际flat结构读取，原SAV不改。RC8实机通知修正及两段幂等另有独立限定证明。

本局Feb4已经实际windup0/90。首个操作断言失败是读取层级错误：计数在
destroy_planet_order.sub_order.planet_killer_weapon_windup_order内，外层order_id
本局为0，旧敌星多次排队后为2；该值不是充能/发射阶段号，不能照搬为2。
后续只按实际嵌套类型及windup/fire计数推进，外层order_id仅检查同一订单保持。
此修正只影响临时操作读取，不修改原检查器或原失败记录；没有额外推进日期。

己方菜单实际可用，Feb2原生queued明确destroy_planet_order/planet12；Feb3仍是
move_to_system_point_order，native路径ETA为Feb4，不能把这一天算作充能。
后继逐档核原生order_id/windup/fire后才推进：到达后0/90、89/90、90/90且fire0、
fire29/30，在最后一天前停住写独立预期。若阶段不符即停，不盲目FF120。

## 本轮干净首月实际结果

EEP05实际新局Jan1与Feb1已原生保存，原startup检查器23项全部PASS_SCOPED。
母星pc_hive，district_hive_2=4且无食物district_hive_3；发电工蜂实际workforce1200。
初始能源200，首月净电+80.9787，只有一个殖民地且自动吞噬关闭；Jan1 core人口5300、
Feb1为5306。舰船和组件能源维护分别8.62043与9.03522，建筑/区划等正常维护仍在。
人口基数尚待同EEP05旧版本实际新局对照，不能由这些数字提前判通过。
首月原件独立封存后，才执行Feb2的size3/loss1自有源功能夹具。

沿既定 branch map，仅运行独立 EEP 05 石质蜂巢干净新局与首月，之后再构造
size3、一个真实 d_lithoid_devastation 的自有非核心行星，执行原生拆解射击。
不重启已停止自然战役，不增加第四个全年经济矩阵。实际数据产生后再追加。

目标为八项首月检查，以及自有非核心原生射击、q 扣损耗、Lithoid 原生路径。
新局与首月先封口，夹具、校准、射击和随机原生奖励单独记账。验收须包含
真实 90/30 时序、无入侵军、prefire founder groups 独立返回预期、C+2/G不增、
制造为零、容量不增、原生随机奖励与自然人口分列，及一次结算／重复／重载。
已有英文等九语言仅静态校验，运行时不在范围内。

## 人口基数的缺口及处理方案

已核旧 baseline run 20261019T053917Z 的完整经济矩阵只有 Hive/Machine/Purifier，
没有同 EEP 05 预设石质蜂巢初始档；不能直接拿有机 Hive5300 或繁荣统一5700
当石质 EEP 的实测基数。生产开局源码未调用删母星人口，仍需实际同预设基线。

当前 RC7 功能分支全部保存、当前 run 正常停机并冻结后，复用既有
single-homeworld-20261019 的不可变 baseline-gate（公开0.3.1，树
abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8），
用其原 prepare/launch/new_game 创建新的隔离中文 baseline run，只采同一
EEP 05 原生 Jan1 初始档。该 run 不加入 RC7 runs、不冒充候选测试；原包先核
open_kaishek PASS 及逐文件 SHA，再启动。旧版本额外赠星人口不计母星损失。
只比较两份新局真正 core 的 founder groups、物种／政体／起源与开局链。

基线完成后正常退出、冻结并归档。若同预设基数实际不相等，保留失败并调查，
不得临时调人口或放宽标准。旧启动工具全保持原字节，不为此重跑已有三类全年。

## 执行前静态复核

已在当前候选UI分支之外，只读复核原0.3.1 baseline包全部文件与原gate一致，
并重新调用现有open_kaishek accept_stellaris_mod入口：24/24脚本、12 DDS、
101本地化键，结果PASS。新报告与源清单归档至
`evidence/1020-rc7-lithoid-baseline-preflight-v1/`。这只是旧基线包输入静态校验，
没有启动新基线实机，不代替候选Lithoid首月／射击或人口基数比较。

## 原生射击的日期与人口预期

干净首月封存后，允许在功能准备中先自然推进一天再排队，尽量让90/30结束日
落在非月初，避免把月脉冲人口增长和返回／随机原生造人混合。具体仍从原生
windup/fire计数和native日期计算，不预填射击开始或完成日期。prefire必须先
固定founder groups返回R、原生损耗1及有效q2；若最后一天确实不跨月，结合
本机已验证的月度人口规则独立事前声明自然核心人口增量0。若实际最后一步
跨月，则另取独立自然人口对照，不能由after总人口残差反推或临时更改预期。
原生随机人口必须另有通知／消息的实际证据，矿物／合金奖励也照实分列。

若最后一次bite随机产生人口，事前期望采用显式分支表：每条原生POP奖励通知
对应core额外100；矿物/合金通知对应core额外0，资源量由原生消息/源码与原档
另列。prefire先固定bite数、R、自然增量和各分支允许值；完成后只按实际原生
消息选择分支，不从core人口残差推算。原settlement的other_core_pop_delta包含
这项独立原生奖励，EEP的manufactured仍必须0；完整期望在最终一天前封存。

己方源完成后的重复派发可使用已验证原生on_action的短输入，源明确为
eep_reg_owned_source、FROM为本局eep_mothership0，先核pc_shattered与五收据。
这是功能夹具的源别名适配，不是执行正例完成；正例必须由实际90/30自然完成。
重复前后同日及真实加载后的SAV交原no-settlement，不覆盖严格差异。

校准实测world750/empires600；已真实重载准备档，两个objective恢复为0、全部EEP
账本及两星实际人口保持，原no-settlement九项通过。先前离线脚本把完整world缓存
也要求全等而AssertionError；差异实际是重载重算的housing/amenities与新colony的
species_refs/job资格缓存，完整strict差异保留，不将这次过宽离线断言写成通过。
首次UI准备因原生化身天灾介绍弹窗遮挡完整源标签而在右键前拒绝操作，没有派发
射击；依实际中文按钮确认原生介绍后继续。两个失败尝试保留原件。
