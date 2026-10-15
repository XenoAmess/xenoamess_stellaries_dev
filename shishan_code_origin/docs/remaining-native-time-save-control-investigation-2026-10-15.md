# 原生快进与保存控制只读调查

日期：2026-10-15。目标为本机 Stellaris 4.5.2、正式 Mod 0.2.1 的后续受控存档矩阵。本协作者不操作GUI、不启动游戏，不在当前无世界的原版进程执行命令。

## 目标与范围

核对当前EXE中的 `fast_forward`、`save`、`savegame`、`ticks_per_turn` 候选命令及帮助/结果字符串，并检查仓库既有runtime助手和原生执行日志。目标是减少7×3原生存档矩阵的重复等待，不改变月度真实模拟或保存来源。

## 方案与验收标准

只读实际EXE的ASCII文本及本仓库已存在证据，记录固定EXE SHA256、文件偏移、原文和历史运行版本。字符串相邻不自动认定命令绑定，旧版本结果不自动迁移。优先提供无副作用的 `help <command>` 给主任务原生确认；未确认的参数、真实模拟语义、同步返回/暂停行为及保存命令可用性保留UNKNOWN，不写PASS。

快进必须与单纯改变日期或跳过tick分开；保存须证实由引擎新写原生sav，不能用读取已有文件、助手复制文件或历史Unknown command当成成功。任何实际时间推进和保存实验仅由主任务在加载隔离副本后执行，并比较日期、局势last_month_progress/进度、项目/人口和暂停状态。

## 调查记录

初次调查完成；本协作者没有执行任何原生命令。文末补充主任务随后执行的4.5.2原生help和64/30天推进回执，历史未确认状态不冒充最新结论。PF-01继续NOT RUN。

## 当前 EXE 直接证据

实际EXE为 `C:/Program Files (x86)/Steam/steamapps/common/Stellaris/stellaris.exe`，SHA256 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。只读ASCII结果保存于 `time-save-investigation/exe-command-strings.json` 和 `exe-behavior-text.json`；这些是字符串与上下文证据，不是反汇编或执行证明。

| 候选 | 当前二进制原文/偏移 | 当前可得结论 |
| --- | --- | --- |
| `fast_forward` | 37641864；附近 `<amount of days>` / `Fast forward a set amount of days`；37613032有`Fast Forwarded` | 可供help核对的明确命令候选；没有证实同步执行、完整tick、结束暂停或参数上限 |
| `ticks_per_turn` / `ticksperturn` | 37641768/37641752；`<amount of ticks>`、`Set amount of ticks per turn, default 1.`；有currently/set to两种结果提示 | 有查询/设值线索；无参查询仍待原生help确认，不能把参数当推进天数 |
| `game_paused` | 37642864；`<true/false>`、`Toggles/Sets the game paused state` | 明确暂停状态候选；不带值可能toggle，后续控制宜核对带布尔值语法 |
| `save` | 37702936邻近`mainmenu_window`、`resume`、`quit`、`resign` | 是菜单相关字符串，不能据此认定console命令存在；另外三个命中位于非此命令文本区，也不作为注册证明 |
| `savegame` / `save_game` | 完整ASCII标识本次未找到 | 仍不能从字符串缺失严格证明命令不存在；仅允许先help查询，不建议猜参数执行 |
| `add_time` | 37634736；帮助为`Advance time without ticking` | 与真正模拟不同，不能用于月结算、人口/项目推进或PF-01 |
| `debug_dumpgamestate` | 37635056；`Dump Gamestate data save as text file`、`<filename suffix>` | 原始文本dump线索，不能当作可重新加载的原生ZIP sav保存入口 |

`fast_forward`附近还出现`<observer>`，但字符串相邻无法证明它属于哪个参数、是否可选或是否切换观察者。主任务应以原生help为准，不凭位置补造第二参数。

## 历史执行与助手证据

4.5.1历史文档提供`fast_forward 30/35`的实际使用：普通项目曾通过真实科研流程在推进后完成，月结算资源分支也有原生sav。但 [RS04历史记录](../../docs/shishan-code-origin-rs04-mixed-species-2026-09-29.md)明确写过`fast_forward 5`在暂停时没有推动日期；另有35天命令后原生终点与字面天数不能简单等同的观察。这些事实支持优先复用该候选，却不能证明4.5.2同步/暂停合同。

[4.5.1原生发现记录](../../docs/shishan-code-origin-runtime-findings-2026-09-27.md)记录过完整输入的`save <name>`返回Unknown command，后续转用菜单保存。旧失败不得直接当4.5.2失败，也不能忽视它后又默认沿用旧命令。

现有 `shishan_code_origin/tools/runtime_feedback.py` 的 `native_save` 走中文菜单、填写明确文件名、等待新文件mtime、复制新ZIP并读取meta/gamestate；当前4.5.2此前多份native_save证据已使用该路径。这是有实际基础的保存路线，复制动作本身仍不能代替引擎新写证据。

另只读查看同仓库 `eat_everything_origin/tools/runtime_1015.py` 的 `wait_for_native_date`：按新GPU帧等待精确HUD日期，不从固定sleep推定完成；旧 `formal_production_native_calendar.py` 还联合要求目标日期、中文“暂停”、对应`Fast Forwarded N Days`回显后才保存。本协作者没有导入它们，因为导入runtime会配置桌面/DPI。所指另一个1015本机运行目录不存在，不能据助手源码冒称找到实际4.5.2快进回执。本次对屎山4.5.2/正式版运行目录的 `.console.json`索引没有找到快进/保存/暂停命令的对应记录，结果保留为0条，而非推断从未有其它方式执行。

## 给主任务的最小原生确认顺序

当前无世界进程只查询：

```text
help fast_forward
help game_paused
help ticks_per_turn
help save
help savegame
help save_game
```

命令名、参数和回显均保存新GPU图/OCR与原始输入回执。`help`若只是列出匹配项，要保留完整结果，不把部分可见列表当已证明缺少命令；不在无世界时执行快进、暂停设置或保存。

加载隔离副本后，优先做一次最小2日探针：保存原生起点、实际暂停状态和日期；根据help确认的语法执行候选 `fast_forward 2` **一次**。检查返回时是否仍在推进，等待完成回显和实际日期，再核对暂停状态。若暂停时不推进，保留该结果，在重新加载的独立分支测试 `game_paused false` 后快进，并在完成后按已证实语法显式暂停；不能把失败探针后又重复命令混成一次精确2日执行。布尔语法仅有当前EXE依据，必须先获得help/结果确认。

为证明“模拟”而非只改日期，下一探针跨一次月界：从同一原生起点分叉，分别正常UI推进与候选快进，对比实际日期、局势进度/last_month_progress、项目科研和真实人口/岗位；至少确认生产月结算确实发生。不能用`Fast Forwarded`字样单独证明所有模拟回调已运行，也不能用固定`time.sleep`证明结束。模态事件若中断推进，先记录现场和已到日期；OCR不清或等待超时不代表命令没执行，不重发推进命令。

`ticks_per_turn`改变每turn执行的tick批量，不等于“只推进N天”。正确性矩阵先保持原生默认/实际查询值，避免为加速同时改变第二个变量；任何后续调整必须有单独前后查询、真实终点和恢复记录，不能从较快画面推出月结算等价。

保存只有在当前help与实际新文件证据证明某个console入口存在时，才设计明确ASCII文件名的最小测试；无该证据继续使用已经验证的中文菜单 `native_save`，按实际新文件mtime、meta日期、ZIP内容、SHA256和重载结果取证。`debug_dumpgamestate`不满足此保存合同，不把`savegame`当作其它Paradox方言的可用命令。

初次调查交付准确的候选入口与不可混淆的语义边界；当时4.5.2的快进同步/自动暂停、完整月模拟和console原生sav保存能力均保持待实机确认，没有新增PASS。以下原生回执只更新实际观察到的分支。

保字节归档证据：[命令名与上下文](evidence/feedback-redesign/remaining-2026-10-15/programmatic/time-save/exe-command-strings.json)、[帮助/行为原文](evidence/feedback-redesign/remaining-2026-10-15/programmatic/time-save/exe-behavior-text.json)、[屎山当前console回执索引](evidence/feedback-redesign/remaining-2026-10-15/programmatic/time-save/recorded-console-index.json)和[历史文档/助手源码摘录与哈希](evidence/feedback-redesign/remaining-2026-10-15/programmatic/time-save/historical-source-evidence.json)。统一源路径/归档路径及字节身份见[独占清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/manifest.json)。没有修改balance负责的formal/vanilla证据子目录。

## 后续原生确认：4.5.2的帮助与一次64天推进

主任务随后在受控经济104文件lab运行 `20261015T112046Z` 加载真实世界，实际执行了以下help。本协作者只读停机后的输入回执、原F12/OCR和原生sav元数据，没有执行console或操作GUI。

| 查询 | 当前原生可见输出 | 已确认范围 |
| --- | --- | --- |
| `help fast_forward` | `fast_forward [<amount of days>] [<observer>]` | 第二参数在本构建帮助中真实存在；本轮只使用天数，observer语义仍未验证 |
| `help game_paused` | `game_paused [<true/false>]`，`Toggles/Sets the game paused state` | 布尔参数帮助已确认；未因此把未执行的设置/查询分支当已通过 |
| `help save` | 可见匹配 `check_save`、`save_detail_ai_build_plan` | 此次过滤结果未出现通用保存入口，不能由部分列表证明所有别名不存在；继续使用已验证的中文原生保存菜单 |

在实际暂停的2209.11.28，主任务只输入一次 `fast_forward 64`。初次命令返回图显示 `Fast Forwarding: 51/640 Ticks`，说明输入工具返回时原生推进仍在运行，不能把该返回当同步完成。后续新F12明确显示2210.02.02、暂停、`Fast Forwarded 64 Days`；30日历计算恰为64天，原生菜单新写sav的meta与gamestate也均为2210.02.02。这一当前构建案例证实可从暂停态启动推进并在该次终点回到暂停，不能沿用旧4.5.1“暂停时不推进”作为当前规则，也不外推所有事件/参数组合。

此后两次输入回执均为 `fast_forward 30`，新原生保存分别为2210.03.02和2210.04.02。首段warm等待的OCR把新完成回显识别成 `Fat   ays`，所以自动guard继续等待；主任务已目视其原F12实际为 `Fast Forwarded 30 Days`，没有重发快进。第二段新F12/OCR同时取得2210.04.02与 `Fast Forwarded 30 Days`。**OCR失败不是命令未执行的证据**，必须保留实际日期、原帧与完成状态，禁止据超时自动重放推进。

三份sav的ZIP原文已只读核验：版本均 `Cygnus v4.5.2`、meta与gamestate日期一致、字节数/SHA256与原生保存回执一致。只核对这些时间/来源字段，不由 `Fast Forwarded` 回显推出所有生产月回调正确；经济/局势合同仍依赖对应存档和UI独立审计。该运行虽有原生Day TSV，也不是PF-01配对矩阵；后续116文件稳定经济运行 `20261015T113522Z` 未带此计时参数，不将混合加载/分支日志当性能对照。

必要原件与图像均保持原字节，位于同一独占归档：

- [fast_forward输入与帮助](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104-native-help-fast_forward.console.json)、[帮助原图](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104-native-help-fast_forward-result.jpg)。
- [暂停帮助原图](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104-native-help-game_paused-result.jpg)、[save过滤结果](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104-native-help-save-result.jpg)。
- [64天输入](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104-mature-fast-forward-64.console.json)、[异步推进中原图](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104-mature-fast-forward-64-result.jpg)、[64天完成原图](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104-mature-after64.jpg)。
- [warm30天输入](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104_F01_warm-advance.console.json)、[OCR误读对应原帧](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104_F01_warm-wait-7.jpg)、[下一30天完成原帧](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/econ104_F01_measured-wait-1.jpg)。
- [独立格式/时间核对](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/day-schema-observation.json)、[26份原件归档清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/archive-manifest.json)。清单保留原源路径、目标、字节数和SHA256，图像逐份与原OCR身份字段一致。
