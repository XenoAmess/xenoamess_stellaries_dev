# RC4 phase-B 迁移探针原始检查点 v1

完整文件白名单为 [selection.json](selection.json)：逐项给出全部462个原始绝对来源路径、包内目标路径、bytes与SHA256。原字节索引 [index.json](index.json) SHA256 为 `772e1c775525dd27af475c532dad96674c3f2ba8c167020595cfc7829e944ed0`；白名单 SHA256 为 `f3fce0177fae144dcb03892e9888d2c43478320882d2d5a42dfe132413010f0c`。

本包462原文件、28,649,242字节，分为：

| 目标路径范围 | 数量／内容 |
| --- | --- |
| `run/` | 427文件，含11原生SAV及各自UI／OCR／动作／load／native-save／audit，phaseb启动失败／重试和截止时间前的press回执。 |
| `analysis/` | 28稳定JSON：11observer与17raw-source／case／check／probe报告，完整路径均在白名单。 |
| 根目录3原件 | `candidate-phase-b-imports.json`、`manifest.json`、`process.json`。 |
| `source_snapshot/` | 原始`source-copy.json`、`gate.json`、`open-kaishek.json`三件；59文件Mod树完整路径／hash引用既有v3 canonical，未重复拷贝。 |
| `runtime-input/` | 本run实际`user_empire_designs_v3.4.txt`，修复候选hash4ce9。 |

十一份原生SAV精确为 `run/m031load.sav`、`m031sync.sav`、`m031reload.sav`、`mpaidload.sav`、`mpaidsync.sav`、`mpaidreload.sav`、`rdesignsync.sav`、`rdesignreload.sav`、`rnamesync.sav`、`rnameload.sav`、`rfleetsync.sav`（均在run/）。对应observer、receipt、audit及gamestate hash已独立交叉核对，不能用observer替代原始SAV。

run `20261019T133314Z`／PID36912 在检查点时仍运行。UI动作截止为 rfleetsync-close-menu 的 UTC `2026-10-19T14:07:39.920141+00:00`；无前缀press仅收该时间以前。**没有读取或复制活动logs、stop或rsizeonly，没有最终整run冻结。** 已有unset-variable日志分析只作项目canonical引用，相关live-log子目录不在载荷内。`phaseb-startup-failure-2.json` 的NOT_READY/F12未产新图失败完整保留，没有用成功重试覆盖。

旧输入引用已提交 `../1019-legacy-damage-run-final/` canonical：p031before／ppaidbefore分别以mig031src／migpaidsrc原字节导入；原paid队列j13ten源0.3.0-rc.1、施伤before在public0.3.1、本检查点为RC4，版本来源不合并。完整导入receipt包含另两个restart/cancel输入，四组alias都核对原件与副本SHA；仅有导入不等于这些其它case已执行。旧巨量UI／Mod包未重复复制。

28报告状态原样为10 FAIL、15 OBSERVATION_ONLY、2 OBSERVED_WITH_FAILURES、1 OBSERVED_SYNC_RELOAD_PENDING。public与paid的完整迁移检查均保留`damage_preserved_in_declared_mode`及`reload_migration_snapshot_preserved`失败。注册／名称绑定报告保留真实设计重载、六核心和实现指针失败，fleet-scope报告保留ship／mobile-starbase设计不一致。name v1的literal alias判断缺陷与v2只更正10语引用解析的历史同时保留，六项native设计FAIL不变，原fraction门槛未放宽。**这是明确含失败的原始证据检查点，迁移／发布未完成。**

[verify.json](verify.json) 独立重读全部462原件／副本、9canonical引用、59 canonical Mod源文件、11组SAV／receipt／audit／observer／gamestate、4导入别名与86图／OCR绑定，结果`PASS_BYTE_SOURCE_BINDING_ONLY`。Git原字节检查另见`git-byte-verify.json`，462载荷均`-text`且过滤前后blob一致。这个PASS只针对字节／来源，不升级任何失败功能报告。

只做离线文件归档，无UI／游戏／Steam操作，无工具／生产Mod／SAV修改或提交；由root统一checkpoint。
