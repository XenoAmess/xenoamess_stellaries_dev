# 异常旧计数与残留状态的隔离探针

日期：2026-10-15。对应[74项追踪](remaining-acceptance-case-ledger-2026-10-15.md)的SV-03，承接[架构实施规则](feedback-redesign-architecture-implementation-2026-10-04.md)及[成功凭证恢复规则](feedback-redesign-implementation-2026-10-04.md)。本文先记录设计，再新增测试事件；只做开发、静态检查和G1，不启动游戏或操作GUI。主任务负责后续简中原生执行、保存与独立审计。

## 目标和范围

独占新增`testing/mod/events/shishan_legacy_anomaly_probe_events.txt`，namespace为`shishan_legacy_anomaly_probe`。全部为隐藏、仅触发的country事件，没有on_action、可见选项或新本地化。现有测试文件和90个正式文件均不改。独立组合包为`_runtime/shishan_code/20261015-remaining/legacy-anomaly-fixture/mod`，先复制正式90文件，再叠加当前testing/mod的快照；报告分别记录来源与每个额外文件的哈希，不把测试包上传Workshop。

探针只设置异常前提。历史计数族清除R，表示模拟“尚无R变量”的旧输入；清除一次迁移和历史异常旗标并设置旧k，不能把此操作解释为正常玩家升级会丢层。没有任何`set_variable`直接设置R/U/T/B/M，也不设置预期国家modifier、发奖或补给资源。历史计数族不写项目成功凭证；残留凭证族仅设置下表列出的异常票据。输入档仍可能保留此前架构统计和modifier的旧缓存，必须先保存输入、再调用生产刷新，由引擎重算结果。

残留凭证族只注入既定无效状态的clean或relapse旗标，不改R、n或物种。它们与历史计数族分开，不运行项目成功奖励。所有准备入口均拒绝同一存档再次准备；下一分支必须重新载入未运行任何本探针的共同源，不通过重置探针标记连续覆盖案例。

## 既定规则和观测预期

生产`shishan_code_architecture_migrate_effect`只在本起源且没有`shishan_code_architecture_migrated`时执行。R缺失则初始化0，四个旧计数各贡献`max(k-1,0)`；缺失计数不贡献。旧计数本身和旧trait不重写；负数或非整数设置`shishan_code_architecture_legacy_invalid`，不会为了计算R把k取整。生产刷新独立按国内实际主谱系人口和全部实际trait重算U、T、B并替换单一架构modifier。

| 准备事件 | 共同源条件及输入 | 第一次生产刷新应观察的结果 |
| --- | --- | --- |
| `.10` MISSING | 有四种旧carrier的共同源；四个k全部清除，R缺失、迁移旗标清除 | R=0，四k仍缺失，无新legacy_invalid；四carrier保留，仍按正式trait计入U。 |
| `.11` ZERO_WITH_CARRIERS | 同源，四个k均置0 | R=0，k各保持0，无新legacy_invalid；不能把carrier图标自动删掉，也不能把carrier数量当额外R。 |
| `.12` NEGATIVE | 同源，四个k均置-3 | R=0，k各保持-3，legacy_invalid置位；不能静默改0或删除carrier。原负值对旧效果的引擎表现仅记录，不声称修复。 |
| `.13` FRACTION_ABOVE_ONE | 同源，四个k均置1.5 | R=2，四个原k均保留1.5且legacy_invalid置位；每项额外0.5，没有向上/下取整。 |
| `.14` POSITIVE_WITHOUT_CARRIERS | 无任何四种旧carrier的共同源，四个k均置3 | R=8，k各保持3，无新legacy_invalid；生产迁移按计数处理，不补造缺失carrier及其首层原收益。记录“计数存在、载体缺席”，不能假称原收益恢复。 |
| `.15` FRACTION_BELOW_ONE | 有四carrier共同源，四个k均置0.5 | R=0，k各保持0.5且legacy_invalid置位；小于1的正小数不会变成负R。 |
| `.16` INTEGER_WITH_CARRIERS | 有四carrier共同源，四个k均置3 | R=8，k各保持3、carrier不变、无新legacy_invalid；与`.14`仅在输入载体和其自然U上不同。 |
| `.20` STALE_CLEAN | 已真实重构、无待领奖励/在研项目的源；只设置clean_success_pending，并清旧callback_state_invalid诊断 | `.91`调用正式`.60`：记录callback_state_invalid并清clean_success_pending，R/n/CD和实体trait不变，不再次清理或生成奖励。 |
| `.21` STALE_RELAPSE | 未重构、无待领奖励/在研项目的源；只设置relapse_pending，并清旧callback_state_invalid诊断 | `.91`调用正式`.60`：记录callback_state_invalid并清relapse_pending，R/n/CD和实体trait不变，不再次复发或生成奖励。 |

历史族共同源优先选原始耗尽旧档`assets/shishan-code-origin/evidence/shishan_reward_exhausted.sav`，或最终真实legacy重载档的只读副本，先确认四carrier确实存在。`.14`可用真实`fb456_natural_claim`，先确认实际主谱系没有任何四carrier。`.20`可用真实清理后已领取的`fb456_claim4`；`.21`用未重构的`fb456_natural_claim`。同一族每项从同一源原生重载，不串联修改；源SHA、国家政体、日期、原k/R和正式生产树均先记录。

这里不设计自动补造无载体首层、删除异常图标、改写负数或合并两个状态trait的补偿策略。当前生产规则明确保留历史，只诊断负数/小数；“missing migrated flag但已有R”或“migrated flag已置位但R缺失”的任意手工破坏组合没有独立修复合同，本次不自行猜测。两个实体状态trait共存的归一化另涉及克隆/清理/复发选择；本夹具的`.20/.21`只验证文档已经明确的残留凭证规则，不能冒称覆盖该全部冲突矩阵。后续若必须覆盖未定补偿策略，单独登记该子项BLOCKED并先定合同。

原四carrier的`triggered_species_modifier.mult`直接读取`from.shishan_code_iteration_*`，没有缺失变量守卫；因此`.10`既要核迁移缺失k规则，也须保留实际出现的原生未设置变量诊断，并定位到旧carrier读取还是迁移代码。不能为消除日志把“缺失”偷换成0，更不能只因R=0正确就忽略其它原生错误。负k原有劳动力/维护/住房等效果也属于被注入的输入，跨tick后岗位或预算变化须独立说明，不误归为刷新自行增加/减少人口。

## 调用与证据

所有入口的trigger与immediate都检查本起源；准备时还要求存在主模板、国内正人口主谱系、无待领奖励/成功凭证、无在研维护/清理/优化。载体族要求四carrier各在至少一个真实主谱系人口模板上；无载体族要求所有实际主谱系都没有四carrier。非起源、无适用carrier、已有pending/项目或重复准备只能输出BLOCKED，不写输入。

以当前玩家国家为控制台上下文，暂停后：

```text
event shishan_legacy_anomaly_probe.13
```

立即原生保存`legacy13_input.sav`；日志应有`SHISHAN_LEGACY_ANOMALY_PROBE_13_INPUT_READY`，国家仅存自有`shishan_legacy_anomaly_probe_prepared`、`shishan_legacy_anomaly_probe_case=13`标记。READY不是验收PASS。继续调用：

```text
event shishan_legacy_anomaly_probe.90
```

`.90`只对历史族调用正式`shishan_code_architecture_refresh_effect`，输出`..._90_REQUESTED_REFRESH`；立即原生保存`legacy13_after.sav`，再调一次并保存`legacy13_replay.sav`，证明迁移幂等。后续完整跨月、退出游戏再用同包重启重载并另存；必须区分同日输入、首次派生、重放和重载，不能只查最后字符串。

`.20/.21`保存输入后改调`.91`，它只请求正式`country_event={id=shishan_code.60}`，输出`..._91_REQUESTED_RECEIPT_RECOVERY`。按事件实际执行时点保存，不把REQUESTED当成已经清旗标；若需要tick，记录日期和普通组装/经济变化。再次`.91`应无第二次状态转换或奖励。

独立审计读取原生Document字段，至少核对四k存在性/原精度、R、迁移/诊断标记、实际人口及全部trait、U/W/P/T/B和单一modifier、n/CD/pending/候选、领袖与外国哨兵。输入→after仅允许生产派生/诊断字段变化，不能有carrier增删、人口迁种或新增R奖励；replay→reload应不重复迁移。自然组装导致P/W变化时重新按当时实际人口算U，不把正常增长当丢人口。缺少原始字段或无法确认应标UNKNOWN，不据顶栏净收入或日志marker推定PASS。

## 原生依据和开发验收

本机Stellaris4.5.2原版`events/utopia_shroud_events.txt:158/207/454`有`remove_country_flag`实例，`common/scripted_effects/00_scripted_effects.txt:17–19`有`log`实例；既有生成`effects.log:225/528/533/3200/3878`列出国家移旗标、变量设置/删除、country_event与log，`triggers.log:442/763/1236`列出`is_researching_special_project`、`has_trait`与`is_variable_set`。这些操作的支持scope包含country；小数为原生float语法。本轮直接核对本机原版和既有生成文档，不宣称新生成4.5.2文档。人口只在已知pop_group scope使用`pop_group_size`，沿用已经在4.5.2实机验证的筛选链。

开发验收要求：事件ID唯一、全部隐藏且只触发、入口守卫与载体要求可定位；每个旧输入值符合表格，直接写入派生输出/奖项/资源/人口的操作不存在；正式生产90文件逐SHA不变；叠加清单完整，所有P文件先过open_kaishek实际4.5.2固定EXE指纹。工具规则不足或UNKNOWN时暂停交付实机，不豁免检查。G1/静态通过只说明夹具结构可以进入主任务，所有异常迁移行为仍为NOT RUN，等待真实日志、原生save与独立审计。

## 开发结果

2026-10-15开发完成：新增11个唯一事件（10–16、20/21、90/91），文件21789字节、SHA-256 `1de79ea7816009e9c7c990dd38a1ca1731c78555c2510e9a4e55350bb47ba4f3`。受限AST检查全部隐藏且只触发、trigger/immediate双重起源检查、七组旧输入准确、22个READY/REQUESTED/BLOCKED日志分支、直接写派生输出或改变资源/物种/奖励的操作不存在；UTF-8无BOM、无替换字符/行尾空白。已有production architecture与receipt受限合同同时通过，仅作开发回归，不算原生执行。

组合包冻结105文件：正式90个逐路径、字节数和SHA完全匹配已发布树`835267fa011282b26bc36b4f38202489e9a5dd137bec40de1bd46596706eae94`；叠加15个测试文件且没有生产覆盖。快照中保留原`events/shishan_feedback_probe_events.txt`，本次新事件，以及并行经济lab的13个文件（`common/static_modifiers/shishan_econ_probe_modifiers.txt`、`common/traits/shishan_econ_probe_traits.txt`、`events/shishan_econ_probe_events.txt`和十语言`localisation/<language>/shishan_econ_probe_l_<language>.yml`）。复制前后来源清单一致；各文件哈希详见`legacy-anomaly-fixture/fixture-manifest.json`。其它lab存在仅为准确保留当前testing快照，不代表本探针自动执行它们。

实际执行下列命令，退出0：

```powershell
python -B C:/workspace/open_kaishek/tools/accept_stellaris_mod.py --mod _runtime/shishan_code/20261015-remaining/legacy-anomaly-fixture/mod --version-file shishan_code_origin/VERSION --game 'C:/Program Files (x86)/Steam/steamapps/common/Stellaris' --expected-exe-sha256 400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83 --report _runtime/shishan_code/20261015-remaining/legacy-anomaly-fixture/package-open-kaishek.json
```

工具提交`2b559966c72f4e845111e3e15652ae2354aaed57`；实际EXE与固定4.5.2指纹相同。结果PASS：30/30脚本、13DDS、十语279键，有限population scope 262处/6文件、零诊断；有限script-value规则NOT_APPLICABLE/0，不扩称完整script-value认证。它仍不覆盖全部opcode、初始化展开或运行语义，所有本探针原生分支仍为**NOT RUN**。

独立开发报告在`_runtime/shishan_code/20261015-remaining/legacy-anomaly-static-check.json`，组合清单及G1在相邻`legacy-anomaly-fixture/`。没有修改原fixture、production、README、VERSION或存档，也没有启动游戏、操作GUI、提交或推送。可交主任务运行；主任务按上述每个输入→首次生产刷新→重放→重载顺序产生真实save后，再由独立raw审计给出各分支结论。
