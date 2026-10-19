# RC6 已完成迁移样本检查点

## 目标与范围

为活动run `20261019T150008Z` 建立独立 `docs/evidence/1019-rc6-migration-checkpoint-v1/`，只冻结已完成迁移样本 r6pautoload、r6preload1、r6prepeatbase、r6prepeat、r6paidauto、r6paidreload1、r6paidrepeat。收集七份原始SAV、receipt／audit、对应实际原生load receipts、稳定UI原图／OCR／actions、source closure与已封口的新v2健康诊断／迁移报告。先向acceptance_analysis核对最终白名单和载入／动作映射，再复制原字节。

## 设计与边界

固定使用显式150008Z路径，不能依赖current-run指针。root独占当前经济UI操作；不操作桌面或游戏，不复制活动logs、不伪造stop、不把活动run称为final freeze。只选择上述完成阶段及经原始receipt／报告证明属于它们的load和动作文件，不能笼统捕获未来r6前缀。完整固定白名单先落selection，再复制并逐源／副本SHA／bytes复核；独立verify重新核对存档、receipt／audit／observer／gamestate／manifest、图片／OCR、工具／source及canonical引用。

从实际run manifest和copied Mod／冻结canonical确定RC6源；工具按报告hash及已确认时间边界保存，只读解析本地依赖，不导入UI／发布模块执行。不把当前磁盘源码自动等同历史worker内存加载源码；prepare缺少执行源码快照时明确声明，新v2健康诊断属于事后分析源，不能回填旧RC5或改写旧v1标准／FAIL。所有旧原始SAV、v1诊断、RC5失败与rootflags marker限制均保留，通过canonical引用并列说明新v2范围。

acceptance确认稳定20份analysis：7个当前样本observer、4个fixture_source／before observer、2个初版PENDING template、公开档partial case／report、公开档complete case／report、paid complete case／report与CLI report。公开完整174/174和paid158/158都仅PASS_SCOPED，嵌套原v1仍FAIL；旧模板与partial PENDING代表已完成的历史诊断文件，不能当作未来样本或完整通过。工具为 `check_migration_1019.py` SHA256 `08b57969060c037c4e03829f0075f8e7314f262527215e991595bd4778456d38`，旧check_1019保持681836d2…；新15项加旧17项测试结果由合同记录，归档只保存既有结果与测试源，不重跑UI或测试。

五份实际载入回执为 r6pautoload／r6preload1／r6paidauto／r6paidreload1各 `-native-load2.load.json`，以及 `r6-public-repeat-load.load.json`。公开重复前另有一次显式返回r6pautoload的真实load，随后r6prepeatbase→r6prepeat要求精确0差异；paid重复直接r6paidreload1→r6paidrepeat。保存七个明确的ctrl+a文件、7阶段前缀、额外public-repeat-load与已完成rc6-load-menu-retry原始动作／帧；排除r6pu及一切经济分支，不据整个r6前缀收集。

源码分为可完整AST解析的纯离线v2分析依赖闭包及9份已知稳定UI核心hash绑定；不跟随运行／导入UI。UI间接publish依赖期间在独立发布任务中变化，不冒充历史worker源码闭包。RC6实际tree为 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`、game PID30812，完整Mod已在 `1019-rc6-static`；复用canonical并与本run实际59文件逐byte核对。活动进程无需停止，也不保存任何日志终态证明。

acceptance最后交付另有 `rc6-migration-v2-delivery-v1.json`（SHA256 `a2018ed215f10cb88877e8b7a368e4ca641747f7e536db1d2413f572a9e0f129`），在上述20JSON之外独立保存其20文件／工具／test／doc完整hash清单。合同与新 `rc6-migration-v2-evidence-mapping-1019.md` 已封口，分别SHA256 `55767fe4155b2707531976bd9f02effa2a3772a2726d5ba012cfe586644faa62` 与 `3b986430de4070c8493725e85fa9dd03ac85223ef56f1ce8b30545a258aa8330`；现在可按固定选择复制。

## 验收标准

七份完成样本齐全且只覆盖授权阶段；原生载入链与动作证据可追溯，所有原始payload保持字节与SHA；源代码与分析工具版本可核；七SAV与报告引用一致；不得包含活动日志、经济测试或后续未完成阶段。记录限定通过／失败、旧v1失败与新v2诊断的区别，不外推全Mod验收或发布完成。完成后输出路径、完整selection、payload数及独立verify结果，交root统一checkpoint，不commit／push。

## 已完成结果

检查点 `docs/evidence/1019-rc6-migration-checkpoint-v1/` 已冻结330个payload、21,050,052字节：run固定白名单291文件、analysis21、合同／映射2、工具源13、source-index／gate3。selection SHA256 `43f88eb35f9961ac0a198b50a7a366bd0aa972b9c21e9aab6035118d0beb018b`；index SHA256 `9bd49ca3bfdf1e13da6175833390384ac90a430ad67a4d9a38ef9a97eaf7438d`；独立verify SHA256 `6de924841b76c247c4cc73a199fd1e40fd72e8caf0a4a911f6ab34ec4a7a4171`。

独立复核全部源／副本、148个canonical引用、7份原生SAV六方绑定、5个实际load、60组图／OCR、7固定ctrl+a、5个offline imports，以及59个actual copied Mod与冻结canonical，并重算得到原RC6 treecc181c8a…。源码／test的纯离线AST本地闭包8文件、UI9份hash绑定共13个唯一源码；交付表24文件逐项hash一致，旧v1 checker681836d2…保持原SHA。未读取活动logs、未收经济r6pu、未伪造stop或调用UI／Git／新测试；runtime历史内存源码仍无独立证明。

公开完整174/174、paid完整／CLI158/158均仅预先声明v2合同的PASS_SCOPED，嵌套原v1 FAIL与旧RC5 FAIL原样保存。public另一次真实return load在case／receipt／预算中明确列出；随后repeatbase→repeat与paid reload→repeat均同SAV SHA、精确0差异。每步有符号比例预算 `[-0.000021,+0.000001]`，独立用报告raw readings复算仍在合同内；该复算是报告读数算术核验，不冒充另一轮原生运行。既有template／partial PENDING、associated mobile-starbase实现未认证、rootflags非design marker证明等边界保持。检查点证据绑定通过，完整Mod验收没有据此改为通过。

root另交接25份作者任务文件（含delivery自身）已提交推送b9fe425a6，旧RC5归档／baseline在ef823de0d；这里只记录交接事实，未调用Git查验或更改这些提交。本新检查点交root与release_pipeline引用后停止写封口目录。
