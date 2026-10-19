# 原生换装舍入与旧档迁移：独立 v2 验收合同

## 原因与保留范围

原 v1 政策要求三防算术比例误差不超过 `1e-6`，RC4/RC5 真实样本未通过。独立普通原生 corvette→原生 NAME_Relic 换装也已复现：before H/A 为 `162.87655/200`，set 后为 `16287.6/20000`、`25034.0412/30740`，算术比例各减少 `2.75e-6`；盾也减少约 `4.20004e-6`。此对照没有 EEP 舰船组件或移动船坞，目标以外 11 艘本国船原始块精确不变。原始 SAV before SHA `ee26b57e209b88e2d38215e1db9060b645683826fe1140a1a842c7a4594e300d`，set SHA `2e8c78cffec9f4185065aaeac27b23c10292175d18741d47861e9c3536420189`；完整来源见[事前校准方案](native-current-ship-health-setter-calibration-1019.md)。重载阶段仍在采集，不预填结果。

真实 getter 导出和算术比例也有差异。导出变量精度不等于已证明的内存 canonical ratio，本合同不声称闭源引擎使用某种固定精度算法。单独保留 `1e-6` 诊断及全部原始差异，不修改原 checker、原模板、原报告、历史 FAIL 或数据。

## 目标、设计与预声明边界

在 **RC6 新进程迁移数据产生前** 建立独立 `eep.1019.migration-case.v2`，仅适用于当前精确 EXE、单人真实加载后修复现存母舰的路径。它接受有界的原生换装／重载比例舍入，不承诺数学上完全无损。它不是原 v1 的通过，也不声称修复移动船坞序列化缓存或支持多人即时读档校正。

每一个可观察迁移或重载步骤，逐层计算 `after.current/after.max - before.current/before.max`，相对于该步骤的 before，而非累计放大容差：

- 最大允许下降为 `0.000021`，即两个 `1e-5` 量级舍入单位加原 `1e-6` 浮点余量。
- 最大允许上升仍为原 `0.000001`，不允许用舍入豁免额外回血。
- 同时输出原 `1e-6` 双向检查结果、原始 current/max、带符号差值、各层上限和全部严格差异。

这是针对本次已观察原生路径预声明的**工程验收预算**，不是声称引擎保证的通用精度。超过即失败，不随 RC6 结果扩大；重复同步不经过重载时仍要求三防及原生快照精确相等。每次实际读取都可能有微小损伤舍入，必须列为兼容限制，不把它描述成完全无损迁移。

实现独立 `tools/check_migration_1019.py` 与有意义的正负测试，保持旧 `tools/check_1019.py` 字节不变。新工具用旧工具的 snapshot/旧 v1 报告作原始诊断，但必须独立计算 v2 三防合同，不能修改嵌套 v1 FAIL。所有原来与精度无关的检查继续必须通过：唯一母舰及原舰船／舰队／船坞身份、原名与位置、原版公开档与付费档独立来源、空／11 项真实付费队列、付款者／费用／进度／民用队列、库存、人口／岗位／布局、开局奖励与经济账本不变。

after 和实际 reload 均须确认完整新设计形状、50 槽／6 required／六核心与新设计名。允许原生重新分配设计索引，但不以名称／shipflag／实体 section 冒充真实引用设计体；必须对比实际设计形状与最大三防。移动船坞旧 implementation 必须另外原样报告，不能把它写成已更新。重载快照除明确声明的设计索引重编号及本合同的损伤数值外，其余合同字段仍须相同；新增原生变化不能由 v2 自动豁免。

## 验收标准

固定正例应同时显示 v1 精度 FAIL、v2 有界舍入通过，且完整保留原失败；负例覆盖超过下降预算、超过上升预算、缺失／非数值／非法最大值、旧设计或缺核心、资源／队列／进度／身份／位置／布局／奖励变化、非法政策和错 EXE/树/单人来源。未知或缺失状态拒绝，不以默认零填缺失防御。不修改生产 Mod 或调用修复回血效果来迎合验收。真实 RC6 单人公开档与真实付费档、重载和重复同步完成前，整体迁移仍待验收。

## 独立工具实施设计（代码实施前）

`check_migration_1019.py` 使用不可由 case 放大的固定预算，显式 schema `eep.1019.migration-case.v2`。只接受两种已绑定夹具角色：public031 原件/真实 partial before/空队列，以及 j13ten 原件/在 public031 下制作的真实 partial before/11项付费队列。生成模板时仅固定原来源路径与完整 SHA、身份、单人路径和政策；RC6 after、实际 reload、重复同步两份路径及实际加载回执均留 null。

RC6 精确源树固定为 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`，EXE 固定为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。读取仍通过原 inspector 原生 SAV/审计/回执/manifest/copied-source 验证；独立补读根 player 和加载回执。单人合同要求 case 明示 single-player postload repair、每份 SAV 仅一个根 player 且 country0、实际原生加载回执的 source SHA/原始字节/日期/UI 日期核验相符。没有原生 multiplayer 布尔字段时，不伪造该字段；这是明确单人操作来源、单 player 存档和原生专用回调的联合范围，不宣称辨认任意网络会话。

每步独立输出三个有符号比例差值，使用十进制读取原始数值进行边界比较，拒绝 bool、NaN/Inf、缺失 current/max、max≤0 和 current 越界。首次 after 与 reload 均逐槽比对冻结真实设计全文，并要求50槽/6required/六个核心；最大三防必须为正且 reload 保持相同。首次 Mother 舰体最大值须保留原值，装甲/护盾须符合这些 C0 固定夹具已经独立源核的44787.6/167310；它们不是由未来 RC6 结果拟合的预算。原旧 source 中已存在的 paid 舰体额外上下文随 before 原值保留。

工具完整嵌入旧 v1 报告，不改变嵌套任何 boolean 或状态。v2 另行要求旧 v1 的全部非精度项通过，并独立强化 population/jobs、所有库存、country ledger/startup flags、队列付款/进度/民用队列、位置/名字/身份、实际设计形状及 reload 快照。reload 快照只移出设计索引和三防数值，两者分别按明确重编号及固定精度/最大值规则核对；其它字段继续精确。完整原始 strict comparator 报告单列，不设 ignored paths。attached-base implementation/完整原始块单独列出，绝不认证为已更新。

重复同步用独立 before/after 两份原生 SAV，要求 snapshot、三防及严格比较全部精确相同，不应用比例预算。若缺少这对样本则保持 PENDING；不会把已完成 after/reload 外推为完整迁移通过。单元测试只使用明确标注的合成观察，不能当作原生通过证据。CLI 的 `template` 输出 PENDING，新报告均独占创建；`check` 只读取真实原生路径，拒绝覆盖既存输出。

定向负例先发现两个独立实现缺口：旧 snapshot 的 queued design shape 不包含设计名，故 v2 另须逐队列项保持真实 queued-design 名称；country 的 audit-filtered variables 与完整原始 variables 两条读数均需独立保持，不能因合成负例只改变其中一路就漏判。先记录后在新 v2 工具补齐，旧 v1 和历史报告仍完全不改。非法身份导致找不到 attached starbase 属前置拒绝，不强行生成空对象继续判通过。

重复项精确定义为两次 `eep_repair_existing_mothership_design` layout-only helper，不能以首次 fullsync 合法新增镜像代替。paid 可直接把已核 reload SAV 作为 repeat_before；两样本间不得 reload，strict0 包含全部 country/fleet variables。public 从另一分支返回时可另读 after 或 reload：case 显式提供 `repeat_load_source=after|reload` 与 `repeat_before_load_receipt`，对来源→新 repeat_before 追加一个真实可观察 load 步骤，独立按同预算、实际形状、最大值、非精度快照和加载回执核对；再对 repeat_before→repeat_after 要求精确0差异。不提供额外 load 来源时，repeat_before 必须就是原 reload 的同 SHA SAV，不能悄悄插入一次未声明的加载后扩大累计预算。

## 实施验证与命令

独立工具 SHA256 `ebbde31cc991daf6c3c8e12415018d6125cbdaaf2b2b4dcda8a1b7be0836897b`；原工具仍为 `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`。新14项定向测试与旧17项队列迁移测试共31项通过，命令 `python -B -m unittest discover -s eat_everything_origin/testing -p '*migration*.py' -v`。新测试覆盖正负预算边界、原 v1 FAIL 保留、非法防御、来源/单人/回执、所有非精度契约、paid11付款/进度/民用队列、额外真实load和精确重复。它们仅为合成契约测试，不是原生迁移结果。

已生成 `evidence/1019-analysis/rc6-public031-migration-v2-template-v1.json` 和 `rc6-paid11-migration-v2-template-v1.json`，两者未来路径仍null、状态PENDING。复制为新case后只填真实完成的 after/reload、各自 `*.load.json` 和 repeat pair，运行 `python -B eat_everything_origin/tools/check_migration_1019.py --output <新report.json> check <新case.json>`。缺重复样本的部分结果返回PENDING，不充当完整迁移通过；前置条件非法返回FAIL。原模板及报告均不覆盖。

首次 RC6 真实只读接入发现初版 adapter 误解原生 `player` 的外层布局，两个读取均在字段解析处拒绝，没有生成输出文件，也未改变 SAV。实际原始布局为 `player={ { name="unknown" country=0 } }`：外层是匿名记录列表，不是可直接调用 named-fields reader 的单条记录。新工具须增加只接受完整匿名 `{...}` 记录、检查平衡括号且拒绝游离 token 的专用 player reader，再对每条内部记录用原 named-fields reader。新增一/多player、空列表、错误嵌套/游离字段负例测试；这是新 adapter 修复，不修改旧 audit/inspector 或验收政策，也不把解析拒绝误称游戏失败。上列初版指纹和已生成模板字节均保留。

修复后独立工具 SHA256 `08b57969060c037c4e03829f0075f8e7314f262527215e991595bd4778456d38`，新15项加旧17项共32测试通过。RC6 真实公开/paid 四份 after/reload、原始两fixture与partial before 均已通过该 adapter 独立读取，原工具 SHA仍为681836d2...。

首份真实 paid 完整 v2 报告 [rc6-paid11-migration-v2-complete-report-v1.json](evidence/1019-analysis/rc6-paid11-migration-v2-complete-report-v1.json)，SHA256 `99064d9498c0ba368546cfcd4a61b3936ac90c1ef2aa1b14af515b5dd54090e2`，158项全部通过，仅为本合同 PASS_SCOPED。它使用已核 raw SAV 生成的独立观察缓存再调用同一 evaluate 函数，并完整记录来源。首次 after/reload 同为 H100459.6044/101460、A44567.245/44787.6、S69177.6657/167310；H相对真实partial before 的比例下降约3.8990735e-6，A约7.9263010e-6、S约4.2321205e-6；本次 reload 无新增三防损失。所有原11付费项、资源、人口/岗位/布局、普通舰状态、经济变量和旧flags均保持；layout-only helper 两次执行后原生SAV SHA仍与reload相同，严格0差异。附原 v1 结论仍FAIL，严格 old→after41、after→reload9、old→reload41项全部保留；attached base旧1865→1880不称已修复。独立完整CLI路径亦在复核，另存新报告，不覆盖这份结果。

公开档的部分 v2 报告 `rc6-public031-migration-v2-partial-report-v1.json`，SHA256 `56ff020d1936c8717ef2dbc925f2f4a941ca0bdd0c8460bea1284519949e883d`，112项中仅重复样本未齐，因此明确PENDING。其after/reload H92960/93960、A44567.245/44787.6、S69177.6657/167310均相同，旧比例FAIL保留，严格36/9/36；须等返回公开分支的真实 repeat pair 后另建完整报告。

公开完整报告 `rc6-public031-migration-v2-complete-report-v1.json` SHA256 `bff7b26f3ebc089f1f863aca341f94fc5688a5bb0c9ea145ab504832a6d33c7e` 已完成174项限定检查。额外原生返回load本步三防增量0、strict9差异全保留；`r6prepeatbase` 与 `r6prepeat` 同原生SHA `edcd11a54b2926254206bd86e920b6f9af9af9b45ef0ca94c947b5fec0dcb09e`，helper pair strict0。paid完整原生CLI亦实际退出0，独立报告 `rc6-paid11-migration-v2-cli-report-v1.json` SHA256 `d85667777cdd77940067baa0fcf3ffe55d357a6d6fd040660f9ff023bf315ec7`，158项全通过。两组原v1诊断仍均FAIL，不改原布尔值；旧partial/PENDING报告字节继续保留。准确最终字段映射及重启证据边界另见 [RC6迁移证据映射](rc6-migration-v2-evidence-mapping-1019.md)。

主线程随后独立执行 `python -B -m unittest discover -s eat_everything_origin/testing -p test_check_migration_1019.py -q`，15项新测试通过，用时0.866秒。这里与分析线程32项合计不矛盾：32项包含这15项与原有17项队列迁移测试。最终交付清单另以 `evidence/1019-analysis/rc6-migration-v2-delivery-v1.json` 逐文件绑定工具、测试、此合同、映射和20份独立JSON；仅供主线程精确暂存/归档，不替代原生case门禁。
