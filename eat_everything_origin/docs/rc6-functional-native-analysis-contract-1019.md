# RC6 功能原生证据：独立只读分析接口

## 范围与来源（实际样本前）

本接口配合 [执行图](rc6-functional-native-execution-map-1019.md)，不另排执行流程。主线程独占游戏/进程/UI，colossus_review 维护执行图和命令，本线程只在主线程确认实际 run/prefix 与不可变保存回执后读取原生 SAV、审计、回执、已完成动作及其截图/OCR。现在没有新功能样本输入，不解析未来前缀、不扫描活动日志，不改生产、门禁、旧 checker 或旧证据，也不创建未来 PASS。

固定候选树 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`，EXE `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。新 run 必须独立绑定其 manifest、实际保存路径、完整 SAV SHA、ZIP gamestate SHA、audit 和 native receipt；不把旧 RC4 的物理17、fleet159/ship997、q19、750/600或日期带入本轮。入口与业务结算复用不变 `tools/check_1019.py`，SHA `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`；完整严格 comparator 不设忽略路径。

本页依据旧 postfire/guard/duration 合同与冻结源码。原 `settlement` 明确只证明结算数学/持久状态，不能证明实际发射、战争、无军队；原 `no-settlement` 要求同日，并且也不足以证明无效目标前提一直成立。原脚本若遇到适用性或解析缺口，保留原拒绝/FAIL，另报告缺项，不能改原门槛来凑通过。

## 输入角色与一次解析

主线程确认实际前缀后提供该分支阶段角色到 immutable `*.native-save.json` 的映射，另列 `*.load.json`、具体输入动作与GPU/OCR路径。角色是语义，不预填文件名、日期或数值。每份 SAV 只做一次完整 observe，后续数学和严格比较复用这份已核解析及完整 hash；只有新证据、解析缺陷或未决字段才重新读。命名输出均独占创建，历史 FAIL 与即时不稳定状态另存，不能覆盖。

最小分析输入还有实际 actor、Mother/core/source 的原生 target 绑定、各物理ID和 prefiring/seed/completion 前提。数字ID与 q 从本轮 SAV 得到。机器与 Lithoid 分支分别绑定，受控夹具日期以实际 SAV 为准；经济锚点不混入人为人口、改size/deposit或成长变量探针。

## 逐类只读报告

| 分支 | 必要角色 | 独立检查与证据边界 |
| --- | --- | --- |
| 敌星 PK | clean/base、calafter、ready/queued、windup、fire-start、last-fire-day、immediate-completed、stable-completed | 保存完整 current_order 嵌套原文、真实 planet target、windup/fire counter及90/30期限；先按首次实际counter起算，不以点击日或CSV min_windup替代。前置source活/q正/战争/正确受益者/core有效/Mother非战斗和无入侵军参与单独核。最后fire29→自然完成与前90日独立分段；缓存和灭国奖励次日清理不追加为武器第31日。 |
| 取消/重放 | queued/charged、cancelled同日、actual reload cancelled；stable-completed、有效双回调后、actual reload后有效回调 | queued/cancel同日全经济五账本/容量/pop/两危机目标/receipts不新增，取消实际订单为空；源仍活。重放只用正确 DEVOURER 完成key、THIS物理源/FROM实际Mother，且源已毁并稳定清理。原命令失误或无效派发不能认证防重。 |
| 普通 q2 | owned-ready50、same-day real-decision-start、逐月progress、precomplete、immediate/stable-completed、repeat/reload | 源50→100、核心−50、合计守恒，actual seed_existing100/need0，实际Situation/q2/T5/progress0。monthly与门槛后次日自然完成从真实progress证明，不写进度。q冻结于启动，后续原生损耗不再扣第二遍。完成按该次实际基线计算 C/G/D/made/worlds/L。 |
| Lithoid owned PK | 独立Li功能ready、该银河calafter/恢复、真实90/30、prefire、immediate/stable-completed、repeat/reload | ready物理size3、真实旧 d_lithoid_devastation恰1、有效q2、pc_hive/owned/noncore/300主体人口；C0/G0/D2/made0条件需实际成立。C加2、G不增、D2/made0、G制造0、lastcapacity0。native随机收益与主体返回分账；不预定随机类别或返还R300。 |
| 9个持续 guard | 每目标ready、idle-next-day、actual reload ready后的fired-same-day | 7旧目标加真实未殖民自然宜居星、中立天然殖民星，逐目标原生前提在idle/fired都成立；core有效、FROM正确。每源用同日idle→fired跑原 no-settlement，同时保留全strict；缺对象、夹具未建立、撤掉flag才回调均不算通过。 |
| 原生colonizing/ground | 同支ready、idle、fired | colonizing真实进度/owner与is_colony联合状态，不把同名flag当原生状态；ground真实双方军队/active combat且idle/fired持续，提前结束即夹具不成立。两状态不能只凭零收益认定。 |
| core迁移/owner-loss | migration-ready、实际决议后newcore、newcore guard前后、receiver绑定/转手前后、同日guard pair | 原eep_core target从旧物理源移至新源、旧标记/deposit/capacity移除，新core actor绑定/所有权/容量正确；owner-loss时绑定仍指新物理源但owner变，旧core仍本国有人防灭国。原生capital与EEP绑定分别记录。所有core物理标记的拒绝不只看当前target。 |
| Mother death | live-before、actual destroyed/cleanup、full initialize/startup/sync后、actual monthly后、actual reload后 | 实际原fleet/ship/base消失，无新actor Mother/juggernaut；EEP授予/初始化flags与经济账本仍在，core持续可用，完整三效果实际输入有证据。tier镜像是历史，不能当仍有真实组件；不把死船dangling target当活实体。毁舰本身引起的队列/维护变化原样strict列出，不套用旧档迁移的“所有船都不消失”条件。 |

真实入口、order/decision、状态guard、结算和重载各自保留scope。不同角色若能由同一原生 SAV 合并，记录其实际SHA和角色来源；不以“共有effect”替代某个实际入口。

## 结算 case 的必填与独立预期

旧 `eep.1019.settlement-case.v1` 必填：`path=normal|colossus`、`before/after`（可选实际reload）、实际 `source_world/core_world`、`expected_q`、明确boolean `native`、`expected_return`、`expected_other_core_pop_delta`、独立 `expected_crisis_progress_delta` 与校准JSON路径/SHA、显式非负 `expected_crisis_empires_progress_delta`，非零empires还须独立正校准来源。固定源码的 Nemesis startup grant只能作为设计依据，实际AP/path仍从本轮before核对；缺失时保留旧checker前置拒绝，不额外加perk迎合工具。

- q：colossus取prefire/真实结算前源size−当时旧实体损耗；normal取启动时持久q，不能用after损耗再扣。
- R：敌方source固定0；本国Machine normal取precomplete实际合格founder groups，含真实50种子迁移后的模拟变化；本国Li colossus取prefire合格founder groups。资格按冻结 `eep_founder_pop`（含改造同种/非purge）与真实 species/group证明，不能抄 after.eep_last_return。当期未能独立判同种/合格时列缺项。
- other-core-pop：非月初最后1日可在源模型/完整阶段前提下事前声明自然delta0；跨月、组装/事件则需独立idle或原生来源。不得用 `aftercore−made−R` 残差作为 expected。
- Li native：冻结 `eep_colossus_native.txt` 的POP分支直接向bound core加100/次，不改source的R；必须从同source/date的新 `MESSAGE_TERRAVORE_CONSUME_WORLD_POP_TEXT` 原生消息或真实通知/截图独立认定被选分支，再将100×次数列入other-core-pop。矿/合金分支由实际类别证据认定其pop项0，资源实际值另列。消息缺失、R无法独立归因、自然量未明即保持人口验收缺项，不残差反拟合。
- 危机：worlds/empires读重复objective内的独立progress，用本银河原生各complete一次的校准差值，不把总menace或“次数+1”代替。empires预期基于prefire所有真实owned colony（含舰载/殖民状态）与战争/所有权前提，不把controlled矿星当owned colony。即时国家尚未cleanup的FAIL保留；stable新报告另存，随后才判重放不再奖励。若实际校准上下文有变化，先报告适用性，不能根据after奖励改预期。

原 `settlement`/`no-settlement` 的结果与独立orders/war/army/pop/native-reward补充报告并列。某个局部PASS不能自动使整个final组PASS。

## 输出接口与 finalcase 提案

新增 `evidence/1019-analysis/rc6-functional-analysis-intake-v1.json` 仅声明角色/字段/现有CLI来源，所有未来实际文件、ID、日期、运行结论和final checks为null/PENDING。收到真实prefix后分别输出 immutable observation、timeline、calibration、settlement-case与原checker report、negative-state/strict supplement、death/core report，再以已证事实提案 `colossus_enemy_fire`、`colossus_cancel_idempotence`、`common_settlement`、`normal_dismantle_regression`、`colossus_guards` 与相关 growth/reload/repeat-init单项。

final提案包含实际项目证据引用/SHA、run_ids、精确生产树、每check的原始字段/输入/报告basis以及缺项；当前不预填true，不生成final index。UI发射/菜单/通知证明只引用实际已完成图与动作，独立进程restart另依真实启动材料；不由SAV同日期或manifest存在推断。新报告也不能弱化已提交迁移v2预算或覆盖旧RC4/RC5/原生即时FAIL。
