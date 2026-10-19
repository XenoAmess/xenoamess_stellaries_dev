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
