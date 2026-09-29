# PR-05 奖励候选契约审计（2026-09-29）

## 目标与范围

验证正式 Mod 的两层正面特质候选与四种可重复增益在 Stellaris 4.5.1 下保持设计契约：机械池先于机械兼容池、兼容池先于迭代池；同层合格候选等权；每次只执行一个主体物种奖励；已持有、相互冲突及帝国条件不合的候选不参与抽取。原版数值及机械物种许可沿用现有 `audit_compat_traits.py` 核对。

本项是只读静态审计，正式 Mod 与生成器均不改。此前已有机械池到兼容池再到迭代池的实机压力存档，以及四种迭代数值的 `1/2` 层实机对照；本项补足候选定义逐项核对，不把静态条件误报为所有候选的运行时数值证明。

## 方案与验收标准

新增只读脚本解析正式 `shishan_code_award_reward` 效果的三条分支及嵌套块，而非只统计特质键出现次数。逐项核验：

1. 两层分别恰有生成器白名单中的 20/19 个不同候选，顺序一致；第三层恰有四种迭代键。
2. 外层存在合格候选的判定，与对应抽签项的 `factor=0` 排除条件完全相同；每项原始权重都为 `1`。已持有原键和映射键、互斥键、格式塔与食物经济条件由白名单逐项给出，不能在输出脚本中遗漏。
3. 每一抽签项只对 `owner_main_species` 加入对应特质；迭代项还恰好给相同后缀的国家计数 `+1`。不允许其他主体物种或全国资源副作用混入。
4. 重新运行 `audit_compat_traits.py`，19 个映射的数值与当前原版特质相同，且允许 `MACHINE ROBOT`；再次运行 `open_kaishek` 正式包检查。

通过时记录具体数量、检查输出及已有实机证据边界；失败时先修复来源，再复验。若发现 Stellaris 特有的脚本语法新事实，补入本仓库知识库。

## 执行结果

`py tools/shishan_code/audit_reward_contract.py --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris'` 返回 `PASS (20 robotic, 19 compatible, 4 iterative)`。解析到正式奖励效果恰有 `if`、`else_if`、`else` 三条互斥分支；前两层每个候选的外层可用条件与对应抽签项的零权排除条件完全相同，同层基础权重均为 `1`，唯一发放目标均为主体物种。第三层四项分别把自身国家计数加 `1` 并给主体物种添加同后缀特质。20 个原版机械候选在 4.5.1 的 `05_species_traits_robotic.txt` 中均声明 `ROBOT MACHINE` 与 `positive` 标签。

`py tools/shishan_code/audit_compat_traits.py --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris'` 返回 `PASS (19 vanilla effects and machine archetypes)`：兼容映射的 19 个数值修正与当前原版一致，且都许可机械两种物种原型。正式包 `open_kaishek` 返回 `PASS`（19/19 脚本、13 DDS、172 个本地化键），报告位于 `_runtime/shishan_code/accept_reward_contract_20260929.json`；`git diff --check` 为零。

**结论：PR-05 的静态候选、等权与映射契约通过。** 既有实机奖励池压力存档只证明实际抽到的候选及层切换，兼容特质的有效数值只以一项岗位特质和四种迭代增益完成受控实机对照。没有对 39 个白名单候选逐一做实机数值对照，也没有以随机样本证明统计等概率；这些仍属于 PR-05 整体验收边界。
