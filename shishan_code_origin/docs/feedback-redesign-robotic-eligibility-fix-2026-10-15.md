# 机械奖励的原版互斥与资格补全

日期：2026-10-15。实施前记录。程序审查发现机械奖励 17/18/19 的互斥表为空，本机 4.5.2 原版却要求三个科研核心及 structural_awareness 互斥。已有随机权重和界面修复不能弥补资格表缺漏；本轮只补真实来源能证明的候选资格，不改数值、层数上限、冷却或奖励机制。

## 原版来源与审计方法

本机游戏为 Stellaris 4.5.2，机械定义位于 `common/traits/05_species_traits_robotic.txt`，SHA-256：`8e3c0d646dc851e2b95102dc1f21fdad1ddc834d8cb62dff876ddfb13e6f9fae`。20 个既有候选都具有 `positive` 标签，并明确允许 `ROBOT` 与 `MACHINE` archetype。

只读解析全部 44 个原版 `common/traits/*.txt` 文件，对每个候选收集所有重复出现的 `opposites` 字段并取并集，再加入其它原版 trait 对它声明的反向互斥。不能把重复字段先转换成覆盖字典；double_jointed、emotion_emulators 的多个原版字段都要保留。反向扫描另发现 suppressed 对三个候选的限制。

资格核对还覆盖 `forbidden_ethics`、`host_has_dlc`、`species_potential_add` 与已有池策略。`species_potential_add` 中的 `can_add_droid_traits`、`owner_is_machine_intelligence` 等原版 helper 使用 `FROM=country`，见 `common/scripted_triggers/05_scripted_triggers_traits.txt:311–341`；不能直接搬到普通回调并假定 FROM 正确。本 Mod 两类合法机械起源满足其中明确的机械智能或个体机械国家分支，不新增无关科技门或 trait points/picks 上限。

## 20 项审计结果

下表为必需的直接/反向互斥并集；`—` 表示没有原版声明的互斥。名称均为真实脚本键。

| ID / 候选 | 互斥并集 | 其它资格或保留策略 |
| --- | --- | --- |
| 01 `trait_robot_power_drills` | — | 机械 archetype |
| 02 `trait_robot_harvesters` | — | 保留使用食物的经济过滤 |
| 03 `trait_robot_superconductive` | — | 机械 archetype |
| 04 `trait_robot_efficient_processors` | — | 机械 archetype |
| 05 `trait_robot_logic_engines` | `trait_robot_suppressed` | 反向互斥，本轮补齐 |
| 06 `trait_robot_loyalty_circuits` | — | 原版禁止 `ethic_gestalt_consciousness`，保留个体限制 |
| 07 `trait_robot_double_jointed` | `trait_robot_bulky`、`trait_interconnected` | 原来已覆盖全部重复/反向声明 |
| 08 `trait_robot_enhanced_memory` | `trait_robot_suppressed` | 反向互斥，本轮补齐 |
| 09 `trait_robot_emotion_emulators` | `trait_robot_uncanny`、`trait_interconnected` | 补漏 interconnected |
| 10 `trait_robot_durable` | `trait_robot_high_maintenance` | 原来已覆盖 |
| 11 `trait_robot_learning_algorithms` | `trait_robot_repurposed_hardware`、`trait_robot_suppressed` | 补漏 suppressed |
| 12 `trait_robot_mass_produced` | `trait_robot_custom_made` | 原来已覆盖 |
| 13 `trait_robot_recycled` | `trait_robot_luxurious` | 原来已覆盖 |
| 14 `trait_robot_propaganda_machines` | `trait_robot_quarrelsome` | 补互斥；保留原池的个体经济过滤 |
| 15 `trait_robot_streamlined_protocols` | `trait_robot_high_bandwidth` | 原来已覆盖 |
| 16 `trait_robot_trading_algorithms` | `trait_robot_scarcity_algorithms` | 补互斥；保留原池的个体经济过滤 |
| 17 `trait_robot_artificial_engineers` | `trait_robot_artificial_physicists`、`trait_robot_artificial_sociologists`、`trait_structural_awareness` | 需要 The Machine Age |
| 18 `trait_robot_artificial_physicists` | `trait_robot_artificial_sociologists`、`trait_robot_artificial_engineers`、`trait_structural_awareness` | 需要 The Machine Age |
| 19 `trait_robot_artificial_sociologists` | `trait_robot_artificial_physicists`、`trait_robot_artificial_engineers`、`trait_structural_awareness` | 需要 The Machine Age |
| 20 `trait_robot_integrated_weaponry` | `trait_robot_delicate_frames` | 需要 The Machine Age |

14 的个体过滤比原版严格：原版潜在添加分支允许机械智能，且没有 gestalt forbidden_ethics；16 也不应被写成原版强制个体。两项均作为既有候选池的保守经济过滤保留，本轮不借互斥修复扩大候选政策。20 原版 `randomized=no`，本 Mod 使用既有显式奖励池，保留此候选，不改成原生随机特质池。

## 最小实现范围

- 保持 `ROBOTIC` 的四元素 tuple API，仅补漏互斥列表；19 个兼容映射不改。
- 新增 `ROBOTIC_REQUIRED_DLC`，四个 Machine Age 候选在国家资格中加入原版 `host_has_dlc`。
- `species_condition(..., compatible=False)` 对 20 个真实机械候选加入 `OR={is_archetype=ROBOT is_archetype=MACHINE}`。原生 `is_archetype` 只支持 species，生成器现有 eligibility、claim 模板 limit、coverage 的 species 子作用域均满足；不把它错误放到 pop_group。
- 所有新增互斥复用同一模板条件，使显示资格、实际发奖与覆盖率一致。单一模板取得一个核心后，其它互斥核心被拒绝；混合模板仅允许仍有真实合格人口的模板领取，不错误把某个模板的限制扩到整个帝国。
- 从修改后的生成器重生成 effects/triggers/events；保持先前 `NOT{AND{...}}`、`hidden_effect`、长名本地化和维护显示键修复。不调用会重写本地化的 `main()`，不修改 VERSION、CHANGELOG 或游戏加载副本。

## 验收线

静态检查须从原版重新独立提取约束，与生成器声明、生成的 eligibility、claim limit、coverage 比较；不能用生产列表生成预期。核心逐个、structural_awareness、各新增反向互斥必须有确定性拒绝检查；正例确认合法机械仍可领，缺 DLC 与非机械模板不能领，混合模板只修改合格部分。保持 234 个权重显式复合取反、槽唯一及 CD 合同。

独立审计、解释器/测试的 archetype 与 DLC 支持由程序检查任务负责，本任务不写其文件。主任务对后续冻结候选统一 G1，并在 rc.4 原生重启后选择核心、重开/下一轮确认其它互斥核心被正确过滤；当前继续运行的 rc.3 不作为修复后的资格证据。实机结果仍为 **NOT RUN**。

## 实施及本次静态检查

已修改生成器的一份候选元数据及两个资格生成入口。三类脚本均从内存重新生成；实际仅 effects 与 triggers 内容改变，events 与原内容字节一致，因此未重写。没有调用生成器 `main()`、修改本地化或写入运行中的冻结副本。

效果产物 SHA-256 为 `f48618e67636987cc6d83375a3cfce8f631a1d0ac5a9333137afb16b5e4b7fe5`；资格 triggers 为 `0a209af0200c9ad66de89c0b1eb4c3ca5e6df809899006297dac6a1e6ddc2111`；未变的事件为 `00640c1717ca3e35a763cafd310bda4e7c3998df04954cb2b1848aba3e9bab72`。

本次独立、只读的临时静态检查通过：

- 重新从 44 个原版 trait 文件建立直接与反向互斥图，20 个候选声明与必需并集完全一致；不是从生产列表生成期望。
- 四项 DLC 国家守卫与原版 `host_has_dlc` 完全一致；20 项的 archetype 条件恰为 ROBOT/MACHINE，且 eligibility、claim 模板 limit、coverage 的 species 条件一致。
- 复用程序任务已补的受限 AST 执行器、清空奖励资格 override 后，执行 68 个真实生成 guard 的正负例：合法机械正例、每个原版互斥负例、非机械 archetype 负例、四项缺 DLC 负例均通过。
- 另对三个核心分别执行一次抽象国内模板奖励，再检查另两个核心的实际生成资格，6 个拒绝检查通过。这里的模板克隆是明确的 fixture hook，不是原生克隆或实机领取证据。
- 三份生成结果与磁盘逐字节一致；234 个权重仍为显式 `NOT{AND{...}}`，没有恢复多子 NOT；生成器 Python AST 和改动脚本的受限 AST、whitespace 检查通过。

程序任务负责将独立原版审计和确定性负例固化到既有审计/测试工具，本记录不冒充其最终运行结果。G1 与 rc.4 原生选择/重开回归仍由主任务登记；没有新实机 PASS。
