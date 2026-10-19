# RC6剩余功能：原生执行图与复用CLI

## 目标、范围与验收

只读核现有runtime/checker、39命令资产、RC4计划和publish的18组合同，为主线程整理最小完整RC6功能流程。本线程不操作桌面、Git、生产或SAV；所有未来步骤PENDING。RC4/RC5证据只用于接口/前提旁证，不晋升为RC6运行成功。最终候选树固定`cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`、59文件；当前run `20261019T150008Z`。其它同树RC6 run须保留各自manifest和PID。

计划新建`testing/colossus_1019_rc6_execution_map.json`，只存命名阶段、现有命令引用及必要新夹具片段，不自动执行。不改原39命令资产（SHA `76adabaf82dc2c10894222bdb425ee1b994307233e1bccb2c251bdf2f07325c8`）。补两个旧资产未覆盖的真实负例：未殖民自然宜居星、中立天然殖民星；保持状态直到回调和after。Li单次自有PK改物理size3+恰1真实d_lithoid_devastation=有效q2/300主体人口/pc_hive，同时覆盖旧损耗扣除。

## 18组合同合并，保持独立门槛

| 运行链 | 同一证据可挂的case | 仍必须单独观测 |
| --- | --- | --- |
| 三政体Jan1/首月/12连续月 | hive/machine/purifier startup及economy，共6组 | 严格干净经济分支；基线用已核0.3.1映射，不重跑 |
| Li新局首月 | lithoid_hive_first_month | 先封存首月经济，再进入公开夹具功能分支 |
| Machine现成新母舰/成长 | mothership_configuration、unlimited_growth、random_components | 同国同日Relic面板、实际jump、实际供电/维护、真实恢复、报告UI仍非collector自动证明 |
| 一次Machine敌星shot+取消/重放 | colossus_enemy_fire、colossus_cancel_idempotence、common_settlement | 真实90/30、无陆军、战争、正确受益者、危机分目标、真实取消及reload |
| 一次Machine q2/50普通决议 | normal_dismantle_regression、common_settlement | 真seed50迁移/守恒、真实T5、自然Situation完成/重载，不写进度 |
| 七持续状态+真实空星/中立/殖民中/地战/核心转手 | colossus_guards | 原生前提和正确FROM，idle/fired同日严格对照；无效事件不能替代正例发射 |
| Li自有有效q2 shot | colossus_enemy_fire的owned分支、common_settlement的native/损耗/返回 | size3−原生deposit1；真实自有星UI90/30；native随机奖励、现有主体返回、G制造分账 |
| 已有RC6两旧档迁移链 | old_save_migration | 公共0.3.1与付费队列来源分开，原严格报告/缓存限制不删 |
| 一次RC6已测档跨进程重启；一次重复生产初始化 | candidate_reload、repeat_initialization | 真退出/新PID/Load；完整initialize/startup/sync实际输入，不把仅layout helper当三者 |

publish基础CASE_CHECKS为17组，启用六真实组件后加random_components成18组。分组证据共用不自动填true或省略检查。

## 推荐串行图

1. **经济先封存**：主线程已明确顺序Purifier→Hive→Machine LAST；最后Machine年末仍C0/L0/R0/six-tier0，在同一已核UI分支直接接entry/collector，无需多load一次。保存年末UI-native receipt作为功能入口，同时保留Jan1/首月。若因异常离开后回来，必须真实Load具体Machine源并核政府/IDs/目录，必要时另存loaded锚点；collector不自动Load，只有日期相同不足以区分三局。经济用当前`runtime_economy_1019.py`，显式RC6 tree/version；之后所有夹具与变量探针都另分支。
2. **成长与母舰**：用现成`check_growth_1019.py entry`从年末receipt自动读本次fleet/ship和活动autosave路径，取其生成的dry-run/execute命令。九节点collector是18个真实月初SAV；接同日repeat/reload、C20500补差、报告UI/真实恢复等既有要求。C10000/R200后改C20500，首次预算200发到R400/P10，第二次仅用真实FF30触发原生monthly补差，剩余10到R410/P0，不是两次各200。不从已人工C10000/20500分支继续作C0吞星正例：实际load干净Machine年末锚点。
3. **准备敌星base与单次奖励校准**：新片段随机绑定一个真实非EEP默认国的自然首都，保存实际国家/物理星ID。显式actor→declare_war，先战争后Mother定位；若用受控set_location，不能充当actual_jump。固定敌基地清场只在确实困战时用既有精确范围命令，清完再保存r6pkbase：目标仍殖民、原主仍活、实际war、无陆军/运输参与、EEP账本未增、Mother不在combat。单独native complete_crisis_objective校准worlds/empires（before复用base、另存calafter），随后真实load base丢弃探针奖励。
4. **取消然后完整敌星shot**：真实右键专属命令→保存queue/windup0或1/90→同日点原生Stop并保存空订单，收益0；实际load取消档后保存/核源仍活、账本不变。重新真实下令；沿真实order字段采windup89/90、首次fire0或1/30、fire29/30、自然完成和次日稳定状态。30日快进只作推进工具，每一步读实际计数，不能从点菜单日期直接推算charge起点。完整之后先等原生国家/人口缓存清理，再对已毁物理星两次回调，同日保存/真实load/再回调；危机empires不得把延后原始灭国奖励误算成重放奖励。
5. **Machine普通q2/50**：从稳定敌星完成账本建旧资产owned_q2_setup/inspect，先SAV证明source50再点真实decision。保存owned-ready与同暂停日normal-start：source+50/core−50、总量不变、seed_existing100/need0、q2/T5/progress0。每次真实FF30、核Situation实际progress；门槛前一日保存，完成后留稳定档、重复已毁入口和同日reload。绝对C/G/D取本次实际敌星q；只有敌星q19时才是19→21，不将RC4的19直接写进RC6。普通入口after made=floor((实际G_before+2)/6)*100，last_manufactured=该值−实际made_before；只有对应G区间不跨制造门槛时才“made保持300”，不能在新银河硬套此旧绝对数。
6. **母舰损毁与核心迁移**：在normal-done且core可用时按[既有损毁片段](colossus-rc4-final-execution-order-1019.md)保存actor再destroy_fleet，完整initialize/startup/sync、真实monthly、已毁档reload后零新Mother，历史tier镜像不当活装备。随后实际load本来就需要的owned-ready做UI核心迁移、newcore负例、真owner-loss负例；旧物理core仍有人作为保命备份。勿用core已失状态证明startup不重生，以免核心guard混淆。
7. **护栏合并**：实际load r6pkbase（敌国仍活、home未因q2reserved）。未殖民负例选home外真实空宜居星，中立负例选真实非交战天然殖民星，避免占用七批home候选。绑定actor/species后造七目标，检查候选至少7且目标实际各自无效；可用state_guard_bind替代硬要求正好7的旧batch_split_bind，七setup原文不动。保存guard-ready，空等1日保存idle，真load ready后派发9目标回调并等同一日保存fired；每源以idle→fired同日比较。再同支转手外国secondary core，实际core仍可用。若新home不足7，不盲打部分构造：先只读确认另一真实系统可供7目标，文档后适配selector，不能把少目标算7个通过。
8. **殖民中+地战**：再load r6pkbase，用旧短片段state_guard_bind、colonizing_reserve_split/start_split、ground_bind_split/armies_split；两独立目标可共用ready/idle/fired三档。idle次日两状态必须都仍真，实际双方/进度有效后才reload ready派发。若地战提前结束，构造不成立，不以未派发/零收益过关。
9. **Li自有PK**：独立Li首月后，实际绑定本run Mother/core，不带Machine数字ID。新variant建pc_hive/300、physical size3、清原deposits后加1个真实d_lithoid_devastation；新inspect要求原生count_deposits恰1、非核心、源本国。保存lith-owned-ready并做本银河单位奖励校准/恢复，然后实际自有星UI90/30。before C0/G0/D2/made0→after C2/G0/D2/made0/L0、capacity差0、G造人0，返还R取实际precomplete founder，不硬填300。native矿/合金/pop随机分列，不假定抽中类别或把native pop计入G制造。

## 实际CLI与可复用入口

以下均供**主线程**执行；本页作者不运行。先在仓库根设置本次真实receipt路径，不能把例中的RC4/RC6旧档当新锚点：

```powershell
$R6Tree = 'cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a'
$R6Receipt = '<actual Machine yearui.native-save.json>'
python eat_everything_origin/tools/check_growth_1019.py entry --anchor-receipt $R6Receipt --prefix r6g
```

entry仅离线PLAN_ONLY、自动读实际fleet/ship/tree/autosave目录。使用其输出的dry_run_command，再由主线程使用execute_command_for_root_only；直接调用runtime_growth时必须显式`--fleet/--ship/--expected-tree`，旧默认159/997和178d树不得沿用。18个SAV收完后：

```powershell
python eat_everything_origin/tools/check_growth_1019.py report --receipt '<r6g-growth-receipt.json>' --repeat-receipt '<actual repeat.native-save.json>' --reload-receipt '<actual reload.native-save.json>' --budget-first-receipt '<actual20500-first.native-save.json>' --budget-second-receipt '<actual20500-second.native-save.json>' --budget-second-mode monthly --startup-receipt '<actual Machine m00.native-save.json>' --output '<new growth report.json>'
python eat_everything_origin/tools/runtime_1019.py console-open '<one ASCII effect from bound plan>' r6-unique-stage
python eat_everything_origin/tools/runtime_1019.py console 'help' r6-console-close
python eat_everything_origin/tools/runtime_1019.py native-save r6pkbase '<actual YYYY.MM.DD>'
python eat_everything_origin/tools/runtime_1019.py native-load r6pkbase r6pkbase-reload
python eat_everything_origin/tools/runtime_1019.py console 'fast_forward 30' r6-phase-unique
python eat_everything_origin/tools/runtime_1019.py frame r6-hud-unique
```

这些是命令模板，尖括号必须取真实receipt/HUD/输出新名，不原样输入。console-open适合连续短片段，`console help`作有记录的原生只读命令并关闭console后才Save/Load。避免旧`monthly-autosaves`用于2201+功能时序：该旧helper日期表固定2200.01～2201.01；普通Situation从任意实际日期开始，使用原生FF30与native-save/真实HUD日期，不能强填旧日历。所有prefix/output拒绝覆盖，当前指针必须仍指同一实际PID/run/tree。

为直接取命名片段，主线程可在自身PowerShell会话定义以下薄调用；它不使用eval、不写脚本文件，不把JSON字符串拼入shell代码。调用前仍核当前run/PID/树与前置SAV：

```powershell
$R6Old = Get-Content -LiteralPath 'eat_everything_origin/testing/colossus_1019_postfire_plan.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$R6Map = Get-Content -LiteralPath 'eat_everything_origin/testing/colossus_1019_rc6_execution_map.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$R6CommandRows = @($R6Old.commands) + @($R6Map.commands)
function Send-R6Effect([string]$R6CommandId, [string]$R6Stage) {
    $R6Found = @($R6CommandRows | Where-Object { $_.id -ceq $R6CommandId })
    if ($R6Found.Count -ne 1) { throw 'Missing or duplicate command id' }
    $R6NativeLine = [string]($R6Found[0].command)
    & python eat_everything_origin/tools/runtime_1019.py console-open $R6NativeLine $R6Stage
    if ($LASTEXITCODE -ne 0) { throw 'Physical console input failed' }
}
```

按上文实测检查点逐段调用，例如敌星绑定`Send-R6Effect r6_enemy_bind r6pk-bind`；真实war后用`r6_enemy_place`，困战才用`r6_enemy_fixed_starbase_clear`；校准用`r6_crisis_calibrate`且之后必load base。旧资产名字直接调用如`owned_q2_setup`、`duplicate_destroyed_enemy_twice`，新Li必须调用`r6_lithoid_loss_setup/inspect`，不误调用旧size2检查。

九目标setup在一次干净r6pkbase加载后，可输入`state_guard_bind`、`r6_uncolonized_bind`、`r6_neutral_bind`，再按active/devouring/credit/destroy/secondary_core/artificial/qzero顺序调用七个`batch_setup_<name>`。实际SAV确认9个不同物理目标、正确actor/core、持续状态，保存ready/idle后真正reload ready，再调用`batch_dispatch`、`r6_uncolonized_dispatch`、`r6_neutral_dispatch`；这些输入不清任何护栏状态。不要因DISPATCH日志存在就当事件trigger已执行成功，独立after与同日idle仍必须检查。

跨进程重启只需与敌星稳定dupereLoad或最后成长档合并一次。由主线程先原生保存并正常退出，再按现有RC6 gate做`prepare-single candidate <该RC6原生SAV绝对路径>`、`launch`，核新manifest/tree与新PID后真实Load导入件并保存。此处不沿用RC4 seeded save；`runtime_1019.py stop`的底层有超时terminate兜底，不能未经观测就把它写成“正常退出”，保留真实stop记录及forced值。

离线checker复用：

```powershell
python eat_everything_origin/tools/check_1019.py --output '<new-mother.json>' mother '<actual native.sav>'
python eat_everything_origin/tools/check_1019.py --output '<new-observe.json>' observe '<actual native.sav>' --world <actual_source_physical_ID> --world <actual_core_physical_ID>
python eat_everything_origin/tools/check_1019.py --output '<new-settlement.json>' settlement '<actual settlement-case.json>'
python eat_everything_origin/tools/check_1019.py --output '<new-negative.json>' no-settlement '<actual negative-case.json>'
```

settlement-case要求schema=eep.1019.settlement-case.v1，path=normal/colossus、before/after/reload、source_world/core_world、expected_q、native、expected_return、expected_other_core_pop_delta、独立worlds单位奖励及校准文件SHA、独立empires预期和正奖励校准。expected_return必须取prefire/precomplete实际合格founder groups，不抄after.eep_last_return。other_core_pop_delta在非月初最后一天可用事前确定的自然0变化；跨月必须有独立idle/原生来源，不拿after残差拟合。Li若抽中native-pop，保留本source/date新MESSAGE_TERRAVORE_CONSUME_WORLD_POP_TEXT对应的原生奖励通知图/OCR，再认定每次100；矿/合金分支则native-pop为0。不能由核心总差反推抽签或把随机人口算作返回。原生startup虽在Nemesis可用时grant perk，仍从Li真实before确认path/AP，不能为适配checker另加perk。

no-settlement严格要求同日，所以guard用idle-day1对fired-day1，不拿ready对次日fired导致日期/自然增长混淆。checker只认原始source/core字段，不证明UI真实发射；原生orders/动作/截图另附。临死缓存FAIL保留，后续稳定报告另建。

`runtime_index_1019.py --index <PENDING-index> missing`可只读看缺项；baseline引用用已核[36月映射](baseline-031-economy-reference-map-1019.md)。不循环observe-check填true，不把progress当final-result，不在本计划创建候选PASS。

## 新variant源依据与供电接口边界

生产`eep_planet_killer_effects.txt:8–20`先取真实planet_size，再export count_deposits(type=d_lithoid_devastation)并相减。原版`common/scripted_effects/00_scripted_effects.txt:8545–8546`真实consume原生咬噬正添加同键；`common/deposits/01_blocker_deposits.txt:1538`定义它为max districts−1的实体阻挡物；generated triggers1712支持`count_deposits={type=<key> count=1}`。变体不写eep_q，以source前/后实体deposits和持久q=2验证。native后续咬噬还会加同类损耗，不能从after损耗再扣第二遍。

本机generated effects/triggers未暴露舰船excess power或单舰get_upkeep getter。`fleet_power`是军力；`used_stockpile_capacity_percentage`是本地库存比例；`planet_resource_compare{type=upkeep}`虽支持ship，但描述明确为scoped colony，用于舰载殖民地账，不可拿非殖民Mother上的0冒充实付。interface/ship*.gui未发现可转用的GetPower/GetUpkeep函数，现有统计/hover由引擎填充。供电/维护仍按[实际UI入口](mothership-power-upkeep-rc4-1019.md)尝试本次Mother hover/open_designer；未显示则保留缺项，不猜造export、不给设计预估冒充实际舰费，也不扩新矩阵。

## 实施后静态核查

新JSON已完成16个ASCII单行片段，43～855字符，全数小于1000；包括受控绑定/战争/放舰/可选精确基地清场、独立危机奖励校准、两类真实负例、Li损耗变体、重复初始化/成长补差/母舰损毁。原39资产字节SHA不变；新旧ID无重复，阶段引用及原生来源都已核对。既有open_kaishek lossless parser解析16/16、退出0、无诊断、roundTrip=true；没有调用UI或执行这些effect。

新计划SHA256 `29b07e97c2503b809957195eb8a137b425ab879c5b945bf32172687000d2ee91`，所有阶段PENDING/runtime_result=null。文档中的PowerShell调用函数只是给root的手工分段入口，没有作为新工具安装或运行。静态结果与CLI源审均不证明RC6引擎行为，最终case由真实SAV/动作/截图/完整日志与独立checker填写。

主线程最新r6pu后置UI范围单列：12/12经济及auto/UI字节相同由其真实报告绑定；之后Queen/contact/crisis/tutorial遮挡和advice-only选择不算配置数值。首次open_designer未真正输入、第二次被初始化弹窗遮住，都不是按钮灰或设计器功能失败；本计划不提前下结论，等待实际打开/hover结果，不增加新UI矩阵。
