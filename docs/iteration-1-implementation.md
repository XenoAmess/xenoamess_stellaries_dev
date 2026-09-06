# 迭代 1 实施记录

## 实施顺序

迭代 1 按需求编号逐项交付：`I1-001` → `I1-002` → `I1-003` → `I1-004` → `I1-005` → `I1-006`，最后执行 `I1-R01`、`I1-R02` 和完整验收矩阵。每一项独立完成设计、实现、静态验收、实机回归、文档更新和 Git 提交/推送；后续需求不得借用“计划实现”冒充当前需求已通过。

## I1-001 方舟舰与游牧帝国殖民地支持

### 状态

- 当前阶段：已完成并通过静态验收、普通殖民地回归和方舟实机回归。
- 目标游戏：Stellaris Pegasus 4.4.6。
- 验收运行：`20260906T021747Z`；Mod 树 SHA-256 `d035b50d2e78523d49f34cbf6d8a258834c69979a8ac25ec622ac06b16e357c6`；实机校验和 `89a6`。

### 4.4.6 数据模型调查

以本机 4.4.6 游戏数据为准：

- 方舟舰承载的殖民地是可殖民行星类 `pc_ark`，`district_set = nomad`，且通过 `ship` 链接到实际方舟舰船；它不是普通舰船 scope 上的岗位容器。
- 游牧帝国可由 country scope 的 `is_nomadic = yes` 识别。
- 原版 `common/decisions/15_nomads_dlc_decisions.txt` 在方舟殖民地使用标准 `owned_planets_only = yes` 行星决议入口，说明 Mod 不需要另造舰船按钮。
- 方舟区划通过原版 `jobs/technicians_add`、`jobs/miners_add`、`jobs/farmers_add` 等 inline script 添加普通岗位键；科研、行政、工业和军职也沿用现有基础岗位键。因此本需求不引入未经引擎定义的“方舟专属同名岗位”。
- `pc_ark` 使用 `gridbox = district_generator` 等标准区划槽位，现有 `district_generator_max_add`、`district_mining_max_add`、`district_farming_max_add` 继续作为适用的区划容量修正；实机仍需分别验证。

以上均为 Stellaris 4.4.6 方言和数据模型结论，只记录在本项目知识库。

### 范围决策

1. 方舟殖民地开放现有全部 13 项岗位扩展决议。原因是 4.4.6 的方舟区划与岗位系统复用这些基础岗位键，没有证据支持任意删减其中一类。
2. 普通、蜂巢、机械等非游牧帝国的已有殖民地保持可用。
3. 游牧帝国仅在 `pc_ark` 方舟殖民地显示这些决议；若未来版本允许游牧帝国拥有另一类岗位殖民载体，必须先新增已验证的类型，而不是无条件放开。
4. 本需求只处理载体兼容性，不改变 1000 矿物、180 天、岗位数量、效率和重复执行语义；这些属于后续需求。
5. 同时把描述符更新为明确的 4.4 兼容范围，消除当前 `supported_version="*"` 的加载错误，作为“日志无新增脚本错误”门禁的前置修复。

### 设计

- 新增一个 Mod 命名空间内的 planet-scope scripted trigger，集中表达“非游牧帝国殖民地，或 `pc_ark` 方舟殖民地”。
- 13 项决议的 `potential` 统一调用该 trigger；不在 13 处复制方舟判定。
- 保持 `owned_planets_only = yes`，由引擎继续负责所有权入口过滤。
- 更新迭代夹具中的 Mod 哈希、描述符合同及 `I1-001` 场景。
- 若 `open_kaishek` 不能验证 `common/scripted_triggers`、决议 `potential` 或自定义 trigger 引用，先在工具仓库记录边界并补齐 profile，再继续修改 Mod。

### 验收标准

- 静态：`open_kaishek` 对 decisions、deposits、scripted trigger 全部返回 `VALIDATED`，且错误引用/未知 scope 形状有负向测试。
- 普通帝国回归：13 项决议仍可进入，至少计划10的既有合同不退化。
- 游牧实机：使用原版预设“刚德森研究船团”的 `pc_ark` 方舟殖民地，能看到适用决议并完整执行至少一项；完成后岗位或对应数值变化可见，存档重载后保持。
- 日志：不再出现本 Mod 描述符 `supported_version` 错误，也不出现本需求新增的脚本错误。
- 范围：本提交只交付 `I1-001`，不提前实现折叠菜单、机仆专属岗位、英文或动态人口机制。

### 回归夹具

- `I1-001-NOMAD-CATALOG`：游牧预设、`pc_ark`、简体中文，断言决议目录存在且非空。
- `I1-001-NOMAD-EXECUTE`：执行计划10，断言成本、工期、deposit、住房/岗位和存档持久化。
- `I1-001-NORMAL-CATALOG`：普通帝国地球，断言原有 13 项仍可访问。
- `I1-001-LOAD`：只启用本 Mod，断言 4.4.6 新日志中没有本 Mod 加载错误。

### 实现结果

- 新增 `common/scripted_triggers/vivhite_workplace_triggers.txt`。`vivhite_workplace_supported_colony` 在 planet scope 中接受非游牧帝国殖民地，或接受 `pc_ark` 方舟殖民地；未知的未来游牧载体不会被意外放开。
- 13 项决议统一增加 `potential = { vivhite_workplace_supported_colony = yes }`，保留原有 `owned_planets_only`、1000 矿物、180 天、AI 权重和 effect。
- 描述符改为版本 `4.4.6-i1.1`、兼容范围 `4.4.*`，4.4.6 不再报告原来的通配符描述符错误。
- `open_kaishek` 已补齐 Stellaris `common/scripted_triggers`、`OR`、`is_planet_class`、`is_nomadic` 和本项目自定义 trigger 的验收能力；工具提交 `840ac14` 已推送。随后本 Mod 的 decisions、deposits 与 scripted trigger 全部静态通过。

### 实机验收结果

- `I1-001-LOAD`：通过。隔离 userdir 仅启用本 Mod，Pegasus 4.4.6 能进入两种新游戏；日志没有本 Mod 的描述符、trigger、decision 或 deposit 解析错误。`error.log` 中缺失的 Workshop 项来自隔离 profile 继承的未启用订阅记录，与被测 Mod 无关。
- `I1-001-NORMAL-CATALOG`：通过。地球联合国的地球上，计划 00—12 共 13 项仍全部可见。证据为 `normal-decisions-top-final`、`normal-decisions-early`、`normal-decisions-middle`、`normal-decisions-late`、`normal-decisions-bottom`。
- `I1-001-NOMAD-CATALOG`：通过。原版预设“刚德森研究船团”的“首都方舟”是 `pc_ark`；计划 00—12 共 13 项全部可见。证据为 `ark-decisions-after-track`、`ark-decisions-early-view`、`ark-decisions-plan05-view`、`ark-decisions-middle-view`、`ark-decisions-late-view`、`ark-decisions-plan10` 和 `ark-decisions-bottom-final`。
- `I1-001-NOMAD-EXECUTE`：通过载体兼容与持久化断言。计划10进入 180 天决议队列并完成；方舟总区划上限由 9 增至 11。测试存档 `i——001——.sav`（1,361,596 字节，SHA-256 `a31941ed239ced6634957706d1a15020aa072ece32625df077806663b637fdb8`）的 `gamestate` 含一个 `type="mod_extend_mining_workplace"`，重载后上限 11 仍保持。证据为 `ark-plan10-after-click`、`ark-plan10-effect-view`、`ark-after-reload` 和 `ark-plan10-persisted`。
- 矿物库存因启用 debug view 且资源栏仅显示取整值，本轮没有把 UI 前后值作为精确扣款证据；静态合同及普通殖民地基线已证明成本仍为 1000。本需求只改变载体入口，未改变资源块。
- 重载时引擎记录一次 `Repaired savegame, cleared 1 invalid deposits!`，但本 Mod 的 deposit 在存档中仅有一个且方舟的 `+2` 效果重载后仍存在，因此该清理不是本次新增 deposit；保留此日志供后续完整矩阵追踪。

### 结论

`I1-001` 已交付。下一项是 `I1-002`，本次提交没有提前实现后续需求。
