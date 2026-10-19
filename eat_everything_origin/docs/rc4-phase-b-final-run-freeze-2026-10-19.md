# RC4 phase-B run133314Z 停止后归档

## 目标与范围

root已通知固定run `20261019T133314Z`／PID36912于UTC `2026-10-19T14:34:31.898945+00:00` 正常停止，`forced=false`、`running_after=false`。先读取该run的process／stop并独立查询该PID身份；确认原Stellaris进程已经停止后，才复制整个logs目录及其全部script_documentation。后续current-run指针与RC5启动均不作为源，始终使用显式133314Z路径。

本轮新增 `docs/evidence/1019-rc4-phase-b-final-run/`，冻结全部停止后logs、manifest／process／stop、rsizeonly的一份原生SAV及完整UI／OCR／action／audit／native-save receipt、nrel导入receipt及全部已产生的载入／HUD失败／两次play0 guard拒绝／直接观察探针。复制稳定的rsizeonly observer／check报告、nrel source只读报告与对应设计文档。已归档phase-B migration checkpoint（11SAV、462payload）和midrun capture-tool supplement（18源码闭包及旧新runtime）仅引用其稳定index／verify，不重复巨量payload或59文件Mod树。

## 设计与边界

先列完整固定白名单，保存原字节、逐文件bytes／SHA256及源路径，复制前后分别复核；独立verify重新核对全部归档文件、完整logs集合、process／stop、SAV与receipt／audit／observer绑定、图片与OCR哈希，以及canonical引用。另用Git属性保证raw payload不经文本换行转换。此归档不执行UI、不导入工具模块、不操作Steam、不改生产代码、不改旧日志／receipt／source-copy，也不提交。

完整error／game／debug必须全部审阅并分类：原生启动baseline missing Workshop、consume_decision override、portrait_container等与已知手输／作用域错误分开；任何新EEP错误、未解释的内容均原样保留，不能静默过滤。nomads.94如本run出现须保留原文并与既有未解决问题联系，不能因原版callback也出现而称无害。

rsizeonly按实际报告保留FAIL；nrel载入helper在日期HUD校验异常，未执行施伤／save／export。play0的两次worker都在console-visible guard拒绝，未输入命令。不存在的nrelbefore／nrelset／nrelload或成功load receipt不得补造。工具补充与Modtree仍RC4的关系保持原记录，工作区RC5没有加载到此run。

## 验收标准

独立确认原game PID已停止；停止后日志完整集合逐byte／SHA一致；新增SAV唯一且完整绑定原生receipt、audit、observer；所有图／OCR成对绑定；原始失败与unknown分类可追溯；旧canonical与中途工具边界不被回填改写。验收只覆盖证据保存完整性，不能把静态通过、工具基准或无日志错误外推为迁移／成长／全Mod通过。结果与精确payload白名单写回本页，由root统一checkpoint。

## 已完成结果

独立CIM于UTC14:38:21.7252063查询PID36912为ABSENT，晚于正常stop，随后复制。归档 `docs/evidence/1019-rc4-phase-b-final-run/` 共108个payload、10,488,569字节，完整白名单 `selection.json`（SHA256 `efcb6d4087c4aa7dc1f3d17e8150541d367d06ab3a3f073d4b58b26a07cb5f91`）；index SHA256 `c5bd429ccf088a36e41a6f9be43fb1122312ebc56c25cb6ae2f5d95d297d3227`。

白名单包括全部19日志（5份script_documentation，共5,886,575字节）、manifest／process／stop各1、rsizeonly38文件、nrel40文件、增量press动作1、稳定分析4、方案快照3。唯一新增SAV是rsizeonly，原生日期2200.01.12，SHA256 `715a8a4d168052ac06cb8867b0394ecac757c6bfd5b189bcf606dbc2b7e66678`；SAV／receipt／audit／observer／manifest／gamestate六者绑定通过。独立verify还核对19个canonical引用、18组图片／OCR、全部源／副本与Git原字节属性；只调用只读hash-object／check-attr，不写Git index、不stage／commit／push。

最终error为39行／39记录：21条baseline missing Workshop、1条consume override、17条EEP变量未设置运行时告警，Machine组21:37:54计12条、Hive组21:46:01计5条。17条不得归入baseline；原始stack定位eep_mothership_effects，执行期变量解析原因仍UNKNOWN。error原字节恰与先前有界只读warning snapshot一致，并不证明后续UI探针通过。game为3条版本／defines信息；debug为1条baseline原生building category警告，具体对象和影响未解释；本run没有portrait_container和nomads.94，历史nomads问题不撤销。完整review SHA256 `fa33a2a66e6c71851b805dcfa6135965b3f303c1c5357346892f91689b7f2192`，另有独立review-verify。

rsizeonly报告4项FAIL原样保留。nrel source-import-only、HUD日期guard失败、无施伤／save／export、两次play0 guard未输入命令均按root交接与实际文件现况记录，直接探针原图／OCR／动作完整保存。不存在的nrelbefore／set／load没有补造。工作区RC5与后续run没有混入；既有phase-B、midrun supplement及canonical源未覆盖。证据保存完整性复核通过，Mod验收仍未通过。
