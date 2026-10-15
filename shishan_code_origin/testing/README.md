# 反馈改版的独立实机探针

日期：2026-10-15。实施依据为[本轮实机验证记录](../docs/runtime-feedback-validation-2026-10-15.md)第 3 项。本目录仅用于开发隔离测试包，不进入正式 `mod/`、Workshop 包或玩家目录。

开发阶段历史状态：当时工具修复尚未完成，Mod 验收暂停。本次只开发探针并作程序性结构分析；完整包级 G1 和 Stellaris 执行均为 **NOT RUN**。主任务将在工具修复完成后，将 `testing/mod/` 覆盖到独立候选副本，先对实际副本执行 G1，再决定运行。不得把文件存在或语法分析当作实机通过。

## 目标与范围

新增 `mod/events/shishan_feedback_probe_events.txt`，只包含两个 `is_triggered_only`、隐藏的国家事件，不接入任何 on_action。所有受控操作只在隔离存档副本中执行；原始证据存档保持只读。

- `.1` 在起源国家建立一个外国共享旧主模板哨兵：保存本国当前主体模板，随机选择另一个 `default` 国家及其真实正人口组，用原生 `change_species` 把该外国人口组换成保存的模板。该效果不修改物种定义，也不改变本国人口。记录外国人口组原模板，便于解释夹具本身造成的变更；之后奖励、清理和复发必须保留这个外国哨兵及旧模板。
- `.2` 只在本起源且没有待选奖励时，提供一张 `shishan_code_reward_ticket_ready` 并调用正式 `shishan_code_award_reward`。它不增加维护次数，不模拟项目研究完成，不直接写 U、R、岗位收入或任何预期输出。正式奖励入口自身可能刷新统计，或在候选耗尽时合法增加 R，这属于被测生产效果。

探针不添加资源、物种特质、岗位、研究倍率、预置架构层数或必中候选。名称展示、自然项目完成和经济数值验收另行进行。

## 已核对的原生能力

本机 4.5.2 原版及现有生成文档共同提供以下构件：`random_country` 可从任意作用域调用，`is_country_type=default` 检查国家类型，`is_same_value=root` 排除事件发起国；国家作用域 `random_owned_pop_group` 选择其人口组；`pop_group_size>0` 只在人口组作用域使用；`change_species` 支持人口组。禁止把国家/星球的 `pop_amount` 别名用于人口组。

`save_global_event_target_as` 支持国家、物种和人口组，可跨隐藏事件观察；普通 `save_event_target_as` 只在未断开的事件链中有效，本夹具因此使用独立命名的全局目标。国家使用 `set_country_flag`，人口组使用合法 `set_variable`；不向人口组写国家旗标。`log` 在当前作用域输出 `game.log`。

原生依据：`effects.log` 的 `random_country`、`random_owned_pop_group`、`change_species`、`save_global_event_target_as`、`set_variable`；`triggers.log` 的 `pop_group_size`、`is_same_value`、`is_country_type`。文档文件仍为旧生成物，4.5.2 原版的 `biogenesis_effects.txt` 另有 `pop_group_size` 与其数值导出实例；本记录不冒称已重新生成 4.5.2 文档。

## 调用与可观察状态

在隔离、非铁人、单人存档中，以被测起源国家为当前玩家，暂停后由主任务调用：

```text
event shishan_feedback_probe.1
event shishan_feedback_probe.2
```

两者的 `immediate` 都再次检查起源，避免控制台强制调用绕过事件 `trigger`。`.1` 还要求有主体模板、尚未完成本夹具，并且有外国 `default` 国家拥有 `pop_group_size>0` 的人口组；没有合格对象时只记录 `BLOCKED` marker，不伪造哨兵。`.1` 完成后拒绝重放；不同分支从未执行探针的共同基线重新建立。

`.1` 的持久观察对象为：

| 对象 | 保存位置 |
| --- | --- |
| 原起源国家 | 全局目标 `shishan_feedback_probe_source_country` |
| 本国旧主体模板 | 全局目标 `shishan_feedback_probe_source_species` |
| 选中的外国国家 | 全局目标 `shishan_feedback_probe_foreign_country`；该国旗标 `shishan_feedback_probe_foreign_sentinel` |
| 选中的外国人口组 | 全局目标 `shishan_feedback_probe_foreign_group`；该组变量 `shishan_feedback_probe_sentinel=1` |
| 外国组被夹具替换前的模板 | 全局目标 `shishan_feedback_probe_foreign_original_species` |
| 起源国家已建立哨兵 | 国家旗标 `shishan_feedback_probe_sentinel_ready` |

日志使用独立 ASCII marker：`SHISHAN_FEEDBACK_PROBE_1_READY_FOREIGN_SENTINEL`、`SHISHAN_FEEDBACK_PROBE_1_BLOCKED_NO_ELIGIBLE_FOREIGN_GROUP`、`SHISHAN_FEEDBACK_PROBE_1_BLOCKED_POSTCONDITION`、`SHISHAN_FEEDBACK_PROBE_1_BLOCKED_PREREQUISITE_OR_REPLAY`；`.2` 使用 `SHISHAN_FEEDBACK_PROBE_2_REQUESTED_CONTROLLED_REWARD` 或 `SHISHAN_FEEDBACK_PROBE_2_BLOCKED_ORIGIN_OR_PENDING`。`READY` / `REQUESTED` 只表示探针条件或请求，不是 Mod 验收 PASS。

## 验收标准与边界

1. G1 对实际独立候选副本和此探针一起执行；不把正式候选的旧报告移作夹具报告。没有通过 G1，不运行对应 P 语言夹具。
2. `.1` 建立后立即暂停并原生另存。审计目标国家不同于来源国且为 `default`，标记组人口大于零、其模板恰为保存的旧主体模板；本国所有人口及所有物种定义与探针前相同。外国原组模板改变是夹具输入，须与生产奖励造成的变化分开。
3. 正常领取实体奖励、清理或复发后，审计本国真实模板的预期变化，同时确认外国标记组仍引用旧模板、该模板特质集合未被共享改写。不能只看本国新图标或字符串出现次数。
4. 原版可能合并人口组，或因外国权利在后续 tick 同化/清除哨兵。若全局组目标失效、标记变量丢失、人口归零或被原版换种，该样本为 **BLOCKED**，须从新基线重建，不能把它记为外国隔离通过。夹具对建立后的即时后置条件作检查，并以单独 marker 报告失败；跨 tick /重载稳定性必须再查原生存档。
5. `.2` 在已有待选票据时不得换组、发奖或改变冷却。成功调用只提供受控交互输入；三选一、延期、重抽和冷却实际行为仍由正式生产效果执行并审计。无论是否成功领取，它都不能充当自然维护/优化研究完成证据。
6. 负例包含非起源国家、没有合格外国人口、`.1` 已建立后的重放、`.2` 已有待选票据。只记录相应 `BLOCKED` marker，不建立额外哨兵、不增加维护次数、不直接写数学期望。

本次开发者只写本 README 与测试事件，不修改正式 Mod、生成器、运行适配器或根文档，不操作游戏、Steam 或桌面。G1、实机结果、原生存档和日志由主任务后续统一登记。

## 本次开发检查

2026-10-15：以既有受限 AST 解析器只读解析新增事件，并作结构检查，通过两个唯一 ID、隐藏且只触发、`immediate` 再次起源守卫、外国选择两处排除 root、人口组使用 `pop_group_size`、唯一 `change_species` 位于外国人口组、没有物种定义修改或直接写数学输出等检查。唯一 `set_variable` 仅写人口组的探针标记，受控奖励只写票据凭证并调用生产入口。README 链接存在；两文件 UTF-8、无 BOM/替代字符/行尾空白检查通过。

这只是开发结构分析，没有执行该解析器的模拟引擎，也没有调用包级验收、运行游戏或生成实机证据。工具修复门禁仍未解除，G1 与真实运行仍为 **NOT RUN**。

2026-10-15主任务补记：open_kaishek修复已提交推送至`2b55996`，53项相关测试通过。主任务重跑实际fixture-rc2包为PASS（26/26脚本、13DDS、268键），已启动隔离4.5.2。上文NOT RUN是开发阶段历史状态；行为结果见本轮实机验证记录，不能从门禁PASS推导实机PASS。

当前执行状态：工具修复已完成并推送，rc.6正式与实际隔离包重新通过G1（25/25及26/26脚本、13DDS、269键），简中实机本轮已执行并正常退出。生产90文件原样复制，夹具只额外加入本目录一个P文件；具体行为、存档及失败证据见[实机记录](../docs/runtime-feedback-validation-2026-10-15.md)。原开发阶段NOT RUN不表示当前整体状态，也不替代各行为结论。

## 加算经济 lab（0.2.1 正式包的独立测试叠加）

先行设计及完整取证规则见[最小受控加算经济探针](../docs/remaining-additive-economy-probe-design-2026-10-15.md)。本节为后续已授权实施；前面的两个 foreign/reward 事件保持原样。lab 仅新增 3 个 P 文件与 10 个测试本地化文件，不改 90 个正式生产文件或生产 on_action。

| 国家控制台入口 | 输入与 READY 后观察 |
| --- | --- |
| `event shishan_econ_probe.10` | 架构等效 OFF：按生产刚刷新得到的实际 T，永久添加每层 -5% 的同键 counter。记录实际输入 `shishan_econ_probe_counter_t`，不会月度追调。 |
| `event shishan_econ_probe.11` | 仅在已有 counter 时移除，使架构 ON；清理 counter 标记和记录，调用生产 refresh。 |
| `event shishan_econ_probe.20` | 添加唯一的 +40% 岗位产出加算输入；不重复叠加。 |
| `event shishan_econ_probe.21` | 仅在已有 +40% 输入时移除。 |
| `event shishan_econ_probe.30` | 添加 `trait_external_econ_probe_positive`，cost=1/positive，无自带经济效果。 |
| `event shishan_econ_probe.31` | 添加 `trait_external_econ_probe_negative`，cost=-1/negative，无自带经济效果。 |
| `event shishan_econ_probe.32` | 添加 `trait_external_econ_probe_hidden`，cost=0/hidden=yes，无自带经济效果。 |

以上都是隐藏、仅触发事件，没有 on_action；国家应为当前玩家，关闭选中的星球/领袖后调用。事件 trigger 限本起源，immediate 再查起源、主模板、正人口主谱系、无 pending/成功票据及没有在研维护/清理/优化。每个入口输出 `SHISHAN_ECON_PROBE_<ID>_READY_...` 或 `..._BLOCKED_...`；READY 仅表示受控输入成功，不是经济验收通过。

`.10` 在 counter 已存在时 BLOCKED，不能用重放静默重新校准；`.11/.21` 缺少待移除对象时 BLOCKED。三个 trait 入口要求没有 counter、没有任一 lab trait，且实际主谱系皆为 ROBOT/MACHINE；只调用既有国内 clone helper，执行前重检并在后置条件核对全部实际主谱系人口已有该键。单个分支只允许一种 lab trait；从同一 S 重载准备下一分支。它们不修改共享物种定义、不直接写 U/R/T/B/n/CD、不发成功凭证、不补资源，也不能代替自然项目或真实第三方整包兼容验收。

最小操作：从 `fb456_natural_claim` 准备并保存共同 S，先用原有 `.1` 建立外国哨兵（若需）。依次重载 S：F00 调 `.10`；F10 调 `.10`、`.20`；F01 不加输入；F11 调 `.20`；FP/FN/FH 调 `.20` 后分别 `.30/.31/.32`。各自先暖完整一月，再测完整一月并原生另存。具体正常岗位与 bonus_workforce 分母、分类 budget、误差、T 固定和样本无效判定按设计执行。

拟定组合包目录为 `_runtime/shishan_code/20261015-remaining/additive-fixture/mod`：正式 90 文件逐字节复制，再叠当前 `testing/mod`，含原 foreign_probe；生产 descriptor/version 仍为 0.2.1。测试专用额外文件、哈希、G1 报告另存运行目录；没有 G1 PASS 不进入此夹具实机。十语言测试标签提供完整键集，九种外语仅静态校验，运行时不在范围内。不得把此包上传 Workshop。

开发静态与 G1 结果实施后回填；目前本节不宣称原生 lab 已执行。

2026-10-15 开发收口：lab 新增 13 文件，连原 foreign_probe 共 14 个额外文件；实际组合包 104 文件，正式 90 文件逐一 SHA-256 与源相同并在 G1 后重查。G1 **PASS：29/29 P 脚本、13 DDS、279 键/语**；全部事件 ID 无重复；十语静态检查为 60 文件/每语 279 键，通过。三个静态负例拒绝缺失 clone 内层 guard、hidden 字段、pending/凭证 guard。详情及完整报告链接见上述设计文档；实际 lab 事件与经济原生回归仍为 NOT RUN，待主任务执行。未改生产、工具或启动游戏。
# v2：独立稳定度控制（经济实验专用）

来源与验收边界见[经济探针设计](../docs/remaining-additive-economy-probe-design-2026-10-15.md)的 v2 章节。`shishan_econ_stability_probe_events.txt`、对应 static modifier 与十语独立 yml 仅供新 `additive-stable-fixture`；原运行中的104文件包保持原样。新包从冻结104逐字节复制后叠12文件，共116，仍是测试环境，禁止用于正式Workshop上传。

原生控制台 `event shishan_econ_probe.40` 只给本国真实首都添加永久 `shishan_econ_probe_stability_control`，其唯一数学输入为 `planet_stability_add=100`。事件要求本起源/default country、主谱系实际人口、首都归本国、无在研三项目/待领/成功/复发凭证。首次 READY，已有控制时 BLOCKED；没有修改预算、U/R/T/B/J、资源或预期输出。前提不满足可能被原生 event trigger 拒发；只有进入 immediate 才保证其对应日志分支，不能伪造未执行事件的 marker。

主任务须从原生存档确认真实 capital 的 stability=100、唯一正确永久 modifier、其它条件不变后，保存七分支共用 S。静态依据 MAX_PLANET_STABILITY=100、capital_scope输出colony及修正Category Colony，不代替实际达到100；G1 与7项结构/负例测试通过时，实际clamp尚 NOT RUN。随后run113522Z的共同源`econstable_common_0302`已独立确认实际100/唯一永久正确modifier及U7/R0/J100，七支窗口仍待证。若缓存需要真实tick刷新，由主任务自然推进并另存共同源，不能直接写 stability 字段。所有分支共用同一受控环境，之后沿原10/20/30/31/32输入矩阵；原自然F01 INVALID数据保留。

2026-10-15 原生收口：首次稳定度100但自然组装仍开启的七支21档因部分civilian人数差1保持INVALID；随后使用原版正常「停止组装机器人」决议并成熟两个月，不改116文件包。新共同源`ecng_common_0502`和七支21档的实际人口P5497及全部国内就业固定，测量期已观察经济context固定，setup及同相位跨支守卫通过；共同源→input→warm的carrier_flags共同暖机变化另列原报告。冻结审计器对有限经济、setup、严格P/W均判PASS。凝聚力/社会学的同区额外40%对照及正/负/隐藏零费特质各+5%通过，被测消费品维护及country_base不变。完整原始档、早期失败、驱动源码与日志见[归档](../docs/evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/README.md)；范围仍限已测岗位/资源，不把新结果覆盖旧INVALID或推广至全部政体、经济与性能。

其它独立夹具的前提、G1和未执行原生边界分别见[月速](../docs/remaining-speed-boundary-probes-2026-10-15.md)、[旧档异常](../docs/remaining-legacy-anomaly-probes-2026-10-15.md)、[性能计算开关](../docs/remaining-performance-measurement-design-2026-10-15.md)。这些测试资产均未混入正式90文件或上传Steam。
