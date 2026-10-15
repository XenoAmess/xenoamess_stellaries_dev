# 实际人口驱动的物种操作与奖励开窗预检

## 目标与证据

依照[缓存延迟修复设计](feedback-redesign-owned-species-cache-fix-2026-10-15.md)，本次修复 rc4 同日清理后真实新模板被旧 `owned_species_refs` 缓存遗漏、导致有限奖励误判耗尽的问题。主任务原生探针已确认同一现场 `any_owned_species` 找不到 refactored 模板，而 `any_owned_pop_group -> species` 能找到；证据为 `rc4-species-cache-result` 与 `rc4-pop-live-species-result`。资格源码没有要求 `trait_shishan_code`，也未禁止 `trait_shishan_refactored`，不能以扩大状态资格替代缓存根因修复。

只修改奖励生成器、生成的奖励 effects/triggers/events，以及 architecture effects。由主任务统一维护版本、G1、运行副本和实机，不改存档或缓存字段。

## 原生依据与方案

rc3 本次生成的 `logs/script_documentation/scopes.log:42` 说明 `species` 支持 pop_group 并输出 species；`effects.log:5689` 说明 `every_owned_pop_group` 支持 country。当前 4.5.2 原版 `events/clone_army_events.txt:630` 也在国家 `every_owned_pop_group` 内切入 `species` 执行物种操作；`events/caravaneer_events.txt:5477` 在同类人口迭代内使用 `modify_species`。这里只借用原生作用域，不采用原版示例的全局共享模板修改。

所有候选资格直接遍历实际正人口组，保留主体谱系比较，进入该组的 `species` 检查原有 archetype、互斥和已有特质，国家 DLC/思潮/食物条件继续留在国家作用域。领取及重构/复发同样以实际正人口组为入口，然后调用既有国内安全 clone helper。

领取和状态替换的迭代 `limit` 内先检查资格，并在真正进入 `species` 执行前用内层 `if` 重新检查。既有 clone helper 一次迁移国内精确旧模板的所有人口组；若同一模板有多个组，即使引擎先选定了外层对象，后续组会读取更新后的物种，并被已有奖励特质或已替换状态特质拒绝。禁止把测试模型的迭代实现当作已证明的原生迭代顺序。

奖励窗口增加隐藏 `.1004` 事件作为预检：开窗 helper 设置唯一窗口锁后发送 `.1004`；它先执行现有 pending refresh，只有仍保有 pending 和窗口锁时才发送可见 `.1000`。`.1000` 继续要求 pending/锁，只计算覆盖率，不再在绘制过程中消耗奖励。真实耗尽仍由 refresh 按现有合同恰加一次 R、finish 清理 pending/锁并发送重复结果；不会先画一个空的三选一窗口。使用隐藏事件边界，不把 refresh helper 嵌进 open helper，以免重新形成五层 scripted effect 初始化链。

## 验收标准

静态：39 条资格不含缓存物种枚举；39 条领取与两个状态入口使用实际正人口组且有执行前重检；原版资格、234 个显式 NOT/AND 权重守卫、权利继承、使节与白绮肖像修复保留；生成器与三个生成文件一致，无新原始本地化 key。程序模型覆盖滞后缓存、同模板多组及内层 guard 缺失负例、同日清理后重开、真耗尽预检清锁且不发 `.1000`。

原生：在同日清理后 R 保持 0、原三个仍合格槽保留并可领取，领取只影响国内实际模板且冷却只减一次；重构/复发与立即后续奖励也能找到新模板。另以真正耗尽的 pending 案例确认只给一次重复结果、没有空选项窗口及遗留窗口锁。先 G1，再由主任务统一运行简体中文实机。

## 开发结果

生产生成已完成。39 条资格全部使用 `any_owned_pop_group`；39 条领取和两个状态入口全部通过正人口组进入实际物种，外层 limit 与内层执行前 limit 一致。生成结果与生成器逐字节一致，全部 P 文件成功解析；不再包含缓存式 `any/every_owned_species`；234 个 NOT/AND 权重守卫、三个继承权利节点、使节及白绮肖像修复仍在。

隐藏 `.1004` 已成为唯一常规开窗前置，先 refresh，再以 pending 与窗口锁双守卫发送 `.1000`；可见 `.1000` 不再执行会消耗票据的 refresh。所有 Mod 事件 ID 无重复。实际 scripted effect 调用图无环，最长 helper 链仍为 4：`award_reward -> architecture_award_repeat_effect -> architecture_refresh_effect -> architecture_migrate_effect`，未引入原生初始化五层深度风险。

开发静态检查通过，尚未运行 G1 或 rc5 实机。该结果不证明原生人口迭代顺序、权利持久化或同日重开已经通过；主任务继续统一验收。

源文件 SHA-256：

- 生成 rewards effects：`dda16c87ec0b3d41ab516942bcf7761e0c789191a565946d4c3dece36e2ec540`。
- 生成 rewards triggers：`1a2899a2ab50ccd48531b9b3d676efdaa7ea6ad7ff22f385fe06cf1b8657058f`。
- 生成 rewards events：`38aafcd5c0644fbb420f8115c9d42f0d13211c2e5087d0581caf44d06e778a3b`。
- architecture effects：`d9714f74ccea754553d815d5a8d88d3260acd212efecd02e1de5a3f6fd4e0663`。
