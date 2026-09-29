# PR-01 维护项目研究点阈值（2026-09-29）

## 目标、范围与方法

现有简中实机已显示 `n=2` 的「维护屎山」费用为 `4000` 社会学，项目已在社会学队列累计 `28.33912` 点，并有自然研究完成结果；尚缺费用阈值前后各一份进度存档。本轮只检验这一费用样本的实际研究点门槛，不改正式 Mod 的成本、回调或奖励逻辑。其他 `n` 和两类项目的费用仍以既有 GUI、动态脚本与自然项目路径共同判断，不把一个样本外推成所有项目的逐点实测。

从[第五阶段正式重载锚点](../assets/shishan-code-origin/evidence/sv01-stage5-reloaded-2229.10.15.sav)出发，保持 `n=2`、维护项目 ID 5 的 `28.33912/4000` 研究进度、清理项目 ID 6 排队。仅在隔离部署副本新建无 BOM 的测试静态修正 `shishan_test_society_threshold = { country_society_research_produces_mult = 30 }`，并在玩家国家作用域暂时加入。这个系数只缩短等待，不改变项目所需研究点。夹具先经 `open_kaishek`；正式 64 文件及 Workshop 已发布内容保持原样。

通过正常时间推进，在项目未完成且累计点数小于 `4000` 时保存一个阈值前存档。再跨月推进，直到项目通过**正常社会学研究结算**完成并弹出简中事件，保存完成态。阈值前后须核对日期、社会学队列项目 ID 与累计点数、项目状态、`n`、局势、主物种奖励和最后完成项目键；必须明确区分“阈值前累计研究点”和“完成当月的社会学产出”，不能将科研库存或顶部净收入当作项目花费。若系数使首次月结算直接越过费用而无法留阈值前样本，降低系数并从无夹具锚点重新开始。

结束后移除临时修正并保存，退出夹具进程，删除唯一测试文件，将部署副本与仓库正式文件逐项哈希比较，再以正式单 Mod 重载终点、运行 `open_kaishek`。记录输入、存档 SHA-256、Steam F12、错误日志及任何原版事件干扰。若引擎在项目完成时不保留精确已消耗点数，本轮只能证明“费用阈值被跨越时完成”，不能宣称引擎内部恰扣 `4000.00000` 的不可见计数。

## 执行结果

**PR-01 `n=2` 维护项目的正常研究门槛子项通过。**简中 Stellaris 4.5.1、Steam 离线、单独启用正式 Mod；隔离部署副本暂加 `shishan_test_society_threshold = { country_society_research_produces_mult = 30 }`（无 BOM），夹具版 `open_kaishek PASS`（20/20 脚本、13 DDS、172 本地化键）。正式版 64 文件和已发布的 Workshop v0.1.0 未修改。起点是 `sv01-stage5-reloaded-2229.10.15.sav`：`n=2`、第五阶段、维护项目 ID 5 在社会学队列 `28.33912/4000`、清理项目 ID 6 排队。

最初 `35+270` 天和另一次 `250` 天整段推进均跨过项目完成点，无法充当门槛前样本；这些尝试没有被当作阈值证据。重新从相同哈希的起点逐段推进，得到：

| 状态 | 游戏日期 | 维护 ID 5 累计点数 | `n` | 局势进度 | 结果 |
| --- | --- | ---: | ---: | ---: | --- |
| [中间存档](../assets/shishan-code-origin/evidence/pr01-precheck-2230.01.15.sav) | 2230.01.15 | 2072.80528 / 4000 | 2 | 971 | 维护仍在研究；SHA-256 `342e9a2ea1c87e6a3f7fffdf50e1232d097df5320478c80f95bcfd2c89936af5` |
| [门槛前存档](../assets/shishan-code-origin/evidence/pr01-threshold-pre-2230.03.15.sav) | 2230.03.15 | 3435.78272 / 4000 | 2 | 985 | 维护仍在社会学队首、清理 ID 6 为零；未提前发奖；SHA-256 `4521cfeff11c1f8d2ff41e9324f37ebec36dd6ecebefe9f359871f2b6ad0b4d8` |
| [完成后存档](../assets/shishan-code-origin/evidence/pr01-threshold-post-2230.04.20.sav) | 2230.04.20 | 维护 ID 5 已出队，清理 ID 6 仍为零 | 3 | 0 | 正常科研完成；SHA-256 `d0da7914af8ab1155002115e092e5172748917ff957ca0ed3e2becd9d3b2ec5e` |

从 `3435.78272` 的存档推进 `35` 游戏日，未使用直接完成命令，出现[简中「维护完成」白绮弹窗](../assets/shishan-code-origin/evidence/pr01-threshold-maintain-completion-event-2230.04.20.jpg)。完成后 `last_completed_special_project=SHISHAN_CODE_MAINTAIN`，主物种只新增 `trait_robot_trading_algorithms`，仍有 `trait_shishan_code`；白绮工程学/社会学阶梯均由 2 层变为 3 层；局势唯一且进度归零。顶部社会学月收入随其他原版事件波动，不作为项目成本或已花费点数证据。引擎未在完成后的存档保留 ID 5 的精确消耗数；本轮只能证实低于 `4000` 时未完成，正常科研继续后完成，不能宣称内部恰扣 `4000.00000`。

随后用 `effect remove_modifier=shishan_test_society_threshold` 撤去加速，保存[干净终点](../assets/shishan-code-origin/evidence/pr01-threshold-clean-2230.04.20.sav)，SHA-256 `dea699a6e7519e3a129cf300d5b147a3d533e81a289d95638333929cdc0aa38a`；原生 `gamestate` 中测试修正名称由完成后 1 处变成 0 处。退出夹具进程并仅删除隔离部署副本的测试脚本后，部署目录与仓库正式 Mod **64/64 文件逐字节一致**；正式版 `open_kaishek PASS`（19/19 脚本、13 DDS、172 键，报告 `_runtime/shishan_code/accept_pr01_threshold_formal_20260929.json`）。

新正式单 Mod 进程校验和 `fe44`，重载干净终点后保存[正式重载存档](../assets/shishan-code-origin/evidence/pr01-threshold-formal-reloaded-2230.04.20.sav)，SHA-256 `f455c065e32a94489f581dc0c335be089d530565c281fbe92620143faabfe127`。日期、`n=3`、唯一局势及进度 `0`、旧屎山特质、新正面特质、白绮三层阶梯、旧清理 ID 6 的零进度均保持；测试修正字符串仍为零。[正式版情报日志](../assets/shishan-code-origin/evidence/pr01-threshold-formal-reload-ui-2230.04.20.jpg)显示第一阶段月进度 `+8`、下一次维护费用 `5000` 且预计 `194` 个月，符合 `2000+1000n`。夹具进程的日志仅有测试修正缺本地化与原版 caravaneer 事件作用域报错；正式重载日志仅列出未启用、未安装的旧 Workshop 路径，未见本 Mod 脚本错误。

本子项仅实测 `n=2` 维护的 `4000` 门槛；其他 `n` 及清理/持续优化每个费用门槛仍未逐点实测。PR-01 整行继续依总验收矩阵判断。
