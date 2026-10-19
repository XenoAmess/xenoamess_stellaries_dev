# 旧 public031 受伤夹具运行的停止后归档方案

## 目标、范围与当前状态

本文先记录方案，现已在 root 正常退出信号后执行。准备时 run `20261019T130448Z`／PID5216 仍用于 EEP05 编辑器调查，因此当时没有复制活动日志；退出后才独立检查并冻结。不操作 UI／游戏／Steam，不修改工具、Mod、SAV 或提交。

同 run 原始 manifest 确认实际运行的唯一 Mod 为 public0.3.1，47文件 tree SHA256 `abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8`，语言简中，EXE SHA256 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。userdir 为 `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T130448Z`；artifact 来源为 `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-legacy-damage\runs\20261019T130448Z`。不得与 root 后续 RC4 迁移 run 或此前 RC4 phase-A 拼接。

停止后拟归档到 `docs/evidence/1019-legacy-damage-run-final/`，包含：全部 logs／script_documentation、manifest／process／stop；下述7份真正成功的原生 SAV 及其 native-save／audit；同 run 相关原生载入、施伤、保存、严格 OCR 失败／重试、别名与 EEP05 调查的截图／OCR／actions／receipts；下述独立分析白名单。只从本 run 及已确认的稳定分析来源取证，不抓取其它 branch 的未完成文件。

## 已确认 canonical 来源，避免重复 Mod

准备包准确路径为 [1019-analysis/legacy-damage-preparation-v1](evidence/1019-analysis/legacy-damage-preparation-v1/)，不是 evidence 直属同名目录。已和 acceptance_analysis 对齐并只读核对：

| canonical 文件 | SHA256 |
| --- | --- |
| `archive-index-v1.json` | `f8d13956ba987b12d6c0f676862b1d05f1614202d5f645e2a118a6be8053d1b1` |
| `archive-verification-v1.json` | `ccc8bf2ad99c337bef59386b7285823d2a503feeb10b51cd9ed1c003b63afcb3` |
| `public031-profile.json` | `6dff682ae7634e3a7bc0030a38aaf01721757e76f97ed9dac67c2356b3451d9e` |
| `public031-gate.json` | `9c7fb1f7937d5101d85cf84460a108fe3853cf3ae14b3a5175a045fcef53c7d3` |
| `public031-open-kaishek.json` | `46b24c5320556463031e026f1535e529c794f29249ac7a0edbabfd3f34ca1681` |

该包只证明 static preparation／来源字节绑定，原状态与64文件索引不改。本次运行归档仅引用其47文件 Mod、原始基线及工具／原生目录，不再复制 public031 Mod 树；独立复核时重新核其 canonical 文件 hash。

## 七份成功原生 SAV 白名单

这些 SHA 已与各自 `*.native-save.json` 核对；正式归档时仍须重读 SAV／audit／receipt 一致性。没有 `ld031armor`，不得创建不存在的阶段或以别名凑成更多原生保存。

| 原生阶段 | 日期 | SHA256 |
| --- | --- | --- |
| ld031clean | 2200.01.01 | `7dcff806a7f6c20cd9a2a607c646f2d96ec2b31d07f88ebbaa5fc9086d6838fd` |
| ld031hurt | 2200.01.01 | `f2d2742aa321b43ec153aa56fd210bce5f3c3828518e4fc63be3987d37f18ebd` |
| ldpaidclean | 2200.01.12 | `5290bdd14f078a5b3b75902bb9231a94dce793ae8363e65066a5e235cd7f2360` |
| ldpaidhurt | 2200.01.12 | `fa0bceedd33ef8957bf200d8ccd97cdde23cbf2e43f2984099f891ae22eb21a0` |
| ldpaidarmor | 2200.01.12 | `4391254b50c1e1fabe975dbcaf9bf30caf0d17ece14bb8d8e9ff8b2c63c67373` |
| p031before | 2200.01.01 | `d5921823d723d4eb0dec5d912ae0e586aac5b903643472d44062229b66b0b1e2` |
| ppaidbefore | 2200.01.12 | `40c8f8dac9530594d501143132d55fef1205346d7f679f16c8858058ed392ff1` |

`partial-source-aliases.json` 已明确 `src031hurt` 是 ld031hurt 原字节别名，`srcpaidarmor` 是 ldpaidarmor 原字节别名，仅为严格 OCR 恢复原生列表识别；正式归档核对 alias／original 实际 hash 并保存 receipt、load动作和截图，不称新生成 SAV。generic ld031hurt 严格 OCR 失败及其截图／回执必须保留，不能只留成功别名重试。

## 来源年代与施伤版本分开

`legacy-import-receipt.json` 与原生 load receipt 明确：空队列原件 `bmm00` 来源于 public0.3.1 run `20261019T053917Z`，SHA `af5f64e2eaadb164e87796d2a9261ac97ef7d716cc3f8b3cec5f4a2f23f787f8`；十一件已付款队列原件 `j13ten` 来源于 `20261014T223819Z`，SHA `834ea5325f93e3d3e92a44aabccd87195564cd4f1292d4439ae865eba5af8d2e`，其原始 provenance 为 **0.3.0-rc.1**。

两原件都在本次 **public0.3.1** profile 原生载入后保存、施伤和建立最终 partial fixture。因此“paid 来源旧档0.3.0-rc.1”“本次施伤运行0.3.1”必须同时保留，不能把 j13ten 改写成原本由0.3.1生成，也不能说本次施伤在0.3.0执行。原件使用 canonical 准备包引用，不重复复制一份并改变来源标签。

## 独立分析白名单与状态保持

稳定源均在 `docs/evidence/1019-analysis/`，由 acceptance_analysis 独占维护；本线程只能原字节复制稳定白名单，不改报告内容或替换历史失败：

- `legacy-ld031-clean-hurt-report-v1.json`：FAIL22／23，装甲未伤，SHA `073fa4b55beda161834c8d7e0b05f72554d8153b338f91593130de90187636ad`。
- `legacy-ldpaid-clean-hurt-report-v1.json`：FAIL27／28，装甲前提未达，SHA `c7ebfffb325e8a1b3440d1cebb056b1a96a40fab7ea11e3d7f23f23eed3ea165`。
- `legacy-ldpaid-hurt-armor-report-v1.json`：OBSERVATION_ONLY，真实护盾耗尽后装甲受伤；原始省略 shield current 不擅自补成0，SHA `fa187ccc538186fa4654e6017ed5988cfd11e9851eccd9fe23688632b2e6bbb0`。
- `legacy-p031before-partial-fixture-report-v1.json`：PASS_SCOPED28，最终三层均正值且部分受伤，SHA `5717450af2ca81b7cf109f974b6c5b3cbb8518e7feb00578df6259bd8336716d`。
- `legacy-ppaidbefore-partial-fixture-report-v1.json`：PASS_SCOPED29，最终三层部分受伤且原十一件已付款队列保持，SHA `c9cce79af4c051bb5655a2a0b931f9f27223dea70f717abc5d66c4f180291c5e`。
- 对应七份 `legacy-<阶段>-observation-v1.json`，阶段严格采用上表白名单。
- `legacy-public031-fraction-migration-case-template-v2.json`／`legacy-paid-fraction-migration-case-template-v2.json` 只作方案／before 绑定；load／sync／reload 仍为 null，不能包装成迁移结果。

最终两个 partial fixture 的所有队列／资源检查及严格差异（public26、paid20）按原报告保留，不删除未解释变化，不把夹具合格等同 RC4 迁移已通过。

## 收到正常 stop 后的归档与验收

1. 收到 root 明确正常退出信号后，读取同 run stop：PID5216、实际UTC、`forced=false`／`running_after=false`；与 manifest／process 的 EXE、启动时间、userdir、单 public031 profile 和 tree 核对。独立确认该源进程已停；未确认前不复制 logs。
2. 停止后枚举完整 userdir logs，包含全部 script_documentation；枚举同 run artifact 中相关 UI／actions／OCR／native receipts／audits／load／wait／失败／重试记录，按实际存在文件形成白名单。原生 SAV 严格只收上表7件。EEP05 编辑器调查若在此 run 完成，其相关原始证据作为独立子范围保留，不混成施伤成功证明。
3. 原字节复制上述载荷及稳定分析白名单；复制前后对源集合、每个源与副本字节数／SHA256逐一核对，源发生变化即不宣称 frozen。记录每个原始路径、目标路径、类型、复制UTC，保持 alias关系与 canonical引用。
4. 生成独立 index 与复核：重新读取所有原件／副本、停止证明、7份 SAV／native receipt／audit、截图／OCR／动作绑定、分析原件、canonical引用，并证明没有重复 Mod 树、缺失7阶段或虚构ld031armor。原始载荷设 `-text` 并核 prospective Git blob 原字节，保留独立 verify，不以复制命令返回成功替代验收。
5. 完整审阅 final error／game，必要时 debug；所有启动 baseline、试验输入、EEP05相关提示和未知错误逐项保留。不能因原生来源或准备包通过就判日志无害，也不能以没有错误替代三层受伤／资源／队列或未来迁移的实际检查。
6. 输出范围严格为旧 public031 夹具运行冻结与 provenance。root 可在其它独立 RC4 run 继续迁移／经济／成长，本线程只进行文件和 CPU 只读复核，绝不控制桌面、游戏或Steam，不提交。

## 收到停止信号与 EEP05 新事实

root 已确认 PID5216 于 UTC `2026-10-19T13:32:28.045820+00:00` 正常退出，stop 的 `forced=false`／`running_after=false`，独立 CIM 查询为 ABSENT。现在按上述方案执行停止后归档；停止由 root 完成，本线程不控制游戏。

归档新增明确白名单：run 内 `eep05-picker`／`eep05-edit-design`／`eep05-editor-unmodified`／`eep05-completion-hover-basis`／`eep05-error-tooltip` 及其相关原动作、截图、OCR。UTC13:31:41.469198的真实 tooltip 图和 OCR 都显示“统治者外观：统治者性别未选定。”，因此旧 EEP05 的缺失性别原因已有原生 UI 证据，不再仅为静态候选。

同时收录 `docs/evidence/1019-eep05-design/fixture-before-gender-repair.txt`／`fixture-after-gender-repair.txt`／`fixture-gender-repair-v1.json` 三份既有原字节修复证据；只读核对 before SHA `b3cee1d3c3475ea6fa9b54cc09eb0f75e848f565a02326bf70c59db0c9ed0e90`、after SHA `4ce9d9217a7ed804776a41e8ac73410bd70d5073bc3379aa55c2c46181938646`，只改变 EEP05.ruler.gender `not_set`→`female`。本次旧 userdir 的实际预设仍为 before／b3cee；新 candidate 使用 after／4ce9，不把仓库候选修复倒填为旧运行输入。仅此静态单字段修复尚未证明新的 RC4 原生选择／开局通过。

## 最终归档结果

已完成 [完整归档](evidence/1019-legacy-damage-run-final/README.md)：418原文件、27,252,632字节，[index](evidence/1019-legacy-damage-run-final/index.json) SHA256 `f78fab26099320e7306995a19d25e181b858db520ce63954295efdf7c2833208`。完整19日志／5脚本文档、三运行证明、七SAV、全部同run相关原始图／OCR／动作／回执、14分析与EEP05修复证据均按原字节保存；不重复47文件Mod树。独立 [verify](evidence/1019-legacy-damage-run-final/verify.json) 重读418原件／副本、5canonical引用、7组SAV／receipt／audit／gamestate、82图／OCR绑定及两个raw alias，全部核对一致；418文件另通过Git原字节校验。

最终error23行、game3行、debug1行完整分类，均有baseline对应；建筑类别对象仍未识别，不称无害。generic ld031hurt的失败stage为ld031-hurt-reload，OCR本身成功读出capital I的`Id031hurt`，失败的是调用方目标标签匹配；失败图／OCR／动作保留，没有成功load receipt，也没有伪造worker异常JSON。其后alias恢复不产生额外保存阶段，ld031armor不存在。

原始FAIL／OBSERVATION／最终partial限定PASS和strict26／20差异原样保留；实际EEP05性别提示已确认，候选修复的新RC4实机仍PENDING。分析见 [review](evidence/1019-legacy-damage-run-final/review.json)，源码／原件来源及状态边界齐全。旧run用户预设b3cee未改，未来新candidate4ce9另列；未操作UI／游戏／Steam、未改Mod／工具／SAV或提交。文件稳定后交主线程统一checkpoint。
