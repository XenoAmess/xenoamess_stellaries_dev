# 屎山代码起源：第二次隔离实机发现

Stellaris 4.5.1，简体中文，仅启用本 Mod；证据截图位于 `_runtime/shishan_code/20260926T111756Z`。

## 已核实

- 开局“维护屎山”项目显示花费 2000 社会学，“清理屎山”显示 8000 社会学。完成一次维护后分别变为 3000 和 10000；后者在同一项目条目上实时更新。
- 第一次维护后局势月速由 1.0 增至 2.0；进入第三阶段后显示 -25% 的资源生产修正。白绮已通过三段开局事件加入，肖像显示正常，解雇按钮呈灰色。

## 项目重复与控制台测试限制

反复使用控制台 `finish_special_projects` 后出现两组“维护屎山”“清理屎山”。该命令会结算所有可用项目，因而不能从这个结果单独断定正常完成一个维护项目也会复制项目。原版 4.5.1 脚本用 `has_special_project` 检查已有项目；为避免重复启用，现于每次启用前检查 `NOT = { has_special_project = ... }`，并取消为了更新动态费用而终止及重新启用清理项目。清理项目的费用已验证会在原项目上实时更新。

旧隔离局已受全项目结算命令影响，不能用来证明修正有效；须新建隔离局，只启动目标项目并验证维护后每种项目仍仅有一项，再验收清理与持续优化。

第三次隔离局 `_runtime/shishan_code/20260926T174803Z` 采用本 Mod 最新副本。控制台 `finish_special_projects` 在当前 4.5.1 中显示 Unknown command，不能作为验收命令。原版联邦特殊项目脚本实际使用国家效果 `complete_special_project = { type = <项目键> }`；以 `effect complete_special_project = { type = SHISHAN_CODE_MAINTAIN }` 在仅启动维护项目的状态执行，控制台确认完成“维护屎山”，局势月速由 +1.0 变 +2.0，并出现维护完成事件。此前先用 `effect abort_special_project = { type = SHISHAN_CODE_CLEAN }` 排除清理项目，控制台确认终止。后续用按项目键精确结算的命令验收。

## 2026-09-27：用户修订后的资源与 UI 回归

- 局势基础月速由 `+1` 改成 `+5`。全新隔离局 `_runtime/shishan_code/20260927T163000Z/progress5.png` 的简体中文局势列表实测显示 `+5.0`；前文 `+1.0/+2.0` 属于旧版本证据，不可用于当前数值验收。维护后当前版本应为 `+6.0`，仍待实机复核。
- A05 事件图改用 V2 概念图重新生成，源图 `assets/shishan-code-origin/generated/A05-attempt-02/original.png`；同局事件截图 `day8_event.png` 中五官完整，未见旧图的面部开裂。旧 A05 只留作历史记录。
- 白绮领袖肖像旧实现把完整半身图交给 `synthqueen_portrait_entity` 的分片网格，造成用户截图里的头身错乱。V2 图经 EvoLink 生成和 Layerize 提取后改用静态 `texturefile`。第一次 1024×1024 DDS 实机只显示胸甲；改为上半身 512×384 DDS 后，新隔离局 `_runtime/shishan_code/20260927T180000Z/vivhite_reloaded_leader.png` 在重载存档后的领袖列表和详情卡同时显示完整头、双侧发饰与肩部，且没有分离肢体。可共享截图复制至 `assets/shishan-code-origin/evidence/vivhite-leader-v2-stellaris-4.5.1.png`。
- 本次运行的 `error.log` 未出现 `shishan`、`vivhite` 或肖像相关错误；该日志检查不代替项目、经济或复活玩法验收。

## 2026-09-27：白绮死亡与首版复活失败

- 在 V2 肖像隔离局通过 `effect owner = { every_owned_leader = { limit = { has_leader_flag = shishan_code_vivhite } kill_leader = { show_notification = no } } }` 实测白绮意外死亡路径；领袖数从 5 变为 4，备份提示弹出，首都出现「重启白绮」。控制台当前选中白绮时作用域是 `leader`，直接执行 `every_owned_leader` 报作用域错误；测试须通过 `owner` 切回国家。
- 支付选项将能量币从 891 扣至 391、决议消失，但领袖仍为 4 人。`error.log` 报 `Target leader not valid` 和未定义备份 event target；故 WH-03 标记 FAIL，不能把出现提示当作复活验收。接下来按实施记录的原版直接克隆与放逐方式修复并重测。
- 第二次隔离局 `20260927T210000Z` 用直接克隆和放逐再次复测仍失败：支付扣除 500 能量币，领袖数仍为 4，日志仍报备份目标无效。根因进一步定位为克隆发生在已执行死亡的 `on_leader_death`；后续改挂原版明确的死亡前回调，并阻止无备份时扣费。
## 2026-09-27：复活备份跨事件作用域

第三次隔离局 `20260927T220000Z` 改用死亡前回调后，白绮死亡事件顺利创建备份并显示重启决议，但重启事件的付费选项因 `exists = event_target:shishan_code_vivhite_backup@root` 为假而隐藏。死亡后存档 `vivhite_postdeath_broken.sav` 的 `saved_leaders` 含 `shishan_code_vivhite_backup0=16777360`，该领袖记录仍为 5 级、传奇行政官、保留特质和肖像；说明备份本体已保存，失效的是局部 event target 跨决议事件的引用。原版 4.5.1 另有 `save_global_event_target_as`，用于跨事件引用；下一版改为带国家后缀的全局目标，并在死亡、付费、重载后确认领袖实际归队。只出现备份提示或决议不能判作复活通过。
## 2026-09-27：白绮付费复活与重载通过

第四次隔离局 `20260927T230000Z` 使用带国家后缀的 `save_global_event_target_as`。死亡后领袖名单由 5 人变 4 人，备份事件与首都「重启白绮」决议均出现；决议事件同时显示付费与保留备份选项。选择付费后能量币由 952 降至 452，合金扣除 200，领袖名单恢复为 5 人，白绮仍为 5 级传奇行政官，肖像及特质图标正常。保存 `vivhite_revived_probe.sav` 并从游戏内重新载入后，领袖名单、等级、肖像仍正确。运行日志未出现与本 Mod、备份目标或 `clone_leader` 有关的错误。证据截图存于 `_runtime/shishan_code/20260927T230000Z/reboot_options.png`、`revived_detail.png` 和 `revived_reloaded_leader.png`。这只覆盖一次死亡与复活；连续第二次死亡、原有经验精确值与其他起源玩法仍待验收。
## 2026-09-27：第二次复活发现经验清零

同一隔离局在首次复活并重载后，为白绮增加 200 经验及原版「善于适应」领袖特质，再次死亡并支付 500 能量币、200 合金。第二次复活后白绮仍为 5 级，新增特质仍在；但存档 `vivhite_second_revive_xp_trait12.03.sav` 中死亡前领袖 `experience=212`，死亡备份和复活后新领袖均无 `experience` 字段，表明 `clone_leader` 在本游戏版本复制等级与特质但不复制当前等级内经验。原版 `events/000_how_to_use_variables_in_script.txt` 允许通过 `trigger:has_experience` 将领袖当前经验写入数值变量，再以变量调用 `add_experience`。后续实现应在死亡前把经验存于国家变量，在付费复活成功后补到新领袖，并清除变量；验收必须比较修复前后存档中的经验数值。

第五次隔离局 `20260927T233000Z` 证明直接把旧经验值传给 `add_experience` 不够：死亡前领袖当前等级经验为 `252`，复活后的存档为 `317.52`，恰好乘上当前 `1.26` 经验获取倍率。修正方案是在新领袖上先授予 1 点基础经验，读取实际获得值作为当下倍率，再把目标经验除以该倍率，扣除已经授予的 1 点基础经验，补授剩余基础经验；仅当旧经验大于零时执行，并在倍率为零时避免除零。验收须比较存档中的旧领袖与新领袖经验值，允许存档浮点精度范围内的误差。

同局热更新 Mod 副本并重新启动游戏、载入修正前存档后，第三次意外死亡前白绮存档经验为 `317.52`。经原有死亡前回调生成备份，触发重启事件并支付 500 能量币及 200 合金；`vivhite_xp_factor_fixed.sav` 中新领袖经验也为 `317.52`，5 级、`leader_trait_adaptable` 与传奇特质均保留，临时经验变量已清除。截图为 `_runtime/shishan_code/20260927T233000Z/revived_factor.png`，运行日志无本 Mod 相关错误。该用例通过非零经验和 `1.26` 倍获取修正检验了经验修复；零经验倍率的边缘情况尚未验证。

局势阶段边界回归将在本隔离局使用控制台 `set_situation_progress` 设置指定值，再截图局势提示并核对实际阶段。游戏控制台执行后会保留旧输入文本，直接自动输入新命令可能插入到旧命令中；测试夹具须先点击输入框末尾、用扫描码退格清空，再输入并执行短命令。先前出现的 `49/1000` 是误输，不能作为 `249` 边界证据。

## 2026-09-27：五阶段自然推进回归

同一隔离局先用正确执行的控制台命令把局势设到 `249/1000`，截图 `_runtime/shishan_code/20260927T233000Z/stage249_verified.png` 显示第一阶段和 `+25%` 修正。随后让游戏按当前基础速度 `+5.0/月` 自然推进：`319/1000` 时为第二阶段、无阶段效果（`stage_month_boundary.png`）；`524/1000` 时为第三阶段、资源与武器等 `-25%`、岗位维护费 `+25%`（`stage3_live.png`）；`814/1000` 时为第四阶段、对应 `-50%/+50%`（`stage4_live.png`）；`974/1000` 时为第五阶段、对应 `-75%/+75%`（`stage5_wait8.png`）。这验证了四次阶段切换和修正方向、幅度，但不是精确边界 `250/500/750/950` 的逐点测试。继续正常推进至 2220.07 后局势停在 `1000/1000`（`stage5_at1000.png`）；到 2225.09 仍为同一局势和第五阶段 `-75%/+75%`（`stage5_longterm.png`），证明末段长期驻留。

控制台连续设置 `250` 时曾多次只显示“Executing effect script.”却未更新进度。复核发现自动化夹具的 `pyautogui.press("enter")` 没有把输入提交给游戏；改用 Windows 扫描码 `0x1C` 发送回车后，按项目键执行 `effect complete_special_project = { type = SHISHAN_CODE_MAINTAIN }` 已成功结算。原来的设置命令均不作为边界证据；须使用修正后的夹具重新逐点验收。

## 2026-09-27：第五阶段维护项目实机结算

在第五阶段 `1000/1000` 启动显示花费 `2000` 社会学的“维护屎山”，再以精确项目键完成。完成事件弹出后，局势回到第一阶段 `0/1000`，月进度由 `+5.0` 变为 `+6.0`，`+25%` 第一阶段修正恢复；截图 `_runtime/shishan_code/20260927T233000Z/maintain_stage5_success_console.png` 和 `maintain_stage5_reset.png`。需继续核对下一轮维护、清理的动态成本与物种奖励，并在随后验证清理、优化及复发分支。

该事件画面随后停止刷新：移动鼠标、点击事件选项、扫描码回车/退出以及空格均未使连续截图产生任何像素差异，尽管进程尚在消耗 CPU 且 Windows `WM_NULL` 探测有响应。当前会话不能继续作为互动验收依据；保留事件与局势截图后，从 `autosave_2226.07.01.sav` 在隔离 userdir 中恢复并复测，若再次发生则作为 Mod 运行时故障排查。

恢复尝试的补充观察：强制结束旧进程后 Windows 显示 Paradox Crash Reporter；新启动的游戏进程于 `16:38:06` 完成图形设备创建，但至 `16:44` 窗口仍为黑色，CPU 基本空闲且未出现主菜单。关闭旧崩溃报告、最小化恢复窗口及调整尺寸都未使游戏绘制。崩溃报告也可能由强制结束产生，目前不能据此把先前的画面停止归因于 Mod。先继续静态审计，再以全新隔离 userdir 排除旧会话状态。

全新隔离 userdir `20260927T084700Z` 复制同一生产 Mod 后再次启动，`system.log` 同样在 `Done creating device` 停止，进程随后几乎无 CPU 活动，主菜单未出现；复制了最近自动存档供恢复使用，但尚未载入。故“旧 userdir 状态”假设未获支持。当前实机验收暂停在游戏启动环境诊断，不能把后续项目场景标记通过。

又用无 Mod 的全新隔离 userdir `20260927T085100Z_vanilla` 作对照，`dlc_load.json` 的 `enabled_mods=[]`。该原版进程也完成相似的启动 CPU 峰值后停留在桌面/空白游戏窗口，没有主菜单。由此可排除“只有本 Mod 导致新进程无法进入主菜单”的判断；主机图形/启动环境需恢复后才可继续 UI 验收。

后续诊断计划：复制一份隔离配置，仅在该副本中把显示模式改为窗口化、分辨率降至 `1280×720`，再试无 Mod 原版启动。若原版可启动，才用同显示配置启动本 Mod 并恢复自动存档；不修改玩家真实配置。当前静态门禁复跑结果：`open_kaishek` `PASS`（18 个脚本解析、13 个 DDS、122 个本地化键），八种非简中翻译审计均为 0 个英文原文残留与 0 个汉字占位。

窗口化无 Mod 对照 `20260927T091000Z_vanilla_window` 也于 `Done creating device` 后保持纯白窗口，超过 2 分钟没有主菜单。边框和桌面正常渲染，而游戏客户区不渲染，因此下一步尝试 Windows 图形驱动重置快捷键，再启动同一无 Mod 对照；若仍失败则不把环境障碍误记为 Mod 功能失败。

Windows 图形驱动重置快捷键执行后，原版窗口仍为纯白。后续只在另一份隔离配置中试另一种游戏渲染器设置；如原版仍无法显示，UI 验收环境确为阻塞项，应继续完成可独立执行的静态审计并保留未测场景清单。

另一份无 Mod 窗口化配置 `20260927T091200Z_vanilla_renderer0` 把渲染器设为 `0` 后也保持纯白窗口。三组无 Mod/有 Mod 对照共同指向当前桌面游戏渲染环境问题，不能通过反复改动 Mod 脚本来解决。

静态奖励池审计发现具体实现风险：第二层目前直接 `add_trait` 的 19 个原版非机械正面特质，在 4.5.1 的 `common/traits/04_species_traits.txt` 中均声明 `allowed_archetypes = { BIOLOGICAL LITHOID }`。即使其 `modifier` 数值对机器也有意义，不能未经验证就认定机械物种实际获得这些原版键。依据设计中允许的机械兼容映射方案，改由同名、同图标、同数值且 `MACHINE ROBOT` 可用的脚本专用特质发奖，并把动态奖励池测试保留为运行时必测。

映射实施后的包级检查最初因 19 个本体 DDS 路径误报失败。已在 `open_kaishek` 提交并推送 `63997f2`：资源路径优先查 Mod，再查锁定的游戏安装目录；工具 4 项单测及全仓库静态验收通过。目标 Mod 重新执行后 `PASS`，19/19 脚本解析、13 个 Mod DDS、160 个本地化键；八种非中英文翻译语义候选审计仍为 0 英文原文残留、0 汉字占位。实机环境仍不能进入主菜单，这些静态结果不构成运行时通过。

`tools/shishan_code/audit_compat_traits.py` 与 4.5.1 本体逐项比对 19 个映射的数值修正、机械物种许可，并遍历十种官方语言检查原版名称及描述键；结果 `PASS (19 vanilla effects and machine archetypes)`。这证明静态数据映射一致，仍需进游戏证明脚本发奖和人口实际增益。

桌面启动诊断还需排除 `-debug_mode` 影响：在新的无 Mod、窗口化隔离配置中不传调试开关做最后一轮对照。若仍纯白，则当前可控的软件参数已不能恢复原版 UI；保留此环境阻塞，不继续反复启动同一配置。

无调试开关的无 Mod 窗口化对照 `20260927T093000Z_vanilla_nodebug` 也在启动 CPU 峰值后停于纯白客户区，无主菜单。证据为 `_runtime/shishan_code/20260927T084700Z/vanilla_nodebug.png`。因此后续简中运行时 UI 回归因主机游戏渲染环境受阻；即使本 Mod 静态包级与先前部分实机场景通过，也不能宣称整体验收完成。

补充主机诊断：`Get-CimInstance Win32_VideoController` 报 NVIDIA GeForce RTX 4060 驱动 `32.0.15.8180`，状态 `OK`；`Get-Service EventLog` 却显示 Windows Event Log 服务为 `Stopped`、启动类型 `Automatic`。`Get-WinEvent` 和 `wevtutil` 均因 RPC 服务不可用而不能读取系统事件。尝试正常启动该服务时短暂进入 `START_PENDING`，随后回到 `STOPPED`，`sc queryex EventLog` 报 Win32 退出码 `4201`。这说明主机诊断基础设施也异常，但目前没有证据能证明 Event Log 服务故障就是 Stellaris 白屏的原因。

按用户要求又用全新隔离目录 `retry_vanilla_20260927_174022` 启动无 Mod 原版，进程 `17412`：`system.log` 再次停止于 `Done creating device`，切至游戏窗口后截图 `_runtime/shishan_code/vanilla_retry_taskbar_174022.png` 为纯黑客户区，没有主菜单。用户随后明确授权重启主机。重启前关闭本次原版进程并保存该日志与截图；重启后先检查原版主菜单，再运行本 Mod，不能把重启前的阻断直接视为已解除。

重启后 `EventLog` 服务已恢复 `Running`，但无 Mod 原版在全新隔离目录 `postreboot_vanilla_20260927_174842` 仍停在 `Done creating device` 后，进程内存增长至约 2.8 GB 后 CPU 基本空闲，主菜单未出现。系统显示从重启前 `2560×1440` 变为 `1024×768`；再以明确写入的 `windowed`、`1024×768`、简体中文配置启动第二个无 Mod 对照 `postreboot_vanilla_1024_20260927_175205`，游戏窗口仍是纯白客户区，截图 `_runtime/shishan_code/postreboot_vanilla_1024_window.png`，日志同样停止在创建图形设备后。两次进程均已正常发送窗口关闭消息退出。Windows 应用事件日志没有记录本轮 Stellaris 崩溃，内存仍有约 22 GB 可用。重启修复了 Event Log 服务，却未恢复当前自动化启动路径的游戏画面；现在等待用户从 Steam 启动原版做独立对照。

日志口径修正：较早已成功进入游戏的隔离会话 `20260927T230000Z`，其 `system.log` 末行也是 `Done creating device`。因此“日志最后写到创建图形设备”**不能单独定位白屏发生在哪个初始化步骤**；白屏结论依赖无 Mod 对照窗口的实际截图、持续不出现主菜单、进程进入低 CPU 状态等观察。当前无 Mod 对照的 `error.log` 仅含缺失的旧 Workshop 项目路径，未记录本 Mod 的加载错误。

重启后又用先前成功实机相同的 `tools/shishan_code/launch_probe.py`、简中、`-debug_mode` 和全新隔离目录 `postreboot_mod_20260927_180200` 启动当前提交的 Mod 副本。游戏内存增长约 2 GB，但游戏窗口未绘制主菜单或局势画面，仍不能执行互动验收；进程已正常关闭。与重启后两组无 Mod 对照一致，不能仅凭这个结果归因于本 Mod。主机当前处于 `1024×768` 显示会话，用户已被请从 Steam 入口手动启动原版作独立对照。

Steam 独立对照已由开发侧执行：`steam.exe -applaunch 281990` 正常打开 Paradox Launcher，播放集显示“无 Mod”；点击“开始游戏”后原版 `stellaris.exe` 进程内存增长至约 2.85 GB、CPU 随后闲置，但游戏窗口依然未绘制主菜单。进程已正常关闭。这个对照排除了“只有隔离 `-userdir` 启动路径白屏”的判断。按 [Steam 官方本地文件验证说明](https://help.steampowered.com/en/faqs/view/0C48-FCBD-DA71-93EB//) 在客户端启动 Stellaris 安装文件验证；Steam 处于离线模式，UI 长时间停在 `0%`，`content_log.txt` 仅记录 `Start validating appID 281990` 和 `Update Queued`，未完成文件检查。下载队列中的该项现已手动暂停在 `0%`，避免离线状态意外变化后自动执行；已向用户询问是否允许 Steam 上线继续验证。

将 Windows 显示模式恢复为先前成功实机使用的 `2560×1440@60Hz` 后，又启动全新、无 Mod 的 `vanilla_2560_after_reboot` 对照。`time.log` 记录启动初始化用时约 `85.9` 秒并结束，游戏窗口占满屏幕、在系统中为前台且可响应窗口消息，进程工作集约 `2.7 GB`；但窗口没有绘制主菜单，屏幕截取仍可见窗口下面的 Steam 页面，证据 `_runtime/shishan_code/vanilla_2560_after_reboot_focused.png`。关闭该进程后，Windows 系统/应用事件日志没有对应的显示驱动重置或游戏崩溃记录。由此排除“仅重启后分辨率变成 1024×768”导致白屏，但不能判定渲染故障的根因。

同日静态资源审计：原版 `common/strategic_resources/00_strategic_resources.txt` 的四种可持续产出稀有资源（活体金属、暗物质、纳米机器、文物）此前漏于本 Mod 的阶段修正；`logs/script_documentation/modifiers.log` 确认四个 `country_*_produces_mult` 修正键由引擎生成。先更新设计与 RS 验收清单，再在 I/III/IV/V 四阶段补齐数值。四个原版英文显示词条缺失，因此新增十种语言的显示键；九种外语由 MiniMax 候选生成，其中日语初稿出现简中字形“产出”，经 MiniMax 二次生成改为“生産量”。候选 JSON 保存在本机 `_runtime/shishan_code/resource_modifier_minimax*.json`；资源名占位保持原版 `$资源键$`。本次 `open_kaishek` 包级复检 `PASS`（19/19 脚本、13 DDS、164 本地化键），翻译审计八种非中英语言的英文残留与汉字占位均为零。四种资源的实际产出范围仍待游戏恢复后按 RS-02 实测。

来源类别再核对：4.5.1 `economic_categories/00_common_categories.txt` 中 `planets`、`stations`、`megastructures` 和 `country_base` 是 `country` 后代；岗位、采集站、研究站分别通过 `planets` 或 `stations` 继承。`monthly_trades`、`subject_tax` 与 `trade_policy` 没有 `country` 父类；`defines/00_defines.txt` 把每月市场交易、附庸税指向前两者。这支持当前单键方案的来源隔离预期，但不等于引擎运行时已验证，尤其不能证明贸易协定是否完全排除。

## 2026-09-27：重启后图形环境排查续篇

目标是让无 Mod 原版重新绘制主菜单，以便继续简中实机验收。范围仅限本机图形环境和全新隔离游戏配置；不调整 Mod 玩法脚本。先分别关闭 Steam 的 Stellaris 游戏叠加界面与 NVIDIA 信息浮窗，用无 Mod 隔离配置启动；若仍空白，则恢复原设置。随后暂时移走 Steam 的 Stellaris 着色器缓存，用新的无 Mod 配置启动并观察主菜单、进程、日志；测试结束将原缓存原位恢复。若上述均失败，再测试 Stellaris 程序的 Windows“禁用全屏优化”兼容性标志，并在测试后恢复原注册表值。每轮验收标准为无 Mod 主菜单实际可见、至少能截取菜单画面；仅出现进程、窗口或启动计时结束均不算通过。所有配置恢复情况和剩余阻塞应记入本节。

Steam Stellaris 专属叠加界面关闭后，原版仍未显示菜单。再关闭 NVIDIA 信息浮窗并用全新无 Mod 目录 `vanilla_no_overlays` 启动，`time.log` 报约 88 秒启动结束、进程增长至约 2.7 GB，窗口仍未绘制菜单；截图 `_runtime/shishan_code/vanilla_no_overlays.png`。NVIDIA 叠加进程在关闭设置后消失，但游戏进程仍加载 `nvspcap64.dll` 与 `gameoverlayrenderer64.dll`，因此这只能排除“关闭两个 UI 开关即可恢复”的简单情况。测试后 NVIDIA 信息浮窗和 Steam 游戏叠加界面均已恢复为开启，游戏进程已关闭。

Steam 的 `steamapps/shadercache/281990` 原缓存先移动至同级备份，原版 `vanilla_fresh_steam_shadercache` 启动后生成了新缓存，仍未显示主菜单。新缓存移动到独立同级目录，原缓存已恢复到原路径，未删除任何旧缓存。NVIDIA `DXCache` 因访问被拒绝而未移动或改动。Windows 应用与系统事件日志在这些启动期间没有图形驱动复位或游戏崩溃记录。图形窗口前后顺序、焦点和命中测试证实 Stellaris 窗口存在并能成为前台，但屏幕截取显示下方 Steam 页面，`PrintWindow` 只得黑色；这表明“可见窗口”不能替代渲染验收。

Windows 针对 `stellaris.exe` 的 `~ DISABLEDXMAXIMIZEDWINDOWEDMODE` 兼容标志也做了单次无 Mod 测试：全新隔离目录 `vanilla_fullscreen_opt_off` 在 `2560×1440`、DX11 下启动约 87 秒，仍未绘制主菜单，截图 `_runtime/shishan_code/vanilla_fullscreen_opt_off.png`。测试后原版进程正常关闭，该兼容标志已从当前用户注册表移除；原有 OneDrive 标志未动。

DirectX 诊断文件 `_runtime/shishan_code/dxdiag_20260927.txt` 报当前系统为 Windows 10 19045、NVIDIA RTX 4060、驱动 `32.0.15.8180`、DirectX 12 和 D3D 11_0 及以上特性级别；同时报该显示驱动文件未经 WHQL 签名、设备虚拟化类型为 `Paravirtualization`。这两项是图形环境的诊断线索，**目前没有证明它们导致 Stellaris 白屏**；系统事件日志也未记录对应的驱动复位。下一项可逆对照是在正常退出 Steam 后直接启动一份新的无 Mod 配置，确认 Steam 进程与注入层是否影响窗口绘制，然后恢复 Steam 离线会话。成功标准仍是实际绘制主菜单。

该无 Steam 进程对照 `vanilla_no_steam_process` 已执行：Steam 使用自身退出命令正常停止，游戏直接运行时未自动拉起 Steam；`time.log` 记录约 81.5 秒启动完成，但主菜单仍不可见，截图 `_runtime/shishan_code/vanilla_no_steam_process.png` 可见下方桌面应用。游戏已正常关闭，Steam 已重新打开且 UI 确认为离线模式。由此排除“Steam 进程正在运行”是这轮白屏的必要条件，不能排除安装文件或其他图形钩子问题。

在等待用户对 Steam 上线完成官方文件验证的答复期间，补做一项**只读、离线、有限范围**的安装完整性调查：读取 Steam 本地 `appmanifest_281990.acf` 指向的已安装 depot manifest，按 [SteamTracking 的 manifest protobuf 定义](https://github.com/SteamTracking/Protobufs/blob/master/steam/content_manifest.proto) 提取至少 `stellaris.exe` 及关键启动资源文件的 SHA-1，与本地文件比对。若本地 manifest 的路径加密、缺失或内容不匹配，则如实记录；即使比对通过，也不能替代 Steam 完整文件验证或证明运行时能绘制菜单。调查脚本和结果保存在被忽略的 `_runtime` 目录，不改 Steam 文件。

离线抽查成功解析当前 `appmanifest_281990.acf` 引用的基础游戏 depot `281991_4474190844677920248`（43905 项）和可执行文件 depot `281992_4855157871014382851`（19 项），文件名未加密。`stellaris.exe`、`PDXSDK.dll`、`steam_api64.dll`、`nakama-sdk.dll` 和 `checksum_manifest.txt` 五个关键文件 SHA-1 均与本地清单一致，结果 `_runtime/shishan_code/offline_manifest_check_result.json`。为排查资源文件局部损坏，进一步对这两个基础 depot 的**全部普通文件**执行只读 SHA-1 比对；跳过目录，严格限制清单路径在 Stellaris 安装目录内，记录匹配、缺失与不匹配的数量和样例。该离线比对仍只证明本地文件与本地缓存清单一致，不等于 Steam 向服务器核验，也不能证明图形驱动正常。

全量离线复核在处理 Steam manifest 的零字节占位文件后完成：基础资源 depot 的 `42795/42795` 普通文件、可执行文件 depot 的 `16/16` 普通文件全部匹配，缺失 `0`、内容不一致 `0`，合计读取约 29.98 GB；原始结果 `_runtime/shishan_code/offline_full_depot_check_result.json`。首次脚本把 6 个清单 SHA 字段为全零的零字节占位文件误报为不匹配；这些本地文件也确实是零字节，修正规则后重跑得到全通过。本地安装损坏不再是目前有证据支持的白屏解释；Steam 仍离线，官方验证仍未执行，但不必为了排除这项而立即上线。

接着在全新无 Mod 隔离配置中测试游戏的真正独占全屏模式（`fullScreen=yes`、`borderless=no`、`2560×1440@60Hz`、DX11），并在进程运行时检查窗口的可见性、扩展样式及 DWM cloaked 属性。目的在于区分边框无全屏合成异常与窗口自身被隐藏；验收依旧要求实际主菜单画面可见，测试后恢复原桌面显示模式并正常关闭游戏。

独占全屏 `vanilla_exclusive_fullscreen` 的启动计时约 94 秒，仍未绘制主菜单；截图 `_runtime/shishan_code/vanilla_exclusive_fullscreen.png` 只见下方 Steam 页面。游戏窗口报告 `visible=1`、`DWM cloaked=0`、矩形为 `2560×1440`，没有窗口被系统隐藏的迹象；但全屏启动把桌面显示模式切到了 `1024×768`，与配置中的 `2560×1440` 不符。游戏正常关闭后，已用显示模式枚举结果将桌面恢复为 `2560×1440@60Hz`。不能据此断言驱动是根因，但独占全屏并未恢复可见游戏画面。

当前无 Mod 对照在原分辨率、窗口化、无边框全屏、独占全屏、DX11 与替代渲染器配置、无 Steam 进程、覆盖层关闭、着色器缓存重建、禁用全屏优化以及重启 Windows 后均无法显示主菜单；42,811 个基础文件与本地 depot 清单全部匹配。后续若要重置显示适配器或安装官方驱动，可能中断桌面会话；已将选项和风险提交用户选择，未在答复前执行。

只读驱动清单补充：`pnputil /enum-drivers` 把当前 NVIDIA 显示驱动列为 `oem13.inf / nvmsoi.inf`，版本 `32.0.15.8180`，签名者为 `NVCleanstall Driver Modding Authority`；这解释了 DXDiag 报非 WHQL 签名，却不能证明白屏的成因。机器还有 Oray 虚拟显示驱动包，但当前 `Get-PnpDevice -Class Display` 只列出已启动的 RTX 4060。考虑到这台机器使用虚拟化 GPU 和远程桌面，替换显示驱动比单次适配器重启更可能使桌面不可用，因此必须按用户答复执行。

同时只读复核了起源条件：本 Mod 的 `species_archetype = { value = MACHINE }` 与原版 4.5.1 `origin_post_apocalyptic_machines` 的机械主体物种条件一致；原版其他起源的 `swap_type` 明确把 `is_individual_machine` 与 `is_machine_empire` 放在同一机械使用路径。这个静态对照支持起源入口允许两类机械帝国的设计，但尚不能替代个体机械帝国建国界面的实机点击验收。
