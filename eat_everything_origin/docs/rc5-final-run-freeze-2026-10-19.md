# RC5 run143452Z 停止后证据归档

## 目标与范围

固定使用 `20261019T143452Z`／PID33260；root报告UTC `2026-10-19T14:59:47.307906+00:00` 正常停止，forced=false、running_after=false。先核process／stop并独立确认该PID已不存在，再复制全部run artifact原始SAV／receipt／audit／UI／OCR／action／imports，完整停止后logs及全部script_documentation、manifest／process／stop、该run的RC5 source-copy／static gate。RC5 manifest绑定tree `1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52`；当前工作区RC6及后续current-run指针不得替代实际源。

归档目录拟为 `docs/evidence/1019-rc5-final-run/`。r5pautoload／r5preload1失败、r5coreguard1／2相同SAV的受限26/26结果、nchealthbefore／set／load三份原生ordinary corvette→NAME_Relic校准均并列保存。startup Welcome首次中文变成问号而拒绝点击的图／OCR与第二次成功关闭动作均保留，不造不存在的第一次click。等待acceptance线程health三SAV报告封口后复制稳定作者报告；原始run可先冻结。

## 设计与边界

先记录固定完整白名单，再逐文件原字节复制并保存源路径、bytes／SHA256；复制前后核对源／副本与完整集合，独立verify检查SAV／receipt／audit／observer／gamestate、UI图／OCR、manifest与RC5 frozen Mod tree。必要源码从实际candidate-rc5／run复制目录或既有匹配hash canonical取证，不从ROOT当前Mod或更新后工具冒充执行源。runtime84b在RC5 prepare之前已封口，属于本run原工具基线；新的health分析v2工具只列为事后分析源，不回填原RC5执行源码。

完整error／game／debug逐条分类，新增EEP告警与启动baseline分开，unknown、nomads.94历史未解释状态与rootflags marker限制保留。血量校准的机制观察及受限coreguard通过不得外推迁移或全Mod通过。source-copy／gate记录静态结果，RC5最终运行失败并列，不冒充正式发布或实机验收完成。本任务不UI、不启动或停止游戏、不调用Git、不提交、不操作Steam、不改Mod／工具或旧证据。

root补充：prepare未创建独立execution-source目录，只有manifest与实际copied Mod，不得补造。完整RC5源码与gate已在 `docs/evidence/1019-rc5-static/` 原字节封存，复用该canonical并逐文件比对本run copied Mod；同时原样保存外部candidate-rc5 gate／open-kaishek。UI核心runtime84b、single-homeworld、1019、1015、shared harness、audit、inspect与check_1019的本run稳定bytes可与midrun canonical核对，按hash保存为事后源码绑定补充，不能称为prepare时快照或内存证明。间接导入的publish_1019期间曾变化，未调用发布／成长模型验收；不取当前publish冒充历史worker已加载源码，root提供的历史commit d0ce2bc31仅记为交接参考，本任务不调用Git取证。

acceptance已封口7个observer、public autoload/reload FAIL报告、coreguard限定26/26 PASS_SCOPED、health OBSERVATION_WITH_FAILURES报告及两份事前PENDING source方案。health原生ship3由普通corvette改为NAME_Relic并重载后target current/max精确保留；setter三层原1e-6检查仍FAIL，reload的Mother回退导致“其他舰船原样”检查FAIL。talon及旧nrelsrc分支未执行。四处rootflags只证明出现，不能推断design-local marker或通用shared design flag机制。

## 验收标准

确认停止后才归档；全run与logs集合齐全、原字节／SHA一致；实际7份SAV逐一绑定原始receipt／audit及稳定observer／报告；coreguard同SAV等价事实保留；两次Welcome证据完整；执行与事后分析工具边界可追溯；所有失败、受限通过、校准结论和unknown如实记录。生成独立index／verify与日志review，给root完整路径、payload数、hash及限制后停止写入，由root统一checkpoint。

## 已完成结果

UTC15:00:50.2872858独立CIM确认PID33260为ABSENT，晚于正常stop，随后冻结至 `docs/evidence/1019-rc5-final-run/`。共356个payload、24,555,646字节：全run原始303文件、完整19日志共5,881,300字节（含5份script_documentation）、15个稳定分析／source报告、7份方案、3份source-index／gate、9份稳定工具源码hash绑定。完整白名单selection SHA256 `eb2068de100d5568be06db81e158bb62a147ad664cb3c2a858ff8a34f40ed155`；index SHA256 `c13b953ade483aad3185ec8aaa7693e3730768676280710b5aa83cbe978c8d2c`。

独立verify确认356个源／副本、83个canonical引用、63组图片／OCR、5个offline imports与7个原生SAV六方绑定。实际59个copied Mod逐字节与 `1019-rc5-static` 一致，并独立按路径、NUL、raw bytes协议重算得到原RC5 tree1cc8b。verify SHA256 `4899c90576f48edf20b50058876d635aae2b3a539571b0731c8c1374a271e543`；source-binding SHA256 `5603d1fea74a666a7e9fae5927201cc0bbcd1da44e00caacf88e0728f56f73d2`。未运行Git／UI，未伪造prepare执行快照，未读取当前ROOT Mod来替代RC5。

r5pautoload／r5preload1的报告保持FAIL（31/40，9失败）；guard1／2同SAV SHA256 `44ebd953fa66ffb2a891db6e24bbe7a38f57ccb8024699a8de116e6aa120562e`，限定26/26 PASS_SCOPED不含实际重载保证。三份health报告保持OBSERVATION_WITH_FAILURES（36/40）：ship3从原生corvette改为NAME_Relic并实际重载后目标current/max精确保持，setter三层原1e-6检查与重载“其他舰船全部不变”检查仍FAIL（Mother回退另列）。原图、receipt、实际命令和raw SAV全部保存；第一次Welcome拒绝没有click，第二次UTF8 click真实存在。rootflags marker和间接publish依赖来源限制保持，事后v2工具不进入原执行源。

最终error22条均baseline（missing Workshop21、consume override1），game3信息、debug1原生building category警告；具体building对象与影响UNKNOWN。没有新增EEP告警或nomads.94，但历史nomads问题不撤销，不能以日志安静推翻RC5失败。完整review SHA256 `bea617af471c05d8a9c903425c89f76e1d2c2d0874f6d31115cc3eb207869c1b`，另有独立review-verify。全部raw与文档同步完成，证据保存完整性通过，Mod验收仍未通过；交root统一checkpoint后停止写封口目录。
