# PR-01 第二次持续优化费用与复发状态验收（2026-09-29）

## 目标与范围

正式验收矩阵要求 `n=2` 时「持续优化」费用为 `8000` 社会学，而现有自然研究证据只到 `n=1` 时下一次费用 `6000`。本轮从已自然完成一次优化且未复发的正式单 Mod 原生存档出发，验证第二次优化的实际社会学研究队列、成功后的计数与奖励、第三次费用，并检查抽签分支对应的局势和项目状态。正式 Mod 脚本不改；如研究成本太高，仅在隔离 Mod 副本加入已验证的社会学加速夹具，完成后移除夹具并使用正式单 Mod 重载。

## 方法与验收标准

使用 `pr04_optimize_natural_no_relapse_post_22290727.sav` 作为 `n=1` 锚点，先在正式单 Mod 中确认项目 GUI 费用 `6000`，启动项目，保存研究中存档并核对社会学队列。正常研究完成后核对 `last_completed_special_project=SHISHAN_CODE_OPTIMIZE`、`n:1→2`、主物种恰好一个合法奖励、白绮阶梯修正各为 `2` 层。若未复发，应仍无局势、保留唯一「重构完成」及全国岗位产出修正，下一次优化显示 `8000`；若复发，应唯一「大厦将倾」从进度 `0` 开始、主物种恢复「屎山代码」、移除岗位修正，并显示维护 `4000`、清理 `12000`。接受随机抽签的实际结果，另一支须以可记录抽签的受控夹具单独验证。由原生存档核对实际社会学研究进度及单位，截图佐证 GUI。保存完成结果并用正式 Mod 重载，排除加速夹具持久化。

前次未复发弹窗标题已修复，本轮顺便核对简体中文新标题和白绮台词。记录游戏版本、Mod 校验和、Steam F12 截图、存档 SHA-256、日志和 `open_kaishek` 结果。`n=2` 的静态公式为 `4000+2000×2=8000`，但只有实机 GUI 与项目队列验证后才能把相应运行时子项判通过。

## 执行结果

从既有[第一次优化自然完成存档](../assets/shishan-code-origin/evidence/pr04_optimize_natural_no_relapse_post_22290727.sav)复制到新的隔离用户目录，启用与正式仓库逐文件 SHA-256 相同的 64 个 Mod 文件。Stellaris 4.5.1 正式单 Mod 校验和 `ba99`；在 `2229.07.27` 的[研究前 GUI](../assets/shishan-code-origin/evidence/pr01-optimize-n1-cost-2229.07.27.jpg)显示「持续优化」费用 `6000` 社会学、预计 `264` 个月。玩家点击研究后，[研究中 GUI](../assets/shishan-code-origin/evidence/pr01-optimize-n1-in-progress-2229.07.27.jpg)显示取消按钮；同日[原生存档](../assets/shishan-code-origin/evidence/pr01-optimize-n1-in-progress-2229.07.27.sav)的项目 ID `4` 为 `status=in_progress`，`society_queue` 指向该 ID，`n=1`，无临时修正。

将先前已验收的 `shishan_test_society_boost` 静态修正**仅复制到隔离 Mod 副本**，其 SHA-256 为 `7c60f6fbdfeca5db0b79340d1496e69156baecf15f694546a1225f72667ea9e6`。隔离夹具经 `open_kaishek` 为 `PASS`（20/20 脚本、13 DDS、172 本地化键）；夹具校验和 `9bab`。加载研究中存档，控制台授予该社会学速度修正，再 `fast_forward 35`；没有调用 `complete_special_project` 或手工调用 Mod 结算事件。正常研究完成后，于 `2229.09.02` 出现[「持续优化完成」白绮弹窗](../assets/shishan-code-origin/evidence/pr01-optimize-n2-natural-complete-2229.09.02.jpg)，这次抽到 90 权重**未复发**分支。游戏内立即移除临时修正；[下一次费用 GUI](../assets/shishan-code-origin/evidence/pr01-optimize-n2-next-cost-2229.09.02.jpg)显示 `8000` 社会学。保存[完成态原生存档](../assets/shishan-code-origin/evidence/pr01-optimize-n2-natural-post-2229.09.02.sav)，无夹具修正引用。

[严格审计脚本](../tools/shishan_code/audit_pr01_optimize_n2.py)与[JSON 结果](../assets/shishan-code-origin/evidence/pr01-optimize-n2-audit-2026-09-29.json)均为 `PASS`：`n:1→2`；旧研究队列结束，下一项目 ID 变为 `5`；主物种只新增 `trait_robot_harvesters`，保留前次 `trait_robot_integrated_weaponry`；白绮工程和社会阶梯修正各恰好一份、倍率 `2`；全国岗位增产修正恰一份，局势为零。完成态仍为 `last_completed_special_project=SHISHAN_CODE_OPTIMIZE`，研究前后没有其他主物种特质删除。

随后停止游戏，从用户目录移走唯一夹具文件，正式 Mod 副本恢复为与仓库 64/64 文件逐字节相同，正式 `open_kaishek` 再次 `PASS`（19/19 脚本、13 DDS、172 键）。全新正式单 Mod 进程、校验和 `ba99` 重载完成态，[情报日志截图](../assets/shishan-code-origin/evidence/pr01-optimize-n2-formal-reload-2229.09.02.jpg)仍为费用 `8000`、预计 `362` 个月，左侧无局势。正式重载 `error.log` 仅有离线 Workshop 缺失文件提示，没有新增本 Mod 脚本错误；其余语言仍仅做静态校验，运行时不在范围内。

| 归档文件 | SHA-256 |
| --- | --- |
| 研究前 GUI | `118fd4589e111b895a71b2a2cdc22c2770630a7bf1b5a605c7923b8cef37efee` |
| 研究中 GUI / 存档 | `688873ae279c4a2736e5140aa710a6853a5582b0e470135cd5afc32cfdcb46d3` / `4de8b7b76b9cdaae0a7fd577c670d4c56d19905362c550ab5cbdff000043926f` |
| 自然完成弹窗 / 存档 | `4a917d48527c0461f99c0218c1cd17465d3e8bc7b3b0dd5a981d2122a9ee9004` / `ca1d2f8f6c5792b545d507f4b4c803b3a8bd1c1fd6f076771d6ee46fd6925d31` |
| 下一次费用 / 正式重载 GUI | `7d0a12f1ecc58551e19f1ace04b07f4a20de83761832ebaf34fc30393f2b3599` / `54282eebe6cc800fe2f4056c831e316391b6cf401c991ad815863cea63247136` |
| 审计 JSON | `8f034a3121aaef8db2de0906e49b864782022e741fdca0ddbec8da9809f8b38a` |

**PR-01 的第二次持续优化研究、`n=2` 后 `8000` 费用、自然结算和正式重载子项通过。** 此次加速结算没有取得恰好 `6000` 点逐点扣除的阈值样本，故“显示费用与实际所需点数完全相等”仍由脚本成本定义与已有普通进度证据支持，不单凭本轮截图宣告该精确阈值已实测。
