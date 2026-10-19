# RC7 结算、取消、普通拆解与护栏原生接收方案

本页在PK开始前固定目标、范围、接口与验收标准。只读了[主线程短执行链](rc7-functional-next-execution-1020.md)、原39条命令、RC6补充16条命令以及现有receiver/checker/inspector/publisher源码；没有读任何尚未交接的 `r7pk*`、`r7normal*`、`r7guard*`、jump/cfgui或活动日志，没有操作UI、Git或Steam，不改工具、Mod、SAV或发布门槛。当前所有本轮运行结论为null/PENDING，旧RC4/RC6通过结果不转移到RC7。

范围是新native settlement、queued/cancel/重复/reload不重发、普通决议seed/时长/完成、无效目标及失主护栏，最后组合共同结算材料。Mother配置、Relic、实际jump、维护UI等由另一个接收线程负责；本线程仅在root明确交接后引用其已封口事实，不重复解析。实际有效发射的UI/订单与无陆军/战争前提必须有独立原件；settlement数学PASS不能代替它们。

## 固定身份、来源与新模板

唯一候选为 `0.4.0-rc.7`，59文件tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，run `20261019T164112Z`，简中单生产Mod。fresh Machine年末已封口core物理2、Mother fleet151/ship1044、受益国0；这是之后每个实际原生档的核对起点，不能把2或其他旧ID直接当后续目标/迁移后核心。Relic新增舰船、维护和jump冷却属于功能基线，不再混入纯经济。

| 来源 | 当前SHA256／用途 |
|---|---|
| `tools/receive_functional_1019.py` | `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`；只调原检查器，接收结果不宣告最终case通过 |
| `tools/check_1019.py` | `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`；原settlement/no-settlement/strict比较保持原样 |
| `testing/inspect_1019.py` | `1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`；完整原生观察与来源绑定 |
| `tools/publish_1019.py` | `06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`；新模板必须绑定此实际接口，旧模板不改 |
| 原39条命令 | `76adabaf82dc2c10894222bdb425ee1b994307233e1bccb2c251bdf2f07325c8`；重复回调、q2/50、护栏、迁移等既有资产 |
| RC6补充16条 | `c9b81e616bc3bc2b79c240f8889fe668d296e5035c80b4cbcb7a9ba18f935650`；`r6_`只作片段ID，不继承旧运行结果或数字ID |

先用既有CLI新建 `docs/evidence/1019-requirements/rc7-settlement-native-intake-template-1020-v1.json`，不覆盖旧模板；随后只核interface_sources、schema、角色格式和18组全null矩阵。模板不填未来SAV路径、SHA或角色，不执行receive/observe。实际收件再另建填入真实对象的intake与新cache/output，原模板保持原字节。

```text
python -B eat_everything_origin/tools/receive_functional_1019.py template --output eat_everything_origin/docs/evidence/1019-requirements/rc7-settlement-native-intake-template-1020-v1.json
python -B eat_everything_origin/tools/receive_functional_1019.py receive --intake <实际新intake> --cache-dir <专用cache> --output <新报告>
```

准备阶段已实际执行template命令并EXIT0；新模板SHA为 `8781bd0eb3e621cc60657f177c86ff86bc2e530bfc3f47d097a2a5bf2f6476e5`，18组/138项check全部null，roles/tasks均空。receiver/checker/inspector/publisher四个SHA逐项与上表一致。没有执行receive或observe，也没有创建任何本轮运行通过结论。

## 原生观察的实际读取边界

receiver的每个role只接受其确切SAV/receipt/audit，且原SAV与manifest须在同一原artifact目录；receipt.archived和audit.save必须恰好指向该SAV。相同SHA的另一文件/回执不能替代。UI保存用 `native_ui_save`；自动存档用 `native_autosave` 并保留真实推进开始时间、新mtime证明。reload角色必须有加载后真实另存的回执，只有load输入或load.json不算新输出。intake里实际原来源使用绝对路径，避免 `Path.resolve` 相对当前工作目录造成歧义；归档后另写canonical映射，不重写原receipt。

重要的源码边界是 `inspect_1019.provenance` 会逐个读取原artifact目录**全部** `*.native-save.json` 与 `*-receipt.json`，不只该role。首次receiver observe会走此扫描。为了不越过root对活跃jump/cfgui等前缀的禁止，真正接收前须明确一个相关回执已写定的只读窗口及允许读取的metadata范围，或由root提供同一world_ids集合的既有原生cache。否则先只封已授权原件、维持待观察，不运行全目录扫描。此项已向root报告，当前不修改原工具或绕过来源检查。

root随后明确放开**metadata隔离限制**：仍只在role/SAV阶段明确封口后启动observe；为原provenance的同SAV SHA/date来源查找，可额外只读本固定run已有 `*.native-save.json`、`*-receipt.json`（包括其他已完成阶段）。这些回执由root在阶段结束生成、之后不改；若遇JSON不完整或原字节变化，保留原失败并暂停等root封口，不吞错。role自身SAV/audit/receipt仍须双读稳定且核明确SHA。此授权不含未交接raw SAV/screens/logs，不据此判未交接阶段PASS，也不扩大数值scope；只读完成的jumpReady/wind1回执metadata不等于可读仍在运行的arrival原件。无需改原工具，实际metadata来源范围和失败均随接收报告记录。

cache身份由SAV SHA、manifest SHA、完整排序world_ids、原checker SHA、原inspector SHA组成；每个相同集合只observe一次，其余报告复用已核cache。改变world union须另建观察，不把不同集合缓存冒充相同证据。接收报告可能为OBSERVATION_ONLY或INCOMPLETE，原task FAIL、全部strict差异与未覆盖条件均保留。

## 最短实际交接：一份角色表与独立期望

root每阶段只需明确：worker已结束且前缀不再写；确切文件白名单/排除项；semantic role→实际保存名、日期、kind与SAV/receipt/audit各path/SHA；实际manifest；当时core/Mother/source/victim及guard target映射；实际输入/GPU/OCR与已声明的受控夹具步骤。不为角色名字重复保存；已有同一实际SAV在前提相同时可兼任角色，但不能虚构新保存或新reload。

| 接收组 | 既有语义角色与最短用途 |
|---|---|
| enemy PK | clean/base/calafter、queued/charge/cancel/cancel_reload、requeued/windup_last/fire_start/prefire/immediate/stable、duplicate/duplicate_reload；restart等真实跨进程材料另交 |
| normal | ready50、decision_start、precomplete/immediate/stable、duplicate/reload；逐月实际Situation/progress另引用已存原件 |
| batch guards | ready/idle/fired；九个不同源的物理ID映射，不用一份目标状态替代九项 |
| native-state guards | colonizing/ground各ready/idle/fired；同日真实状态保持与双方/军队归属另核 |
| core guards | before/after、newcore_idle/fired、ownerloss_idle/fired；绑定旧/新物理核心及仍存活的本国人口 |
| Lithoid owned PK | ready/calafter/restored、queued/windup_last/fire_start/prefire/immediate/stable、duplicate/reload；独立新局来源及损耗/人口奖励 |

role名称可用 `enemy_pk.prefire`、`normal.precomplete` 等唯一语义键，实际文件名仍照root原保存名。world_ids取该份intake所有实际source/core/guard的union；每个ID须来自相应新SAV的 `type=planet` event target和原生world，国家capital的colony ID不能当物理星球ID。不同run须显式additional_run_ids和角色manifest，不能静默跨run。

## 结算与有效发射的分开验收

`settlement-case` 必须为 `eep.1019.settlement-case.v1`，path为normal或colossus，填写实际source_world/core_world、expected_q、明确native布尔值、expected_return、expected_other_core_pop_delta、独立worlds奖励校准与SHA、empires预期及正值校准。原checker明确受益国/core owner0；实际不符即报前置差异，不改checker适配。

PK的q从prefire实际物理size减真实 `d_lithoid_devastation` 个数取；normal的q从真实任务启动持久值取，不能再扣期间原生咬下产生的损耗。C增加q；普通G增加q、Lithoid native G不增；D为2+floor(C/4)；made总量为floor(G/6)×100。本次之前账本可能已非零，全部从对应before取，不套旧q19/C19/made300。

enemy期望返还为0；自有/normal返回R先独立按prefire/precomplete合格founder groups及冻结源码资格算，不抄after的eep_last_return。other_core_pop_delta要有事前依据：完成不跨月且无其他人口事件时可预声明自然0；跨月须独立idle/原生来源。Li原生随机人口每次100须有该目标/日期实际原生通知图/OCR；没有人口奖励则为0，不能拿核心总差反推抽签或把奖励算进R。所有校准/期望在比较after前固定。

危机worlds/empires奖励来自本银河scratch独立校准，分别读原生objective；真实Load恢复基线后另存restored，不能保留探针收益。stable才核最后殖民地灭国的自然清理和empires奖励，immediate若仍有旧owner/country缓存就原样保留，不能提前认定没有empires或把后来清理当重复奖励。

原settlement检查EEP五账本、容量、真实pc_shattered、无owner/controller、原生pop groups/jobs与存活计数清空、五种仅一次receipt，以及危机分目标。保留残留历史colony引用，不把它单独判为活殖民地；原strict全差异同时保留。发射另核实际destroy_planet_order的物理目标、真实90 windup与30 fire子订单计数、prefire29→自然完成，不把定位set_location或手工callback当有效shot。war participants/goal和无陆军参与从base/charge/prefire原生战争/armies/运输/地战对象及UI分别取，独立ground guard的人造军队不混入有效shot。

## 取消、普通任务和护栏

queued前后、charge→同日真实Stop cancel、cancel→实际reload另存、stable→duplicate→duplicate_reload各用适当同日no-settlement；它仅检查C/G/D/made/worlds、core人口/容量、source class/colony/五receipt、危机不变。跨日期不得把自然人口变化硬套此接口，须补同日实际对照或留未覆盖；同日业务PASS也不擦除附带full strict FAIL。重复callback只对已毁且带receipt的源，不对有效活源代替自然发射。取消还应核真实Stop输入、订单清空、源仍活以及无提前成长，不能只从账本零推断按过停止。

normal先核真实UI决议与ready50→start：source50→100、core−50、总人口守恒、seed_existing100/seed_need0、q2、months5、Situation进度0。逐月原生Situation目标/进度和自然precomplete→immediate→stable证明时长/完成，不改进度，不预填150天。返回期望取实际precomplete对象，之后同日重复/reload不重发。

batch九源必须不同，七home源分别有active/devouring/credit/destroy/secondary_core/artificial/qzero真实前提，另有home外未殖民源与真实中立殖民源；qzero为物理size2+两真实损耗，而非只改eep_q。ready→FF1 idle与Load ready→dispatch→FF1 fired须在同日、前提仍真时逐源no-settlement。未准备满七个home可选对象则夹具不成立，不能把未派发当成功拒绝。colonizing要真实仍在殖民；ground要实际持续地战及双方真实归属，不以create_army日志代替战斗。bound/foreign/migrated core各自拒绝需对应真实eep_core/owner/binding，core失主还要旧core保有本国人口而新bound core属外方，不能误用已空国或source本身无效解释拒绝。

## 归档、partial与最终边界

每个root交接小段原件两次稳定读、逐字节复制、记录绝对原源/大小/SHA与项目canonical映射；已封Machine年末、Mother配置、20源等相同字节只引用，不重复全年解析或Mod复制。新receiver接口来源另绑定真实d4da SHA；旧模板、源工具、原报告不改。失败、重试、缺项、immediate缓存和所有strict差异独立封存。停止后完整日志只能由root明确交接后接收，本阶段不读活动日志。

发布partial对应 `colossus_enemy_fire`、`colossus_cancel_idempotence`、`normal_dismantle_regression`、`colossus_guards`、`common_settlement` 的具体已证check，未证值继续null。common八项需要Machine enemy/normal与Li native损耗/返回分支合并，单enemy数学不能自动全组true。当前不写final-result、不发布、不宣告18组通过；新模板与本页只是准备接口，所有运行结论保持null。
