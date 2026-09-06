# Stellaris 验收夹具特性调研计划

本文先定义调研边界和落地标准，再进行网络检索与夹具实现。目标不是收集攻略，而是把 Stellaris 4.4.6 中可重复、可观察、可归因的机制转化为 Mod 回归验收能力。

## 证据等级

1. 本机固定版本游戏文件、工具模板、运行日志与实机截图是最高等级证据；最终自动断言必须能回到这些材料。
2. Paradox 官方 Wiki、官方开发日志、官方论坛工作人员说明用于解释机制和发现入口；凡版本可能漂移的内容，必须再用本机 4.4.6 文件或实机复核。
3. 社区 Wiki、指南和讨论只作为检索线索，不单独决定通过/失败。
4. 每项结论记录来源、适用版本、实机复核状态和对应夹具能力；无法确认版本的内容标记“候选”，不得进入硬断言。

## 调研主题

- 启动与隔离：`-userdir`、显示设置、DLC/Mod 装载、依赖与加载顺序、校验和。
- 确定性控制：`commands_at_date.txt`、控制台命令、暂停/速度、日期触发、AI 开关与观察者模式。
- 场景构造：原版帝国 preset、civic/authority/origin 组合、普通星球与特殊载体、人口和岗位前置条件。
- 状态观察：游戏日志、错误日志、调试提示、UI/OCR、存档 ZIP/gamestate、截图与动作证据。
- P 语言运行语义：scope、trigger/effect、decision、deposit、modifier、事件目标与持久化。
- 本地化与 UI：简体中文实机中的原始 key 泄漏、长菜单、DPI/坐标系、键盘布局与输入法；英文及其他翻译语言只做静态键、编码、引用和占位文本检查。
- 回归生命周期：冻结游戏/Mod 哈希，准备、执行、保存、重载、断言、清理及历史证据保留。

## 第一批拟落地能力

1. `prepare` 可选写入隔离 userdir 的定时命令，并在 manifest 中冻结；默认运行保持无注入。
2. 用声明式运行 profile 组合帝国、命令、目标日期和断言，语言固定为 `l_simp_chinese`，避免把 I1-003 特例硬编码进工具。
3. 在关键阶段自动采集资源、日期、暂停状态、窗口尺寸、DPI 感知、OCR 与日志摘要。
4. 存档断言同时检查容器、`gamestate` 目标键、出现次数和重载后的 UI 数值。
5. 日志按当前 Mod 路径/命名空间归因，区分环境噪声、引擎警告和被测脚本错误。
6. 对非机仆、失控机仆、普通殖民地和特殊载体建立最小政体/载体矩阵，避免只测 happy path。
7. `prepare` 可选接收一个已验证 ZIP 存档作为 seed，复制到隔离 userdir 并冻结源/副本哈希；用于简体中文的反向政体和重载夹具，不能替代当前版本新游戏基线。

## 第一轮调研结果（2026-09-06）

### 4.3/4.4 经济与劳动力模型

- Paradox 官方《Stellaris Dev Diary #407 - The 4.3 ‘Cetus’ Open Beta》说明：每人口岗位来源已大量改为静态岗位数，失业人口月末转为 Civilian/Maintenance Drone，多类产出加成改为岗位效率，并调整了殖民地自动化与观察者 UI。来源：<https://forum.paradoxplaza.com/forum/developer-diary/stellaris-dev-diary-407-the-4-3-cetus-open-beta.1887023/page-21>。
- 本机 4.4.6 `localisation/*/megacorp_l_*.yml` 的 `EXPLAIN_WORKFORCE_NOT_LIMITED`、`EXPLAIN_WORKFORCE_OF_LIMIT` 和 `JOB_WORKFORCE_SLIDER*` 进一步确认：岗位 UI 同时存在当前劳动力 `CURRENT`、玩家限制 `LIMIT` 和脚本最大容量 `MAX`。岗位卡片显示的已分配劳动力不能代替最大容量断言。
- 夹具结论：岗位类 Mod 至少采集四层数据——modifier 静态合同、当前/最大劳动力提示、符合条件人口是否实际转入、存档/reload；只截一张岗位列表会产生假红或假绿。

### 可重复状态构造与保存

- 本机 4.4.6 `tools/commands_at_date.txt` 明确要求把文件复制到 userdir，按未来游戏日期执行控制台命令；过期日期不会补执行，且不支持铁人/多人。运行 `20260906T105249Z` 已以 `minerals 5000` 实机证明资源注入成功。
- 夹具结论：资源、AI/观察者开关、效果注入和测试存档优先安排为不同日期的定时命令；manifest 必须记录原始顺序与文本。对 scope 敏感的 `effect` 仍需用目标存档/日志确认实际作用对象，不能因命令被调度就判成功。
- 已落地 `inspect-save`：定位隔离 userdir 中指定 `.sav`，验证 ZIP 容器，记录文件与 `gamestate` 的大小/SHA-256、成员列表，并对目标 token 做精确计数。I1-003 首次完成存档已证明目标 deposit 恰好出现一次；下一步把 token 从易受 shell 引号影响的 CLI 参数提升为声明式断言文件。
- I1-003 重复执行进一步证明：Stellaris 4.4.6 的 `add_deposit` 对同一个 type 会生成不同实例 ID，两个实例可同时绑定同一 `deposit_holder`，对应岗位 `MAX` 线性增加；存档检查的计数因此是行为断言，不只是完整性检查。

### 版本冻结与兼容回归

- Paradox 官方补丁说明反复提醒旧存档不保证跨版本完全兼容，并建议通过 Steam Betas 回退所需版本。来源：<https://forum.paradoxplaza.com/forum/threads/dev-team-official-2-0-2-patch-released-checksum-5e2f.1084989/>、<https://forum.paradoxplaza.com/forum/threads/dev-team-3-7-4-patch-released-checksum-fc72.1576252/>。
- 夹具结论：可复现运行必须同时冻结游戏 EXE 哈希、版本/校验和、Mod 树哈希、固定的简体中文语言、DLC/Mod 装载集合和存档哈希。跨游戏版本复用历史存档只能做迁移场景，不能覆盖当前版本的新游戏基线。

## 完成标准

- 网络调研结果补入本文或专题文档，包含可点击来源与本机复核结论。
- 每项进入实现的能力先更新需求/设计文档，再修改工具。
- 工具变更通过单元测试和真实 Stellaris 隔离运行；Mod 仍须先通过 `open_kaishek`。
- I1-003 当前验收不等待全部长期调研完成：先使用已确认的定时命令、实机 UI、日志和存档能力闭环，再把可复用经验回填本文。
- 本项目运行时能力只在简体中文上验收；英文及其他语言的翻译仅通过静态本地化合同，不安排语言切换实机。
