# UI-01 简体中文界面证据收口（2026-09-30）

## 目标与方法

按[既定验收矩阵](shishan-code-origin-acceptance-plan.md)逐项复核已归档的简体中文单 Mod 实机截图、项目研究终点和 v0.1.1 修复结果。此轮是只读证据复核，不把旧截图冒充新的实机运行；唯一新增归档是已拍摄的起源悬停截图。对未测试的随机对白变体或其他语言不作实机结论。

## 逐项结果

| UI-01 项目 | 证据与结论 |
| --- | --- |
| 起源与挑战警告 | [起源卡悬停](../assets/shishan-code-origin/evidence/ui01-origin-challenge-warning.png)实际显示完整简中设定、特质预算、机械资格和红色「警告：具有挑战性的起源」。红字位于悬停提示的「惩罚」区，右侧固定说明区没有重复显示。这符合现行 `negative_description` 脚本。该图从原隔离运行 `_runtime/shishan_code/20260927T163000Z/origin_selected.png` 原样复制，SHA-256 `6bb5a2158568b9bee0950a7b03639c1d854864835b4eb4fb062519547c71fcfd`。 |
| 五阶段与月进度 | [第一阶段与月速](../assets/shishan-code-origin/evidence/individual-machine-start-situation.jpg)、[第五阶段重载](../assets/shishan-code-origin/evidence/sv01-stage5-reload-situation-2229.10.15.jpg)可见情报日志标题、阶段效果和修正；II、III、IV 的简中截图与阶段边界已在[SC-03 实机记录](shishan-code-origin-runtime-findings-2026-09-27.md)逐项核对。 |
| 研究所与岗位 | [建筑解锁](../assets/shishan-code-origin/evidence/individual-machine-building-unlocked.jpg)、[维护员岗位](../assets/shishan-code-origin/evidence/individual-machine-maintainer-job.jpg)显示简中名称、描述和产出；两类机械政体的岗位来源另见[SC-05](shishan-code-origin-sc05-research-institute-2026-09-29.md)。 |
| 项目动态名称与费用 | [维护费用](../assets/shishan-code-origin/evidence/pr02-maintain-natural-next-maintain-2227.05.17.jpg)、[清理费用](../assets/shishan-code-origin/evidence/pr02-maintain-natural-next-clean-2227.05.17.jpg)、[清理后持续优化](../assets/shishan-code-origin/evidence/clean-natural-optimize-cost-2229.06.22.jpg)、[第二次优化后的费用](../assets/shishan-code-origin/evidence/pr01-optimize-n2-next-cost-2229.09.02.jpg)覆盖名称与随 `n` 变化的数字。 |
| 白绮肖像与四组对白 | [领袖列表与详情卡](../assets/shishan-code-origin/evidence/vivhite-leader-v2-stellaris-4.5.1.png)的 V2 半身像布局正确。交谈、维护、清理、复发四组的标题、正文、按钮和 A05 事件图分别见[交谈](../assets/shishan-code-origin/evidence/ui01-vivhite-talk-2205.04.26.jpg)、[维护](../assets/shishan-code-origin/evidence/ui01-vivhite-maintain-2205.04.26.jpg)、[清理](../assets/shishan-code-origin/evidence/ui01-vivhite-clean-2205.04.26.jpg)、[复发](../assets/shishan-code-origin/evidence/ui01-vivhite-relapse-2205.04.26.jpg)。清理后未复发的专属「持续优化完成」还见[独立事件图](../assets/shishan-code-origin/evidence/pr04-optimize-dialogue-fixed-2229.07.27.jpg)。这些截图各验证一个对白变体；随机候选的全部文案由本地化静态校验覆盖。 |
| 复活与禁止交谈 | [资源不足](../assets/shishan-code-origin/evidence/vivhite-reboot-insufficient-after-reload.jpg)、[足额复活](../assets/shishan-code-origin/evidence/vivhite-reboot-exact-resources-after-reload.jpg)及[待复活决议修复](shishan-code-origin-ui01-talk-tooltip-fix-2026-09-30.md)覆盖禁用提示、点击无反应、复活后可交谈。v0.1.1 修复后不再泄漏内部旗标。 |
| 奖励结果 | [耗尽后的迭代候选](../assets/shishan-code-origin/evidence/reward-pool-iteration-tier.jpg)与[岗位产出增益两层重载](../assets/shishan-code-origin/evidence/iteration-output-plus2-reload.jpg)可读，无原始键；候选逻辑和数值是否全面正确仍由 PR-05 专项矩阵判断。 |

以上已检的简中界面未见原始本地化键、乱码、占位符或艺术资源加载缺失。UI-01 对界面展示的验收为 **PASS**；这不替代 RS、PR 等机制矩阵中的未完成运行时组合。

正式 v0.1.1 再次通过 `open_kaishek`：19/19 P 脚本、13 DDS、173 本地化键，报告为 `_runtime/shishan_code/accept_ui01_close_20260930.json`。`audit_translations.py` 对八种非英文非中文官方语言报告英语原文残留 0、汉字占位 0；连同英文的包级键、文件头、编码、引用检查，九种非简中语言**静态校验通过，运行时不在范围内**。
