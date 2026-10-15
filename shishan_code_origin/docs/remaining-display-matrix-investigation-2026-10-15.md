# UI-04 显示矩阵只读调查

日期：2026-10-15。目标包为正式 `0.2.1`，90 个生产文件；不含展示探针或运行时夹具。

## 目标与范围

依据原测试方案第 5.3 节、G0 和 UI-04，调查游戏原生分辨率与 UI 缩放边界，为主任务冻结显示矩阵提供资料。范围包括本机 Windows 只读显示模式枚举、原版设置布局与 GUI 定义、既有用户配置和运行适配器的实际行为。只向本篇独占文档和 `_runtime` 调查 JSON 写入证据，不操作桌面、不修改显示模式或设置、不启动游戏，不修改生产包或运行工具。

## 方案与验收标准

1. 读取并记录设置文件、GUI 定义和适配器的路径、哈希与相关原文，区分声明的默认值、候选模式、历史配置和实际生效值。
2. 只调用 Windows `EnumDisplaySettings` 等查询 API；不调用 `ChangeDisplaySettings`，不更改 DPI awareness、屏幕、窗口或注册表。保存当前模式和所有枚举模式。系统枚举不能代替游戏原生可选性证明。
3. 提出最低合法分辨率、1920×1080、2560×1440及各自最小/默认/最大合法 UI 缩放的候选矩阵；未由原生设置或实际行为证明的边界明确标为 UNKNOWN/待实机确认。
4. 明确主任务仍需使用正式生产包、简中、同一暂停存档及真实重启重载确认的项目。静态调查完成不等于 UI-04 PASS；不支持或环境阻塞应保留设置证据，不能自动省略。

## 调查记录

只读调查已完成；UI-04 实际显示矩阵仍为 `NOT RUN`。原方案要求完整机制名、系数、状态和按钮可读可操作；列表原生截断可单独记录，但必须有正常操作可达的全文。Windows 显示缩放与游戏 UI 缩放分别记录。

证据为 [只读调查 JSON](evidence/feedback-redesign/remaining-2026-10-15/programmatic/display/display-matrix-readonly-20261015.json)，最初生成于 `_runtime/shishan_code/20261015-runtime/display-matrix-readonly-20261015.json`，现已保字节归档。JSON 保存全部模式、相关原文行、文件 SHA256 和来源范围；它不属于生产包。

### 原生规则与边界

- `C:/Program Files (x86)/Steam/steamapps/common/Stellaris/unchecked_defines/00_interface.txt:118–121` 声明 `GUI_BASELINE_WIDTH=1280`、`GUI_BASELINE_HEIGHT=720`、`GUI_EXTRA_HEIGHT_MAX=0`、`MIN_GUI_SCALE=0.5`。前两项注释是 GUI 脚本采用的基准尺寸，不能据此断言最低合法分辨率为 1280×720。
- 原版 `settings-layout.json:43–56` 将全屏和窗口分辨率交给 SDL 的 `fullscreenResolution` / `windowedResolution` provider，并带有 `borderlessCurrentResolution` 变体。文本没有固定的合法分辨率枚举。无边框模式的请求分辨率不能脱离当前桌面尺寸单独当作已生效的证据。
- `interface/settings_view.gui:1143–1178` 的 `gui_scale_spinner` 使用 `maxValue=100`、`startValue=0`；同文件 `resolution_spinner:814–825` 也使用这两个值。这只是原生逻辑填充的 spinner 控件定义，不能把它解释成 UI 缩放最高 100 倍、最低 0 倍或默认 0 倍。
- 简中 `localisation/simp_chinese/main_2_l_simp_chinese.yml:3305` 明确提示最大缩放依赖分辨率，并提醒过高值可使部分界面超出屏幕。读取范围内没有给出每个分辨率的数值上限或默认值，不能从该提示恢复出完整数值表。

### 当前 Windows 与历史引擎证据

本次仅查询 `EnumDisplayDevices`、`EnumDisplaySettings`、`EnumDisplayMonitors`、`GetMonitorInfo`、`GetScaleFactorForMonitor`。活动主显示器为 `\\.\DISPLAY1`，当前 1920×1080、32 位色、60 Hz；工作区 1920×1040，Windows 缩放 100%。另有三个未活动显示设备，其设置查询返回无法定位，是未活动设备记录，不是主显示器查询失败。没有调用显示或 DPI 设置函数。

主显示器枚举 26 个模式、24 种尺寸，最低像素面积为 640×480。640×480、1024×768、1280×720、1920×1080、2560×1440 均在系统枚举中。系统枚举仅证明驱动提供模式。

更直接的历史依据位于实际 RC6 运行 `20261015T090720Z/logs/system.log:56–79`：原生 `graphicssettings.cpp` 输出 24 条 `Usable res`，从 640×480@59 开始，包含 1920×1080@60 和 2560×1440@60，最高到 2560×1600@59。因此 **最低引擎枚举可用候选是 640×480**。该日志来自历史 RC6 夹具运行；当时实际渲染尺寸为 1600×900。它没有证明正式 0.2.1 在 640×480 下实际选中、加载并完成长名交互。

用户普通配置的 `settings.txt` 保存 1920×1080、`gui_scale=1.000000`；同目录 `pdx_settings.txt` 保存无边框、2560×1440，二者并不一致。不能挑其中一个当当前游戏实际尺寸，亦不能把既有用户值 1.0 宣称为原生默认。历史 RC6 隔离配置则保存窗口 1600×900、`gui_scale=0.750000`，对应日志实际尺寸一致。这仅覆盖历史组合，不迁移为正式包显示矩阵 PASS。

### G0 待冻结矩阵

| 分辨率 | 候选依据 | 最小缩放 | 默认缩放 | 最大缩放 | 当前实机状态 |
| --- | --- | --- | --- | --- | --- |
| 640×480 | 系统支持，历史引擎最低 `Usable res` | 原版定义 0.5，仍核对选单端点 | UNKNOWN，需核对默认及自动限制 | UNKNOWN，需原生端点 | NOT RUN |
| 1920×1080 | 原方案显式目标，系统与历史引擎支持 | 原版定义 0.5，仍核对选单端点 | UNKNOWN；既有用户值 1.0 仅供定位 | UNKNOWN，需原生端点 | NOT RUN |
| 2560×1440 | 原方案显式目标，系统与历史引擎支持 | 原版定义 0.5，仍核对选单端点 | UNKNOWN；不能沿用用户配置推定 | UNKNOWN，需原生端点 | NOT RUN |

仅供寻找端点的几何假设 `min(width/1280,height/720)` 对三行分别得到 0.5、1.5、2.0。**这不是从原生实现得到的上限公式，不是合法性断言**；它没有证明端点步长、舍入、默认值、低分辨率自动钳制或实际界面可操作性。不得据此直接把 0.5/1.5/2.0 写成已经查明的最大缩放。

主任务应先打开原生设置，保存分辨率列表最低端、各分辨率缩放最小端/默认/最大端及禁用状态的实际画面。640×480 若未出现在原生选择器，或引擎拒绝/回退，保留完整证据后再选下一项；不能因布局较小而自行用 1280×720 替代。默认值应来自隔离配置下原生恢复默认或缺省设置生成的结果，记录实际生效值；默认在当前分辨率受限时，分别记录请求与钳制后的值。最小、默认、最大若重合，可去重执行同一实际组合，但保留三个标签及原生相同值证据。

### 现有适配器的限制

本次只读源码，没有导入 `runtime_feedback` 或通用 harness。通用 harness 在导入时即执行 DPI awareness 设置，不能把导入它作为纯查询操作。

`shishan_code_origin/tools/runtime_feedback.py:31–46` 在 `prepare` 中固定请求窗口 1600×900、缩放 0.75；通用 harness 默认又请求无边框 2560×1440。直接调用现有 `prepare` 不会产生上表要求的矩阵。准备 manifest 的 requested 字段也不是实际设置验收。

其新鲜 Steam F12 GPU 截图、图像实际尺寸、`GetClientRect` 与 `ClientToScreen` 证据格式可供主任务复用，但 console 仍含 `(1200,750)`、`(200,317)` 等固定点击位置；它们在 640×480 或不同缩放下可能越界或命中错误控件。历史坐标不可直接套用，须依新原图/OCR定位。截图查看器缩放、OCR识别成功和系统工作区尺寸均不能代替实际客户区/画面尺寸。

当前桌面 1920×1080 下，完整 2560×1440 窗口无法全部置于工作区；1920×1080 带边框窗口也可能超出 1920×1040 工作区。主任务需要明确选择实际可覆盖全画面的显示模式并核验物理图像尺寸，不能截取裁切窗口后声称完整矩阵已验收。本调查不改变桌面或选择模式。

### 主任务实际 UI 验收清单

1. 先核对正式 90 文件、唯一启用包及无 fixture。只读比较当前生产清单与发布验收 `release-identity.json.content` 完全相同，规范 `mod_tree_sha256` 为 `835267fa011282b26bc36b4f38202489e9a5dd137bec40de1bd46596706eae94`；未包含 `events/shishan_feedback_probe_events.txt`。报告另记通用 harness 的原始内容树散列 `ce525436177a71179d1715887b504dd43e59294e43cdd9e05a3a5c20deaa17dc`；两者散列算法不同，不能混写。
2. 从原生设置冻结实际合法矩阵，记录 Windows 分辨率/缩放、显示模式、游戏请求值、原生写回值、日志实际尺寸、GPU 原图像素尺寸及选单端点。每个必需但环境无法执行的组合记 BLOCKED；有证据的原生不支持组合单独说明，不记 PASS。
3. 两类机械政体分别加载相应的同一暂停状态，在矩阵组合中复核国家修正列表及悬停、架构详情、起源/局势说明、维护/优化结果和三选一/reroll 禁用原因。逐字核对「基于低内聚高耦合的旧时代集成服务架构」18字，完整名称、5%规则、U/R/T/M、覆盖、冷却及按钮都须可读可操作。紧凑标题/列表原生省略时单独记录，展示正常可达的全文路径。
4. 保留新 GPU 原图、OCR JSON及人工复核。不得用 OCR 是否识别出全名代替边界、图标、按钮和滚动可达性的目视检查，也不得将调试 dump 的存在当正常可达全文。
5. 各状态原生保存后正常关闭，以同一正式生产包真正重启、重载并复看名称与关键值。覆盖普通奖励、耗尽 R+1、清理/复发及重抽/冷却状态；如复用旧夹具存档，应确认没有必须依赖已移除 probe 的排队事件或本地化，并单独记录来源。保存/重载的源哈希和实际加载证据不能由准备 manifest 代替。

本篇交付的是 G0 输入资料和后续验收步骤。没有启动游戏、发送输入、捕获桌面、改变显示/配置、编辑生产或 runtime 工具；非简中运行时不在范围内。正式包重新启动、显示边界和保存重载的最终结论仍由主任务新增实机证据决定。

## 后续正式包原生 G0 选单证据

主任务在纯正式90文件运行 `20261015T103709Z` 完成窗口模式原生分辨率完整循环，共18个不同选项；最低为 **1280×720**。新证据为 `formal021-native-resolution-cycle.json`。之前系统/历史引擎枚举的640×480仍是已观察事实，但当前原生窗口选择器完整循环未提供它；当前G0显示矩阵因此应采用1280×720为最低选项，不能继续把驱动列表当游戏选择器。

同一运行的 `formal021-native-scale-endpoints.json` 保存三档分辨率逐项选中的端点：

| 分辨率 | 原生选中的最小缩放 | 原生选中的最大缩放 | 默认值 | 实际应用/长名渲染 |
| --- | --- | --- | --- | --- |
| 1280×720 | 0.5× | 1.0× | 尚无恢复默认证据 | NOT RUN |
| 1920×1080 | 0.5× | 1.5× | 尚无恢复默认证据 | NOT RUN |
| 2560×1440 | 0.5× | 2.0× | 尚无恢复默认证据 | NOT RUN |

两个主任务JSON均明确 `selection_only_not_applied=true`；当时实际窗口仍为1600×900。这些证据已把“候选端点”推进到“原生选单可选性”，不能据此声称对应物理画面尺寸、缩放渲染、长名可读性或重载已通过。主任务报告该运行正常退出、未强制结束。分辨率与六个缩放端点的原图SHA256已只读逐一核对一致；本协作者未进行额外GUI操作，也没有替代主任务目视确认。

补充JSON为 [原生G0只读索引](evidence/feedback-redesign/remaining-2026-10-15/programmatic/display/display-matrix-native-g0-addendum-20261015.json)，保留原始调查JSON及当时UNKNOWN，不覆盖旧快照。原始[18项分辨率循环](evidence/feedback-redesign/remaining-2026-10-15/programmatic/display/formal021-native-resolution-cycle.json)、[六个缩放端点](evidence/feedback-redesign/remaining-2026-10-15/programmatic/display/formal021-native-scale-endpoints.json)、[help命令回执](evidence/feedback-redesign/remaining-2026-10-15/programmatic/display/formal021-native-console-help.console.json)和[原始OCR](evidence/feedback-redesign/remaining-2026-10-15/programmatic/display/formal021-native-console-help-result.ocr.json)也已保字节复制。UI-04整体仍为 NOT RUN。

归档位置和原始源路径映射见[独占证据清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/manifest.json)，未更改原报告内容或哈希；原图由主任务正式实机证据归档负责。
