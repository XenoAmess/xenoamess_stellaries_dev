# PR-04 持续优化自然完成后的复发分支验收（2026-09-29）

## 目标与范围

现有正式单 Mod 自然研究两次优化都抽到未复发，10% 复发仅有直接调用正式分支回调的受控证据。本轮从已归档的 `n=1`、第二次优化研究中原生存档出发，使用隔离 Mod 副本固定抽签为复发，让项目仍由社会学研究队列自然完成，验证项目成功结算至复发事件、局势和后续项目的完整链路。正式 Mod 脚本和先前证据保持不变。

## 方法与验收标准

隔离夹具只做两项可审计改动：在 `shishan_code.30` 的 `random_list` 中将未复发权重 `90` 改为 `0`、复发权重保持 `10`；复用已验证的 `shishan_test_society_boost` 提高社会学研究速度。正式脚本仍保持 `90:10`，即标称复发概率 `10%`。夹具须先通过 `open_kaishek`，并记录与正式 Mod 的文件差异、哈希和运行校验和。加载正式版研究中存档后给玩家临时研究加速，正常推进到项目完成，不使用直接完成项目或直接调用 `shishan_code.31`。完成后移除加速修正。

成功标准：`n:1→2` 恰好一次、社会学队列结束、主物种恰获一次有效奖励；旧「重构完成」特质及全国岗位产出修正删除，旧「屎山代码」恢复；只出现一个「大厦将倾」，其创建时进度从 `0` 起算，往后按正常月速推进；后续项目改为「维护屎山」成本 `4000`、清理成本 `12000`；白绮复发对白由对应池展示，修正层数与新的 `n` 一致。原生存档和 Steam F12 截图均归档。然后移除夹具，用正式单 Mod 全新进程重载，前述状态不改变；正式 Mod 必须再次通过 `open_kaishek`。若自然研究终点晚于局势首个结算月，应从事件发生日期与月速计算进度，不把非零保存进度误判为没有从零开始。

当前仅以一次固定权重的分支覆盖功能，不用少量随机样本估计概率；对正式脚本 `90:10` 另做静态核对。非中文语言只进行静态验收，运行时不在范围内。

## 执行结果

- 正式版 `shishan_code_events.txt` 保留未复发与复发 `90:10`。隔离夹具只将前者改为 `0`，后者仍是 `10`；两版事件文件 SHA-256 分别为 `a97594ad94cd528760eb33e27d7a8a2f8c2663e63ae667014cf59592aaa2f1e8` 和 `634314fe2d39fcdd063bd9c7a9416c6aeb622279f472c77a8f3831e1435c7143`。隔离夹具另有临时社会学加速静态修正，正式目录无此文件。夹具运行校验和为 `3350`，`open_kaishek` 为 `PASS`（20/20 脚本、13 DDS、172 个本地化键）。
- 从[第二次优化研究中存档](../assets/shishan-code-origin/evidence/pr01-optimize-n1-in-progress-2229.07.27.sav)加载，给予临时社会学加速后正常推进至 `2229.08.05`。游戏完成研究并展示[白绮复发事件](../assets/shishan-code-origin/evidence/pr04-relapse-natural-vivhite-2229.08.05.jpg)，没有直接调用项目完成或复发事件命令。移除临时修正后在同日保存[原生存档](../assets/shishan-code-origin/evidence/pr04-relapse-natural-post-2229.08.05.sav)，SHA-256 为 `cb315dbb13414dfac07667c89da40c77effc6d546ceaff73a07fa6e8118ea0c5`。
- [原生存档审计](../assets/shishan-code-origin/evidence/pr04-relapse-natural-audit-2026-09-29.json)通过全部 8 项断言：`n:1→2`、社会学队列结束、主物种只得到一次正面机械特质 `trait_robot_artificial_engineers`，并以 `trait_shishan_code` 取代 `trait_shishan_refactored`；全国重构岗位增产修正从 `[1]` 变为 `[]`；仅创建一个 `situation_shishan_code`，存档原生进度为 `0`；白绮研究修正仍只有一份基础层和两层累计层；维护、清理项目恢复，优化项目退出；存档中不存在临时加速修正。[局势截图](../assets/shishan-code-origin/evidence/pr04-relapse-situation-2229.08.05.jpg)中的 `7.0` 是“下月预计 +7.0”，不是已累计进度。
- 夹具状态下的项目费用界面：[维护 `4000`](../assets/shishan-code-origin/evidence/pr04-relapse-maintain-cost-2229.08.05.jpg)、[清理 `12000`](../assets/shishan-code-origin/evidence/pr04-relapse-clean-cost-2229.08.05.jpg)。随后把运行目录恢复到与正式 Mod **64/64 文件逐字节相同**，正式 `open_kaishek` 再次 `PASS`（19/19 脚本、13 DDS、172 键）。全新进程启动的正式校验和为 `ba99`；重新加载同一存档后，简中界面仍显示[局势当前进度 `0.0/1000.0`、下月预计 `+7.0`](../assets/shishan-code-origin/evidence/pr04-relapse-formal-reload-situation-2229.08.05.jpg)、[维护 `4000`](../assets/shishan-code-origin/evidence/pr04-relapse-formal-reload-maintain-2229.08.05.jpg)和[清理 `12000`](../assets/shishan-code-origin/evidence/pr04-relapse-formal-reload-clean-2229.08.05.jpg)。

**结论：PR-04 复发分支的自然研究结算和正式版重载子项通过。** 这是固定抽签的分支覆盖，不能据此统计真实复发频率；正式随机权重仅有脚本静态证据。非中文语言静态校验通过，运行时不在范围内。整体验收仍需处理其他矩阵余项。
