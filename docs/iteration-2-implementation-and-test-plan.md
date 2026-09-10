# 迭代 2 实施与测试验收方案

## 1. 实施设计

### 1.1 `open_kaishek` 前置能力

在 Stellaris 4.4.6 profile 中把 `uses_district_set` 登记为 planet/ship 可用的 trigger。测试至少覆盖：

- deposit 的 `triggered_planet_modifier -> potential -> uses_district_set = habitat` 正向通过；
- profile 返回 trigger 类型和明确作用域；
- 拼错的 `uses_district_sets` 继续返回 `UNKNOWN_OPCODE`；
- 显式错误 scope 继续返回 `INVALID_SCOPE`；
- CLI 对含该形状的真实最小 deposit 文件返回 `VALIDATED`。

该能力只证明 4.4.6 静态语法形状可识别，不宣称模拟游戏运行时语义。

### 1.2 I2-001 deposit 映射

在既有五个 deposit 内增加 `triggered_planet_modifier`，所有新增区划效果都以如下 potential 为门：

```text
potential = { uses_district_set = habitat }
```

- `mod_extend_generator_workplace`：`district_hab_energy_max_add = 2`；既有无条件总区划 `+2` 保留。
- `mod_extend_mining_workplace`：`district_hab_mining_max_add = 2`；既有无条件总区划 `+2` 保留。
- `mod_extend_physics_res_workplace`、`mod_extend_society_res_workplace`、`mod_extend_engineering_res_workplace`：各增加 `planet_max_districts_add = 2` 和 `district_hab_science_max_add = 2`，且只在 habitat 条件下生效。

不把三种 habitat 容量一次性全部塞入每个生产计划，避免执行电力计划却同时解锁采矿/科研容量。

### 1.3 I2-002 计划 14

新增决议：

```text
decision_14_extend_population_development
```

它复用 `vivhite_workplace_supported_colony`、菜单展开 flag、1000 矿物、180 天和 `ai_weight = 0`，执行后添加：

```text
mod_extend_population_development
```

该 deposit 的 `planet_modifier` 固定为：

```text
planet_housing_add = 600
logistic_growth_mult = 0.1
planet_pop_assembly_mult = 0.1
```

不用政体分支：同一殖民地可能同时具有自然增长与机械组装，两个百分比各自只作用于已存在的通道。可重复性继续由多个同名 deposit 实例叠加实现。

### 1.4 本地化和版本

- 简体中文为文本真源，新增 deposit 名称/说明和计划 14 名称/说明。
- 同步补齐其余 9 种官方语言；运行时仍只允许 `l_simp_chinese`。
- 开发版本抬升为 `1.2.0-rc.1`，同步 `VERSION`、`descriptor.mod`、迭代 2 合同和 changelog。
- 不改 Workshop BBCode，因为本轮不发布 Steam；Workshop 页面仍描述已发布的 `1.1.0`。

## 2. 声明式夹具

新增 `fixtures/iteration-2`：

- `mod-contract.json`：冻结版本、公共决议合同、五个 habitat 映射和计划 14 三个 modifier。
- `scenarios.json`：列出静态场景及未来运行时场景；本轮运行时状态统一为 `deferred_no_game_launch_by_user`，不得填入伪造截图或数值。

建议场景：

| ID | 阶段 | 断言 |
| --- | --- | --- |
| I2-001-STATIC-MAPPING | 本轮 | 五个 deposit 的条件、目标 modifier 和数值精确匹配 |
| I2-001-HAB-E/M/S | 后续实机 | 三类居住站资源容量分别精确 `+2`，非目标不变 |
| I2-001-SCOPE-REGRESSION | 后续实机 | 普通行星和方舟不获得科研计划的 habitat 总槽位 |
| I2-001-REPEAT-RELOAD | 后续实机 | 重复再 `+2`，重载保持 |
| I2-002-STATIC-CONTRACT | 本轮 | 计划 14、deposit、住房和双 `+10%` 完整 |
| I2-002-ORGANIC/MACHINE/DUAL | 后续实机 | 各人口生产通道只获得设计内百分比 |
| I2-002-REPEAT-RELOAD | 后续实机 | 重复后双 `+20%`、两个 deposit、重载保持 |
| I2-LOC-STATIC | 本轮 | 10 语言 64 键精确同构，非中文仅静态通过 |

## 3. 本轮纯离线验收步骤

1. `open_kaishek`：全量 Maven package、Python schema、parser/CLI smoke、确定性 JAR 门禁、远端 `core-ci`。
2. `open_kaishek` CLI：用 `stellaris-4.4.6` profile 分别校验 Mod 的 decisions、deposits、scripted trigger。
3. 本仓库：`python -m unittest discover -s tests -v`，覆盖 15 个计划、habitat 条件、计划 14、版本和 10 语言合同。
4. 校验 `fixtures/iteration-2/*.json` 可解析、Mod 树哈希与当前生产目录一致、`git diff --check` 成功。
5. 进程守卫：执行前后确认没有由本任务启动 `stellaris.exe` 或 Paradox Launcher；不调用任何 GUI 自动化入口。

## 4. 后续简体中文实机方案（本轮不执行）

未来获得启动许可后，按“居住站区划 → 普通/方舟反向 → 人口通道矩阵 → 重复/重载”的顺序执行。每个场景保留：隔离 userdir manifest、生产 Mod 树 SHA-256、游戏版本/校验和、执行前后 UI、存档 token 计数和新鲜日志。

非中文语言永远不进入实机矩阵；只能报告“静态校验通过”或“运行时不在范围内”。

## 5. 完成口径

- 本轮可以完成：需求落地、工具支持、Mod 代码、翻译、声明式夹具和静态验收。
- 本轮不能宣称：Stellaris 实机通过、居住站 UI 数值已观察、人口增长/组装运行时已验证或可发布正式版。
- `1.2.0-rc.1` 只作为未发布候选；后续实机通过、changelog 收口并收到发布指令后，才能抬升正式版本和上传 Steam。

## 6. 实施记录（2026-09-09）

- `open_kaishek` 已加入 `uses_district_set` 的 Stellaris 4.4.6 trigger 合同；本地 Maven、schema、CLI、合成夹具及确定性构建门禁通过，远端 `core-ci` 通过。
- `open_kaishek` 远端通过记录：`https://github.com/XenoAmess/open_kaishek/actions/runs/34364148518`；随后使用同一构建产物检查本仓库生产 decisions、deposits、scripted trigger，三次均为 `VALIDATED`，语法与语义诊断均为 0。
- 本地 Stellaris 4.4.6 原版脚本确认：`common/districts/03_habitat_districts.txt` 明确列出 `district_hab_energy_max_add`、`district_hab_mining_max_add` 与 `district_hab_science_max_add`；原版 deposits/buildings 也实际使用这些 modifier。
- 本地原版脚本确认 `logistic_growth_mult` 与 `planet_pop_assembly_mult` 均为现役 modifier；本实现采用与原版一致的 `0.1` 数值形状。
- Mod 代码及 10 种官方语言已经落地，生产 Mod 目录仍为 15 个文件，冻结树哈希为 `b6c9d7c69da87c8c8377ed456c8a5b3c13ffe545af0f63771bd62cc7c0c8585a`。
- `py -m unittest discover -s tests -v` 共 33 项通过；迭代 2 三项静态场景据此标记为 `passed`，未来实机场景仍全部延期。
- 本轮没有启动 Stellaris、Paradox Launcher 或前台自动化；所有运行时场景保持 `deferred_no_game_launch_by_user`。

## 7. 实机验收与 v1.2.0 发布门禁（2026-09-10）

用户已经解除前台占用限制，并授权启动游戏完成迭代 2 验收；运行时仍严格只使用简体中文。本轮以 `1.2.0-rc.1` 的冻结 Mod 树作为候选输入，执行顺序如下：

1. 重新运行 `open_kaishek` 和仓库静态门禁，建立隔离 `userdir`，仅启用维护版物品对应的候选副本。
2. 在居住站上分别记录反应堆、采矿、研究区划容量基线；施加计划 09、10、04—06 对应 deposit 后，目标容量必须分别精确增加 `2`，非目标容量不得联动。
3. 在普通行星记录计划 04—06 的反向范围证据，确认 habitat 条件不会额外增加普通行星总区划槽位；既有岗位效果不属于该反向断言。
4. 在存在自然增长和/或机械组装通道的殖民地记录计划 14 前后来源；一次效果必须为住房 `+600`、自然增长倍率 `+10%`、机械组装倍率 `+10%`。没有基础通道时只验证不凭空创建人口。
5. 至少对一个 habitat 容量效果和计划 14 做第二次叠加，并通过简体中文保存/载入路径复核；存档中同名 deposit 应各出现两次，稳定效果应为双倍。
6. 保存运行 manifest、关键截图/OCR、存档哈希与 token 计数，检查 fresh 日志中没有本 Mod 可归因的错误；任一核心断言失败即停止发布。

只有上述运行时门禁全部通过，才把未发布候选提升为正式 `1.2.0`，同步 `VERSION`、描述符、合同和正式 changelog；Steam Change Note 必须以 `[v1.2.0]` 开头。随后更新维护版物品 `3797257579`，复核公开可见性、远端版本/文件、Change Note 和只读上游 `3710613857` 未变化，最后创建并推送 Git 标签 `v1.2.0`。

### 7.1 Stellaris 4.4 控制台输入经验（2026-09-10）

实机首次输入发现，系统仍处于中文 IME 模式：`pyautogui.write` 输入的 ASCII 字母进入了拼音组字，空格被 IME 解释为候选词上屏，使 `effect add_deposit=...` 变成含中文的非法命令并返回 `Unknown command`。这些失败命令没有修改存档。

正确夹具流程是：打开控制台后先用物理 Shift 扫描码切换到 IME 英文模式，再用 `type-text` 输入完整命令，最后发送两次物理 Enter：第一次确保结束潜在的组字状态，第二次执行命令。每次输入前用足量物理 Backspace 清空残留文本，并保留对应 action JSON。

控制台的稳定开关快捷键是物理 `Shift+Alt+C`（扫描码 `0x2a 0x38 0x2e`）。关闭控制台后，动态添加 deposit 的 `triggered_planet_modifier` 不保证在同一暂停帧内刷新到区划 UI；夹具必须至少推进到后续月度重算，再重新打开殖民地界面取值。计划 09 首次执行后即时界面仍显示反应堆 `0/3`，推进时间后才稳定显示 `0/5`，因此“控制台说明出现目标 modifier”不能替代最终 UI 断言。

### 7.2 实机执行结论（run `20260910T010503Z`）

- 隔离 userdir 只启用维护版候选，运行语言为简体中文；主菜单确认游戏版本 `Pegasus v4.4.6`、Modded 校验和 `6cd8`。
- 输入候选为 15 个文件、树哈希 `b6c9d7c69da87c8c8377ed456c8a5b3c13ffe545af0f63771bd62cc7c0c8585a`。
- 居住站基线为反应堆 `0/3`、航天采矿湾 `0/10`、研究区划 `0/4`、总区划槽 `2/9`。
- 计划 09 执行两次、计划 10 执行一次、计划 04/05/06 各执行一次并等待重算后，结果为反应堆 `0/7`、航天采矿湾 `0/12`、研究区划 `0/10`、总区划槽 `2/21`；各目标增量和重复叠加均与设计完全一致。
- 计划 14 连续执行两次；游戏效果说明每次均解析为住房 `+600`、人口增长速度 `+10%`、机械人口组装速度 `+10%`。存档中该 deposit 精确出现两次。
- 普通首都“剑栏”使用显式 `capital_scope` 施加物理研究 deposit；游戏效果说明只列住房、物理学家岗位和岗位效率，不列 habitat 总区划或研究区划容量，普通行星总区划槽保持 `2/15`。
- 最终复核存档为 `i2_runtime_final.sav`；存档能够解包 `gamestate` 与 `meta`，各目标 deposit 的 token 计数与执行次数一致。
- 重载 `i2_runtime_final.sav` 后，复核值仍为反应堆 `0/7`、航天采矿湾 `0/12`、研究区划 `0/10`、总区划槽 `2/21`。
- fresh `error.log` 中两条 `Wrong scope for effect 'add_deposit'` 由验收操作时的一次无星球 scope 探针产生；普通行星反向随后用显式 `capital_scope` 重跑成功。启动时的缺失 Workshop 文件记录来自隔离 userdir 中未启用的旧描述符；没有发现候选 Mod 脚本可归因的加载错误。
- 结论：迭代 2 的简体中文运行时门禁通过；其余 9 种语言仅能报告“静态校验通过”或“运行时不在范围内”。本节结论取代本文前面仍保留的历史延期状态。
