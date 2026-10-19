# RC7 功能原生证据的离线接收与最短采样

## 目标与范围

本页先定义新的离线工具 `tools/receive_functional_1019.py`，不另建 UI 执行器。继续使用 [RC6 功能执行图](rc6-functional-native-execution-map-1019.md) 中已经核对的原生入口、39条旧片段及16条补充片段；不改 runtime、growth、生产 Mod、gate、旧 checker、历史报告或存档，不操作游戏、Steam、进程、活动日志和 Git。主线程提供 RC7 的实际 run、frozen tree、prefix 和固定 receipt 后才读取相应 SAV。当前所有 RC7 运行事实 PENDING，本文不填写未来日期、数字 ID、q、随机结果或 PASS。

RC6 成长预算的已知新事实由主线程确认：未显式指定 `while.count` 时实际止于100，而预期单次200。RC7 将显式写 `count=200`。该源差异不把 RC6 `R300/P110` 诊断改成 `R400/P10`，也不替未来 RC7 原生样本认证预算。成长 reporter 仍由其原负责线程维护，本工具不修改其代码或数值政策。

## 接收合同与工具设计

输入 schema 为 `eep.1019.functional-intake.v1`，显式给出 `expected_run_id`、`expected_tree_sha256`、`expected_version`、manifest 路径和 SHA、每一语义 role 对应的原生 receipt 路径/SHA 与 SAV 路径/SHA、需要完整抽取的物理 `world_ids`。跨进程恢复可另声明 `additional_run_ids` 并在恢复 role 指定该实际 run 的 manifest 引用；所有 run 仍必须是相同显式 tree/version/EXE/语言，不能自动接纳目录中的其它run。同一 SAV 可以承担多种角色，角色不是多做一次 UI 保存的要求。未知的字段保留 null；没有固定 receipt 的文件不会被自动发现或读取。工具不轮询目录、不按 prefix 猜文件、不读日志。

原生 UI save receipt 与原生 autosave receipt 均须是实际已固定的对象，包含精确 `archived`、`sha256`、`date`。UI save 必须还具有 `written_at/history`；autosave 必须具有 `source/command_started_ns/source_mtime_ns`，且 mtime 晚于真实推进命令。不能把 autosave 写成有原生菜单保存，不能用相同 SHA 的另一名称 receipt 代替本角色回执。所有 receipt、SAV、manifest、audit 的 SHA 与角色对应关系在解析前核对。

工具只导入原 `check_1019.py` 及其纯只读依赖，按原 SHA 锁定，不导入 runtime/UI/发布模块。每个唯一 SAV+manifest+所需 world 集合完整 observe 一次；缓存 envelope 绑定 observation 本身的 SHA、原 SAV/manifest/checker/inspector SHA 与 world 集合，重用前重新核对文件和缓存内容。相同字节的多个角色可以共享解析，但每个角色的精确 receipt 仍独立核对。缓存失配、源文件变化、缺字段、未知 task、未填 expected 值均拒绝，不能默填0或覆写缓存。

支持的离线任务只有原 `mother/growth/compare/no-settlement/settlement`。settlement case 仍采用原 `eep.1019.settlement-case.v1`，只把其 before/after/reload 由实际 role 转成对应原 SAV 路径；q、R、other-core-pop、两危机目标预期及校准证据必须独立填齐，原函数和严格 comparator 完全不变。每个 task 分别保留原始 FAIL 或 PASS_SCOPED；接收总报告始终是 `OBSERVATION_ONLY` 或 `INCOMPLETE`，不将任何局部 PASS 自动填入18组最终检查。

每个已解析 role 附完整 Mother `current_order` 原文、fleet/ship实际身份、原生变量与选定世界原始观察引用，供之后独立时序/war/army/有效前提报告使用。原 settlement 不证明实际发射，原 no-settlement 不证明负例前提。接收器不会宣称它已经补齐这些语义检查。

工具生成模板时静态读取 `publish_1019.py` 的 `CASE_CHECKS/COMPONENT_CHECKS`，不导入或执行发布模块；18组及其 checks 全为 null/PENDING。每个组列明证据来源链和欠缺项。输出只新建，不覆盖旧 intake、缓存、FAIL、report 或 final-result。最少验收覆盖精确 receipt 角色、相同SHA不同名称、SHA变更、错误tree/run/version/语言、autosave时序、缓存损坏、任务缺role与字段、不接受未来占位、18组未晋升，外加原生固定样本只读 smoke。

## 已有 CLI 如何接实际 RC7 prefix

主线程只需给出实际 prefix 和阶段到 receipt 的映射；离线线程填模板的固定路径/SHA，不让主线程手写已有游戏数据。例如：

```powershell
python -B eat_everything_origin/tools/receive_functional_1019.py template --output '<new-intake.json>'
python -B eat_everything_origin/tools/receive_functional_1019.py receive --intake '<actual-bound-intake.json>' --cache-dir '<exclusive-analysis-cache>' --output '<new-receive-report.json>'
```

模板不是执行计划，不能直接用于接收。原 CLI 也可直接使用，`--output` 必须放子命令之前：

```powershell
python -B eat_everything_origin/tools/check_1019.py --output '<new-observation.json>' observe '<actual.sav>' --world <physical-source> --world <physical-core>
python -B eat_everything_origin/tools/check_1019.py --output '<new-negative.json>' no-settlement '<actual-case.json>'
python -B eat_everything_origin/tools/check_1019.py --output '<new-settlement.json>' settlement '<actual-case.json>'
```

直接逐条 CLI 会重复完整解析相同 SAV；新接收器仅消除此串行消耗，不更改判据。真实发射、normal decision、restore、guard等原生输入由主线程继续独占；本工具不发送命令。

## 最短必要的原生顺序与并行分析

| 主线程串行链 | 最少保留的实际阶段；可复用同一保存承担角色 | SAV固定后可并行的只读分析 |
| --- | --- | --- |
| RC7 干净功能锚点 | 实际 load 干净 Machine C0 档后另存本run锚点；manifest/tree/PID/语言明确，不能以旧RC6同日期代替 | 母舰装备/唯一身份、账本/tiers0、各物理target、已完成经济的源适用性清单；不重做经济 |
| 敌星准备和校准 | 实际目标alive/战争/core/Mother就位且无入侵；base；worlds/empires各原生complete一次的calafter；实际load base弃校准收益 | 基线q、native owned colonies、war/army、两objective独立delta；随后排队分析无需等待报告写完 |
| 取消与实际重排 | queued；实际充能counter；同日Stop后的cancel；真实reload cancel；重排queued | 同日queue/cancel/reload零收益、完整订单清空、源仍活、C/L/R无增；正确回调 key 和输入链 |
| 完整敌星 PK | 以真实首次counter定起点；windup89/90、fire0/30、fire29/30、自然完成即时、下一日稳定；跨月auto按实际需要留下，不额外菜单保存每一日 | 每个固定阶段立刻抽取raw order；90/30日历分段、零提前worlds/empires收益；prefire人口与q；即时FAIL独立保留，稳定结算另报 |
| 已毁回调/重载与进程重启 | 稳定完成后正确DEVOURER双回调同日保存；实际reload后再回调保存；其中一个稳定档可合并一次真实stop/新PID/load/保存 | 原5账本、容量、pop、objective去重；重启必须另绑定进程记录，不能只凭save日期 |
| Machine normal q2/50 | ready50；真实decision后同日start100/核心−50；真实月度Situation进度直到T5；precomplete；自然完成、稳定、重复入口/reload | seed_existing100/need0/总人口守恒；冻结q2与T5；预先R/自然人口独立归因；正常结算公式、去重和保持正常时长 |
| 9持久guard + colonizing/ground | 按执行图ready→idle次日；真实load ready→正确FROM派发→同日fired。9目标可共享三SAV，colonizing/ground两目标可共享另一三SAV；前提必须到idle/fired仍真 | 各source/core独立no-settlement+完整strict，native状态、双军队、无结算不能替代缺对象/失败setup |
| core变更、owner-loss | 正常core decision前后；新core拒绝；真转手后仍绑定新core但owner异国，旧core有人保命；同日idle/fired对照 | 旧marker/deposit/capacity移除、新绑定和容量、全部core拒绝、completion再次检查core owner |
| 实际恢复与死亡 | 恢复另从有效功能锚点分支：受伤before与固定>=6日后的自然after，并留普通舰控制；死亡用core有效before→实际destroy/cleanup→完整3效果→真实monthly→reload | 恢复current/max、自然期间source/tiers/成长一致、每类regen独立；死亡唯一Mother/附base消失而flags保留、无再生，不把历史tiers当活组件 |
| Li自有非核心 PK | 独立Li干净首月后功能分支；size3/真实旧损耗deposit1/q2/300founder ready；本银河calafter/恢复；真实90/30→prefire→即时/稳定/去重/reload | C+2/G0/D2/made0、损耗恰扣一次；R来自prefire资格，native随机奖励图/消息独立分类，不用after人口残差反推 |

`restore` 在本接收合同中明确区分三件事：受伤后自然恢复、取消/稳定档的实际原生reload、真实退出进程后新PID重启。它们不相互替代；主线程只需按本次要认证的实际分支交付，不为一个泛称增加UI步骤。若当前任务仅指其中一种，其余仍保持缺项，不能填成通过。

最短链不沿用RC4的q19/750/600或数字ID，也不把RC6成长人工C20500分支继续当C0吞星前提。敌星一次shot兼用实际发射/敌方人口不返回/共同结算/危机/成长零提前；Li一次shot兼用自有非core/native损耗/返回。normal一次真实decision仍不能由上述共享effect替代。主线程进行下一个阶段时，离线解析、订单、危机校准、guard、结算和归档索引核对可并行；相同SAV的observe仅由一个缓存任务负责，避免重复抢CPU。

## 18组 final-result 的精确交接边界

| 组 | 本接收器的可提供材料 | 仍需独立认证 |
| --- | --- | --- |
| hive/machine/purifier startup与economy，共6组 | 只引用已完成资料的实际文件/SHA，不重跑、不改结果 | RC7源差异适用性由发布流程处理，不把RC6证据改写为RC7 |
| lithoid_hive_first_month | 引用已完成首月干净链 | 必须与后续人工Li功能分支分开 |
| mothership_configuration | mother原checker、实际design/required/slots/身份/变量观察 | 同国同日Relic、实际jump、UI供电/维护、其它主宰负对照与既有优势 |
| unlimited_growth | PK/cancel/guard无非法增长、death和恢复独立报告材料 | 成长collector/reporter、四属性每级系数、regen、报告UI、jump/shipyards |
| random_components | 实际装备/tiers与固定状态作为受控背景 | 独立成长reporter全六类正效应、每5级自然抽签、R400/P10→monthlyR410/P0、源归因与重载 |
| colossus_enemy_fire | raw订单90/30、自然完成、source/core观察 | 实际原生操作图、war、无入侵、正确受益人、Li自有非core入口 |
| colossus_guards | 同日no-settlement和完整strict、状态观察 | 每种native无效前提持续、正确THIS/FROM、completion重新检查 |
| colossus_cancel_idempotence | queue/cancel/replay/reload原checker与精确receipt | 实际Stop输入、正确生产callback、稳定清理后危机恰一次 |
| common_settlement | 原settlement全部字段及独立q/R/人口/两危机预期 | Machine enemy/normal与Li native分支材料齐全才能合并 |
| normal_dismantle_regression | 同日seed、实际Situation进度、原settlement/reload | 实际原生decision与自然T5完成，禁止写progress |
| old_save_migration | 引用已sealed v2与嵌套v1 FAIL，不执行迁移代码 | 当前发布门禁只接受指定RC6树，RC7适用性不能由接收器授权 |
| candidate_reload | 单样本账本/奖励/identity比较 | 真stop状态、新PID、实际load来源/输入，不能用layout-only或普通reload替代 |
| repeat_initialization | 引用已sealed RC6 41检查/完整ZIP相同报告 | RC7跨树适用性不能改原report或其限定范围 |

当前 `publish_1019.py::validate_runtime_index` 要求全部run、case、static source都等于最终候选tree；`validate_component_attribution` 和迁移v2还有指定源树约束。RC7只加count200同样产生新tree，故现有门禁不能直接载入RC6全部结果。此为明确发布衔接缺口，交release负责人处置；本工具不改gate、不重写manifest或旧case、不以小源差异自行授权跨树PASS。最终索引仍由发布线程创建，所有证据必须是真实项目路径/SHA、真实run_ids和明确tree，不能把接收总报告当final-result。

### 实施中确认的发布决策

发布负责人转达主线程最新明确决策：不增加 source bridge 或 gate 复杂度，保留严格 exact-tree，后续重跑 RC7 三类新开局/全年与两类迁移。旧 baseline、真实旧fixture和既定精度政策只作输入参考，不作为RC7 runtime PASS。见 [RC7 源差异与未采用桥接方案记录](rc7-zero-reward-source-equivalence-design-20261020.md) 的封口决策。本分析接收器不负责重做经济；上表“引用已完成资料”只作历史/输入索引，RC7 final 对应 checks 仍全部 PENDING，直至新的同树原生证据实际完成。当前从RC6干净C0导入的成长锚点也不能当RC7新开局/经济。

新工具和17项定向测试已实施，通过静态接口读取、拒绝未来模板、SHA变化、exact-tree/run/version/语言、未知任务、原严格比较参数、缓存损坏拒绝覆盖、真实固定原生receipt角色及autosave时序等边界。4项receipt测试只读取现成RC6原件，临时反例仅写JSON；没有创建或编辑任何SAV。后续以这两个已固定原生保存作工具 smoke，只验证接收/缓存/原checker传递，报告明确RC6 fixture，18组 final 仍 null/PENDING；不把它当RC7实机结果。

### 已执行的工具验证与封口

`python -B -m unittest discover -s eat_everything_origin/testing -p test_receive_functional_1019.py -q` 实际退出0，17 tests/0.290s 全部通过（本机4项真实receipt检查没有skip）。随后以固定RC6 `r6mcyearui/r6mcinit2` 两个原生保存执行接收 CLI；两者分别绑定精确的 native-save/audit，world_ids仅物理4。before执行一次完整observe，after复用同一cache；两role独立receipt仍分别核对，实际唯一Mother均为fleet125，日期均2201.01.01。原strict task为PASS_SCOPED/零差异，接收总报告为OBSERVATION_ONLY；18组所有checks仍null，true计数0。没有读取RC7未来样本、growth新采样或活动日志。

固定材料：

- `tools/receive_functional_1019.py` SHA256 `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`。
- `testing/test_receive_functional_1019.py` SHA256 `8f3bc54369b0be5a1b91b5847af43b0d3d58a1f3f44a5c66ee990619d5b923b9`。
- [PENDING模板](evidence/1019-analysis/rc7-functional-receiver-intake-template-v1.json) SHA256 `102b7b8e9cba2fde005d5add0e474aefddc77ee8bfffd6f792c57f51b2601fb4`。
- [RC6工具smoke输入](evidence/1019-analysis/rc7-functional-receiver-rc6-smoke-input-v1.json) SHA256 `f87ca398e89f65b9ce8abb7b9575b3c0d929704a4638e96f985774a0c44bef03`；[只读smoke报告](evidence/1019-analysis/rc7-functional-receiver-rc6-smoke-report-v1.json) SHA256 `88591b408298999707446fcd1387b170cbe191250b51e638057b92387e37ea52`。
- 单份[observation缓存](evidence/1019-analysis/rc7-functional-receiver-smoke-cache-v1/595de3efe90695fab59415ac73b1326c1b0bd25d4e8d8d4bdd8059cbd75e99af.json) SHA256 `7104573f0dd71895eefb5276e998b5baeea481386071c9cbd353e446f3dae3b9`。

以上七件（本文、工具、测试、模板、smoke输入、smoke报告、单份缓存）封口，之后只等待实际功能prefix并直接分析固定证据。若发布接口字节变化，现模板按设计拒绝旧fingerprint，届时基于当时真实接口另建实际输入，不改已封口模板。原checker/inspector仍为既定681836/1ec3ad SHA，没有新包装执行流程或额外游戏操作。
