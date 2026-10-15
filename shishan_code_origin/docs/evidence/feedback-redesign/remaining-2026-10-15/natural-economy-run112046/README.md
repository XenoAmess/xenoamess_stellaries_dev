# 原自然F01经济窗口：INVALID原件

run20261015T112046Z，主任务于2026-10-15 19:29:59正常停止，forced=false/running_after=false。使用简中4.5.2、debug/gamestatetimer及旧经济104文件组合包：正式90文件逐SHA未改，加原foreign/economy测试14文件，不是纯正式包，也没有legacy-anomaly探针。原始[manifest](manifest.json)、[停止记录](stop.json)、[实际dlc_load](userdir-dlc_load.json)、[设置快照](userdir-settings.txt)均保留。

原方案窗口结论为**INVALID**，完整七支经济矩阵为**NOT RUN**，即时人口P/加权分子W严格检查为**FAIL**。仅核心输入守卫为PASS，不能把该局部结果改成经济通过。这里归档的是旧规则实际三档及其失败边界，不用后来修订的就业审计规则或新v2稳定度夹具重写原结果。

## 三份真实原生存档

| 阶段 | 原生日期 | SAV / 原始来源meta | SAV SHA-256 |
| --- | --- | --- | --- |
| common | 2210.02.02 | [原SAV](econ104_common_0202.sav) / [原生来源记录](econ104_common_0202.native-save.json) | b0dce89057b0082b588e5030bc8c6b8c8283c7017dc65fa08716e00de173def2 |
| F01 warm | 2210.03.02 | [原SAV](econ104_F01_warm.sav) / [原生来源记录](econ104_F01_warm.native-save.json) | 5602fd4c1f3ceba20439d72d26eb43a5c451fb46f8ebdb5cec7ed1f904c34095 |
| F01 measured | 2210.04.02 | [原SAV](econ104_F01_measured.sav) / [原生来源记录](econ104_F01_measured.native-save.json) | 0eed7c29c739d5b9cf762677700561da72fb05e2ec9c15ddf64f09d12aab6dd2 |

[只读归档完整性核对](independent-natural-economy-archive-integrity.json)确认三份_runtime副本与各自原生userdir文件逐byte一致、ZIP恰含meta/gamestate、meta原文与来源记录完全相同、两处日期相等、gamestate长度匹配。37张原图与37份OCR的SHA、实际图像尺寸全部匹配。该报告的完整性PASS仅说明证据未错配，不改变经济INVALID或严格P/W FAIL。

本轮由真实console `fast_forward 64`准备共同基线，再分别`fast_forward 30`暖月和测量月，命令/输入/确认/保存/等待动作均保留；这是披露受控时间推进的经济试跑，不是从2200开始的纯自然新局路线。

## 原审计与独立漂移

[原规则独立窗口审计](independent-natural-F01-window-audit.json)冻结SHA `80dd96ca6d7efbff442e2f50c65e72157b2e6a94d4b4a2e5f96efa705198af2e`；[共同基线precheck](independent-econ104-common-baseline-precheck.json)冻结SHA `f78ea2d20eafc986093be32a225d789df8dc38d16233de45c028557c243e7c43`。前者仅有F01，F00/F10/F11/FP/FN/FH六支缺席，没有完整矩阵算术验收。

| 阶段 | 实际P/W | 已存缓存P/W | 实际U | 稳定度 |
| --- | --- | --- | --- | --- |
| common | 5491 / 38437 | 5485 / 38395 | 7 | 72.6918 |
| warm | 5497 / 38479 | 5491 / 38437 | 7 | 72.7026 |
| measured | 5503 / 38521 | 5497 / 38479 | 7 | 72.714 |

每月普通civilian实际就业2390→2396→2402；被测维护员真实100、bonus10，原版biologist真实60、bonus6及相应容量/auto均稳定。旧完整就业签名因此不满足不变要求；暖月到测量月稳定度还独立增加0.0114，大于原epsilon0.0001，足以使窗口INVALID。U/T/B保持不等于全经济上下文保持，不能用后续放宽无关就业的设计抹掉这次稳定度漂移或严格缓存FAIL。

run内既有before/after就业修订源码、测试快照与后续开发报告作为**工具开发来源**保原，未执行这些副本、未加入Mod，也不把开发测试PASS当本窗口native经济PASS。它们的最终名称/哈希以本目录清单为准；原两个经济报告字节及旧工具依据保持不变。

最终另存[修订就业/载体观测边界后的必要条件核对](independent-natural-F01-final-boundary-context-check.json)，SHA `f25519688b36515e69573feb8e1f16ffffd9af5e73527b794411276e2db501ed`：被测类别就业字段和语义分配保持，普通civilian增长不再误判为被测就业漂移；稳定度仍超原epsilon，结论依然INVALID、严格P/W FAIL、矩阵NOT RUN，不把civilian自然增长归因于架构。旧80dd报告保持原字节，未用修订报告覆盖。

[已执行的32项开发测试报告](independent-employment-carrier-development-tests.json)SHA `6cb339751be1cecb669ad15ab8cb05a6001017249ca48b2f4999b1ef3a8258d4`，与旧31项中间版和更早23项分开。最终[来源快照](additive-runtime-matrix-employment-carrier-revision.py)SHA `d6948a5d874b6684912df3e53f69bb3db5e65b925956b5a9068733d0da152787`及[测试快照](additive-runtime-matrix-tests-employment-carrier-revision.py)SHA `bd5beb7b10315e62b7ee762eb68ef84ed248a3f9d9d94e8bda2afdf2da7896e2`原样归档，仅供开发provenance，不作为新的native经济结果。当前目录同时保留before/after/final六个既有源码/测试副本，未执行它们。

## warm等待守卫误判：12帧全部保留

主任务报告warm等待守卫在已推进后仍未接受暂停状态，产生0–11共12帧；主任务实际查看wait7后关闭console继续原生保存，没有重发warm命令。归档者独立直接看wait7，console显示“Fast Forwarded 64 Days”和一次“Fast Forwarded 30 Days”，右上2210.03.02/暂停及底部暂停横幅清楚；该帧OCR也包含03.02与两处暂停。保留误判记录，不能拿等待守卫拒绝当成Mod没有执行推进或补一次推进。

| 帧 | 原图 | 原始OCR |
| --- | --- | --- |
| 0 | [wait0](econ104_F01_warm-wait-0.jpg) | [OCR0](econ104_F01_warm-wait-0.ocr.json) |
| 1 | [wait1](econ104_F01_warm-wait-1.jpg) | [OCR1](econ104_F01_warm-wait-1.ocr.json) |
| 2 | [wait2](econ104_F01_warm-wait-2.jpg) | [OCR2](econ104_F01_warm-wait-2.ocr.json) |
| 3 | [wait3](econ104_F01_warm-wait-3.jpg) | [OCR3](econ104_F01_warm-wait-3.ocr.json) |
| 4 | [wait4](econ104_F01_warm-wait-4.jpg) | [OCR4](econ104_F01_warm-wait-4.ocr.json) |
| 5 | [wait5](econ104_F01_warm-wait-5.jpg) | [OCR5](econ104_F01_warm-wait-5.ocr.json) |
| 6 | [wait6](econ104_F01_warm-wait-6.jpg) | [OCR6](econ104_F01_warm-wait-6.ocr.json) |
| 7 | [wait7](econ104_F01_warm-wait-7.jpg) | [OCR7](econ104_F01_warm-wait-7.ocr.json) |
| 8 | [wait8](econ104_F01_warm-wait-8.jpg) | [OCR8](econ104_F01_warm-wait-8.ocr.json) |
| 9 | [wait9](econ104_F01_warm-wait-9.jpg) | [OCR9](econ104_F01_warm-wait-9.ocr.json) |
| 10 | [wait10](econ104_F01_warm-wait-10.jpg) | [OCR10](econ104_F01_warm-wait-10.ocr.json) |
| 11 | [wait11](econ104_F01_warm-wait-11.jpg) | [OCR11](econ104_F01_warm-wait-11.ocr.json) |

[原warm命令记录](econ104_F01_warm-advance.console.json)、[原enter动作](econ104_F01_warm-advance-enter.action.json)、[目视确认后的关闭动作](econ104_F01_warm-close-console-after-visual-confirmation.action.json)及各保存动作一并保原。本次只核证据和披露误判，不修订OCR守卫或声称它已稳定。

## 日志及归档完整性

[原始error.log](error.log)21行均为已有未启用Workshop目录descriptor提示，game_text/script及其它新增0；不删原21行。测试INVALID、严格P/W FAIL来自存档/窗口对照，与“本次error.log无新增脚本错误”是不同结论。

[完整停机logs.zip](logs.zip)保留20个原始日志，逐entry校验bytes/SHA，包含原gamestatetimer日志；programmatic单独的timer取证目录没有访问或修改。[原件清单](archive-manifest.json)记录199个选定顶层原件（包括JSON/JPG/console/native-save/action、3SAV、六个既有源码/测试副本、完整日志及设置快照）的来源哈希；[本目录文件哈希清单](file-manifest.json)另覆盖本索引和原件清单，自身不递归自哈希。原始JSON里的来源路径作为不可改provenance保留，新导航引用均为本仓库相对路径。

所有原SAV/图/OCR/日志/旧审计均保字节，没有修改生产、当前run指针、原输入或共享发布文档；没有操作GUI/启停游戏/提交推送。已等待工具开发终稿并核对冻结SHA后封口，旧自然窗口结论保持INVALID、全矩阵NOT RUN。
