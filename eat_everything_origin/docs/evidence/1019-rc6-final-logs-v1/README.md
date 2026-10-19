# RC6 最终日志原字节包

固定 run `20261019T150008Z`，PID `30812`，Mod `0.4.0-rc.6`，中文 `l_simp_chinese`，树 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`。原始 stop 时间为 `2026-10-19T16:38:02.658777+00:00`，`forced=false`、`running_after=false`。归档前及独立复核时，两次 OS 查询均确认该 PID 不存在。`process.json` 的 direct 启动命令与 manifest 一致；这是已有启动收据与停后进程查询的绑定，不是补造历史 OS 启动捕获。

`logs/` 完整复制固定 userdir 下全部 19 份最终日志，包含 5 份 `script_documentation`，共 **5,946,297 字节**；`run/` 仅复制 manifest/process/stop 三份元数据。总计 **22 个原始 payload、5,971,299 字节**，逐一与源文件比较原字节、长度和 SHA-256，并复核完整文件集合。包内 `* -text` 保留原始换行；未截取或过滤任何日志。RC6 static、migration checkpoint 及历史 nomads 审阅使用 8 个 canonical 引用；未复制 SAV、成长动作或 Mod 文件。

`review.json` 覆盖完整 error/game/system/debug 的 **283 行、265 条记录**。完整 `error.log` 的 24 条记录为：

| 原行号 | 数量 | 记录类别 | 保留状态 |
| --- | ---: | --- | --- |
| 1–21 | 21 | mod discovery 缺失文件 | 影响未知；未白名单 |
| 22 | 1 | `decision_lithoid_swarm_consume_world` 重定义，指向 `zz_eep_native_decision.txt:2` | 影响未知；路径明确不等于无害 |
| 23 | 1 | `portrait_container` 缺失，`interface/select_empire_design.gui` | 原因、归属和影响未解释 |
| 24 | 1 | EEP while 达到 100 次中止 | 真实 EEP 运行时错误；未解释 |

第 24 行时间戳 `[00:24:35]`，原文点名 `eep_mothership_effects.txt:35`、`eep_sync_mothership_components`（调用位于 `:195`）及 `eep_sync_mothership`。本包不从本地钟点推断触发的输入阶段、存档或根因。`debug.log` 另有 1 条建筑类别查询失败，其对象与影响未知。共 **25 条诊断全部保留未解释或影响未知**。

`game.log` 的 20 条记录保留版本/defines、同步、3 次世界生成及 13 次事件选择；`system.log` 的 238 行/220 条记录保留图形、显示模式与音频初始化；这些只是原始活动观察。四份已审日志没有 nomads 字符串，历史 RC4 的 2 条 nomads 诊断仍为 **UNEXPLAINED**，引用旧报告且未改动旧报告。零新记录不解除历史未知项。

`verify.json` 的独立复核 **13/13** 通过，范围仅为字节、来源、终止身份、选择完整性和分类完整性。static 工具原结果保持其有限的静态范围。这里没有用例 PASS、final-result 或 Mod 验收通过声明。

封口 SHA-256：

- `index.json`：`10df4d1aa1eb45ae1bd9554da46e7c298303a6d638f342ad33df18e5a61c9a2f`
- `review.json`：`b4875dd17e1a8b949e8fb99fcd670b6aec5770f3c3e891ff64b718ef75bd8756`
- `verify.json`：`367466eb7d650a16592dd7cf66b166363ae333a8b94b50598092c545ed2c16a3`
- `logs/error.log`：`b8a0cc17158bf05ebde64f42ed71ec17bd12687d5488fb8d6e7d462ceaf740f6`

`archive.py`、`review.py`、`verify.py` 是本包的证据制作与复核脚本，已有产物禁止覆盖。未操作 UI、Git、Steam、生产内容、current-run 或 RC7；未修改项目工具代码。主线程统一提交本包。
