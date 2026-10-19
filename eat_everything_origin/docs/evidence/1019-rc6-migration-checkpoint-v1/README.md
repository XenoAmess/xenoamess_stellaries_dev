# RC6 已完成迁移检查点

仅覆盖run `20261019T150008Z` 中已完成的7个迁移样本。活动日志、经济分支r6pu、后续样本及stop证明均未读取或收集；这不是最终run冻结或全Mod验收。

完整白名单为 `selection.json`：330个原字节payload、21,050,052字节，含291个固定run文件、21个稳定分析／交付JSON、2份合同／映射、13份工具源及3份静态source-index／gate。index SHA256 `9bd49ca3bfdf1e13da6175833390384ac90a430ad67a4d9a38ef9a97eaf7438d`；独立verify SHA256 `6de924841b76c247c4cc73a199fd1e40fd72e8caf0a4a911f6ab34ec4a7a4171`。

`verify.json`逐一复核330源／副本、148个canonical引用、实际59个copied Mod（独立重算tree `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`）、7SAV六方绑定、5份原生load、60组图片／OCR、7个固定ctrl+a及5个offline imports。load原回执的 `state_verified=false` 保持不变，后续SAV审计单独提供游戏状态证据。

七样本为r6pautoload、r6preload1、r6prepeatbase、r6prepeat、r6paidauto、r6paidreload1、r6paidrepeat。公开重复对r6prepeatbase／r6prepeat同SAV SHA256 `edcd11a54b2926254206bd86e920b6f9af9af9b45ef0ca94c947b5fec0dcb09e`；paid reload／repeat同SAV SHA256 `bedebd4ad6911f16b4fb57a1ead239afc650d3dedd730833c10c902a7466e5d7`。公开另一次返回r6pautoload的真实载入已显式保存、单独计入预算，没有把隐藏load并入精确重复对。

| 已封口诊断 | 结果 | 原v1诊断 |
|---|---|---|
| public031完整v2 | PASS_SCOPED，174/174 | FAIL保留 |
| paid11完整v2及独立CLI | PASS_SCOPED，158/158 | FAIL保留 |
| 初版两template及public partial | 历史PENDING保留 | 未改写 |

v2只适用预先声明的固定EXE／RC6tree、简中单人postload repair及真实受伤夹具。每次真实load的有符号比例变化预算为 `[-0.000021, +0.000001]`；全部非精度不变量、实际设计／六核心、队列、账本与重复精确0差异要求保持。独立复核另用报告raw readings重算各步预算，不能称数学无损迁移。attached mobile-starbase实现仍只是原始观察，root flags出现不证明design-local marker。旧v1工具SHA `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`、RC5原FAIL和原SAV均未改。

离线v2分析／测试的AST本地Python闭包完整8文件，UI核心9份另以此前canonical绑定，合计13份唯一源码。v2工具SHA `08b57969060c037c4e03829f0075f8e7314f262527215e991595bd4778456d38`。没有声称prepare时存在执行源码快照或进程内存loaded-source证明；变化中的间接UI publish依赖没有冒充历史worker源码。交付清单的24份稳定文件逐项核对，交付表中的历史checkpoint待办状态保持原字节，实际完成结果由本index／verify表达。没有调用UI、Git或重新运行游戏／测试。
