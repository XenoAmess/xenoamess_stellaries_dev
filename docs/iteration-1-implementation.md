# 迭代 1 实施记录

## 实施顺序

迭代 1 按需求编号逐项交付：`I1-001` → `I1-002` → `I1-003` → `I1-004`，最后执行 `I1-R01`、`I1-R02` 和完整验收矩阵。`I1-005` 与 `I1-006` 已由用户明确决定不做。每一项独立完成设计、实现、静态验收、实机回归、文档更新和 Git 提交/推送；后续需求不得借用“计划实现”冒充当前需求已通过。

## I1-001 方舟舰与游牧帝国殖民地支持

### 状态

- 当前阶段：已完成并通过静态验收、普通殖民地回归和方舟实机回归。
- 目标游戏：Stellaris Pegasus 4.4.6。
- 验收运行：`20260906T021747Z`；Mod 树 SHA-256 `d035b50d2e78523d49f34cbf6d8a258834c69979a8ac25ec622ac06b16e357c6`；实机校验和 `89a6`。

### 4.4.6 数据模型调查

以本机 4.4.6 游戏数据为准：

- 方舟舰承载的殖民地使用 `pc_ark`、`district_set = nomad`，且岗位/区划界面链接到实际方舟舰船。I1-002 实机日志进一步确认：从该界面执行决议时 root scope 是 `ship`，不能把它等同于普通 `planet` scope；`is_planet_class = pc_ark`、`add_deposit` 等已实测能在这条方舟决议路径工作，但任何新增 opcode 都必须按 `ship` scope 重新验收。
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

- 新增一个 Mod 命名空间内的载体 scripted trigger，集中表达“非游牧帝国普通殖民地，或 `pc_ark` 方舟殖民地”。该 trigger 会从普通殖民地的 `planet` scope 和方舟界面的 `ship` scope 调用。
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

## I1-002 可折叠的决议菜单

### 状态

- 当前阶段：已通过静态验收与 Stellaris 4.4.6 普通殖民地/方舟实机回归。
- 前置需求：`I1-001` 已通过；折叠入口必须沿用同一个载体兼容 trigger。

### 4.4.6 原版依据

- 原版 `common/decisions/13_cosmic_storms_decisions.txt` 使用一对 `enactment_time = 0` 决议，以互斥 `potential` 分别显示启用和停用入口，证明“两个即时决议切换同一状态”是 4.4.6 支持的模式。
- 4.4.6 脚本提供 `has_carrier_flag`、`set_carrier_flag` 与 `remove_carrier_flag`，原版决议大量用它们保存殖民载体状态；它们是普通行星和方舟舰共同可用的状态原语。
- 当前简体中文本地化已经预留 `decision_extend_workplace_expand` 与 `decision_extend_workplace_collapse` 两组键，但原脚本没有定义对应决议，描述文本也只是临时占位。

### 设计

1. 默认收起：没有 `vivhite_workplace_menu_expanded` carrier flag 时，只显示“展开岗位扩展计划”入口，13 项功能决议全部隐藏。
2. 展开：执行零成本、零工期的 `decision_extend_workplace_expand`，设置上述 carrier flag；随后隐藏展开入口，显示收起入口与 13 项功能决议。
3. 收起：执行零成本、零工期的 `decision_extend_workplace_collapse`，移除 carrier flag；随后恢复默认单入口状态。
4. 13 项功能决议在原 `vivhite_workplace_supported_colony` 条件外增加 `has_carrier_flag` 条件，不改成本、工期或效果。
5. 展开状态按殖民地保存，避免在一个殖民地操作却让所有行星菜单同时展开；普通殖民地和 `pc_ark` 使用相同实现。
6. 两个入口均保持 `owned_planets_only = yes`、`ai_weight = { weight = 0 }`，AI 不主动操作纯 UI 状态。

### 验收标准与夹具

- `I1-002-DEFAULT-COLLAPSED`：新游戏普通地球和方舟各只显示一个 Mod 展开入口，不显示计划 00—12。
- `I1-002-EXPAND`：点击展开后，展开入口消失，收起入口和计划 00—12 全部可访问。
- `I1-002-COLLAPSE`：点击收起后，13 项功能入口立即隐藏，且只恢复一个展开入口；连续展开/收起不产生重复入口。
- `I1-002-PERSISTENCE`：展开状态存档重载后保持；收起后再次存档重载也不会永久丢失展开入口。
- 静态门禁：`open_kaishek` 识别 decisions 中的 `NOT`、`has_carrier_flag`、`set_carrier_flag` 和 `remove_carrier_flag`，并对旧的 planet-only flag 方案、拼错的 flag 操作/错误值形状保持 fail-closed。
- 回归门禁：I1-001 的普通殖民地/方舟载体条件和 13 项决议功能合同不变，新日志无本功能脚本错误。

### 首轮实机失败与设计修订

- 验收运行 `20260906T041510Z` 的普通地球场景通过：新游戏默认只显示展开入口；展开后目录 00—12 全部可访问；收起后只剩展开入口；`i002-expanded.sav` 与 `i002-collapsed.sav` 分别证明两种状态均跨重载保持。
- 同一运行进入原版预设“刚德森研究船团”的“首都方舟”后，默认收起入口可见，但点击展开无效。`error.log` 明确报告 `has_planet_flag` 和 `set_planet_flag` 的当前 scope 为 `ship`、支持 scope 仅为 `planet`；这不是 UI 自动化误判。
- 首轮方案因此判定失败，不能交付。修订方案统一改用 carrier flag；它保持每个殖民载体独立，不退化为帝国级状态，同时覆盖普通 `planet` 与方舟 `ship` 两种决议 root scope。
- `open_kaishek` 首轮只验证了 opcode 名称与声明 scope，没有把“该 Mod 的方舟可达决议”纳入 fail-closed 合同，因而产生静态假绿。按仓库规则，先在工具仓库撤销这组三个 planet-only flag 的放行、登记 carrier flag 形状和负例，再继续 Mod 修订。

### 最终实机结果

- 修订后验收运行：`20260906T053229Z`；游戏版本 `Pegasus 4.4.6`，Mod 校验和 `48c5`，Mod 树 SHA-256 为 `a57b0feb7082199eec88ca470e4d268134f1af0eb26928a961a11ae745a5a18b`。
- 普通地球：默认态恰好一个展开入口；展开后恰好一个收起入口且计划 00—12 可访问；再次收起后计划全部隐藏。`i002-carrier-earth-expanded.sav`（1,014,854 字节，SHA-256 `4C8F88EE568151764F33B11664D1FC9334DDD024D67E1AB9B157928CC197FF29`）重载后仍保持展开。
- 刚德森研究船团“首都方舟”：默认态、展开态和再次收起态均通过；展开目录从计划 00 遍历至计划 12。`i002-carrier-ark-collapsed.sav`（1,054,651 字节，SHA-256 `C269BD1F3A90D09FEE7DE8FBE8458AA165C40755E8D780AE5110A907E3B29F17`）重载后仍恰好显示一个展开入口，计划 00 与收起入口均不可见。
- 两种载体各完成一次完整展开/收起循环，OCR 计数没有出现重复入口。运行日志没有 `carrier_flag`、`planet_flag`、scope、未知 trigger/effect 或 `vivhite_workplace` 相关错误；仅有与本 Mod 无关的已卸载 Workshop 项路径提示。
- 关键截图与动作记录保存在本地 `_runtime/20260906T053229Z`；机器可读结论冻结到 `fixtures/iteration-1/scenarios.json`。

### 结论

`I1-002` 已交付。下一项是 `I1-003`，本次提交没有提前实现后续需求。

## I1-003 机仆活体陈设岗位决议

### 状态

- 当前阶段：设计冻结，待实现、静态验收与实机回归。
- 前置需求：沿用 `I1-001` 的载体兼容入口和 `I1-002` 的折叠菜单；不在本项提前完成全量英文本地化 `I1-004`。

### 4.4.6 原版依据

- 原版 `common/pop_jobs/00_other_jobs.txt` 定义的岗位键是 `bio_trophy`，对应岗位槽位 modifier 为 `job_bio_trophy_add`。岗位只允许非机器人、具有 `citizenship_organic_trophy`，且处于 `bio_trophy` 或 `bio_trophy_unemployment` 类别的人口填充。
- 原版 `common/buildings/08_unity_buildings.txt` 的有机庇护所直接使用 `job_bio_trophy_add`；原版殖民地类型还使用 `pop_bio_trophy_bonus_workforce_mult` 调整该岗位效率，因此两项 modifier 均有 4.4.6 实例。
- 失控机仆的 civic 键为 `civic_machine_servitor`。原版当前内容在需考虑 civic 有效性的入口使用 country-scope `has_valid_civic = civic_machine_servitor`；本决议从殖民载体通过 `owner` 链接进入 country scope。
- 原版预设 `custodianship_machine_age`（界面名“地球监护者”）同时具有失控机仆 civic 和有机次要物种，适合作为执行及就业实机夹具；普通地球联合国和非机仆机械帝国用于反向可见性检查。

### 参数决策

需求中的数量、成本、工期和效率为待确认项。为保持本 Mod 当前 13 项岗位扩展的统一合同，本项采用：

- 决议成本：1000 矿物。
- 执行时间：180 天。
- 活体陈设岗位：`+600`。
- 活体陈设岗位效率：`+10%`。
- 住房：`+600`，与其余单类岗位扩展 deposit 一致，避免新增岗位与现有扩展的住房口径分叉。
- 重复执行：继续使用“决议执行 `add_deposit` 添加一个同名永久 deposit”的现有结构，不另加一次性 flag 或独立叠层机制；实机同时记录首次与重复执行行为，并与现有计划10的同名 deposit 规则对照。

### 设计

1. 新增 `decision_13_extend_bio_trophy_workplace` 和 `mod_extend_bio_trophy_workplace`，编号承接计划 00—12。
2. 决议除公共载体 trigger 和菜单展开 flag 外，在 `potential` 中要求 `owner = { has_valid_civic = civic_machine_servitor }`；非失控机仆连入口都不显示。
3. deposit 的岗位 modifier 再重复检查 owner 的有效 civic。即使通过控制台或其他 Mod 非正常添加 deposit，非机仆政体也不会获得无效活体陈设岗位。
4. AI 权重、成本、工期、图标和 `add_deposit` 方式与现有功能决议一致。
5. 简体中文为新增决议/deposit 提供完整文本。英文仅补齐访问本功能必需的展开/收起入口及本功能四个键；现有计划 00—12 的全量英文仍属于 `I1-004`。
6. 描述符版本推进至 `4.4.6-i1.3`，并更新 Mod 树哈希、机器可读合同和场景夹具。

### 验收标准与夹具

- `I1-003-VISIBILITY`：地球监护者展开菜单后能看到计划13；普通帝国与非机仆机械帝国展开后看不到计划13。
- `I1-003-EXECUTE`：地球监护者执行计划13，立即扣除 1000 矿物，180 天后 deposit 生效；岗位界面/提示显示新增活体陈设容量，合格有机人口可进入该岗位。
- `I1-003-REPEAT`：首次完成后再次执行，记录同名 deposit 和岗位数是否叠加，并与计划10使用同一 `add_deposit` 语义；不得产生负岗位或脚本错误。
- `I1-003-PERSISTENCE`：完成后的 deposit 与岗位状态跨存档重载保持。
- `I1-003-LOCALISATION`：简体中文和英文环境均显示本功能可读的入口、决议名、决议说明、deposit 名和 deposit 说明，不显示这六个本功能/依赖键的原始 key。
- 静态门禁：`open_kaishek` 对决议、deposit、scripted trigger 全部 `VALIDATED`；对错误 civic scope、拼错的 `job_bio_trophy_add`/`has_valid_civic` 保持 fail-closed。
- 回归门禁：I1-001 方舟兼容、I1-002 折叠状态和计划 00—12 合同不退化；本轮日志无可归因于本功能的错误。
