# 迭代 1：Stellaris 实机回归方案

## 目标与范围

以 Workshop `3710613857` 当前原始版本为不可变被测输入，在 Stellaris Pegasus 4.4.6 中验证：Mod 能否被单独加载、13 个星球决议是否可见且可执行、执行结果是否成为预期星球特征，以及存档重载后是否保持。迭代 1 不修改 Mod 行为；发现的问题先作为基线缺陷记录。

## 文档先行约束

本方案是实机自动化、夹具文件和验收工具代码的前置设计。后续实现必须可追溯到本文的步骤和断言；运行中出现的新知识实时补入基线记录，再修改工具。

## 固定输入

- 游戏：Steam App `281990`，Pegasus 4.4.6；锁定 `stellaris.exe` SHA-256。
- Mod：仓库 `vivhite_infinite_positions/mod`；锁定整树 SHA-256，只在隔离 userdir 中复制运行。
- 启用项：只启用 `mod/ugc_3710613857.mod`，不读取或改写玩家真实 Documents profile。
- 语言与界面：简体中文、2560×1440、无教程、非铁人、`-debug_mode`。
- 证据：每个关键状态保存截图、OCR JSON、动作 JSON、进程记录和本轮游戏日志。

## 快捷键与输入策略

1. Stellaris 对普通虚拟按键注入并不稳定；核心键采用 Windows 物理扫描码：控制台 `0x29`、回车 `0x1c`、空格 `0x39`、Esc `0x01`、F7 `0x41`。
2. 物理扫描码组合键已由工具支持，但 Stellaris 4.4.6 实测 `Ctrl+S` 不触发保存。当前可靠流程是物理 `Esc` 打开菜单，OCR 定位一次“保存游戏”，随后用物理 `Ctrl+A`、键盘输入和物理回车完成命名；不得把 `Ctrl+S` 写成稳定快捷键。
3. 使用 `Space` 控制暂停，F7 打开当前布局中的“殖民地和星域”。F 键对应项可能随导航栏排序变化，因此夹具必须记录当前布局，不能把 F7 当作跨 profile 常量。
4. 鼠标只用于没有稳定键盘入口的对象：选择具体星球、点击决议、拖动游戏内不响应滚轮的滚动条。
5. 每次时间推进前后都截图确认暂停状态，避免 OCR 推理期间游戏意外继续。

## 回归场景

### S01 单 Mod 加载

- 准备全新隔离 userdir，复制并比对 Mod 整树哈希。
- 直接启动固定游戏 EXE，进入主菜单和新游戏。
- 断言主菜单显示 Modded checksum；检查 `error.log`、`game.log` 和 `debug.log`。
- `LOAD-GREEN` 要求 Mod 自身没有加载错误；只要出现可归因于本 Mod 的加载错误即为 `RED`。

### S02 普通帝国决议目录

- 使用预设“地球联合国”，选择地球，打开“决议”。
- 从顶部到底部遍历并识别 `plan00` 至 `plan12` 共 13 项。
- 断言每项成本 1000 矿物、工期 180 天，效果文本与静态合同一致。
- 记录菜单长度、可滚动方式、是否存在折叠/分类入口。

### S03 普通帝国执行与持久化

- 暂停状态下记录地球的矿物余额、规模、住房和特征基线。
- 执行“计划10：深层采矿站扩增”，断言矿物扣除 1000 且出现 180 天进度。
- 以最快速度推进至完成后立即暂停。
- 断言地产/星球特征中出现“扩增的深层采矿站”，并核对：最大区划数 `+2`、矿工岗位 `+600`、矿工岗位效率 `+10%`。
- 创建测试存档，重载后再次断言特征和效果仍存在。

### S04 重复执行语义

- 在 S03 通过后，对同一星球再次执行计划10。
- 记录决议是否仍可选、同名 deposit 是否新增/覆盖、数值是否叠加。
- 当前脚本没有显式重复限制，因此该场景必须以实机结果冻结，不能从代码形态推断。

### S05 政体矩阵

- 蜂巢：行政、研究及资源岗位应切换为对应子个体岗位。
- 机械：同上，并检查已改名/移除的岗位键是否产生日志错误。
- 失控机仆：单独检查有机人口与机械岗位分流。
- 游牧/方舟：确认星球决议入口是否适用；不适用时应明确隐藏或拒绝原因。

### S06 语言与长菜单

- 简体中文：全部标题、描述和数值完整显示。
- 英文：冻结当前缺少英文 localisation 的行为，后续迭代再定义期望。
- 13 项直接铺开：冻结当前无折叠入口、滚轮不驱动列表但拖动滚动条有效的行为。

## 夹具设计

- `fixtures/iteration-1/mod-contract.json`：游戏/Mod 哈希、13 个决议与 deposit 的静态映射、成本、工期和预期效果。
- `fixtures/iteration-1/scenarios.json`：上述场景、前置条件、动作、断言和证据名。
- `_runtime/<run-id>/manifest.json`：每轮机器与输入指纹；`_runtime` 为本机证据，不入库。
- `tools/stellaris_acceptance.py`：仅实现本文需要的隔离启动、物理键输入、截图/OCR、动作记录和关闭流程。

## 工具运行方式

在仓库根目录使用项目虚拟环境；所有命令都读写 `_runtime/current-run.json` 指向的当前隔离运行，不接触真实 Documents profile：

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-acceptance.txt
.\.venv\Scripts\python.exe tools\stellaris_acceptance.py prepare
.\.venv\Scripts\python.exe tools\stellaris_acceptance.py launch
.\.venv\Scripts\python.exe tools\stellaris_acceptance.py capture frontend
```

核心输入示例：物理 Esc 为 `press-scan 0x01`，物理 `Ctrl+A` 为 `press-scan-chord 0x1d 0x1e`；优先使用 `press-scan`/`press-scan-chord` 和 `click-text`，只有没有稳定入口时才用 `click-point`/`drag`。结束时运行：

```powershell
.\.venv\Scripts\python.exe tools\stellaris_acceptance.py stop
```

`prepare` 会检查固定游戏 EXE 和 Mod 整树哈希；任一输入漂移时拒绝运行，必须先显式更新夹具合同。桌面锁定时截图和输入也会拒绝继续。

## 通过标准

- `STATIC-GREEN`：先通过 `D:\workspace\open_kaishek` 的 Stellaris 4.4.6 profile；不等于运行时通过。
- `LOAD-GREEN`：精确单 Mod 进入主菜单/实局，且没有 Mod 加载错误。
- `SCENARIO-GREEN`：指定场景的 UI、效果、日志和存档重载断言全部通过。
- 任一断言失败均记录为 `RED`，保留固定输入哈希和最小复现证据，不用“可以进入游戏”代替功能结论。

## 当前执行进度

- S01：已进入主菜单和普通帝国实局；发现 `supported_version="*"` 被 4.4.6 记录为无效，故严格 `LOAD-GREEN` 为 `RED`。
- S02：已确认 13 项全部存在，均为 1000 矿物/180 天；已确认菜单无折叠入口且需拖动滚动条。
- S03：计划10 已完成一次实机执行和存档重载。矿物扣除 1000，180 天队列完成后基础规模仍为 18，总区划上限由 18 变为 20，采矿区上限由 7 变为 9；可用住房显示为 720，不能误记为岗位数。重载后数值保持，存档 `gamestate` 中存在 `type="mod_extend_mining_workplace"`。4.4.6 的“地产”页是分公司/宗主持有界面，不能作为星球特征证据；岗位面板已显示劳工总量 2400 和扩展后的岗位行，但在当前 UI 尺寸下仍需通过专门夹具逐项断言矿工岗位。
- S04—S06：方案已冻结，待逐项执行或在本轮报告中标为未执行。
- I1-001 实现回归（`20260906T021747Z`）：普通地球和游牧 `pc_ark` 方舟均覆盖计划 00—12；方舟计划10完成后总区划上限由 9 增至 11，存档含 `mod_extend_mining_workplace`，重载后仍为 11；新日志无本 Mod 加载或脚本错误。详细证据与限制见《迭代 1 实施记录》及《Stellaris 实机自动化经验》。
