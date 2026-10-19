# RC7 三类新局完整经济接收审核方案

本页在接收新样本前固定审核范围。只读了既有接收计划、RC7 经济适配器和采集器源码；没有运行分析器、读取 `r7puc` 未封口文件、活动日志或当前 run 指针，没有操作 UI、Git、Steam、Mod 或工具。只有 root 明确通知对应 worker 已结束、前缀不再写入且实际来源已固定后，才读取和归档该局。三政府都使用真实 RC7 新局的完整 12 月，不采用 RC6 source bridge，也不把旧 `r7pu` 四月失败包补成全年。

## 前缀与既有分析器

现有 [rc7-economy-analysis-v1.py](evidence/1019-analysis/rc7-economy-analysis-v1.py) SHA256 为 `7b510ee8508fc551786fbe76f608e159ad056e867dc8c70c2fac356c199fa337`。源码与 AST 只读检查确认：`--prefix` 传入 `analyze(branch, prefix)`，所有样本路径由参数拼接，校验为 1–20 位安全 ASCII，没有 `r7pu`、`r7hvc` 或 `r7mc` 字面硬编码。因此可以原样接收 `r7puc/purifier`、`r7hvc/hive`、`r7mc/machine`；换前缀无需新增 v2，原 v1 保持原字节。

输出目录按 government branch 固定为 `evidence/1019-rc7-economy/{purifier,hive,machine}`，并以 `exist_ok=False` 拒绝覆盖。接收时须确认输出目标尚不存在；失败重试另立目录和新的补充映射，不能删除旧证据后重跑。原 `purifier-attempt1-partial` 和仅两件文件的预备 worker-ui 空包不作为新局完整证据。

既有运行边界固定为 run `20261019T164112Z`、版本 `0.4.0-rc.7`、tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，与 [原三局计划](rc7-fresh-economy-and-lithoid-receive-plan-1020.md) 一致。实际回执若不符则停止接收并记录差异，不替换身份以适配样本。以后确有分析缺陷时，先另写设计再产生新的不可变版本；不热改 v1 或原报告。

## 完整序列与原生身份

每局必须具备原生 `m00`（2200.01.01）、逐次独立 FF30 的 `m01..m12`（2200.02.01 至 2201.01.01）、另存 `yearui`（2201.01.01）、总经济 receipt、各月 receipt/audit/economy JSON、m12 auto/UI comparison、原 manifest 及对应输入/GPU/OCR 链。m00 与 yearui 各自保留确切 native-save receipt，不用同 SHA 的其他回执替代。基线仍为已封口 0.3.1 同政府 m00 与 12 月，不称纯原版对照。

总 receipt 的实际格式是 `status=OBSERVATION_ONLY`、`state`、`plan`、`collector_sha256`、`snapshots`、`commands`、`year_ui`、`auto_ui_comparison`、`cleanup_errors`；源码没有顶层 schema，不补造字段。只接受 `COLLECTED_NOT_ACCEPTED`、12 snapshots、12 commands、12 planned months、空 cleanup errors。`ABORTED`、`CLEANUP_REQUIRED`、缺月或未生成 yearUI 只封失败/部分证据，不能运行完整通过流程。

逐月核 plan/receipt 的实际前缀、government、run、manifest SHA、tree/version、anchor receipt/SAV SHA 和日期；每个命令必须实际为 `fast_forward 30`，其 action 文本、物理 Enter 及先后顺序分别有原件。核每月新 autosave 的 prior/actual mtime、command_started_ns、CRC、原生日期、SAV/audit/gamestate SHA 与 HUD/OCR 的新图绑定。日期必须逐月独立递增，不能以一次 FF360 或未来同名文件替代。解析 Mother/core/ship/fleet/colony 均取该银河实际 SAV，不沿用旧 ID。

对每份原生档重新核完整 `budget.current_month/last_month` 的收入、支出与 balance parent/category，库存、人口实体、岗位、区划、殖民地及国家 native/flags，不能只信已有 audit 的摘要数字。三政府分别核真实 founder/government，Hive 必须有机且无 Lithoid/Machine traits，Machine 必须真实 machine founder。全过程保持 C/L/R/六 tiers 为 0、六个真实 core 正确装备、自动吞噬关闭；开局及首月只有一殖民地、母星类型正确，m00 初始能量 200、人口与同政府基线 m00 一致，首月发电岗位真实有人就业。

独立计算 12 个候选月的实际能量净额并要求每月不为负，保留所有其他资源与负项；按原 v1 的每资源账本核库存差额与当月净额，容差仅沿用已声明 `0.00001`，不为结果放宽。正常维护须实际存在 ships、ship_components、planet_buildings、原生 `planet_districts` 及其子类别支出，母舰折扣与旧源一致且只作用于对应母舰 fleet。m12 与同日 yearUI 必须通过既有经济字段比较，不能把日期一致当字段一致。

## 四项操作约束的独立审核

分析器的 `no_resource_injection`、`no_trade_subsidy`、`no_job_closure`、`no_ship_disband` 原本保持 null，完成 12 月本身不会把它们变成 true。后续另写逐政府补充审核报告，引用 root 的实际受控 worker、完整新局至总 receipt 结束的动作链、源代码和原生观察；不改原生成报告。

| 约束 | 必须核对的证据与限制 |
|---|---|
| 无注资 | 所有实际控制台输入仅为既定 FF30；没有资源/库存修改命令。各资源逐月库存账本闭合是独立佐证，不能单独证明整个动作历史。 |
| 无贸易补贴 | 新局至总 receipt 的实际输入没有贸易/外交补贴动作；保留预算类别与逐资源账本的全部原值，异常单列。不能凭最后库存推断未交易。 |
| 无关岗 | 实际输入没有关闭岗位动作；全部检查点的有限岗位 workforce_limit 等于 max_workforce，并复核岗位实体/布局。岗位有人就业与不存在历史关岗是不同断言。 |
| 无拆舰 | 实际输入没有拆舰动作；每个检查点的初始所有舰船 ID、姓名和 fleet 归属均保持。检查点之间的历史仍依受控动作链及 root 明确交接核实。 |

约束审核范围只到该经济总 receipt/cleanup 结束。后置母舰媒体、成长、PK 或其他功能分支应另立前缀，不收进全年动作链，不用后置步骤覆盖经济期间的事实。这里只能表述为受控 worker 输入范围审核，不宣称全系统输入审计。缺任一必要来源时对应约束继续 null，整组 case 保持 PENDING。

## 新焦点 helper 与执行来源闭包

旧失败使用 `runtime_single_homeworld.py` SHA `cb0d2d2469c47183eac3211148bbf6c9e51b263bc719c35bfb9981e18326ea34`；修复后计划读取的当前源为 `ce9e5de261f477ee23c52979ea5140c6881a414f5728d30af17d1c7f2ff7b2a3`，见 [焦点修复设计与测试](titlebar-focus-recovery-1020.md)。这只是本页读取时的源码值，不预先认定未来 worker 实际使用了它。验收仍要取 root 明确固定的执行源码/导入时点及前后 SHA，逐字节封存，若发生漂移保留旧快照与事实，不能回填“执行时相同”。

总 receipt 仅绑定 `runtime_economy_1019.py` 的 collector SHA；既有 branch report 的 parser_sources 也没有覆盖新焦点 helper。因此不能复用旧 growth 大包的 helper hash 作为新经济动作来源，必须额外绑定实际新 worker 源与其执行链：`runtime_economy_1019 → runtime_growth_1019.LiveBackend → runtime_1019 → runtime_single_homeworld → runtime.py`，并绑定审计/原生读取/发布检查所用本地导入来源。可复用已封口且字节相同的文件，但新 helper 必须有独立新来源副本及实际调用说明；manifest 的 59 件 Mod 文件与辅助工具来源是两个不同绑定。

本次只读记录的稳定源 SHA：collector `d5f6a21fd2408779ae7b6494bacb21d83e5cb3245644af1c69673006749d56f0`，growth backend `cab98ce18119f27838456dd6118001cc7fee5254b3150c5e5c8fcf5365f7e747`，runtime_1019 `003b04d9046088107ada8359d2189f16c70cbf99833990765574d217e9ac7c87`，GPU/native UI helper `84b7fdda9489392f5abab5fc71c9bd61bcc5933185a02f7c6c479d703b155ffc`。这些值是接收比对依据，不能替代实际执行证据。标题栏恢复动作若实际出现，保留其成功/失败 action、窗口/PID/坐标与前后状态，不据离线测试宣告实机恢复成功。

## 封口与结果表达

root 完结通知后才按具体完成前缀收件；原件先后两次字节/metadata 稳定检查，逐项原字节复制，列绝对来源、项目内相对路径、大小、SHA，独立复核完整集合、CRC、引用、图/OCR、输入/Enter。新薄包、完整 worker UI 原链、源闭包和操作约束补充审核分别建新索引，不修改先前 sealed 文件。预备空包不伪装已有原件，不预填未收到的文件路径或 hash。

分析通过只表示 branch startup/12 月预算和同日 auto/UI 字段的限定通过；完整两组 case 还要汇集真实 UI、四项操作约束与最终真实 stop 后的日志证据。活动日志本轮不读不封，未齐项保持 PENDING，不写 final-result，不把非中文静态校验写成实机通过。

## r7puc 完结交接与实施范围（收件前）

root 明确交接：纯经济 worker session2001 已 EXIT0；`r7puc-economy-receipt.json` 为 COLLECTED_NOT_ACCEPTED、12 snapshots、空 cleanup errors；yearUI 日期 2201.01.01、原 SAV SHA `e036f3594d980c2e7797623d948fbd7f7be0cf042b120593504a4dd627c03eaf`，与 m12 逐字节相同。现按本页既定方案运行原 v1 的 `--branch purifier --prefix r7puc`，再独立封该固定前缀的 newgame、m00..12、yearUI、receipt 与 exit cleanup；排除后置 `r7pucmedia*`、已在焦点包中的 cursor-reset/recover 动作、其他新局与活动日志。

root 同时交接实际受控 worker 仅执行 `new_game(EEP04, r7puc) → make_plan(显式 RC7 tree/version) → collect`，未操作资源、交易、闭岗或拆舰。本轮仍逐件核实际 type_text action 和原生观察，四项约束最终仅表述为该受控 worker 范围，不宣称全系统审计。旧高成长分支的控制台历史可能跨新局保留；OCR 的历史文字不等于本局实际输入，须以原 action 与原生 C/L/R/六 core 为准。原 `r7pu` 失败、原 v1 分析器及既有 sealed 证据不改。

原 v1 已生成新的 `evidence/1019-rc7-economy/purifier` 薄包：57 原始 payload、8,923,328 B，报告为 PASS_SCOPED，四项操作约束仍 null，未改原报告。实际 12 月电力为 +46.23969 至 +46.75291，能量 200→757.88612；这仅陈述新银河实测，不能改写旧 RC6 或 `r7pu` 的不同数值。已看到的输入原件共 111 actions，其中 14 个 type_text 恰为 12 条 FF30 与两次保存命名，无其他文本输入。

接下来独立验证薄包，并在新 `evidence/1019-rc7-purifier-economy-worker-ui-v2` 封完整受控动作原链。当前白名单为 284 个纯经济 `r7puc*` 文件；其 56 个已在薄包的同字节前缀原件仅作 canonical 映射，不重复复制；manifest 另外引用薄包。其余 UI 原件逐字节复制。源闭包复用原 growth 包内仍完全一致的 18 件本地执行来源，额外保存 collector 与新焦点 helper 两件；新 helper 只新增标准库/第三方 imports，没有新增本地模块。原文档的 worker-ui-v1 空包继续排除。另写独立四约束范围审核与 PENDING 提案，不把原分析报告中的 null 改为 true。索引封口后再独立核 payload、canonical 原件、图/OCR、12条实际输入/Enter及源映射；活动日志和后置 media 不入包。

维护来源还需补齐两件小型原源文件：报告使用的原版 `00_common_categories.txt`（证明 district 子类别父链）和 0.3.1 基线 `eep_modifiers.txt`（证明母舰维护折扣保持）。它们在本轮只读确认没有可直接复用的同路径项目内副本，故原字节单独收进 source，记录绝对原来源与 SHA。RC7 当前 modifier 继续复用已封口 static canonical，不重复复制。此补充不修改游戏文件或维护规则。

归档 index 预检曾把薄包 57 payload 的数量误当作图/OCR 组数，预设 57 组后主动断言失败；当时尚未输出 index，未产生通过报告。独立目录计数确认 UI 原件实际为 52 对图/OCR，原图与 OCR 均完整一一对应；最终按这 52 对及其实际 receipt/HUD 引用封口，不补造五组图。这是离线归档计数错误，不是游戏或 Mod 测试失败。

## r7hvc 完结交接与实施范围（收件前）

root 明确交接 Hive session7895 EXIT0，固定 run `20261019T164112Z`，提供“receiptSHA” `42bf7a730d70d4e78ba658f17159f36c74f1aabace85ecc472e0c23478c83a9d`（后经明确为yearUI native-save回执）；总经济状态为COLLECTED_NOT_ACCEPTED、12 snapshots、空 cleanup errors；yearUI SAV SHA `9191c0e4ca368d09564a3f42693015bf4deef616234dd0bbdadab5306cb5d60b`，与 m12 原 ZIP 相同。现在只接收固定 `r7hvc` 完成前缀，按既有 v1 `--branch hive --prefix r7hvc` 分析，再独立复核薄包、完整 UI/动作链和四约束。source 复用 Pu 已封口20件执行源与原生维护来源，逐件核当前 SHA 后另写本 worker 的交接映射，不把 Pu 执行事实改成 Hive。

root 实际受控链仅为选择原生 EEP02 有机吞噬蜂群新局、显式 RC7 make_plan、collect，无资源/交易/闭岗/拆舰动作。首月预报数值为 workforce507/max1200、净电23.14466，年末净电30.45124/库存521.14698；这些只是交接值，仍须原生独立核实。Jan1缓存净电65.48168仅为m00观察，不能当实际首月收入。root 已开始其他政府，本接收不读 `r7mc`、活动日志或UI，不改 Pu 或旧 partial；缺最终停机日志的两组 case 继续 PENDING。

收件初检捕获对象 SHA 不符：实际总 `r7hvc-economy-receipt.json` 两次原字节稳定 SHA 为 `01c3f9106ad52f77ceec1f33211f37779b9da2572cb76b0d867ca04cd7b161ea`，不是本线程最初误按总回执理解的42bf…。总 receipt 的实际状态/12月/cleanup及yearUI原ZIP与交接一致。保留初次指纹断言失败，已通知root核明42bf…对应哪个 receipt；不改原件、分析结果或放宽SHA。继续仅做授权的只读原生/输入核验，最终按确认的真实对象分别绑定。

root随后明确：42bf…来自 `collect.year_ui.receipt_sha256`，即 `r7hvcyearui.native-save.json`，不是总经济receipt；本线程独立读取该文件所得完整SHA也恰为42bf…。总receipt以双读01c3…为准，yearUI原SAV以9191…为准。这是交接“receiptSHA”省略yearUI前缀造成的对象辨析，不是源字节漂移；三对象各自按真实路径/SHA绑定，初次对象指纹错误事实保留。

Hive原件白名单实际为277件 `r7hvc*`，108个actions、50对图/OCR、14个type_text（12条FF30与两次保存名），25个鼠标动作仅属新局/保存/控制台聚焦。完整原链将另封 `evidence/1019-rc7-hive-economy-worker-ui-v1`：薄包中已封的56件同前缀原件加manifest只作57个canonical原件引用，其余221件UI原件原字节复制；不重复复制已存在的20件源闭包、原生维护源或Mod。新source映射明确链接本Hive worker交接与这些相同源，不能把Pu的执行对象混用。完成薄包后独立原生复核，再生成四约束限定报告/PENDING提案及独立包verify。

## r7mc 完结交接与实施范围（收件前）

root明确交接新Machine session98202 EXIT0，固定run `20261019T164112Z`，总 `r7mc-economy-receipt.json` 为COLLECTED_NOT_ACCEPTED、12 snapshots、cleanup[]。yearUI原SAV SHA为 `41a19510e73c8e92da7d0877dc29dfbcff6ccacda66457a6a34522a9d388d2db`，与m12同原ZIP；yearUI native-save回执SHA为 `53537b73a903710631729ef8f77dc4573129d7845f37ad090c86c7e76e421bae`，明确不是总receipt SHA。现在按原v1 `--branch machine --prefix r7mc` 只接收这一不再写入的纯经济前缀，沿用两局模式生成薄包、独立原生verify、完整UI原链、20源复用映射、四约束限定审核与PENDING提案，不改已有包或原分析器。

root实际新局参数为原生picker的EEP03铁心灭绝者，受控链仅new_game→显式RC7 make_plan→collect，无资源/交易/闭岗/拆船；仍须逐件核实际type_text/Enter/鼠标动作与原生岗位、人口、维护。首月交接净电2.85755、technician_drone905/max1800、core物理2、Mother151/1044，均待原生独立比对；m00缓存88.90835不能当实收首月。root已转 `r7initrepeat*`、`r7cfg*`、`r7relic6*` 新功能前缀，本接收严格不读这些、活动日志或UI，不纳入纯经济。未齐最终停机日志时两case继续PENDING。

Machine初检总receipt实际SHA为 `0a832e38bd1d158ec3876817446b80d0507b9d53427ee28c7bbab4027d04ea8a`，与另两yearUI对象分别绑定，无字段混淆。实际284件固定前缀原件、111 actions、52对图/OCR、14个type_text（12 FF30与两次存档名）、26个新局/保存/聚焦鼠标动作。将新封 `evidence/1019-rc7-machine-economy-worker-ui-v1`：薄包56件前缀原件加manifest只canonical引用，其余228件UI原件原字节复制。20件当前执行来源已与Pu canonical逐件匹配，后续仅写本Machine worker交接/动作映射，源与Mod均不重复复制；保持既有包原样。
