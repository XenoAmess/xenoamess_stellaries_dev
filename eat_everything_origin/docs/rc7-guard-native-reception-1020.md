# RC7四支guard原生接收准备

依据已封口[guard最短执行卡](rc7-guard-minimal-execution-card-1020.md)准备A/B/C/D四支独立薄包。本页只定义接收与验收接口，不读取当前normal、未来guard或活动日志，不操作UI/Git，不新增Mod、工具、fixture或矩阵。只有root逐支明确完成并交付精确白名单、SAV SHA后，才开始读取该支原件；当前所有guard运行结论仍PENDING。

固定中文run `20261019T164112Z`、RC7 tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`、EXE `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。实际root若另明确run或角色来源，必须显式绑定相应manifest，不把旧O/M的历史run、数字ID、C19等带入。原checker 681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc、inspector 1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92、receiver d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5、publisher接口06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918保持原字节。

## 目标、范围与包结构

每支只归档root交接的ready R、idle I、fired F三档及构造／真实Load／实际dispatch／等量自然推进的必要原UI和输入链，三个角色可复用真实同一SAV而不额外保存。建议目的目录分别为`evidence/1019-rc7-guard-a-v1`、`-b-v1`、`-c-v1`、`-d-v1`，只有收到真实闭合资料才创建。原case、命令、v2静态包、20source closure、Mod、已封经济／PK／normal来源只canonical引用，不重复复制。

每支一份原receiver intake：world_ids为该支所有实际source与实际EEP bound core的物理ID union，每个R/I/F各observe一次。然后每个目标建原`no-settlement`任务，before=该支I、after=该支F，只填实际source_world/core_world。完整strict与所有原错误保留，不改checker、不删路径、不将跨日R→F当同日对照。若原工具因缺失容量等真实状态拒绝，保留原FAIL／错误，先判实际前提是否建立，不能静默补字段。

## 精确角色及读取规则

| 支路／角色 | root需明确的实际来源 | 该role的用途 |
| --- | --- | --- |
| A ready/idle/fired | 从真实Load已封r7pkbase构造出的三档 | 九持久源＋当前bound core共享；不是每球三档 |
| B ready/idle/fired | 再次独立真实Load r7pkbase，实际殖民中／地战／外国secondary状态构造后的三档 | 三目标状态能持续才共享；不能沿A占满home的状态继续 |
| C ready/idle/fired | 实际Load成功normalready2后，真实迁移决议已完成的新bound core三档 | normalready2只复用为迁移前来源；失败normalready不能代替 |
| D ready/idle/fired | C迁移成立后，当前新core真实转交活receiver且旧core仍是本国普通殖民地的三档 | 实际EEP core是外国new core；dispatch source是旧core |

R证明无效状态已建立；I是R上仅自然推进1日后的实际保存；F是**真正Load同一个R**、实际派发本支回调后推进同样1日的保存。R和Load回执必须精确绑定同一原SAV SHA；F必须是Load后新保存的实际结果，不能拿Load输入冒充。只比较I/F实际date相同的状态；若root不得不增加构造tick，按真实R重新定义I/F，不能沿文件名假设日期。

每个role必须有原save/audit/native-save（或真实autosave合同）绝对path/SHA，原manifest与SAV共目录，receipt.archived与audit.save精确指该原SAV/date/SHA。原件双读稳定；JSON缺失、变化、未封口或来源不符即原样失败并等root明确，不吞错。只读已授权精确stem后接`.`或`-`及明确操作白名单，不用宽前缀吸入未交接的reload／后续支路；封口后不追加新raw。

原provenance查找仍仅按root既有授权读取固定run已完成的`*.native-save.json`与`*-receipt.json`元数据作同SAV SHA/date来源查找，不据此读取未交接raw。记录前后元数据SHA及新增完成对象，已有对象必须不变。canonical引用需SHA真实闭合；尚未封口的normal或其他agent包不读取或引用虚构索引。

## A：十个目标的共享接收

R/I/F实际必须绑定九个不同type=planet的guard源，且与另一个实际EEP bound core身份分清。七批源均有真实colony和人口，各自active、being_devoured、credit_done、destroy_done、secondary eep_core、人工类型、size2加两个真实lithoid devastation等状态在三档持续。人工以原生class／人工属性为证，qzero以真实deposit实体计数为证，不用同名flag或eep_q写值替代。

home外uncolonized须真实无colony/owner/殖民过程、自然digestible且不同于七批；neutral须实际活default非actor自然首都、未与actor交战，且非core/active/settled。执行V优先覆盖O/M的单一片段，实际输入逐字核对；尤其uncolonized bind和dispatch都必须用v2，只有bind成功而旧dispatch停在NOT_READY不能判拒绝。

F的实际dispatch链为batch_dispatch、uncolonized_dispatch v2、neutral_dispatch、current_bound_core_reject。分别核THIS为各实际物理源、FROM为实际唯一Mother。为九源各建一个I/F no-settlement，当前bound core另建一个，合计10任务。当前核心任务source_world可以等于core_world，原负例函数允许；不套positive settlement的source≠core条件。每个目标均独立核存在／状态持续／确实回调，不能只用总账零差证明十项。

## B：殖民中、地战与外国secondary

殖民中对象必须有实际原生colonizing状态、进度/species/owner等对象证据；同时如实记录is_colony。is_colony=no时只支持真实“殖民中联合拒绝”，不声称隔离了单一谓词。仅start_colony输入或命名flag不能证明状态已建立。

地战须实际ground_combat及双方关联army对象，actor为攻击方、原星主为守方、目标与战争身份正确。army成员的实际键以本SAV为准（已知colony ID与物理planet ID要分清），不能用创建军队、驻扎或占领代替正在战斗。R/I/F均须保持该状态；若I已结束，则保留夹具未建立的partial，不给ground guard PASS，也不把本支军队混入有效PK的无陆军结论。

若按卡合并外国secondary，它须在B-R前已实际转交仍活且正与actor交战的victim，持久eep_core仍在；生产bound core另有本国可用对象。B-R/I/F都核同一外国owner及标记，不把转手前后owner变化塞进对照。三目标成立时共用三档、各1个I/F任务，共3任务；若root明确未合并，则只接实际两目标，外国core另有真实独立三档才能补支持，不能造空角色。

## C与D：迁移和失主

C迁移前引用成功normalready2的已封canonical（卡给May28、source1/colony18/pop50、core2/colony0/pop5177，只作为历史来源提示，不在本准备阶段预读或硬写未来ID）。实际迁移必须有原UI决议、old/new物理别名、旧core仍有人且变普通、新core标记/deposit/容量／生产绑定及原生capital分别查证。C-R/I/F均保持迁移成功，新bound core为source和core，建1个I/F任务。

D在实际转手后R/I/F核：receiver活且非actor；EEP绑定仍为外国new core；旧core仍owner0且population>0、无EEP core标记；actor initialized与Mother仍在、core_available=no。真实capital是否自动选回旧core另记，不能当EEP重绑。dispatch THIS是旧core这个普通本国源，FROM为Mother；no-settlement的source_world填实际旧core、core_world填实际外国new core，建1任务。如果生产binding丢失／重绑／无效状态不持续，先保留原事实，不能仅因无收益判完成时core owner重校验成功。

## 补充不变量、实际输入与验收

原no-settlement顶层直接覆盖同日／tree、五账本C/G/D/made/worlds、core实际人口/容量、源class/colony/once receipts、危机raw，并附完整strict。另独立核last-return/manufactured/capacity、L/next、组件B/R/P与六country/fleet tiers、唯一growth modifier均I/F不增加，保留完整原生值；不预填某支都应为零。worlds/empires命名objective分别读progress及present状态，其他原生危机变化照实记录；若原函数因任何实际差异FAIL，保留FAIL，不用“不是EEP”删掉它。

实际输入用原O/M/V文件SHA和id回溯，V相同id优先；typed action和物理Enter须完整，NOT_READY/MISSING不当dispatch。root主动日志摘录明确为诊断摘录，最终停机完整日志由最终归档另处理；不读活动日志。原图/OCR绑定图SHA/PID/date，纯UI文字不替代原生owner／colony／combat。

每支独立index、原件复制来源清单、原receiver报告/缓存、源状态及增长不变量补充、限定部分提案、独立字节／引用／ZIP／role／实际Load／I-F日期／图OCR复核和README闭合。已有source与其他已封包只引用。A/B/C/D四组三档足够，不增加逐球保存或新进程。

只有实际无效前提持续、THIS/FROM正确、回调确实派发、源未毁且原生无收益时，才分别提案colossus_guards对应项。all_core_worlds需要A本国secondary／当前bound、B外国secondary及C迁移bound共同证据；completion_revalidates_core_owner由D实际失主状态支持。unlimited.invalid_or_cancelled_no_growth中invalid半支须这些实际growth不变量，与既有取消半支分别映射；不足仍null/PENDING，不由一支顶替全部守卫或整项。当前不创建任何运行报告或最终PASS。

准备时已复核执行卡SHA `e46e1b359ef6bcba3caea9bfca902ab8595124a44f6cf1ad36def373f58bf8b6`；原四接口及O/M/V三命令资产的七个既有SHA均匹配。产物仅本文，没有创建未来包、intake角色或运行报告；等待逐支实际白名单。
