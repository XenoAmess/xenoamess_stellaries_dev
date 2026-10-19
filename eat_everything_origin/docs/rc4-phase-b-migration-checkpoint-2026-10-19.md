# RC4 phase-B 迁移探针原始检查点归档

## 目标、范围与验收

只读归档仍在运行的 run `20261019T133314Z` 已稳定的指定阶段，完整保留 FAIL 与未知差异。此为原始阶段检查点，不是最终 run 日志冻结或迁移验收完成；不操作 UI／游戏／Steam，不修改工具／生产 Mod／SAV，不提交。

范围为 m031load／sync／reload、mpaidload／sync／reload、rdesignsync／reload、rnamesync／rnameload、rfleetsync，共11份成功原生 SAV 与对应 UI／OCR／action／load／save／audit，公开／paid 导入 receipt、原始 source／gate／manifest 和独立 observer／case／check／raw-source 报告。排除当前正在执行的 rsizeonly、之后的其它探针、stop 证明与整个活动 logs 目录。源 run PID36912，简中，tree `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`。

UI动作范围按精确阶段前缀锁定；无前缀 `press-*` 仅收UTC不晚于 rfleetsync-close-menu 的 `2026-10-19T14:07:39.920141+00:00`，随后新增无关文件不并入。完整逐文件白名单先落文件，再复制；复制前后验证这些已选文件的 bytes／SHA256 与副本一致，不要求活动 run 的其它文件集合停止增长。

## 来源复用与版本边界

旧 public031 夹具使用已提交 `docs/evidence/1019-legacy-damage-run-final/` 的418文件归档及其 index／verify／七SAV，按导入receipt核对 p031before／ppaidbefore→mig031src／migpaidsrc 原字节绑定，避免重复旧UI／Mod大归档。paid原始队列j13ten来自0.3.0-rc.1，本次受伤before生成于public0.3.1；后续本检查点运行的是RC4，三层来源不合并。

RC4源码／门禁复用 `docs/evidence/1019-rc4-pk2-duration/archive-index-v3.json` 及 `source_snapshot/`。本包收录小型原始 source-copy／gate／open-kaishek 和当前 manifest／process，并引用既有59文件canonical Mod树，不再复制其它run的全部证据。candidate-phase-b-imports.json 中其它重启／取消导入如出现，保留完整原receipt，未列阶段不据此宣告验收。

## 实施及独立复核设计

1. 对当前源manifest、11SAV与各自native-save／audit、稳定action／OCR、分析报告建立完整明细白名单，记录每个来源路径、目标路径、类型、bytes和SHA256；明确不包含rsizeonly／活动logs／stop。
2. 按原字节复制白名单；逐项重读源和副本，确认原件未变、副本一致。原生SAV与receipt／audit的save／gamestate hashes须匹配；有效OCR的image／PID绑定独立核对，失败截图和调用方失败证据不删除。
3. 所有check／observer／raw-source／case报告保持作者原状态；FAIL、历史v1与v2更正、strict全部差异原样保留。只读归档不修改预期、不重跑工具以覆盖报告、不以文件完整视为功能通过。
4. 引用旧来源、RC4 canonical tree与导入alias关系逐hash重读；独立验证报告和原始bytes索引分开。原始载荷设`-text`并核Git blob不归一化。
5. 输出确切包路径、完整白名单文件路径及payload数；明确process仍活动、没有终态日志或stop复制、没有rsizeonly，交root统一checkpoint。

## 已对齐的稳定报告白名单

acceptance_analysis 已确认以下28 JSON原件稳定，保留原版v1/v2而不覆盖；完整文件级路径及hash将在包内 `selection.json` 中展开：

- 11观察：`rc4-{m031load,m031sync,m031reload,mpaidload,mpaidsync,mpaidreload,rdesignsync,rdesignreload,rnamesync,rnameload,rfleetsync}-observation-v1.json`。
- 17分析／case：`rc4-m031-native-health-raw-source-v1.json`、`rc4-m031-old-before-to-load-report-v1.json`、`rc4-m031-reload-persistence-raw-source-v1.json`、`rc4-public031-fraction-migration-sync-case-v1.json`、`rc4-public031-fraction-migration-sync-check-v1.json`、`rc4-public031-fraction-migration-complete-case-v1.json`、`rc4-public031-fraction-migration-complete-check-v1.json`、`rc4-public031-fraction-migration-series-report-v1.json`、`rc4-paid-fraction-migration-complete-case-v1.json`、`rc4-paid-fraction-migration-complete-check-v1.json`、`rc4-paid-fraction-migration-series-report-v1.json`、`rc4-mpaid-reload-persistence-raw-source-v1.json`、`rc4-design-registration-probe-report-v1.json`、`rc4-design-name-binding-probe-report-v1.json`、`rc4-design-name-binding-probe-report-v2.json`、`rc4-fleet-scope-design-probe-report-v1.json`、`rc4-mobile-starbase-design-pointer-source-v1.json`。

不复制其 `rc4-migration-unset-variable-log-observation-v1` 子目录或活动 logs；既有该问题分析仅作项目canonical引用，不并入这28 JSON。design-name v1的literal alias判断缺陷与v2仅更正10语引用解析的历史同时保留，六项native设计FAIL不变；不放宽原fraction门槛。

## 执行结果与完整白名单

已建立 [phase-B raw checkpoint v1](evidence/1019-rc4-phase-b-migration-checkpoint-v1/README.md)，完整逐文件白名单见 [selection.json](evidence/1019-rc4-phase-b-migration-checkpoint-v1/selection.json)，包含所有462个原始绝对路径及包内目标、bytes、SHA256。payload共462文件、28,649,242字节：run/427（含11SAV），analysis/28，三根元数据／imports，source_snapshot/3小型原始证明，runtime-input/1。未复制活动logs／stop／rsizeonly，也没有最终进程冻结。

[index.json](evidence/1019-rc4-phase-b-migration-checkpoint-v1/index.json) SHA256 `772e1c775525dd27af475c532dad96674c3f2ba8c167020595cfc7829e944ed0`；[verify.json](evidence/1019-rc4-phase-b-migration-checkpoint-v1/verify.json) 重读462原件／副本、9canonical引用、59原Mod文件引用、11原生SAV及receipt／audit／observer／gamestate、四导入alias、86图OCR绑定，全字节／来源通过，另核462Git原始blob无归一化。旧source canonical复用，没有重复巨量旧run或Mod归档。

全部28报告保持10 FAIL／15 OBSERVATION_ONLY／2 OBSERVED_WITH_FAILURES／1 OBSERVED_SYNC_RELOAD_PENDING。迁移的fraction与reload snapshot失败，以及注册／名字／fleet scope实现设计不一致均原样保留；未把数据完整性通过表述为迁移或整Mod通过。启动NOT_READY失败也保留。归档文件稳定后停止写，root统一提交；本线程未操作UI／改工具或生产。
