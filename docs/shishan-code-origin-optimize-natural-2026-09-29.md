# PR-04 持续优化自然研究验收（2026-09-29）

## 目标、范围与方法

验证已重构的正式单 Mod 存档中，「持续优化」由玩家在简体中文 GUI 启动、进入社会学项目队列、经正常月结算完成，而不只是通过调试命令直接调用完成回调。基线采用已归档且自然完成清理的 `clean_natural_post_22290622.sav`：局势已结束、主体物种有「重构完成」、`n=0`、项目费用为 `4000`。先在无测试修正的正式 Mod 副本中启动项目并保存研究中基线，检查 `society_queue`、项目仍存在及费用。

为缩短约 `4000` 社会学研究的等待，只在隔离用户目录的 Mod 副本中加入无 BOM UTF-8 的测试静态修正 `shishan_test_society_boost = { country_society_research_produces_mult = 1000 }`；先让 `open_kaishek` 检查该隔离副本，重启游戏，加载研究中基线后用控制台给玩家临时添加此修正。不得修改正式 Mod 的项目定义、完成回调或随机权重，也不得使用 `complete_special_project` 冒充自然完成。完成后立即撤销测试修正，再保存、退出并移走隔离测试文件，用正式单 Mod 重载结果。

通过标准：正常月结算后 `last_completed_special_project=SHISHAN_CODE_OPTIMIZE`，旧队列结束，`n:0→1` 恰好一次，下一次优化费用为 `6000`，主物种恰好新增一次有效奖励。随机的 90% 未复发或 10% 复发两支接受实际结果；若未复发，保持「重构完成」和无局势；若复发，移除「重构完成」、恢复「屎山代码」，只出现一个进度为 `0` 的局势，项目名恢复「维护屎山」且费用为 `3000`、清理费用为 `10000`。后续正式单 Mod 重载必须保持所有状态。记录项目过程和结果的画面、存档、哈希及脚本日志。单次自然抽签只验证发生的分支，不用于估计 10% 概率；另一分支沿用先前强制回调的结构化验收。

## 执行记录

从正式单 Mod、无测试修正的 `2229.06.22` 存档，在情报日志中点击「持续优化」研究；GUI 显示费用 `4000`，按钮变成「取消」、状态为“研究中”。保存[研究中基线](../assets/shishan-code-origin/evidence/pr04_optimize_research_pre.sav)，SHA-256 为 `f0c52bf10e87bdb907af423eb360c4fbed31615a37fccf8dcd6c5510e2d339c5`；`gamestate` 中 `SHISHAN_CODE_OPTIMIZE` 项目状态为 `in_progress`、`n=0`、无局势，尚无临时加速修正。

隔离测试副本仅新增无 BOM UTF-8 静态修正 `shishan_test_society_boost = { country_society_research_produces_mult = 1000 }`，其文件 SHA-256 为 `7c60f6fbdfeca5db0b79340d1496e69156baecf15f694546a1225f72667ea9e6`；`open_kaishek` 对副本为 `PASS`（20/20 脚本，报告 `_runtime/shishan_code/accept_pr04_optimize_fixture_20260929.json`）。第一次控制台输入 `effect add_modifier=shishan_test_society_boost` 被 4.5.1 日志拒绝：`Expected "add_modifier = {"`；正确命令为 `effect add_modifier={modifier=shishan_test_society_boost days=-1}`。控制台随后回显社会学产出 `+100000%`，再执行 `fast_forward 35`，由游戏自然研究流程触发完成事件，没有使用 `complete_special_project`。

本次随机结果是**未复发**。游戏停于 `2229.07.27`，白绮完成事件显示，旧研究项目消失；情报日志重新出现「持续优化」，费用 `6000`。执行 `effect remove_modifier=shishan_test_society_boost` 后保存[完成结果](../assets/shishan-code-origin/evidence/pr04_optimize_natural_no_relapse_post_22290727.sav)，SHA-256 为 `df9de04b00a936455bc53e1a270469a174fb9c79e59b04fa001ad00bd82826ad`。存档中 `last_completed_special_project=SHISHAN_CODE_OPTIMIZE`、`n=1`、主体机械物种新增原版正面特质 `trait_robot_integrated_weaponry` 恰好一次，仍有「重构完成」，局势为零；测试加速修正已无存档引用。[完成弹窗](../assets/shishan-code-origin/evidence/pr04-optimize-natural-event-2229.07.27.jpg)与[下一次费用](../assets/shishan-code-origin/evidence/pr04-optimize-natural-next-cost-2229.07.27.jpg)均为 Steam F12 实机截图。

发现一处界面文案：虽然情报日志的项目名已正确显示「持续优化」，未复发时复用的白绮弹窗仍以「维护完成」为标题，并可能说“旧核心还在呼吸”。这不影响已观察到的项目结算，但与重构后“持续优化”的语境不一致，列入后续文案修正。另有隔离测试修正缺少本地化引发的日志提示；该文件已从用户目录移走，正式 Mod 树与隔离用户目录的 64 个 Mod 文件现已逐字节一致，正式 Mod 重跑 `open_kaishek` 为 `PASS`（19/19 脚本，169 本地化键，报告 `_runtime/shishan_code/accept_pr04_formal_reloaded_20260929.json`）。

从正式单 Mod 校验和 `0d87` 全新启动并重载完成结果后，[情报日志画面](../assets/shishan-code-origin/evidence/pr04-optimize-natural-reload-2229.07.27.jpg)仍只有「持续优化」可研究，费用 `6000`；左侧无「大厦将倾」局势。加载后的估计研究时间从测试加速时的 `1` 个月恢复为 `264` 个月，证实临时修正没有作为运行依赖残留。**PR-04 的未复发自然研究完成及存档重载子项通过**；复发随机分支由先前强制完成回调覆盖，但没有在本轮自然抽中。
