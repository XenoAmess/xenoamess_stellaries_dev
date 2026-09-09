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
