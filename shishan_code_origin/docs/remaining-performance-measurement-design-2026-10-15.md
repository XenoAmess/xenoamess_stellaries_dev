# PF-01 原生性能测量能力与后续设计

日期：2026-10-15。目标生产版本 `0.2.1`。本回合只调查与设计，不新写 P 夹具、不启动游戏、不发送 GUI 输入、不注入进程或修改生产/运行工具。

## 目标与验收范围

原 PF-01 要求小/中/大帝国、1/10/50个有真实人口的主体谱系模板，协同开/关各100月，预热后比较刷新/每日tick的 p50/p95，并调查同配置p95恶化超过10%的可复现情况。用户排除NAT自然新局/长期路线，不等于排除本性能用例。

本调查优先寻找 4.5.2 原生可导出逐次计时的 profiler，明确记录时钟、样本单位、采样/聚合方式与可审计产物。单纯100月总时长、平均FPS、肉眼流畅或稀疏OCR日期采样均不足以构造每日tick分布，不得冒充 PF-01 PASS。

## 调查方案与验收标准

1. 只读实际引擎生成文档、仓库现有工具/证据与原版文件。必要时只读 EXE ASCII 命令注册字符串；字符串仅表示候选存在，不能证明命令可执行、支持参数、产生指定计时或在本构建可用。
2. 需要外部资料时仅使用官方/一级来源，不将 CK3 命令或旧 Stellaris 版本未经核对地当成4.5.2能力。
3. 给主任务最小只读 help/profiler 候选核查步骤，明确哪些已由本机证据确认、哪些必须实机验证；不在本协作者侧调用它们。
4. 为1/10/50真实模板及小/中/大规模提出隔离受控输入方案，保留国内谱系、人口总量与分布、领袖、岗位和刷新次数可审计性；开/关对照只改变协同贡献及刷新路径，不能写期望性能输出。
5. 若逐tick或脚本刷新计时能力未取得，列明具体缺口及可继续的最小验证工作；不因当前没有工具就删除用例，也不把统计替代品登记为原合同PASS。

## 调查记录

初次只读调查完成时，原生计时短运行、性能前置夹具和全部PF-01测量均为 NOT RUN。后续新增计算OFF基础设施的静态验收与一次原生短运行格式观察见文末；PF-01整体仍为 NOT RUN。

## 已找到的原生测量路径

### 每日耗时：优先核验 `-gamestatetimer`

官方 [Dev Diary #410 - 4.3 Performance Comparisons](https://steamcommunity.com/games/281990/announcements/detail/510730583362502785)（2026-02-05）介绍启动参数 `-gamestatetimer`：在日志目录输出TSV，列为 `Game Date`、`Time Unit`、`Seconds`，示例包含Micro与Day行。该文属于4.3背景，不能独自证明本机4.5.2行为。

本机4.5.2 EXE的SHA256仍为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。只读ASCII检查找到：

| 十进制文件偏移 | 原始字符串 | 可证明的范围 |
| --- | --- | --- |
| 36687088 | `gamestatetimer` | 当前二进制保有此标识符 |
| 37376120 | `logs/gametimer_%04d%02d%02d_%02d%02d%02d.tsv` | 当前二进制保有计时输出文件名格式 |
| 37376256附近 | `Game Date` / `Time Unit` / `Seconds` | 存在与官方示例相符的字段 |
| 37376340 | `Micro` | 存在微tick单位标签 |

初次调查时，这是**有官方出处且当前二进制有对应字符串的候选能力**。当时尚无本机新TSV，因此没有确认逐日记录完整性、时间单位边界、是否包含等待/暂停、刷新缓存或导出刷新时点。文末补充主任务随后实际启动所得的Day格式观察；仍不能从字符串直接写“4.5.2逐日测量已通过”。

主任务最小能力核验：在下一次隔离运行的实际进程参数中加入 `-gamestatetimer`（不改Steam永久启动项），加载副本并推进少量完整日和至少一次跨月，正常停止后归档新增 `logs/gametimer_*.tsv`。核对请求参数确实出现在进程清单、文件mtime/哈希、表头、Day行数量和连续日期，暂停窗口是否产生日样本，以及跨月样本的归属。确认后的Day行才可作为每日耗时输入。它是启动参数，不能当console命令执行。

另发现 `logs/%stimer_dump_%s.txt`、`DATE,FULL_TICK,` 和各系统计时标签；尚未定位其公开启动/导出入口和样本语义，保留为次级线索。`timer`、`profile_start`等相邻启动标识也未验证，不推荐据此任意拼命令。

### 脚本刷新：`script_profiler` 有累计导出依据，分位数仍有缺口

当前EXE包含 `script_profiler`（37642592）、启用提示（37622048）及再次执行关闭并导出 `script_profiling.log` / `script_profiling_summary.log` 的提示（37622128）。原生格式字符串另含 `Total Time`、`Average Time`、`Hits` 和 `Node, Total Time, Hits`。这比借用其它Paradox游戏命令可靠，但仍未实际执行。

官方 [Dev Diary #397 - Shadows of the Shroud is Out, What's Next? (Performance)](https://steamcommunity.com/games/281990/announcements/detail/503963131223999792)（2025-10-02）介绍用脚本profiler定位累计时间、调用次数和平均耗时。此资料支持诊断用途，未提供每次调用的独立样本。

如果新日志只有每节点总耗时/次数/均值，**不能从这些聚合量还原每次刷新的p50/p95**。100月累计报告可定位热点、核对命中次数和平均开销，不能填充刷新分位数。

后续优先检查真实日志是否带逐次事件或可清空的独立窗口；若没有，可另行设计100个等条件、每窗口恰好一次生产刷新调用的计时实验。每窗必须有可识别的原生计时节点、Hits=1、完整父子节点说明及唯一日志，才能将该窗的原生耗时视为一个样本。若需要独占事件包装生产刷新，计量名应写“刷新包装事件的inclusive时间”，并提供空包装基线，不能宣称纯函数独占CPU时间。控制台本身、日志和profiler开关有测量开销；两组须使用相同方式。此方案尚未实现，不能预设scripted effect名称必定保留为独立计时节点。

## 交给主任务的最小诊断查询

本轮全部命令均未由本协作者执行。正式纯生产运行 `20261015T103709Z` 已由主任务执行 `help`，对应 `formal021-native-console-help-result.jpg/.ocr.json` 与 `.console.json`；它只证明console帮助入口存在，右侧Debug Stats/Time/Graph等界面未作性能测量。

先进行只读帮助查询：

```text
help script_profiler
help debug_stats
help ticks_per_turn
ticks_per_turn
```

最后一项不带参数，当前EXE有“currently”与“set to”两种提示，意图仅查询现值；若本机构建help不支持该形式，就停止并保留输出，不附带数值以免改变仿真配置。

只有help和隔离日志取证确认后，才在暂停副本执行一次 `script_profiler`，推进短窗口，再次执行它关闭并取新日志。此操作改变诊断采集状态并写日志，不是纯帮助查询，不由本协作者执行。`debug_stats`若仅显示最近30次平均、最近一次日耗时或FPS，仍不能从稀疏截图恢复完整分布。没有把HOI4/CK3的 `imgui show profiler`、`debug_dumpticktasks` 等名称移植为本机Stellaris命令。

## 数据合同与统计方法

- 每个样本保留原生文件哈希、行号、游戏日期、原始Time Unit和Seconds；确认单位后才统一为ms。只取Day单位，不把Micro/Day/Month/Year相加重复计量。检查缺日、重复日期、负值/非有限值和断开的采样窗口；异常保留诊断，不静默补零或插值。
- 预先固定至少12完整月预热，之后各组100完整游戏月。预热与测量日期边界以原生日志和存档共同核对，加载/暂停/原生保存成本另外记录，不混入后又按“异常”任意删峰。
- 固定经验分位数为nearest rank：排序N个样本，取 `ceil(p*N)` 位，分别p=0.50和0.95；保存N、最小/最大、原始样本和完整算法版本。日耗时与刷新调用各有独立样本集合，不能混用两者单位。
- 原架构按月刷新，月界样本在所有日样本中占比较小，可能未进入全体日p95。除全体日p50/p95，还分别报告月界/非月界日分布与真正刷新调用的分布，防止月度开销被总体百分位掩盖；不能因此删除全体日合同。
- 同配置比较 `p95_on/p95_off - 1`。超过10%先按相同输入复验，至少三组配对、交错ON/OFF顺序，记录温度/进程干扰/日志模式。调查线不是一次噪声样本即可宣布失败或通过的门槛。
- 固定机器、电源/线程配置、游戏速度、ticks_per_turn、DLC、包、显示设置、相机位置及展开的界面。官方#397也提醒镜头所在星系/银河视图可影响性能；两组使用同一视角，测量期间不反复OCR或保存，不用启动/加载所花时间冒充游戏日tick成本。

## 1/10/50真实模板与规模前置设计

初次调查不写P夹具、不创建/修改sav。后续单独授权只实施文末的计算开关基础设施，尚未实施下面的人口/模板规模夹具。建议先冻结一个可重载的受控银河和两类机械政体种子，使用原生人口/殖民/模板API建立候选网格；数字是G0提案，未执行。三档规模分别固定为1/10/50颗本国殖民地、每颗10000真实人口，总人口10000/100000/500000。与1/10/50个真实主体谱系模板交叉后共9种规模输入，每种仍需两政体和开/关配对。若实际种子无法满足，先调整并记录G0输入，而不是把缺失组合记PASS。

每颗殖民地按T个模板均分10000人口；T=50时每模板每地200人口，避免用1个人口或空模板拼数量。国内实际模板数以原生pop_group的species、size>0及主谱系base_ref关系审计，不能按滞后的owned_species_refs、UI模板列表或全银河物种总数代替。实际pop group数可能因类别/权利/就业拆分，应另报，不能假设总数等于T或殖民地数×T。

模板建立采用原生 `modify_species` 的同谱系新模板，再通过 `create_pop_group` / `transfer_pop_amount` 从既有真实人口分配，保留总人口。保留主模板1个、另建T−1个变体；不得用独立 `create_species` 生成外来谱系冒充主体变体。仅改名字是否会被引擎合并尚无证据；优先从当前原版资格/反向opposites图中选择相容的特质组合，构造50个可区分而**特质总数相同**的合法变体，冻结同一每模板U和全国加权U。两政体各自核对资格，不能把个体机械的合法组合直接套给格式塔。50模板若无法保持此条件，先完成最小原生模板可区分性核验，明确剩余工作。

每档先固定真实岗位和资源容量、n/R、领袖、科技、政策、星球类型/宜居度、权利与队列；保持外国/非主体人口对照和银河其余部分不变。由相同原生sav分叉开/关，原生保存并重载后复查分布。自然人口组装、模板合并、迁移、自动建设、事件和战争导致的分歧要保留并解释；可用有来源的原生受控前提关闭相关变化，但两组必须相同，不编辑测量输出。

### 开/关语义必须先分清

现有经济反向modifier仅抵消岗位加成，生产的 `shishan_code_architecture_refresh_effect` 仍运行人口/特质遍历。它可用于经济隔离，却不是“刷新计算关”的性能基线。正式0.2.1没有跳过此刷新的开关；去掉起源或清除bonus也会改变其它机制，不能充当等条件性能OFF。

后续计算开/关需要单独记录受控运行副本的一处最小切换，明确保留正式刷新原文、入口、频率和调用链，只在OFF跳过这段计算，并保留明确的包差异清单。不能依赖另一个同名scripted effect文件“猜测覆盖顺序”；也不能改已发布90文件后仍声称正式包身份未变。两副本均需G1与实际加载日志，并以真正正式包补ON参考，量化额外条件分支/测量包装成本。初次调查时尚未实施切换；文末已补实施与静态证据，原生ON/OFF测量仍未运行。

## 交付与真实剩余工作

调查证据位于 `_runtime/shishan_code/20261015-remaining/performance-investigation/`：`exe-profiler-strings.json`、`exe-profiler-string-context.json`、`exe-timer-command-strings.json`、`exe-timer-context-secondary.json`、`exe-dump-candidate-strings.json`、`official-source-index.json`。只读ASCII提取包含文件偏移与固定EXE身份；未反汇编、附加进程、注入或执行二进制。现有仓库运行适配器提供启动/输入/截图/存档与日志归档，没有已实施的逐日TSV或逐次刷新分位数采集器；实际引擎 effects/triggers 文档也不是console命令注册表，不能从其缺少profiler条目推出命令不存在。

下一步依次为：本机短运行确认 `-gamestatetimer` 的Day样本 → 确认script profiler真实导出粒度 → 冻结/实现受控性能前置及计算OFF方式并G1 → 运行预热和100月配对 → 对分位数/原始数据做独立只读审计。若script profiler只有累计值，仍须补逐次刷新测量能力；这个缺口不会由每日TSV或100月总时长自动消失。PF-01保留NOT RUN，不因NAT排除删去，也不将本调查完成写成性能通过。

必要原始JSON已保字节归档：[初次调查测量能力状态](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance/measurement-readiness.json)、[profiler ASCII证据](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance/exe-profiler-strings.json)、[tick/timer标识](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance/exe-timer-command-strings.json)、[计时TSV字段与上下文](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance/exe-timer-context-secondary.json)和[官方来源索引](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance/official-source-index.json)。两份包含无关文本的宽范围冗余ASCII上下文仅留本机，未冒充新原生数据；必要原始字段已在归档文件中保留。[独占清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/manifest.json)记原源/归档路径和不变SHA256。初次归档时尚无本机原生时间采样；后续新增观察单独归档，不覆盖这份历史状态，也不产生性能PASS。

## 后续授权：最小计算开关 builder 的实施合同

主任务随后明确授权实现独立计算OFF基础设施，人口/模板规模夹具仍不在本轮实施。以下先记录准确接口，替代上一轮“尚未实现”状态但保留其历史语境。

- 新工具位于 `testing/tools/build_performance_fixture.py`，只用标准库；CLI需要显式 `--output`，默认源为正式 `mod` 和正式发布 `release-identity.json`。先核对version=0.2.1、正式清单90文件逐字节身份、目标effect唯一及fixture前缀未被生产占用，再复制到新目录。拒绝已存在输出，禁止目标位于生产、testing或任何现有运行包内部；不运行桌面助手，不修改当前104文件经济夹具或运行中游戏。
- 唯一被修改的生产相对路径为 `common/scripted_effects/shishan_code_architecture_effects.txt`，仅在 `shishan_code_architecture_refresh_effect` 原body外包一个if。原body包括注释、空白和换行按原字节保留，builder必须能移除包装机械还原整个文件并逐字节匹配正式源。其它89个生产文件保持byteexact，不用同名额外文件覆盖加载顺序。
- 执行原body的条件为 `OR={NOT={has_origin=origin_shishan_code} NOT={has_country_flag=shishan_perf_probe_compute_off}}`。只有有起源且OFFflag有效时跳过整个原body；不移除/重设现有架构modifier、U/R/T/B/M或人口。失去起源时仍执行原清理路径，避免测试flag妨碍原版安全撤销。
- 独立附加事件源位于 `testing/performance/mod/events/shishan_perf_probe_events.txt`。`.1`只在本人origin、已有架构modifier、迁移完成、缓存变量齐备、P>0、无奖励/项目回调待结算和无在研专属项目时设置该country的OFFflag；没有跨国遍历、全局target或自动on_action。`.2`只移除本人OFFflag恢复ON，不立即重算B。`.3`在同类稳定前置下调用真实生产refresh，供后续profiler检查；没有生成任何timing数据或预期数值。
- OFF是**停止刷新计算、保留既有B**，不是关闭经济加成。100月两组要保持相同人口、特质、R和经济输入，使OFF保留的B等于ON本应重算的B；输入发生变化则显式报告控制失效，不能把OFF陈旧缓存冒充生产结果。
- 包中仅90生产投影（1处可还原覆盖、89处不变）加1个隐藏事件文件，共91文件；附带独立VERSION、原文还原副本、修改offset和源/产物SHA256清单，均在受控包外。先G1，再运行静态/模型负例，封口后不再改包。
- 负例应拒绝源身份污染、重复effect/破损包装、其它生产文件被改、输出覆盖、伪timing/经济写入及绕过guard。离线实际AST正例需确认ON等价于正式body、OFF不触及现存B/变量/遍历、另一国家不受影响、失去起源仍清理、恢复ON才重新计算。此模型证据不等于原生时钟、profiler或完整PF矩阵验收。

## 计算OFF基础设施：实施与静态结果

已新增 [builder](../testing/tools/build_performance_fixture.py)、[独占事件](../testing/performance/mod/events/shishan_perf_probe_events.txt) 和 [10项测试](../../tests/test_shishan_performance_fixture.py)。正式源仍为0.2.1的90文件，原生产树SHA256 `835267fa011282b26bc36b4f38202489e9a5dd137bec40de1bd46596706eae94` 未改；也没有修改104文件经济夹具。

执行顺序与退出码如下，G1先于夹具程序验收：

```text
python -B shishan_code_origin/testing/tools/build_performance_fixture.py --output _runtime/shishan_code/20261015-remaining/performance-fixture
# exit 0；91文件、89生产文件byteexact、完整原文可机械还原

python -B C:/workspace/open_kaishek/tools/accept_stellaris_mod.py --mod _runtime/shishan_code/20261015-remaining/performance-fixture/mod --version-file _runtime/shishan_code/20261015-remaining/performance-fixture/VERSION --game "C:/Program Files (x86)/Steam/steamapps/common/Stellaris" --expected-exe-sha256 400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83 --report _runtime/shishan_code/20261015-remaining/performance-fixture/package-open-kaishek.json
# exit 0；PASS：26/26脚本、13 DDS、十语言各269键

python -B -m unittest discover -s tests -p test_shishan_performance_fixture.py -v
# exit 0；10 tests、0 skipped、0.406s
```

独立AST测试实际执行产物中的开关与原刷新，未用另一套公式生成预期：ON与正式生产AST的变量/modifier/flags完全相同；两个实际人口组的初始U=3。改变人口分布后，OFF保持原缓存与B，执行人口遍历和modifier写入次数均为0；移除OFF本身不重算，下一次实际调用才得到U=3.6。失去起源时即使仍有OFFflag也撤销旧B。负例还拒绝无缓存、无modifier、未迁移、奖励凭证未处理或项目在研时开OFF，以及源污染、其它生产文件变化、重复effect、破损包装、已存在/嵌套输出和伪timing事件资产。

隔离包接口仅供主任务后续原生核验：稳定副本已有正常B时 `event shishan_perf_probe.1` 申请OFF，`.2`恢复ON（下一次正常刷新生效），`.3`调用一次真实refresh入口。各入口只作用于当前国家；拒绝时只记诊断、不改变计算开关。`.1`成功日志为 `SHISHAN_PERF_PROBE_OFF_RETAIN_EXISTING_B`。尚未在原生执行这些入口，不能把AST模型的遍历计数视为引擎profiler。

封口后的91文件保持不变。必要证据已保字节归档：[源清单/还原offset](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-fixture/source-manifest.json)、[G1报告](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-fixture/package-open-kaishek.json)、[10项测试回执](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-fixture/static-tests-initial.json)、[静态封口](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-fixture/sealed-static-summary.json)及[归档清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-fixture/archive-manifest.json)。PASS只指这份计算开关基础设施的包级/静态/模型合同。它不关闭经济B，不是正式发布包，尚无1/10/50模板规模输入、原生ON/OFF对照、逐次刷新时钟或PF-01通过结论。

## 主任务原生短运行：Day格式观察

主任务在经济104文件lab的运行 `20261015T112046Z` 实际带 `-gamestatetimer` 启动4.5.2，11:29:59 UTC正常退出，`forced=false`、`running_after=false`。这次运行使用的不是上述91文件计算OFF夹具。本协作者只在停机后读取和归档日志、运行清单及原生操作回执，没有启动进程或操作GUI。

原生 `gametimer_20261015_192252.tsv` 为35374字节，SHA256 `4a0a320a0ae89672ae9c61ea405c4a78b4fb3828590a4e34f4f4503c157d62c4`，表头实际为 `Game Date / Time Unit / Seconds`（前两列原文保留尾空格）。1369行数据中，Micro=1227、Day=122、Week=17、Month=3；全部三列，Seconds均有限且非负。Day首条为2209.11.30、0.327236秒，末条为2210.04.01、0.355059秒；按实际30日历逐条检查，此区间无内部缺日、重复或倒序。原始Micro从2209.11.28开始，初始两日期没有Day行，因此没有补零、插值或把它说成从UI起点完整采样；边界标签/暂停等待是否入时钟仍待校准。

这证明当前构建能够实际导出原生Day记录，不能证明完整性能合同。该短段无12月预热、100月测量、配对OFF、小中大/1/10/50模板矩阵，也未确认逐次脚本刷新时钟。本次不计算p50/p95，不将经济lab的一段日志写成PF-01 PASS。

原始TSV及原生清单/帮助/推进/保存回执与图像共26份，均保持原字节：[原生TSV](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/gametimer_20261015_192252.tsv)、[格式审计与Day原行号](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/day-schema-observation.json)、[26份来源归档清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/performance-native-shortprobe/archive-manifest.json)。保存包元数据独立读取核对到2210.02.02、03.02、04.02；这里只核时间和原生来源，生产经济/月回调正确性由其它实机合同审计。
