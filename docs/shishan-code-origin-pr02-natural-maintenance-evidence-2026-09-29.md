# PR-02 自然维护完成原生证据归档（2026-09-29）

## 目标与范围

既有[实机记录](shishan-code-origin-runtime-findings-2026-09-27.md)描述了一次 `n=1→2` 的自然「维护屎山」研究终点，但原生存档仍仅在隔离用户目录，仓库缺少可直接复核的输入。把研究中的前存档、自然完成的后存档和当时 Steam F12 画面归档，严格区分临时社会学加速夹具与正式 Mod。此工作不改正式 Mod 或项目效果。前存档局势进度 `12`，属第一阶段；此前第五阶段另有受控项目完成证据，两种完成方法须分开陈述。

## 验收标准与方法

复制既有原生 ZIP 存档及游戏内截图，逐文件记录 SHA-256。从 `gamestate` 读取前后日期、`society_queue` 中的项目进度、项目状态、`shishan_code_maintenance_count`、局势进度与月速度、白绮科研修正倍率、主体物种奖励。前存档必须仍研究中；后存档必须显示自然项目已完成，`n` 恰增一次，月速度加 `1`，旧特质保留且新增一个正面奖励。因完成弹窗与后存档相隔四个月，后存档不能直接显示归零瞬间；以事件截图的完成时间、后存档的 `28=4×7`、项目完成字段和正式效果脚本共同判断归零。核对简中截图的完成事件及下一轮维护/清理费用。后存档含隔离测试加速修正，不能作为正式单 Mod 重载的通过证据；正式版的静态校验单独运行 `open_kaishek`。

## 执行结果

[研究中存档](../assets/shishan-code-origin/evidence/pr02-maintain-natural-pre-2226.11.17.sav)为 `2226.11.17`，主国 `society_queue` 的维护项目 ID `5` 已累计 `56.43412` 社会学研究点；`n=1`、局势第一阶段进度 `12`、月进度 `6`、主体机械物种 ID `855638017` 尚无 `trait_robot_artificial_sociologists`，也没有临时研究加速修正。GUI 当时显示项目成本 `3000`，见[既有实机记录](shishan-code-origin-runtime-findings-2026-09-27.md)。

隔离夹具仅为国家添加 `shishan_test_society_boost` 加快**社会学研究产出**；游戏正常研究进度在 `2227.01.04` 触发[「维护完成」白绮弹窗](../assets/shishan-code-origin/evidence/pr02-maintain-natural-complete-2227.01.04.jpg)，右侧局势月进度已为 `7.0`。该弹窗不是通过 `complete_special_project` 触发。后续继续运行到 `2227.05.17` 才保存[完成后存档](../assets/shishan-code-origin/evidence/pr02-maintain-natural-post-2227.05.17.sav)及[下一轮维护费用截图](../assets/shishan-code-origin/evidence/pr02-maintain-natural-next-maintain-2227.05.17.jpg)/[清理费用截图](../assets/shishan-code-origin/evidence/pr02-maintain-natural-next-clean-2227.05.17.jpg)。这三张画面显示维护费用 `4000`、清理费用 `12000`、局势月速度 `7.0`。

[只读审计脚本](../tools/shishan_code/audit_pr02_natural_maintenance.py)对原生存档返回 `PASS`，机器可读[结果](../assets/shishan-code-origin/evidence/pr02-natural-maintenance-audit-2026-09-29.json)的 SHA-256 为 `ba5b748be9b4d7df98c80b850ee0424baed0a3e875174809b290fe517aaa7415`。前后存档的 `n:1→2`，旧维护研究队列消失，玩家 `last_completed_special_project=SHISHAN_CODE_MAINTAIN`，月进度 `6→7`；主体物种保留唯一一个 `trait_shishan_code`，新获唯一一个 `trait_robot_artificial_sociologists`。后存档进度 `28` 是完成后四个月按 `7/月` 再次前进的结果，符合回到零后重新累计；后存档有一处临时加速修正引用，**不作为正式 Mod 干净重载证据**。前/后存档 SHA-256 分别为 `34cf5985b1c346588a500a80ca0e01b03abd4b60331ec7b26c62370eaf0f13b2`、`17e68bec9fbdb30b84585b5cea9338a3e8519bf23e4bb69b13a3f4d5894ec403`。三张截图 SHA-256 依次为 `863de935d97aeb95e9cf043174d0bbf10e93b85b0313a060a5b2898f850c97ea`、`ca4acad22e3a8c631640b9b7488eb5b555e9d03392b236821b9d4e83686e1d51`、`22c54fe7ce8aaa139f15a375bce1d5b2dbf5adac8a738b587fa7116a8523f89a`。

此前第五阶段以游戏控制台精确项目键触发真实完成效果，已在[原实机记录](shishan-code-origin-runtime-findings-2026-09-27.md)单独记载；它证明第五阶段切回第一阶段的完成效果，不能冒充自然研究终点。第一阶段自然研究完成子项至此有可复核原生证据，PR-02 仍有取消/中断及全奖励候选的独立检查。

当前正式 Mod 的 `open_kaishek` 复核为 `PASS`（19/19 脚本、13 DDS、172 本地化键），没有把隔离测试修正写入正式包。
