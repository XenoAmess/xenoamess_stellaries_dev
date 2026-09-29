# PR-02 复发后维护项目取消验收（2026-09-29）

## 目标、范围与方法

沿用[正式版复发存档](../assets/shishan-code-origin/evidence/pr04-relapse-natural-post-2229.08.05.sav)的 `n=2`、局势第一阶段状态，在正式单 Mod 简中游戏里启动第三次「维护屎山」。正常推进到社会学队列累计正进度后，先保存研究中存档，再从情报日志取消项目并于同日保存。用原生存档比较 `n`、主物种特质、白绮修正、局势进度、研究队列和项目实例；用 Steam F12 截图验证项目恢复为可研究且费用保持 `4000`。测试仅覆盖真实 UI 取消，不把控制台直接触发回调算作项目完成。

## 验收标准

取消前的项目必须为 `SHISHAN_CODE_MAINTAIN`，社会学队列进度大于 `0`；取消后项目仍可重新研究、社会学队列不再指向原研究实例。两份同日存档的 `n=2`、主物种特质、白绮基础及累计研究修正、局势进度都相同，且不出现新的完成奖励。若取消后需要下一游戏日才重新显示，应按实际事件时序记录；不因等待跨月造成的自然局势前进误判为取消改变进度。

本项承接[总验收方案](shishan-code-origin-acceptance-plan.md) PR-02；它不能替代第五阶段维护自然完成、研究队列中断或恶意重复直接调用回调的测试。正式 Mod 还须通过 `open_kaishek`，非中文语言仅静态校验，运行时不在范围内。

## 执行结果

正式 Mod 64/64 文件与运行目录逐字节一致，启动校验和 `ba99`；本轮正式版 `open_kaishek PASS`（19/19 脚本、13 DDS、172 键）。从复发后存档启动第三次维护，正常推进 35 游戏日至 `2229.09.10`，[界面显示研究进度 `28/4000`](../assets/shishan-code-origin/evidence/pr02-n2-cancel-in-progress-2229.09.10.jpg)。[研究中存档](../assets/shishan-code-origin/evidence/pr02-n2-cancel-in-progress-2229.09.10.sav)的原生社会学队列记录 `progress=28.33912`、`special_project=5`，项目实例状态 `in_progress`。

在同一暂停日期通过项目界面的“取消”按钮终止，[界面立刻恢复“维护屎山，可用”及费用 `4000`](../assets/shishan-code-origin/evidence/pr02-n2-cancel-post-2229.09.10.jpg)。[取消后存档](../assets/shishan-code-origin/evidence/pr02-n2-cancel-post-2229.09.10.sav)中项目实例仍是 ID `5`，状态已不再是 `in_progress`；社会学队列返回原科技 `tech_colonial_centralization`，不再指向维护项目。[原生对比审计](../assets/shishan-code-origin/evidence/pr02-n2-cancel-audit-2026-09-29.json)为 `PASS`（7/7）：`n=2`、主物种特质、白绮基础与两层累计修正、单个局势进度 `7`、最近成功完成的项目键全部保持一致；两份存档都无临时加速修正。研究中/取消后存档 SHA-256 分别为 `bb00f67df8acfd2c186c77b46c4076db1ccbfc9ae5cb7ba42ae06b54b7e85684`、`deb27893654458e8447a2eb814f1c506c427be1253ff6354f5295c9e4b025b2d`。

**结论：PR-02 `n=2` 第一阶段真实 UI 取消子项通过。** 原生队列曾累计真实进度，取消没有结算或清零局势。研究中断、恶意重复回调和第五阶段自然维护另行验收；本结果不覆盖它们。
