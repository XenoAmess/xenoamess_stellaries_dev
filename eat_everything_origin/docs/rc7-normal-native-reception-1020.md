# RC7 Machine普通q2拆解接收准备

本次沿当前同一Machine功能分支继续，简体中文、固定run `20261019T164112Z`、RC7 tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`。root报告敌星stable原settlement 25/25已通过、实际May28，账本C21/G21/D7/made300/L2、core物理2人口5177；这些是阶段交接背景，本页尚未获得normal原件，不能作为normal已运行结论。敌星完成包由functional_intake统一封口，本agent仅在其封口后引用，不重复归档。

目标是接收既有owned_q2_setup/inspect后真实planet决议、T5自然Situation完成及重复／实际重载链。当前没有实际eep_reg_owned_source；源ID是未来random结果，不能沿用旧fixture或从八候选预填。只在root明确各role完成、给SAV SHA和白名单后读取原SAV/audit/receipt/UI链；所有未来r7normal*、当前活动r7pkfire、活动日志和UI均不读，不操作Git或Mod/工具。

## 原工具与输入

继续使用原receiver `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`、checker `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`、inspector `1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`、publisher接口 `06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`。复用[已生成的原CLI intake模板](evidence/1019-requirements/rc7-settlement-native-intake-template-1020-v1.json)，不增加矩阵或改工具。原39命令SHA `76adabaf82dc2c10894222bdb425ee1b994307233e1bccb2c251bdf2f07325c8`不变。

role仍用原`native_ui_save`结构：原始save/receipt/audit各绝对path和SHA；若某步真实使用autosave，必须按原接口`native_autosave`及fresh source_mtime/advance-start证据表达，不冒充UI保存。manifest与原SAV同run目录；receipt.archived和audit.save精确匹配原路径。薄包映射另列，不回写原回执。world_ids仅实际core2和实际source的union，每个新role原observe一次，按相同精确键复用缓存。

| 语义role | 预计前缀，仅待交接 | 原生核对重点 | 原工具任务用途 |
| --- | --- | --- | --- |
| normal_ready50 | r7normalready | 实际alias、size2/pc_machine、actor0所有、非core、无损耗、恰50 founder；fixture未改EEP账本 | 决议前完整基线；亦保留迁移独立恢复点 |
| normal_decision_start | r7normalstart | 真实决议输入；source50→100、core−50、总数守恒；seed_existing100/seed_need0、q2、months5、Situation progress0 | 同暂停日seed转移独立核验；不调用settlement代证决议 |
| normal_m01..m04 | r7normalm01等 | 实际日期、target Situation身份与progress、source实际pop/deposits、EEP账本 | 只读真实T5过程；不硬套每个文件名必等于一个自然月 |
| normal_precomplete | r7normalprecomplete | 最后完成前日期／progress、源仍活、持久q2、实际可返回founder groups及核心人口；预先固定other_core_pop_delta依据 | normal结算before |
| normal_immediate | r7normalimmediate | 自然完成首个原生状态、源摧毁/无owner/pop/jobs、一次receipt/账本、真实核心人口 | 与precomplete运行原settlement |
| normal_stable | r7normalstable | 原生回调／后续自然清理已稳定；若immediate不同则原样保留 | 主结算after及重复before |
| normal_duplicate | r7normalduplicate | 原normal_destroyed_source_repeat实际输入和Enter；已毁源重复回调、无新增支付 | stable→duplicate同日原no-settlement |
| normal_reload | r7normalreload等 | 实际Load指向已保存原件SHA，Load后另存新SAV；有重复回调则再核实际输入 | duplicate或stable→真实reload同日原no-settlement；完整strict保留 |

上述名字与前缀只是接收准备，不代表这些文件已存在。根绑定、实际source ID、各date、SHA和每步是否真的保存均等待root交接。单阶段若中断只形成事实partial，不拿空包作证据。

## 结算期望与独立人口依据

沿既有方案，实际setup一次、inspect后暂停保存ready50，再真正点“吞噬：献于唯一王座”；禁止用eep_begin替代UI。相同暂停日应源50→100、核心−50，总人口守恒，真实seed_existing100/seed_need0、q2、months5及Situation progress0分别查原生记录。T5指原Situation周期，完成日期与进度从存档读取，不预填150日。

在root交接账本不变的前提下，q2普通分支预期C21→23、G21→23、D=2+floor(23/4)=7、made=floor(23/6)×100=300、L=floor(23/10)=2。故本次新增制造0、容量新增0，不能按旧C19→21或G跨档套100制造。接收时先核实际ready/precomplete before值；若实际与此背景不同，保留差异并使用真实before重算，不覆盖源变量。

Return只由precomplete实际source可返回founder groups逐组独立求和，species按实际actor founder及修饰模板／purge状态核定；不能硬写100，不能用eep_last_return作期望，也不能从after核心人口残差反推。`expected_other_core_pop_delta`必须在读取自然完成after前由原生时间区间／人口机制和已固定对照独立确定，并把值与依据写入case；不因after不合而调整成残差。若证据不足，保持结算人口项未获支持，先报告缺口，不编造0或新要求。

normal路径的q使用持久eep_q2；precomplete若已有每月bite产生的损耗deposit，不再将该任务自身损耗从持久q重复扣除。判定和case均沿原normal settlement接口，不改checker。危机worlds/empires期望沿已独立校准的750/600输入与真实源原星主／灭国情况；保留既有enemy-ships等其他objective，不将危机总分拟合成拆球奖励。人口项、制造项、capacity项分别验算。

## 薄包与验收边界

只复制明确交接的精确stem（后接`.`或`-`）与操作白名单，避免已发生过的cancel*串入cancelreload问题；原始诊断不得抹去。每段原件双读稳定后绑定，完整UI原图/OCR与实际type_text/物理click/Enter链归档。完成receipt metadata仍只按原授权查同SAV SHA/date来源，不能据回执metadata读取未交接raw。复用已封20source closure、RC7静态Mod和独立危机校准引用，不重复Mod或敌星原件。

原receiver只运行已授权角色的observe和原settlement/no-settlement任务；readiness、真实决议、Situation、seed与实际输入由独立原生及UI证据补充。完整strict差异保留，限域支付不变不等于整个SAV只读。正式结果仍18组原矩阵，未获证据项null/PENDING；非中文运行时不在范围内。

当前交付仅此接收准备文档；normal运行结论、实际角色和源ID均待后续明确交接，未生成normal证据空包或最终PASS。
